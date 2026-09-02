#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import ImageFont

from audit_lightweight_candidates import (
    REVIEWED_COMPONENT_INCREASES,
    connected_component_sizes,
    percentile,
)
from build_jaha import should_keep_ridi_codepoint
from build_lightweight_microfonts import AUDIT_CODEPOINTS, DEFAULT_FIGURES


MAX_EXAMPLES = 40
RASTER_PPEM = 256


def glyph_area(font: TTFont, codepoint: int) -> float | None:
    glyph_name = font.getBestCmap().get(codepoint)
    if glyph_name is None:
        return None
    glyph_set = font.getGlyphSet()
    pen = AreaPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return abs(float(pen.value))


def glyph_advance(font: TTFont, codepoint: int) -> int | None:
    glyph_name = font.getBestCmap().get(codepoint)
    if glyph_name is None:
        return None
    return font["hmtx"][glyph_name][0]


def raster_ink(font: ImageFont.FreeTypeFont, character: str) -> int:
    mask = font.getmask(character, mode="L")
    return int(np.asarray(mask, dtype=np.uint8).sum())


def zero_gap(font: TTFont) -> float:
    cmap = font.getBestCmap()
    glyph_name = cmap[ord("0")]
    glyph_set = font.getGlyphSet()
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    bounds = pen.bounds
    advance = font["hmtx"][glyph_name][0]
    return float(bounds[0] + advance - bounds[2])


