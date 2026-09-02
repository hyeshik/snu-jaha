#!/usr/bin/env fontforge -lang=py -script
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from build_jaha import suppress_c_stderr
from build_lightweight_microfonts import (
    DEFAULT_FIGURES,
    build_latin,
    make_ridi_subset,
    parse_latin_source,
    rewrite_audit_metadata,
)
from build_ridi_weight import repair_overlapped_hints


HEAVY_AUDIT_TEXT = """
느 스 그 노 누 니 시 소 기 가 나 사
뾂 뼒 뼮 뿳 휇 흙 뿔 률 쫓 빛 활 괄
쀻 뺨 뺌 뿜 뾰 뽑 뚫 뺄 뺀 빽 뺐 뺏
자하연의 연구 기록 반복적 건조 스트레스와 회복 속도
기공 회복과 유전자 발현 시점에 미치는 영향
0123456789
"""
HEAVY_AUDIT_CODEPOINTS = {
    ord(character)
    for character in HEAVY_AUDIT_TEXT
    if not character.isspace()
}


@dataclass(frozen=True)
class ExtraBoldCandidate:
    offset: int
    method: str
    weight_type: str
    counter: str

    @property
    def slug(self) -> str:
        return f"N{self.offset}-{self.method}"

    @property
    def family(self) -> str:
        return f"SNU Jaha ExtraBold Audit CJK N{self.offset} {self.method.title()}"

    @property
    def postscript_name(self) -> str:
        return f"SNUJahaExtraBoldAuditCJK-N{self.offset}{self.method.title()}"

    @property
    def figure_x_scale(self) -> float:
        return 1 - self.offset * (1 - 0.944) / 24


EXTRABOLD_CANDIDATES = tuple(
    ExtraBoldCandidate(offset, method, weight_type, counter)
    for offset in (28, 30, 32, 36)
    for method, weight_type, counter in (
        ("auto", "auto", "auto"),
        ("retain", "auto", "retain"),
        ("cjk", "CJK", "auto"),
    )
)


def weight_subset(
    subset: Path,
    output: Path,
    candidate: ExtraBoldCandidate,
    quiet: bool,
) -> None:
    import fontforge

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(subset))
    try:
        font.reencode("unicode")
        changed = 0
        recentered = 0
        with suppress_c_stderr(quiet):
            for glyph in list(font.glyphs()):
                if glyph.unicode not in HEAVY_AUDIT_CODEPOINTS:
                    continue
                if glyph.references:
                    glyph.unlinkRef()
                original_width = glyph.width
                original_bounds = glyph.boundingBox()
                original_center = (original_bounds[0] + original_bounds[2]) / 2
                glyph.changeWeight(
                    candidate.offset,
                    candidate.weight_type,
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
                    recentered += 1
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
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()
    repaired_hints, validation = repair_overlapped_hints(output, quiet)
    print(
        f"{output}: glyphs={changed}, offset={candidate.offset}, "
        f"method={candidate.method}, recentered={recentered}, "
        f"figure_x_scale={candidate.figure_x_scale:.6f}, "
        f"overlapped_hints_repaired={repaired_hints}, "
        f"validate=0x{validation:x}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build representative ExtraBold audit microfonts."
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
    make_ridi_subset(
        Path(args.ridibatang),
        subset,
        quiet,
        HEAVY_AUDIT_CODEPOINTS,
    )
    for candidate in EXTRABOLD_CANDIDATES:
        weight_subset(
            subset,
            output_dir / f"CJK-XB-{candidate.slug}.otf",
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
