#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont


EXPECTED_GSUB = {"frac", "liga", "lnum", "onum", "pnum", "tnum", "zero"}
EXPECTED_GPOS = {"kern", "mark"}
EXPECTED_DEFAULT_FIGURE_ADVANCE = 520
EXPECTED_ITALIC_FIGURE_ADVANCE = 498
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
    cap_height: int
    x_height: int
    reference_advances: dict[str, int]
    italic_reference_advances: dict[str, int]
    figure_bounds: dict[str, tuple[float, float, float, float]]


STYLE_PROFILES = {
    "Thin": StyleProfile(
        weight_class=100,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 700, "M": 806, "g": 536, "n": 565},
        italic_reference_advances={"H": 696, "M": 797, "g": 512, "n": 541},
        figure_bounds={
            "0": (42, -11, 478, 663),
            "3": (81, -11, 458, 663),
            "8": (56, -15, 464, 667),
        },
    ),
    "Light": StyleProfile(
        weight_class=300,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 720, "M": 828, "g": 542, "n": 575},
        italic_reference_advances={"H": 717, "M": 820, "g": 530, "n": 555},
        figure_bounds={
            "0": (36, -18, 484, 670),
            "3": (73, -18, 465, 670),
            "8": (49, -22, 471, 674),
        },
    ),
    "Regular": StyleProfile(
        weight_class=400,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 731, "M": 839, "g": 545, "n": 581},
        italic_reference_advances={"H": 729, "M": 831, "g": 539, "n": 562},
        figure_bounds={
            "0": (33, -21, 487, 673),
            "3": (71, -21, 468, 673),
            "8": (46, -25, 474, 677),
        },
    ),
    "Medium": StyleProfile(
        weight_class=500,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 729, "M": 843, "g": 554, "n": 588},
        italic_reference_advances={"H": 727, "M": 836, "g": 549, "n": 569},
        figure_bounds={
            "0": (30, -21, 490, 673),
            "3": (67, -21, 472, 673),
            "8": (43, -25, 477, 677),
        },
    ),
    "SemiBold": StyleProfile(
        weight_class=600,
        cap_height=654,
        x_height=493,
        reference_advances={"H": 728, "M": 847, "g": 564, "n": 594},
        italic_reference_advances={"H": 726, "M": 841, "g": 558, "n": 576},
        figure_bounds={
            "0": (28, -21, 492, 673),
            "3": (64, -21, 475, 673),
            "8": (40, -25, 480, 677),
        },
    ),
    "Bold": StyleProfile(
        weight_class=700,
        cap_height=654,
        x_height=494,
        reference_advances={"H": 727, "M": 851, "g": 573, "n": 600},
        italic_reference_advances={"H": 725, "M": 845, "g": 568, "n": 583},
        figure_bounds={
            "0": (25, -21, 495, 673),
            "3": (61, -21, 478, 673),
            "8": (37, -25, 483, 677),
        },
    ),
    "ExtraBold": StyleProfile(
        weight_class=800,
        cap_height=654,
        x_height=494,
        reference_advances={"H": 727, "M": 853, "g": 577, "n": 603},
        italic_reference_advances={"H": 724, "M": 848, "g": 573, "n": 587},
        figure_bounds={
            "0": (23, -21, 497, 673),
            "3": (59, -21, 480, 673),
            "8": (35, -25, 485, 677),
        },
    ),
}

