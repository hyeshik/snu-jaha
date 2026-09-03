#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from fontTools.otlLib.builder import (
    buildLookup,
    buildPairPosClassesSubtable,
    buildValue,
)
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

from build_jaha import is_hangul_codepoint, should_keep_ridi_codepoint


DEFAULT_MIN_GUARD = 20
DEFAULT_CLEARANCE = 30
DEFAULT_BUCKET_SIZE = 5


class GuardStats(NamedTuple):
    guarded_glyphs: int
    hangul_glyphs: int
    guarded_classes: int
    hangul_classes: int
    guard_min: int
    guard_max: int
    lookup_index: int


def round_up(value: float, step: int) -> int:
    return int(math.ceil(value / step) * step)


def round_down(value: float, step: int) -> int:
    return int(math.floor(value / step) * step)


def guard_units(
    *,
    right_overhang: float,
    hangul_left_side_bearing: float,
    minimum: int = DEFAULT_MIN_GUARD,
    clearance: int = DEFAULT_CLEARANCE,
    bucket_size: int = DEFAULT_BUCKET_SIZE,
) -> int:
    required = right_overhang + clearance - hangul_left_side_bearing
    return max(minimum, round_up(required, bucket_size))


def glyph_bounds(glyph_set, glyph_name: str):
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return pen.bounds


def encoded_glyph_codepoints(font: TTFont) -> dict[str, set[int]]:
    codepoints: dict[str, set[int]] = defaultdict(set)
    for codepoint, glyph_name in font.getBestCmap().items():
        codepoints[glyph_name].add(codepoint)
    return codepoints


def is_guard_input_codepoint(codepoint: int) -> bool:
    return (
        not should_keep_ridi_codepoint(codepoint)
        and unicodedata.category(chr(codepoint))[0] in {"L", "N"}
    )


def encoded_latin_and_figure_glyphs(font: TTFont) -> set[str]:
    return {
        glyph_name
        for glyph_name, codepoints in encoded_glyph_codepoints(font).items()
        if any(is_guard_input_codepoint(codepoint) for codepoint in codepoints)
    }


def substitution_outputs(subtable, available: set[str]) -> set[str]:
    if hasattr(subtable, "ExtSubTable"):
        return substitution_outputs(subtable.ExtSubTable, available)

    outputs: set[str] = set()
    mapping = getattr(subtable, "mapping", None)
    if mapping:
        outputs.update(target for source, target in mapping.items() if source in available)

    alternates = getattr(subtable, "alternates", None)
    if alternates:
        for source, targets in alternates.items():
            if source in available:
                outputs.update(targets)

    ligatures = getattr(subtable, "ligatures", None)
    if ligatures:
        for first, candidates in ligatures.items():
            if first not in available:
                continue
            for ligature in candidates:
                if all(component in available for component in ligature.Component):
                    outputs.add(ligature.LigGlyph)
    return outputs


def terminal_latin_and_figure_glyphs(font: TTFont) -> set[str]:
    glyphs = encoded_latin_and_figure_glyphs(font)
    if "GSUB" not in font:
        return glyphs

    lookups = font["GSUB"].table.LookupList
    if lookups is None:
        return glyphs
    while True:
        discovered = set()
        for lookup in lookups.Lookup:
            for subtable in lookup.SubTable:
                discovered.update(substitution_outputs(subtable, glyphs))
        discovered -= glyphs
        if not discovered:
            return glyphs
        glyphs.update(discovered)


