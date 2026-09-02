# SNU Jaha

SNU Jaha is an OpenType/CFF serif prototype for Korean research and long-form
reading. Its name comes from Jahayeon (자하연) at Seoul National University.
The Regular build keeps Korean and East Asian glyphs from RIDIBatang and
replaces Latin, Cyrillic, and general punctuation with Roboto Serif 14pt
Regular. Default `0–9` figures come from RIDIBatang for restrained academic
number setting.

The first end-to-end build deliberately contains one style. It establishes the
source policy, geometry, metadata, OpenType feature retention, verification,
and specimen before the family grows to more weights.

## Design decisions

- Korean base: RIDIBatang 1.0.1, including all 11,172 modern Hangul syllables.
- Latin source: Roboto Serif v1.008, static 14pt optical-size Regular.
- Default figures: RIDIBatang's unscaled lining, tabular `0–9`, each with a
  560-unit advance. Roboto Serif numeral alternates remain available through
  explicit OpenType features.
- Latin geometry: 89.5% horizontal scale, 93.6% vertical scale, and an 11-unit
  downward shift in the 1000 UPM coordinate system. This common transform is
  fitted to representative Latin glyphs already present in RIDIBatang (`H`,
  `M`, `A`, `I`, `N`, `o`, `x`, `n`, `g`, and `p`) while retaining Roboto
  Serif's internal proportions.
- CJK punctuation, fullwidth forms, enclosed alphanumerics, and common CJK
  context symbols stay with RIDIBatang.
- ASCII/general punctuation, Latin and Cyrillic alphabets, figure alternates,
  and the Roboto Serif GSUB/GPOS features come from Roboto Serif.
- Roboto Serif kerning values are scaled with the Latin geometry.
- Hyphen, en dash, and em dash use figure-specific optical kerning before
  RIDIBatang's default digits; the mathematical minus sign remains unkerned.
- Family, full, and PostScript names are rewritten to `SNU Jaha`,
  `SNU Jaha Regular`, and `SNUJaha-Regular`.

The current transform is a measured starting point rather than a frozen family
contract. See `ALIGNMENT.md` for the reference measurements. The specimen gives
the evidence needed to tune spacing, punctuation, and stroke color before
adding weights.

## Build

Requirements:

- FontForge with Python scripting support
- Python 3 and fontTools
- Typst for the specimen
- `curl`, `sha256sum`, and `unzip`

Run:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make PYTHON=.venv/bin/python specimen
```

This creates:

- `dist/SNUJaha-Regular.otf`
- `proof/SNUJaha-Regular-Specimen.pdf`

For a dense three-page Korean/English scientific reading test with statistics,
units, tables, and citations, run:

```sh
make PYTHON=.venv/bin/python mixed-text-proof
```

This creates `proof/SNUJaha-Regular-Mixed-Text-Proof.pdf`.

`make sources` downloads the pinned official inputs and verifies their SHA-256
digests. Source fonts and generated outputs are intentionally ignored by Git.

## Verification

```sh
make PYTHON=.venv/bin/python test
make PYTHON=.venv/bin/python verify
```

The output audit checks CFF format, UPM, weight and embedding metadata, full
modern Hangul coverage, representative Latin/Cyrillic coverage, family names,
and the expected Roboto Serif layout features.

## Sources and licensing

- [RIDIBatang](https://ridicorp.com/ridibatang/), copyright RIDI and Sandoll.
- [Roboto Serif](https://github.com/googlefonts/roboto-serif), copyright the
  Roboto Serif Project Authors.

Both sources and SNU Jaha are distributed under the SIL Open Font License 1.1.
See `LICENSE`, `licenses/RIDIBatang.txt`, and `licenses/RobotoSerif.txt`.
SNU Jaha is an independent derivative and is not endorsed by the upstream
projects.
