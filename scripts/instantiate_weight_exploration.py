#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from build_weight_exploration_microfonts import LATIN_CANDIDATES
from instantiate_roboto_serif import instantiate


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Instantiate Roboto Serif sources for the weight study."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    source = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for candidate in LATIN_CANDIDATES:
        instantiate(
            source,
            output_dir / f"Roboto-{candidate.slug}.ttf",
            candidate.weight,
            grade=candidate.grade,
        )


if __name__ == "__main__":
    main()
