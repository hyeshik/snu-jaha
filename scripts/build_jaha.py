#!/usr/bin/env fontforge -lang=py -script
from __future__ import annotations

import argparse
import contextlib
import os
from pathlib import Path
from typing import Iterator


FAMILY_NAME = "SNU Jaha"
POSTSCRIPT_NAME = "SNUJaha-Regular"
STYLE_NAME = "Regular"
VERSION = "0.1.0"
VENDOR_ID = "HCHK"
TARGET_UPM = 1000

LATIN_X_SCALE = 0.895
LATIN_Y_SCALE = 0.936
LATIN_Y_SHIFT = -11.0

RIDI_COPYRIGHT = (
    "Copyright © 2019 RIDI & Sandoll. All rights reserved. "
    "Font designed by Sandoll Inc."
)
ROBOTO_COPYRIGHT = (
    "Copyright 2020 The Roboto Serif 14pt Project Authors "
    "(https://github.com/googlefonts/RobotoSerif)"
)
DERIVATIVE_COPYRIGHT = "Copyright (c) 2026 Hyeshik Chang (modifications)."
COPYRIGHT_TEXT = " ".join(
    (RIDI_COPYRIGHT, ROBOTO_COPYRIGHT, DERIVATIVE_COPYRIGHT)
)
LICENSE_DESCRIPTION = (
    "This Font Software is licensed under the SIL Open Font License, Version 1.1."
)
LICENSE_URL = "https://openfontlicense.org"

# The Korean source remains responsible for Korean and East Asian glyphs. The
# The Latin source supplies Latin, Cyrillic, punctuation, and the glyph slots
# and OpenType alternates for figures. Finalization replaces the default 0–9
# outlines and metrics with RIDIBatang originals without disturbing those
# feature connections. Context symbols commonly used as Korean list markers
# remain with RIDIBatang so that circled and enclosed forms keep a coherent CJK
# texture.
CJK_CODEPOINT_RANGES = (
    (0x1100, 0x11FF),
    (0x2E80, 0x2EFF),
    (0x2F00, 0x2FDF),
    (0x3000, 0x303F),
    (0x3040, 0x30FF),
    (0x3100, 0x312F),
    (0x3130, 0x318F),
    (0x31A0, 0x31EF),
    (0x31F0, 0x32FF),
    (0x3300, 0x9FFF),
    (0xA960, 0xA97F),
    (0xAC00, 0xD7FF),
    (0xF900, 0xFAFF),
    (0xFE30, 0xFE4F),
    (0xFF00, 0xFFEF),
    (0x20000, 0x2EBEF),
    (0x30000, 0x3134F),
)

CJK_CONTEXT_RANGES = (
    (0x20D0, 0x20FF),
    (0x2460, 0x24FF),
    (0x25A0, 0x25FF),
    (0x2700, 0x27BF),
    (0x1F100, 0x1F1FF),
)

PRIVATE_USE_RANGES = (
    (0xE000, 0xF8FF),
    (0xF0000, 0xFFFFD),
    (0x100000, 0x10FFFD),
)


@contextlib.contextmanager
def suppress_c_stderr(enabled: bool) -> Iterator[None]:
    if not enabled:
        yield
        return
    saved_stderr = os.dup(2)
    devnull = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull, 2)
        yield
    finally:
        os.dup2(saved_stderr, 2)
        os.close(saved_stderr)
        os.close(devnull)


