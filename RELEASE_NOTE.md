# SNU Jaha 0.2.2

Apply the approved macOS system-font sizing and baseline fit to all 14 upright
and italic styles, keeping the SNU Jaha family and file names.

- Scale Hangul and Jamo uniformly by 0.937366801 and raise them 61.106322487 units.
- Scale Latin and other glyphs uniformly by 1.043479405 and raise them
  11.478273458 units, updating advances, kerning, anchors, and hint zones.
- Set line metrics to 952 / −241 / 0, enable USE_TYPO_METRICS, and add a Roman
  baseline at zero while retaining safe Windows clipping bounds.
- Keep tabular figures as the default, with final advances of 543 units upright
  and 520 units italic, and retain native Roboto Serif kerning and substitutions.
- Retain integer CFF export and distribution audits for the full weight range,
  ExtraBold outlines, and italic-to-CJK collision guards.
- Update font metadata and the distribution package to 0.2.2.

`SNUJaha-0.2.2.zip` contains 14 OTFs and the font licenses.
