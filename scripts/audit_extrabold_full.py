#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.ttLib import TTFont
from PIL import ImageFont

from audit_extrabold_candidates import (
    LATIN_SENTINELS,
    TOPOLOGY_PPEMS,
    raster_topology,
)
from audit_lightweight_candidates import percentile
from audit_weight_range import zero_gap
from build_extrabold_microfonts import HEAVY_AUDIT_CODEPOINTS
from build_jaha import should_keep_ridi_codepoint
from build_lightweight_microfonts import DEFAULT_FIGURES


MAX_EXAMPLES = 50
FULL_RASTER_PPEM = 64
REVIEWED_COUNTER_AREA_MINIMA = {"뼮": 0.68}


def outline_area(glyph_set, glyph_name: str) -> float:
    pen = AreaPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return abs(float(pen.value))


def raster_ink(font: ImageFont.FreeTypeFont, character: str) -> int:
    return int(np.asarray(font.getmask(character, mode="L"), dtype=np.uint8).sum())


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "minimum": min(values),
        "first_percentile": percentile(values, 0.01),
        "median": median(values),
        "ninety_ninth_percentile": percentile(values, 0.99),
        "maximum": max(values),
    }


def audit(
    regular_path: Path,
    bold_path: Path,
    extrabold_path: Path,
) -> dict[str, object]:
    paths = {
        "Regular": regular_path,
        "Bold": bold_path,
        "ExtraBold": extrabold_path,
    }
    fonts = {name: TTFont(path) for name, path in paths.items()}
    raster_fonts = {
        name: ImageFont.truetype(str(path), FULL_RASTER_PPEM)
        for name, path in paths.items()
    }
    try:
        cmaps = {name: font.getBestCmap() for name, font in fonts.items()}
        glyph_sets = {name: font.getGlyphSet() for name, font in fonts.items()}
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

        empty_glyphs = []
        advance_mismatches = []
        vector_order_violations = []
        raster_order_violations = []
        raster_equalities = []
        regular_ratios = []
        bold_ratios = []
        for codepoint in cjk_codepoints:
            glyph_names = {
                name: cmap[codepoint] for name, cmap in cmaps.items()
            }
            areas = {
                name: outline_area(glyph_sets[name], glyph_name)
                for name, glyph_name in glyph_names.items()
            }
            advances = {
                name: fonts[name]["hmtx"][glyph_name][0]
                for name, glyph_name in glyph_names.items()
            }
            if len(set(advances.values())) != 1:
                advance_mismatches.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "advances": advances,
                    }
                )
            if areas["Regular"] > 0 and areas["ExtraBold"] <= 0:
                empty_glyphs.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                    }
                )
            if areas["Bold"] > 0 and areas["ExtraBold"] <= areas["Bold"]:
                vector_order_violations.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "areas": areas,
                    }
                )
            if codepoint in hangul_codepoints and areas["Regular"] > 0:
                regular_ratios.append(areas["ExtraBold"] / areas["Regular"])
                bold_ratios.append(areas["Bold"] / areas["Regular"])

        for codepoint in hangul_codepoints:
            character = chr(codepoint)
            ink = {
                name: raster_ink(font, character)
                for name, font in raster_fonts.items()
            }
            if ink["ExtraBold"] < ink["Bold"]:
                raster_order_violations.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": character,
                        "ink": ink,
                    }
                )
            elif ink["ExtraBold"] == ink["Bold"]:
                raster_equalities.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": character,
                        "ink": ink,
                    }
                )

        latin_regular_ratios = []
        latin_bold_ratios = []
        for character in LATIN_SENTINELS:
            codepoint = ord(character)
            areas = {
                name: outline_area(glyph_sets[name], cmaps[name][codepoint])
                for name in paths
            }
            latin_regular_ratios.append(areas["ExtraBold"] / areas["Regular"])
            latin_bold_ratios.append(areas["Bold"] / areas["Regular"])

        topology_merges = []
        counter_losses = []
        counter_area_reviews = []
        counter_area_losses = []
        audited_hangul = [
            chr(codepoint)
            for codepoint in sorted(HEAVY_AUDIT_CODEPOINTS)
            if 0xAC00 <= codepoint <= 0xD7A3
        ]
        for character in audited_hangul:
            for ppem in TOPOLOGY_PPEMS:
                bold_topology = raster_topology(bold_path, character, ppem)
                extrabold_topology = raster_topology(
                    extrabold_path,
                    character,
                    ppem,
                )
                if (
                    extrabold_topology["foreground_count"]
                    < bold_topology["foreground_count"]
                ):
                    topology_merges.append(
                        {
                            "character": character,
                            "ppem": ppem,
                            "bold": bold_topology["foreground_count"],
                            "extrabold": extrabold_topology["foreground_count"],
                        }
                    )
                if (
                    extrabold_topology["counter_count"]
                    < bold_topology["counter_count"]
                ):
                    counter_losses.append(
                        {
                            "character": character,
                            "ppem": ppem,
                            "bold": bold_topology["counter_count"],
                            "extrabold": extrabold_topology["counter_count"],
                        }
                    )
                if ppem == 64 and bold_topology["counter_area"]:
                    ratio = (
                        extrabold_topology["counter_area"]
                        / bold_topology["counter_area"]
                    )
                    if ratio < 0.70:
                        item = {
                            "character": character,
                            "ratio": ratio,
                            "bold": bold_topology["counter_area"],
                            "extrabold": extrabold_topology["counter_area"],
                        }
                        reviewed_minimum = REVIEWED_COUNTER_AREA_MINIMA.get(
                            character
                        )
                        if (
                            reviewed_minimum is not None
                            and ratio >= reviewed_minimum
                        ):
                            counter_area_reviews.append(item)
                        else:
                            counter_area_losses.append(item)

        hangul_summary = summarize(regular_ratios)
        bold_summary = summarize(bold_ratios)
        latin_summary = summarize(latin_regular_ratios)
        latin_bold_summary = summarize(latin_bold_ratios)
        hangul_separation = hangul_summary["median"] - bold_summary["median"]
        latin_separation = latin_summary["median"] - latin_bold_summary["median"]
        script_difference = abs(
            hangul_summary["median"] - latin_summary["median"]
        )
        extra_zero_gap = zero_gap(fonts["ExtraBold"])

        failures = []
        if any(
            difference["missing"] or difference["extra"]
            for difference in cmap_differences.values()
        ):
            failures.append("cmap mismatch")
        if empty_glyphs:
            failures.append("new empty CJK glyph")
        if advance_mismatches:
            failures.append("CJK advance mismatch")
        if vector_order_violations:
            failures.append("CJK vector order")
        if raster_order_violations:
            failures.append("Hangul raster order")
        if not 1.44 <= hangul_summary["median"] <= 1.54:
            failures.append("Hangul median ratio")
        if not 0.08 <= hangul_separation <= 0.16:
            failures.append("Hangul Bold separation")
        if (
            hangul_summary["ninety_ninth_percentile"]
            - hangul_summary["first_percentile"]
            > 0.10
        ):
            failures.append("Hangul ratio spread")
        if not 45 <= extra_zero_gap <= 51:
            failures.append("00 gap")
        if not 1.47 <= latin_summary["median"] <= 1.56:
            failures.append("Latin median ratio")
        if not 0.06 <= latin_separation <= 0.14:
            failures.append("Latin Bold separation")
        if script_difference > 0.05:
            failures.append("mixed-script ratio")
        if any(item["ppem"] == 64 for item in counter_losses):
            failures.append("64 ppem counter loss")
        if counter_area_losses:
            failures.append("64 ppem counter area")

        return {
            "pass": not failures,
            "failures": failures,
            "encoded_codepoints": len(common_codepoints),
            "cjk_codepoints": len(cjk_codepoints),
            "hangul_codepoints": len(hangul_codepoints),
            "cmap_differences": cmap_differences,
            "hangul_area_ratio": hangul_summary,
            "bold_hangul_area_ratio": bold_summary,
            "hangul_bold_separation": hangul_separation,
            "latin_area_ratio": latin_summary,
            "bold_latin_area_ratio": latin_bold_summary,
            "latin_bold_separation": latin_separation,
            "mixed_script_difference": script_difference,
            "zero_gaps": {
                name: zero_gap(font) for name, font in fonts.items()
            },
            "full_raster_ppem": FULL_RASTER_PPEM,
            "empty_glyph_count": len(empty_glyphs),
            "empty_glyph_examples": empty_glyphs[:MAX_EXAMPLES],
            "advance_mismatch_count": len(advance_mismatches),
            "advance_mismatch_examples": advance_mismatches[:MAX_EXAMPLES],
            "vector_order_violation_count": len(vector_order_violations),
            "vector_order_violation_examples": vector_order_violations[:MAX_EXAMPLES],
            "raster_order_violation_count": len(raster_order_violations),
            "raster_order_violation_examples": raster_order_violations[:MAX_EXAMPLES],
            "raster_equality_count": len(raster_equalities),
            "raster_equality_examples": raster_equalities[:MAX_EXAMPLES],
            "representative_topology": {
                "merges": topology_merges,
                "counter_losses": counter_losses,
                "counter_area_reviews": counter_area_reviews,
                "counter_area_losses": counter_area_losses,
            },
        }
    finally:
        for font in fonts.values():
            font.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the full Bold-to-ExtraBold construction."
    )
    parser.add_argument("--regular", required=True)
    parser.add_argument("--bold", required=True)
    parser.add_argument("--extrabold", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = audit(
        Path(args.regular),
        Path(args.bold),
        Path(args.extrabold),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    status = "PASS" if report["pass"] else "FAIL"
    print(
        f"{status}: encoded={report['encoded_codepoints']}, "
        f"hangul={report['hangul_codepoints']}, "
        f"Hangul median={report['hangul_area_ratio']['median']:.3f}, "
        f"Latin median={report['latin_area_ratio']['median']:.3f}, "
        f"00 gap={report['zero_gaps']['ExtraBold']:.1f}, "
        f"failures={','.join(report['failures']) or '-'}"
    )
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
