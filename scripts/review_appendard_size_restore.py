#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

from build_appendard_fit_candidates import Fit, transform_font
from measure_hangul_latin_balance import CAP_SAMPLE, glyph_metrics


MODERN_HANGUL = range(0xAC00, 0xD7A4)
STRATEGIES = (
    ("keep-center", "Keep Center"),
    ("keep-shift", "Keep Shift"),
    ("keep-bottom", "Keep Bottom"),
)
JAHA_SAFE_Y_SCALE = 0.984


@dataclass(frozen=True)
class Family:
    label: str
    prefix: str
    input_path: Path


def percentile_summary(values: list[float]) -> dict[str, float]:
    return {
        label: float(np.percentile(values, percentile))
        for label, percentile in (
            ("min", 0),
            ("p01", 1),
            ("median", 50),
            ("p99", 99),
            ("max", 100),
        )
    }


def modern_hangul_bounds(font: TTFont) -> list[tuple[int, tuple[float, ...]]]:
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    rows = []
    for codepoint in MODERN_HANGUL:
        glyph_name = cmap.get(codepoint)
        if glyph_name is None:
            continue
        pen = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(pen)
        if pen.bounds is not None:
            rows.append((codepoint, tuple(float(value) for value in pen.bounds)))
    return rows


def audit_font(path: Path) -> dict[str, object]:
    font = TTFont(path)
    try:
        rows = modern_hangul_bounds(font)
        y_mins = [bounds[1] for _, bounds in rows]
        y_maxs = [bounds[3] for _, bounds in rows]
        heights = [bounds[3] - bounds[1] for _, bounds in rows]
        os2 = font["OS/2"]
        cap_rows = [glyph_metrics(font, character) for character in CAP_SAMPLE]
        cap_top = float(np.median([row["y_max"] for row in cap_rows]))
        g_bottom = glyph_metrics(font, "g")["y_min"]
        median_y_min = float(np.median(y_mins))
        median_y_max = float(np.median(y_maxs))
        return {
            "path": str(path),
            "modern_hangul": len(rows),
            "head": {
                "y_min": font["head"].yMin,
                "y_max": font["head"].yMax,
            },
            "line_metrics": {
                "typo_descender": os2.sTypoDescender,
                "typo_ascender": os2.sTypoAscender,
                "win_descender": -os2.usWinDescent,
                "win_ascender": os2.usWinAscent,
            },
            "hangul_y_min": percentile_summary(y_mins),
            "hangul_y_max": percentile_summary(y_maxs),
            "hangul_height": percentile_summary(heights),
            "median_positions": {
                "top_minus_cap_top": median_y_max - cap_top,
                "bottom_minus_g_bottom": median_y_min - g_bottom,
            },
            "metric_overflow": {
                "above_typo_ascender": sum(
                    value > os2.sTypoAscender for value in y_maxs
                ),
                "below_typo_descender": sum(
                    value < os2.sTypoDescender for value in y_mins
                ),
                "above_win_ascender": sum(
                    value > os2.usWinAscent for value in y_maxs
                ),
                "below_win_descender": sum(
                    value < -os2.usWinDescent for value in y_mins
                ),
            },
        }
    finally:
        font.close()


def anchor_shift(
    strategy: str,
    before: dict[str, float],
    selected_fit: Fit,
) -> float:
    if strategy == "keep-shift":
        return selected_fit.y_shift
    if strategy == "keep-center":
        anchor = (before["y_min"] + before["y_max"]) / 2
    elif strategy == "keep-bottom":
        anchor = before["y_min"]
    else:
        raise ValueError(f"unknown strategy: {strategy}")
    transformed_anchor = selected_fit.y_scale * anchor + selected_fit.y_shift
    return transformed_anchor - anchor


def recommended_fit(label: str, selected_fit: Fit) -> Fit:
    return Fit(
        x_scale=1,
        y_scale=JAHA_SAFE_Y_SCALE if label == "SNU Jaha" else 1,
        x_shift=0,
        y_shift=selected_fit.y_shift,
        advance_scale=1,
        common_syllables=selected_fit.common_syllables,
    )


