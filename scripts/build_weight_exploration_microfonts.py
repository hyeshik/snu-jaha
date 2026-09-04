#!/usr/bin/env fontforge -lang=py -script
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from build_jaha import (
    HANGUL_Y_SCALE,
    HANGUL_Y_SHIFT,
    VERSION,
    flatten_cid_font,
    is_hangul_codepoint,
    merge_capital_a_overlaps,
    remove_cjk_from_latin,
    remove_layout_lookups,
    suppress_c_stderr,
    transform_latin,
)
from build_lightweight_microfonts import rewrite_audit_metadata
from build_ridi_weight import repair_overlapped_hints


STRUCTURE_STRESS_TEXT = """
뾂 뼒 뼮 뿔 쫓
"""

AUDIT_TEXT = STRUCTURE_STRESS_TEXT + """
가 나 다 라 마 바 사 아 자 차 카 타 파 하
느 스 그 노 누 니 시 소 기
뻢 벒 벮 뿳 휇 흙 뽔 률 쫃 빛 활 괄
쐀 뺨 뺌 뾜 뾰 뽑 뚫 뺄 뺀 빽 뺔 뺏
자하연의 연구 기록 반복적 건조 스트레스와 회복 속도
기공 회복과 유전자 발현 시점에 미치는 영향
0123456789
"""
AUDIT_CODEPOINTS = {
    ord(character) for character in AUDIT_TEXT if not character.isspace()
}
DEFAULT_FIGURES = "0123456789"
FINAL_FIGURE_SCALE = 520 / 560
RASTER_PPEM = 128


@dataclass(frozen=True)
class WeightTarget:
    style: str
    minimum: float
    center: float
    maximum: float


WEIGHT_TARGETS = {
    target.style: target
    for target in (
        WeightTarget("Thin", 0.54, 0.58, 0.62),
        WeightTarget("Light", 0.79, 0.82, 0.84),
        WeightTarget("Medium", 1.17, 1.19, 1.21),
        WeightTarget("SemiBold", 1.31, 1.35, 1.38),
        WeightTarget("Bold", 1.45, 1.50, 1.54),
        WeightTarget("ExtraBold", 1.58, 1.61, 1.64),
    )
}


SELECTED_CJK_CONSTRUCTIONS = {
    "Thin": (-28, "retain", 1.0),
    "Light": (-12, "auto", 1.0),
    "Medium": (14, "auto", 1.0),
    "SemiBold": (22, "auto", 1.0),
    "Bold": (28, "retain", 1.04),
    "ExtraBold": (36, "retain", 1.08),
}

SELECTED_LATIN_CONSTRUCTIONS = {
    "Thin": (100, -10),
    "Light": (250, 0),
    "Medium": (500, 0),
    "SemiBold": (565, 0),
    "Bold": (610, 0),
    "ExtraBold": (660, 0),
}


@dataclass(frozen=True)
class CJKCandidate:
    style: str
    offset: int
    counter: str = "auto"
    advance_scale: float | None = None

    @property
    def sign_slug(self) -> str:
        prefix = "M" if self.offset < 0 else "P"
        return f"{prefix}{abs(self.offset)}"

    @property
    def slug(self) -> str:
        advance = (
            ""
            if self.advance_scale is None
            else f"-A{round(self.advance_scale * 100)}"
        )
        return f"{self.style}-{self.sign_slug}-{self.counter}{advance}"

    @property
    def label(self) -> str:
        sign = "−" if self.offset < 0 else "+"
        advance = (
            ""
            if self.advance_scale is None
            else f" {round(self.advance_scale * 100)}%"
        )
        return f"{self.style} {sign}{abs(self.offset)} {self.counter}{advance}"

    @property
    def family(self) -> str:
        return f"SNU Jaha Weight Study CJK {self.slug.replace('-', ' ')}"

    @property
    def postscript_name(self) -> str:
        return f"SNUJahaWeightStudyCJK-{self.slug.replace('-', '')}"

    @property
    def figure_x_scale(self) -> float:
        return 1 - self.offset * (1 - 0.944) / 24

    @property
    def hangul_advance_scale(self) -> float:
        if self.advance_scale is not None:
            return self.advance_scale
        return 1.04 if self.style == "Bold" else 1.0


