from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_jaha as builder
import build_ridi_weight as weight_builder
import build_lightweight_microfonts as lightweight_builder
import audit_lightweight_candidates as lightweight_audit
import instantiate_roboto_serif as roboto_instancer


class BuildJahaPolicyTests(unittest.TestCase):
    def test_family_identity(self) -> None:
        self.assertEqual(builder.FAMILY_NAME, "SNU Jaha")
        self.assertEqual(builder.POSTSCRIPT_NAME, "SNUJaha-Regular")
        self.assertEqual(builder.VERSION, "0.1.0")
        self.assertEqual(builder.STYLE_SPECS["Regular"].weight_class, 400)
        self.assertEqual(builder.STYLE_SPECS["Thin"].weight_class, 100)
        self.assertEqual(builder.STYLE_SPECS["Light"].weight_class, 300)
        self.assertEqual(builder.STYLE_SPECS["Medium"].weight_class, 500)
        self.assertEqual(builder.STYLE_SPECS["SemiBold"].weight_class, 600)
        self.assertEqual(builder.STYLE_SPECS["Bold"].weight_class, 700)
        self.assertEqual(
            builder.STYLE_SPECS["Bold"].postscript_name,
            "SNUJaha-Bold",
        )
        self.assertEqual(builder.STYLE_SPECS["Medium"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["SemiBold"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["Thin"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["Light"].stylemap, 0)

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

    def test_intermediate_latin_instances_keep_regular_axes(self) -> None:
        self.assertEqual(
            roboto_instancer.AXIS_LOCATIONS,
            {"GRAD": 0, "opsz": 14, "wdth": 100},
        )

    def test_lightweight_microfont_matrix_covers_search_space(self) -> None:
        candidates = lightweight_builder.CJK_CANDIDATES
        self.assertEqual(len(candidates), 12)
        self.assertEqual(
            {
                (candidate.style, candidate.offset, candidate.counter)
                for candidate in candidates
            },
            {
                (style, -offset, counter)
                for style, offsets in (
                    ("Light", (6, 8, 10)),
                    ("Thin", (16, 20, 24)),
                )
                for offset in offsets
                for counter in ("auto", "squish")
            },
        )

    def test_lightweight_figure_correction_extends_weight_curve(self) -> None:
        candidates = {
            (candidate.style, candidate.offset): candidate
            for candidate in lightweight_builder.CJK_CANDIDATES
        }
        self.assertAlmostEqual(
            candidates[("Light", -6)].figure_x_scale,
            1.014,
        )
        self.assertAlmostEqual(
            candidates[("Thin", -24)].figure_x_scale,
            1.056,
        )

    def test_only_reviewed_jamo_separations_are_exempted(self) -> None:
        reviewed = {"character": "뿳", "regular": 5, "candidate": 6}
        larger_split = {"character": "뿳", "regular": 5, "candidate": 7}
        unknown = {"character": "흙", "regular": 4, "candidate": 5}
        self.assertTrue(
            lightweight_audit.is_reviewed_component_increase(reviewed)
        )
        self.assertFalse(
            lightweight_audit.is_reviewed_component_increase(larger_split)
        )
        self.assertFalse(
            lightweight_audit.is_reviewed_component_increase(unknown)
        )


if __name__ == "__main__":
    unittest.main()
