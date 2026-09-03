#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from fontTools.otlLib.builder import (
    buildLookup,
    buildPairPosGlyphsSubtable,
    buildValue,
)
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from add_italic_cjk_guard import GuardStats, append_guard_lookup


HORIZONTAL_VALUE_FIELDS = ("XPlacement", "XAdvance")
BUILD_TIMESTAMP = 3871152000  # 2026-09-02 00:00:00 UTC in the OpenType epoch.
KERN_SCALE = 0.895
DEFAULT_FIGURES = "0123456789"
DEFAULT_FIGURE_ADVANCE = 520
DASHES_WITH_FIGURE_KERNING = "-–—"
DASH_FIGURE_KERNING = {
    "0": -15,
    "1": -20,
    "2": -40,
    "3": -20,
    "4": -30,
    "5": -20,
    "6": 0,
    "7": -30,
    "8": 0,
    "9": 0,
}


@dataclass(frozen=True)
class StyleMetrics:
    cap_height: int
    x_height: int


STYLE_METRICS = {
    "Thin": StyleMetrics(
        cap_height=654,
        x_height=492,
    ),
    "Light": StyleMetrics(
        cap_height=654,
        x_height=492,
    ),
    "Regular": StyleMetrics(
        cap_height=654,
        x_height=492,
    ),
    "Medium": StyleMetrics(
        cap_height=654,
        x_height=492,
    ),
    "SemiBold": StyleMetrics(
        cap_height=654,
        x_height=493,
    ),
    "Bold": StyleMetrics(
        cap_height=654,
        x_height=494,
    ),
    "ExtraBold": StyleMetrics(
        cap_height=654,
        x_height=494,
    ),
}
CAP_HEIGHT = STYLE_METRICS["Regular"].cap_height
X_HEIGHT = STYLE_METRICS["Regular"].x_height


def resolved_style_metrics(
    style: str,
    cap_height: int | None = None,
    x_height: int | None = None,
) -> StyleMetrics:
    default = STYLE_METRICS[style]
    return StyleMetrics(
        cap_height=default.cap_height if cap_height is None else cap_height,
        x_height=default.x_height if x_height is None else x_height,
    )


def pair_position_subtables(lookup):
    if lookup.LookupType == 2:
        yield from lookup.SubTable
    elif lookup.LookupType == 9:
        for extension in lookup.SubTable:
            if extension.ExtensionLookupType == 2:
                yield extension.ExtSubTable


def scale_value_record(value, factor: float) -> int:
    if value is None:
        return 0
    changed = 0
    for field in HORIZONTAL_VALUE_FIELDS:
        amount = getattr(value, field, None)
        if amount is None:
            continue
        scaled = round(amount * factor)
        if scaled != amount:
            setattr(value, field, scaled)
            changed += 1
    return changed


def scale_pair_subtable(subtable, factor: float) -> int:
    changed = 0
    if subtable.Format == 1:
        for pair_set in subtable.PairSet:
            for pair in pair_set.PairValueRecord:
                changed += scale_value_record(pair.Value1, factor)
                changed += scale_value_record(pair.Value2, factor)
    elif subtable.Format == 2:
        for class1 in subtable.Class1Record:
            for class2 in class1.Class2Record:
                changed += scale_value_record(class2.Value1, factor)
                changed += scale_value_record(class2.Value2, factor)
    return changed


def kern_lookup_indices(font: TTFont) -> set[int]:
    if "GPOS" not in font:
        return set()
    feature_list = font["GPOS"].table.FeatureList
    if feature_list is None:
        return set()
    return {
        index
        for record in feature_list.FeatureRecord
        if record.FeatureTag == "kern"
        for index in record.Feature.LookupListIndex
    }


def scale_kerning(font: TTFont, factor: float) -> tuple[int, int]:
    indices = kern_lookup_indices(font)
    changed = 0
    lookups = font["GPOS"].table.LookupList.Lookup if indices else []
    for index in sorted(indices):
        for subtable in pair_position_subtables(lookups[index]):
            changed += scale_pair_subtable(subtable, factor)
    if "kern" in font:
        for subtable in font["kern"].kernTables:
            pairs = getattr(subtable, "kernTable", None)
            if pairs is None:
                continue
            for pair, amount in list(pairs.items()):
                pairs[pair] = round(amount * factor)
    return len(indices), changed


def dash_figure_adjustments(cmap: dict[int, str]) -> dict[tuple[str, str], int]:
    return {
        (cmap[ord(dash)], cmap[ord(figure)]): amount
        for dash in DASHES_WITH_FIGURE_KERNING
        for figure, amount in DASH_FIGURE_KERNING.items()
        if amount
    }


def add_dash_figure_kerning(font: TTFont) -> int:
    if "GPOS" not in font:
        return 0
    gpos = font["GPOS"].table
    if gpos.FeatureList is None or gpos.LookupList is None:
        return 0

    adjustments = dash_figure_adjustments(font.getBestCmap())
    pairs = {
        pair: (buildValue({"XAdvance": amount}), buildValue({}))
        for pair, amount in adjustments.items()
    }
    subtable = buildPairPosGlyphsSubtable(pairs, font.getReverseGlyphMap())
    lookup = buildLookup([subtable], table="GPOS")
    lookup_index = len(gpos.LookupList.Lookup)
    gpos.LookupList.Lookup.append(lookup)
    gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)

    for record in gpos.FeatureList.FeatureRecord:
        if record.FeatureTag != "kern":
            continue
        record.Feature.LookupListIndex.append(lookup_index)
        record.Feature.LookupCount = len(record.Feature.LookupListIndex)
    return len(adjustments)


def encoded_charstring_width(width: int, private) -> int | None:
    if width == private.defaultWidthX:
        return None
    return width - private.nominalWidthX


