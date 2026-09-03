from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "package_distribution.py"


def load_packager():
    spec = importlib.util.spec_from_file_location("package_distribution", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageDistributionTests(unittest.TestCase):
    def test_license_headers_preserve_both_sources_and_modification_credit(self):
        project_header = (ROOT / "LICENSE").read_text().split(
            "This Font Software", 1
        )[0]
        ridi_header = (ROOT / "licenses" / "RIDIBatang.txt").read_text().split(
            "This Font Software", 1
        )[0]
        roboto_header = (ROOT / "licenses" / "RobotoSerif.txt").read_text().split(
            "This Font Software", 1
        )[0]

        self.assertIn("RIDI & Sandoll", project_header)
        self.assertIn("Roboto Serif Project Authors", project_header)
        self.assertIn("Hyeshik Chang (modifications)", project_header)
        self.assertIn("RIDI & Sandoll", ridi_header)
        self.assertIn("Roboto Serif Project Authors", roboto_header)

    def test_distribution_contains_only_flat_fonts_and_licenses(self):
        packager = load_packager()

        self.assertEqual(len(packager.EXPECTED_OTF_FILENAMES), 14)
        self.assertEqual(
            [name for _, name in packager.LICENSE_ENTRIES],
            [
                "LICENSE.txt",
                "LICENSE-RIDIBatang.txt",
                "LICENSE-RobotoSerif.txt",
            ],
        )

        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            otf_dir = project_root / "otf"
            otf_dir.mkdir()
            for name in packager.EXPECTED_OTF_FILENAMES:
                (otf_dir / name).write_bytes(b"font")
            for source, _ in packager.LICENSE_ENTRIES:
                path = project_root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("license")

            first = project_root / "first.zip"
            second = project_root / "second.zip"
            packager.write_distribution(otf_dir, first, project_root)
            packager.write_distribution(otf_dir, second, project_root)

            with ZipFile(first) as archive:
                self.assertEqual(
                    archive.namelist(), packager.expected_archive_entries()
                )
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertTrue(
                all("/" not in name for name in packager.expected_archive_entries())
            )

    def test_distribution_requires_the_complete_family(self):
        packager = load_packager()

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                packager.find_expected_otfs(Path(tmp))


if __name__ == "__main__":
    unittest.main()
