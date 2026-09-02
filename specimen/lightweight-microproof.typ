#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let coral = rgb("#A64B3C")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let audit = json("../build/lightweight-audit/audit.json")

#set page(
  paper: "a4",
  margin: (left: 17mm, right: 17mm, top: 16mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.6pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · LIGHT / THIN MICROPROOF
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.6mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.6pt, fill: gray)[REPRESENTATIVE GLYPHS · NOT FULL FONT BUILDS],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.68em)

#let eyebrow(body) = text(size: 6.8pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let cjk(label) = audit.at("cjk").find(item => item.at("label") == label)
#let latin(label) = audit.at("latin").find(item => item.at("label") == label)
#let cjk-font(label) = cjk(label).at("family")
#let latin-font(label) = latin(label).at("family")
#let pair-font(cjk-label, latin-label) = (cjk-font(cjk-label), latin-font(latin-label))
#let ratio(value) = str(calc.round(value * 1000) / 1000)
#let metric(item) = [ink #ratio(item.at("median_ratio")) · 00 #str(calc.round(item.at("zero_gap") * 10) / 10)]
#let status(item) = if item.at("pass") [#text(fill: green, weight: 700)[PASS]] else [#text(fill: coral, weight: 700)[CHECK]]

#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / NEGATIVE OUTLINE AUDIT]
  #v(3.5mm)
  #text(size: 24pt, weight: 700, body)
  #if note != none [
    #v(1.8mm)
    #text(size: 8.2pt, fill: gray, note)
  ]
  #v(4.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let sample-cell(cjk-label, latin-label, size: 18pt, body) = block[
  #text(font: pair-font(cjk-label, latin-label), size: size, body)
]

// Page 1 — measured shortlist
#align(center)[
  #eyebrow[STAGE 1 / REPRESENTATIVE MICROFONTS]
  #v(7mm)
  #text(size: 32pt, weight: 700)[가벼운 굵기의 첫 관문]
  #v(2.5mm)
  #text(size: 13.5pt, fill: green)[Outline integrity before nominal weight]
]

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 6mm,
    [
      #eyebrow[CONNECTION REVIEW]
      #v(1.5mm)
      #text(size: 11pt, weight: 700, fill: green)[뿳 · 휇 허용]
      #v(1mm)
      #text(size: 7.4pt, fill: gray)[독립 자모 획의 접점 분리이며 주요 획 손상 없음]
    ],
    [
      #eyebrow[COUNTER RESULT]
      #v(1.5mm)
      #text(size: 11pt, weight: 700)[AUTO 우세]
      #v(1mm)
      #text(size: 7.4pt, fill: gray)[squish는 한글 ink가 같고 00 간격만 기준 이탈]
    ],
    [
      #eyebrow[STAGE 1 RESULT]
      #v(1.5mm)
      #text(size: 11pt, weight: 700)[−6/333 · −20/200]
      #v(1mm)
      #text(size: 7.4pt, fill: gray)[Light와 Thin의 full-font 진입 후보]
    ],
  )
]

