#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let brown = rgb("#8A5A35")
#let purple = rgb("#76528A")
#let coral = rgb("#C34F45")
#let gray = rgb("#667085")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let audit = json("../build/snu-family-compatibility/audit.json")
#let raster-dir = "../build/snu-family-compatibility/rasters"

#let families = (
  ("SNU Jaha", accent),
  ("SNU Appendard", green),
  ("SNU Edge", brown),
  ("SNU Sprout", purple),
)
#let styles = (
  ("Thin", 100),
  ("Light", 300),
  ("Regular", 400),
  ("Medium", 500),
  ("SemiBold", 600),
  ("Bold", 700),
  ("ExtraBold", 800),
)

#let family(name) = audit.at("families").find(item => item.at("name") == name)
#let style(name, style-name) = family(name).at("styles").find(item => item.at("style") == style-name)
#let glyph(name, character) = style(name, "Regular").at("glyphs").at(character)
#let round1(value) = calc.round(value * 10) / 10
#let percent(value) = str(round1(value * 100)) + "%"
#let unit(value) = str(calc.round(value))

#set page(
  paper: "a4",
  margin: (left: 16mm, right: 16mm, top: 15mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.4pt, tracking: 0.08em, fill: gray)[
      SNU FONT FAMILY · SIZE / WEIGHT / BASELINE COMPATIBILITY
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.5mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.3pt, fill: gray)[Jaha · Appendard · Edge · Sprout / 100–800],
      text(size: 6.8pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Appendard", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.76em)

#let eyebrow(body) = text(size: 6.7pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let title(body, note: none) = block(breakable: false)[
  #eyebrow[CROSS-FAMILY PROOF / CONTROLLED COMPARISON]
  #v(2.7mm)
  #text(size: 23pt, weight: 700, body)
  #if note != none [
    #v(1.5mm)
    #text(size: 8pt, fill: gray, note)
  ]
  #v(3.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let family-label(name, color) = text(size: 6.7pt, weight: 700, tracking: 0.08em, fill: color, name)
#let sample-row(name, color, body, weight: 400, size: 20pt, note: none) = block(breakable: false)[
  #grid(
    columns: (34mm, 1fr),
    column-gutter: 4mm,
    [
      #family-label(name, color)
      #if note != none [#v(0.7mm) #text(size: 6.4pt, fill: gray, note)]
    ],
    [#text(font: name, weight: weight, size: size, body)],
  )
]

#let weight-ladder(name, color) = block(breakable: false)[
  #family-label(name, color)
  #v(1.5mm)
  #grid(
    columns: (19mm, 1fr),
    row-gutter: 1.1mm,
    ..styles.map(pair => (
      [#text(size: 6.4pt, fill: gray)[#pair.at(0) #str(pair.at(1))]],
      [#text(font: name, size: 13pt, weight: pair.at(1))[자하연 Research Hgx 0127 흙]],
    )).flatten(),
  )
]

