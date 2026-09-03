#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


MODERN_HANGUL = range(0xAC00, 0xD7A4)
HANGUL_RANGES = (
    range(0x1100, 0x1200),
    range(0x3130, 0x3190),
    range(0xA960, 0xA980),
    range(0xAC00, 0xD7A4),
    range(0xD7B0, 0xD800),
)
BLEND_LEVELS = (
    ("1:2", "O1A2", 2 / 3),
    ("1:1", "O1A1", 1 / 2),
    ("2:1", "O2A1", 1 / 3),
)


@dataclass(frozen=True)
class Fit:
    x_scale: float
    y_scale: float
    x_shift: float
    y_shift: float
    advance_scale: float
    common_syllables: int


@dataclass(frozen=True)
class Source:
    label: str
    input_path: Path
    prefix: str


def is_hangul(codepoint: int) -> bool:
    return any(codepoint in codepoint_range for codepoint_range in HANGUL_RANGES)


def glyph_bounds(glyph_set, glyph_name: str) -> tuple[float, float, float, float]:
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    if pen.bounds is None:
        raise ValueError(f"empty outline: {glyph_name}")
    return tuple(float(value) for value in pen.bounds)


def hangul_rows(font: TTFont, codepoints: list[int]) -> np.ndarray:
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    rows = []
    for codepoint in codepoints:
        glyph_name = cmap[codepoint]
        x_min, y_min, x_max, y_max = glyph_bounds(glyph_set, glyph_name)
        advance = font["hmtx"][glyph_name][0]
        rows.append((x_min, y_min, x_max, y_max, advance))
    return np.asarray(rows, dtype=np.float64)


def fit_to_target(source: TTFont, target: TTFont) -> Fit:
    source_cmap = source.getBestCmap()
    target_cmap = target.getBestCmap()
    common = [
        codepoint
        for codepoint in MODERN_HANGUL
        if codepoint in source_cmap and codepoint in target_cmap
    ]
    if len(common) < 1000:
        raise ValueError(f"too few common modern Hangul syllables: {len(common)}")
    source_rows = hangul_rows(source, common)
    target_rows = hangul_rows(target, common)

    source_widths = source_rows[:, 2] - source_rows[:, 0]
    source_heights = source_rows[:, 3] - source_rows[:, 1]
    target_widths = target_rows[:, 2] - target_rows[:, 0]
    target_heights = target_rows[:, 3] - target_rows[:, 1]
    x_scale = float(np.median(target_widths / source_widths))
    y_scale = float(np.median(target_heights / source_heights))
    advance_scale = float(np.median(target_rows[:, 4] / source_rows[:, 4]))
    x_shift = float(
        (
            np.median(target_rows[:, 0] - x_scale * source_rows[:, 0])
            + np.median(target_rows[:, 2] - x_scale * source_rows[:, 2])
        )
        / 2
    )
    y_shift = float(
        (
            np.median(target_rows[:, 1] - y_scale * source_rows[:, 1])
            + np.median(target_rows[:, 3] - y_scale * source_rows[:, 3])
        )
        / 2
    )
    return Fit(
        x_scale=x_scale,
        y_scale=y_scale,
        x_shift=x_shift,
        y_shift=y_shift,
        advance_scale=advance_scale,
        common_syllables=len(common),
    )


def interpolate_fit(full_fit: Fit, alpha: float) -> Fit:
    if not 0 < alpha < 1:
        raise ValueError(f"blend alpha must be between zero and one: {alpha}")
    return Fit(
        x_scale=1 + alpha * (full_fit.x_scale - 1),
        y_scale=1 + alpha * (full_fit.y_scale - 1),
        x_shift=alpha * full_fit.x_shift,
        y_shift=alpha * full_fit.y_shift,
        advance_scale=1 + alpha * (full_fit.advance_scale - 1),
        common_syllables=full_fit.common_syllables,
    )


def encoded_charstring_width(width: int, private) -> int | None:
    if width == private.defaultWidthX:
        return None
    return width - private.nominalWidthX


