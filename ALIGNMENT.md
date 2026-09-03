# Latin alignment

SNU Jaha aligns Roboto Serif to the Latin glyphs already drawn in RIDIBatang,
instead of relying on nominal ascender, descender, or OS/2 values. All
measurements below use the Regular masters in a 1000 UPM coordinate system.
The selected production instance uses Roboto Serif `wdth=91`. Its outlines
retain the 0.895 horizontal scale while its advances use the tighter 0.889
scale; the vertical fit is unchanged from the earlier width study.

## Reference glyph fit

The reference set is `H M A I N o x n g p`: several cap widths, lowercase body
shapes, and two descenders. One affine transform is shared by every Roboto
Serif glyph so its internal texture and proportions remain coherent. Comparing
visible bounds and advance widths across the set gives the rounded transform:

```text
xScale = 0.895
advanceScale = 0.889
yScale = 0.936
yShift = −11
```

Representative results are shown below. Bounds are `xMin…xMax × yMin…yMax`;
advance is the following number.

| Glyph | RIDIBatang | Roboto Serif source | SNU Jaha mapped |
| --- | ---: | ---: | ---: |
| `H` | 37.7…714 × −5…663; 752 | 50…772 × 0…710; 822 | 42.4…688.6 × −11…653.6; 731 |
| `M` | 37.7…855 × −5…663; 893 | 51…893 × −2…710; 944 | 42.7…796.3 × −12.9…653.6; 839 |
| `g` | 31…515 × −244…494.1; 525 | 28…599 × −244…572.1; 613 | 23.2…534.3 × −239.4…524.5; 545 |
| `n` | 36…574 × −5…492; 606 | 41…628 × 0…547; 653 | 35.0…560.3 × −11…501.0; 581 |
| `o` | 41…519 × −17…492; 560 | 46…566 × −11…547; 612 | 39.3…504.7 × −21.3…501.0; 544 |

The source designs do not have identical proportions—RIDIBatang's `A` is
relatively wide while its `g` is compact—so no single transform can make every
glyph coincide. The chosen values minimize the overall mismatch without
individually distorting letters.

## Vertical relationship to Hangul

Roboto Serif's visible `H` top becomes 653.56 and its `x` top becomes 491.632,
so the OS/2 cap-height and x-height are rounded to 654 and 492. The mapped `H`
has a visual center of 321.28. RIDIBatang's modern Hangul median visual center
is 304.6, leaving a 16.7-unit offset—close to the 14.3-unit relationship used
by SNU Edge, but with the absolute Latin size taken directly from RIDIBatang.

The slightly wider `wdth=91` outlines retain Roboto Serif's proportions. Their
0.889 advances bring the representative visible pair-gap median to 60 units,
matching RIDIBatang Latin at 60 and the current Hangul median at 61. Horizontal
kerning values remain scaled by the 0.895 outline factor.

Roboto Serif builds `A` with a separate crossbar overlapping the two diagonal
stems. The final build unions those contours for `A`, accented variants, `AE`,
and related Cyrillic forms. This preserves the silhouette while eliminating
raster seams at the two joins, especially in Bold and ExtraBold.

## Default figures by posture

Upright default `0–9` outlines come from RIDIBatang, then their outlines and
tabular cells are reduced together from 560 to 520 units. Vertical geometry is
unchanged, spanning roughly −25…677. The selected width keeps the restrained
RIDIBatang silhouettes while fitting the mapped Roboto Serif Latin.

The base glyph names remain the Roboto Serif names, so opt-in `onum`, `pnum`,
`zero`, `frac`, `sups`, `subs`, and `sinf` substitutions stay connected. The
`lnum` feature is intentionally a no-op because the RIDIBatang defaults are
already lining figures; `tnum` likewise leaves them at their default tabular
width.

Italic styles instead keep Roboto Serif's native default `0–9` outlines. Their
560-unit source advances become 498 units through the same 0.889 advance scale
as the surrounding Latin. No figure outline is transplanted after the native
italic build, and `lnum` remains active along with the other upstream numeral
features.

## Dash–figure spacing

Roboto Serif supplied no kerning from hyphen, en dash, or em dash into its
figures. In upright styles, after the RIDIBatang defaults are installed, those
three punctuation marks share the following optical adjustments for `0`
through `9`:

```text
−15, −20, −40, −20, −30, −20, 0, −30, 0, 0
```

The larger corrections for `1`, `2`, and `7` compensate for their open upper
left silhouettes at dash height. U+2212 MINUS SIGN intentionally remains
unkerned so signed values retain stable tabular spacing in equations and data
columns. Italic styles retain Roboto Serif's unkerned source relationship
because both the punctuation and figures come from the same transformed font.

## Italic Latin-to-Hangul boundary

Italic styles use native Roboto Serif italic outlines at the same axis and
affine-transform coordinates. Their Hangul remains upright. A geometry-derived
class lookup is appended to every `kern` feature: all encoded non-CJK letters
and numbers, plus GSUB-reachable alternates or ligatures, are bucketed by right
overhang, while Hangul is bucketed by left sidebearing. The pair adjustment is
the smallest 5-unit step that provides at least 30 units of optical clearance,
with a 20-unit minimum. This covers `f` ligatures, numeral variants, and the
less obvious `T`, `K`, `V`, `W`, and `Y` boundaries without maintaining a
fragile character list.