def component_review(
    regular_path: Path,
    candidate_path: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    reviewed = []
    unexpected = []
    for codepoint in sorted(AUDIT_CODEPOINTS):
        if codepoint < 0xAC00:
            continue
        character = chr(codepoint)
        regular_sizes = connected_component_sizes(regular_path, character)
        candidate_sizes = connected_component_sizes(candidate_path, character)
        difference = len(candidate_sizes) - len(regular_sizes)
        if difference <= 0:
            continue
        item = {
            "character": character,
            "regular": len(regular_sizes),
            "candidate": len(candidate_sizes),
            "regular_sizes": regular_sizes,
            "candidate_sizes": candidate_sizes,
        }
        if REVIEWED_COMPONENT_INCREASES.get(character) == difference:
            reviewed.append(item)
        else:
            unexpected.append(item)
    return reviewed, unexpected


def audit(
    thin_path: Path,
    light_path: Path,
    regular_path: Path,
) -> dict[str, object]:
    paths = {
        "Thin": thin_path,
        "Light": light_path,
        "Regular": regular_path,
    }
    fonts = {name: TTFont(path) for name, path in paths.items()}
    raster_fonts = {
        name: ImageFont.truetype(str(path), RASTER_PPEM)
        for name, path in paths.items()
    }
    try:
        cmaps = {name: font.getBestCmap() for name, font in fonts.items()}
        regular_codepoints = set(cmaps["Regular"])
        cmap_differences = {
            name: {
                "missing": sorted(regular_codepoints - set(cmap)),
                "extra": sorted(set(cmap) - regular_codepoints),
            }
            for name, cmap in cmaps.items()
            if name != "Regular"
        }
        common_codepoints = sorted(
            set.intersection(*(set(cmap) for cmap in cmaps.values()))
        )
        cjk_codepoints = [
            codepoint
            for codepoint in common_codepoints
            if should_keep_ridi_codepoint(codepoint)
            or chr(codepoint) in DEFAULT_FIGURES
        ]
        hangul_codepoints = [
            codepoint
            for codepoint in common_codepoints
            if 0xAC00 <= codepoint <= 0xD7A3
        ]

        vector_area_reviews = []
        area_order_violations = []
        empty_glyphs = []
        hangul_ratios = {"Thin": [], "Light": []}
        strict_codepoints = {
            codepoint
            for codepoint in AUDIT_CODEPOINTS
            if codepoint >= 0xAC00 or chr(codepoint) in DEFAULT_FIGURES
        }
        strict_order_violations = []
        for codepoint in common_codepoints:
            areas = {
                name: glyph_area(font, codepoint)
                for name, font in fonts.items()
            }
            if any(area is None for area in areas.values()):
                continue
            regular_area = areas["Regular"]
            raster_areas = {
                name: raster_ink(font, chr(codepoint))
                for name, font in raster_fonts.items()
            }
            if regular_area > 0:
                for name in ("Thin", "Light"):
                    if areas[name] <= 0:
                        empty_glyphs.append(
                            {"character": chr(codepoint), "style": name}
                        )
                if codepoint in hangul_codepoints:
                    hangul_ratios["Thin"].append(areas["Thin"] / regular_area)
                    hangul_ratios["Light"].append(areas["Light"] / regular_area)
            if not (
                areas["Thin"] <= areas["Light"] + 0.01
                and areas["Light"] <= areas["Regular"] + 0.01
            ):
                vector_area_reviews.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "vector_areas": areas,
                        "raster_areas": raster_areas,
                    }
                )
            if not (
                raster_areas["Thin"] <= raster_areas["Light"]
                and raster_areas["Light"] <= raster_areas["Regular"]
            ):
                area_order_violations.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "raster_areas": raster_areas,
                        "vector_areas": areas,
                    }
                )
            if codepoint in strict_codepoints and regular_area > 0 and not (
                areas["Thin"] < areas["Light"] < areas["Regular"]
            ):
                strict_order_violations.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "areas": areas,
                    }
                )

        advance_mismatches = []
        for codepoint in cjk_codepoints:
            advances = {
                name: glyph_advance(font, codepoint)
                for name, font in fonts.items()
            }
            if len(set(advances.values())) != 1:
                advance_mismatches.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "advances": advances,
                    }
                )

        component_results = {}
        unexpected_components = []
        for name in ("Thin", "Light"):
            reviewed, unexpected = component_review(
                regular_path,
                paths[name],
            )
            component_results[name] = {
                "reviewed": reviewed,
                "unexpected": unexpected,
            }
            unexpected_components.extend(
                {"style": name, **item} for item in unexpected
            )

        failures = []
        if any(
            value["missing"] or value["extra"]
            for value in cmap_differences.values()
        ):
            failures.append("cmap mismatch")
        if empty_glyphs:
            failures.append("new empty glyph")
        if area_order_violations:
            failures.append("encoded raster area order")
        if strict_order_violations:
            failures.append("sentinel area order")
        if advance_mismatches:
            failures.append("CJK advance mismatch")
        if unexpected_components:
            failures.append("unexpected raster component increase")

        ratio_summary = {
            name: {
                "minimum": min(values),
                "first_percentile": percentile(values, 0.01),
                "median": median(values),
                "maximum": max(values),
            }
            for name, values in hangul_ratios.items()
        }
        return {
            "pass": not failures,
            "failures": failures,
            "encoded_codepoints": len(common_codepoints),
            "cjk_codepoints": len(cjk_codepoints),
            "hangul_codepoints": len(hangul_codepoints),
            "cmap_differences": cmap_differences,
            "hangul_area_ratios": ratio_summary,
            "zero_gaps": {
                name: zero_gap(font) for name, font in fonts.items()
            },
            "raster_ppem": RASTER_PPEM,
            "empty_glyph_count": len(empty_glyphs),
            "empty_glyph_examples": empty_glyphs[:MAX_EXAMPLES],
            "vector_area_review_count": len(vector_area_reviews),
            "vector_area_review_examples": vector_area_reviews[:MAX_EXAMPLES],
            "area_order_violation_count": len(area_order_violations),
            "area_order_violation_examples": area_order_violations[:MAX_EXAMPLES],
            "strict_order_violation_count": len(strict_order_violations),
            "strict_order_violation_examples": strict_order_violations[:MAX_EXAMPLES],
            "advance_mismatch_count": len(advance_mismatches),
            "advance_mismatch_examples": advance_mismatches[:MAX_EXAMPLES],
            "component_review": component_results,
        }
    finally:
        for font in fonts.values():
            font.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the full Thin–Light–Regular encoded range."
    )
    parser.add_argument("--thin", required=True)
    parser.add_argument("--light", required=True)
    parser.add_argument("--regular", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = audit(
        Path(args.thin),
        Path(args.light),
        Path(args.regular),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    status = "PASS" if report["pass"] else "FAIL"
    ratios = report["hangul_area_ratios"]
    print(
        f"{status}: encoded={report['encoded_codepoints']}, "
        f"hangul={report['hangul_codepoints']}, "
        f"Thin median={ratios['Thin']['median']:.3f}, "
        f"Light median={ratios['Light']['median']:.3f}, "
        f"failures={','.join(report['failures']) or '-'}"
    )
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