#v(7mm)
#eyebrow[NUMERIC SHORTLIST]
#v(2mm)
#grid(
  columns: (25mm, 31mm, 31mm, 1fr),
  row-gutter: 2.2mm,
  [#text(size: 7pt, fill: gray)[PAIR]],
  [#text(size: 7pt, fill: gray)[CJK]],
  [#text(size: 7pt, fill: gray)[LATIN]],
  [#text(size: 7pt, fill: gray)[MIXED SAMPLE]],
  [#eyebrow[LIGHT A · 추천]],
  [#text(size: 8pt)[−6 auto · 0.913]],
  [#text(size: 8pt)[wght 333 · 0.915]],
  [#sample-cell("Light -6 auto", "Light wght 333", size: 15pt)[자하연 Recovery 24 h]],
  [#eyebrow[LIGHT B]],
  [#text(size: 8pt)[−8 auto · 0.885]],
  [#text(size: 8pt)[wght 320 · 0.899]],
  [#sample-cell("Light -8 auto", "Light wght 320", size: 15pt)[자하연 Recovery 24 h]],
  [#eyebrow[THIN A]],
  [#text(size: 8pt)[−20 auto · 0.713]],
  [#text(size: 8pt)[wght 180 · 0.700]],
  [#sample-cell("Thin -20 auto", "Thin wght 180", size: 15pt)[자하연 Recovery 24 h]],
  [#eyebrow[THIN B · 추천]],
  [#text(size: 8pt)[−20 auto · 0.713]],
  [#text(size: 8pt)[wght 200 · 0.726]],
  [#sample-cell("Thin -20 auto", "Thin wght 200", size: 15pt)[자하연 Recovery 24 h]],
)

#v(8mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (24mm, 1fr),
  row-gutter: 3.2mm,
  [#eyebrow[REGULAR]], [#text(size: 21pt)[느 스 그 노 · 뾂 뿳 휇 흙 뿔 률]],
  [#eyebrow[LIGHT A]], [#sample-cell("Light -6 auto", "Light wght 333", size: 21pt)[느 스 그 노 · 뾂 뿳 휇 흙 뿔 률]],
  [#eyebrow[LIGHT B]], [#sample-cell("Light -8 auto", "Light wght 320", size: 21pt)[느 스 그 노 · 뾂 뿳 휇 흙 뿔 률]],
  [#eyebrow[THIN A]], [#sample-cell("Thin -20 auto", "Thin wght 180", size: 21pt)[느 스 그 노 · 뾂 뿳 휇 흙 뿔 률]],
  [#eyebrow[THIN B]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 21pt)[느 스 그 노 · 뾂 뿳 휇 흙 뿔 률]],
)

#pagebreak()

// Page 2 — Light CJK construction matrix
#title(
  [Light: offset과 counter 방식],
  note: [각 행은 같은 offset입니다. 라틴은 비교를 격리하기 위해 모두 Roboto wght 333을 사용합니다.],
)

#v(5mm)
#grid(
  columns: (19mm, 1fr, 1fr),
  column-gutter: 5mm,
  row-gutter: 4mm,
  [#eyebrow[OFFSET]], [#eyebrow[AUTO]], [#eyebrow[SQUISH]],
  [#eyebrow[−6]],
  [
    #sample-cell("Light -6 auto", "Light wght 333", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Light -6 auto")) · #status(cjk("Light -6 auto"))]
  ],
  [
    #sample-cell("Light -6 squish", "Light wght 333", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Light -6 squish")) · #status(cjk("Light -6 squish"))]
  ],
  [#eyebrow[−8]],
  [
    #sample-cell("Light -8 auto", "Light wght 333", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Light -8 auto")) · #status(cjk("Light -8 auto"))]
  ],
  [
    #sample-cell("Light -8 squish", "Light wght 333", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Light -8 squish")) · #status(cjk("Light -8 squish"))]
  ],
  [#eyebrow[−10]],
  [
    #sample-cell("Light -10 auto", "Light wght 333", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Light -10 auto")) · #status(cjk("Light -10 auto"))]
  ],
  [
    #sample-cell("Light -10 squish", "Light wght 333", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Light -10 squish")) · #status(cjk("Light -10 squish"))]
  ],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[10–11 PT ROLE CHECK]
  #v(2mm)
  #grid(
    columns: (18mm, 1fr),
    row-gutter: 2mm,
    [#text(size: 7pt, fill: gray)[REGULAR]], [#text(size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum 17.2 µm]],
    [#text(size: 7pt, fill: gray)[−6 AUTO]], [#sample-cell("Light -6 auto", "Light wght 333", size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum 17.2 µm]],
    [#text(size: 7pt, fill: gray)[−8 AUTO]], [#sample-cell("Light -8 auto", "Light wght 320", size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum 17.2 µm]],
    [#text(size: 7pt, fill: gray)[−10 AUTO]], [#sample-cell("Light -10 auto", "Light wght 320", size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum 17.2 µm]],
  )
]

#v(7mm)
#eyebrow[TABULAR FIGURES]
#v(2mm)
#grid(
  columns: (18mm, 1fr),
  row-gutter: 2.2mm,
  [#text(size: 7pt, fill: gray)[REGULAR]], [#text(size: 15pt)[00 · 100 · 200 · 700 · 1000]],
  [#text(size: 7pt, fill: gray)[−6 AUTO]], [#sample-cell("Light -6 auto", "Light wght 333", size: 15pt)[00 · 100 · 200 · 700 · 1000]],
  [#text(size: 7pt, fill: gray)[−8 AUTO]], [#sample-cell("Light -8 auto", "Light wght 333", size: 15pt)[00 · 100 · 200 · 700 · 1000]],
  [#text(size: 7pt, fill: gray)[−10 AUTO]], [#sample-cell("Light -10 auto", "Light wght 333", size: 15pt)[00 · 100 · 200 · 700 · 1000]],
)

#pagebreak()

// Page 3 — Thin CJK construction matrix
#title(
  [Thin: 구조가 버티는 한계],
  note: [라틴은 모두 Roboto wght 200입니다. 9–14 pt는 진단용, 18 pt 이상이 실제 목표입니다.],
)

#v(5mm)
#grid(
  columns: (19mm, 1fr, 1fr),
  column-gutter: 5mm,
  row-gutter: 4mm,
  [#eyebrow[OFFSET]], [#eyebrow[AUTO]], [#eyebrow[SQUISH]],
  [#eyebrow[−16]],
  [
    #sample-cell("Thin -16 auto", "Thin wght 200", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Thin -16 auto")) · #status(cjk("Thin -16 auto"))]
  ],
  [
    #sample-cell("Thin -16 squish", "Thin wght 200", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Thin -16 squish")) · #status(cjk("Thin -16 squish"))]
  ],
  [#eyebrow[−20]],
  [
    #sample-cell("Thin -20 auto", "Thin wght 200", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Thin -20 auto")) · #status(cjk("Thin -20 auto"))]
  ],
  [
    #sample-cell("Thin -20 squish", "Thin wght 200", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Thin -20 squish")) · #status(cjk("Thin -20 squish"))]
  ],
  [#eyebrow[−24]],
  [
    #sample-cell("Thin -24 auto", "Thin wght 200", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Thin -24 auto")) · #status(cjk("Thin -24 auto"))]
  ],
  [
    #sample-cell("Thin -24 squish", "Thin wght 200", size: 19pt)[느 스 기 가 · 흙 뿳 휇]
    #linebreak()
    #text(size: 7pt, fill: gray)[#metric(cjk("Thin -24 squish")) · #status(cjk("Thin -24 squish"))]
  ],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[SIZE THRESHOLD / −20 AUTO]
  #v(2mm)
  #grid(
    columns: (16mm, 1fr),
    row-gutter: 2mm,
    [#text(size: 7pt, fill: gray)[11 PT]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 11pt)[흙과 뿔의 속공간 · recovery 17.2 µm]],
    [#text(size: 7pt, fill: gray)[14 PT]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 14pt)[흙과 뿔의 속공간 · recovery 17.2 µm]],
    [#text(size: 7pt, fill: gray)[18 PT]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 18pt)[흙과 뿔의 속공간 · recovery 17.2 µm]],
    [#text(size: 7pt, fill: gray)[24 PT]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 24pt)[흙과 뿔의 속공간]],
  )
]

#pagebreak()

// Page 4 — connection audit
#title(
  [접합부 검토: 허용 가능한 분리],
  note: [64 ppem raster에서 component가 하나 늘어난 뿳과 휇입니다. 벡터 구조와 이진 raster를 함께 검사해 독립 자모 획 사이 접점의 분리로 판정했습니다.],
)

#v(6mm)
#grid(
  columns: (24mm, 1fr, 1fr),
  column-gutter: 7mm,
  row-gutter: 5mm,
  [#eyebrow[CONTROL]], [#eyebrow[뿳]], [#eyebrow[휇]],
  [#eyebrow[REGULAR]], [#text(size: 52pt)[뿳]], [#text(size: 52pt)[휇]],
  [#eyebrow[LIGHT −6]], [#sample-cell("Light -6 auto", "Light wght 333", size: 52pt)[뿳]], [#sample-cell("Light -6 auto", "Light wght 333", size: 52pt)[휇]],
  [#eyebrow[LIGHT −8]], [#sample-cell("Light -8 auto", "Light wght 320", size: 52pt)[뿳]], [#sample-cell("Light -8 auto", "Light wght 320", size: 52pt)[휇]],
  [#eyebrow[THIN −20]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 52pt)[뿳]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 52pt)[휇]],
  [#eyebrow[THIN −24]], [#sample-cell("Thin -24 auto", "Thin wght 180", size: 52pt)[뿳]], [#sample-cell("Thin -24 auto", "Thin wght 180", size: 52pt)[휇]],
)

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[REVIEW RESULT]
  #v(2mm)
  #text(size: 9pt)[
    두 글자 모두 Regular의 굵기 때문에 서로 다른 자모 획이 raster에서 닿아 있었습니다.
    음수 offset에서는 그 접점만 분리되고, 획 내부가 끊기거나 작은 획이 유실되지는 않습니다.
    따라서 이 두 component 증가는 검토 완료 예외로 기록하고 구조 hard gate를 통과시켰습니다.
  ]
]

#pagebreak()

// Page 5 — Latin axis and mixed shortlist
#title(
  [Roboto 축과 혼합문장 shortlist],
  note: [라틴 축만 바꾼 뒤, 수치상 가까운 한글 후보와 조합했습니다.],
)

#v(5mm)
#grid(
  columns: (26mm, 1fr, 28mm),
  row-gutter: 3mm,
  [#eyebrow[LATIN]], [#eyebrow[HAMBURGEFONTS · minimum oxygen]], [#eyebrow[INK RATIO]],
  [#eyebrow[W320]], [#text(font: latin-font("Light wght 320"), size: 18pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("Light wght 320").at("median_ratio"))]],
  [#eyebrow[W333]], [#text(font: latin-font("Light wght 333"), size: 18pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("Light wght 333").at("median_ratio"))]],
  [#eyebrow[W350]], [#text(font: latin-font("Light wght 350"), size: 18pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("Light wght 350").at("median_ratio"))]],
  [#eyebrow[W180]], [#text(font: latin-font("Thin wght 180"), size: 18pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("Thin wght 180").at("median_ratio"))]],
  [#eyebrow[W200]], [#text(font: latin-font("Thin wght 200"), size: 18pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("Thin wght 200").at("median_ratio"))]],
  [#eyebrow[W230]], [#text(font: latin-font("Thin wght 230"), size: 18pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("Thin wght 230").at("median_ratio"))]],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#eyebrow[MIXED-SCRIPT PAIRS]
#v(2mm)
#grid(
  columns: (22mm, 1fr),
  row-gutter: 4mm,
  [#eyebrow[REGULAR]], [#text(size: 20pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#eyebrow[LIGHT A]], [#sample-cell("Light -6 auto", "Light wght 333", size: 20pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#eyebrow[LIGHT B]], [#sample-cell("Light -8 auto", "Light wght 320", size: 20pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#eyebrow[THIN A]], [#sample-cell("Thin -20 auto", "Thin wght 180", size: 20pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#eyebrow[THIN B]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 20pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[SCIENTIFIC FIGURES AND UNITS]
  #v(2mm)
  #grid(
    columns: (20mm, 1fr),
    row-gutter: 2.3mm,
    [#text(size: 7pt, fill: gray)[LIGHT A]], [#sample-cell("Light -6 auto", "Light wght 333", size: 12pt)[00 · 31.20% · 4.8 × 10⁶ · −2.7°C · 17.2 µm]],
    [#text(size: 7pt, fill: gray)[LIGHT B]], [#sample-cell("Light -8 auto", "Light wght 320", size: 12pt)[00 · 31.20% · 4.8 × 10⁶ · −2.7°C · 17.2 µm]],
    [#text(size: 7pt, fill: gray)[THIN A]], [#sample-cell("Thin -20 auto", "Thin wght 180", size: 12pt)[00 · 31.20% · 4.8 × 10⁶ · −2.7°C · 17.2 µm]],
    [#text(size: 7pt, fill: gray)[THIN B]], [#sample-cell("Thin -20 auto", "Thin wght 200", size: 12pt)[00 · 31.20% · 4.8 × 10⁶ · −2.7°C · 17.2 µm]],
  )
]