def candidates(
    style: str,
    offsets: tuple[int, ...],
    counters: tuple[str, ...] = ("auto",),
) -> tuple[CJKCandidate, ...]:
    return tuple(
        CJKCandidate(style, offset, counter)
        for offset in offsets
        for counter in counters
    )


CJK_CANDIDATES = (
    *candidates("Thin", (-26, -28, -30, -32), ("auto", "retain")),
    *candidates("Light", (-10, -12, -14, -16)),
    *candidates("Medium", (10, 12, 14, 16)),
    *candidates("SemiBold", (20, 22, 24, 26)),
    *candidates("Bold", (28, 30, 32, 34), ("auto", "retain")),
    *(
        CJKCandidate("ExtraBold", offset, counter, advance_scale)
        for offset in (36, 38, 40, 42, 44)
        for counter in ("auto", "retain")
        for advance_scale in (1.04, 1.08)
    ),
)


@dataclass(frozen=True)
class LatinCandidate:
    style: str
    weight: int
    grade: int = 0

    @property
    def slug(self) -> str:
        return f"{self.style}-W{self.weight}-G{self.grade}"

    @property
    def label(self) -> str:
        grade = "" if self.grade == 0 else f" GRAD {self.grade:+d}"
        return f"{self.style} wght {self.weight}{grade}"


LATIN_CANDIDATES = tuple(
    LatinCandidate(style, weight, grade)
    for style, locations in (
        (
            "Thin",
            (
                (100, -50),
                (100, -25),
                (100, -10),
                (100, -5),
                (100, 0),
                (120, 0),
                (140, 0),
            ),
        ),
        ("Light", ((250, 0), (270, 0), (290, 0))),
        ("Medium", ((485, 0), (500, 0), (515, 0))),
        ("SemiBold", ((565, 0), (580, 0), (595, 0))),
        ("Bold", ((610, 0), (620, 0), (630, 0), (645, 0), (660, 0))),
        (
            "ExtraBold",
            ((660, 0), (680, 0), (700, 0), (725, 0), (750, 0), (775, 0)),
        ),
    )
    for weight, grade in locations
)


def make_ridi_subset(source: Path, output: Path, quiet: bool) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source))
    try:
        flatten_cid_font(font, quiet)
        font.reencode("unicode")
        remove_layout_lookups(font)
        for glyph in list(font.glyphs()):
            if glyph.glyphname == ".notdef" or glyph.unicode in AUDIT_CODEPOINTS:
                continue
            font.removeGlyph(glyph)
        rewrite_audit_metadata(
            font,
            "SNU Jaha Weight Study CJK Source",
            "SNUJahaWeightStudyCJK-Source",
        )
        with suppress_c_stderr(quiet):
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()


def transform_hangul_geometry(font, advance_scale: float) -> int:
    transformed = 0
    for glyph in list(font.glyphs()):
        if not is_hangul_codepoint(glyph.unicode):
            continue
        if glyph.references:
            glyph.unlinkRef()
        original_advance = glyph.width
        new_advance = round(original_advance * advance_scale)
        glyph.transform(
            (
                1,
                0,
                0,
                HANGUL_Y_SCALE,
                (new_advance - original_advance) / 2,
                HANGUL_Y_SHIFT,
            )
        )
        glyph.width = new_advance
        transformed += 1
    return transformed


def finalize_figures(font) -> int:
    finalized = 0
    for glyph in list(font.glyphs()):
        if glyph.unicode < 0 or chr(glyph.unicode) not in DEFAULT_FIGURES:
            continue
        glyph.transform((FINAL_FIGURE_SCALE, 0, 0, 1, 0, 0))
        glyph.width = 520
        finalized += 1
    return finalized


