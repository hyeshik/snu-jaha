# Latin alignment

SNU Jaha aligns Roboto Serif to the Latin glyphs already drawn in RIDIBatang,
instead of relying on nominal ascender, descender, or OS/2 values. All
measurements below use the Regular masters in a 1000 UPM coordinate system.

## Reference glyph fit

The reference set is `H M A I N o x n g p`: several cap widths, lowercase body
shapes, and two descenders. One affine transform is shared by every Roboto
Serif glyph so its internal texture and proportions remain coherent. Comparing
visible bounds and advance widths across the set gives the rounded transform:

```text
xScale = 0.895
yScale = 0.936
yShift = −11
```

Representative results are shown below. Bounds are `xMin…xMax × yMin…yMax`;
advance is the following number.

| Glyph | RIDIBatang | Roboto Serif source | SNU Jaha mapped |
| --- | ---: | ---: | ---: |
| `H` | 37.7…714 × −5…663; 752 | 53…801 × 0…710; 853 | 47.4…717 × −11…653.6; 763 |
| `M` | 37.7…855 × −5…663; 893 | 54…925 × −2…710; 979 | 48.3…827.9 × −12.9…653.6; 876 |
| `g` | 31…515 × −244…494.1; 525 | 30…619 × −244…573.1; 633 | 26.9…554 × −239.4…525.4; 567 |
| `n` | 36…574 × −5…492; 606 | 42…648 × 0…547; 675 | 37.6…580 × −11…501.0; 604 |
| `o` | 41…519 × −17…492; 560 | 48…587 × −11…547; 635 | 43.0…525.4 × −21.3…501.0; 568 |

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

Horizontal kerning values are scaled by the same 0.895 factor as outlines and
advance widths.

## Default figures

The default `0–9` outlines and metrics are copied from RIDIBatang without any
scaling. They are restrained lining figures with 560-unit tabular advances and
visible vertical bounds spanning roughly −25…677. This replaces Roboto Serif's
more irregular default figure silhouettes, whose transformed advances were
501 units.

The base glyph names remain the Roboto Serif names, so opt-in `onum`, `pnum`,
`zero`, `frac`, `sups`, `subs`, and `sinf` substitutions stay connected. The
`lnum` feature is intentionally a no-op because the RIDIBatang defaults are
already lining figures; `tnum` likewise leaves them at their default tabular
width.

## Dash–figure spacing

Roboto Serif supplied no kerning from hyphen, en dash, or em dash into its
figures. After the RIDIBatang defaults are installed, those three punctuation
marks share the following optical adjustments for `0` through `9`:

```text
−15, −20, −40, −20, −30, −20, 0, −30, 0, 0
```

The larger corrections for `1`, `2`, and `7` compensate for their open upper
left silhouettes at dash height. U+2212 MINUS SIGN intentionally remains
unkerned so signed values retain stable tabular spacing in equations and data
columns.