def collect_geometry_classes(
    font: TTFont,
    bucket_size: int,
) -> tuple[dict[int, tuple[str, ...]], dict[int, tuple[str, ...]]]:
    glyph_set = font.getGlyphSet()
    hmtx = font["hmtx"]
    guarded_classes: dict[int, list[str]] = defaultdict(list)
    hangul_classes: dict[int, list[str]] = defaultdict(list)

    for glyph_name in terminal_latin_and_figure_glyphs(font):
        bounds = glyph_bounds(glyph_set, glyph_name)
        if bounds is None:
            continue
        advance_width = hmtx[glyph_name][0]
        right_overhang = bounds[2] - advance_width
        guarded_classes[round_up(right_overhang, bucket_size)].append(glyph_name)

    for glyph_name, codepoints in encoded_glyph_codepoints(font).items():
        if not any(is_hangul_codepoint(codepoint) for codepoint in codepoints):
            continue
        bounds = glyph_bounds(glyph_set, glyph_name)
        if bounds is not None:
            hangul_classes[round_down(bounds[0], bucket_size)].append(glyph_name)

    return (
        {key: tuple(sorted(value)) for key, value in guarded_classes.items()},
        {key: tuple(sorted(value)) for key, value in hangul_classes.items()},
    )


def append_guard_lookup(
    font: TTFont,
    *,
    minimum: int = DEFAULT_MIN_GUARD,
    clearance: int = DEFAULT_CLEARANCE,
    bucket_size: int = DEFAULT_BUCKET_SIZE,
) -> GuardStats:
    if "GPOS" not in font:
        raise ValueError("The input font has no GPOS table.")
    if font["post"].italicAngle == 0:
        raise ValueError("The input font is not marked as italic.")

    guarded_classes, hangul_classes = collect_geometry_classes(font, bucket_size)
    if not guarded_classes:
        raise ValueError("The input font has no non-CJK terminal letters or figures.")
    if not hangul_classes:
        raise ValueError("The input font has no Hangul glyphs.")

    pairs = {}
    guard_values = []
    for right_overhang, guarded_glyphs in guarded_classes.items():
        for left_side_bearing, hangul_glyphs in hangul_classes.items():
            guard = guard_units(
                right_overhang=right_overhang,
                hangul_left_side_bearing=left_side_bearing,
                minimum=minimum,
                clearance=clearance,
                bucket_size=bucket_size,
            )
            pairs[(guarded_glyphs, hangul_glyphs)] = (
                buildValue({"XAdvance": guard}),
                buildValue({}),
            )
            guard_values.append(guard)

    subtable = buildPairPosClassesSubtable(pairs, font.getReverseGlyphMap())
    lookup = buildLookup([subtable], table="GPOS")
    gpos = font["GPOS"].table
    lookup_index = len(gpos.LookupList.Lookup)
    gpos.LookupList.Lookup.append(lookup)
    gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)

    kern_features = [
        record.Feature
        for record in gpos.FeatureList.FeatureRecord
        if record.FeatureTag == "kern"
    ]
    if not kern_features:
        raise ValueError("The input font has no GPOS kern feature.")
    for feature in kern_features:
        feature.LookupListIndex.append(lookup_index)
        feature.LookupCount = len(feature.LookupListIndex)

    return GuardStats(
        guarded_glyphs=sum(map(len, guarded_classes.values())),
        hangul_glyphs=sum(map(len, hangul_classes.values())),
        guarded_classes=len(guarded_classes),
        hangul_classes=len(hangul_classes),
        guard_min=min(guard_values),
        guard_max=max(guard_values),
        lookup_index=lookup_index,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add italic letter/figure-to-upright-Hangul optical guards."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--minimum", type=int, default=DEFAULT_MIN_GUARD)
    parser.add_argument("--clearance", type=int, default=DEFAULT_CLEARANCE)
    parser.add_argument("--bucket-size", type=int, default=DEFAULT_BUCKET_SIZE)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Input and output paths must differ.")

    font = TTFont(args.input)
    try:
        stats = append_guard_lookup(
            font,
            minimum=args.minimum,
            clearance=args.clearance,
            bucket_size=args.bucket_size,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        font.save(args.output)
    finally:
        font.close()
    print(
        f"{args.output}: guarded_glyphs={stats.guarded_glyphs}, "
        f"hangul_glyphs={stats.hangul_glyphs}, "
        f"guarded_classes={stats.guarded_classes}, "
        f"hangul_classes={stats.hangul_classes}, "
        f"guard_range={stats.guard_min}..{stats.guard_max}, "
        f"lookup_index={stats.lookup_index}"
    )


if __name__ == "__main__":
    main()
