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
#let report = json("../build/appendard-blend/report.json")
#let raster-dir = "../build/appendard-blend/rasters"

#let families = (
  ("SNU Jaha", "snujaha-progression.png", accent),
  ("SNU Edge", "snuedge-progression.png", brown),
  ("SNU Sprout", "snusprout-progression.png", purple),
)
#let candidate-ratios = (("2:1", "O2A1", 1 / 3), ("1:1", "O1A1", 1 / 2), ("1:2", "O1A2", 2 / 3))
#let comparison-ratios = (("1:0", "original", 0), ..candidate-ratios, ("0:1", "full-fit", 1))
#let progression = (("2:1", "O2A1"), ("1:1", "O1A1"), ("1:2", "O1A2"))
#let family(label) = report.at("families").find(item => item.at("label") == label)
#let blend(label, ratio) = family(label).at("blends").find(item => item.at("ratio") == ratio)
#let full-fit(label) = family(label).at("full_fit_candidate")
#let blend-font(label, ratio) = blend(label, ratio).at("candidate_family")
#let comparison-font(label, ratio) = if ratio == "1:0" { label } else if ratio == "0:1" { full-fit(label).at("candidate_family") } else { blend-font(label, ratio) }
#let raster-slug(slug) = lower(slug)
#let pct(value) = str(calc.round(value * 1000) / 10) + "%"
#let num(value) = str(calc.round(value * 10) / 10)
#let long-proof = [
  반복적 건조 처리 후 canopy temperature와 stomatal conductance를 24 h 간격으로 측정했다.
  Control group 48개체의 recovery index는 0.742 ± 0.021, treatment group은 0.781 ± 0.014였다.
  Mixed-effects model에서 soil moisture가 10% 감소할 때 response time은 1.8 h 늘었고,
  bootstrap 95% confidence interval은 1.2–2.4 h였다. 이 결과는 drought recovery 과정에서
  leaf temperature와 water-use efficiency가 함께 변한다는 가설을 지지한다.
]

#set page(
  paper: "a4",
  margin: (left: 16mm, right: 16mm, top: 15mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.4pt, tracking: 0.08em, fill: gray)[
      REGULAR HANGUL BLEND · ORIGINAL:APPENDARD 1:0 → 2:1 → 1:1 → 1:2 → 0:1
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.5mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.3pt, fill: gray)[Jaha · Edge · Sprout / twelve candidates + originals],
      text(size: 6.8pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Appendard", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.78em)

#let eyebrow(body) = text(size: 6.7pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let title(body, note: none) = block(breakable: false)[
  #eyebrow[REGULAR CANDIDATE / INTERMEDIATE GEOMETRY]
  #v(2.7mm)
  #text(size: 23pt, weight: 700, body)
  #if note != none [#v(1.5mm) #text(size: 8pt, fill: gray, note)]
  #v(3.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let ratio-card(ratio, alpha, note) = box(width: 100%, inset: 4mm, radius: 1.3mm, stroke: 0.5pt + rule)[
  #eyebrow[ORIGINAL:APPENDARD]
  #v(1.5mm)
  #text(size: 24pt, weight: 700)[#ratio]
  #v(1mm)
  #text(size: 8pt, fill: green)[full fit의 #pct(alpha)]
  #v(2mm)
  #text(size: 7pt, fill: gray)[#note]
]