def rewrite_names(font: TTFont, family_name: str, postscript_name: str) -> None:
    replacements = {
        1: family_name,
        2: "Regular",
        3: f"1.000;SNU;{postscript_name}",
        4: f"{family_name} Regular",
        6: postscript_name,
        16: family_name,
        17: "Regular",
    }
    name_table = font["name"]
    for record in name_table.names:
        if record.nameID not in replacements:
            continue
        record.string = replacements[record.nameID].encode(
            record.getEncoding(), errors="replace"
        )

    cff = font["CFF "].cff
    top_dict = cff.topDictIndex[0]
    cff.fontNames[0] = postscript_name
    top_dict.FamilyName = family_name
    top_dict.FullName = f"{family_name} Regular"
    top_dict.Weight = "Regular"


def transform_font(
    input_path: Path,
    output_path: Path,
    candidate_family: str,
    candidate_postscript: str,
    fit: Fit,
) -> int:
    font = TTFont(input_path, recalcTimestamp=False)
    try:
        cmap = font.getBestCmap()
        encoded_hangul_names = sorted(
            {
                glyph_name
                for codepoint, glyph_name in cmap.items()
                if is_hangul(codepoint)
            }
        )
        glyph_set = font.getGlyphSet()
        top_dict = font["CFF "].cff.topDictIndex[0]
        private = top_dict.Private
        global_subrs = top_dict.GlobalSubrs

        old_bounds = {}
        for glyph_name in encoded_hangul_names:
            try:
                old_bounds[glyph_name] = glyph_bounds(glyph_set, glyph_name)
            except ValueError:
                continue
        affected_names = sorted(old_bounds)
        old_metrics = {
            glyph_name: font["hmtx"][glyph_name]
            for glyph_name in affected_names
        }
        for glyph_name in affected_names:
            old_advance, old_lsb = old_metrics[glyph_name]
            new_advance = round(old_advance * fit.advance_scale)
            pen = T2CharStringPen(
                encoded_charstring_width(new_advance, private),
                glyphSet=None,
            )
            transformed_pen = TransformPen(
                pen,
                (
                    fit.x_scale,
                    0,
                    0,
                    fit.y_scale,
                    fit.x_shift,
                    fit.y_shift,
                ),
            )
            glyph_set[glyph_name].draw(transformed_pen)
            top_dict.CharStrings[glyph_name] = pen.getCharString(
                private=private,
                globalSubrs=global_subrs,
            )
            font["hmtx"][glyph_name] = (
                new_advance,
                round(fit.x_scale * old_lsb + fit.x_shift),
            )

            if "vmtx" in font:
                advance_height, old_tsb = font["vmtx"][glyph_name]
                old_y_max = old_bounds[glyph_name][3]
                new_y_max = fit.y_scale * old_y_max + fit.y_shift
                vertical_origin = old_tsb + old_y_max
                font["vmtx"][glyph_name] = (
                    advance_height,
                    round(vertical_origin - new_y_max),
                )

        rewrite_names(font, candidate_family, candidate_postscript)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        font.save(output_path, reorderTables=False)
    finally:
        font.close()
    return len(affected_names)


def median_summary(font: TTFont, codepoints: list[int]) -> dict[str, object]:
    rows = hangul_rows(font, codepoints)
    medians = np.median(rows, axis=0)
    return {
        "x_min": float(medians[0]),
        "y_min": float(medians[1]),
        "x_max": float(medians[2]),
        "y_max": float(medians[3]),
        "advance": float(medians[4]),
        "width": float(np.median(rows[:, 2] - rows[:, 0])),
        "height": float(np.median(rows[:, 3] - rows[:, 1])),
    }


