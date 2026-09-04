# Weight construction

SNU Jaha 0.2.0 uses seven static weights in upright and native italic
postures. Regular is the fixed optical anchor; all other weights were selected
by comparing CJK and Latin raster coverage against that unchanged font.

All Roboto Serif instances use `opsz=14` and `wdth=91`. Their outlines are
scaled horizontally by 0.895 and vertically by 0.936, shifted down 11 units,
and centered in advances scaled by 0.889. Hangul keeps the production 0.984
vertical scale and 24.862-unit upward shift in every style.

## Production range

| Style | OS/2 class | RIDIBatang construction | Roboto Serif | Hangul advance | Upright figure x-scale |
|---|---:|---:|---:|---:|---:|
| Thin | 100 | `−28 retain` | `wght 100, GRAD −10` | 100% | 1.065333 |
| Light | 300 | `−12 auto` | `wght 250` | 100% | 1.028000 |
| Regular | 400 | source | `wght 400` | 100% | 1.000000 |
| Medium | 500 | `+14 auto` | `wght 500` | 100% | 0.967333 |
| SemiBold | 600 | `+22 auto` | `wght 565` | 100% | 0.948667 |
| Bold | 700 | `+28 retain` | `wght 610` | 104% | 0.934667 |
| ExtraBold | 800 | `+36 retain` | `wght 660` | 108% | 0.916000 |

Each RIDIBatang construction starts from Regular rather than from the preceding
weight. Synthetic weighting is recentered in the original cell. Bold and
ExtraBold then widen visible Hangul and jamo cells to 104% and 108%, while
invisible Hangul fillers and CJK punctuation keep their source advances.

Upright default digits are RIDIBatang outlines in a common 520-unit tabular
cell. The per-weight x-scale compensates for synthetic outline growth before
the final 520/560 family reduction. Italic digits remain native Roboto Serif
italic outlines in a 498-unit transformed cell.

## Selection measurements

The production leaders are reproduced alongside 48 CJK and 27 Latin
microfonts at 128
ppem. The ratios below are raster ink coverage per advance, normalized to
Regular. This makes the 104% and 108% heavy Hangul cells comparable to Latin
without mistaking a wider cell for a darker glyph.

| Style | CJK coverage | Latin coverage | Script difference |
|---|---:|---:|---:|
| Thin | 0.574 | 0.575 | 0.001 |
| Light | 0.826 | 0.810 | 0.016 |
| Medium | 1.203 | 1.195 | 0.008 |
| SemiBold | 1.320 | 1.316 | 0.004 |
| Bold | 1.400 | 1.397 | 0.003 |
| ExtraBold | 1.475 | 1.486 | 0.011 |

The adjacent coverage increases are approximately 44%, 21%, 20%, 10%, 6%,
and 5%. The first three large steps create visibly distinct Thin, Light,
Regular, and Medium roles; the upper range closes in evenly without the former
SemiBold-to-Bold jump.

The proof includes `뿔`, `뼒`, `뼮`, `뾂`, and `쫓` as encoded glyphs rather
than relying on a fallback font. Uppercase `A` and its related glyphs also run
through the production overlap removal, so the diagonal/crossbar junction in
heavy Latin is the same geometry used by the release fonts.

## Full-font audit

The Thin–Light–Regular audit covers all 12,656 encoded characters and all
11,172 modern Hangul syllables. It reports no cmap, advance, strict ordering,
or 256 ppem raster-order violation. Full Hangul outline-area medians are 0.565
for Thin and 0.822 for Light. Their `00` outline gaps are 92 and 78 units,
versus 66 units in Regular.

The Bold–ExtraBold audit uses coverage per advance for mixed-script color.

| Measure | Bold | ExtraBold |
|---|---:|---:|
| Median Hangul coverage / Regular | 1.417 | 1.496 |
| Median Latin coverage / Regular | 1.403 | 1.496 |
| `00` outline gap | 48 | 44 |

ExtraBold is 0.079 above Bold in median Hangul coverage and 0.093 above it in
Latin. Its Hangul/Latin median difference is below 0.001. Every modern Hangul
syllable remains heavier than Bold in vector area and at 64 ppem raster ink.
All 1,765 unique Hangul bigrams found in the specimen sources have positive
outline spacing; the minimum is 17.1 units across 5,834 occurrences.

ExtraBold remains a display weight. Dense forms produce foreground joins, and
the representative raster audit records counter losses at 32 ppem in `뾂`
and at 24 ppem in `휇`. No audited counter disappears at 64 ppem, and no
retained 64 ppem counter falls below 70% of its Bold area. A remaining-counter
area below 55% or any 64 ppem counter disappearance fails the build.

## Intended roles

| Style | Intended use |
|---|---|
| Thin 100 | large display from 18 pt |
| Light 300 | secondary text, captions, restrained display |
| Regular 400 | continuous reading |
| Medium 500 | introductions, labels, inline emphasis |
| SemiBold 600 | section headings and key results |
| Bold 700 | document titles and strong hierarchy |
| ExtraBold 800 | primary display titles and high-impact figures from 18 pt |

Thin and ExtraBold rows below their intended sizes are diagnostic. They do not
promise body-text performance.

## Native italic range

Each weight has a native Roboto Serif italic at the same axis coordinates.
Hangul remains upright and geometrically identical to its corresponding
upright style. A final class-pair `kern` lookup guarantees at least 30 units of
optical clearance at measured Latin/figure-to-Hangul boundaries. The complete
italic audit checks all seven styles and 20 shaped risk sequences.

## Reproduction

Run the microfont selection study with:

```sh
make PYTHON=.venv/bin/python weight-exploration
```

This writes `build/weight-exploration/audit.json` and the seven-page proof
`proof/SNUJaha-Weight-Exploration-Microproof.pdf`.

Run the full release audits with:

```sh
make PYTHON=.venv/bin/python weight-range-audit
make PYTHON=.venv/bin/python extrabold-full-audit
make PYTHON=.venv/bin/python italic-guard-audit
```

Their reports are `build/full-weight-audit.json`,
`build/extrabold-full-audit.json`, and
`build/italic-cjk-guard-audit.json`.
