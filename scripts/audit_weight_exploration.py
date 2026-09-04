#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path
from statistics import median

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from build_weight_exploration_microfonts import (
    AUDIT_CODEPOINTS,
    CJK_CANDIDATES,
    DEFAULT_FIGURES,
    LATIN_CANDIDATES,
    RASTER_PPEM,
    SELECTED_CJK_CONSTRUCTIONS,
    SELECTED_LATIN_CONSTRUCTIONS,
    WEIGHT_TARGETS,
)


LATIN_SENTINELS = "HAMBURGEFONTSminimumoxygenResearch"
TOPOLOGY_PPEMS = (24, 32, 48, 64)


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = round((len(ordered) - 1) * fraction)
    return ordered[index]


def glyph_metrics(font: TTFont, character: str) -> dict[str, object] | None:
    cmap = font.getBestCmap()
    glyph_name = cmap.get(ord(character))
    if glyph_name is None:
        return None
    glyph_set = font.getGlyphSet()
    bounds_pen = BoundsPen(glyph_set)
    area_pen = AreaPen(glyph_set)
    glyph_set[glyph_name].draw(bounds_pen)
    glyph_set[glyph_name].draw(area_pen)
    if bounds_pen.bounds is None:
        return None
    return {
        "advance": font["hmtx"][glyph_name][0],
        "bounds": tuple(float(value) for value in bounds_pen.bounds),
        "area": abs(float(area_pen.value)),
    }


def decoded_family(font: TTFont) -> str:
    names = {
        record.toUnicode()
        for record in font["name"].names
        if record.nameID == 1
    }
    return sorted(names)[0]


def raster_coverage(path: Path, text: str, ppem: int = RASTER_PPEM) -> float:
    font = ImageFont.truetype(str(path), ppem)
    ink = 0
    advance = 0.0
    for character in text:
        ink += int(np.asarray(font.getmask(character, mode="L"), dtype=np.uint8).sum())
        advance += font.getlength(character)
    return ink / (255 * advance * ppem)


