# SNU Jaha

Explore the complete SNU typeface collection on the [QBio Fonts website](https://qbio.io/share/fonts/).

SNU Jaha is an OpenType/CFF serif prototype for Korean research and long-form
reading. Its name comes from Jahayeon (자하연) at Seoul National University.
The family keeps Korean and East Asian glyphs from RIDIBatang and replaces
Latin, Cyrillic, and general punctuation with Roboto Serif 14pt. Upright and
native italic postures are supplied at seven measured weights. Upright `0–9`
figures come from RIDIBatang for restrained academic number setting. Italic
styles retain Roboto Serif's native italic figures so numbers and Latin text
share one posture and rhythm.

## Design decisions

- Korean base: RIDIBatang 1.0.1, including all 11,172 modern Hangul syllables.
- Latin source: Roboto Serif v1.008 upright and native italic at a 14pt optical
  size and `wdth=91`.
- Default figures: upright styles use RIDIBatang lining, tabular `0–9`,
  horizontally reduced with their cells from 560 to 520 units. Weighted
  outlines are corrected before that common reduction. Italic styles keep the
  transformed Roboto Serif italic defaults at 498 units, together with their
  original `lnum`, `onum`, `pnum`, `tnum`, and related substitutions.
- Latin geometry: 89.5% horizontal outline scale, 88.9% advance scale, 93.6%
  vertical scale, and an 11-unit downward shift in the 1000 UPM coordinate
  system. Each outline is centered in its separately scaled advance. This transform is
  fitted to representative Latin glyphs already present in RIDIBatang (`H`,
  `M`, `A`, `I`, `N`, `o`, `x`, `n`, `g`, and `p`) while retaining Roboto
  Serif's internal proportions.
- Hangul optical geometry: original RIDIBatang outline width, 98.4% vertical
  scale, and a 24.862-unit upward shift. Thin through SemiBold retain the source
  advance. Bold and ExtraBold widen visible Hangul advances to 104% and 108%
  respectively and center each outline in the enlarged cell. Invisible Hangul
  filler controls retain their source widths. This keeps the adopted
  Original:Appendard 2:1 baseline adjustment and reviewed optical-size
  restoration unchanged.
- CJK punctuation, fullwidth forms, enclosed alphanumerics, and common CJK
  context symbols stay with RIDIBatang.
- ASCII/general punctuation, Latin and Cyrillic alphabets, figure alternates,
  and the Roboto Serif GSUB/GPOS features come from Roboto Serif.
- Roboto Serif kerning values are scaled by 89.5% with the Latin outlines.
- Italic Latin and figure terminals and upright Hangul are grouped by their
  measured right overhang and left sidebearing. A final `kern` lookup
  guarantees at least 30 units of optical clearance for every class pair. Its
  input set starts from all encoded non-CJK letters and numbers and follows
  GSUB outputs, so `f` ligatures, numeral alternates, `T`, `K`, `V`, `W`, `Y`,
  and other potential overhangs are covered.
- Uppercase Latin `A`, its accented forms, and `AE` relatives have their
  crossbar/stem overlaps merged into continuous outlines, preventing white
  seams in heavy weights and small raster sizes.
- Seven Roboto arrow symbols whose source interpolation reverses below Regular
  at `wdth=91` keep their Regular outlines in Thin and Light. This prevents a
  lighter style from rendering darker than the following style.
- In upright styles, hyphen, en dash, and em dash use figure-specific optical
  kerning before RIDIBatang's default digits. Italic styles retain Roboto
  Serif's native dash-to-figure spacing. The mathematical minus sign remains
  unkerned in both postures.
- Family, style, full, and PostScript names are rewritten for all fourteen
  `SNU Jaha` styles, with correct italic and Bold Italic linking bits.

## Complete weight range

Version 0.2.0 keeps Regular unchanged and deliberately expands both sides of
it. The production coordinates are the reviewed leaders from the
Regular-anchored microfont study:

| Style | Metadata | RIDIBatang construction | Roboto source | Hangul advance | Figure x-scale |
|---|---:|---:|---:|---:|---:|
| Thin | 100 | −28 retain | `wght 100, GRAD −10` | 100% | 106.5333% |
| Light | 300 | −12 auto | `wght 250` | 100% | 102.8% |
| Regular | 400 | source | `wght 400` | 100% | 100% |
| Medium | 500 | +14 auto | `wght 500` | 100% | 96.7333% |
| SemiBold | 600 | +22 auto | `wght 565` | 100% | 94.8667% |
| Bold | 700 | +28 retain | `wght 610` | 104% | 93.4667% |
| ExtraBold | 800 | +36 retain | `wght 660` | 108% | 91.6% |

Korean, East Asian context glyphs, and the upright default figures receive the
listed FontForge weight offset. Weighting is first recentered in the original
cell. Bold and ExtraBold then widen only visible Hangul cells and distribute
the added space equally on both sides. CJK punctuation remains fixed. Upright
default figures finish in a common
520-unit cell. Italic default figures come from the corresponding Roboto Serif
instance and finish at 498 units after the Latin advance transform. Latin and
general punctuation use static upright or native italic Roboto Serif instances
at `wdth=91` and the listed weight coordinates, then retain the Regular
geometry transform.

Every synthetic weight starts directly from RIDIBatang Regular; no stage is
derived from another weighted output. Thin, Bold, and ExtraBold use `retain`
counter handling. ExtraBold remains a display style because some dense
counter and join changes are visible at small sizes; its accepted review
records are documented in `WEIGHTS.md`.

The full-font audit checks all 12,656 encoded characters, including all 11,172
modern Hangul syllables, for missing outlines, unexpected advance changes, and
`Thin ≤ Light ≤ Regular` raster-ink order. The ExtraBold audit independently
checks the intentional 104%/108% heavy-weight advances, complete
`Bold < ExtraBold` CJK
vector, 64 ppem raster order, and every Hangul bigram found in the specimen
sources for nonpositive inter-glyph spacing. The
upright specimen compares all seven weights, stresses dense Hangul counters,
figures, and the repaired capital-A junction, and tests hierarchy over six
pages and three raster resolutions. A separate four-page italic proof covers
the complete posture range, mixed scientific text, and Latin-to-Hangul risk
boundaries.

See `WEIGHTS.md` for measured ink areas, tabular-figure spacing, role
assignments, and the accepted upper-weight construction.

To reproduce the production weight selection around the unchanged Regular,
run:

```sh
make PYTHON=.venv/bin/python weight-exploration
```

This builds representative CJK and Latin microfonts for Thin, Light, Medium,
SemiBold, Bold, and ExtraBold; measures each candidate against fixed Regular
coverage; and writes `build/weight-exploration/audit.json` plus
the seven-page comparison proof
`proof/SNUJaha-Weight-Exploration-Microproof.pdf`. The microfonts include
the production Hangul geometry and 520-unit figures. Bold candidates include
the selected 104% Hangul advance. ExtraBold explores `+36` through
`+44`, `auto` and `retain` counters, and 104%/108% Hangul advances; its spacing
gate rejects any candidate with a nonpositive audited Hangul-pair outline gap.
Latin microfonts apply the same capital-`A` overlap cleanup as production so
the diagonal/crossbar junction remains valid at heavy weights. These are
review assets, not release fonts.

For the focused SemiBold–Bold–ExtraBold comparison, run:

```sh
make PYTHON=.venv/bin/python upper-weight-comparison
```

This records the selected Bold `+28 retain` and ExtraBold `+36 retain` pair
against the previous `+32`/`+44` construction, including 104%/108% Hangul
cells and matched Roboto Serif coordinates. The two-page result is
`proof/SNUJaha-Upper-Weight-Microproof.pdf`.

The common Latin transform remains a measured family parameter. See
`ALIGNMENT.md` for the reference measurements; the full specimen supplies the
evidence for any future spacing, punctuation, or optical-size refinement.

## Build

Requirements:

- FontForge with Python scripting support
- Python 3, fontTools, Pillow, NumPy, and uharfbuzz
- Typst for optional specimens
- `curl`, `sha256sum`, and `unzip`

Run:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make PYTHON=.venv/bin/python specimen
```

This creates the Regular font and its specimen:

- `dist/SNUJaha-Regular.otf`
- `proof/SNUJaha-Regular-Specimen.pdf`

To build the complete family, run:

```sh
make PYTHON=.venv/bin/python build
```

This creates fourteen fonts named
`dist/SNUJaha-{Thin,Light,Regular,Medium,SemiBold,Bold,ExtraBold}{,Italic}.otf`.
To also create both family proofs, run:

```sh
make PYTHON=.venv/bin/python family-specimen
make PYTHON=.venv/bin/python italic-specimen
```

This additionally creates the six-page upright
`proof/SNUJaha-Full-Weight-Range-Specimen.pdf` and the
four-page `proof/SNUJaha-Italic-Family-Specimen.pdf`. The italic target also
writes `build/italic-cjk-guard-audit.json` and 144 dpi page previews.

To build, verify, and package the complete family for distribution, run:

```sh
make PYTHON=.venv/bin/python distribution
```

The resulting `dist/SNUJaha-0.2.0.zip` has a flat archive root containing the
14 OTF files plus `LICENSE.txt`, `LICENSE-RIDIBatang.txt`, and
`LICENSE-RobotoSerif.txt`. The package deliberately excludes specimens, source
fonts, and project documentation. Archive entry order, timestamps, permissions,
and compression are fixed so identical inputs produce identical ZIP bytes.

The Latin-to-Hangul guard is OpenType pair positioning and therefore operates
inside one shaping run. Applications that split an italic Latin span and the
following upright Korean into separate runs cannot apply cross-run kerning;
when the mixed phrase itself is set in SNU Jaha Italic, its Hangul remains
visually upright and the guard is active.

To compare SNU Jaha with the current SNU Appendard, SNU Edge, and SNU Sprout
instances under controlled size, weight, and baseline conditions, run:

```sh
make PYTHON=.venv/bin/python compatibility-specimen
```

This creates the 11-page `proof/SNU-Family-Compatibility-Specimen.pdf`, a
machine-readable audit at `build/snu-family-compatibility/audit.json`, exact
common-baseline raster panels, and 144 dpi page previews. The proof compares
all four families at their seven shared weights, records reference-glyph and
line-box metrics, alternates families on a single unshifted baseline, and
stresses small scientific text, figures, units, punctuation, and document
hierarchies. The sibling output locations can be overridden with
`SNU_APPENDARD_DIR`, `SNU_EDGE_DIR`, and `SNU_SPROUT_DIR`.

To compare the production Roboto Serif Regular with a disposable Charis 7.000
Regular Latin replacement, run:

```sh
make PYTHON=.venv/bin/python charis-regular-comparison
```

This downloads and verifies the official Charis 7.000 archive, builds the
candidate as the separately installable `SNU Jaha Latin Alt` family, audits
all 11,172 modern Hangul syllables and the production default figures for
identity, and creates
`proof/SNUJaha-Roboto-Charis-Regular-Comparison.pdf`. The candidate preserves
Charis's native horizontal proportions and applies only a 100.5% vertical
scale with a 7-unit downward shift. It does not replace any production font.

To build disposable Regular candidates that interpolate each family's original
Hangul geometry toward SNU Appendard Regular, run:

```sh
make PYTHON=.venv/bin/python appendard-blend-specimen
```

This leaves the canonical fonts unchanged and creates twelve uniquely named
candidate OTFs under `build/appendard-blend/candidates`, the measured geometry
at `build/appendard-blend/report.json`, exact common-baseline rasters, and the
comparison proof `proof/SNU-Appendard-Blend-Regular-Candidates.pdf`. For each
of Jaha, Edge, and Sprout, the original-to-Appendard transform is applied at
original:Appendard ratios 2:1, 1:1, 1:2, and 0:1. The 0:1 endpoint is each
family's own full-fit font, not SNU Appendard itself. Latin, figures,
punctuation, global line metrics, and weight metadata are not transformed.

To measure the Hangul-to-Latin size balance of the selected 2:1 candidates
against RIDIBatang, NanumSquare Regular, and LINE Seed Sans KR Regular, run:

```sh
make PYTHON=.venv/bin/python appendard-balance-audit
```

The normalized outline-height, width, advance, and baseline-position report is
written to `build/appendard-blend/hangul-latin-balance-2to1.json`.

To build disposable Jaha and Edge candidates that restore the original vertical
size around the selected 2:1 geometry and audit center-, shift-, and
bottom-anchored alternatives, run:

```sh
make PYTHON=.venv/bin/python appendard-size-restore-review
```

The audit is written to `build/appendard-size-restore/report.json`, with its
comparison proof at `proof/SNU-Appendard-2to1-Size-Restore-Review.pdf`.

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

To reproduce the ExtraBold Stage 1 search, run:

```sh
make PYTHON=.venv/bin/python extrabold-audit
```

This compares 12 positive-weight CJK microfonts and five Roboto Serif
instances, audits counters and connections at 24, 32, 48, and 64 ppem, and
creates `proof/SNUJaha-ExtraBold-Microproof.pdf`. The command remains a Stage 1
search and does not itself replace the reviewed full ExtraBold construction.

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
figure source, dimensions, and advances, family names, and the expected Roboto
Serif layout features. `make italic-guard-audit` additionally checks every
measured letter/figure-to-Hangul geometry-class pair and shapes representative
`f`, `ff`, `fi`, `fl`, `T`, `K`, `V`, `W`, `Y`, lowercase, and figure risk
boundaries in every weight.

## Continuous integration and releases

GitHub Actions runs the unit tests, builds all 14 fonts from pinned sources,
checks every font, runs the full weight and italic-clearance audits, verifies
the flat ZIP layout, and uploads the ZIP as a 30-day workflow artifact on every
push and pull request. A tag matching the project version exactly (for example,
`v0.2.0`) publishes that same audited artifact as a GitHub Release using
`RELEASE_NOTE.md`; a mismatched tag is rejected before the build.

## Sources and licensing

- [RIDIBatang](https://ridicorp.com/ridibatang/), copyright RIDI and Sandoll.
- [Roboto Serif](https://github.com/googlefonts/roboto-serif), copyright the
  Roboto Serif Project Authors.

Both sources and SNU Jaha are distributed under the SIL Open Font License 1.1.
See `LICENSE`, `licenses/RIDIBatang.txt`, and `licenses/RobotoSerif.txt`.
SNU Jaha is an independent derivative and is not endorsed by the upstream
projects.