def in_ranges(codepoint: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    return any(start <= codepoint <= end for start, end in ranges)


def is_cjk_codepoint(codepoint: int) -> bool:
    return in_ranges(codepoint, CJK_CODEPOINT_RANGES)


def should_keep_ridi_codepoint(codepoint: int) -> bool:
    return (
        is_cjk_codepoint(codepoint)
        or in_ranges(codepoint, CJK_CONTEXT_RANGES)
        or in_ranges(codepoint, PRIVATE_USE_RANGES)
    )


def transformed_advance(width: float, scale: float = LATIN_X_SCALE) -> int:
    return round(width * scale)


def flatten_cid_font(font, quiet: bool) -> bool:
    if not getattr(font, "cidfontname", None):
        return False
    with suppress_c_stderr(quiet):
        font.cidFlatten()
    return True


def remove_layout_lookups(font) -> int:
    names = list(font.gpos_lookups) + list(font.gsub_lookups)
    for name in names:
        font.removeLookup(name)
    return len(names)


def remove_non_cjk_glyphs(font) -> int:
    removed = 0
    for glyph in list(font.glyphs()):
        keep = glyph.glyphname == ".notdef" or should_keep_ridi_codepoint(
            glyph.unicode
        )
        if not keep:
            font.removeGlyph(glyph)
            removed += 1
    return removed


def remove_cjk_from_latin(font) -> int:
    removed = 0
    for glyph in list(font.glyphs()):
        if should_keep_ridi_codepoint(glyph.unicode):
            font.removeGlyph(glyph)
            removed += 1
    return removed


def transform_latin(font) -> int:
    glyphs = list(font.glyphs())
    for glyph in glyphs:
        if glyph.references:
            glyph.unlinkRef()

    changed = 0
    for glyph in glyphs:
        original_width = glyph.width
        glyph.transform(
            (LATIN_X_SCALE, 0, 0, LATIN_Y_SCALE, 0, LATIN_Y_SHIFT)
        )
        glyph.width = 0 if original_width == 0 else transformed_advance(original_width)
        changed += 1
    return changed


def rewrite_metadata(font) -> None:
    font.familyname = FAMILY_NAME
    font.fullname = f"{FAMILY_NAME} {STYLE_NAME}"
    font.fontname = POSTSCRIPT_NAME
    font.weight = "Normal"
    font.version = VERSION
    font.copyright = COPYRIGHT_TEXT
    font.os2_weight = 400
    font.os2_width = 5
    font.os2_fstype = 0
    font.os2_vendor = VENDOR_ID
    font.os2_stylemap = 64
    font.italicangle = 0

    source_notice = (
        "SNU Jaha is a derivative of RIDIBatang and Roboto Serif. "
        "The upstream names are used only for attribution."
    )
    font.sfnt_names = (
        ("English (US)", "Copyright", COPYRIGHT_TEXT),
        ("English (US)", "Family", FAMILY_NAME),
        ("English (US)", "SubFamily", STYLE_NAME),
        ("English (US)", "UniqueID", f"{VERSION};{VENDOR_ID};{POSTSCRIPT_NAME}"),
        ("English (US)", "Fullname", f"{FAMILY_NAME} {STYLE_NAME}"),
        ("English (US)", "Version", f"Version {VERSION}"),
        ("English (US)", "PostScriptName", POSTSCRIPT_NAME),
        ("English (US)", "Trademark", source_notice),
        ("English (US)", "Manufacturer", "Hyeshik Chang"),
        (
            "English (US)",
            "Designer",
            "RIDI, Sandoll, Roboto Serif Project Authors; Hyeshik Chang (modifications)",
        ),
        ("English (US)", "Preferred Family", FAMILY_NAME),
        ("English (US)", "Preferred Styles", STYLE_NAME),
        ("English (US)", "Compatible Full", f"{FAMILY_NAME} {STYLE_NAME}"),
        ("English (US)", "License", LICENSE_DESCRIPTION),
        ("English (US)", "License URL", LICENSE_URL),
    )


def build(ridibatang: Path, roboto_serif: Path, output: Path, quiet: bool) -> None:
    try:
        import fontforge
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Run with FontForge: fontforge -lang=py -script scripts/build_jaha.py"
        ) from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    transformed_latin = output.with_suffix(".latin.otf")

    with suppress_c_stderr(quiet):
        latin = fontforge.open(str(roboto_serif))
    try:
        latin.reencode("unicode")
        if latin.em != TARGET_UPM:
            latin.em = TARGET_UPM
        latin_cjk_removed = remove_cjk_from_latin(latin)
        latin_changed = transform_latin(latin)
        with suppress_c_stderr(quiet):
            latin.generate(str(transformed_latin), flags=("opentype",))
    finally:
        latin.close()

    with suppress_c_stderr(quiet):
        base = fontforge.open(str(ridibatang))
    try:
        flattened = flatten_cid_font(base, quiet)
        base.reencode("unicode")
        removed_lookups = remove_layout_lookups(base)
        ridi_removed = remove_non_cjk_glyphs(base)
        with suppress_c_stderr(quiet):
            base.mergeFonts(str(transformed_latin))
        rewrite_metadata(base)
        with suppress_c_stderr(quiet):
            validation = base.validate()
            base.generate(str(output), flags=("opentype",))
    finally:
        base.close()
        transformed_latin.unlink(missing_ok=True)

    print(
        f"{output}: cid_flattened={flattened}, "
        f"ridi_non_cjk_removed={ridi_removed}, "
        f"ridi_lookups_removed={removed_lookups}, "
        f"roboto_cjk_removed={latin_cjk_removed}, "
        f"roboto_glyphs_transformed={latin_changed}, "
        f"latin_transform=({LATIN_X_SCALE:.3f},{LATIN_Y_SCALE:.3f},"
        f"{LATIN_Y_SHIFT:.1f}), validate=0x{validation:x}"
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Build SNU Jaha Regular from RIDIBatang and Roboto Serif."
    )
    result.add_argument("--ridibatang", required=True)
    result.add_argument("--roboto-serif", required=True)
    result.add_argument("--output", required=True)
    result.add_argument("--verbose-fontforge", action="store_true")
    return result


def main() -> None:
    args = parser().parse_args()
    build(
        Path(args.ridibatang),
        Path(args.roboto_serif),
        Path(args.output),
        quiet=not args.verbose_fontforge,
    )


if __name__ == "__main__":
    main()
