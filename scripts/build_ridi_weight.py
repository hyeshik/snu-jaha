#!/usr/bin/env fontforge -lang=py -script
from __future__ import annotations

import argparse
from pathlib import Path

from build_jaha import (
    flatten_cid_font,
    should_keep_ridi_codepoint,
    suppress_c_stderr,
)


DEFAULT_FIGURES = "0123456789"
DEFAULT_FIGURE_X_SCALE = 0.944
OVERLAPPED_HINTS = 0x800000


def should_weight(codepoint: int) -> bool:
    return should_keep_ridi_codepoint(codepoint) or (
        codepoint >= 0 and chr(codepoint) in DEFAULT_FIGURES
    )


def repair_overlapped_hints(output: Path, quiet: bool) -> tuple[int, int]:
    import fontforge

    repaired_output = output.with_name(f"{output.stem}.rehinted{output.suffix}")
    with suppress_c_stderr(quiet):
        font = fontforge.open(str(output))
    repaired = 0
    try:
        font.reencode("unicode")
        with suppress_c_stderr(quiet):
            for glyph in font.glyphs():
                if glyph.validate(1) & OVERLAPPED_HINTS:
                    glyph.autoHint()
                    repaired += 1
            validation = font.validate(1)
            if repaired:
                font.generate(str(repaired_output), flags=("opentype",))
    finally:
        font.close()
    if repaired:
        repaired_output.replace(output)
    else:
        repaired_output.unlink(missing_ok=True)
    return repaired, validation


def build(
    source: Path,
    output: Path,
    offset: int,
    figure_x_scale: float,
    counter: str,
    quiet: bool,
) -> None:
    try:
        import fontforge
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Run with FontForge: "
            "fontforge -lang=py -script scripts/build_ridi_weight.py"
        ) from exc

    with suppress_c_stderr(quiet):
        font = fontforge.open(str(source))
    try:
        flattened = flatten_cid_font(font, quiet)
        font.reencode("unicode")
        changed = 0
        recentered = 0
        figures_scaled = 0
        with suppress_c_stderr(quiet):
            for glyph in list(font.glyphs()):
                if not should_weight(glyph.unicode):
                    continue
                if glyph.references:
                    glyph.unlinkRef()
                original_width = glyph.width
                original_bounds = glyph.boundingBox()
                original_center = (original_bounds[0] + original_bounds[2]) / 2
                glyph.changeWeight(offset, "auto", 0, 0, counter)
                if glyph.width != original_width:
                    weighted_bounds = glyph.boundingBox()
                    weighted_center = (weighted_bounds[0] + weighted_bounds[2]) / 2
                    glyph.transform(
                        (1, 0, 0, 1, original_center - weighted_center, 0)
                    )
                    glyph.width = original_width
                    recentered += 1
                if glyph.unicode >= 0 and chr(glyph.unicode) in DEFAULT_FIGURES:
                    glyph.transform(
                        (
                            figure_x_scale,
                            0,
                            0,
                            1,
                            original_center * (1 - figure_x_scale),
                            0,
                        )
                    )
                    glyph.width = original_width
                    figures_scaled += 1
                changed += 1
        output.parent.mkdir(parents=True, exist_ok=True)
        with suppress_c_stderr(quiet):
            validation = font.validate()
            font.generate(str(output), flags=("opentype",))
    finally:
        font.close()

    repaired_hints = 0
    if offset < 0:
        repaired_hints, validation = repair_overlapped_hints(output, quiet)
    print(
        f"{output}: cid_flattened={flattened}, weighted={changed}, "
        f"advance_preserved={recentered}, "
        f"figures_x_scaled={figures_scaled}, "
        f"overlapped_hints_repaired={repaired_hints}, "
        f"figure_x_scale={figure_x_scale:.3f}, "
        f"offset={offset}, counter={counter}, validate=0x{validation:x}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a conservative synthetic RIDIBatang weight source."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--offset", type=int, required=True)
    parser.add_argument(
        "--figure-x-scale",
        type=float,
        default=DEFAULT_FIGURE_X_SCALE,
    )
    parser.add_argument(
        "--counter",
        choices=("auto", "retain"),
        default="auto",
    )
    parser.add_argument("--verbose-fontforge", action="store_true")
    args = parser.parse_args()
    build(
        Path(args.input),
        Path(args.output),
        args.offset,
        args.figure_x_scale,
        args.counter,
        quiet=not args.verbose_fontforge,
    )


if __name__ == "__main__":
    main()
