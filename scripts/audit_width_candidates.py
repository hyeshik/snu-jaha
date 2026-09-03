#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

from build_width_candidates import CANDIDATES


LATIN_SAMPLE = "HAMBURGEFONTSminimumoxygenResearch"
MIXED_SAMPLE = (
    "환경 반응을 분석한 Research dataset에서 minimum oxygen concentration은 "
    "18.4 µmol/L였으며 recovery time은 6.3 h로 측정되었다."
)
IDENTITY_SAMPLE = "환경자하연글꼴0123456789"
BOUNDS_SAMPLE = "HxmngopMW"


def font_name(font: TTFont, name_id: int) -> str:
    for record in font["name"].names:
        if record.nameID == name_id:
            try:
                return record.toUnicode()
            except UnicodeDecodeError:
                continue
    return ""


def text_advance(font: TTFont, text: str) -> int:
    cmap = font.getBestCmap()
    metrics = font["hmtx"].metrics
    return sum(metrics[cmap[ord(character)]][0] for character in text)


def glyph_bounds(glyph_set, glyph_name: str) -> list[float] | None:
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    if pen.bounds is None:
        return None
    return [round(value, 3) for value in pen.bounds]


def coverage(font: TTFont, text: str) -> float:
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    total_area = 0.0
    for character in text:
        pen = AreaPen(glyph_set)
        glyph_set[cmap[ord(character)]].draw(pen)
        total_area += abs(pen.value)
    denominator = text_advance(font, text) * font["head"].unitsPerEm
    return total_area / denominator


def glyph_record(font: TTFont, character: str) -> tuple[tuple, tuple[int, int]]:
    cmap = font.getBestCmap()
    glyph_name = cmap[ord(character)]
    pen = RecordingPen()
    font.getGlyphSet()[glyph_name].draw(pen)
    return tuple(pen.value), font["hmtx"][glyph_name]


def identity_mismatches(reference: TTFont, candidate: TTFont) -> list[str]:
    return [
        character
        for character in IDENTITY_SAMPLE
        if glyph_record(reference, character) != glyph_record(candidate, character)
    ]


def structural_errors(font: TTFont, expected_family: str) -> list[str]:
    errors = []
    if font_name(font, 1) != expected_family:
        errors.append(f"family is {font_name(font, 1)!r}")
    if "CFF " not in font or "glyf" in font:
        errors.append("outlines are not CFF")
    if font["head"].unitsPerEm != 1000:
        errors.append(f"UPM is {font['head'].unitsPerEm}")
    if font["OS/2"].usWeightClass != 400:
        errors.append(f"weight class is {font['OS/2'].usWeightClass}")
    cmap = font.getBestCmap()
    hangul_count = sum(0xAC00 <= codepoint <= 0xD7A3 for codepoint in cmap)
    if hangul_count != 11172:
        errors.append(f"modern Hangul coverage is {hangul_count}")
    for character in "0123456789":
        glyph_name = cmap[ord(character)]
        if font["hmtx"][glyph_name][0] != 520:
            errors.append(f"figure {character} is not 520 units wide")
    return errors


def measure(path: Path) -> dict[str, object]:
    font = TTFont(path, recalcTimestamp=False)
    try:
        cmap = font.getBestCmap()
        metrics = font["hmtx"].metrics
        glyph_set = font.getGlyphSet()
        glyphs = {}
        for character in BOUNDS_SAMPLE:
            glyph_name = cmap[ord(character)]
            glyphs[character] = {
                "advance": metrics[glyph_name][0],
                "bounds": glyph_bounds(glyph_set, glyph_name),
            }
        return {
            "path": str(path),
            "family": font_name(font, 1),
            "latin_advance": text_advance(font, LATIN_SAMPLE),
            "mixed_advance": text_advance(font, MIXED_SAMPLE),
            "latin_coverage": round(coverage(font, LATIN_SAMPLE), 7),
            "glyphs": glyphs,
        }
    finally:
        font.close()


def audit(
    current_path: Path,
    ridibatang_path: Path,
    candidate_dir: Path,
    output: Path,
) -> None:
    current = measure(current_path)
    ridibatang = measure(ridibatang_path)
    current_font = TTFont(current_path, recalcTimestamp=False)
    try:
        candidates = []
        for spec in CANDIDATES:
            path = candidate_dir / f"{spec.stem}.otf"
            measured = measure(path)
            candidate_font = TTFont(path, recalcTimestamp=False)
            try:
                mismatches = identity_mismatches(current_font, candidate_font)
                errors = structural_errors(candidate_font, spec.family_name)
            finally:
                candidate_font.close()
            if mismatches:
                errors.append(
                    "changed Hangul or figures: " + "".join(mismatches)
                )
            if errors:
                raise SystemExit(f"{path}: " + "; ".join(errors))
            measured.update(
                {
                    "key": spec.key,
                    "width_axis": spec.width,
                    "x_scale": spec.x_scale,
                    "latin_advance_ratio": round(
                        measured["latin_advance"] / current["latin_advance"],
                        7,
                    ),
                    "mixed_advance_ratio": round(
                        measured["mixed_advance"] / current["mixed_advance"],
                        7,
                    ),
                    "identity_mismatches": mismatches,
                    "validation_errors": errors,
                }
            )
            candidates.append(measured)
    finally:
        current_font.close()

    report = {
        "latin_sample": LATIN_SAMPLE,
        "mixed_sample": MIXED_SAMPLE,
        "identity_sample": IDENTITY_SAMPLE,
        "current": current,
        "ridibatang": ridibatang,
        "candidates": candidates,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure SNU Jaha Regular width candidates."
    )
    parser.add_argument("--current", required=True)
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    audit(
        Path(args.current),
        Path(args.ridibatang),
        Path(args.candidate_dir),
        Path(args.output),
    )


if __name__ == "__main__":
    main()