#let metric-table(label, color) = {
  let item = family(label)
  let before = item.at("before")
  let endpoint = item.at("full_fit_candidate").at("after")
  table(
    columns: (29mm, 23mm, 23mm, 23mm, 23mm),
    inset: (x: 1.4mm, y: 1.4mm),
    stroke: 0.35pt + rule,
    align: (left, right, right, right, right),
    table.header([#eyebrow[STATE]], [#eyebrow[Y MIN]], [#eyebrow[Y MAX]], [#eyebrow[WIDTH]], [#eyebrow[ADV]]),
    [#text(fill: color, weight: 700)[1:0]], [#num(before.at("y_min"))], [#num(before.at("y_max"))], [#num(before.at("width"))], [#num(before.at("advance"))],
    ..progression.map(pair => {
      let after = blend(label, pair.at(0)).at("after")
      (
        [#text(fill: color, weight: 700)[#pair.at(0)]],
        [#num(after.at("y_min"))],
        [#num(after.at("y_max"))],
        [#num(after.at("width"))],
        [#num(after.at("advance"))],
      )
    }).flatten(),
    [#text(fill: color, weight: 700)[0:1]], [#num(endpoint.at("y_min"))], [#num(endpoint.at("y_max"))], [#num(endpoint.at("width"))], [#num(endpoint.at("advance"))],
  )
}

// 01 — definition and transform matrix
#align(center)[
  #v(5mm)
  #eyebrow[NINE INTERMEDIATE + THREE FULL-FIT REGULAR CANDIDATES]
  #v(7mm)
  #text(size: 29pt, weight: 700)[원본과 Appendard 사이의 세 지점]
  #v(2mm)
  #text(size: 12.5pt, fill: green)[Original:Appendard · 2:1 / 1:1 / 1:2]
]

#v(9mm)
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 5mm,
  ratio-card("2:1", 1 / 3, [원본 비례를 가장 많이 유지하는 후보]),
  ratio-card("1:1", 1 / 2, [원본과 full fit의 정확한 중간]),
  ratio-card("1:2", 2 / 3, [Appendard 방향이 가장 강한 후보]),
)

#v(7mm)
#eyebrow[INTERPOLATED TRANSFORMS]
#v(1.5mm)
#table(
  columns: (27mm, 17mm, 20mm, 20mm, 24mm, 22mm),
  inset: (x: 1.2mm, y: 1.3mm),
  stroke: 0.35pt + rule,
  align: (left, center, right, right, right, right),
  table.header([#eyebrow[FAMILY]], [#eyebrow[RATIO]], [#eyebrow[X SCALE]], [#eyebrow[Y SCALE]], [#eyebrow[SHIFT X/Y]], [#eyebrow[ADV]]),
  ..families.map(family-pair => {
    let label = family-pair.at(0)
    candidate-ratios.map(ratio-pair => {
      let fit = blend(label, ratio-pair.at(0)).at("fit")
      (
        [#text(fill: family-pair.at(2), weight: 700)[#label]],
        [#ratio-pair.at(0)],
        [#pct(fit.at("x_scale"))],
        [#pct(fit.at("y_scale"))],
        [+#num(fit.at("x_shift")) / +#num(fit.at("y_shift"))],
        [#pct(fit.at("advance_scale"))],
      )
    }).flatten()
  }).flatten(),
)

#v(6mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  #eyebrow[INTERPOLATION RULE]
  #v(1mm)
  각 후보는 원본 outline에서 직접 생성했습니다. scale과 advance는 identity 100%에서 full fit 값까지,
  shift는 0에서 full fit 값까지 같은 alpha로 선형 보간했습니다. 앞 후보를 다시 변환하지 않습니다.
]

#v(6mm)
#text(size: 7.3pt, fill: coral)[
  CANDIDATE ONLY — 라틴·숫자·구두점·전역 line metrics·원본 저장소의 canonical font는 변경하지 않았습니다.
]

#pagebreak()

// 02–04 — one family per page
#for (index, family-pair) in families.enumerate() [
  #let label = family-pair.at(0)
  #let raster = family-pair.at(1)
  #let color = family-pair.at(2)
  #title(
    [#label: 단계별 변화],
    note: [1:0 원본 → 2:1 → 1:1 → 1:2 → 0:1 가족별 full fit. 모든 raster 행은 동일 baseline입니다.],
  )
  #v(3mm)
  #align(center)[#image(raster-dir + "/" + raster, width: 82%)]
  #v(4mm)
  #metric-table(label, color)
  #v(5mm)
  #eyebrow[INTERNAL LATIN–HANGUL BALANCE / 17 PT]
  #v(1.5mm)
  #grid(
    columns: (20mm, 1fr),
    row-gutter: 2.3mm,
    ..comparison-ratios.map(state => (
      [#text(size: 6.3pt, fill: color, weight: 700)[#state.at(0)]],
      [#text(font: comparison-font(label, state.at(0)), size: 17pt)[Hgx 0127 환경 한글 흙]],
    )).flatten(),
  )
  #v(5mm)
  #box(width: 100%, inset: 3.5mm, radius: 1.3mm, fill: wash)[
    한글 하단이 충분히 올라왔는지와 동시에, 원본의 descender 깊이 및 H/x/g와 한글 사이의 고유 크기 관계가 남아 있는지 확인합니다.
  ]
  #if index < families.len() - 1 [#pagebreak()]
]

#pagebreak()

// 05 — same ratio across all families
#v(8mm)
#title(
  [같은 반영 비율에서 세 가족 비교],
  note: [각 panel은 Jaha·Edge·Sprout를 1:0 원본부터 0:1 가족별 full fit까지 같은 baseline에 놓습니다.],
)
#v(3mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 5mm,
  row-gutter: 3mm,
  ..comparison-ratios.map(state => [
    #image(raster-dir + "/blend-" + raster-slug(state.at(1)) + ".png", width: 100%)
  ]),
)

#v(2mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 8mm,
  [#eyebrow[1:0 → 0:1] #v(1mm) 각 가족의 원본, 세 중간 후보, full-fit 결과를 동일 baseline에서 연속 비교합니다.],
  [#eyebrow[ENDPOINTS] #v(1mm) 1:0과 0:1 모두 Jaha·Edge·Sprout의 고유 글꼴 형태를 유지합니다.],
)

#pagebreak()

// 06 — exact mixed runs across all five states
#title(
  [다섯 상태를 실제 한 줄에서 비교],
  note: [1:0 원본부터 0:1 가족별 full fit까지 exact raster를 renderer-side baseline shift 없이 조판했습니다.],
)
#v(4mm)
#image(raster-dir + "/mixed-ratios.png", width: 100%)
#v(5mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  가족 경계에서 한글 하단뿐 아니라 advance 변화에 따른 space 리듬, 라틴 descender 깊이, 한글의 상대적 크기를 함께 봅니다.
]

#pagebreak()

// 07 — live inline shaping across five states
#v(8mm)
#title(
  [다섯 상태의 실제 inline shaping],
  note: [같은 환경 Hgx run을 9·13·20 pt로 반복해 크기별 인상과 endpoint 차이를 확인합니다.],
)
#v(5mm)
#for (size-label, size) in (("9 PT", 9pt), ("13 PT", 13pt), ("20 PT", 20pt)) [
  #eyebrow[#size-label / LIVE INLINE]
  #v(1.3mm)
  #for (ratio, slug, alpha) in comparison-ratios [
    #grid(
      columns: (21mm, 1fr),
      [#text(size: 6.3pt, weight: 700, fill: gray)[#ratio]],
      [
        #text(size: size)[
          #text(font: comparison-font("SNU Jaha", ratio), fill: accent)[환경 Hgx]
          #text(font: comparison-font("SNU Edge", ratio), fill: brown)[ 환경 Hgx]
          #text(font: comparison-font("SNU Sprout", ratio), fill: purple)[ 환경 Hgx]
          #text(font: "SNU Appendard", fill: green)[ 0127 한글]
        ]
      ],
    )
    #v(1mm)
  ]
  #v(3mm)
]

#v(3mm)
#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
  1:0에서는 각 가족 원본을, 0:1에서는 각 가족 형태를 유지한 full-fit Jaha·Edge·Sprout를 사용합니다.
]

#pagebreak()

// 08–10 — one long paragraph page per family
#for (index, family-pair) in families.enumerate() [
  #let label = family-pair.at(0)
  #let color = family-pair.at(2)
  #v(8mm)
  #title(
    [#label: 긴 혼합 문장 비교],
    note: [같은 한글·영어·숫자·단위 문단을 1:0부터 0:1까지 다섯 상태로 반복해 네 줄 이상의 글줄 폭과 본문 크기 인상을 비교합니다.],
  )
  #v(5mm)
  #text(size: 7pt, weight: 700, tracking: 0.08em, fill: color)[#label]
  #v(2.5mm)
  #for (ratio, slug, alpha) in comparison-ratios [
    #grid(
      columns: (15mm, 1fr),
      column-gutter: 3mm,
      [#eyebrow[#ratio]],
      [
        #text(font: comparison-font(label, ratio), size: 9.5pt)[#long-proof]
      ],
    )
    #v(5mm)
  ]
  #box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
    한글 받침의 baseline 위치와 English lowercase의 x-height·descender, 대문자 약어, 소수점,
    en dash, percent sign 및 단위 주변의 spacing을 한 문단 안에서 함께 확인합니다.
  ]
  #if index < families.len() - 1 [#pagebreak()]
]

