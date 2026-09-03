#let ink = rgb("#192234")
#let accent = rgb("#1E5275")
#let blue = rgb("#477CA0")
#let green = rgb("#397363")
#let ochre = rgb("#9A6938")
#let coral = rgb("#A34F48")
#let violet = rgb("#735B86")
#let gray = rgb("#687382")
#let pale = rgb("#F0F3F4")
#let rule = rgb("#D5DDE2")
#let paper = rgb("#FCFBF7")
#let audit = json("../build/width-comparison/audit.json")
#let candidates = audit.at("candidates")
#let current = audit.at("current")
#let ridi = audit.at("ridibatang")
#let pct(value) = str(calc.round(value * 1000) / 10) + "%"
#let ratio(value) = pct(value / current.at("latin_advance"))

#set page(
  paper: "a4",
  margin: (left: 16mm, right: 16mm, top: 14mm, bottom: 15mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.2pt, tracking: 0.09em, fill: gray)[SNU JAHA · REGULAR WIDTH STUDY]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.4mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.2pt, fill: gray)[Roboto Serif width-axis study · RIDIBatang control],
      text(size: 6.6pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.72em)

#let eyebrow(body, color: accent) = text(
  size: 6.6pt,
  weight: 700,
  tracking: 0.105em,
  fill: color,
  body,
)
#let title(body, note: none) = block(breakable: false)[
  #eyebrow[REGULAR 400 / WIDTH CANDIDATE REVIEW]
  #v(2.5mm)
  #text(size: 22pt, weight: 700, body)
  #if note != none [#v(1.5mm) #text(size: 8pt, fill: gray, note)]
  #v(3.2mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]
#let short-row(label, family, recipe, color, body, size: 20pt) = block(breakable: false)[
  #grid(
    columns: (25mm, 1fr),
    column-gutter: 4mm,
    [
      #eyebrow(label, color: color)
      #v(0.8mm)
      #text(size: 6.3pt, fill: gray, recipe)
    ],
    [#text(font: family, size: size, body)],
  )
  #v(2.2mm)
]
#let texture-row(label, family, recipe, color) = block(breakable: false)[
  #grid(
    columns: (25mm, 1fr),
    column-gutter: 4mm,
    [#eyebrow(label, color: color) #v(0.7mm) #text(size: 6.2pt, fill: gray, recipe)],
    [
      #text(font: family, size: 15.5pt)[HAMBURGEFONTS minimum oxygen Hxngp · 환경 0127]
      #v(0.7mm)
      #text(font: family, size: 9.4pt)[RNA-seq response · recovery time 6.3 h · CO₂ 418.2 µmol/L]
    ],
  )
  #v(2mm)
]
#let long-row(label, family, recipe, color, body) = block(breakable: false)[
  #grid(
    columns: (25mm, 1fr),
    column-gutter: 4mm,
    [#eyebrow(label, color: color) #v(0.7mm) #text(size: 6.2pt, fill: gray, recipe)],
    [
      #set text(font: family, size: 8.55pt)
      #set par(justify: true, leading: 0.68em)
      #body
    ],
  )
  #v(2.5mm)
]
#let card(label, family, recipe, color, body) = block(
  breakable: false,
  width: 100%,
  inset: 3.2mm,
  radius: 1.2mm,
  stroke: 0.45pt + rule,
)[
  #eyebrow(label, color: color)
  #h(1.5mm)
  #text(size: 6.2pt, fill: gray, recipe)
  #v(1.5mm)
  #set text(font: family, size: 8.3pt)
  #set par(justify: true, leading: 0.68em)
  #body
]

