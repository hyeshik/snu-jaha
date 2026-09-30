#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from statistics import median

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
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
from build_jaha import (
    STYLE_SPECS,
    should_expand_hangul_advance,
    should_keep_ridi_codepoint,
    transformed_hangul_advance,
)
from build_lightweight_microfonts import DEFAULT_FIGURES


MAX_EXAMPLES = 50
FULL_RASTER_PPEM = 64
MINIMUM_RETAINED_COUNTER_AREA_RATIO = 0.55
SPECIMEN_DIR = Path(__file__).resolve().parents[1] / "specimen"
MODERN_HANGUL_RUN = re.compile(r"[가-힣]{2,}")


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


def extract_hangul_bigrams(text: str) -> Counter[str]:
    bigrams: Counter[str] = Counter()
    for match in MODERN_HANGUL_RUN.finditer(text):
        run = match.group()
        bigrams.update(run[index : index + 2] for index in range(len(run) - 1))
    return bigrams


def specimen_hangul_bigrams(directory: Path = SPECIMEN_DIR) -> Counter[str]:
    bigrams: Counter[str] = Counter()
    for path in sorted(directory.glob("*.typ")):
        bigrams.update(extract_hangul_bigrams(path.read_text(encoding="utf-8")))
    return bigrams


def horizontal_bounds(glyph_set, glyph_name: str) -> tuple[float, float]:
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    if pen.bounds is None:
        return (0.0, 0.0)
    return (float(pen.bounds[0]), float(pen.bounds[2]))


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
        regular_coverage_ratios = []
        bold_coverage_ratios = []
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
            expected_advances = {
                name: (
                    transformed_hangul_advance(
                        advances["Regular"],
                        STYLE_SPECS[name],
                    )
                    if should_expand_hangul_advance(codepoint)
                    else advances["Regular"]
                )
                for name in paths
            }
            # The final uniform fit rounds after weight-specific expansion;
            # expanding an already rounded Regular can differ by one unit.
            tolerance = 1 if should_expand_hangul_advance(codepoint) else 0
            if any(
                abs(advances[name] - expected_advances[name]) > tolerance
                for name in paths
            ):
                advance_mismatches.append(
                    {
                        "codepoint": f"U+{codepoint:04X}",
                        "character": chr(codepoint),
                        "advances": advances,
                        "expected": expected_advances,
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
                regular_coverage_ratios.append(
                    (areas["ExtraBold"] / advances["ExtraBold"])
                    / (areas["Regular"] / advances["Regular"])
                )
                bold_coverage_ratios.append(
                    (areas["Bold"] / advances["Bold"])
                    / (areas["Regular"] / advances["Regular"])
                )

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
        latin_regular_coverage_ratios = []
        latin_bold_coverage_ratios = []
        for character in LATIN_SENTINELS:
            codepoint = ord(character)
            areas = {
                name: outline_area(glyph_sets[name], cmaps[name][codepoint])
                for name in paths
            }
            advances = {
                name: fonts[name]["hmtx"][cmaps[name][codepoint]][0]
                for name in paths
            }
            latin_regular_ratios.append(areas["ExtraBold"] / areas["Regular"])
            latin_bold_ratios.append(areas["Bold"] / areas["Regular"])
            latin_regular_coverage_ratios.append(
                (areas["ExtraBold"] / advances["ExtraBold"])
                / (areas["Regular"] / advances["Regular"])
            )
            latin_bold_coverage_ratios.append(
                (areas["Bold"] / advances["Bold"])
                / (areas["Regular"] / advances["Regular"])
            )

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
                        if ratio >= MINIMUM_RETAINED_COUNTER_AREA_RATIO:
                            counter_area_reviews.append(item)
                        else:
                            counter_area_losses.append(item)

        hangul_summary = summarize(regular_ratios)
        bold_summary = summarize(bold_ratios)
        hangul_coverage_summary = summarize(regular_coverage_ratios)
        bold_coverage_summary = summarize(bold_coverage_ratios)
        latin_summary = summarize(latin_regular_ratios)
        latin_bold_summary = summarize(latin_bold_ratios)
        latin_coverage_summary = summarize(latin_regular_coverage_ratios)
        latin_bold_coverage_summary = summarize(latin_bold_coverage_ratios)
        hangul_separation = (
            hangul_coverage_summary["median"]
            - bold_coverage_summary["median"]
        )
        latin_separation = (
            latin_coverage_summary["median"]
            - latin_bold_coverage_summary["median"]
        )
        script_difference = abs(
            hangul_coverage_summary["median"]
            - latin_coverage_summary["median"]
        )
        extra_zero_gap = zero_gap(fonts["ExtraBold"])

        specimen_bigrams = specimen_hangul_bigrams()
        spacing_rows = []
        extrabold_font = fonts["ExtraBold"]
        extrabold_cmap = cmaps["ExtraBold"]
        extrabold_glyph_set = glyph_sets["ExtraBold"]
        for pair, occurrences in specimen_bigrams.items():
            left_name = extrabold_cmap[ord(pair[0])]
            right_name = extrabold_cmap[ord(pair[1])]
            _, left_x_max = horizontal_bounds(extrabold_glyph_set, left_name)
            right_x_min, _ = horizontal_bounds(extrabold_glyph_set, right_name)
            left_advance = extrabold_font["hmtx"][left_name][0]
            spacing_rows.append(
                {
                    "pair": pair,
                    "occurrences": occurrences,
                    "gap": left_advance - left_x_max + right_x_min,
                }
            )
        spacing_rows.sort(key=lambda item: (item["gap"], item["pair"]))
        nonpositive_spacing = [item for item in spacing_rows if item["gap"] <= 0]

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
        if not 1.47 <= hangul_coverage_summary["median"] <= 1.53:
            failures.append("Hangul median coverage ratio")
        if not 0.06 <= hangul_separation <= 0.10:
            failures.append("Hangul Bold coverage separation")
        if (
            hangul_coverage_summary["ninety_ninth_percentile"]
            - hangul_coverage_summary["first_percentile"]
            > 0.15
        ):
            failures.append("Hangul coverage ratio spread")
        if not 44 <= extra_zero_gap <= 48:
            failures.append("00 gap")
        if not 1.46 <= latin_coverage_summary["median"] <= 1.53:
            failures.append("Latin median coverage ratio")
        if not 0.07 <= latin_separation <= 0.12:
            failures.append("Latin Bold coverage separation")
        if script_difference > 0.05:
            failures.append("mixed-script coverage ratio")
        if any(item["ppem"] == 64 for item in counter_losses):
            failures.append("64 ppem counter loss")
        if counter_area_losses:
            failures.append("64 ppem counter area")
        if nonpositive_spacing:
            failures.append("nonpositive Hangul spacing")

        return {
            "pass": not failures,
            "failures": failures,
            "encoded_codepoints": len(common_codepoints),
            "cjk_codepoints": len(cjk_codepoints),
            "hangul_codepoints": len(hangul_codepoints),
            "hangul_advance_scales": {
                name: STYLE_SPECS[name].hangul_advance_scale
                for name in paths
            },
            "cmap_differences": cmap_differences,
            "hangul_area_ratio": hangul_summary,
            "bold_hangul_area_ratio": bold_summary,
            "hangul_coverage_ratio": hangul_coverage_summary,
            "bold_hangul_coverage_ratio": bold_coverage_summary,
            "hangul_bold_coverage_separation": hangul_separation,
            "latin_area_ratio": latin_summary,
            "bold_latin_area_ratio": latin_bold_summary,
            "latin_coverage_ratio": latin_coverage_summary,
            "bold_latin_coverage_ratio": latin_bold_coverage_summary,
            "latin_bold_coverage_separation": latin_separation,
            "mixed_script_coverage_difference": script_difference,
            "zero_gaps": {
                name: zero_gap(font) for name, font in fonts.items()
            },
            "hangul_spacing": {
                "specimen_directory": str(SPECIMEN_DIR),
                "unique_pairs": len(spacing_rows),
                "occurrences": sum(specimen_bigrams.values()),
                "minimum_gap": spacing_rows[0]["gap"],
                "nonpositive_pair_count": len(nonpositive_spacing),
                "nonpositive_occurrences": sum(
                    item["occurrences"] for item in nonpositive_spacing
                ),
                "tightest_pairs": spacing_rows[:MAX_EXAMPLES],
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
        f"Hangul coverage={report['hangul_coverage_ratio']['median']:.3f}, "
        f"Latin coverage={report['latin_coverage_ratio']['median']:.3f}, "
        f"00 gap={report['zero_gaps']['ExtraBold']:.1f}, "
        f"Hangul pair gap={report['hangul_spacing']['minimum_gap']:.1f}, "
        f"failures={','.join(report['failures']) or '-'}"
    )
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