#pagebreak()

// 11 — target and decision checklist
#v(8mm)
#title(
  [Appendard 기준과 최종 판단 항목],
  note: [후보 페이지와 동일한 혼합 문단을 수정하지 않은 Appendard로 조판했습니다.],
)
#v(5mm)
#eyebrow[APPENDARD TARGET / 9.5 PT]
#v(2mm)
#text(font: "SNU Appendard", size: 9.5pt)[#long-proof]
#v(8mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(4mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[SHORT NUMERIC CONTROL]
    #v(1.5mm)
    #text(font: "SNU Appendard", size: 9.5pt)[
      반복적 건조 처리는 재급수 뒤 기공 전도도의 회복 시간을 단축했다. 처리군 48개체의
      24 h 평균은 0.781 ± 0.014였다.
    ]
  ],
  [
    #eyebrow[DECISION CHECKLIST]
    #v(1.5mm)
    ① 하단 처짐이 충분히 완화됐는가?\
    ② 한글이 라틴에 비해 작아지지 않았는가?\
    ③ 원본의 descender 성격이 적당히 남았는가?\
    ④ 세 가족에 같은 ratio를 쓸지, 가족별로 고를지?
  ],
)

#v(7mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[NEXT DECISION]
  #v(1.2mm)
  Regular의 ratio를 승인한 뒤에만 선택된 alpha를 각 weight의 독립 full fit에 적용합니다.
  세 가족이 반드시 같은 ratio를 사용할 필요는 없습니다.
]