#let short-text = [환경 Research 기록 · oxygen response 24 h]
#let long-text = [
  반복적 건조 처리 뒤 stomatal conductance와 photosystem II efficiency의 회복 속도를 분석했다.
  Control 16개체와 treatment 32개체를 0, 2, 8, 24, 48 h에 측정했으며, soil water content는
  31.2%에서 9.5%까지 감소했다. Estimated recovery constant는 6.3 h였고 95% CI는 4.8–7.9 h였다.
  RNA sequencing에서는 sample당 4.2 M reads를 얻었으며 median mapping rate는 94.7%였다.
]
#let narrow-text = [
  환경 반응의 시간적 변화를 설명하기 위해 transcript abundance, leaf temperature, CO₂ exchange를 함께 측정했다.
  Peak response는 8 h에서 관찰되었고 normalized effect size는 0.73 ± 0.08이었다. These observations support
  a timing-based model rather than a simple increase in response amplitude.
]

// Page 1 — immediate short-text comparison
#title(
  [Roboto Serif 폭 후보 5종],
  note: [현행 Jaha와 RIDIBatang 원본을 양 끝 기준으로 두었습니다. 모든 후보는 세로 크기와 baseline이 현행과 같습니다.],
)

#v(4mm)
#box(width: 100%, inset: 3.5mm, radius: 1.2mm, fill: pale)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 5mm,
    [#eyebrow[CONSTANT] #v(1mm) #text(size: 7.3pt)[opsz 14 · wght 400 · y 0.936 · shift −11]],
    [#eyebrow[JAHA FIGURES] #v(1mm) #text(size: 7.3pt)[0–9는 모든 Jaha 행에서 RIDIBatang 원형]],
    [#eyebrow[READING ORDER] #v(1mm) #text(size: 7.3pt)[안전한 축 조정 → 가로 축소 완화]],
  )
]

#v(5mm)
#short-row([CURRENT], "SNU Jaha", [W100 / X.895], accent, short-text)
#short-row([RIDI ORIGINAL], "RIDIBatang", [원본 한글·라틴], gray, short-text)
#short-row([A · MILD], "SNU Jaha Width A", [W95 / X.895], blue, short-text)
#short-row([B · MODERATE], "SNU Jaha Width B", [W92 / X.895], green, short-text)
#short-row([C · NARROW], "SNU Jaha Width C", [W90 / X.895], ochre, short-text)
#short-row([D · REBALANCED], "SNU Jaha Width D", [W85 / X.915], coral, short-text)
#short-row([E · AXIS-LED], "SNU Jaha Width E", [W80 / X.930], violet, short-text)

#v(2mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(3mm)
#text(size: 7.2pt, fill: gray)[
  짧은 행에서는 개별 글자의 찌그러짐, `Research`와 `minimum`의 폭, 한글과 영문 사이의 색 농도를 먼저 비교합니다.
]

#pagebreak()

// Page 2 — texture and measured width
#title(
  [글자꼴과 문장 폭을 분리해 보기],
  note: [첫 줄은 대표 대문자·소문자 윤곽, 둘째 줄은 학술 문맥의 숫자·단위 조합입니다.],
)

#v(4mm)
#texture-row([CURRENT], "SNU Jaha", [W100 / X.895], accent)
#texture-row([RIDI ORIGINAL], "RIDIBatang", [원본 한글·라틴], gray)
#texture-row([A · MILD], "SNU Jaha Width A", [W95 / X.895], blue)
#texture-row([B · MODERATE], "SNU Jaha Width B", [W92 / X.895], green)
#texture-row([C · NARROW], "SNU Jaha Width C", [W90 / X.895], ochre)
#texture-row([D · REBALANCED], "SNU Jaha Width D", [W85 / X.915], coral)
#texture-row([E · AXIS-LED], "SNU Jaha Width E", [W80 / X.930], violet)

