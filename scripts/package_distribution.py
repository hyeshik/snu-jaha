#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FAMILY_PREFIX = "SNUJaha"
STYLE_NAMES = (
    "Thin",
    "ThinItalic",
    "Light",
    "LightItalic",
    "Regular",
    "RegularItalic",
    "Medium",
    "MediumItalic",
    "SemiBold",
    "SemiBoldItalic",
    "Bold",
    "BoldItalic",
    "ExtraBold",
    "ExtraBoldItalic",
)
EXPECTED_OTF_FILENAMES = tuple(
    f"{FAMILY_PREFIX}-{style}.otf" for style in STYLE_NAMES
)
LICENSE_ENTRIES = (
    ("LICENSE", "LICENSE.txt"),
    ("licenses/RIDIBatang.txt", "LICENSE-RIDIBatang.txt"),
    ("licenses/RobotoSerif.txt", "LICENSE-RobotoSerif.txt"),
)
ZIP_TIMESTAMP = (2026, 9, 2, 0, 0, 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create the flat SNU Jaha distribution ZIP."
    )
    parser.add_argument("--input-dir", default="dist")
    parser.add_argument("--output", required=True)
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    return parser


def find_expected_otfs(input_dir: Path) -> list[Path]:
    paths = [input_dir / filename for filename in EXPECTED_OTF_FILENAMES]
    missing = [path.name for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing expected OTF file(s): " + ", ".join(missing))
    return paths


def find_license_files(project_root: Path) -> list[tuple[Path, str]]:
    entries = [
        (project_root / source, archive_name)
        for source, archive_name in LICENSE_ENTRIES
    ]
    missing = [str(path) for path, _ in entries if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing license file(s): " + ", ".join(missing))
    return entries


def expected_archive_entries() -> list[str]:
    return list(EXPECTED_OTF_FILENAMES) + [name for _, name in LICENSE_ENTRIES]


def write_entry(archive: ZipFile, source: Path, archive_name: str) -> None:
    info = ZipInfo(archive_name, ZIP_TIMESTAMP)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(
        info,
        source.read_bytes(),
        compress_type=ZIP_DEFLATED,
        compresslevel=9,
    )


def write_distribution(input_dir: Path, output: Path, project_root: Path) -> None:
    fonts = find_expected_otfs(input_dir)
    licenses = find_license_files(project_root)
    output.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output, "w") as archive:
        for font_path in fonts:
            write_entry(archive, font_path, font_path.name)
        for license_path, archive_name in licenses:
            write_entry(archive, license_path, archive_name)

    with ZipFile(output) as archive:
        entries = archive.namelist()
    expected = expected_archive_entries()
    if entries != expected:
        raise RuntimeError(f"Unexpected distribution layout: {entries}")
    print(f"Wrote {output}")


def resolve_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else project_root / path


def main() -> None:
    args = build_parser().parse_args()
    project_root = Path(args.project_root).resolve()
    write_distribution(
        resolve_path(project_root, args.input_dir),
        resolve_path(project_root, args.output),
        project_root,
    )


if __name__ == "__main__":
    main()
