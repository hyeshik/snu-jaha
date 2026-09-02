#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from functools import lru_cache
from pathlib import Path
from statistics import median

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from audit_lightweight_candidates import decoded_family, percentile
from build_extrabold_microfonts import (
    HEAVY_AUDIT_CODEPOINTS,
    EXTRABOLD_CANDIDATES,
)
from build_lightweight_microfonts import DEFAULT_FIGURES


LATIN_SENTINELS = "HMAINoxngp"
CJK_PATTERN = re.compile(r"CJK-XB-N(\d+)-(auto|retain|cjk)\.otf")
LATIN_PATTERN = re.compile(r"Latin-W(\d+)\.otf")
TOPOLOGY_PPEMS = (24, 32, 48, 64)


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
def raster_topology(path: Path, character: str, ppem: int) -> dict[str, object]:
    pixels = raster_mask(str(path), character, ppem)
    foreground = component_sizes(pixels, True)
    counters = component_sizes(pixels, False, enclosed_only=True)
    return {
        "foreground_count": len(foreground),
        "foreground_sizes": foreground,
        "counter_count": len(counters),
        "counter_sizes": counters,
        "counter_area": sum(counters),
    }


def candidate_spec(path: Path):
    match = CJK_PATTERN.fullmatch(path.name)
    if match is None:
        raise ValueError(path)
    offset = int(match.group(1))
    method = match.group(2)
    return next(
        candidate
        for candidate in EXTRABOLD_CANDIDATES
        if candidate.offset == offset and candidate.method == method
    )


def audit_cjk(
    regular_path: Path,
    bold_path: Path,
    candidate_path: Path,
) -> dict[str, object]:
    spec = candidate_spec(candidate_path)
    regular = TTFont(regular_path)
    bold = TTFont(bold_path)
    candidate = TTFont(candidate_path)
    try:
        ratios = []
        bold_ratios = []
        missing = []
        advance_mismatches = []
        strict_order_violations = []
        hangul_characters = [
            chr(codepoint)
            for codepoint in sorted(HEAVY_AUDIT_CODEPOINTS)
            if codepoint >= 0xAC00
        ]
        for codepoint in sorted(HEAVY_AUDIT_CODEPOINTS):
            character = chr(codepoint)
            regular_metrics = glyph_metrics(regular, character)
            bold_metrics = glyph_metrics(bold, character)
            candidate_metrics = glyph_metrics(candidate, character)
            if (
                regular_metrics is None
                or bold_metrics is None
                or candidate_metrics is None
            ):
                missing.append(character)
                continue
            if codepoint >= 0xAC00:
                ratios.append(
                    candidate_metrics["area"] / regular_metrics["area"]
                )
                bold_ratios.append(bold_metrics["area"] / regular_metrics["area"])
            if candidate_metrics["advance"] != regular_metrics["advance"]:
                advance_mismatches.append(character)
            if (
                codepoint >= 0xAC00 or character in DEFAULT_FIGURES
            ) and candidate_metrics["area"] <= bold_metrics["area"]:
                strict_order_violations.append(character)

        foreground_merges = []
        counter_losses = []
        counter_area_losses = []
        for character in hangul_characters:
            for ppem in TOPOLOGY_PPEMS:
                bold_topology = raster_topology(bold_path, character, ppem)
                candidate_topology = raster_topology(
                    candidate_path,
                    character,
                    ppem,
                )
                if (
                    candidate_topology["foreground_count"]
                    < bold_topology["foreground_count"]
                ):
                    foreground_merges.append(
                        {
                            "character": character,
                            "ppem": ppem,
                            "bold": bold_topology["foreground_count"],
                            "candidate": candidate_topology["foreground_count"],
                        }
                    )
                if (
                    candidate_topology["counter_count"]
                    < bold_topology["counter_count"]
                ):
                    counter_losses.append(
                        {
                            "character": character,
                            "ppem": ppem,
                            "bold": bold_topology["counter_count"],
                            "candidate": candidate_topology["counter_count"],
                        }
                    )
                if ppem == 64 and bold_topology["counter_area"]:
                    area_ratio = (
                        candidate_topology["counter_area"]
                        / bold_topology["counter_area"]
                    )
                    if area_ratio < 0.70:
                        counter_area_losses.append(
                            {
                                "character": character,
                                "ratio": area_ratio,
                                "bold": bold_topology["counter_area"],
                                "candidate": candidate_topology["counter_area"],
                            }
                        )

        zero_metrics = glyph_metrics(candidate, "0")
        zero_gap = (
            zero_metrics["bounds"][0]
            + zero_metrics["advance"]
            - zero_metrics["bounds"][2]
        )
        median_ratio = median(ratios)
        bold_median_ratio = median(bold_ratios)
        first_percentile = percentile(ratios, 0.01)
        ninety_ninth_percentile = percentile(ratios, 0.99)
        failures = []
        if missing:
            failures.append("missing glyphs")
        if advance_mismatches:
            failures.append("advance mismatch")
        if strict_order_violations:
            failures.append("not heavier than Bold")
        if not 1.44 <= median_ratio <= 1.54:
            failures.append("median ink ratio")
        if not 0.08 <= median_ratio - bold_median_ratio <= 0.16:
            failures.append("Bold separation")
        if ninety_ninth_percentile - first_percentile > 0.10:
            failures.append("Hangul ratio spread")
        if not 45 <= zero_gap <= 51:
            failures.append("00 gap")
        if foreground_merges:
            failures.append("foreground merges")
        if counter_losses:
            failures.append("counter loss")
        if counter_area_losses:
            failures.append("counter area")
        return {
            "label": f"+{spec.offset} {spec.method}",
            "offset": spec.offset,
            "method": spec.method,
            "weight_type": spec.weight_type,
            "counter": spec.counter,
            "figure_x_scale": spec.figure_x_scale,
            "family": decoded_family(candidate),
            "median_ratio": median_ratio,
            "bold_median_ratio": bold_median_ratio,
            "bold_separation": median_ratio - bold_median_ratio,
            "first_percentile_ratio": first_percentile,
            "ninety_ninth_percentile_ratio": ninety_ninth_percentile,
            "ratio_spread": ninety_ninth_percentile - first_percentile,
            "zero_gap": zero_gap,
            "missing": missing,
            "advance_mismatches": advance_mismatches,
            "strict_order_violations": strict_order_violations,
            "foreground_merges": foreground_merges,
            "counter_losses": counter_losses,
            "counter_area_losses": counter_area_losses,
            "pass": not failures,
            "failures": failures,
        }
    finally:
        regular.close()
        bold.close()
        candidate.close()


