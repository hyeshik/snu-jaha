# Weight development

All published Roboto Serif instances use `opsz=14` and `wdth=91`. Their
outlines are scaled horizontally by 0.895 and centered in advances scaled by
0.889. The `wght`
coordinates below describe the remaining family progression.

## Candidate A

The first four-style range preserves the approved Bold as the upper bound and
divides the Regular-to-Bold interval into three equal construction steps.

| Style | Output class | RIDIBatang increase | Roboto source `wght` | Figure x-scale |
|---|---:|---:|---:|---:|
| Regular | 400 | +0 | 400 | 1.000000 |
| Medium | 500 | +8 | 466.667 | 0.981333 |
| SemiBold | 600 | +16 | 533.333 | 0.962667 |
| Bold | 700 | +24 | 600 | 0.944000 |

The Roboto coordinates follow
`400 + (output weight - 400) × 2/3`. This is intentionally more conservative
than copying the output class directly to the Latin source axis. It retains the
mixed-script color approved in the first Bold proof.

## Measured progression

Ink areas below are measured from the final 1000 UPM CFF outlines. They are not
normalized percentages; the useful signal is the progression across each row.

| Glyph | Regular | Medium | SemiBold | Bold |
|---|---:|---:|---:|---:|
| 한 | 236,791 | 264,713 | 292,963 | 321,514 |
| 흙 | 269,569 | 304,370 | 339,576 | 375,129 |
| H | 165,754 | 191,204 | 217,771 | 242,940 |
| M | 204,463 | 232,087 | 259,987 | 285,591 |
| n | 108,512 | 125,786 | 142,789 | 159,312 |
| g | 157,247 | 177,167 | 196,692 | 215,673 |

The Hangul steps are close to linear in absolute ink area. Latin also remains
visibly progressive; `H` has a smaller final increment, but the broader sample
and the mixed-text proof keep SemiBold and Bold distinct.

## Upright tabular figures

All upright default digits finish at a 520-unit advance in every style and have
no digit-to-digit pair kerning. Horizontal outline correction first offsets the
outward growth caused by synthetic weighting; the selected B treatment then
reduces each RIDIBatang outline and its tabular cell together by 520/560. The
visible `00` gap progresses from 66 units in Regular to 60, 56, and 50 units in
Medium, SemiBold, and Bold. Italic styles instead retain Roboto Serif's native
italic tabular defaults at a 498-unit transformed advance.

## Roles

- Regular 400: continuous text and dense reading.
- Medium 500: introductions, labels, and restrained inline emphasis.
- SemiBold 600: section headings and key results.
- Bold 700: document titles and strong hierarchy.

An alternative scheme would relabel the current Bold as SemiBold and add
RIDIBatang +32 with Roboto Serif 700 as a new Bold. Candidate A does not need
that expansion: its four stages are distinguishable at 9–25 pt, while another
synthetic Hangul step would put additional pressure on the counters of `흙`,
`뿔`, and `률`. The stronger scheme remains a future display-weight option, not
the current text-family Bold.

## Light and Thin acceptance criteria

Light and Thin require negative synthetic weighting of the RIDIBatang source.
This is a different risk class from the positive Medium-to-Bold steps: fine
strokes, serif joins, and dots can split or disappear. A candidate succeeds
only when it passes every hard gate below and then passes the quantitative and
visual targets. Matching a nominal weight number alone is not sufficient.

### Intended roles

- Light 300: secondary text, introductions, captions, and restrained display;
  it must remain usable at 10–11 pt in print-oriented layouts.
- Thin 100: titles and large display at 18 pt or larger. Its 9–11 pt rendering
  is diagnostic, not a promise of body-text suitability.

The two styles must be visibly distinct from each other and from Regular in
their intended size ranges. Thin that works only at 32 pt or larger is too
fragile for this family.

### Outline hard gates

1. Preserve all 11,172 modern Hangul mappings and leave no newly empty encoded
   CJK, context-symbol, or default-figure glyph.
2. Introduce no new FontForge validation bits relative to the corresponding
   Regular build and remain loadable as OpenType/CFF by fontTools, FreeType,
   and Typst.
3. At 64 ppem, no audited glyph may gain a connected raster component relative
   to Regular. An increased component count is treated as a split stroke or
   serif until visual inspection proves otherwise.