def build_source(
    source: Source,
    target_path: Path,
    output_dir: Path,
) -> dict[str, object]:
    input_font = TTFont(source.input_path)
    target_font = TTFont(target_path)
    try:
        full_fit = fit_to_target(input_font, target_font)
        common = [
            codepoint
            for codepoint in MODERN_HANGUL
            if codepoint in input_font.getBestCmap()
            and codepoint in target_font.getBestCmap()
        ]
        before = median_summary(input_font, common)
        target = median_summary(target_font, common)
    finally:
        input_font.close()
        target_font.close()

    blends = []
    for ratio, slug, alpha in BLEND_LEVELS:
        fit = interpolate_fit(full_fit, alpha)
        candidate_family = f"{source.label} Blend {slug}"
        candidate_postscript = f"{source.prefix}Blend{slug}-Regular"
        output_path = output_dir / f"{source.prefix}Blend-{slug}-Regular.otf"
        transformed_glyphs = transform_font(
            source.input_path,
            output_path,
            candidate_family,
            candidate_postscript,
            fit,
        )
        candidate_font = TTFont(output_path)
        try:
            after = median_summary(candidate_font, common)
        finally:
            candidate_font.close()
        blends.append(
            {
                "ratio": ratio,
                "slug": slug,
                "alpha": alpha,
                "output": str(output_path),
                "candidate_family": candidate_family,
                "fit": asdict(fit),
                "transformed_glyphs": transformed_glyphs,
                "after": after,
            }
        )
    full_fit_family = f"{source.label} Appendard Fit"
    full_fit_postscript = f"{source.prefix}AppendardFit-Regular"
    full_fit_output = output_dir / f"{source.prefix}AppendardFit-Regular.otf"
    full_fit_glyphs = transform_font(
        source.input_path,
        full_fit_output,
        full_fit_family,
        full_fit_postscript,
        full_fit,
    )
    full_fit_font = TTFont(full_fit_output)
    try:
        full_fit_after = median_summary(full_fit_font, common)
    finally:
        full_fit_font.close()
    return {
        "label": source.label,
        "input": str(source.input_path),
        "prefix": source.prefix,
        "full_fit": asdict(full_fit),
        "before": before,
        "target": target,
        "blends": blends,
        "full_fit_candidate": {
            "ratio": "0:1",
            "slug": "O0A1",
            "alpha": 1,
            "output": str(full_fit_output),
            "candidate_family": full_fit_family,
            "fit": asdict(full_fit),
            "transformed_glyphs": full_fit_glyphs,
            "after": full_fit_after,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build disposable Regular Hangul candidates interpolated toward "
            "SNU Appendard."
        )
    )
    parser.add_argument("--jaha", required=True)
    parser.add_argument("--edge", required=True)
    parser.add_argument("--sprout", required=True)
    parser.add_argument("--appendard", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    sources = (
        Source(
            "SNU Jaha",
            Path(args.jaha),
            "SNUJaha",
        ),
        Source(
            "SNU Edge",
            Path(args.edge),
            "SNUEdge",
        ),
        Source(
            "SNU Sprout",
            Path(args.sprout),
            "SNUSprout",
        ),
    )
    results = [
        build_source(source, Path(args.appendard), output_dir)
        for source in sources
    ]
    report = {
        "target": str(Path(args.appendard)),
        "target_family": "SNU Appendard",
        "ratio_definition": "original:Appendard",
        "blend_levels": [
            {"ratio": ratio, "slug": slug, "alpha": alpha}
            for ratio, slug, alpha in BLEND_LEVELS
        ],
        "families": results,
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for result in results:
        for blend in result["blends"]:
            fit = blend["fit"]
            print(
                f"{blend['output']}: ratio={blend['ratio']}, "
                f"glyphs={blend['transformed_glyphs']}, "
                f"scale=({fit['x_scale']:.4f},{fit['y_scale']:.4f}), "
                f"shift=({fit['x_shift']:.1f},{fit['y_shift']:.1f}), "
                f"advance={fit['advance_scale']:.4f}"
            )
        full_fit_candidate = result["full_fit_candidate"]
        fit = full_fit_candidate["fit"]
        print(
            f"{full_fit_candidate['output']}: ratio=0:1, "
            f"glyphs={full_fit_candidate['transformed_glyphs']}, "
            f"scale=({fit['x_scale']:.4f},{fit['y_scale']:.4f}), "
            f"shift=({fit['x_shift']:.1f},{fit['y_shift']:.1f}), "
            f"advance={fit['advance_scale']:.4f}"
        )
    print(f"{report_path}: candidates={len(results) * (len(BLEND_LEVELS) + 1)}")


if __name__ == "__main__":
    main()
