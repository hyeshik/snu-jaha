#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


STYLES = ("Regular", "SemiBold", "ExtraBold")
INK = "#182236"
GRAY = "#667085"
RULE = "#D7DEE6"
BASELINE = "#C34F45"
PAPER = "#FCFBF7"
COLORS = ("#174D7A", "#2B6D65", "#8A5A35", "#76528A")


@dataclass(frozen=True)
class FamilySource:
    label: str
    prefix: str
    directory: Path

    def font_path(self, style: str) -> Path:
        return self.directory / f"{self.prefix}-{style}.otf"


def label_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def draw_label(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    size: int,
    *,
    fill: str = GRAY,
) -> None:
    draw.text(position, text, font=label_font(size), fill=fill, anchor="la")


def render_family_rows(
    sources: tuple[FamilySource, ...], style: str, output: Path
) -> None:
    width, height = 2000, 1120
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    draw_label(draw, (72, 48), f"COMMON BASELINE / {style.upper()}", 30, fill=INK)
    draw_label(
        draw,
        (72, 92),
        "128 ppem · identical y coordinate · baseline shown in red",
        21,
    )

    text_x = 470
    for index, source in enumerate(sources):
        baseline_y = 278 + index * 250
        path = source.font_path(style)
        if not path.is_file():
            raise SystemExit(f"missing font: {path}")
        font = ImageFont.truetype(str(path), 128)
        draw.line((text_x, baseline_y, width - 72, baseline_y), fill=BASELINE, width=2)
        draw.line(
            (text_x, baseline_y - 128, width - 72, baseline_y - 128),
            fill=RULE,
            width=1,
        )
        draw_label(draw, (72, baseline_y - 42), source.label, 28, fill=COLORS[index])
        draw_label(draw, (72, baseline_y - 5), style, 20)
        draw.text(
            (text_x, baseline_y),
            "Hgx 0127 한글 흙",
            font=font,
            fill=INK,
            anchor="ls",
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def render_mixed_rows(
    sources: tuple[FamilySource, ...], output: Path
) -> None:
    width, height = 2400, 980
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    draw_label(draw, (72, 48), "FOUR FAMILIES ON ONE BASELINE", 30, fill=INK)
    draw_label(
        draw,
        (72, 92),
        "Every coloured run shares exactly one baseline; no per-family offset is applied.",
        21,
    )

    segments = (
        "자하 Hgx ",
        "연구 Hgx ",
        "환경 Hgx ",
        "24 h 한글",
    )
    for row, style in enumerate(STYLES):
        baseline_y = 300 + row * 280
        draw.line((330, baseline_y, width - 72, baseline_y), fill=BASELINE, width=2)
        draw_label(draw, (72, baseline_y - 30), style, 27, fill=INK)
        draw_label(draw, (72, baseline_y + 8), f"{(400, 600, 800)[row]}", 19)
        x = 330.0
        for index, (source, segment) in enumerate(zip(sources, segments)):
            font = ImageFont.truetype(str(source.font_path(style)), 100)
            draw.text(
                (round(x), baseline_y),
                segment,
                font=font,
                fill=COLORS[index],
                anchor="ls",
            )
            x += draw.textlength(segment, font=font)

    legend_y = height - 54
    x = 330
    for color, source in zip(COLORS, sources):
        draw.rectangle((x, legend_y, x + 26, legend_y + 26), fill=color)
        draw_label(draw, (x + 38, legend_y - 2), source.label, 19, fill=INK)
        x += 430

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render exact common-baseline comparison panels for SNU fonts."
    )
    parser.add_argument("--jaha-dir", required=True)
    parser.add_argument("--appendard-dir", required=True)
    parser.add_argument("--edge-dir", required=True)
    parser.add_argument("--sprout-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    sources = (
        FamilySource("SNU Jaha", "SNUJaha", Path(args.jaha_dir)),
        FamilySource("SNU Appendard", "SNUAppendard", Path(args.appendard_dir)),
        FamilySource("SNU Edge", "SNUEdge", Path(args.edge_dir)),
        FamilySource("SNU Sprout", "SNUSprout", Path(args.sprout_dir)),
    )
    output_dir = Path(args.output_dir)
    for style in STYLES:
        render_family_rows(
            sources,
            style,
            output_dir / f"baseline-{style.lower()}.png",
        )
    render_mixed_rows(sources, output_dir / "mixed-baselines.png")
    print(f"{output_dir}: baseline panels={len(STYLES) + 1}")


if __name__ == "__main__":
    main()