4. Preserve every essential dot, diagonal, serif, and junction in the sparse
   sentinels `느 스 그 노 누 니 시 소 기 가 나 사` and the dense sentinels
   `뾂 뼒 뼮 뿳 휇 흙 뿔 률 쫓 빛 활 괄`.
5. Reject needle-like serif ends, flattened bowls, visibly pinched joins, and
   accidental sharp corners even if the glyph remains technically connected.

The Regular Hangul baseline contains ink areas from 127,913 to 382,517 square
font units, with a median of 279,450. The sparse and dense sentinels above come
from those extremes and supplement the more familiar proof words.

### Weight and mixed-script targets

All area ratios are measured against the final SNU Jaha Regular outlines after
the common Latin geometry transform.

| Measure | Light target | Thin target |
|---|---:|---:|
| Median Hangul ink-area ratio | 0.88–0.93 | 0.68–0.76 |
| Median Latin ink-area ratio | 0.88–0.93 | 0.68–0.76 |
| Hangul/Latin median-ratio difference | ≤ 0.04 | ≤ 0.05 |
| Minimum adjacent-family area separation | 0.06 from Regular | 0.12 from Light |

Roboto Serif at `wght` 333.333 and 200 provides initial Latin medians of about
0.917 and 0.727 on `H M A I N o x n g p`. These are reference points, not
preselected answers. RIDIBatang offsets must be selected by the same final-font
measurements rather than assumed from the positive-weight curve.

Across the full encoded set, ink area must be nondecreasing
(`Thin ≤ Light ≤ Regular`). Audited letters and default figures must be
strictly ordered; equality is allowed only for intentionally weight-invariant
symbols. The first-percentile Hangul ratio must remain at least 0.80 for Light
and 0.55 for Thin; a lower outlier triggers glyph-level inspection even when
the median passes.

### Geometry and spacing gates

- Preserve every Hangul advance exactly in Thin and Light. The historical
  candidate review used 560-unit default figures; production applies the later
  selected 520-unit B treatment uniformly after weighting.
- Keep digit-to-digit kerning at zero. Repeated-figure spacing must be repaired
  inside the common tabular cell, not with pair positioning.
- Target an outline `00` gap of `78 ± 3` units for Light and `90 ± 5` units for
  Thin, continuing outward from Regular's 72-unit gap.
- Keep the Latin baseline transform unchanged. Visible cap and x-height tops
  may differ from Regular by at most 2 units after rounding.
- Preserve all current GSUB/GPOS features and recheck dash-to-figure spacing in
  each new style.
- Set OpenType classes to Light 300 and Thin 100. Both styles use neither the
  Regular nor Bold legacy style bit, and both use `macStyle == 0`.

### Raster and specimen gates

The proof must include vector and unhinted grayscale raster comparisons at 96,
144, and 300 dpi.

- Light: mandatory checks at 9, 10, 11, 14, and 24 pt; it must have continuous
  essential strokes at 10–11 pt and an even paragraph color at 11 pt.
- Thin: diagnostic checks at 9, 11, and 14 pt, plus mandatory checks at 18,
  24, and 36 pt; it must be structurally complete and visibly intentional from
  18 pt upward.
- Both: compare Korean-only, Latin-only, mixed Korean/Latin, tabular figures,
  scientific units, punctuation, and the sparse/dense sentinel sets.
- A mixed run must not make either script look more than one weight step darker
  than the other. Two reviewers should be able to order `Thin–Light–Regular`
  correctly without seeing the labels.

### Candidate search, before full builds

Start with representative-glyph microproofs rather than thinning all CJK
glyphs immediately:

- Light: RIDIBatang offsets `-6`, `-8`, and `-10`; Roboto source weights in the
  `320–350` range.
- Thin: RIDIBatang offsets `-16`, `-20`, and `-24`; Roboto source weights in the
  `180–230` range.
- Compare at least FontForge's current `auto` and `squish` counter behavior.

Only the best Light and Thin construction candidates proceed to full-font
builds, the all-glyph monotonicity scan, and the final specimen. If none passes
the hard gates, the correct result is to omit that style rather than publish a
damaged synthetic weight.

### Stage 1 microfont result

