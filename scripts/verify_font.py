#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


EXPECTED_GSUB = {"frac", "liga", "lnum", "onum", "pnum", "tnum", "zero"}
EXPECTED_GPOS = {"kern", "mark"}
EXPECTED_DEFAULT_FIGURE_ADVANCE = 560
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


@dataclass(frozen=True)
class StyleProfile:
    weight_class: int
    postscript_name: str
    fs_selection: int
    mac_style: int
    cap_height: int
    x_height: int
    reference_advances: dict[str, int]
    figure_bounds: dict[str, tuple[float, float, float, float]]


STYLE_PROFILES = {
    "Thin": StyleProfile(
        weight_class=100,
        postscript_name="SNUJaha-Thin",
        fs_selection=0,
        mac_style=0,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 729, "M": 840, "g": 557, "n": 585},
        figure_bounds={
            "0": (46, -11, 514, 663),
            "3": (87, -11, 493, 663),
            "8": (60, -15, 500, 667),
        },
    ),
    "Light": StyleProfile(
        weight_class=300,
        postscript_name="SNUJaha-Light",
        fs_selection=0,
        mac_style=0,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 752, "M": 864, "g": 563, "n": 598},
        figure_bounds={
            "0": (39, -18, 521, 670),
            "3": (79, -18, 501, 670),
            "8": (53, -22, 507, 674),
        },
    ),
    "Regular": StyleProfile(
        weight_class=400,
        postscript_name="SNUJaha-Regular",
        fs_selection=64,
        mac_style=0,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 763, "M": 876, "g": 567, "n": 604},
        figure_bounds={
            "0": (36, -21, 524, 673),
            "3": (76, -21, 504, 673),
            "8": (50, -25, 510, 677),
        },
    ),
    "Medium": StyleProfile(
        weight_class=500,
        postscript_name="SNUJaha-Medium",
        fs_selection=0,
        mac_style=0,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 762, "M": 880, "g": 575, "n": 609},
        figure_bounds={
            "0": (33, -21, 527, 673),
            "3": (72, -21, 508, 673),
            "8": (46, -25, 514, 677),
        },
    ),
    "SemiBold": StyleProfile(
        weight_class=600,
        postscript_name="SNUJaha-SemiBold",
        fs_selection=0,
        mac_style=0,
        cap_height=654,
        x_height=493,
        reference_advances={"H": 760, "M": 882, "g": 584, "n": 616},
        figure_bounds={
            "0": (30, -21, 530, 673),
            "3": (69, -21, 511, 673),
            "8": (43, -25, 517, 677),
        },
    ),
    "Bold": StyleProfile(
        weight_class=700,
        postscript_name="SNUJaha-Bold",
        fs_selection=32,
        mac_style=1,
        cap_height=654,
        x_height=494,
        reference_advances={"H": 758, "M": 887, "g": 593, "n": 622},
        figure_bounds={
            "0": (27, -21, 533, 673),
            "3": (65, -21, 515, 673),
            "8": (40, -25, 520, 677),
        },
    ),
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
        style_names = decoded_names(font, 2)
        if len(style_names) != 1 or not style_names <= STYLE_PROFILES.keys():
            errors.append(f"unexpected style names: {sorted(style_names)}")
            style_name = "Regular"
        else:
            style_name = next(iter(style_names))
        profile = STYLE_PROFILES[style_name]

        if "CFF " not in font or "glyf" in font:
            errors.append("output must use CFF outlines")
        if font["head"].unitsPerEm != 1000:
            errors.append("unitsPerEm must be 1000")
        if font["OS/2"].usWeightClass != profile.weight_class:
            errors.append(f"weight class must be {profile.weight_class}")
        if font["OS/2"].fsSelection != profile.fs_selection:
            errors.append(f"fsSelection must be {profile.fs_selection}")
        if font["head"].macStyle != profile.mac_style:
            errors.append(f"macStyle must be {profile.mac_style}")
        if font["OS/2"].fsType != 0:
            errors.append("embedding must be unrestricted")
        if font["OS/2"].sCapHeight != profile.cap_height:
            errors.append(f"cap height must be {profile.cap_height}")
        if font["OS/2"].sxHeight != profile.x_height:
            errors.append(f"x-height must be {profile.x_height}")

        cmap = font.getBestCmap()
        hangul_count = sum(0xAC00 <= codepoint <= 0xD7A3 for codepoint in cmap)
        if hangul_count != 11172:
            errors.append(f"modern Hangul coverage is {hangul_count}, expected 11172")
        for character in "가힣Aa0éЖ":
            if ord(character) not in cmap:
                errors.append(f"missing required character U+{ord(character):04X}")
        for character, expected_advance in profile.reference_advances.items():
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
        zero_name = cmap[ord("0")]
        zero_zero_kerning = pair_x_advance(font, zero_name, zero_name)
        if zero_zero_kerning != 0:
            errors.append(
                f"00 kerning is {zero_zero_kerning}; "
                "tabular default figures must remain unkerned"
            )
        glyph_set = font.getGlyphSet()
        for character, expected_bounds in profile.figure_bounds.items():
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
        if decoded_names(font, 6) != {profile.postscript_name}:
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
            f"{path}: OK; style={style_name}, glyphs={len(font.getGlyphOrder())}, "
            f"cmap={len(cmap)}, hangul={hangul_count}, "
            f"GSUB={','.join(sorted(feature_tags(font, 'GSUB')))}, "
            f"GPOS={','.join(sorted(feature_tags(font, 'GPOS')))}"
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_font.py FONT.otf")
    verify(Path(sys.argv[1]))
