#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


MODERN_HANGUL = range(0xAC00, 0xD7A4)
CAP_SAMPLE = "HIMNO"
X_HEIGHT_SAMPLE = "aceimnorsuvwxz"
LATIN_SIZE_SAMPLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
LATIN_BODY_SAMPLE = "HgxM"
REFERENCE_GLYPHS = "HMxg"


@dataclass(frozen=True)
class Family:
    label: str
    source_name: str
    source_path: Path
    family_path: Path
    adjusted_path: Path


def glyph_metrics(font: TTFont, character: str) -> dict[str, float]:
    glyph_name = font.getBestCmap()[ord(character)]
    pen = BoundsPen(font.getGlyphSet())
    font.getGlyphSet()[glyph_name].draw(pen)
    if pen.bounds is None:
        raise ValueError(f"empty outline: {character} / {glyph_name}")
    scale = 1000 / font["head"].unitsPerEm
    x_min, y_min, x_max, y_max = (value * scale for value in pen.bounds)
    advance = font["hmtx"][glyph_name][0] * scale
    return {
        "x_min": float(x_min),
        "y_min": float(y_min),
        "x_max": float(x_max),
        "y_max": float(y_max),
        "width": float(x_max - x_min),
        "height": float(y_max - y_min),
        "advance": float(advance),
    }


def median_metrics(rows: list[dict[str, float]]) -> dict[str, float]:
    return {
        key: float(np.median([row[key] for row in rows]))
        for key in rows[0]
    }


def shared_hangul(paths: tuple[Path, ...]) -> list[int]:
    cmaps = []
    for path in paths:
        font = TTFont(path, lazy=True)
        try:
            cmaps.append(font.getBestCmap())
        finally:
            font.close()
    return [
        codepoint
        for codepoint in MODERN_HANGUL
        if all(codepoint in cmap for cmap in cmaps)
    ]


def summarize_font(path: Path, hangul_codepoints: list[int]) -> dict[str, object]:
    font = TTFont(path)
    try:
        cmap = font.getBestCmap()
        hangul_rows = [
            glyph_metrics(font, chr(codepoint))
            for codepoint in hangul_codepoints
            if codepoint in cmap
        ]
        cap_rows = [glyph_metrics(font, character) for character in CAP_SAMPLE]
        x_height_rows = [
            glyph_metrics(font, character) for character in X_HEIGHT_SAMPLE
        ]
        latin_rows = [
            glyph_metrics(font, character) for character in LATIN_SIZE_SAMPLE
        ]
        body_rows = [
            glyph_metrics(font, character) for character in LATIN_BODY_SAMPLE
        ]
        references = {
            character: glyph_metrics(font, character)
            for character in REFERENCE_GLYPHS
        }
        hangul = median_metrics(hangul_rows)
        cap = median_metrics(cap_rows)
        x_height = median_metrics(x_height_rows)
        latin = median_metrics(latin_rows)
        body_y_min = min(row["y_min"] for row in body_rows)
        body_y_max = max(row["y_max"] for row in body_rows)
        latin_body_span = body_y_max - body_y_min
        return {
            "path": str(path),
            "units_per_em": font["head"].unitsPerEm,
            "hangul": hangul,
            "latin_cap": cap,
            "latin_x_height": x_height,
            "latin_alphabet": latin,
            "latin_body": {
                "sample": LATIN_BODY_SAMPLE,
                "y_min": body_y_min,
                "y_max": body_y_max,
                "height": latin_body_span,
            },
            "ratios": {
                "hangul_height_to_cap": hangul["height"] / cap["height"],
                "hangul_height_to_x_height": (
                    hangul["height"] / x_height["height"]
                ),
                "hangul_height_to_latin_body": (
                    hangul["height"] / latin_body_span
                ),
                "hangul_width_to_latin_width": (
                    hangul["width"] / latin["width"]
                ),
                "hangul_advance_to_latin_advance": (
                    hangul["advance"] / latin["advance"]
                ),
            },
            "positions_per_1000_em": {
                "hangul_top_minus_cap_top": hangul["y_max"] - cap["y_max"],
                "hangul_bottom_minus_g_bottom": (
                    hangul["y_min"] - references["g"]["y_min"]
                ),
            },
            "reference_glyphs": references,
        }
    finally:
        font.close()


def ratio_delta(
    before: dict[str, object], after: dict[str, object]
) -> dict[str, dict[str, float]]:
    before_ratios = before["ratios"]
    after_ratios = after["ratios"]
    assert isinstance(before_ratios, dict)
    assert isinstance(after_ratios, dict)
    return {
        key: {
            "before": float(before_ratios[key]),
            "after": float(after_ratios[key]),
            "relative_change": float(after_ratios[key] / before_ratios[key] - 1),
            "percentage_point_change": float(
                100 * (after_ratios[key] - before_ratios[key])
            ),
        }
        for key in before_ratios
    }


def audit_family(family: Family) -> dict[str, object]:
    paths = (family.source_path, family.family_path, family.adjusted_path)
    hangul_codepoints = shared_hangul(paths)
    if len(hangul_codepoints) < 1000:
        raise ValueError(
            f"{family.label}: too few shared Hangul syllables: "
            f"{len(hangul_codepoints)}"
        )
    states = {
        "upstream_source": summarize_font(family.source_path, hangul_codepoints),
        "snu_regular_before": summarize_font(family.family_path, hangul_codepoints),
        "snu_regular_2_to_1": summarize_font(
            family.adjusted_path,
            hangul_codepoints,
        ),
    }
    return {
        "label": family.label,
        "source_name": family.source_name,
        "shared_modern_hangul": len(hangul_codepoints),
        "samples": {
            "cap": CAP_SAMPLE,
            "x_height": X_HEIGHT_SAMPLE,
            "latin_size": LATIN_SIZE_SAMPLE,
            "latin_body": LATIN_BODY_SAMPLE,
            "reference_glyphs": REFERENCE_GLYPHS,
        },
        "states": states,
        "comparisons": {
            "upstream_to_2_to_1": ratio_delta(
                states["upstream_source"],
                states["snu_regular_2_to_1"],
            ),
            "snu_before_to_2_to_1": ratio_delta(
                states["snu_regular_before"],
                states["snu_regular_2_to_1"],
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Measure Hangul-to-Latin size balance before and after the "
            "Original:Appendard 2:1 adjustment."
        )
    )
    parser.add_argument("--jaha-source", required=True)
    parser.add_argument("--jaha", required=True)
    parser.add_argument("--jaha-adjusted", required=True)
    parser.add_argument("--edge-source", required=True)
    parser.add_argument("--edge", required=True)
    parser.add_argument("--edge-adjusted", required=True)
    parser.add_argument("--sprout-source", required=True)
    parser.add_argument("--sprout", required=True)
    parser.add_argument("--sprout-adjusted", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    families = (
        Family(
            "SNU Jaha",
            "RIDIBatang",
            Path(args.jaha_source),
            Path(args.jaha),
            Path(args.jaha_adjusted),
        ),
        Family(
            "SNU Edge",
            "NanumSquare Regular",
            Path(args.edge_source),
            Path(args.edge),
            Path(args.edge_adjusted),
        ),
        Family(
            "SNU Sprout",
            "LINE Seed Sans KR Regular",
            Path(args.sprout_source),
            Path(args.sprout),
            Path(args.sprout_adjusted),
        ),
    )
    report = {
        "ratio": "Original:Appendard 2:1",
        "normalization": "outline coordinates normalized to 1000 units/em",
        "families": [audit_family(family) for family in families],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{output}: families={len(families)}")


if __name__ == "__main__":
    main()