def audit_latin(
    regular_path: Path,
    bold_path: Path,
    candidate_path: Path,
) -> dict[str, object]:
    match = LATIN_PATTERN.fullmatch(candidate_path.name)
    if match is None:
        raise ValueError(candidate_path)
    weight = int(match.group(1))
    regular = TTFont(regular_path)
    bold = TTFont(bold_path)
    candidate = TTFont(candidate_path)
    try:
        ratios = []
        bold_ratios = []
        for character in LATIN_SENTINELS:
            regular_metrics = glyph_metrics(regular, character)
            bold_metrics = glyph_metrics(bold, character)
            candidate_metrics = glyph_metrics(candidate, character)
            ratios.append(candidate_metrics["area"] / regular_metrics["area"])
            bold_ratios.append(bold_metrics["area"] / regular_metrics["area"])
        median_ratio = median(ratios)
        bold_median_ratio = median(bold_ratios)
        cap_top = glyph_metrics(candidate, "H")["bounds"][3]
        x_top = glyph_metrics(candidate, "x")["bounds"][3]
        regular_cap_top = glyph_metrics(regular, "H")["bounds"][3]
        regular_x_top = glyph_metrics(regular, "x")["bounds"][3]
        failures = []
        if not 1.47 <= median_ratio <= 1.56:
            failures.append("median ink ratio")
        if not 0.06 <= median_ratio - bold_median_ratio <= 0.14:
            failures.append("Bold separation")
        if abs(cap_top - regular_cap_top) > 2:
            failures.append("cap height")
        if abs(x_top - regular_x_top) > 2:
            failures.append("x-height")
        return {
            "label": f"wght {weight}",
            "weight": weight,
            "family": decoded_family(candidate),
            "median_ratio": median_ratio,
            "bold_median_ratio": bold_median_ratio,
            "bold_separation": median_ratio - bold_median_ratio,
            "cap_top": cap_top,
            "x_top": x_top,
            "pass": not failures,
            "failures": failures,
        }
    finally:
        regular.close()
        bold.close()
        candidate.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure representative ExtraBold microfonts."
    )
    parser.add_argument("--regular", required=True)
    parser.add_argument("--bold", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    regular_path = Path(args.regular)
    bold_path = Path(args.bold)
    candidate_dir = Path(args.candidate_dir)
    cjk = [
        audit_cjk(regular_path, bold_path, path)
        for path in sorted(candidate_dir.glob("CJK-XB-*.otf"))
    ]
    latin = [
        audit_latin(regular_path, bold_path, path)
        for path in sorted(candidate_dir.glob("Latin-*.otf"))
    ]
    pairs = sorted(
        (
            {
                "cjk": cjk_candidate["label"],
                "latin": latin_candidate["label"],
                "ratio_difference": abs(
                    cjk_candidate["median_ratio"]
                    - latin_candidate["median_ratio"]
                ),
            }
            for cjk_candidate in cjk
            if cjk_candidate["pass"]
            for latin_candidate in latin
            if latin_candidate["pass"]
            and abs(
                cjk_candidate["median_ratio"]
                - latin_candidate["median_ratio"]
            )
            <= 0.05
        ),
        key=lambda item: item["ratio_difference"],
    )
    report = {"cjk": cjk, "latin": latin, "pairs": pairs}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for section in (cjk, latin):
        for candidate in section:
            status = "PASS" if candidate["pass"] else "FAIL"
            print(
                f"{status} {candidate['label']}: "
                f"median={candidate['median_ratio']:.3f}, "
                f"failures={','.join(candidate['failures']) or '-'}"
            )
    print(f"eligible pairs={len(pairs)}")


if __name__ == "__main__":
    main()