def figure_horizontal_transform(
    source_advance: int,
    target_advance: int,
) -> tuple[float, float]:
    scale = target_advance / source_advance
    shift = (target_advance - source_advance * scale) / 2
    return scale, shift


def replace_default_figures(
    font: TTFont,
    ridibatang: TTFont,
    figure_advance: int = DEFAULT_FIGURE_ADVANCE,
) -> int:
    target_cmap = font.getBestCmap()
    source_cmap = ridibatang.getBestCmap()
    source_glyphs = ridibatang.getGlyphSet()
    top_dict = font["CFF "].cff.topDictIndex[0]
    private = top_dict.Private

    replaced = 0
    for character in DEFAULT_FIGURES:
        codepoint = ord(character)
        target_name = target_cmap[codepoint]
        source_name = source_cmap[codepoint]
        source_width, source_lsb = ridibatang["hmtx"][source_name]
        target_width = figure_advance
        x_scale, x_shift = figure_horizontal_transform(
            source_width,
            target_width,
        )

        pen = T2CharStringPen(
            encoded_charstring_width(target_width, private), glyphSet=None
        )
        source_glyphs[source_name].draw(
            TransformPen(pen, (x_scale, 0, 0, 1, x_shift, 0))
        )
        top_dict.CharStrings[target_name] = pen.getCharString(
            private=private,
            globalSubrs=top_dict.GlobalSubrs,
        )
        target_lsb = round(source_lsb * x_scale + x_shift)
        font["hmtx"][target_name] = (target_width, target_lsb)
        replaced += 1
    return replaced


def uses_ridibatang_default_figures(italic: bool) -> bool:
    return not italic


def make_lining_figures_default(font: TTFont) -> int:
    if "GSUB" not in font:
        return 0
    feature_list = font["GSUB"].table.FeatureList
    if feature_list is None:
        return 0
    changed = 0
    for record in feature_list.FeatureRecord:
        if record.FeatureTag != "lnum":
            continue
        changed += len(record.Feature.LookupListIndex)
        record.Feature.LookupListIndex = []
        record.Feature.LookupCount = 0
    return changed


def finalize(
    source: Path,
    ridibatang_path: Path,
    output: Path,
    kern_scale: float,
    style: str,
    cap_height: int | None = None,
    x_height: int | None = None,
    figure_advance: int = DEFAULT_FIGURE_ADVANCE,
    italic: bool = False,
) -> None:
    metrics = resolved_style_metrics(style, cap_height, x_height)
    font = TTFont(source, recalcTimestamp=False)
    ridibatang = (
        TTFont(ridibatang_path)
        if uses_ridibatang_default_figures(italic)
        else None
    )
    try:
        if ridibatang is None:
            default_figure_source = "Roboto Serif"
            replaced_figures = 0
            disabled_lnum_lookups = 0
        else:
            default_figure_source = "RIDIBatang"
            replaced_figures = replace_default_figures(
                font,
                ridibatang,
                figure_advance,
            )
            disabled_lnum_lookups = make_lining_figures_default(font)
        lookup_count, value_count = scale_kerning(font, kern_scale)
        dash_figure_pairs = 0 if italic else add_dash_figure_kerning(font)
        guard_stats: GuardStats | None = (
            append_guard_lookup(font) if italic else None
        )
        figure_advances = {
            font["hmtx"][font.getBestCmap()[ord(character)]][0]
            for character in DEFAULT_FIGURES
        }
        font["head"].fontRevision = 0.1
        font["head"].created = BUILD_TIMESTAMP
        font["head"].modified = BUILD_TIMESTAMP
        font["head"].macStyle = (
            (1 if style == "Bold" else 0) | (2 if italic else 0)
        )
        font["OS/2"].fsSelection = (
            (1 if italic else 0)
            | (32 if style == "Bold" else 0)
            | (64 if style == "Regular" and not italic else 0)
        )
        font["OS/2"].sCapHeight = metrics.cap_height
        font["OS/2"].sxHeight = metrics.x_height
        for table_tag in ("DSIG", "FFTM"):
            if table_tag in font:
                del font[table_tag]
        output.parent.mkdir(parents=True, exist_ok=True)
        font.save(output, reorderTables=False)
    finally:
        if ridibatang is not None:
            ridibatang.close()
        font.close()
    print(
        f"{output}: style={style}, default_figure_source={default_figure_source}, "
        f"replaced_default_figures={replaced_figures}, "
        f"disabled_lnum_lookups={disabled_lnum_lookups}, "
        f"dash_figure_pairs={dash_figure_pairs}, "
        f"figure_advances={','.join(map(str, sorted(figure_advances)))}, "
        f"kern_lookups={lookup_count}, "
        f"kern_values_scaled={value_count}, kern_scale={kern_scale:.3f}, "
        f"italic_guard="
        f"{guard_stats.guard_min if guard_stats else 'none'}"
        f"{('..' + str(guard_stats.guard_max)) if guard_stats else ''}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--kern-scale", type=float, default=KERN_SCALE)
    parser.add_argument("--style", choices=STYLE_METRICS, default="Regular")
    parser.add_argument("--cap-height", type=int)
    parser.add_argument("--x-height", type=int)
    parser.add_argument(
        "--figure-advance",
        type=int,
        default=DEFAULT_FIGURE_ADVANCE,
    )
    parser.add_argument("--italic", action="store_true")
    args = parser.parse_args()
    finalize(
        Path(args.input),
        Path(args.ridibatang),
        Path(args.output),
        args.kern_scale,
        args.style,
        args.cap_height,
        args.x_height,
        args.figure_advance,
        args.italic,
    )


if __name__ == "__main__":
    main()
