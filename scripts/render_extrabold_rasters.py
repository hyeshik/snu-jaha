#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


COUNTER_GLYPHS = "뺄뼒뽑뼮"
MERGE_GLYPHS = "괄레발빽뺄뺌뼒쀻적"
SCALE = 6


def glyph_bitmap(font: ImageFont.FreeTypeFont, character: str, ppem: int) -> Image.Image:
    canvas = Image.new("L", (ppem + 12, ppem + 12), 255)
    bounds = font.getbbox(character)
    x = (canvas.width - (bounds[2] - bounds[0])) // 2 - bounds[0]
    y = (canvas.height - (bounds[3] - bounds[1])) // 2 - bounds[1]
    ImageDraw.Draw(canvas).text((x, y), character, font=font, fill=0)
    pixels = np.asarray(canvas)
    return Image.fromarray(np.where(pixels < 128, 0, 255).astype(np.uint8))


def render_strip(font_path: Path, characters: str, ppem: int, output: Path) -> None:
    font = ImageFont.truetype(str(font_path), ppem)
    cell_size = ppem + 12
    strip = Image.new("L", (cell_size * len(characters), cell_size), 255)
    for index, character in enumerate(characters):
        strip.paste(glyph_bitmap(font, character, ppem), (index * cell_size, 0))
    strip.resize(
        (strip.width * SCALE, strip.height * SCALE),
        Image.Resampling.NEAREST,
    ).save(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render exact binary raster strips for ExtraBold review."
    )
    parser.add_argument("--bold", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    candidate_dir = Path(args.candidate_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fonts = {
        "bold": Path(args.bold),
        "n30-auto": candidate_dir / "CJK-XB-N30-auto.otf",
        "n30-retain": candidate_dir / "CJK-XB-N30-retain.otf",
        "n32-auto": candidate_dir / "CJK-XB-N32-auto.otf",
    }
    for label, font_path in fonts.items():
        for ppem in (24, 32, 64):
            render_strip(
                font_path,
                COUNTER_GLYPHS,
                ppem,
                output_dir / f"counter-{label}-{ppem}.png",
            )
        render_strip(
            font_path,
            MERGE_GLYPHS,
            64,
            output_dir / f"merge-{label}-64.png",
        )


if __name__ == "__main__":
    main()