def make_regular(source_subset: Path, output: Path, quiet: bool) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source_subset))
    try:
        font.reencode("unicode")
        transformed = transform_hangul_geometry(font, 1.0)
        figures = finalize_figures(font)
        rewrite_audit_metadata(
            font,
            "SNU Jaha Weight Study CJK Regular",
            "SNUJahaWeightStudyCJK-Regular",
        )
        with suppress_c_stderr(quiet):
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()
    repaired, validation = repair_overlapped_hints(output, quiet)
    print(
        f"{output}: hangul_transformed={transformed}, figures={figures}, "
        f"overlapped_hints_repaired={repaired}, validate=0x{validation:x}"
    )


def weight_subset(
    source_subset: Path,
    output: Path,
    candidate: CJKCandidate,
    quiet: bool,
) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source_subset))
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
                weighted_bounds = glyph.boundingBox()
                weighted_center = (weighted_bounds[0] + weighted_bounds[2]) / 2
                glyph.transform(
                    (1, 0, 0, 1, original_center - weighted_center, 0)
                )
                glyph.width = original_width
                if chr(glyph.unicode) in DEFAULT_FIGURES:
                    scale = candidate.figure_x_scale
                    glyph.transform(
                        (scale, 0, 0, 1, original_center * (1 - scale), 0)
                    )
                changed += 1
        transformed = transform_hangul_geometry(
            font,
            candidate.hangul_advance_scale,
        )
        figures = finalize_figures(font)
        rewrite_audit_metadata(
            font,
            candidate.family,
            candidate.postscript_name,
        )
        with suppress_c_stderr(quiet):
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()
    repaired, validation = repair_overlapped_hints(output, quiet)
    print(
        f"{output}: glyphs={changed}, offset={candidate.offset}, "
        f"counter={candidate.counter}, hangul_transformed={transformed}, "
        f"hangul_advance_scale={candidate.hangul_advance_scale:.3f}, "
        f"figures={figures}, figure_x_scale={candidate.figure_x_scale:.6f}, "
        f"overlapped_hints_repaired={repaired}, validate=0x{validation:x}"
    )


def build_latin(
    source: Path,
    output: Path,
    candidate: LatinCandidate,
    quiet: bool,
) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source))
    try:
        font.reencode("unicode")
        removed = remove_cjk_from_latin(font)
        transformed = transform_latin(font)
        capital_a_merged = merge_capital_a_overlaps(font)
        family = f"SNU Jaha Weight Study Latin {candidate.slug.replace('-', ' ')}"
        rewrite_audit_metadata(
            font,
            family,
            f"SNUJahaWeightStudyLatin-{candidate.slug.replace('-', '')}",
        )
        with suppress_c_stderr(quiet):
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()
    repaired, validation = repair_overlapped_hints(output, quiet)
    print(
        f"{output}: cjk_removed={removed}, transformed={transformed}, "
        f"capital_a_overlaps_merged={capital_a_merged}, "
        f"overlapped_hints_repaired={repaired}, validate=0x{validation:x}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build microfonts for the Regular-anchored weight study."
    )
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--latin-source-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--verbose-fontforge", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source_subset = output_dir / "CJK-Source.otf"
    quiet = not args.verbose_fontforge
    make_ridi_subset(Path(args.ridibatang), source_subset, quiet)
    make_regular(source_subset, output_dir / "CJK-Regular.otf", quiet)
    for candidate in CJK_CANDIDATES:
        weight_subset(
            source_subset,
            output_dir / f"CJK-{candidate.slug}.otf",
            candidate,
            quiet,
        )

    latin_source_dir = Path(args.latin_source_dir)
    for candidate in LATIN_CANDIDATES:
        source = latin_source_dir / f"Roboto-{candidate.slug}.ttf"
        if not source.is_file():
            raise SystemExit(f"missing Latin source: {source}")
        build_latin(
            source,
            output_dir / f"Latin-{candidate.slug}.otf",
            candidate,
            quiet,
        )


if __name__ == "__main__":
    main()
