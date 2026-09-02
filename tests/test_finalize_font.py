from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import finalize_font as finalizer


class FinalizeFontPolicyTests(unittest.TestCase):
    def test_charstring_width_uses_target_private_metrics(self) -> None:
        private = SimpleNamespace(defaultWidthX=560, nominalWidthX=885)
        self.assertIsNone(finalizer.encoded_charstring_width(560, private))
        self.assertEqual(finalizer.encoded_charstring_width(600, private), -285)

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


if __name__ == "__main__":
    unittest.main()
