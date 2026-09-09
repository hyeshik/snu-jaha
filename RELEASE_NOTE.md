# SNU Jaha 0.2.1

This release addresses missing Hangul, Latin text, and italic figures reported
when printing from Pages on macOS Tahoe to an HP Color LaserJet Pro M281fdw.
Final OTF export now rounds CFF outline and hint coordinates to integers after
all transformations. The observed failure pattern matches fractional
coordinates; physical reprinting remains pending.

- Check every generated glyph for integer coordinates before packaging.
- Update italic-figure verification to the final integer bounds.
- Preserve glyph coverage, advance widths, GSUB features, and upright kerning;
  recalculate italic CJK collision guards from the rounded outlines.

Validated all 14 OTFs and the 52-test suite. Distribution also runs the weight
range, ExtraBold, and italic CJK guard audits.

`SNUJaha-0.2.1.zip` contains 14 OTFs and the font licenses.
