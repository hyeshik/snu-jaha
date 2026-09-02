# SNU Jaha

SNU Jaha is an OpenType/CFF serif prototype for Korean research and long-form
reading. Its name comes from Jahayeon (자하연) at Seoul National University.
The Regular build keeps Korean and East Asian glyphs from RIDIBatang and
replaces Latin, Cyrillic, and general punctuation with Roboto Serif 14pt
Regular. Default `0–9` figures come from RIDIBatang for restrained academic
number setting. The complete six-style range adds Thin, Light, Medium,
SemiBold, and Bold with measured source weights rather than treating weight
names as direct source-font substitutions.

## Design decisions

- Korean base: RIDIBatang 1.0.1, including all 11,172 modern Hangul syllables.
- Latin source: Roboto Serif v1.008 at a 14pt optical size.
- Default figures: RIDIBatang lining, tabular `0–9`, each with a 560-unit
  advance in every style. Weighted outlines are corrected within that fixed
  cell; Roboto Serif numeral alternates remain available through explicit
  OpenType features.
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
- Family, style, full, and PostScript names are rewritten for the six
  `SNU Jaha` styles.

## Complete weight range

The range keeps the approved Bold as its upper bound, retains the three measured
positive steps, and adds the two negative-weight constructions that passed the
representative and full-font audits:

| Style | Metadata | RIDIBatang increase | Roboto source `wght` | Figure x-scale |
|---|---:|---:|---:|---:|
| Thin | 100 | −20 | 200 | 104.6667% |
| Light | 300 | −6 | 333.333 | 101.4% |
| Regular | 400 | +0 | 400 | 100% |
| Medium | 500 | +8 | 466.667 | 98.1333% |
| SemiBold | 600 | +16 | 533.333 | 96.2667% |
| Bold | 700 | +24 | 600 | 94.4% |

Korean, East Asian context glyphs, and the default figures receive the listed
FontForge weight offset. Their advance widths are preserved; any glyph whose
weighting changes its advance is recentered before its original advance is
restored. Latin and general punctuation use static Roboto Serif instances at
the listed source coordinates and retain the Regular geometry transform.

The conservative source-weight mapping keeps the current Bold at 700. A second
scheme that would relabel it SemiBold and add RIDIBatang +32 / Roboto 700 as a
new Bold was considered, but the four Regular–Bold steps are visibly distinct
while the stronger scheme would put more pressure on dense Hangul counters at
small sizes.

The full-font audit checks all 12,656 encoded characters, including all 11,172
modern Hangul syllables, for missing outlines, advance changes, and
`Thin ≤ Light ≤ Regular` raster-ink order. Its specimen compares all six
weights, stresses dense Hangul counters and figures, and tests academic
document hierarchy over four pages and three raster resolutions.

See `WEIGHTS.md` for measured ink areas, tabular-figure spacing, role
assignments, and the comparison with a stronger alternative Bold.

The common Latin transform remains a measured family parameter. See
`ALIGNMENT.md` for the reference measurements; the full specimen supplies the
evidence for any future spacing, punctuation, or optical-size refinement.

## Build

Requirements:

- FontForge with Python scripting support
- Python 3, fontTools, Pillow, and NumPy
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

To build and verify all six static styles and the complete proof, run:

```sh
make PYTHON=.venv/bin/python family-specimen
```

This creates `dist/SNUJaha-{Thin,Light,Regular,Medium,SemiBold,Bold}.otf`,
`proof/SNUJaha-Full-Weight-Range-Specimen.pdf`, and four-page raster proofs at
96, 144, and 300 dpi.

To build the first Bold candidate and its three-page comparison proof, run:

```sh
make PYTHON=.venv/bin/python bold-specimen
```

This creates:

- `dist/SNUJaha-Bold.otf`
- `proof/SNUJaha-Bold-Candidate-Specimen.pdf`

To build all four styles and the three-page weight-range proof, run:

```sh
make PYTHON=.venv/bin/python weight-specimen
```

This additionally creates:

- `dist/SNUJaha-Medium.otf`
- `dist/SNUJaha-SemiBold.otf`
- `proof/SNUJaha-Weight-Range-Specimen.pdf`

To reproduce the representative-glyph search that selected Light and Thin, run:

```sh
make PYTHON=.venv/bin/python lightweight-audit
```

This builds disposable CJK/Latin microfonts, measures outline area, tabular
figure spacing, advances, and 64 ppem connectivity, then creates
`proof/SNUJaha-Light-Thin-Microproof.pdf`. The accepted Stage 1 construction
coordinates and reviewed connection exceptions are recorded in `WEIGHTS.md`.

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
make PYTHON=.venv/bin/python verify-all
```

The output audits check CFF format, UPM, style flags, weight and embedding
metadata, full modern Hangul coverage, representative Latin/Cyrillic coverage,
figure dimensions and advances, family names, and the expected Roboto Serif
layout features.

## Sources and licensing

- [RIDIBatang](https://ridicorp.com/ridibatang/), copyright RIDI and Sandoll.
- [Roboto Serif](https://github.com/googlefonts/roboto-serif), copyright the
  Roboto Serif Project Authors.

Both sources and SNU Jaha are distributed under the SIL Open Font License 1.1.
See `LICENSE`, `licenses/RIDIBatang.txt`, and `licenses/RobotoSerif.txt`.
SNU Jaha is an independent derivative and is not endorsed by the upstream
projects.
