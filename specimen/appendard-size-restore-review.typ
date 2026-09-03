#let ink = rgb("#182236")
#let blue = rgb("#174D7A")
#let coral = rgb("#C34F45")
#let gray = rgb("#667085")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let report = json("../build/appendard-size-restore/report.json")
#let states = (
  ("original", "ORIGINAL"),
  ("selected-2-to-1", "2:1 SELECTED"),
  ("recommended", "OPTICAL RESTORE · ADOPTED"),
  ("keep-center", "RESTORE / CENTER"),
  ("keep-shift", "RESTORE / SHIFT"),
  ("keep-bottom", "RESTORE / BOTTOM"),
)
#let family(label) = report.at("families").find(item => item.at("label") == label)
#let state(label, slug) = family(label).at("states").at(slug)
#let font-name(label, slug) = if slug == "original" {
  label
} else if slug == "selected-2-to-1" {
  label + " Blend O2A1"
} else {
  state(label, slug).at("candidate_family")
}
#let num(value) = str(calc.round(value * 10) / 10)
#let scale-num(value) = str(calc.round(value * 1000) / 1000)
#let eyebrow(body) = text(size: 6.7pt, weight: 700, tracking: 0.11em, fill: blue, body)
#let long-proof = [
  반복적 건조 처리 후 canopy temperature와 stomatal conductance를 24 h 간격으로 측정했다.
  Control group의 recovery index는 0.742 ± 0.021, treatment group은 0.781 ± 0.014였다.
]

#set page(
  paper: "a4",
  margin: (left: 16mm, right: 16mm, top: 15mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.4pt, tracking: 0.08em, fill: gray)[2:1 VERTICAL SIZE RESTORATION REVIEW]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.5mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.3pt, fill: gray)[Decision record · optical restore adopted across the production families],
      text(size: 6.8pt, fill: blue)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Appendard", size: 9pt, lang: "ko", fill: ink)
#set par(leading: 0.72em)

#for (index, label) in ("SNU Jaha", "SNU Edge").enumerate() [
  #let item = family(label)
  #eyebrow[REGULAR / ORIGINAL:APPENDARD 2:1]
  #v(2.8mm)
  #text(size: 23pt, weight: 700)[#label: 세로 크기 복원 검토와 채택]
  #v(1.8mm)
  #text(size: 8pt, fill: gray)[채택안은 가로·advance를 원복하고, Jaha y-scale은 안전한 0.984, Edge는 1.0을 사용합니다.]
  #v(3.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
  #v(5mm)

  #eyebrow[BASELINE RUN / 20 PT]
  #v(1.5mm)
  #grid(
    columns: (31mm, 1fr),
    row-gutter: 2.2mm,
    ..states.map(pair => (
      [#text(size: 6.2pt, weight: 700, fill: if pair.at(0) == "recommended" { blue } else if pair.at(0) == "selected-2-to-1" { coral } else { gray })[#pair.at(1)]],
      [#text(font: font-name(label, pair.at(0)), size: 20pt)[환경 Hgx 흙 Mixed 0127]],
    )).flatten(),
  )

  #v(6mm)
  #eyebrow[MEASURED MODERN HANGUL EXTENTS]
  #v(1.5mm)
  #table(
    columns: (34mm, 19mm, 19mm, 22mm, 22mm, 26mm),
    inset: (x: 1.2mm, y: 1.2mm),
    stroke: 0.35pt + rule,
    align: (left, right, right, right, right, right),
    table.header([STATE], [Y SCALE], [Y SHIFT], [MED Y MIN], [MED Y MAX], [ABOVE ASC]),
    ..states.map(pair => {
      let selected = state(label, pair.at(0))
      let fit = selected.at("fit")
      let audit = selected.at("audit")
      (
        [#pair.at(1)],
        [#scale-num(fit.at("y_scale"))],
        [#num(fit.at("y_shift"))],
        [#num(audit.at("hangul_y_min").at("median"))],
        [#num(audit.at("hangul_y_max").at("median"))],
        [#audit.at("metric_overflow").at("above_typo_ascender")],
      )
    }).flatten(),
  )

  #v(6mm)
  #eyebrow[LONG MIXED TEXT / 9 PT]
  #v(1.5mm)
  #grid(
    columns: (27mm, 1fr),
    row-gutter: 2.2mm,
    ..states.map(pair => (
      [#text(size: 6.2pt, weight: 700, fill: gray)[#pair.at(1)]],
      [#text(font: font-name(label, pair.at(0)), size: 9pt)[#long-proof]],
    )).flatten(),
  )

  #v(5mm)
  #box(width: 100%, inset: 4mm, radius: 1.4mm, fill: wash)[
    #if label == "SNU Jaha" [
      ascender 800을 넘는 현대 한글 수와 상단 인상을 우선 봅니다. line metric을 늘리면 다른 SNU 글꼴과의 줄높이 호환성이 달라집니다.
    ] else [
      ascender 850 안에 남는지, Montserrat 대문자와의 높이 차이가 과해지지 않는지, 받침이 다시 낮아 보이지 않는지 확인합니다.
    ]
  ]
  #if index == 0 [#pagebreak()]
]
