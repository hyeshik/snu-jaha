from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_jaha as builder
import build_ridi_weight as weight_builder


class BuildJahaPolicyTests(unittest.TestCase):
    def test_family_identity(self) -> None:
        self.assertEqual(builder.FAMILY_NAME, "SNU Jaha")
        self.assertEqual(builder.POSTSCRIPT_NAME, "SNUJaha-Regular")
        self.assertEqual(builder.VERSION, "0.1.0")
        self.assertEqual(builder.STYLE_SPECS["Regular"].weight_class, 400)
        self.assertEqual(builder.STYLE_SPECS["Bold"].weight_class, 700)
        self.assertEqual(
            builder.STYLE_SPECS["Bold"].postscript_name,
            "SNUJaha-Bold",
        )

    def test_hangul_and_cjk_punctuation_stay_with_ridi(self) -> None:
        for codepoint in (0x1100, 0x3131, 0x3001, 0xAC00, 0xD7A3, 0xFF01):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(builder.should_keep_ridi_codepoint(codepoint))

    def test_latin_and_general_punctuation_come_from_roboto(self) -> None:
        for codepoint in (0x0041, 0x0061, 0x0030, 0x00E9, 0x201C, 0x20A9):
            with self.subTest(codepoint=codepoint):
                self.assertFalse(builder.should_keep_ridi_codepoint(codepoint))

    def test_context_symbols_stay_with_ridi(self) -> None:
        for codepoint in (0x2460, 0x25A0, 0x1F100):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(builder.should_keep_ridi_codepoint(codepoint))

    def test_latin_advance_uses_declared_scale(self) -> None:
        self.assertEqual(builder.transformed_advance(1000), 895)
        self.assertEqual(builder.transformed_advance(560), 501)

    def test_vertical_transform_matches_reference_glyph_fit(self) -> None:
        roboto_cap_top = 710
        roboto_x_top = 537
        transformed_cap_top = (
            roboto_cap_top * builder.LATIN_Y_SCALE + builder.LATIN_Y_SHIFT
        )
        transformed_x_top = (
            roboto_x_top * builder.LATIN_Y_SCALE + builder.LATIN_Y_SHIFT
        )
        self.assertAlmostEqual(transformed_cap_top, 653.56)
        self.assertAlmostEqual(transformed_x_top, 491.632)
        self.assertAlmostEqual(
            (builder.LATIN_Y_SHIFT + transformed_cap_top) / 2,
            321.28,
        )

    def test_bold_default_figures_keep_tabular_cells(self) -> None:
        self.assertEqual(weight_builder.DEFAULT_FIGURE_X_SCALE, 0.944)
        for character in "0123456789":
            with self.subTest(character=character):
                self.assertTrue(weight_builder.should_weight(ord(character)))
        self.assertFalse(weight_builder.should_weight(ord("A")))


if __name__ == "__main__":
    unittest.main()