def build_family(
    family: Family,
    family_report: dict[str, object],
    candidate_dir: Path,
    output_dir: Path,
) -> dict[str, object]:
    selected = next(
        blend for blend in family_report["blends"] if blend["ratio"] == "2:1"
    )
    selected_fit = Fit(**selected["fit"])
    before = family_report["before"]
    states = {
        "original": {
            "fit": asdict(Fit(1, 1, 0, 0, 1, selected_fit.common_syllables)),
            "audit": audit_font(family.input_path),
        },
        "selected-2-to-1": {
            "fit": asdict(selected_fit),
            "audit": audit_font(candidate_dir / Path(selected["output"]).name),
        },
    }
    recommended = recommended_fit(family.label, selected_fit)
    recommended_family = f"{family.label} 2to1 Optical Restore"
    recommended_postscript = f"{family.prefix}2to1OpticalRestore-Regular"
    recommended_output = (
        output_dir / f"{family.prefix}2to1-OpticalRestore-Regular.otf"
    )
    recommended_glyphs = transform_font(
        family.input_path,
        recommended_output,
        recommended_family,
        recommended_postscript,
        recommended,
    )
    states["recommended"] = {
        "candidate_family": recommended_family,
        "output": str(recommended_output),
        "transformed_glyphs": recommended_glyphs,
        "fit": asdict(recommended),
        "audit": audit_font(recommended_output),
    }
    for slug, display_name in STRATEGIES:
        fit = Fit(
            x_scale=selected_fit.x_scale,
            y_scale=1,
            x_shift=selected_fit.x_shift,
            y_shift=anchor_shift(slug, before, selected_fit),
            advance_scale=selected_fit.advance_scale,
            common_syllables=selected_fit.common_syllables,
        )
        compact_slug = "".join(part.title() for part in slug.split("-"))
        candidate_family = f"{family.label} 2to1 Y Restore {display_name}"
        candidate_postscript = (
            f"{family.prefix}2to1YRestore{compact_slug}-Regular"
        )
        output_path = (
            output_dir
            / f"{family.prefix}2to1-YRestore-{compact_slug}-Regular.otf"
        )
        transformed_glyphs = transform_font(
            family.input_path,
            output_path,
            candidate_family,
            candidate_postscript,
            fit,
        )
        states[slug] = {
            "candidate_family": candidate_family,
            "output": str(output_path),
            "transformed_glyphs": transformed_glyphs,
            "fit": asdict(fit),
            "audit": audit_font(output_path),
        }
    return {
        "label": family.label,
        "prefix": family.prefix,
        "input": str(family.input_path),
        "states": states,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build and audit disposable vertical-size restoration variants "
            "around the selected Original:Appendard 2:1 fit."
        )
    )
    parser.add_argument("--jaha", required=True)
    parser.add_argument("--edge", required=True)
    parser.add_argument("--blend-report", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    blend_report = json.loads(Path(args.blend_report).read_text(encoding="utf-8"))
    report_families = {
        item["label"]: item for item in blend_report["families"]
    }
    families = (
        Family("SNU Jaha", "SNUJaha", Path(args.jaha)),
        Family("SNU Edge", "SNUEdge", Path(args.edge)),
    )
    output_dir = Path(args.output_dir)
    results = [
        build_family(
            family,
            report_families[family.label],
            Path(args.candidate_dir),
            output_dir,
        )
        for family in families
    ]
    report = {
        "selected_ratio": "Original:Appendard 2:1",
        "restoration": (
            "compare the recommended optical restore with three full "
            "vertical-scale restoration anchors"
        ),
        "strategies": ["recommended", *(slug for slug, _ in STRATEGIES)],
        "families": results,
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{report_path}: families={len(results)}, candidates={len(results) * 4}")


if __name__ == "__main__":
    main()
