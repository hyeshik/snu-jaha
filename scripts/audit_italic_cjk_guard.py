#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

import uharfbuzz as hb
from fontTools.pens.areaPen import AreaPen
from fontTools.ttLib import TTFont

from add_italic_cjk_guard import (
    DEFAULT_BUCKET_SIZE,
    DEFAULT_CLEARANCE,
    collect_geometry_classes,
    glyph_bounds,
    terminal_latin_and_figure_glyphs,
)
from build_jaha import is_hangul_codepoint


STYLES = ("Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold")
RISK_SEQUENCES = (
    "f한",
    "ff한",
    "fi한",
    "fl한",
    "T한",
    "K한",
    "V한",
    "W한",
    "Y한",
    "J한",
    "j한",
    "r한",
    "t한",
    "x한",
    "z한",
    "0한",
    "1한",
    "2한",
    "7한",
    "8한",
)
LATIN_WEIGHT_SAMPLE = "HMAINoxngp"
HANGUL_GEOMETRY_SAMPLE = "환경한글뿳휇흙률"
EXPECTED_ITALIC_FIGURE_ADVANCE = 498


def style_path(font_dir: Path, style: str) -> Path:
    return font_dir / f"SNUJaha-{style}Italic.otf"


def upright_style_path(font_dir: Path, style: str) -> Path:
    return font_dir / f"SNUJaha-{style}.otf"


def guard_x_advance(font: TTFont, left: str, right: str) -> int:
    lookup = font["GPOS"].table.LookupList.Lookup[-1]
    subtable = lookup.SubTable[0]
    if lookup.LookupType != 2 or subtable.Format != 2:
        raise ValueError("The final GPOS lookup is not the italic class guard.")
    if left not in subtable.Coverage.glyphs:
        return 0
    class1 = subtable.ClassDef1.classDefs.get(left, 0)
    class2 = subtable.ClassDef2.classDefs.get(right, 0)
    value = subtable.Class1Record[class1].Class2Record[class2].Value1
    return getattr(value, "XAdvance", 0) if value is not None else 0


def shape(font_data: bytes, text: str):
    face = hb.Face(font_data)
    font = hb.Font(face)
    font.scale = (face.upem, face.upem)
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(font, buffer, {"kern": True, "liga": True})
    return list(zip(buffer.glyph_infos, buffer.glyph_positions))


def shaped_boundary_clearance(
    font: TTFont,
    font_data: bytes,
    text: str,
) -> tuple[float, list[str]]:
    shaped = shape(font_data, text)
    glyph_order = font.getGlyphOrder()
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    hangul_names = {
        glyph_name
        for codepoint, glyph_name in cmap.items()
        if 0xAC00 <= codepoint <= 0xD7A3
    }

    x = 0
    positioned = []
    for info, position in shaped:
        name = glyph_order[info.codepoint]
        bounds = glyph_bounds(glyph_set, name)
        positioned.append((name, bounds, x + position.x_offset))
        x += position.x_advance

    hangul_index = next(
        index for index, (name, _, _) in enumerate(positioned) if name in hangul_names
    )
    if hangul_index == 0:
        raise ValueError(f"{text!r} has no Latin-to-Hangul boundary")
    latin_name, latin_bounds, latin_x = positioned[hangul_index - 1]
    hangul_name, hangul_bounds, hangul_x = positioned[hangul_index]
    if latin_bounds is None or hangul_bounds is None:
        raise ValueError(f"{text!r} contains an empty boundary glyph")
    clearance = (hangul_x + hangul_bounds[0]) - (latin_x + latin_bounds[2])
    return clearance, [name for name, _, _ in positioned]


def glyph_area(font: TTFont, character: str) -> float:
    glyph_set = font.getGlyphSet()
    glyph_name = font.getBestCmap()[ord(character)]
    pen = AreaPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return abs(float(pen.value))