ITALIC_FIGURE_BOUNDS = {
    "Thin": {
        "0": (30.619, -21.296, 468.276, 598.334),
        "3": (-3.389, -79.328, 457.533, 598.337),
        "8": (21.666, -20.361, 475.43, 665.726),
    },
    "Light": {
        "0": (27.936, -21.296, 466.485, 598.338),
        "3": (-9.654, -80.264, 456.642, 598.341),
        "8": (13.616, -20.361, 475.438, 665.729),
    },
    "Regular": {
        "0": (26.147, -21.296, 466.485, 598.336),
        "3": (-13.235, -80.264, 455.745, 598.337),
        "8": (10.03, -20.361, 474.536, 665.728),
    },
    "Medium": {
        "0": (23.46, -21.296, 469.169, 599.272),
        "3": (-15.025, -80.264, 461.113, 598.332),
        "8": (7.351, -20.359, 479.906, 665.73),
    },
    "SemiBold": {
        "0": (21.667, -21.296, 472.748, 599.272),
        "3": (-16.814, -80.264, 465.591, 599.271),
        "8": (4.66, -20.361, 485.276, 665.728),
    },
    "Bold": {
        "0": (18.985, -21.296, 476.33, 600.206),
        "3": (-19.5, -80.264, 470.066, 600.207),
        "8": (1.982, -20.359, 490.65, 665.729),
    },
    "ExtraBold": {
        "0": (18.09, -21.296, 478.12, 600.206),
        "3": (-20.395, -80.264, 471.855, 600.204),
        "8": (1.076, -20.36, 493.329, 665.728),
    },
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


def contour_control_bounds(glyph_set, glyph_name: str):
    recording = RecordingPen()
    glyph_set[glyph_name].draw(recording)
    contours = []
    points = []
    for operator, operands in recording.value:
        if operator == "moveTo":
            points = []
        if operator in {"moveTo", "lineTo", "curveTo", "qCurveTo"}:
            points.extend(point for point in operands if point is not None)
        if operator in {"closePath", "endPath"} and points:
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            contours.append((min(xs), min(ys), max(xs), max(ys)))
            points = []
    return contours


def has_detached_capital_a_crossbar(glyph_set, glyph_name: str) -> bool:
    return any(
        y_max - y_min <= 150 and x_max - x_min >= 100
        for x_min, y_min, x_max, y_max in contour_control_bounds(
            glyph_set,
            glyph_name,
        )
    )


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


def italic_guard_is_attached(font: TTFont) -> bool:
    if "GPOS" not in font:
        return False
    gpos = font["GPOS"].table
    if gpos.LookupList is None or not gpos.LookupList.Lookup:
        return False
    guard_index = len(gpos.LookupList.Lookup) - 1
    guard_lookup = gpos.LookupList.Lookup[guard_index]
    if guard_lookup.LookupType != 2 or not guard_lookup.SubTable:
        return False
    if not all(subtable.Format == 2 for subtable in guard_lookup.SubTable):
        return False
    kern_features = [
        record.Feature
        for record in gpos.FeatureList.FeatureRecord
        if record.FeatureTag == "kern"
    ]
    return bool(kern_features) and all(
        guard_index in feature.LookupListIndex for feature in kern_features
    )


def verify(path: Path) -> None:
    errors: list[str] = []
    with TTFont(path) as font:
        style_names = decoded_names(font, 2)
        if len(style_names) != 1:
            errors.append(f"unexpected style names: {sorted(style_names)}")
            style_name = "Regular"
            italic = False
        else:
            output_style_name = next(iter(style_names))
            italic = output_style_name.endswith(" Italic")
            style_name = output_style_name.removesuffix(" Italic")
            if style_name not in STYLE_PROFILES:
                errors.append(f"unexpected style names: {sorted(style_names)}")
                style_name = "Regular"
        profile = STYLE_PROFILES[style_name]
        expected_fs_selection = (
            (1 if italic else 0)
            | (32 if style_name == "Bold" else 0)
            | (64 if style_name == "Regular" and not italic else 0)
        )
        expected_mac_style = (
            (1 if style_name == "Bold" else 0) | (2 if italic else 0)
        )

        if "CFF " not in font or "glyf" in font:
            errors.append("output must use CFF outlines")
        if font["head"].unitsPerEm != 1000:
            errors.append("unitsPerEm must be 1000")
        if font["OS/2"].usWeightClass != profile.weight_class:
            errors.append(f"weight class must be {profile.weight_class}")
        if font["OS/2"].fsSelection != expected_fs_selection:
            errors.append(f"fsSelection must be {expected_fs_selection}")
        if font["head"].macStyle != expected_mac_style:
            errors.append(f"macStyle must be {expected_mac_style}")
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
        reference_advances = (
            profile.italic_reference_advances
            if italic
            else profile.reference_advances
        )
        for character, expected_advance in reference_advances.items():
            glyph_name = cmap[ord(character)]
            actual_advance = font["hmtx"][glyph_name][0]
            if actual_advance != expected_advance:
                errors.append(
                    f"{character} advance is {actual_advance}, "
                    f"expected {expected_advance}"
                )
        expected_figure_advance = (
            EXPECTED_ITALIC_FIGURE_ADVANCE
            if italic
            else EXPECTED_DEFAULT_FIGURE_ADVANCE
        )
        for character in "0123456789":
            glyph_name = cmap[ord(character)]
            actual_advance = font["hmtx"][glyph_name][0]
            if actual_advance != expected_figure_advance:
                errors.append(
                    f"{character} advance is {actual_advance}, "
                    f"expected {'Roboto Serif' if italic else 'RIDIBatang'} "
                    f"advance {expected_figure_advance}"
                )
        zero_name = cmap[ord("0")]
        zero_zero_kerning = pair_x_advance(font, zero_name, zero_name)
        if zero_zero_kerning != 0:
            errors.append(
                f"00 kerning is {zero_zero_kerning}; "
                "tabular default figures must remain unkerned"
            )
        glyph_set = font.getGlyphSet()
        capital_a_name = cmap[ord("A")]
        if has_detached_capital_a_crossbar(glyph_set, capital_a_name):
            errors.append("A crossbar remains a detached overlapping contour")
        expected_figure_bounds = (
            ITALIC_FIGURE_BOUNDS[style_name]
            if italic
            else profile.figure_bounds
        )
        for character, expected_bounds in expected_figure_bounds.items():
            glyph_name = cmap[ord(character)]
            pen = BoundsPen(glyph_set)
            glyph_set[glyph_name].draw(pen)
            actual_bounds = tuple(round(value, 3) for value in pen.bounds)
            if actual_bounds != expected_bounds:
                errors.append(
                    f"{character} bounds are {actual_bounds}, "
                    f"expected {'Roboto Serif' if italic else 'RIDIBatang'} "
                    f"bounds {expected_bounds}"
                )

        if decoded_names(font, 1) != {"SNU Jaha"}:
            errors.append(f"unexpected family names: {sorted(decoded_names(font, 1))}")
        if decoded_names(font, 16) != {"SNU Jaha"}:
            errors.append(
                f"unexpected preferred family names: {sorted(decoded_names(font, 16))}"
            )
        expected_output_style = f"{style_name}{' Italic' if italic else ''}"
        if decoded_names(font, 17) != {expected_output_style}:
            errors.append(
                f"unexpected preferred style names: {sorted(decoded_names(font, 17))}"
            )
        if decoded_names(font, 4) != {f"SNU Jaha {expected_output_style}"}:
            errors.append(f"unexpected full names: {sorted(decoded_names(font, 4))}")
        expected_postscript_name = (
            f"SNUJaha-{style_name}{'Italic' if italic else ''}"
        )
        if decoded_names(font, 6) != {expected_postscript_name}:
            errors.append(
                f"unexpected PostScript names: {sorted(decoded_names(font, 6))}"
            )
        if font["CFF "].cff.fontNames != [expected_postscript_name]:
            errors.append(
                f"unexpected CFF font names: {font['CFF '].cff.fontNames}"
            )
        italic_angle = font["post"].italicAngle
        if italic and italic_angle == 0:
            errors.append("italic output must have a nonzero italic angle")
        if not italic and italic_angle != 0:
            errors.append("upright output must have a zero italic angle")

        missing_gsub = EXPECTED_GSUB - feature_tags(font, "GSUB")
        missing_gpos = EXPECTED_GPOS - feature_tags(font, "GPOS")
        if missing_gsub:
            errors.append("missing GSUB features: " + ", ".join(sorted(missing_gsub)))
        if missing_gpos:
            errors.append("missing GPOS features: " + ", ".join(sorted(missing_gpos)))
        if italic and not italic_guard_is_attached(font):
            errors.append("italic CJK guard is not the final kern lookup")
        lnum_lookups = feature_lookup_indices(font, "GSUB", "lnum")
        if italic and not lnum_lookups:
            errors.append("italic lnum must retain the Roboto Serif substitution")
        if not italic and lnum_lookups:
            errors.append("upright lnum must leave RIDIBatang figures unchanged")
        for feature_tag in EXPECTED_ACTIVE_FIGURE_FEATURES:
            if not feature_lookup_indices(font, "GSUB", feature_tag):
                errors.append(f"{feature_tag} figure feature must remain active")
        for dash in "-–—":
            dash_name = cmap[ord(dash)]
            for figure, expected in EXPECTED_DASH_FIGURE_KERNING.items():
                if italic:
                    expected = 0
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
            f"{path}: OK; style={style_name}{' Italic' if italic else ''}, "
            f"glyphs={len(font.getGlyphOrder())}, "
            f"cmap={len(cmap)}, hangul={hangul_count}, "
            f"GSUB={','.join(sorted(feature_tags(font, 'GSUB')))}, "
            f"GPOS={','.join(sorted(feature_tags(font, 'GPOS')))}"
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_font.py FONT.otf")
    verify(Path(sys.argv[1]))
