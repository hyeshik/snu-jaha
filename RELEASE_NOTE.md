# SNU Jaha v0.2.0

SNU Jaha 0.2.0 rebuilds the complete static family around an unchanged Regular
with a wider and more practical optical weight range.

## Family

- Seven weights from Thin through ExtraBold, each in upright and native italic
  posture, provide 14 static OpenType/CFF fonts.
- RIDIBatang supplies Hangul and East Asian context glyphs; Roboto Serif 14pt
  supplies the Latin, Cyrillic, general punctuation, and OpenType layout system.
- Upright styles use fitted RIDIBatang tabular figures. Italic styles retain
  Roboto Serif's native italic figures and numeral features.
- Reviewed baseline, optical size, width, advance, weight, dash-to-figure
  spacing, capital-A joins, and italic-to-Hangul clearance are applied across
  the family.
- Thin through ExtraBold now use reviewed `−28`, `−12`, source, `+14`, `+22`,
  `+28`, and `+36` RIDIBatang constructions, paired with independently fitted
  Roboto Serif instances.
- Bold and ExtraBold use 104% and 108% visible Hangul advances to preserve
  spacing at their selected optical weights.

## Distribution

The release asset is `SNUJaha-0.2.0.zip`. Its flat archive root contains 14
static OTF files, `LICENSE.txt`, `LICENSE-RIDIBatang.txt`, and
`LICENSE-RobotoSerif.txt`. Specimens, source fonts, build files, and other
project documents are not included.

Every font reports `Version 0.2.0` in OpenType name ID 5, `0.2` in
`head.fontRevision`, and `0.2.0` in the CFF version field.
