#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


EXPECTED_GSUB = {"frac", "liga", "lnum", "onum", "pnum", "tnum", "zero"}
EXPECTED_GPOS = {"kern", "mark"}
EXPECTED_REFERENCE_ADVANCES = {"H": 763, "M": 876, "g": 567, "n": 604}
EXPECTED_DEFAULT_FIGURE_ADVANCE = 560
EXPECTED_DEFAULT_FIGURE_BOUNDS = {
    "0": (36, -21, 524, 673),
    "3": (76, -21, 504, 673),
    "8": (50, -25, 510, 677),
}
EXPECTED_ACTIVE_FIGURE_FEATURES = {
    "frac",
    "onum",
    "pnum",
    "sinf",
    "subs",
    "sups",
    "tnum",
    "zero",
}
EXPECTED_DASH_FIGURE_KERNING = {
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


def decoded_names(font: TTFont, name_id: int) -> set[str]:
    return {
        record.toUnicode()
        for record in font["name"].names
        if record.nameID == name_id
    }


def feature_tags(font: TTFont, table_tag: str) -> set[str]:
    if table_tag not in font:
        return set()
    feature_list = font[table_tag].table.FeatureList
    if feature_list is None:
        return set()
    return {record.FeatureTag for record in feature_list.FeatureRecord}


def feature_lookup_indices(font: TTFont, table_tag: str, feature_tag: str) -> list[int]:
    if table_tag not in font:
        return []
    feature_list = font[table_tag].table.FeatureList
    if feature_list is None:
        return []
    return [
        index
        for record in feature_list.FeatureRecord
        if record.FeatureTag == feature_tag
        for index in record.Feature.LookupListIndex
    ]


def pair_position_subtables(lookup):
    if lookup.LookupType == 2:
        yield from lookup.SubTable
    elif lookup.LookupType == 9:
        for extension in lookup.SubTable:
            if extension.ExtensionLookupType == 2:
                yield extension.ExtSubTable


def value_x_advance(value) -> int:
    return getattr(value, "XAdvance", 0) if value is not None else 0


def pair_x_advance(font: TTFont, left: str, right: str) -> int:
    total = 0
    gpos = font["GPOS"].table
    for lookup_index in feature_lookup_indices(font, "GPOS", "kern"):
        lookup = gpos.LookupList.Lookup[lookup_index]
        for subtable in pair_position_subtables(lookup):
            if left not in subtable.Coverage.glyphs:
                continue
            if subtable.Format == 1:
                pair_set = subtable.PairSet[
                    subtable.Coverage.glyphs.index(left)
                ]
                for pair in pair_set.PairValueRecord:
                    if pair.SecondGlyph != right:
                        continue
                    total += value_x_advance(pair.Value1)
                    total += value_x_advance(pair.Value2)
            elif subtable.Format == 2:
                class1 = subtable.ClassDef1.classDefs.get(left, 0)
                class2 = subtable.ClassDef2.classDefs.get(right, 0)
                pair = subtable.Class1Record[class1].Class2Record[class2]
                total += value_x_advance(pair.Value1)
                total += value_x_advance(pair.Value2)
    return total


def verify(path: Path) -> None:
    errors: list[str] = []
    with TTFont(path) as font:
        if "CFF " not in font or "glyf" in font:
            errors.append("output must use CFF outlines")
        if font["head"].unitsPerEm != 1000:
            errors.append("unitsPerEm must be 1000")
        if font["OS/2"].usWeightClass != 400:
            errors.append("weight class must be 400")
        if font["OS/2"].fsType != 0:
            errors.append("embedding must be unrestricted")
        if font["OS/2"].sCapHeight != 654:
            errors.append("cap height must be 654")
        if font["OS/2"].sxHeight != 492:
            errors.append("x-height must be 492")

        cmap = font.getBestCmap()
        hangul_count = sum(0xAC00 <= codepoint <= 0xD7A3 for codepoint in cmap)
        if hangul_count != 11172:
            errors.append(f"modern Hangul coverage is {hangul_count}, expected 11172")
        for character in "가힣Aa0éЖ":
            if ord(character) not in cmap:
                errors.append(f"missing required character U+{ord(character):04X}")
        for character, expected_advance in EXPECTED_REFERENCE_ADVANCES.items():
            glyph_name = cmap[ord(character)]
            actual_advance = font["hmtx"][glyph_name][0]
            if actual_advance != expected_advance:
                errors.append(
                    f"{character} advance is {actual_advance}, "
                    f"expected {expected_advance}"
                )
        for character in "0123456789":
            glyph_name = cmap[ord(character)]
            actual_advance = font["hmtx"][glyph_name][0]
            if actual_advance != EXPECTED_DEFAULT_FIGURE_ADVANCE:
                errors.append(
                    f"{character} advance is {actual_advance}, "
                    f"expected RIDIBatang advance {EXPECTED_DEFAULT_FIGURE_ADVANCE}"
                )
        glyph_set = font.getGlyphSet()
        for character, expected_bounds in EXPECTED_DEFAULT_FIGURE_BOUNDS.items():
            glyph_name = cmap[ord(character)]
            pen = BoundsPen(glyph_set)
            glyph_set[glyph_name].draw(pen)
            actual_bounds = tuple(round(value, 3) for value in pen.bounds)
            if actual_bounds != expected_bounds:
                errors.append(
                    f"{character} bounds are {actual_bounds}, "
                    f"expected RIDIBatang bounds {expected_bounds}"
                )

        if decoded_names(font, 1) != {"SNU Jaha"}:
            errors.append(f"unexpected family names: {sorted(decoded_names(font, 1))}")
        if decoded_names(font, 2) != {"Regular"}:
            errors.append(f"unexpected style names: {sorted(decoded_names(font, 2))}")
        if decoded_names(font, 6) != {"SNUJaha-Regular"}:
            errors.append(
                f"unexpected PostScript names: {sorted(decoded_names(font, 6))}"
            )

        missing_gsub = EXPECTED_GSUB - feature_tags(font, "GSUB")
        missing_gpos = EXPECTED_GPOS - feature_tags(font, "GPOS")
        if missing_gsub:
            errors.append("missing GSUB features: " + ", ".join(sorted(missing_gsub)))
        if missing_gpos:
            errors.append("missing GPOS features: " + ", ".join(sorted(missing_gpos)))
        if feature_lookup_indices(font, "GSUB", "lnum"):
            errors.append("lnum must leave the default RIDIBatang figures unchanged")
        for feature_tag in EXPECTED_ACTIVE_FIGURE_FEATURES:
            if not feature_lookup_indices(font, "GSUB", feature_tag):
                errors.append(f"{feature_tag} figure feature must remain active")
        for dash in "-–—":
            dash_name = cmap[ord(dash)]
            for figure, expected in EXPECTED_DASH_FIGURE_KERNING.items():
                figure_name = cmap[ord(figure)]
                actual = pair_x_advance(font, dash_name, figure_name)
                if actual != expected:
                    errors.append(
                        f"{dash}{figure} kerning is {actual}, expected {expected}"
                    )
        minus_name = cmap[ord("−")]
        for figure in EXPECTED_DASH_FIGURE_KERNING:
            figure_name = cmap[ord(figure)]
            actual = pair_x_advance(font, minus_name, figure_name)
            if actual != 0:
                errors.append(
                    f"−{figure} kerning is {actual}, expected unkerned minus sign"
                )

        if errors:
            raise SystemExit(f"{path} failed verification:\n- " + "\n- ".join(errors))

        print(
            f"{path}: OK; glyphs={len(font.getGlyphOrder())}, "
            f"cmap={len(cmap)}, hangul={hangul_count}, "
            f"GSUB={','.join(sorted(feature_tags(font, 'GSUB')))}, "
            f"GPOS={','.join(sorted(feature_tags(font, 'GPOS')))}"
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_font.py FONT.otf")
    verify(Path(sys.argv[1]))
