#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from render_snu_family_baselines import (
    BASELINE,
    COLORS,
    GRAY,
    INK,
    PAPER,
    RULE,
    draw_label,
)


@dataclass(frozen=True)
class Row:
    label: str
    path: Path
    color: str


BLENDS = (
    ("2:1", "O2A1"),
    ("1:1", "O1A1"),
    ("1:2", "O1A2"),
)
STATES = (
    ("1:0", None),
    *BLENDS,
    ("0:1", None),
)
FAMILY_SPECS = (
    ("SNU Jaha", "SNUJaha", COLORS[0]),
    ("SNU Edge", "SNUEdge", COLORS[2]),
    ("SNU Sprout", "SNUSprout", COLORS[3]),
)


def render_rows(
    title: str,
    rows: tuple[Row, ...],
    output: Path,
    *,
    subtitle: str,
) -> None:
    width = 2000
    height = 180 + len(rows) * 220
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    draw_label(draw, (72, 48), title, 30, fill=INK)
    draw_label(
        draw,
        (72, 92),
        subtitle,
        21,
    )
    text_x = 470
    for index, row in enumerate(rows):
        baseline_y = 270 + index * 220
        font = ImageFont.truetype(str(row.path), 128)
        draw.line((text_x, baseline_y, width - 72, baseline_y), fill=BASELINE, width=2)
        draw.line(
            (text_x, baseline_y - 128, width - 72, baseline_y - 128),
            fill=RULE,
            width=1,
        )
        draw_label(draw, (72, baseline_y - 34), row.label, 25, fill=row.color)
        draw.text(
            (text_x, baseline_y),
            "Hgx 0127 한글 흙",
            font=font,
            fill=INK,
            anchor="ls",
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def render_mixed_ratios(
    original_paths: dict[str, Path],
    candidate_dir: Path,
    appendard: Row,
    output: Path,
) -> None:
    width, height = 2400, 1540
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    draw_label(draw, (72, 48), "FIVE STATES ON ONE BASELINE", 30, fill=INK)
    draw_label(
        draw,
        (72, 92),
        "Ratio is original:Appendard · every coloured run shares one red baseline",
        21,
    )
    for index, (ratio, slug) in enumerate(STATES):
        baseline_y = 310 + index * 280
        draw.line((390, baseline_y, width - 72, baseline_y), fill=BASELINE, width=2)
        draw_label(draw, (72, baseline_y - 30), f"Original:Appendard {ratio}", 25, fill=INK)
        x = 390.0
        segments = []
        for (label, prefix, color), text in zip(
            FAMILY_SPECS,
            ("환경 Hgx ", "환경 Hgx ", "환경 Hgx "),
        ):
            if ratio == "1:0":
                path = original_paths[label]
            elif ratio == "0:1":
                path = candidate_dir / f"{prefix}AppendardFit-Regular.otf"
            else:
                path = candidate_dir / f"{prefix}Blend-{slug}-Regular.otf"
            segments.append(
                (
                    text,
                    Row(
                        label,
                        path,
                        color,
                    ),
                )
            )
        segments.append(("0127 한글", appendard))
        for text, selected in segments:
            font = ImageFont.truetype(str(selected.path), 104)
            draw.text(
                (round(x), baseline_y),
                text,
                font=font,
                fill=selected.color,
                anchor="ls",
            )
            x += draw.textlength(text, font=font)
    draw_label(
        draw,
        (360, height - 42),
        "1:0 uses each original family; 0:1 uses each family's full-fit version.",
        19,
        fill=GRAY,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render intermediate original-to-Appendard baseline panels."
    )
    parser.add_argument("--jaha", required=True)
    parser.add_argument("--edge", required=True)
    parser.add_argument("--sprout", required=True)
    parser.add_argument("--appendard", required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    original_paths = {
        "SNU Jaha": Path(args.jaha),
        "SNU Edge": Path(args.edge),
        "SNU Sprout": Path(args.sprout),
    }
    candidate_dir = Path(args.candidate_dir)
    appendard = Row(
        "SNU Appendard / target",
        Path(args.appendard),
        COLORS[1],
    )
    output_dir = Path(args.output_dir)
    for label, prefix, color in FAMILY_SPECS:
        progression = [Row(f"Original:Appendard 1:0", original_paths[label], color)]
        for ratio, slug in BLENDS:
            progression.append(
                Row(
                    f"Original:Appendard {ratio}",
                    candidate_dir / f"{prefix}Blend-{slug}-Regular.otf",
                    color,
                )
            )
        progression.append(
            Row(
                "Original:Appendard 0:1",
                candidate_dir / f"{prefix}AppendardFit-Regular.otf",
                color,
            )
        )
        render_rows(
            f"{label.upper()} / ORIGINAL TO APPENDARD",
            tuple(progression),
            output_dir / f"{prefix.lower()}-progression.png",
            subtitle="128 ppem · original → 2:1 → 1:1 → 1:2 → family full fit",
        )

    for ratio, slug in STATES:
        rows = []
        for label, prefix, color in FAMILY_SPECS:
            if ratio == "1:0":
                path = original_paths[label]
            elif ratio == "0:1":
                path = candidate_dir / f"{prefix}AppendardFit-Regular.otf"
            else:
                path = candidate_dir / f"{prefix}Blend-{slug}-Regular.otf"
            rows.append(Row(f"{label} / {ratio}", path, color))
        output_slug = slug.lower() if slug is not None else (
            "original" if ratio == "1:0" else "full-fit"
        )
        render_rows(
            f"ORIGINAL:APPENDARD {ratio} / COMMON BASELINE",
            tuple(rows),
            output_dir / f"blend-{output_slug}.png",
            subtitle="128 ppem · identical y coordinate · no renderer-side offset",
        )
    render_mixed_ratios(
        original_paths,
        candidate_dir,
        appendard,
        output_dir / "mixed-ratios.png",
    )
    print(f"{output_dir}: baseline panels=9")


if __name__ == "__main__":
    main()
