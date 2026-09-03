#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import ImageFont


LATIN_SAMPLE = "HAMBURGEFONTSminimumoxygenResearch"
LATIN_READING_SAMPLE = (
    "Repeated drought exposure alters recovery kinetics and transcriptomic response"
)
HANGUL_SAMPLE = "자하연연구환경가나다라마바사아흙뿔률쫓빛활괄"
REFERENCE_GLYPHS = "HMAIxnogp"
DEFAULT_FIGURES = "0123456789"
RASTER_PPEM = 128
CANDIDATE_FAMILY_NAME = "SNU Jaha Latin Alt"


def normalized_bounds(font: TTFont, character: str) -> list[float]:
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    pen = BoundsPen(glyph_set)
    glyph_set[cmap[ord(character)]].draw(pen)
    if pen.bounds is None:
        return [0.0, 0.0, 0.0, 0.0]
    factor = 1000 / font["head"].unitsPerEm
    return [float(value * factor) for value in pen.bounds]


def normalized_advance(font: TTFont, character: str) -> float:
    cmap = font.getBestCmap()
    advance = font["hmtx"][cmap[ord(character)]][0]
    return float(advance * 1000 / font["head"].unitsPerEm)


def normalized_area(font: TTFont, character: str) -> float:
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    pen = AreaPen(glyph_set)
    glyph_set[cmap[ord(character)]].draw(pen)
    factor = 1000 / font["head"].unitsPerEm
    return abs(float(pen.value)) * factor * factor


def glyph_metrics(font: TTFont, character: str) -> dict[str, object]:
    bounds = normalized_bounds(font, character)
    return {
        "advance": normalized_advance(font, character),
        "bounds": bounds,
        "width": bounds[2] - bounds[0],
        "height": bounds[3] - bounds[1],
        "area": normalized_area(font, character),
    }


def sample_metrics(font: TTFont, text: str) -> dict[str, float]:
    advance = sum(normalized_advance(font, character) for character in text)
    area = sum(normalized_area(font, character) for character in text)
    return {
        "characters": len(text),
        "advance": advance,
        "advance_per_character": advance / len(text),
        "coverage": area / (advance * 1000),
    }


def raster_coverage(path: Path, text: str) -> float:
    font = ImageFont.truetype(str(path), RASTER_PPEM)
    ink = sum(sum(font.getmask(character, mode="L")) for character in text)
    advance = sum(font.getlength(character) for character in text)
    return ink / (255 * advance * RASTER_PPEM)


def feature_tags(font: TTFont, table_tag: str) -> list[str]:
    if table_tag not in font:
        return []
    feature_list = font[table_tag].table.FeatureList
    if feature_list is None:
        return []
    return sorted({record.FeatureTag for record in feature_list.FeatureRecord})


def family_names(font: TTFont) -> list[str]:
    return sorted(
        {
            record.toUnicode()
            for record in font["name"].names
            if record.nameID == 1
        }
    )


def font_summary(path: Path) -> dict[str, object]:
    font = TTFont(path)
    try:
        os2 = font["OS/2"]
        return {
            "path": str(path),
            "family_names": family_names(font),
            "units_per_em": font["head"].unitsPerEm,
            "weight_class": os2.usWeightClass,
            "cap_height": os2.sCapHeight,
            "x_height": os2.sxHeight,
            "latin": sample_metrics(font, LATIN_SAMPLE),
            "reading": sample_metrics(font, LATIN_READING_SAMPLE),
            "raster_latin_coverage": raster_coverage(path, LATIN_SAMPLE),
            "glyphs": {
                character: glyph_metrics(font, character)
                for character in REFERENCE_GLYPHS
            },
            "gsub_features": feature_tags(font, "GSUB"),
            "gpos_features": feature_tags(font, "GPOS"),
        }
    finally:
        font.close()


def bounds_rms(first: dict[str, object], second: dict[str, object]) -> dict[str, float]:
    x_differences = []
    y_differences = []
    for character in REFERENCE_GLYPHS:
        first_bounds = first["glyphs"][character]["bounds"]
        second_bounds = second["glyphs"][character]["bounds"]
        x_differences.extend(
            (first_bounds[0] - second_bounds[0], first_bounds[2] - second_bounds[2])
        )
        y_differences.extend(
            (first_bounds[1] - second_bounds[1], first_bounds[3] - second_bounds[3])
        )
    return {
        "x": math.sqrt(sum(value * value for value in x_differences) / len(x_differences)),
        "y": math.sqrt(sum(value * value for value in y_differences) / len(y_differences)),
    }


def hangul_mismatches(first: TTFont, second: TTFont) -> list[str]:
    first_cmap = first.getBestCmap()
    second_cmap = second.getBestCmap()
    mismatches = []
    for codepoint in range(0xAC00, 0xD7A4):
        character = chr(codepoint)
        if (
            normalized_advance(first, character) != normalized_advance(second, character)
            or normalized_bounds(first, character) != normalized_bounds(second, character)
            or abs(normalized_area(first, character) - normalized_area(second, character)) > 0.01
            or codepoint not in first_cmap
            or codepoint not in second_cmap
        ):
            mismatches.append(f"U+{codepoint:04X}")
    return mismatches


