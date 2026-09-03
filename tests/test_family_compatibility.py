from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_snu_family_compatibility as audit
import build_appendard_fit_candidates as appendard_fit
import measure_hangul_latin_balance as balance
import render_snu_family_baselines as baseline_renderer
import review_appendard_size_restore as restore_review


class FamilyCompatibilityPolicyTests(unittest.TestCase):
    def test_shared_weight_range_is_complete_and_ordered(self) -> None:
        self.assertEqual(
            audit.STYLES,
            (
                ("Thin", 100),
                ("Light", 300),
                ("Regular", 400),
                ("Medium", 500),
                ("SemiBold", 600),
                ("Bold", 700),
                ("ExtraBold", 800),
            ),
        )

    def test_audit_samples_cover_size_weight_and_scientific_figures(self) -> None:
        self.assertTrue(set("HMxngp한가흙0") <= set(audit.REFERENCE_GLYPHS))
        self.assertEqual(audit.FIGURE_SAMPLE, "00112233445566778899")
        self.assertIn("Research", audit.LATIN_SAMPLE)
        self.assertIn("환경", audit.HANGUL_SAMPLE)

    def test_font_paths_follow_static_family_naming(self) -> None:
        source = audit.FamilySource("SNU Edge", "SNUEdge", Path("instance_otf"))
        self.assertEqual(
            source.font_path("SemiBold"),
            Path("instance_otf/SNUEdge-SemiBold.otf"),
        )

    def test_exact_baseline_panels_cover_reviewed_heavy_weights(self) -> None:
        self.assertEqual(
            baseline_renderer.STYLES,
            ("Regular", "SemiBold", "ExtraBold"),
        )

    def test_appendard_fit_transforms_korean_ranges_only(self) -> None:
        for codepoint in (0x1100, 0x3131, 0xA960, 0xAC00, 0xD7A3, 0xD7B0):
            with self.subTest(codepoint=codepoint):
                self.assertTrue(appendard_fit.is_hangul(codepoint))
        for codepoint in (0x0041, 0x0030, 0x3001, 0x4E00):
            with self.subTest(codepoint=codepoint):
                self.assertFalse(appendard_fit.is_hangul(codepoint))

    def test_appendard_fit_keeps_default_cff_width_implicit(self) -> None:
        private = type(
            "Private",
            (),
            {"defaultWidthX": 864, "nominalWidthX": 700},
        )()
        self.assertIsNone(appendard_fit.encoded_charstring_width(864, private))
        self.assertEqual(
            appendard_fit.encoded_charstring_width(900, private),
            200,
        )

    def test_appendard_blend_interpolates_from_identity(self) -> None:
        full = appendard_fit.Fit(0.9, 0.8, 30, 60, 0.85, 11172)
        halfway = appendard_fit.interpolate_fit(full, 0.5)
        self.assertEqual(halfway.x_scale, 0.95)
        self.assertEqual(halfway.y_scale, 0.9)
        self.assertEqual(halfway.x_shift, 15)
        self.assertEqual(halfway.y_shift, 30)
        self.assertEqual(halfway.advance_scale, 0.925)
        self.assertEqual(halfway.common_syllables, 11172)

    def test_balance_audit_uses_shared_size_references(self) -> None:
        self.assertEqual(balance.CAP_SAMPLE, "HIMNO")
        self.assertIn("x", balance.X_HEIGHT_SAMPLE)
        self.assertEqual(balance.LATIN_BODY_SAMPLE, "HgxM")
        self.assertEqual(balance.REFERENCE_GLYPHS, "HMxg")

    def test_size_restore_anchor_preserves_selected_center(self) -> None:
        fit = appendard_fit.Fit(0.97, 0.9, 5, 20, 0.98, 11172)
        before = {"y_min": -200, "y_max": 800}
        shift = restore_review.anchor_shift("keep-center", before, fit)
        original_center = 300
        selected_center = fit.y_scale * original_center + fit.y_shift
        self.assertEqual(original_center + shift, selected_center)

    def test_jaha_optical_restore_uses_safe_geometry(self) -> None:
        selected = appendard_fit.Fit(0.97, 0.971, 7, 25, 0.972, 11172)
        restored = restore_review.recommended_fit("SNU Jaha", selected)
        self.assertEqual(restored.x_scale, 1)
        self.assertEqual(restored.y_scale, restore_review.JAHA_SAFE_Y_SCALE)
        self.assertEqual(restored.x_shift, 0)
        self.assertEqual(restored.y_shift, selected.y_shift)
        self.assertEqual(restored.advance_scale, 1)


if __name__ == "__main__":
    unittest.main()
