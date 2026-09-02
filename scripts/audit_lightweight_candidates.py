#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import median

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from build_lightweight_microfonts import AUDIT_CODEPOINTS, DEFAULT_FIGURES


LATIN_SENTINELS = "HMAINoxngp"
CJK_PATTERN = re.compile(r"CJK-(Light|Thin)-N(\d+)-(auto|squish)\.otf")
LATIN_PATTERN = re.compile(r"Latin-W(\d+)\.otf")
REVIEWED_COMPONENT_INCREASES = {"뿳": 1, "휇": 1}


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


def connected_component_sizes(
    path: Path,
    character: str,
    ppem: int = 64,
) -> list[int]:
    font = ImageFont.truetype(str(path), ppem)
    bounds = font.getbbox(character)
    width = max(1, bounds[2] - bounds[0] + 12)
    height = max(1, bounds[3] - bounds[1] + 12)
    image = Image.new("L", (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((6 - bounds[0], 6 - bounds[1]), character, font=font, fill=255)
    pixels = np.asarray(image) >= 128
    visited = np.zeros_like(pixels, dtype=bool)
    component_sizes = []
    for row, column in np.argwhere(pixels):
        if visited[row, column]:
            continue
        component_size = 0
        stack = [(int(row), int(column))]
        visited[row, column] = True
        while stack:
            current_row, current_column = stack.pop()
            component_size += 1
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    if row_offset == column_offset == 0:
                        continue
                    next_row = current_row + row_offset
                    next_column = current_column + column_offset
                    if not (
                        0 <= next_row < pixels.shape[0]
                        and 0 <= next_column < pixels.shape[1]
                    ):
                        continue
                    if (
                        pixels[next_row, next_column]
                        and not visited[next_row, next_column]
                    ):
                        visited[next_row, next_column] = True
                        stack.append((next_row, next_column))
        component_sizes.append(component_size)
    return sorted(component_sizes, reverse=True)


def decoded_family(font: TTFont) -> str:
    names = {
        record.toUnicode()
        for record in font["name"].names
        if record.nameID == 1
    }
    return sorted(names)[0]


def is_reviewed_component_increase(item: dict[str, object]) -> bool:
    expected = REVIEWED_COMPONENT_INCREASES.get(item["character"])
    return expected == item["candidate"] - item["regular"]


def audit_cjk(regular_path: Path, candidate_path: Path) -> dict[str, object]:
    match = CJK_PATTERN.fullmatch(candidate_path.name)
    if match is None:
        raise ValueError(candidate_path)
    style, offset_text, counter = match.groups()
    regular = TTFont(regular_path)
    candidate = TTFont(candidate_path)
    try:
        ratios = []
        missing = []
        advance_mismatches = []
        component_increases = []
        for codepoint in sorted(AUDIT_CODEPOINTS):
            character = chr(codepoint)
            regular_metrics = glyph_metrics(regular, character)
            candidate_metrics = glyph_metrics(candidate, character)
            if regular_metrics is None or candidate_metrics is None:
                missing.append(character)
                continue
            if codepoint >= 0xAC00:
                ratios.append(
                    candidate_metrics["area"] / regular_metrics["area"]
                )
            if candidate_metrics["advance"] != regular_metrics["advance"]:
                advance_mismatches.append(character)
            regular_components = connected_component_sizes(
                regular_path,
                character,
            )
            candidate_components = connected_component_sizes(
                candidate_path,
                character,
            )
            if len(candidate_components) > len(regular_components):
                component_increases.append(
                    {
                        "character": character,
                        "regular": len(regular_components),
                        "candidate": len(candidate_components),
                        "regular_sizes": regular_components,
                        "candidate_sizes": candidate_components,
                    }
                )

        zero_metrics = glyph_metrics(candidate, "0")
        zero_gap = (
            zero_metrics["bounds"][0]
            + zero_metrics["advance"]
            - zero_metrics["bounds"][2]
        )
        ratio_range = (0.88, 0.93) if style == "Light" else (0.68, 0.76)
        first_percentile_min = 0.80 if style == "Light" else 0.55
        gap_range = (75, 81) if style == "Light" else (85, 95)
        median_ratio = median(ratios)
        first_percentile = percentile(ratios, 0.01)
        unexpected_component_increases = [
            item
            for item in component_increases
            if not is_reviewed_component_increase(item)
        ]
        failures = []
        if missing:
            failures.append("missing glyphs")
        if advance_mismatches:
            failures.append("advance mismatch")
        if unexpected_component_increases:
            failures.append("split raster components")
        if not ratio_range[0] <= median_ratio <= ratio_range[1]:
            failures.append("median ink ratio")
        if first_percentile < first_percentile_min:
            failures.append("first-percentile ink ratio")
        if not gap_range[0] <= zero_gap <= gap_range[1]:
            failures.append("00 gap")
        return {
            "label": f"{style} -{offset_text} {counter}",
            "style": style,
            "offset": -int(offset_text),
            "counter": counter,
            "family": decoded_family(candidate),
            "median_ratio": median_ratio,
            "first_percentile_ratio": first_percentile,
            "zero_gap": zero_gap,
            "missing": missing,
            "advance_mismatches": advance_mismatches,
            "component_increases": component_increases,
            "reviewed_component_increases": [
                item
                for item in component_increases
                if is_reviewed_component_increase(item)
            ],
            "unexpected_component_increases": unexpected_component_increases,
            "pass": not failures,
            "failures": failures,
        }
    finally:
        regular.close()
        candidate.close()


def audit_latin(regular_path: Path, candidate_path: Path) -> dict[str, object]:
    match = LATIN_PATTERN.fullmatch(candidate_path.name)
    if match is None:
        raise ValueError(candidate_path)
    weight = int(match.group(1))
    style = "Light" if weight >= 300 else "Thin"
    regular = TTFont(regular_path)
    candidate = TTFont(candidate_path)
    try:
        ratios = []
        for character in LATIN_SENTINELS:
            regular_metrics = glyph_metrics(regular, character)
            candidate_metrics = glyph_metrics(candidate, character)
            ratios.append(candidate_metrics["area"] / regular_metrics["area"])
        median_ratio = median(ratios)
        ratio_range = (0.88, 0.93) if style == "Light" else (0.68, 0.76)
        cap_top = glyph_metrics(candidate, "H")["bounds"][3]
        x_top = glyph_metrics(candidate, "x")["bounds"][3]
        regular_cap_top = glyph_metrics(regular, "H")["bounds"][3]
        regular_x_top = glyph_metrics(regular, "x")["bounds"][3]
        failures = []
        if not ratio_range[0] <= median_ratio <= ratio_range[1]:
            failures.append("median ink ratio")
        if abs(cap_top - regular_cap_top) > 2:
            failures.append("cap height")
        if abs(x_top - regular_x_top) > 2:
            failures.append("x-height")
        return {
            "label": f"{style} wght {weight}",
            "style": style,
            "weight": weight,
            "family": decoded_family(candidate),
            "median_ratio": median_ratio,
            "cap_top": cap_top,
            "x_top": x_top,
            "pass": not failures,
            "failures": failures,
        }
    finally:
        regular.close()
        candidate.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure Light and Thin representative microfonts."
    )
    parser.add_argument("--regular", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    regular_path = Path(args.regular)
    candidate_dir = Path(args.candidate_dir)
    cjk = [
        audit_cjk(regular_path, path)
        for path in sorted(candidate_dir.glob("CJK-*.otf"))
        if path.name != "CJK-Regular.otf"
    ]
    latin = [
        audit_latin(regular_path, path)
        for path in sorted(candidate_dir.glob("Latin-*.otf"))
    ]
    report = {"cjk": cjk, "latin": latin}
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


if __name__ == "__main__":
    main()