The representative-glyph search built 12 CJK microfonts across all planned
offset/counter combinations and six transformed Roboto Serif instances. The
following `auto` results determine the shortlist; area and gap values are
measured against the final SNU Jaha Regular.

| CJK candidate | Median area | First percentile | `00` gap | Result |
|---|---:|---:|---:|---|
| Light −6 | 0.913 | 0.907 | 77.3 | promote |
| Light −8 | 0.885 | 0.875 | 79.2 | viable alternate |
| Light −10 | 0.856 | 0.844 | 81.1 | too light; gap high |
| Thin −16 | 0.770 | 0.751 | 87.0 | too dark |
| Thin −20 | 0.713 | 0.691 | 91.1 | promote |
| Thin −24 | 0.656 | 0.629 | 95.4 | too light; gap high |

`squish` produced the same audited Hangul area as `auto`, but held the `00`
gap near 70–71 units in every candidate. It therefore loses without providing
a measured outline-integrity advantage. Full builds will use `auto`.

| Roboto source | Median Latin area | Result |
|---|---:|---|
| Light 320 | 0.899 | pass |
| Light 333.333 | 0.915 | promote |
| Light 350 | 0.940 | too dark |
| Thin 180 | 0.700 | pass |
| Thin 200 | 0.726 | promote |
| Thin 230 | 0.771 | too dark |

Every negative CJK candidate increases the 64 ppem component count of `뿳`
from five to six and `휇` from six to seven. Enlarged vector outlines and binary
rasters show the same transition even at the smallest offset: a contact between
independent jamo strokes in the Regular raster opens into whitespace. No
within-stroke break or glyph loss occurs. These two exact `+1` transitions are
therefore recorded as reviewed exceptions; a larger increase or the same
change in any other glyph remains a hard failure.

Stage 1 promotes RIDIBatang `−6 auto` with Roboto Serif `wght 333.333` for
Light, and RIDIBatang `−20 auto` with Roboto Serif `wght 200` for Thin. The
Light pair has only a 0.002 script-to-script median difference and preserves a
0.087 separation from Regular. The Thin pair differs by 0.013 and retains the
conservative Roboto coordinate predicted by the existing family mapping.
Light `−8 / 320` remains a viable alternate if the full paragraph proof shows
that the promoted Light is too close to Regular, but it does not proceed as a
parallel construction path.

## Stage 2 full-font result

The promoted constructions were applied to all RIDIBatang glyphs retained in
SNU Jaha and merged with their corresponding transformed Roboto Serif
instances. Both outputs contain 12,999 glyphs and 12,656 encoded characters,
including all 11,172 modern Hangul syllables.

| Style | RIDI construction | Roboto `wght` | Hangul median | Hangul p1 | `00` gap |
|---|---:|---:|---:|---:|---:|
| Thin 100 | −20 auto | 200 | 0.704 | 0.684 | 84 |
| Light 300 | −6 auto | 333.333 | 0.911 | 0.904 | 72 |
| Regular 400 | source | 400 | 1.000 | 1.000 | 66 |

The complete encoded audit found no missing or newly empty glyph, no CJK or
figure advance mismatch, no sentinel ordering failure, and no 256 ppem raster
ink-order violation. The full Hangul ratio ranges are 0.667–0.740 for Thin and
0.901–0.923 for Light. These tighter full-set distributions confirm that the
representative glyphs did not hide an unusually weak or dark Hangul class.

Fourteen Latin composite or overlapping-contour glyphs produce misleading
signed vector-area totals because the static Regular and variable instances
encode their overlaps differently. All fourteen pass the union-aware 256 ppem
raster comparison; they are retained as review records rather than failures.
The hard sentinels remain strictly ordered in vector area.

The reviewed `뿳` and `휇` component separations are unchanged in the full
fonts, and no other audited glyph gains a raster component. Thin initially
created one overlapped CFF stem hint in `쀻`; the negative-weight build now
recalculates only glyphs carrying that FontForge validation bit after export.
The repaired Thin source and merged Thin font have the same validation mask as
their corresponding Light/Regular stages.

Before the ExtraBold study, the six-style family was:

| Style | Role |
|---|---|
| Thin 100 | display from 18 pt; 9–14 pt remains diagnostic |
| Light 300 | introductions, captions, and secondary text from 10–11 pt |
| Regular 400 | continuous reading |
| Medium 500 | restrained inline emphasis |
| SemiBold 600 | section headings and key results |
| Bold 700 | document titles and strong hierarchy |

## ExtraBold development

ExtraBold is treated as a new display style above the approved Bold, not as a
reason to relabel the existing family. Serif weight cannot be extended by
outline growth alone: the principal risk is that independent jamo strokes join
and enclosed counters collapse before the style becomes sufficiently distinct.

### Stage 1 alternatives

The representative search evaluates four RIDIBatang offsets (`+28`, `+30`,
`+32`, and `+36`) with three FontForge constructions:

- `auto`: extend the same weight and counter behavior used through Bold;
- `retain`: use automatic stroke classification while asking FontForge to
  retain counters;
- `CJK`: use CJK stroke classification with automatic counters.

Roboto Serif is independently sampled at `wght 610`, `620`, `633.333`, `650`,
and `666.667`. A further custom construction remains available only if the
direct candidates fail: use direction-dependent outline growth or protect the
specific jamo counters that close early. That path requires explicit glyph
rules and is not introduced as a fallback in the normal build.

### Promotion gates

A CJK microfont can proceed to a full build only when all audited glyphs retain
their mappings and advances, remain strictly heavier than Bold, and meet these
targets:

| Measure | ExtraBold target |
|---|---:|
| Median Hangul ink-area ratio vs Regular | 1.44–1.54 |
| Median separation from Bold | 0.08–0.16 |
| Hangul p99–p1 ratio spread | ≤ 0.10 |
| Outline `00` gap | 45–51 units |
| Hangul/Latin median-ratio difference | ≤ 0.05 |
| Enclosed counter area at 64 ppem | ≥ 70% of Bold |

The initial hard topology gate records every foreground-component merge and
enclosed-counter loss relative to Bold at 24, 32, 48, and 64 ppem. Positive
weight can legitimately join two independent jamo strokes, so a recorded merge
may be accepted only after enlarged vector and exact binary-raster review. An
enclosed counter that disappears at 64 ppem is not reviewable and rejects the
candidate. The intended minimum size must be decided from the 24 and 32 ppem
evidence before promotion; a candidate that works only above 24 pt is a display
style and must be documented as such.

The Latin candidate must have a median ratio of 1.47–1.56, remain 0.06–0.14
above Bold, and retain the common baseline, cap-height, and x-height geometry
within two font units. Full-font promotion would then repeat the encoded glyph,
advance, monotonicity, CFF validation, feature, dash-to-figure, and multi-DPI
specimen checks already used for the other styles.

### Stage 1 result

All 12 CJK microfonts preserved the representative mappings and advances and
were strictly heavier than Bold. None passed the initial topology gate without
review. The useful numerical shortlist is:

| Candidate | Hangul median | Separation from Bold | `00` gap | Merge / counter records |
|---|---:|---:|---:|---:|
| `+30 auto` | 1.440 | 0.088 | 50.4 | 32 / 2 |
| `+30 retain` | 1.493 | 0.142 | 50.4 | 36 / 2 |
| `+32 auto` | 1.470 | 0.118 | 49.2 | 43 / 2 |
| `+32 retain` | 1.527 | 0.175 | 49.2 | 45 / 1 |

The `CJK` method produces the same audited Hangul areas as `auto` but leaves
the repeated-figure gap at 77.7–80.0 units, so it provides no advantage and is
eliminated. Roboto Serif `wght 633.333` is the only Latin sample that passes all
numeric gates, with a 1.498 median and 0.071 separation from Bold.

The closest mixed-script color is therefore RIDIBatang `+30 retain` with
Roboto Serif `wght 633.333`: their median ratios differ by 0.005. Its two
counter-loss records are `뼒` at 24 ppem and `뺄` at 32 ppem; neither counter is
lost at 64 ppem, but seven representative foreground joins remain there.
RIDIBatang `+32 auto` with the same Latin source is the construction-consistent
alternate; it differs by 0.028 in mixed-script color and records nine joins at
64 ppem.

The five-page microproof presents the offset ladder, method comparison, exact
binary rasters, and mixed-script finalists. Visual review accepted `+30 retain`
as the best balance: its joins are consistent with a display ExtraBold rather
than damaged letterforms, and the small raster counter records do not erase
glyph identity. That review promotes only this construction to Stage 2.

