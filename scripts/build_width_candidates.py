#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from instantiate_roboto_serif import instantiate


@dataclass(frozen=True)
class Candidate:
    key: str
    family_name: str
    width: float
    x_scale: float

    @property
    def stem(self) -> str:
        width = f"{self.width:g}"
        scale = f"{self.x_scale:.3f}".replace(".", "")
        return f"SNUJaha-Width-{self.key}-W{width}-X{scale}"


CANDIDATES = (
    Candidate("A", "SNU Jaha Width A", 95, 0.895),
    Candidate("B", "SNU Jaha Width B", 92, 0.895),
    Candidate("C", "SNU Jaha Width C", 90, 0.895),
    Candidate("D", "SNU Jaha Width D", 85, 0.915),
    Candidate("E", "SNU Jaha Width E", 80, 0.930),
)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def build_candidates(
    variable_source: Path,
    ridibatang: Path,
    output_dir: Path,
    fontforge: str,
) -> None:
    scripts_dir = Path(__file__).resolve().parent
    build_script = scripts_dir / "build_jaha.py"
    finalize_script = scripts_dir / "finalize_font.py"
    output_dir.mkdir(parents=True, exist_ok=True)

    for candidate in CANDIDATES:
        latin_source = output_dir / f"RobotoSerif-W{candidate.width:g}.ttf"
        raw_output = output_dir / f"{candidate.stem}.raw.otf"
        output = output_dir / f"{candidate.stem}.otf"

        instantiate(
            variable_source,
            latin_source,
            weight=400,
            width=candidate.width,
        )
        run(
            [
                fontforge,
                "-lang=py",
                "-script",
                str(build_script),
                "--ridibatang",
                str(ridibatang),
                "--roboto-serif",
                str(latin_source),
                "--output",
                str(raw_output),
                "--style",
                "Regular",
                "--latin-x-scale",
                str(candidate.x_scale),
                "--latin-advance-scale",
                str(candidate.x_scale),
                "--family-name",
                candidate.family_name,
            ]
        )
        run(
            [
                sys.executable,
                str(finalize_script),
                "--input",
                str(raw_output),
                "--ridibatang",
                str(ridibatang),
                "--output",
                str(output),
                "--kern-scale",
                str(candidate.x_scale),
                "--style",
                "Regular",
            ]
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build disposable Regular width candidates for SNU Jaha."
    )
    parser.add_argument("--variable-source", required=True)
    parser.add_argument("--ridibatang", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--fontforge", default="fontforge")
    args = parser.parse_args()
    build_candidates(
        Path(args.variable_source),
        Path(args.ridibatang),
        Path(args.output_dir),
        args.fontforge,
    )


if __name__ == "__main__":
    main()
