#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

from build_jaha import VERSION, font_revision


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
        reference_advances={"H": 684, "M": 789, "g": 532, "n": 556},
        italic_reference_advances={"H": 679, "M": 780, "g": 499, "n": 529},
        figure_bounds={
            "0": (46, -7, 474, 659),
            "3": (85, -7, 453, 659),
            "8": (60, -11, 460, 663),
        },
    ),
    "Light": StyleProfile(
        weight_class=300,
        cap_height=654,
        x_height=492,
        reference_advances={"H": 707, "M": 814, "g": 539, "n": 568},
        italic_reference_advances={"H": 704, "M": 805, "g": 519, "n": 546},
        figure_bounds={
            "0": (39, -15, 481, 667),
            "3": (76, -15, 462, 667),
            "8": (52, -19, 468, 671),
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
        x_height=493,
        reference_advances={"H": 729, "M": 845, "g": 559, "n": 590},
        italic_reference_advances={"H": 726, "M": 838, "g": 553, "n": 573},
        figure_bounds={
            "0": (28, -21, 492, 673),
            "3": (64, -21, 474, 673),
            "8": (41, -25, 479, 677),
        },
    ),
    "SemiBold": StyleProfile(
        weight_class=600,
        cap_height=654,
        x_height=493,
        reference_advances={"H": 728, "M": 849, "g": 568, "n": 597},
        italic_reference_advances={"H": 725, "M": 843, "g": 563, "n": 580},
        figure_bounds={
            "0": (26, -21, 494, 673),
            "3": (61, -21, 477, 673),
            "8": (38, -25, 482, 677),
        },
    ),
    "Bold": StyleProfile(
        weight_class=700,
        cap_height=654,
        x_height=494,
        reference_advances={"H": 727, "M": 852, "g": 574, "n": 601},
        italic_reference_advances={"H": 725, "M": 846, "g": 570, "n": 584},
        figure_bounds={
            "0": (24, -21, 496, 673),
            "3": (59, -21, 479, 673),
            "8": (36, -25, 484, 677),
        },
    ),
    "ExtraBold": StyleProfile(
        weight_class=800,
        cap_height=654,
        x_height=494,
        reference_advances={"H": 726, "M": 854, "g": 581, "n": 605},
        italic_reference_advances={"H": 724, "M": 850, "g": 577, "n": 589},
        figure_bounds={
            "0": (22, -21, 498, 673),
            "3": (57, -21, 482, 673),
            "8": (34, -25, 486, 677),
        },
    ),
}

ITALIC_FIGURE_BOUNDS = {
    "Thin": {
        "0": (32.41, -21.296, 469.171, 598.336),
        "3": (1.085, -79.328, 458.43, 598.338),
        "8": (27.041, -20.363, 475.436, 665.723),
    },
    "Light": {
        "0": (29.726, -21.296, 467.379, 598.335),
        "3": (-6.074, -79.328, 457.534, 598.335),
        "8": (18.992, -20.364, 475.439, 665.724),
    },
    "Regular": {
        "0": (26.147, -21.296, 466.485, 598.336),
        "3": (-13.235, -80.264, 455.745, 598.337),
        "8": (10.03, -20.361, 474.536, 665.728),
    },
    "Medium": {
        "0": (22.563, -21.296, 470.959, 599.273),
        "3": (-15.919, -80.264, 462.905, 599.271),
        "8": (6.447, -20.358, 482.589, 665.73),
    },
    "SemiBold": {
        "0": (19.88, -21.296, 474.539, 600.208),
        "3": (-18.605, -80.264, 467.38, 599.271),
        "8": (3.768, -20.363, 487.964, 665.724),
    },
    "Bold": {
        "0": (18.983, -21.296, 476.329, 600.206),
        "3": (-19.5, -80.264, 470.959, 600.206),
        "8": (1.979, -20.356, 491.544, 665.731),
    },
    "ExtraBold": {
        "0": (17.195, -21.296, 479.014, 600.207),
        "3": (-21.288, -80.264, 473.653, 600.207),
        "8": (0.189, -20.36, 495.125, 665.728),
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
        expected_revision = font_revision()
        if abs(font["head"].fontRevision - expected_revision) > 1 / 65536:
            errors.append(
                f"head.fontRevision is {font['head'].fontRevision}, "
                f"expected {expected_revision}"
            )
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
        if decoded_names(font, 5) != {f"Version {VERSION}"}:
            errors.append(
                f"unexpected version names: {sorted(decoded_names(font, 5))}"
            )
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
        cff_version = font["CFF "].cff.topDictIndex[0].version
        if cff_version != VERSION:
            errors.append(f"CFF version is {cff_version!r}, expected {VERSION!r}")
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
