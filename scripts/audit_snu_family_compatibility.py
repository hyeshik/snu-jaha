#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import ImageFont


STYLES = (
    ("Thin", 100),
    ("Light", 300),
    ("Regular", 400),
    ("Medium", 500),
    ("SemiBold", 600),
    ("Bold", 700),
    ("ExtraBold", 800),
)
HANGUL_SAMPLE = "자하연연구환경가나다라마바사아흙뿔률쫓빛활괄"
LATIN_SAMPLE = "HAMBURGEFONTSminimumoxygenResearch"
FIGURE_SAMPLE = "00112233445566778899"
REFERENCE_GLYPHS = "HMxngp한가흙0"
RASTER_PPEM = 128


@dataclass(frozen=True)
class FamilySource:
    name: str
    prefix: str
    directory: Path

    def font_path(self, style: str) -> Path:
        return self.directory / f"{self.prefix}-{style}.otf"


def glyph_metrics(font: TTFont, character: str) -> dict[str, object]:
    cmap = font.getBestCmap()
    glyph_name = cmap[ord(character)]
    glyph_set = font.getGlyphSet()
    bounds_pen = BoundsPen(glyph_set)
    area_pen = AreaPen(glyph_set)
    glyph_set[glyph_name].draw(bounds_pen)
    glyph_set[glyph_name].draw(area_pen)
    return {
        "advance": font["hmtx"][glyph_name][0],
        "bounds": [float(value) for value in bounds_pen.bounds],
        "area": abs(float(area_pen.value)),
    }


def sample_metrics(font: TTFont, text: str) -> dict[str, object]:
    metrics = [glyph_metrics(font, character) for character in text]
    upm = font["head"].unitsPerEm
    total_advance = sum(item["advance"] for item in metrics)
    total_area = sum(item["area"] for item in metrics)
    return {
        "advance": total_advance,
        "area": total_area,
        "coverage": total_area / (total_advance * upm),
        "bounds": [
            min(item["bounds"][0] for item in metrics),
            min(item["bounds"][1] for item in metrics),
            max(item["bounds"][2] for item in metrics),
            max(item["bounds"][3] for item in metrics),
        ],
    }


def raster_coverage(path: Path, text: str) -> float:
    font = ImageFont.truetype(str(path), RASTER_PPEM)
    ink = 0
    advance = 0.0
    for character in text:
        ink += int(np.asarray(font.getmask(character, mode="L"), dtype=np.uint8).sum())
        advance += font.getlength(character)
    return ink / (255 * advance * RASTER_PPEM)


def line_metrics(font: TTFont) -> dict[str, int]:
    os2 = font["OS/2"]
    hhea = font["hhea"]
    return {
        "units_per_em": font["head"].unitsPerEm,
        "typo_ascender": os2.sTypoAscender,
        "typo_descender": os2.sTypoDescender,
        "typo_line_gap": os2.sTypoLineGap,
        "typo_box": os2.sTypoAscender - os2.sTypoDescender + os2.sTypoLineGap,
        "hhea_ascender": hhea.ascent,
        "hhea_descender": hhea.descent,
        "hhea_line_gap": hhea.lineGap,
        "hhea_box": hhea.ascent - hhea.descent + hhea.lineGap,
        "win_ascent": os2.usWinAscent,
        "win_descent": os2.usWinDescent,
        "cap_height": os2.sCapHeight,
        "x_height": os2.sxHeight,
    }


def audit_family(source: FamilySource) -> dict[str, object]:
    style_results = []
    for style, weight in STYLES:
        path = source.font_path(style)
        if not path.is_file():
            raise SystemExit(f"missing {source.name} {style}: {path}")
        font = TTFont(path)
        try:
            family_names = {
                record.toUnicode()
                for record in font["name"].names
                if record.nameID == 1
            }
            if family_names != {source.name}:
                raise SystemExit(
                    f"{path}: family names {sorted(family_names)}, "
                    f"expected {source.name}"
                )
            if font["OS/2"].usWeightClass != weight:
                raise SystemExit(
                    f"{path}: weight {font['OS/2'].usWeightClass}, expected {weight}"
                )
            style_results.append(
                {
                    "style": style,
                    "weight": weight,
                    "path": str(path),
                    "hangul": sample_metrics(font, HANGUL_SAMPLE),
                    "latin": sample_metrics(font, LATIN_SAMPLE),
                    "figures": sample_metrics(font, FIGURE_SAMPLE),
                    "raster_hangul_coverage": raster_coverage(
                        path,
                        HANGUL_SAMPLE,
                    ),
                    "raster_latin_coverage": raster_coverage(
                        path,
                        LATIN_SAMPLE,
                    ),
                    "glyphs": {
                        character: glyph_metrics(font, character)
                        for character in REFERENCE_GLYPHS
                    },
                }
            )
            if style == "Regular":
                regular_line_metrics = line_metrics(font)
        finally:
            font.close()

    regular = next(
        item for item in style_results if item["style"] == "Regular"
    )
    for item in style_results:
        for script in ("hangul", "latin", "figures"):
            item[script]["relative_to_regular"] = (
                item[script]["coverage"] / regular[script]["coverage"]
            )
        item["raster_hangul_relative_to_regular"] = (
            item["raster_hangul_coverage"]
            / regular["raster_hangul_coverage"]
        )
        item["raster_latin_relative_to_regular"] = (
            item["raster_latin_coverage"]
            / regular["raster_latin_coverage"]
        )

    return {
        "name": source.name,
        "prefix": source.prefix,
        "directory": str(source.directory),
        "line_metrics": regular_line_metrics,
        "styles": style_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure size, weight, and baseline compatibility across SNU fonts."
    )
    parser.add_argument("--jaha-dir", required=True)
    parser.add_argument("--appendard-dir", required=True)
    parser.add_argument("--edge-dir", required=True)
    parser.add_argument("--sprout-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    sources = (
        FamilySource("SNU Jaha", "SNUJaha", Path(args.jaha_dir)),
        FamilySource(
            "SNU Appendard",
            "SNUAppendard",
            Path(args.appendard_dir),
        ),
        FamilySource("SNU Edge", "SNUEdge", Path(args.edge_dir)),
        FamilySource("SNU Sprout", "SNUSprout", Path(args.sprout_dir)),
    )
    report = {
        "raster_ppem": RASTER_PPEM,
        "samples": {
            "hangul": HANGUL_SAMPLE,
            "latin": LATIN_SAMPLE,
            "figures": FIGURE_SAMPLE,
        },
        "styles": [
            {"style": style, "weight": weight} for style, weight in STYLES
        ],
        "families": [audit_family(source) for source in sources],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"{output}: families={len(sources)}, styles={len(STYLES)}, "
        f"raster_ppem={RASTER_PPEM}"
    )


if __name__ == "__main__":
    main()
