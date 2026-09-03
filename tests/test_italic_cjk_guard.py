from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import add_italic_cjk_guard as guard


class ItalicCjkGuardTests(unittest.TestCase):
    def test_guard_inputs_include_letters_and_figures_but_not_cjk(self) -> None:
        self.assertTrue(guard.is_guard_input_codepoint(ord("T")))
        self.assertTrue(guard.is_guard_input_codepoint(ord("7")))
        self.assertTrue(guard.is_guard_input_codepoint(ord("Ж")))
        self.assertFalse(guard.is_guard_input_codepoint(ord("한")))
        self.assertFalse(guard.is_guard_input_codepoint(ord("①")))
        self.assertFalse(guard.is_guard_input_codepoint(ord("–")))

    def test_guard_covers_overhang_and_hangul_side_bearing(self) -> None:
        self.assertEqual(
            guard.guard_units(right_overhang=45, hangul_left_side_bearing=20),
            55,
        )
        self.assertEqual(
            guard.guard_units(right_overhang=-30, hangul_left_side_bearing=40),
            20,
        )

    def test_ligature_outputs_are_discovered_from_letter_inputs(self) -> None:
        ligature = SimpleNamespace(Component=["f"], LigGlyph="f_f")
        subtable = SimpleNamespace(ligatures={"f": [ligature]})
        self.assertEqual(
            guard.substitution_outputs(subtable, {"f"}),
            {"f_f"},
        )
        self.assertEqual(guard.substitution_outputs(subtable, {"T"}), set())

    def test_single_alternate_and_extension_outputs_are_discovered(self) -> None:
        single = SimpleNamespace(mapping={"K": "K.alt"})
        alternate = SimpleNamespace(alternates={"T": ["T.alt", "T.swash"]})
        extension = SimpleNamespace(LookupType=7, ExtSubTable=alternate)
        self.assertEqual(
            guard.substitution_outputs(single, {"K"}),
            {"K.alt"},
        )
        self.assertEqual(
            guard.substitution_outputs(extension, {"T"}),
            {"T.alt", "T.swash"},
        )


if __name__ == "__main__":
    unittest.main()