def figure_mismatches(candidate: TTFont, reference: TTFont) -> list[str]:
    mismatches = []
    for character in DEFAULT_FIGURES:
        if (
            normalized_advance(candidate, character)
            != normalized_advance(reference, character)
            or normalized_bounds(candidate, character)
            != normalized_bounds(reference, character)
            or abs(
                normalized_area(candidate, character)
                - normalized_area(reference, character)
            )
            > 0.01
        ):
            mismatches.append(character)
    return mismatches


def audit(
    ridibatang_path: Path,
    charis_source_path: Path,
    roboto_path: Path,
    charis_path: Path,
) -> dict[str, object]:
    summaries = {
        "ridibatang": font_summary(ridibatang_path),
        "charis_source": font_summary(charis_source_path),
        "roboto": font_summary(roboto_path),
        "charis": font_summary(charis_path),
    }

    ridibatang = TTFont(ridibatang_path)
    roboto = TTFont(roboto_path)
    charis = TTFont(charis_path)
    try:
        hangul = hangul_mismatches(roboto, charis)
        figures = figure_mismatches(charis, roboto)
    finally:
        ridibatang.close()
        roboto.close()
        charis.close()

    roboto_latin = summaries["roboto"]["latin"]
    charis_latin = summaries["charis"]["latin"]
    ridi_latin = summaries["ridibatang"]["latin"]
    comparison = {
        "charis_advance_vs_roboto": (
            charis_latin["advance"] / roboto_latin["advance"]
        ),
        "charis_coverage_vs_roboto": (
            charis_latin["coverage"] / roboto_latin["coverage"]
        ),
        "roboto_coverage_distance_from_ridi": abs(
            roboto_latin["coverage"] - ridi_latin["coverage"]
        ),
        "charis_coverage_distance_from_ridi": abs(
            charis_latin["coverage"] - ridi_latin["coverage"]
        ),
        "roboto_bounds_rms_from_ridi": bounds_rms(
            summaries["roboto"], summaries["ridibatang"]
        ),
        "charis_bounds_rms_from_ridi": bounds_rms(
            summaries["charis"], summaries["ridibatang"]
        ),
    }

    failures = []
    if summaries["charis"]["family_names"] != [CANDIDATE_FAMILY_NAME]:
        failures.append("candidate family name")
    if summaries["charis"]["weight_class"] != 400:
        failures.append("candidate weight class")
    if summaries["charis"]["cap_height"] != 667:
        failures.append("candidate cap height")
    if summaries["charis"]["x_height"] != 477:
        failures.append("candidate x height")
    if hangul:
        failures.append("Hangul changed")
    if figures:
        failures.append("production figures changed")
    if comparison["charis_advance_vs_roboto"] >= 1:
        failures.append("candidate is not narrower")
    if (
        comparison["charis_coverage_distance_from_ridi"]
        >= comparison["roboto_coverage_distance_from_ridi"]
    ):
        failures.append("candidate weight is not closer to RIDIBatang")
    if not {"kern", "mark"} <= set(summaries["charis"]["gpos_features"]):
        failures.append("required positioning features")

    return {
        "pass": not failures,
        "failures": failures,
        "raster_ppem": RASTER_PPEM,
        "samples": {
            "latin": LATIN_SAMPLE,
            "reading": LATIN_READING_SAMPLE,
            "hangul": HANGUL_SAMPLE,
            "reference_glyphs": REFERENCE_GLYPHS,
        },
        "transform": {
            "x_scale": 1.0,
            "y_scale": 1.005,
            "y_shift": -7.0,
        },
        "fonts": summaries,
        "comparison": comparison,
        "hangul_mismatch_count": len(hangul),
        "hangul_mismatch_examples": hangul[:50],
        "figure_mismatch_count": len(figures),
        "figure_mismatch_examples": figures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the Roboto Serif and Charis Regular SNU Jaha comparison."
    )
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--charis-source", required=True)
    parser.add_argument("--roboto", required=True)
    parser.add_argument("--charis", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = audit(
        Path(args.ridibatang),
        Path(args.charis_source),
        Path(args.roboto),
        Path(args.charis),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    status = "PASS" if report["pass"] else "FAIL"
    comparison = report["comparison"]
    print(
        f"{status}: advance={comparison['charis_advance_vs_roboto']:.3f}, "
        f"coverage={comparison['charis_coverage_vs_roboto']:.3f}, "
        f"Hangul mismatches={report['hangul_mismatch_count']}, "
        f"figure mismatches={report['figure_mismatch_count']}, "
        f"failures={','.join(report['failures']) or '-'}"
    )
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
