#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


AXIS_LOCATIONS = {
    "GRAD": 0,
    "opsz": 14,
    "wdth": 100,
}


def instantiate(source: Path, output: Path, weight: float) -> None:
    font = TTFont(source, recalcTimestamp=False)
    try:
        locations = {**AXIS_LOCATIONS, "wght": weight}
        instantiateVariableFont(
            font,
            locations,
            inplace=True,
            updateFontNames=False,
            static=True,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        font.save(output, reorderTables=False)
    finally:
        font.close()
    print(
        f"{output}: GRAD=0, opsz=14, wdth=100, wght={weight:.3f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Instantiate a static Roboto Serif source for SNU Jaha."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--weight", type=float, required=True)
    args = parser.parse_args()
    instantiate(Path(args.input), Path(args.output), args.weight)


if __name__ == "__main__":
    main()
