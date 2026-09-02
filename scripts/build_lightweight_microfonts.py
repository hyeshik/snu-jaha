#!/usr/bin/env fontforge -lang=py -script
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from build_jaha import (
    VERSION,
    flatten_cid_font,
    remove_cjk_from_latin,
    remove_layout_lookups,
    suppress_c_stderr,
    transform_latin,
)


AUDIT_TEXT = """
느 스 그 노 누 니 시 소 기 가 나 사
뾂 뼒 뼮 뿳 휇 흙 뿔 률 쫓 빛 활 괄
자하연의 연구 기록 반복적 건조 스트레스와 회복 속도
기공 회복과 유전자 발현 시점에 미치는 영향
0123456789
"""
AUDIT_CODEPOINTS = {ord(character) for character in AUDIT_TEXT if not character.isspace()}
DEFAULT_FIGURES = "0123456789"


@dataclass(frozen=True)
class CJKCandidate:
    style: str
    offset: int
    counter: str

    @property
    def slug(self) -> str:
        return f"{self.style}-N{abs(self.offset)}-{self.counter}"

    @property
    def family(self) -> str:
        return (
            f"SNU Jaha Audit CJK {self.style} "
            f"N{abs(self.offset)} {self.counter.title()}"
        )

    @property
    def postscript_name(self) -> str:
        return f"SNUJahaAuditCJK-{self.slug.replace('-', '')}"

    @property
    def figure_x_scale(self) -> float:
        return 1 - self.offset * (1 - 0.944) / 24


CJK_CANDIDATES = tuple(
    CJKCandidate(style, -offset, counter)
    for style, offsets in (("Light", (6, 8, 10)), ("Thin", (16, 20, 24)))
    for offset in offsets
    for counter in ("auto", "squish")
)


def rewrite_audit_metadata(font, family: str, postscript_name: str) -> None:
    font.familyname = family
    font.fullname = family
    font.fontname = postscript_name
    font.weight = "Normal"
    font.version = VERSION
    font.os2_weight = 400
    font.os2_width = 5
    font.os2_fstype = 0
    font.os2_stylemap = 64
    font.italicangle = 0
    font.sfnt_names = (
        ("English (US)", "Family", family),
        ("English (US)", "SubFamily", "Regular"),
        ("English (US)", "Fullname", family),
        ("English (US)", "Version", f"Version {VERSION}"),
        ("English (US)", "PostScriptName", postscript_name),
        ("English (US)", "Preferred Family", family),
        ("English (US)", "Preferred Styles", "Regular"),
    )


def make_ridi_subset(
    source: Path,
    output: Path,
    quiet: bool,
    audit_codepoints: set[int] = AUDIT_CODEPOINTS,
) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source))
    try:
        flatten_cid_font(font, quiet)
        font.reencode("unicode")
        remove_layout_lookups(font)
        for glyph in list(font.glyphs()):
            if glyph.glyphname == ".notdef" or glyph.unicode in audit_codepoints:
                continue
            font.removeGlyph(glyph)
        rewrite_audit_metadata(
            font,
            "SNU Jaha Audit CJK Regular",
            "SNUJahaAuditCJK-Regular",
        )
        with suppress_c_stderr(quiet):
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()


def weight_subset(
    subset: Path,
    output: Path,
    candidate: CJKCandidate,
    quiet: bool,
) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(subset))
    try:
        font.reencode("unicode")
        changed = 0
        with suppress_c_stderr(quiet):
            for glyph in list(font.glyphs()):
                if glyph.unicode not in AUDIT_CODEPOINTS:
                    continue
                if glyph.references:
                    glyph.unlinkRef()
                original_width = glyph.width
                original_bounds = glyph.boundingBox()
                original_center = (original_bounds[0] + original_bounds[2]) / 2
                glyph.changeWeight(
                    candidate.offset,
                    "auto",
                    0,
                    0,
                    candidate.counter,
                )
                if glyph.width != original_width:
                    weighted_bounds = glyph.boundingBox()
                    weighted_center = (
                        weighted_bounds[0] + weighted_bounds[2]
                    ) / 2
                    glyph.transform(
                        (1, 0, 0, 1, original_center - weighted_center, 0)
                    )
                if chr(glyph.unicode) in DEFAULT_FIGURES:
                    scale = candidate.figure_x_scale
                    glyph.transform(
                        (scale, 0, 0, 1, original_center * (1 - scale), 0)
                    )
                glyph.width = original_width
                changed += 1
        rewrite_audit_metadata(
            font,
            candidate.family,
            candidate.postscript_name,
        )
        with suppress_c_stderr(quiet):
            validation = font.validate()
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()
    print(
        f"{output}: glyphs={changed}, offset={candidate.offset}, "
        f"counter={candidate.counter}, "
        f"figure_x_scale={candidate.figure_x_scale:.6f}, "
        f"validate=0x{validation:x}"
    )


def build_latin(
    source: Path,
    output: Path,
    label: str,
    quiet: bool,
) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source))
    try:
        font.reencode("unicode")
        removed = remove_cjk_from_latin(font)
        transformed = transform_latin(font)
        family = f"SNU Jaha Audit Latin W{label}"
        rewrite_audit_metadata(
            font,
            family,
            f"SNUJahaAuditLatin-W{label}",
        )
        with suppress_c_stderr(quiet):
            validation = font.validate()
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()
    print(
        f"{output}: cjk_removed={removed}, transformed={transformed}, "
        f"validate=0x{validation:x}"
    )


def parse_latin_source(value: str) -> tuple[str, Path]:
    try:
        label, path = value.split("=", 1)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected LABEL=PATH") from exc
    return label, Path(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build representative Light and Thin audit microfonts."
    )
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--latin-source", action="append", type=parse_latin_source)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--verbose-fontforge", action="store_true")
    args = parser.parse_args()
    if not args.latin_source:
        parser.error("at least one --latin-source is required")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    subset = output_dir / "CJK-Regular.otf"
    quiet = not args.verbose_fontforge
    make_ridi_subset(Path(args.ridibatang), subset, quiet)
    for candidate in CJK_CANDIDATES:
        weight_subset(
            subset,
            output_dir / f"CJK-{candidate.slug}.otf",
            candidate,
            quiet,
        )
    for label, source in args.latin_source:
        build_latin(
            source,
            output_dir / f"Latin-W{label}.otf",
            label,
            quiet,
        )


if __name__ == "__main__":
    main()
