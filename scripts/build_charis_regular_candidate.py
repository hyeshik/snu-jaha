#!/usr/bin/env fontforge -lang=py -script
from __future__ import annotations

import argparse
from pathlib import Path

import build_jaha as jaha


CANDIDATE_FAMILY_NAME = "SNU Jaha Latin Alt"
CANDIDATE_POSTSCRIPT_NAME = "SNUJahaLatinAlt-Regular"
CHARIS_X_SCALE = 1.0
CHARIS_Y_SCALE = 1.005
CHARIS_Y_SHIFT = -7.0
CHARIS_COPYRIGHT = "Copyright (c) 1997-2025 SIL Global."


def transformed_advance(width: float) -> int:
    return round(width * CHARIS_X_SCALE)


def transform_charis(font) -> int:
    glyphs = list(font.glyphs())
    for glyph in glyphs:
        if glyph.references:
            glyph.unlinkRef()

    changed = 0
    for glyph in glyphs:
        original_width = glyph.width
        glyph.transform(
            (
                CHARIS_X_SCALE,
                0,
                0,
                CHARIS_Y_SCALE,
                0,
                CHARIS_Y_SHIFT,
            )
        )
        glyph.width = 0 if original_width == 0 else transformed_advance(original_width)
        changed += 1
    return changed


def rewrite_candidate_metadata(font) -> None:
    copyright_text = " ".join(
        (jaha.RIDI_COPYRIGHT, CHARIS_COPYRIGHT, jaha.DERIVATIVE_COPYRIGHT)
    )
    source_notice = (
        "SNU Jaha Latin Alt is a comparison derivative of RIDIBatang and "
        "Charis 7.000. The upstream names are used only for attribution."
    )
    font.familyname = CANDIDATE_FAMILY_NAME
    font.fullname = f"{CANDIDATE_FAMILY_NAME} Regular"
    font.fontname = CANDIDATE_POSTSCRIPT_NAME
    font.weight = "Normal"
    font.version = jaha.VERSION
    font.copyright = copyright_text
    font.os2_weight = 400
    font.os2_width = 5
    font.os2_fstype = 0
    font.os2_vendor = jaha.VENDOR_ID
    font.os2_stylemap = 64
    font.italicangle = 0
    font.sfnt_names = (
        ("English (US)", "Copyright", copyright_text),
        ("English (US)", "Family", CANDIDATE_FAMILY_NAME),
        ("English (US)", "SubFamily", "Regular"),
        (
            "English (US)",
            "UniqueID",
            f"{jaha.VERSION};{jaha.VENDOR_ID};{CANDIDATE_POSTSCRIPT_NAME}",
        ),
        ("English (US)", "Fullname", f"{CANDIDATE_FAMILY_NAME} Regular"),
        ("English (US)", "Version", f"Version {jaha.VERSION}"),
        ("English (US)", "PostScriptName", CANDIDATE_POSTSCRIPT_NAME),
        ("English (US)", "Trademark", source_notice),
        ("English (US)", "Manufacturer", "Hyeshik Chang"),
        (
            "English (US)",
            "Designer",
            "RIDI, Sandoll, SIL Global; Hyeshik Chang (modifications)",
        ),
        ("English (US)", "Preferred Family", CANDIDATE_FAMILY_NAME),
        ("English (US)", "Preferred Styles", "Regular"),
        (
            "English (US)",
            "Compatible Full",
            f"{CANDIDATE_FAMILY_NAME} Regular",
        ),
        ("English (US)", "License", jaha.LICENSE_DESCRIPTION),
        ("English (US)", "License URL", jaha.LICENSE_URL),
    )


def build(ridibatang: Path, charis: Path, output: Path, quiet: bool) -> None:
    try:
        import fontforge
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Run with FontForge: fontforge -lang=py -script "
            "scripts/build_charis_regular_candidate.py"
        ) from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    transformed_latin = output.with_suffix(".latin.otf")

    with jaha.suppress_c_stderr(quiet):
        latin = fontforge.open(str(charis))
    try:
        latin.reencode("unicode")
        if latin.em != jaha.TARGET_UPM:
            latin.em = jaha.TARGET_UPM
        latin_cjk_removed = jaha.remove_cjk_from_latin(latin)
        latin_changed = transform_charis(latin)
        with jaha.suppress_c_stderr(quiet):
            latin.generate(str(transformed_latin), flags=("opentype",))
    finally:
        latin.close()

    with jaha.suppress_c_stderr(quiet):
        base = fontforge.open(str(ridibatang))
    try:
        flattened = jaha.flatten_cid_font(base, quiet)
        base.reencode("unicode")
        removed_lookups = jaha.remove_layout_lookups(base)
        ridi_removed = jaha.remove_non_cjk_glyphs(base)
        hangul_transformed = jaha.transform_hangul(
            base,
            jaha.STYLE_SPECS["Regular"],
        )
        with jaha.suppress_c_stderr(quiet):
            base.mergeFonts(str(transformed_latin))
        rewrite_candidate_metadata(base)
        with jaha.suppress_c_stderr(quiet):
            validation = base.validate()
            base.generate(str(output), flags=("opentype",))
    finally:
        base.close()
        transformed_latin.unlink(missing_ok=True)

    print(
        f"{output}: family={CANDIDATE_FAMILY_NAME}, "
        f"cid_flattened={flattened}, ridi_non_cjk_removed={ridi_removed}, "
        f"ridi_lookups_removed={removed_lookups}, "
        f"hangul_transformed={hangul_transformed}, "
        f"charis_cjk_removed={latin_cjk_removed}, "
        f"charis_glyphs_transformed={latin_changed}, "
        f"latin_transform=({CHARIS_X_SCALE:.3f},{CHARIS_Y_SCALE:.3f},"
        f"{CHARIS_Y_SHIFT:.1f}), validate=0x{validation:x}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the disposable Charis-based SNU Jaha Regular candidate."
    )
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--charis", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--verbose-fontforge", action="store_true")
    args = parser.parse_args()
    build(
        Path(args.ridibatang),
        Path(args.charis),
        Path(args.output),
        quiet=not args.verbose_fontforge,
    )


if __name__ == "__main__":
    main()
