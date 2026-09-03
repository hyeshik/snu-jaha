from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import finalize_font as finalizer


class FinalizeFontPolicyTests(unittest.TestCase):
    def test_selected_default_figure_advance_is_520(self) -> None:
        self.assertEqual(finalizer.DEFAULT_FIGURE_ADVANCE, 520)

    def test_default_figure_source_follows_posture(self) -> None:
        self.assertTrue(finalizer.uses_ridibatang_default_figures(False))
        self.assertFalse(finalizer.uses_ridibatang_default_figures(True))

    def test_style_metrics_follow_visible_latin_bounds(self) -> None:
        self.assertEqual(finalizer.STYLE_METRICS["Regular"].cap_height, 654)
        self.assertEqual(finalizer.STYLE_METRICS["Thin"].x_height, 492)
        self.assertEqual(finalizer.STYLE_METRICS["Light"].x_height, 492)
        self.assertEqual(finalizer.STYLE_METRICS["Regular"].x_height, 492)
        self.assertEqual(finalizer.STYLE_METRICS["Medium"].x_height, 492)
        self.assertEqual(finalizer.STYLE_METRICS["SemiBold"].x_height, 493)
        self.assertEqual(finalizer.STYLE_METRICS["Bold"].cap_height, 654)
        self.assertEqual(finalizer.STYLE_METRICS["Bold"].x_height, 494)
        self.assertEqual(finalizer.STYLE_METRICS["ExtraBold"].cap_height, 654)
        self.assertEqual(finalizer.STYLE_METRICS["ExtraBold"].x_height, 494)

    def test_candidate_metrics_can_override_production_defaults(self) -> None:
        metrics = finalizer.resolved_style_metrics("Regular", 667, 477)
        self.assertEqual(metrics.cap_height, 667)
        self.assertEqual(metrics.x_height, 477)
        self.assertEqual(
            finalizer.resolved_style_metrics("Regular"),
            finalizer.STYLE_METRICS["Regular"],
        )

    def test_charstring_width_uses_target_private_metrics(self) -> None:
        private = SimpleNamespace(defaultWidthX=560, nominalWidthX=885)
        self.assertIsNone(finalizer.encoded_charstring_width(560, private))
        self.assertEqual(finalizer.encoded_charstring_width(600, private), -285)

    def test_figure_width_candidate_scales_outline_and_advance_together(self) -> None:
        scale, shift = finalizer.figure_horizontal_transform(560, 520)
        self.assertAlmostEqual(scale, 520 / 560)
        self.assertEqual(shift, 0)
        self.assertEqual(round(36 * scale + shift), 33)

    def test_lnum_becomes_noop_without_changing_other_figure_features(self) -> None:
        lnum = SimpleNamespace(LookupListIndex=[34], LookupCount=1)
        onum = SimpleNamespace(LookupListIndex=[33], LookupCount=1)
        records = [
            SimpleNamespace(FeatureTag="lnum", Feature=lnum),
            SimpleNamespace(FeatureTag="onum", Feature=onum),
        ]
        font = {
            "GSUB": SimpleNamespace(
                table=SimpleNamespace(
                    FeatureList=SimpleNamespace(FeatureRecord=records)
                )
            )
        }

        self.assertEqual(finalizer.make_lining_figures_default(font), 1)
        self.assertEqual(lnum.LookupListIndex, [])
        self.assertEqual(lnum.LookupCount, 0)
        self.assertEqual(onum.LookupListIndex, [33])
        self.assertEqual(onum.LookupCount, 1)

    def test_dash_figure_adjustments_share_one_optical_policy(self) -> None:
        cmap = {
            ord(character): f"glyph-{ord(character):04X}"
            for character in finalizer.DASHES_WITH_FIGURE_KERNING
            + finalizer.DEFAULT_FIGURES
        }
        adjustments = finalizer.dash_figure_adjustments(cmap)

        self.assertEqual(len(adjustments), 21)
        for dash in finalizer.DASHES_WITH_FIGURE_KERNING:
            dash_name = cmap[ord(dash)]
            self.assertEqual(adjustments[(dash_name, cmap[ord("1")])], -20)
            self.assertEqual(adjustments[(dash_name, cmap[ord("2")])], -40)
            self.assertEqual(adjustments[(dash_name, cmap[ord("7")])], -30)
            self.assertNotIn((dash_name, cmap[ord("6")]), adjustments)


if __name__ == "__main__":
    unittest.main()