#v(3mm)
#table(
  columns: (30mm, 27mm, 25mm, 31mm, 1fr),
  inset: (x: 1.7mm, y: 1.5mm),
  stroke: 0.35pt + rule,
  align: (left, left, right, right, left),
  table.header(
    [#eyebrow[VERSION]],
    [#eyebrow[RECIPE]],
    [#eyebrow[ADVANCE]],
    [#eyebrow[VS CURRENT]],
    [#eyebrow[ROLE]],
  ),
  [Current], [W100 / X.895], [#current.at("latin_advance")], [100.0%], [현행 기준],
  [RIDI original], [original], [#ridi.at("latin_advance")], [#ratio(ridi.at("latin_advance"))], [원본 질감 기준],
  [A], [W95 / X.895], [#candidates.at(0).at("latin_advance")], [#pct(candidates.at(0).at("latin_advance_ratio"))], [보수적 감소],
  [B], [W92 / X.895], [#candidates.at(1).at("latin_advance")], [#pct(candidates.at(1).at("latin_advance_ratio"))], [중간 감소],
  [C], [W90 / X.895], [#candidates.at(2).at("latin_advance")], [#pct(candidates.at(2).at("latin_advance_ratio"))], [강한 축 조정],
  [D], [W85 / X.915], [#candidates.at(3).at("latin_advance")], [#pct(candidates.at(3).at("latin_advance_ratio"))], [축·변환 재분배],
  [E], [W80 / X.930], [#candidates.at(4).at("latin_advance")], [#pct(candidates.at(4).at("latin_advance_ratio"))], [폭 축 중심],
)

#pagebreak()

// Page 3 — full-width long mixed text
#title(
  [긴 혼합문장의 행색],
  note: [동일한 8.55 pt, 문단 폭, 정렬, 행간입니다. 영문 용어가 만드는 회색 띠와 줄 끝 위치를 비교합니다.],
)

#v(4mm)
#long-row([CURRENT], "SNU Jaha", [W100 / X.895], accent, long-text)
#long-row([RIDI ORIGINAL], "RIDIBatang", [원본 한글·라틴], gray, long-text)
#long-row([A · MILD], "SNU Jaha Width A", [W95 / X.895], blue, long-text)
#long-row([B · MODERATE], "SNU Jaha Width B", [W92 / X.895], green, long-text)
#long-row([C · NARROW], "SNU Jaha Width C", [W90 / X.895], ochre, long-text)
#long-row([D · REBALANCED], "SNU Jaha Width D", [W85 / X.915], coral, long-text)
#long-row([E · AXIS-LED], "SNU Jaha Width E", [W80 / X.930], violet, long-text)

#pagebreak()

// Page 4 — narrow reading measure
#title(
  [좁은 단에서 드러나는 차이],
  note: [같은 문장을 좁은 폭에 넣었습니다. 줄바꿈뿐 아니라 `minimum`, `response`, `amplitude` 내부의 밀도를 확인합니다.],
)

#v(4mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 7mm,
  row-gutter: 4mm,
  card([CURRENT], "SNU Jaha", [W100 / X.895], accent, narrow-text),
  card([RIDI ORIGINAL], "RIDIBatang", [원본 한글·라틴], gray, narrow-text),
  card([A · MILD], "SNU Jaha Width A", [W95 / X.895], blue, narrow-text),
  card([B · MODERATE], "SNU Jaha Width B", [W92 / X.895], green, narrow-text),
  card([C · NARROW], "SNU Jaha Width C", [W90 / X.895], ochre, narrow-text),
  card([D · REBALANCED], "SNU Jaha Width D", [W85 / X.915], coral, narrow-text),
  card([E · AXIS-LED], "SNU Jaha Width E", [W80 / X.930], violet, narrow-text),
  block(width: 100%, inset: 3.2mm, radius: 1.2mm, fill: pale)[
    #eyebrow[CHECKLIST]
    #v(1.5mm)
    #text(size: 7.4pt, fill: gray)[
      ① `M/m/o`가 눌려 보이지 않는가?\
      ② 영문 단어가 한글보다 별도의 띠처럼 보이지 않는가?\
      ③ 작은 크기에서 counter가 닫히지 않는가?\
      ④ 문단의 줄 수와 rag가 자연스러운가?
    ]
  ],
)