### Stage 2 full-font result

The approved construction starts again from RIDIBatang Regular, applies `+30`
with `retain` counter behavior to all 11,805 eligible source glyphs, and first
recenters every changed outline in its original advance. Modern Hangul and
Hangul jamo cells are then widened to 104%, with the additional space divided
equally between the two sidebearings. Invisible Hangul filler controls and CJK
punctuation remain at their source advances. Default figures receive the 0.93
weight-stage outline correction and then the family-wide 520/560 outline/cell
reduction. The result is merged with the transformed
Roboto Serif `wght 633.333` instance and published as ExtraBold 800.

| Measure | Full ExtraBold result |
|---|---:|
| Encoded characters | 12,656 |
| Modern Hangul | 11,172 |
| Median Hangul area / Regular | 1.509 |
| Hangul p1–p99 | 1.461–1.551 |
| Median Hangul separation from Bold | 0.147 |
| Median Latin area / Regular | 1.498 |
| Median Latin separation from Bold | 0.071 |
| Hangul/Latin median difference | 0.011 |
| `00` gap | 46 units |
| Hangul advance scale | 1.04 |
| Minimum specimen Hangul-pair gap | 3.1 units |

The complete audit found no cmap difference, newly empty CJK glyph, unexpected
advance change, vector-area reversal, or 64 ppem raster-ink reversal between
Bold and ExtraBold. The intentional Hangul cell expansion changes the median
modern-syllable advance from 943 to 981 units; figures and other CJK glyphs do
not expand. Every modern Hangul syllable is strictly darker in both vector area
and 64 ppem raster ink. The generated CFF and merged font retain the same
validation masks as the corresponding accepted family stages.

At the former 943-unit Hangul advance, 617 of the 1,518 unique Hangul bigrams
collected from the specimen sources had a nonpositive outline gap. The widened
981-unit cell leaves all 1,518 pairs positive across 4,453 occurrences; the
tightest measured gap is 3.1 units. This is an ExtraBold spacing correction,
not a general proportional-width policy for the lighter styles.

The full-font rounding adds one small-size counter record (`뾂` at 48 ppem) to
the two Stage 1 records (`뼒` at 24 ppem and `뺄` at 32 ppem); none loses a
counter at 64 ppem. At 64 ppem, `뼮` retains all counters but their combined
area is 69.2% of Bold rather than the nominal 70% gate. This one-pixel boundary
case is accepted as the reviewed exception already visible in the microproof;
lower ratios or any 64 ppem counter disappearance remain failures.

ExtraBold is intended for primary titles, covers, and high-impact numeric
results from 18 pt upward. Its 10–14 pt rows remain diagnostic and do not make
it a body-text weight. The completed seven-weight range adds:

| Style | Role |
|---|---|
| ExtraBold 800 | strong display titles and key figures from 18 pt |

## Native italic range

Each published weight also has a native Roboto Serif italic counterpart at the
same `opsz=14`, `wdth=91`, and `wght` coordinate. The Latin outline, advance,
vertical fit, and kerning scale follow the corresponding upright style. Default
italic figures come from the same Roboto Serif instance at a 498-unit advance;
Hangul remains the upright RIDIBatang-derived construction.

Italic-to-Hangul spacing is derived after the final transforms. The build
collects every encoded non-CJK letter and number, follows GSUB single
substitutions, alternates, and ligatures to their terminal glyphs, and groups
their right overhangs in 5-unit classes. Upright Hangul left sidebearings are
grouped the same way. A final class-pair `kern` lookup supplies a 20-unit
minimum guard and increases it where needed to guarantee 30 units of optical
outline clearance. The seven-font audit covers every resulting letter and
figure terminal, all retained Hangul glyphs, and shaped `f`, `ff`, `fi`, `fl`,
`T`, `K`, `V`, `W`, `Y`, `J`, `j`, `r`, `t`, `x`, `z`, and default-figure
boundaries. Across the seven weights, the
italic representative-Latin median ink ratio is 0.9856–0.9944 of upright; the
mapped `H` and `x` tops differ by less than 0.004 units. All Hangul advances
and reviewed Hangul geometry samples remain identical between postures.
