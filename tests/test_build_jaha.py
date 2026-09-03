from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_jaha as builder
import build_ridi_weight as weight_builder
import build_lightweight_microfonts as lightweight_builder
import build_extrabold_microfonts as extrabold_builder
import audit_lightweight_candidates as lightweight_audit
import audit_extrabold_full as full_extrabold_audit
import build_charis_regular_candidate as charis_candidate
import build_width_candidates as width_candidates
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
        self.assertEqual(builder.STYLE_SPECS["ExtraBold"].weight_class, 800)
        self.assertEqual(builder.STYLE_SPECS["ExtraBold"].fontforge_weight, "Heavy")
        self.assertEqual(
            builder.STYLE_SPECS["Bold"].postscript_name,
            "SNUJaha-Bold",
        )
        self.assertEqual(builder.STYLE_SPECS["Medium"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["SemiBold"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["Thin"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["Light"].stylemap, 0)
        self.assertEqual(builder.STYLE_SPECS["ExtraBold"].stylemap, 0)
        self.assertEqual(
            builder.STYLE_SPECS["Regular"].output_style_name(True),
            "Regular Italic",
        )
        self.assertEqual(
            builder.STYLE_SPECS["Bold"].output_postscript_name(True),
            "SNUJaha-BoldItalic",
        )
        self.assertEqual(builder.STYLE_SPECS["Regular"].output_stylemap(True), 1)
        self.assertEqual(builder.STYLE_SPECS["Bold"].output_stylemap(True), 33)

    def test_version_maps_to_unique_opentype_revision(self) -> None:
        self.assertEqual(builder.font_revision(), 0.1)
        self.assertEqual(builder.font_revision("1.2.34"), 1.234)
        with self.assertRaises(ValueError):
            builder.font_revision("1.10.0")
        with self.assertRaises(ValueError):
            builder.font_revision("1.2.100")

    def test_hangul_and_cjk_punctuation_stay_with_ridi(self) -> None:
        for codepoint in (0x1100, 0x3131, 0x3001, 0xAC00, 0xD7A3, 0xFF01):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(builder.should_keep_ridi_codepoint(codepoint))

    def test_hangul_optical_restore_matches_reviewed_geometry(self) -> None:
        self.assertEqual(builder.HANGUL_Y_SCALE, 0.984)
        self.assertAlmostEqual(builder.HANGUL_Y_SHIFT, 24.8622817344205)
        for codepoint in (0x1100, 0x3131, 0xA960, 0xAC00, 0xD7A3, 0xD7B0):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(builder.is_hangul_codepoint(codepoint))
        for codepoint in (0x0041, 0x3001, 0x4E00, 0xD7A4):
            with self.subTest(codepoint=codepoint):
                self.assertFalse(builder.is_hangul_codepoint(codepoint))
        for codepoint in (0x115F, 0x1160, 0x3164):
            with self.subTest(codepoint=codepoint):
                self.assertFalse(builder.should_expand_hangul_advance(codepoint))
        for codepoint in (0x1100, 0x3131, 0xAC00, 0xD7A3):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(builder.should_expand_hangul_advance(codepoint))

    def test_extrabold_hangul_advance_is_widened(self) -> None:
        self.assertEqual(builder.EXTRABOLD_HANGUL_ADVANCE_SCALE, 1.04)
        self.assertEqual(
            builder.hangul_advance_scale(builder.STYLE_SPECS["Regular"]),
            1.0,
        )
        self.assertEqual(
            builder.hangul_advance_scale(builder.STYLE_SPECS["Bold"]),
            1.0,
        )
        self.assertEqual(
            builder.hangul_advance_scale(builder.STYLE_SPECS["ExtraBold"]),
            1.04,
        )
        self.assertEqual(
            builder.transformed_hangul_advance(
                943,
                builder.STYLE_SPECS["ExtraBold"],
            ),
            981,
        )

    def test_latin_and_general_punctuation_come_from_roboto(self) -> None:
        for codepoint in (0x0041, 0x0061, 0x0030, 0x00E9, 0x201C, 0x20A9):
            with self.subTest(codepoint=codepoint):
                self.assertFalse(builder.should_keep_ridi_codepoint(codepoint))

    def test_context_symbols_stay_with_ridi(self) -> None:
        for codepoint in (0x2460, 0x25A0, 0x1F100):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(builder.should_keep_ridi_codepoint(codepoint))

    def test_latin_advance_uses_declared_scale(self) -> None:
        self.assertEqual(builder.LATIN_X_SCALE, 0.895)
        self.assertEqual(builder.LATIN_ADVANCE_SCALE, 0.889)
        self.assertEqual(builder.transformed_advance(1000), 889)
        self.assertEqual(builder.transformed_advance(560), 498)
        self.assertEqual(builder.transformed_advance(1000, 0.93), 930)
        self.assertEqual(
            builder.postscript_family_name("SNU Jaha Width E"),
            "SNUJahaWidthE",
        )

    def test_production_separates_outline_and_advance_scales(self) -> None:
        self.assertEqual(builder.transformed_advance(822, 0.889), 731)

    def test_capital_a_family_is_selected_for_overlap_merging(self) -> None:
        for glyph_name in ("A", "Aacute", "Aogonek", "AE", "Acyr"):
            with self.subTest(glyph_name=glyph_name):
                self.assertTrue(builder.is_capital_a_family(glyph_name))
        for glyph_name in ("a", "arrowleft", "B"):
            with self.subTest(glyph_name=glyph_name):
                self.assertFalse(builder.is_capital_a_family(glyph_name))

    def test_width_candidate_matrix_covers_axis_and_transform_options(self) -> None:
        self.assertEqual(
            [
                (candidate.key, candidate.width, candidate.x_scale)
                for candidate in width_candidates.CANDIDATES
            ],
            [
                ("A", 95, 0.895),
                ("B", 92, 0.895),
                ("C", 90, 0.895),
                ("D", 85, 0.915),
                ("E", 80, 0.930),
            ],
        )

    def test_charis_candidate_keeps_native_width_and_fits_vertical_bounds(self) -> None:
        self.assertEqual(charis_candidate.CANDIDATE_FAMILY_NAME, "SNU Jaha Latin Alt")
        self.assertNotIn("Charis", charis_candidate.CANDIDATE_FAMILY_NAME)
        self.assertEqual(charis_candidate.CHARIS_X_SCALE, 1.0)
        self.assertEqual(charis_candidate.CHARIS_Y_SCALE, 1.005)
        self.assertEqual(charis_candidate.CHARIS_Y_SHIFT, -7.0)
        self.assertEqual(charis_candidate.transformed_advance(560), 560)

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
            {"GRAD": 0, "opsz": 14, "wdth": 91},
        )
        self.assertEqual(roboto_instancer.WEIGHT_FLOOR, 400)
        self.assertEqual(
            roboto_instancer.WEIGHT_FLOOR_CODEPOINTS,
            {0x2191, 0x2193, 0x2196, 0x2197, 0x2198, 0x2199, 0x27F7},
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

    def test_extrabold_microfont_matrix_covers_search_space(self) -> None:
        candidates = extrabold_builder.EXTRABOLD_CANDIDATES
        self.assertEqual(len(candidates), 12)
        self.assertEqual(
            {
                (
                    candidate.offset,
                    candidate.method,
                    candidate.weight_type,
                    candidate.counter,
                )
                for candidate in candidates
            },
            {
                (offset, method, weight_type, counter)
                for offset in (28, 30, 32, 36)
                for method, weight_type, counter in (
                    ("auto", "auto", "auto"),
                    ("retain", "auto", "retain"),
                    ("cjk", "CJK", "auto"),
                )
            },
        )

    def test_extrabold_figure_correction_extends_weight_curve(self) -> None:
        candidates = {
            (candidate.offset, candidate.method): candidate
            for candidate in extrabold_builder.EXTRABOLD_CANDIDATES
        }
        self.assertAlmostEqual(
            candidates[(32, "auto")].figure_x_scale,
            0.9253333333333333,
        )
        self.assertAlmostEqual(
            candidates[(36, "auto")].figure_x_scale,
            0.916,
        )

    def test_extrabold_spacing_corpus_extracts_modern_hangul_pairs(self) -> None:
        pairs = full_extrabold_audit.extract_hangul_bigrams(
            "연구환경 Research 24 h, 식물환경"
        )
        self.assertEqual(pairs["연구"], 1)
        self.assertEqual(pairs["구환"], 1)
        self.assertEqual(pairs["환경"], 2)
        self.assertEqual(pairs["식물"], 1)
        self.assertEqual(pairs["물환"], 1)

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