#let metric-table() = table(
  columns: (28mm, 18mm, 18mm, 20mm, 20mm, 20mm, 22mm),
  inset: (x: 1.5mm, y: 1.4mm),
  stroke: 0.35pt + rule,
  align: (left, right, right, right, right, right, right),
  table.header(
    [#eyebrow[FAMILY]],
    [#eyebrow[H TOP]],
    [#eyebrow[X TOP]],
    [#eyebrow[한 TOP]],
    [#eyebrow[한 BOTTOM]],
    [#eyebrow[한 ADV]],
    [#eyebrow[0 ADV]],
  ),
  ..families.map(pair => {
    let name = pair.at(0)
    let h = glyph(name, "H")
    let x = glyph(name, "x")
    let han = glyph(name, "한")
    let zero = glyph(name, "0")
    (
      [#text(fill: pair.at(1), weight: 700)[#name]],
      [#unit(h.at("bounds").at(3))],
      [#unit(x.at("bounds").at(3))],
      [#unit(han.at("bounds").at(3))],
      [#unit(han.at("bounds").at(1))],
      [#unit(han.at("advance"))],
      [#unit(zero.at("advance"))],
    )
  }).flatten(),
)

// 01 — cover and map
#align(center)[
  #v(6mm)
  #eyebrow[COMPREHENSIVE SPECIMEN / STATIC OTF]
  #v(7mm)
  #text(size: 31pt, weight: 700)[네 서체, 하나의 기준선]
  #v(2mm)
  #text(size: 13pt, fill: green)[Size · weight · baseline · mixed-line compatibility]
]

#v(10mm)
#for (name, color) in families [
  #sample-row(name, color, [자하연의 연구 환경 · Hgx 0127], size: 23pt)
  #v(4mm)
]

#v(6mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr),
    column-gutter: 10mm,
    row-gutter: 4mm,
    [#eyebrow[01 / SIZE] #v(1mm) 동일 point size에서 한글 상·하단, H/x/g, 숫자 폭과 시각 크기를 비교합니다.],
    [#eyebrow[02 / BASELINE] #v(1mm) 같은 y 좌표의 raster와 실제 inline 조판을 나누어 검사합니다.],
    [#eyebrow[03 / WEIGHT] #v(1mm) 100–800의 절대 먹색과 각 가족 Regular 대비 증가율을 함께 봅니다.],
    [#eyebrow[04 / APPLICATION] #v(1mm) 작은 본문, 숫자·단위, 혼합 위계에서 가족 교체의 충격을 확인합니다.],
  )
]

#v(8mm)
#text(size: 7.5pt, fill: gray)[
  조건: UPM 1000 · Thin 100 / Light 300 / Regular 400 / Medium 500 / SemiBold 600 / Bold 700 / ExtraBold 800 ·
  Jaha·Edge optical restore / Sprout Original:Appendard 2:1 · outline 면적률과 128 ppem raster coverage 병기.
  이 proof는 서로 다른 디자인의 차이를 없애는 시험이 아니라,
  차이가 문서 조합에서 허용 가능한지 판단하기 위한 통제된 관찰판입니다.
]

#pagebreak()

// 02 — regular size
#title(
  [Regular 400의 시각 크기],
  note: [동일 24 pt, 동일 문구, 동일 baseline. 글자 폭과 검은 면적뿐 아니라 top/bottom 위치를 함께 봅니다.],
)
#v(4mm)
#for (name, color) in families [
  #sample-row(name, color, [Hgx 0127 한글 흙 자하연], size: 24pt, note: [24 PT / 400])
  #v(4mm)
]

#v(4mm)
#metric-table()

#v(6mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[MEASURED HEIGHT]
    #v(1.5mm)
    #text(size: 8.2pt)[
      Jaha의 H top은 654 UPM으로 네 가족 중 가장 낮고, Sprout은 734 UPM으로 가장 높습니다.
      반면 대표 한글 top은 788–806 UPM에 모여 있어 라틴 대문자에서 크기 차이가 더 크게 드러납니다.
    ]
  ],
  [
    #eyebrow[WIDTH]
    #v(1.5mm)
    #text(size: 8.2pt)[
      Jaha의 ‘한’ advance는 952 UPM으로 다른 세 가족의 864–877 UPM보다 넓습니다.
      같은 줄에서 가족을 바꾸면 높이보다 먼저 줄 길이와 문장 리듬이 달라질 수 있습니다.
    ]
  ],
)

#v(6mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(4mm)
#for (size-label, size) in (("9 PT", 9pt), ("12 PT", 12pt), ("18 PT", 18pt)) [
  #grid(
    columns: (16mm, 1fr),
    [#eyebrow[#size-label]],
    [#for (name, color) in families [#text(font: name, size: size, weight: 400, fill: color)[환경 Hgx] #h(3mm)]],
  )
  #v(2.3mm)
]

#pagebreak()

// 03 — regular baseline and line boxes
#title(
  [Baseline: 좌표와 line box],
  note: [붉은 선은 네 폰트에 동일하게 준 y=0입니다. 회색 선은 1 em 위이며, 어떤 optical offset도 적용하지 않았습니다.],
)
#v(4mm)
#image(raster-dir + "/baseline-regular.png", width: 100%)

#v(5mm)
#table(
  columns: (31mm, 18mm, 20mm, 20mm, 20mm, 20mm),
  inset: (x: 1.5mm, y: 1.4mm),
  stroke: 0.35pt + rule,
  align: (left, right, right, right, right, right),
  table.header(
    [#eyebrow[FAMILY]], [#eyebrow[CAP]], [#eyebrow[X]], [#eyebrow[TYPO BOX]], [#eyebrow[HHEA BOX]], [#eyebrow[LINE GAP]],
  ),
  ..families.map(pair => {
    let m = family(pair.at(0)).at("line_metrics")
    (
      [#text(fill: pair.at(1), weight: 700)[#pair.at(0)]],
      [#unit(m.at("cap_height"))],
      [#unit(m.at("x_height"))],
      [#unit(m.at("typo_box"))],
      [#unit(m.at("hhea_box"))],
      [#unit(m.at("hhea_line_gap"))],
    )
  }).flatten(),
)

#v(5mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  #eyebrow[READING THE RESULT]
  #v(1.3mm)
  동일 baseline 자체는 안정적이지만 자연 행 높이는 Jaha 1000, Appendard 1193, Edge 1135,
  Sprout 1324 UPM으로 다릅니다. 앱이 run별 font metrics로 line box를 결정하면 가족 교체 시 행간이 변할 수 있습니다.
  여러 가족을 한 문단에서 섞을 때는 자동 행간보다 문서 수준의 고정 leading을 권장합니다.
]

#pagebreak()

// 04 — heavy baselines
#title(
  [Baseline: SemiBold와 ExtraBold],
  note: [굵기가 올라갈 때 top·bottom 위치가 이동하는지, descender와 복잡한 한글이 기준선을 압박하는지 봅니다.],
)
#v(3mm)
#align(center)[#image(raster-dir + "/baseline-semibold.png", width: 78%)]
#v(4mm)
#align(center)[#image(raster-dir + "/baseline-extrabold.png", width: 78%)]

#v(4mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 8mm,
  [#eyebrow[CHECK / 600] #v(1mm) 절 제목과 강조 수치에 해당합니다. H, g, 0, ‘한’, ‘흙’의 상하 정렬과 가족별 어두워지는 속도를 함께 봅니다.],
  [#eyebrow[CHECK / 800] #v(1mm) display 조합입니다. 같은 weight 이름이 같은 절대 먹색을 뜻하지 않으므로 counter 폐쇄와 크기 인상을 우선합니다.],
)

#pagebreak()

// 05 — two ladders
#title(
  [Weight ladder I],
  note: [Jaha와 Appendard. 모든 행은 13 pt이며 style metadata 100–800을 그대로 호출했습니다.],
)
#v(5mm)
#weight-ladder("SNU Jaha", accent)
#v(7mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(6mm)
#weight-ladder("SNU Appendard", green)

#v(7mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  #eyebrow[OBSERVE]
  #v(1mm)
  Thin에서 Appendard가 훨씬 가볍고, Bold 이후에는 더 빠르게 어두워집니다. Jaha는 100–800 전체 변화폭이 상대적으로 좁아 named weight만으로 두 가족의 농도를 맞추기 어렵습니다.
]

#pagebreak()

// 06 — two ladders
#title(
  [Weight ladder II],
  note: [Edge와 Sprout. 앞 페이지와 같은 크기·문구·호출 조건입니다.],
)
#v(5mm)
#weight-ladder("SNU Edge", brown)
#v(7mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(6mm)
#weight-ladder("SNU Sprout", purple)

#v(7mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  #eyebrow[OBSERVE]
  #v(1mm)
  Edge와 Sprout도 Light 이후 기울기가 Jaha보다 큽니다. 특히 ExtraBold 조합은 800↔800만 보지 말고 700↔800 교차 비교까지 포함해야 시각 무게가 맞는 지점을 찾을 수 있습니다.
]

#pagebreak()

// 07 — quantitative curves
#title(
  [정량 weight 균일도],
  note: [각 셀은 128 ppem raster coverage의 ‘해당 가족 Regular 대비 비율’입니다. 100%가 각 가족의 400입니다.],
)
#v(4mm)
#eyebrow[HANGUL / RELATIVE TO EACH REGULAR]
#v(1.5mm)
#table(
  columns: (30mm,) + (17.5mm,) * 7,
  inset: (x: 1.1mm, y: 1.5mm),
  stroke: 0.35pt + rule,
  align: (left,) + (right,) * 7,
  table.header([#eyebrow[FAMILY]], ..styles.map(pair => [#eyebrow[#str(pair.at(1))]])),
  ..families.map(pair => (
    [#text(fill: pair.at(1), weight: 700)[#pair.at(0)]],
    ..styles.map(weight-pair => [#percent(style(pair.at(0), weight-pair.at(0)).at("raster_hangul_relative_to_regular"))]),
  )).flatten(),
)

#v(6mm)
#eyebrow[LATIN / RELATIVE TO EACH REGULAR]
#v(1.5mm)
#table(
  columns: (30mm,) + (17.5mm,) * 7,
  inset: (x: 1.1mm, y: 1.5mm),
  stroke: 0.35pt + rule,
  align: (left,) + (right,) * 7,
  table.header([#eyebrow[FAMILY]], ..styles.map(pair => [#eyebrow[#str(pair.at(1))]])),
  ..families.map(pair => (
    [#text(fill: pair.at(1), weight: 700)[#pair.at(0)]],
    ..styles.map(weight-pair => [#percent(style(pair.at(0), weight-pair.at(0)).at("raster_latin_relative_to_regular"))]),
  )).flatten(),
)

#v(7mm)
#eyebrow[REGULAR / ABSOLUTE COVERAGE]
#v(1.5mm)
#table(
  columns: (32mm, 31mm, 31mm, 31mm),
  inset: (x: 1.5mm, y: 1.5mm),
  stroke: 0.35pt + rule,
  align: (left, right, right, right),
  table.header([#eyebrow[FAMILY]], [#eyebrow[HANGUL]], [#eyebrow[LATIN]], [#eyebrow[FIGURES]]),
  ..families.map(pair => {
    let regular = style(pair.at(0), "Regular")
    (
      [#text(fill: pair.at(1), weight: 700)[#pair.at(0)]],
      [#percent(regular.at("hangul").at("coverage"))],
      [#percent(regular.at("latin").at("coverage"))],
      [#percent(regular.at("figures").at("coverage"))],
    )
  }).flatten(),
)

#v(7mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[REGULAR MATCH]
    #v(1mm)
    한글 Regular의 절대 면적률은 22.98–24.39%로 가깝습니다. 기본 본문끼리는 굵기보다 폭·height와 serif/sans 질감 차이가 더 먼저 보입니다.
  ],
  [
    #eyebrow[RANGE MISMATCH]
    #v(1mm)
    ExtraBold/Regular 한글 비는 Jaha #percent(style("SNU Jaha", "ExtraBold").at("raster_hangul_relative_to_regular")), Appendard #percent(style("SNU Appendard", "ExtraBold").at("raster_hangul_relative_to_regular")), Edge #percent(style("SNU Edge", "ExtraBold").at("raster_hangul_relative_to_regular")), Sprout #percent(style("SNU Sprout", "ExtraBold").at("raster_hangul_relative_to_regular"))입니다. Jaha의 상단 weight는 더 완만한 축입니다.
  ],
)

#pagebreak()

// 08 — exact and live mixed lines
#title(
  [한 줄에 네 가족 섞기],
  note: [위 이미지는 exact raster, 아래 행은 Typst inline shaping입니다. 어느 쪽도 baseline shift를 사용하지 않습니다.],
)
#v(4mm)
#image(raster-dir + "/mixed-baselines.png", width: 100%)

#v(6mm)
#eyebrow[LIVE INLINE / 400]
#v(1.5mm)
#text(size: 17pt, weight: 400)[
  #text(font: "SNU Jaha", fill: accent)[자하연 Hgx]
  #text(font: "SNU Appendard", fill: green)[ 연구환경 0127]
  #text(font: "SNU Edge", fill: brown)[ baseline 24 h]
  #text(font: "SNU Sprout", fill: purple)[ 한글 흙]
]
#v(4mm)
#eyebrow[LIVE INLINE / 600]
#v(1.5mm)
#text(size: 17pt, weight: 600)[
  #text(font: "SNU Sprout", fill: purple)[자하연 Hgx]
  #text(font: "SNU Edge", fill: brown)[ 연구환경 0127]
  #text(font: "SNU Appendard", fill: green)[ baseline 24 h]
  #text(font: "SNU Jaha", fill: accent)[ 한글 흙]
]
#v(4mm)
#eyebrow[LIVE INLINE / 800]
#v(1.5mm)
#text(size: 17pt, weight: 800)[
  #text(font: "SNU Edge", fill: brown)[자하연 Hgx]
  #text(font: "SNU Jaha", fill: accent)[ 연구환경 0127]
  #text(font: "SNU Sprout", fill: purple)[ baseline 24 h]
  #text(font: "SNU Appendard", fill: green)[ 한글 흙]
]

#v(7mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  가족 경계에서 확인할 항목: 대문자 높이의 점프 · 한글 장평 변화 · g descender 깊이 · 숫자 높이 ·
  space 전후의 리듬 · 400→600→800에서 한 run만 갑자기 어두워지는지.
]

#pagebreak()

// 09 — sizes, figures, punctuation
#title(
  [작은 크기·숫자·단위 stress],
  note: [화면 본문과 학술 데이터에서 자주 만나는 8–12 pt, tabular 수치, dash, minus, 위·아래 첨자를 반복합니다.],
)
#v(4mm)
#for (size-label, size) in (("8 PT", 8pt), ("9.5 PT", 9.5pt), ("11 PT", 11pt), ("14 PT", 14pt)) [
  #eyebrow[#size-label / REGULAR 400]
  #v(1mm)
  #for (name, color) in families [
    #grid(
      columns: (27mm, 1fr),
      [#text(size: 6.2pt, fill: color, weight: 700)[#name]],
      [#text(font: name, size: size)[엽록소 농도는 17.2 ± 0.8 µmol m#super[-2] s#super[-1]였고, 24–48 h 회복률은 91.7%였다. Hgx 0127]],
    )
    #v(1mm)
  ]
  #v(2.8mm)
]

#pagebreak()

// 10 — figures and punctuation
#title(
  [숫자·단위·구두점 stress],
  note: [같은 데이터 문자열로 tabular 폭, dash/minus의 중심 높이, 괄호와 첨자, 작은 수치 열의 정렬을 검사합니다.],
)
#v(4mm)
#eyebrow[FIGURES / DASH / MINUS / PUNCTUATION]
#v(2mm)
#for (name, color) in families [
  #grid(
    columns: (31mm, 1fr),
    [#family-label(name, color)],
    [#text(font: name, size: 12.5pt)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 · (24.8%) · [95% CI]]],
  )
  #v(3mm)
]

#v(4mm)
#eyebrow[FIGURE WEIGHT LADDER / SAME 11 PT CELL]
#v(1.5mm)
#table(
  columns: (29mm,) + (18mm,) * 7,
  inset: (x: 1mm, y: 1.7mm),
  stroke: 0.35pt + rule,
  align: (left,) + (center,) * 7,
  table.header([#eyebrow[FAMILY]], ..styles.map(pair => [#eyebrow[#str(pair.at(1))]])),
  ..families.map(pair => (
    [#text(fill: pair.at(1), weight: 700, size: 6.5pt)[#pair.at(0)]],
    ..styles.map(weight-pair => [#text(font: pair.at(0), size: 11pt, weight: weight-pair.at(1))[0127]]),
  )).flatten(),
)

#v(6mm)
#eyebrow[TABULAR COLUMN / REGULAR 400]
#v(2mm)
#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  column-gutter: 4mm,
  ..families.map(pair => [
    #box(width: 100%, inset: 3mm, radius: 1mm, stroke: 0.4pt + rule)[
      #text(size: 6.2pt, weight: 700, fill: pair.at(1))[#pair.at(0)]
      #v(1.5mm)
      #align(right)[#text(font: pair.at(0), size: 10pt)[
        1,248.00\
        17.20\
        −0.63\
        91.70%
      ]]
    ]
  ]),
)

#v(4mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  #eyebrow[SMALL-SIZE DECISION]
  #v(1mm)
  8–9.5 pt에서는 serif/sans 질감과 x-height 차이가 크게 보입니다. 숫자가 표의 열을 이루는 경우에는 baseline뿐 아니라 tabular 폭과 괄호·minus의 중심 높이를 독립적으로 확인합니다.
]

#pagebreak()

// 11 — applied combinations
#title(
  [실제 문서 위계 조합],
  note: [한 줄 안의 run 교체뿐 아니라 제목–초록–본문–표 캡션 사이의 크기·무게 연결을 네 가지 recipe로 시험합니다.],
)
#v(4mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 8mm,
  row-gutter: 8mm,
  [
    #box(width: 100%, inset: 4mm, radius: 1.5mm, stroke: 0.5pt + rule)[
      #eyebrow[A / JAHA BODY + APPENDARD UI]
      #v(2mm)
      #text(font: "SNU Appendard", size: 18pt, weight: 700)[반복적 건조와 회복]
      #v(1mm)
      #text(font: "SNU Edge", size: 8pt, weight: 500, fill: brown)[RESEARCH NOTE 24-017 · 2026.09]
      #v(3mm)
      #text(font: "SNU Jaha", size: 9.5pt)[처리군 48개체의 평균 회복 시간은 17.2 ± 0.8 h였다. Control 대비 effect size는 0.63이었다.]
      #v(2mm)
      #text(font: "SNU Appendard", size: 7.5pt, fill: gray)[Table 1. Recovery kinetics at 24–48 h.]
    ]
  ],
  [
    #box(width: 100%, inset: 4mm, radius: 1.5mm, stroke: 0.5pt + rule)[
      #eyebrow[B / EDGE TITLE + JAHA TEXT]
      #v(2mm)
      #text(font: "SNU Edge", size: 18pt, weight: 700)[자하연 수질 관측 2026]
      #v(1mm)
      #text(font: "SNU Sprout", size: 8pt, weight: 500, fill: purple)[n = 1,248 · median interval 7 d]
      #v(3mm)
      #text(font: "SNU Jaha", size: 9.5pt)[용존 산소는 8.41 mg L#super[-1]로 측정됐으며, 95% CI는 8.17–8.65였다.]
      #v(2mm)
      #text(font: "SNU Edge", size: 7.5pt, fill: gray)[Figure 2. Seasonal oxygen profile.]
    ]
  ],
  [
    #box(width: 100%, inset: 4mm, radius: 1.5mm, stroke: 0.5pt + rule)[
      #eyebrow[C / SPROUT DISPLAY + APPENDARD BODY]
      #v(2mm)
      #text(font: "SNU Sprout", size: 18pt, weight: 700)[식물환경 데이터 보고서]
      #v(1mm)
      #text(font: "SNU Jaha", size: 8pt, weight: 500, fill: accent)[Methods · Results · Discussion]
      #v(3mm)
      #text(font: "SNU Appendard", size: 9.5pt)[RNA abundance는 2, 8, 24 h에 측정했고 minimum read depth는 18.4 M였다.]
      #v(2mm)
      #text(font: "SNU Sprout", size: 7.5pt, fill: gray)[Supplementary dataset S3.]
    ]
  ],
  [
    #box(width: 100%, inset: 4mm, radius: 1.5mm, stroke: 0.5pt + rule)[
      #eyebrow[D / SAME-LINE EMPHASIS]
      #v(2mm)
      #text(font: "SNU Jaha", size: 17pt, weight: 700)[핵심 결과]
      #v(2mm)
      #text(font: "SNU Jaha", size: 9.5pt)[회복률은 ]
      #text(font: "SNU Edge", size: 9.5pt, weight: 700, fill: brown)[91.7%]
      #text(font: "SNU Jaha", size: 9.5pt)[였고, ]
      #text(font: "SNU Appendard", size: 9.5pt, weight: 600, fill: green)[p = 0.004]
      #text(font: "SNU Jaha", size: 9.5pt)[로 유의했다.]
      #v(3mm)
      #text(font: "SNU Sprout", size: 7.5pt, fill: gray)[Mixed inline run / no baseline shift]
    ]
  ],
)

#v(9mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 7mm,
  [#eyebrow[PASS SIGNAL] #v(1mm) 같은 역할에서 가족을 바꿔도 행의 top/bottom과 색이 위계를 깨지 않습니다.],
  [#eyebrow[CHECK SIGNAL] #v(1mm) 800 조합 또는 작은 serif/sans 혼합에서 한 run만 돌출됩니다.],
  [#eyebrow[REMEDY] #v(1mm) 먼저 인접 weight를 교차 비교하고, 그 다음 size/leading을 문서 토큰으로 조정합니다.],
)

#v(9mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[RECOMMENDED REVIEW ORDER]
  #v(1.5mm)
  ① 400의 H/x/한 폭과 baseline → ② 600·800의 교차 weight → ③ 8–12 pt 숫자·단위 →
  ④ 실제 앱의 line-height 엔진 → ⑤ 위 recipe를 프로젝트의 대표 문서로 치환해 최종 승인.
]