@lru_cache(maxsize=None)
def raster_mask(path_text: str, character: str, ppem: int) -> np.ndarray:
    font = ImageFont.truetype(path_text, ppem)
    bounds = font.getbbox(character)
    width = max(1, bounds[2] - bounds[0] + 12)
    height = max(1, bounds[3] - bounds[1] + 12)
    image = Image.new("L", (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((6 - bounds[0], 6 - bounds[1]), character, font=font, fill=255)
    return np.asarray(image) >= 128


def component_sizes(
    pixels: np.ndarray,
    foreground: bool,
    enclosed_only: bool = False,
) -> list[int]:
    targets = pixels if foreground else ~pixels
    visited = np.zeros_like(targets, dtype=bool)
    sizes = []
    for row, column in np.argwhere(targets):
        if visited[row, column]:
            continue
        size = 0
        touches_border = False
        stack = [(int(row), int(column))]
        visited[row, column] = True
        while stack:
            current_row, current_column = stack.pop()
            size += 1
            if (
                current_row in (0, targets.shape[0] - 1)
                or current_column in (0, targets.shape[1] - 1)
            ):
                touches_border = True
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    if row_offset == column_offset == 0:
                        continue
                    next_row = current_row + row_offset
                    next_column = current_column + column_offset
                    if not (
                        0 <= next_row < targets.shape[0]
                        and 0 <= next_column < targets.shape[1]
                    ):
                        continue
                    if (
                        targets[next_row, next_column]
                        and not visited[next_row, next_column]
                    ):
                        visited[next_row, next_column] = True
                        stack.append((next_row, next_column))
        if not enclosed_only or not touches_border:
            sizes.append(size)
    return sorted(sizes, reverse=True)


@lru_cache(maxsize=None)
def raster_topology(path: Path, character: str, ppem: int) -> dict[str, int]:
    pixels = raster_mask(str(path), character, ppem)
    return {
        "foreground": len(component_sizes(pixels, True)),
        "counters": len(component_sizes(pixels, False, enclosed_only=True)),
    }


def sample_vector_coverage(font: TTFont, text: str) -> float:
    metrics = [glyph_metrics(font, character) for character in text]
    present = [item for item in metrics if item is not None]
    return sum(item["area"] for item in present) / (
        sum(item["advance"] for item in present) * font["head"].unitsPerEm
    )


def hangul_pair_spacing(
    font: TTFont,
    characters: list[str],
) -> dict[str, float | int]:
    sidebearings = []
    for character in characters:
        metrics = glyph_metrics(font, character)
        if metrics is None:
            continue
        sidebearings.append(
            (
                metrics["advance"] - metrics["bounds"][2],
                metrics["bounds"][0],
            )
        )
    gaps = [
        right_sidebearing + left_sidebearing
        for right_sidebearing, _ in sidebearings
        for _, left_sidebearing in sidebearings
    ]
    return {
        "minimum": min(gaps),
        "nonpositive_count": sum(gap <= 0 for gap in gaps),
        "pair_count": len(gaps),
    }


def topology_changes(
    regular_path: Path,
    candidate_path: Path,
    characters: list[str],
) -> dict[str, list[dict[str, object]]]:
    result = {
        "foreground_splits": [],
        "foreground_merges": [],
        "counter_gains": [],
        "counter_losses": [],
    }
    for character in characters:
        for ppem in TOPOLOGY_PPEMS:
            regular = raster_topology(regular_path, character, ppem)
            candidate = raster_topology(candidate_path, character, ppem)
            record = {
                "character": character,
                "ppem": ppem,
                "regular": regular,
                "candidate": candidate,
            }
            if candidate["foreground"] > regular["foreground"]:
                result["foreground_splits"].append(record)
            if candidate["foreground"] < regular["foreground"]:
                result["foreground_merges"].append(record)
            if candidate["counters"] > regular["counters"]:
                result["counter_gains"].append(record)
            if candidate["counters"] < regular["counters"]:
                result["counter_losses"].append(record)
    return result


def audit_cjk(
    regular_path: Path,
    candidate_dir: Path,
) -> list[dict[str, object]]:
    regular = TTFont(regular_path)
    try:
        hangul_characters = [
            chr(codepoint)
            for codepoint in sorted(AUDIT_CODEPOINTS)
            if 0xAC00 <= codepoint <= 0xD7A3
        ]
        hangul_text = "".join(hangul_characters)
        regular_raster = raster_coverage(regular_path, hangul_text)
        regular_vector = sample_vector_coverage(regular, hangul_text)
        regular_metrics = {
            character: glyph_metrics(regular, character)
            for character in hangul_characters
        }
        selected_bold_offset, selected_bold_counter, selected_bold_advance = (
            SELECTED_CJK_CONSTRUCTIONS["Bold"]
        )
        selected_bold_spec = next(
            spec
            for spec in CJK_CANDIDATES
            if spec.style == "Bold"
            and spec.offset == selected_bold_offset
            and spec.counter == selected_bold_counter
            and spec.hangul_advance_scale == selected_bold_advance
        )
        selected_bold_path = candidate_dir / f"CJK-{selected_bold_spec.slug}.otf"
        selected_bold_raster_ratio = (
            raster_coverage(selected_bold_path, hangul_text) / regular_raster
        )
        results = []
        for spec in CJK_CANDIDATES:
            path = candidate_dir / f"CJK-{spec.slug}.otf"
            candidate = TTFont(path)
            try:
                missing = []
                advance_mismatches = []
                area_ratios = []
                for character in hangul_characters:
                    baseline = regular_metrics[character]
                    current = glyph_metrics(candidate, character)
                    if baseline is None or current is None:
                        missing.append(character)
                        continue
                    area_ratios.append(current["area"] / baseline["area"])
                    expected_advance = round(
                        baseline["advance"] * spec.hangul_advance_scale
                    )
                    if current["advance"] != expected_advance:
                        advance_mismatches.append(
                            {
                                "character": character,
                                "expected": expected_advance,
                                "actual": current["advance"],
                            }
                        )
                vector_ratio = (
                    sample_vector_coverage(candidate, hangul_text)
                    / regular_vector
                )
                raster_ratio = (
                    raster_coverage(path, hangul_text) / regular_raster
                )
                zero = glyph_metrics(candidate, "0")
                zero_gap = zero["bounds"][0] + zero["advance"] - zero["bounds"][2]
                pair_spacing = hangul_pair_spacing(candidate, hangul_characters)
                structural_reference_path = (
                    selected_bold_path
                    if spec.style == "ExtraBold"
                    else regular_path
                )
                structural_reference = (
                    selected_bold_spec.label
                    if spec.style == "ExtraBold"
                    else "Regular"
                )
                reference_raster_ratio = (
                    selected_bold_raster_ratio
                    if spec.style == "ExtraBold"
                    else 1.0
                )
                changes = topology_changes(
                    structural_reference_path,
                    path,
                    hangul_characters,
                )
                target = WEIGHT_TARGETS[spec.style]
                structure_count = sum(len(records) for records in changes.values())
                critical_structure_count = sum(
                    1
                    for records in changes.values()
                    for record in records
                    if record["ppem"] == 64
                )
                within_target = target.minimum <= raster_ratio <= target.maximum
                results.append(
                    {
                        "label": spec.label,
                        "style": spec.style,
                        "offset": spec.offset,
                        "counter": spec.counter,
                        "family": decoded_family(candidate),
                        "path": str(path),
                        "hangul_advance_scale": spec.hangul_advance_scale,
                        "target": {
                            "minimum": target.minimum,
                            "center": target.center,
                            "maximum": target.maximum,
                        },
                        "median_area_ratio": median(area_ratios),
                        "first_percentile_area_ratio": percentile(area_ratios, 0.01),
                        "ninety_ninth_percentile_area_ratio": percentile(
                            area_ratios,
                            0.99,
                        ),
                        "vector_coverage_ratio": vector_ratio,
                        "raster_coverage_ratio": raster_ratio,
                        "raster_separation_from_reference": (
                            raster_ratio - reference_raster_ratio
                        ),
                        "structural_reference": structural_reference,
                        "target_error": abs(raster_ratio - target.center),
                        "zero_gap": zero_gap,
                        "hangul_pair_spacing": pair_spacing,
                        "missing": missing,
                        "advance_mismatches": advance_mismatches,
                        **changes,
                        "structure_change_count": structure_count,
                        "critical_structure_change_count": critical_structure_count,
                        "within_target": within_target,
                        "numeric_pass": (
                            within_target
                            and not missing
                            and not advance_mismatches
                            and (
                                spec.style != "ExtraBold"
                                or pair_spacing["nonpositive_count"] == 0
                            )
                        ),
                        "structural_review_required": structure_count > 0,
                    }
                )
            finally:
                candidate.close()
        return results
    finally:
        regular.close()


def audit_latin(
    regular_path: Path,
    candidate_dir: Path,
) -> list[dict[str, object]]:
    regular = TTFont(regular_path)
    try:
        regular_raster = raster_coverage(regular_path, LATIN_SENTINELS)
        regular_vector = sample_vector_coverage(regular, LATIN_SENTINELS)
        regular_cap_top = glyph_metrics(regular, "H")["bounds"][3]
        regular_x_top = glyph_metrics(regular, "x")["bounds"][3]
        results = []
        for spec in LATIN_CANDIDATES:
            path = candidate_dir / f"Latin-{spec.slug}.otf"
            candidate = TTFont(path)
            try:
                vector_ratio = (
                    sample_vector_coverage(candidate, LATIN_SENTINELS)
                    / regular_vector
                )
                raster_ratio = (
                    raster_coverage(path, LATIN_SENTINELS) / regular_raster
                )
                cap_top = glyph_metrics(candidate, "H")["bounds"][3]
                x_top = glyph_metrics(candidate, "x")["bounds"][3]
                target = WEIGHT_TARGETS[spec.style]
                within_target = target.minimum <= raster_ratio <= target.maximum
                geometry_flags = []
                if abs(cap_top - regular_cap_top) > 2:
                    geometry_flags.append("cap height")
                if abs(x_top - regular_x_top) > 2:
                    geometry_flags.append("x-height")
                results.append(
                    {
                        "label": spec.label,
                        "style": spec.style,
                        "weight": spec.weight,
                        "grade": spec.grade,
                        "family": decoded_family(candidate),
                        "path": str(path),
                        "target": {
                            "minimum": target.minimum,
                            "center": target.center,
                            "maximum": target.maximum,
                        },
                        "vector_coverage_ratio": vector_ratio,
                        "raster_coverage_ratio": raster_ratio,
                        "target_error": abs(raster_ratio - target.center),
                        "cap_top": cap_top,
                        "x_top": x_top,
                        "geometry_flags": geometry_flags,
                        "within_target": within_target,
                        "numeric_pass": within_target,
                    }
                )
            finally:
                candidate.close()
        return results
    finally:
        regular.close()


def recommend_pairs(
    cjk: list[dict[str, object]],
    latin: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    recommendations = {}
    for style, target in WEIGHT_TARGETS.items():
        selected_cjk_construction = SELECTED_CJK_CONSTRUCTIONS.get(style)
        selected_latin_construction = SELECTED_LATIN_CONSTRUCTIONS.get(style)
        pairs = []
        for cjk_candidate in (item for item in cjk if item["style"] == style):
            for latin_candidate in (
                item for item in latin if item["style"] == style
            ):
                script_difference = abs(
                    cjk_candidate["raster_coverage_ratio"]
                    - latin_candidate["raster_coverage_ratio"]
                )
                target_error = (
                    abs(cjk_candidate["raster_coverage_ratio"] - target.center)
                    + abs(latin_candidate["raster_coverage_ratio"] - target.center)
                )
                matched = (
                    cjk_candidate["numeric_pass"]
                    and latin_candidate["numeric_pass"]
                    and script_difference <= 0.04
                )
                pairs.append(
                    {
                        "style": style,
                        "selected_cjk": (
                            selected_cjk_construction is not None
                            and (
                                cjk_candidate["offset"],
                                cjk_candidate["counter"],
                                cjk_candidate["hangul_advance_scale"],
                            )
                            == selected_cjk_construction
                        ),
                        "selected_latin": (
                            selected_latin_construction is not None
                            and (
                                latin_candidate["weight"],
                                latin_candidate["grade"],
                            )
                            == selected_latin_construction
                        ),
                        "cjk": cjk_candidate["label"],
                        "cjk_family": cjk_candidate["family"],
                        "cjk_ratio": cjk_candidate["raster_coverage_ratio"],
                        "latin": latin_candidate["label"],
                        "latin_family": latin_candidate["family"],
                        "latin_ratio": latin_candidate["raster_coverage_ratio"],
                        "script_difference": script_difference,
                        "target_error": target_error,
                        "structure_change_count": cjk_candidate[
                            "structure_change_count"
                        ],
                        "critical_structure_change_count": cjk_candidate[
                            "critical_structure_change_count"
                        ],
                        "matched": matched,
                    }
                )
        pairs.sort(
            key=lambda item: (
                not item["matched"],
                item["target_error"] + item["script_difference"],
                item["critical_structure_change_count"],
                item["structure_change_count"],
            )
        )
        if (
            selected_cjk_construction is not None
            and selected_latin_construction is not None
        ):
            selected_pair = next(
                item
                for item in pairs
                if item["selected_cjk"] and item["selected_latin"]
            )
            selected_pair["selected"] = True
            remaining_pairs = [
                item for item in pairs if item is not selected_pair
            ]
            recommendations[style] = [selected_pair, *remaining_pairs[:4]]
        else:
            pairs[0]["provisional"] = True
            recommendations[style] = pairs[:5]
    return recommendations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the Regular-anchored weight exploration microfonts."
    )
    parser.add_argument("--regular", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    candidate_dir = Path(args.candidate_dir)
    cjk = audit_cjk(candidate_dir / "CJK-Regular.otf", candidate_dir)
    latin = audit_latin(Path(args.regular), candidate_dir)
    recommendations = recommend_pairs(cjk, latin)
    report = {
        "raster_ppem": RASTER_PPEM,
        "targets": {
            style: {
                "minimum": target.minimum,
                "center": target.center,
                "maximum": target.maximum,
            }
            for style, target in WEIGHT_TARGETS.items()
        },
        "cjk": cjk,
        "latin": latin,
        "recommendations": recommendations,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for style, pairs in recommendations.items():
        best = pairs[0]
        status = "SELECTED" if best.get("selected") else "PROVISIONAL"
        print(
            f"{status} {style}: {best['cjk']} {best['cjk_ratio']:.3f} / "
            f"{best['latin']} {best['latin_ratio']:.3f}; "
            f"script_delta={best['script_difference']:.3f}, "
            f"structure={best['structure_change_count']}"
        )


if __name__ == "__main__":
    main()
