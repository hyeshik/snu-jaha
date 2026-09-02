# Weight development

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
| 한 | 240,642 | 269,017 | 297,726 | 326,742 |
| 흙 | 273,953 | 309,318 | 345,098 | 381,228 |
| H | 166,344 | 196,096 | 223,029 | 240,648 |
| M | 207,449 | 237,217 | 265,181 | 291,983 |
| n | 109,876 | 128,164 | 145,708 | 161,805 |
| g | 160,278 | 182,118 | 202,097 | 219,054 |

The Hangul steps are close to linear in absolute ink area. Latin also remains
visibly progressive; `H` has a smaller final increment, but the broader sample
and the mixed-text proof keep SemiBold and Bold distinct.

## Tabular figures

All default digits retain a 560-unit advance in every style and have no
digit-to-digit pair kerning. Horizontal outline correction offsets the outward
growth caused by synthetic weighting. The visible `00` gap progresses from 72
units in Regular to 66, 60, and 54 units in Medium, SemiBold, and Bold.

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
