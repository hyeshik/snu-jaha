#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


AXIS_LOCATIONS = {
    "GRAD": 0,
    "opsz": 14,
    "wdth": 91,
}
WEIGHT_FLOOR = 400
WEIGHT_FLOOR_CODEPOINTS = frozenset(
    (0x2191, 0x2193, 0x2196, 0x2197, 0x2198, 0x2199, 0x27F7)
)


def apply_weight_floor(
    font: TTFont,
    source: Path,
    weight: float,
    width: float,
    optical_size: float,
    grade: float,
) -> int:
    if weight >= WEIGHT_FLOOR:
        return 0
    reference = TTFont(source, recalcTimestamp=False)
    try:
        instantiateVariableFont(
            reference,
            {
                "GRAD": grade,
                "opsz": optical_size,
                "wdth": width,
                "wght": WEIGHT_FLOOR,
            },
            inplace=True,
            updateFontNames=False,
            static=True,
        )
        target_cmap = font.getBestCmap()
        reference_cmap = reference.getBestCmap()
        replaced = 0
        for codepoint in WEIGHT_FLOOR_CODEPOINTS:
            target_name = target_cmap.get(codepoint)
            reference_name = reference_cmap.get(codepoint)
            if target_name is None or reference_name is None:
                continue
            font["glyf"].glyphs[target_name] = copy.deepcopy(
                reference["glyf"][reference_name]
            )
            font["hmtx"][target_name] = reference["hmtx"][reference_name]
            replaced += 1
        return replaced
    finally:
        reference.close()


def instantiate(
    source: Path,
    output: Path,
    weight: float,
    width: float = AXIS_LOCATIONS["wdth"],
    optical_size: float = AXIS_LOCATIONS["opsz"],
    grade: float = AXIS_LOCATIONS["GRAD"],
) -> None:
    font = TTFont(source, recalcTimestamp=False)
    try:
        locations = {
            "GRAD": grade,
            "opsz": optical_size,
            "wdth": width,
            "wght": weight,
        }
        instantiateVariableFont(
            font,
            locations,
            inplace=True,
            updateFontNames=False,
            static=True,
        )
        weight_floor_glyphs = apply_weight_floor(
            font,
            source,
            weight,
            width,
            optical_size,
            grade,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        font.save(output, reorderTables=False)
    finally:
        font.close()
    print(
        f"{output}: GRAD={grade:g}, opsz={optical_size:g}, "
        f"wdth={width:g}, wght={weight:.3f}, "
        f"weight_floor_glyphs={weight_floor_glyphs}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Instantiate a static Roboto Serif source for SNU Jaha."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--weight", type=float, required=True)
    parser.add_argument("--width", type=float, default=AXIS_LOCATIONS["wdth"])
    parser.add_argument(
        "--optical-size",
        type=float,
        default=AXIS_LOCATIONS["opsz"],
    )
    parser.add_argument("--grade", type=float, default=AXIS_LOCATIONS["GRAD"])
    args = parser.parse_args()
    instantiate(
        Path(args.input),
        Path(args.output),
        args.weight,
        args.width,
        args.optical_size,
        args.grade,
    )


if __name__ == "__main__":
    main()