def posture_alignment(font: TTFont, upright: TTFont) -> dict:
    cmap = font.getBestCmap()
    upright_cmap = upright.getBestCmap()
    hangul_codepoints = [
        codepoint for codepoint in cmap if is_hangul_codepoint(codepoint)
    ]
    advance_mismatches = [
        codepoint
        for codepoint in hangul_codepoints
        if font["hmtx"][cmap[codepoint]][0]
        != upright["hmtx"][upright_cmap[codepoint]][0]
    ]

    geometry_mismatches = []
    for character in HANGUL_GEOMETRY_SAMPLE:
        italic_bounds = glyph_bounds(font.getGlyphSet(), cmap[ord(character)])
        upright_bounds = glyph_bounds(
            upright.getGlyphSet(), upright_cmap[ord(character)]
        )
        italic_advance = font["hmtx"][cmap[ord(character)]][0]
        upright_advance = upright["hmtx"][upright_cmap[ord(character)]][0]
        if italic_bounds != upright_bounds or italic_advance != upright_advance:
            geometry_mismatches.append(character)

    figure_advances = {
        character: font["hmtx"][cmap[ord(character)]][0]
        for character in "0123456789"
    }
    if set(figure_advances.values()) != {EXPECTED_ITALIC_FIGURE_ADVANCE}:
        raise ValueError(f"unexpected italic figure advances: {figure_advances}")

    latin_area_ratios = [
        glyph_area(font, character) / glyph_area(upright, character)
        for character in LATIN_WEIGHT_SAMPLE
    ]
    latin_bounds = {
        character: glyph_bounds(font.getGlyphSet(), cmap[ord(character)])
        for character in "Hx"
    }
    upright_latin_bounds = {
        character: glyph_bounds(
            upright.getGlyphSet(), upright_cmap[ord(character)]
        )
        for character in "Hx"
    }
    top_differences = {
        character: latin_bounds[character][3] - upright_latin_bounds[character][3]
        for character in "Hx"
    }
    median_area_ratio = median(latin_area_ratios)

    if advance_mismatches:
        raise ValueError(f"Hangul advance mismatches: {len(advance_mismatches)}")
    if geometry_mismatches:
        raise ValueError(
            "upright Hangul geometry changed in italic: "
            + "".join(geometry_mismatches)
        )
    if any(abs(difference) > 1 for difference in top_differences.values()):
        raise ValueError(f"italic Latin vertical fit changed: {top_differences}")
    if not 0.93 <= median_area_ratio <= 1.05:
        raise ValueError(
            f"italic Latin median area ratio is {median_area_ratio:.3f}"
        )
    return {
        "hangul_advance_mismatches": len(advance_mismatches),
        "upright_hangul_geometry_sample_mismatches": len(geometry_mismatches),
        "italic_figure_advances": figure_advances,
        "latin_top_differences": {
            character: round(value, 3)
            for character, value in top_differences.items()
        },
        "latin_median_area_ratio_to_upright": round(median_area_ratio, 4),
    }


def audit_font(path: Path, upright_path: Path) -> dict:
    font_data = path.read_bytes()
    font = TTFont(path)
    upright = TTFont(upright_path)
    try:
        guarded_classes, hangul_classes = collect_geometry_classes(
            font,
            DEFAULT_BUCKET_SIZE,
        )
        class_clearances = []
        for guarded_key, guarded_glyphs in guarded_classes.items():
            for hangul_key, hangul_glyphs in hangul_classes.items():
                guard = guard_x_advance(
                    font,
                    guarded_glyphs[0],
                    hangul_glyphs[0],
                )
                class_clearances.append(guard + hangul_key - guarded_key)

        samples = {}
        for text in RISK_SEQUENCES:
            clearance, glyphs = shaped_boundary_clearance(font, font_data, text)
            samples[text] = {
                "clearance": round(clearance, 3),
                "glyphs": glyphs,
            }

        minimum_class_clearance = min(class_clearances)
        minimum_sample_clearance = min(
            sample["clearance"] for sample in samples.values()
        )
        if minimum_class_clearance < DEFAULT_CLEARANCE:
            raise ValueError(
                f"{path}: class clearance {minimum_class_clearance:.3f} is below "
                f"{DEFAULT_CLEARANCE}"
            )
        if minimum_sample_clearance < DEFAULT_CLEARANCE:
            raise ValueError(
                f"{path}: shaped clearance {minimum_sample_clearance:.3f} is below "
                f"{DEFAULT_CLEARANCE}"
            )
        return {
            "posture_alignment": posture_alignment(font, upright),
            "terminal_letter_and_figure_glyphs": len(
                terminal_latin_and_figure_glyphs(font)
            ),
            "hangul_glyphs": sum(map(len, hangul_classes.values())),
            "letter_and_figure_geometry_classes": len(guarded_classes),
            "hangul_geometry_classes": len(hangul_classes),
            "minimum_class_clearance": round(minimum_class_clearance, 3),
            "minimum_sample_clearance": round(minimum_sample_clearance, 3),
            "samples": samples,
        }
    finally:
        upright.close()
        font.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit every SNU Jaha italic letter/figure-to-Hangul guard class."
    )
    parser.add_argument("--font-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = {
        "policy": {
            "minimum_clearance": DEFAULT_CLEARANCE,
            "bucket_size": DEFAULT_BUCKET_SIZE,
            "risk_sequences": list(RISK_SEQUENCES),
        },
        "styles": {
            style: audit_font(
                style_path(args.font_dir, style),
                upright_style_path(args.font_dir, style),
            )
            for style in STYLES
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"{args.output}: {len(STYLES)} italic styles; all letter/figure geometry "
        f"classes and "
        f"{len(RISK_SEQUENCES)} shaped risk sequences clear >= "
        f"{DEFAULT_CLEARANCE} units"
    )


if __name__ == "__main__":
    main()
