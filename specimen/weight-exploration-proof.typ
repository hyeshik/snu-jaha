#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let coral = rgb("#A64B3C")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let audit = json("../build/weight-exploration/audit.json")

#set page(
  paper: "a4",
  margin: (left: 17mm, right: 17mm, top: 16mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.6pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · REGULAR-ANCHORED WEIGHT STUDY
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.6mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.6pt, fill: gray)[REPRESENTATIVE MICROFONTS · NOT RELEASE FONTS],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.72em)

#let styles = ("Thin", "Light", "Medium", "SemiBold", "Bold", "ExtraBold")
#let eyebrow(body) = text(size: 6.8pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let ratio(value) = str(calc.round(value * 1000) / 1000)
#let count(item, key) = str(item.at(key).len())
#let cjk(label) = audit.at("cjk").find(item => item.at("label") == label)
#let latin(label) = audit.at("latin").find(item => item.at("label") == label)
#let best(style) = audit.at("recommendations").at(style).at(0)
#let pair-font(pair) = (pair.at("cjk_family"), pair.at("latin_family"))
#let mixed-pair(pair, size: 18pt, body) = text(font: pair-font(pair), size: size, body)
#let mixed-best(style, size: 18pt, body) = mixed-pair(best(style), size: size, body)
#let status(item) = if item.at("numeric_pass") [
  #text(fill: green, weight: 700)[TARGET]
] else [
  #text(fill: coral, weight: 700)[OUT]
]
#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / OPTICAL RANGE EXPANSION]
  #v(3.5mm)
  #text(size: 24pt, weight: 700, body)
  #if note != none [
    #v(1.8mm)
    #text(size: 8.2pt, fill: gray, note)
  ]
  #v(4.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]
#let candidate-row(item) = (
  [#eyebrow[#item.at("label")]],
  [#text(size: 8pt)[#ratio(item.at("raster_coverage_ratio"))]],
  [#text(size: 8pt)[#ratio(item.at("median_area_ratio"))]],
  [#text(size: 8pt)[#count(item, "foreground_splits") / #count(item, "foreground_merges") / #count(item, "counter_losses")]],
  [#text(size: 8pt)[#status(item)]],
)

// Page 1 — targets and numeric leaders
#align(center)[
  #eyebrow[STAGE 1 / 48 CJK + 27 LATIN MICROFONTS]
  #v(7mm)
  #text(size: 31pt, weight: 700)[Regular는 두고, 양끝을 벌리기]
  #v(2.5mm)
  #text(size: 13.5pt, fill: green)[Six optical roles around one fixed reading weight]
]

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 6mm,
    [#eyebrow[ANCHOR] #v(1.5mm) #text(size: 11pt, weight: 700)[Regular 1.000]],
    [#eyebrow[LOWER TARGETS] #v(1.5mm) #text(size: 11pt, weight: 700)[0.58 · 0.82]],
    [#eyebrow[UPPER TARGETS] #v(1.5mm) #text(size: 11pt, weight: 700)[1.19 · 1.35 · 1.50]],
  )
]

#v(7mm)
#eyebrow[REVIEWED PRODUCTION PAIRS / 128 PPEM RASTER COVERAGE]
#v(2mm)
#table(
  columns: (22mm, 38mm, 19mm, 38mm, 19mm, 18mm),
  inset: (x: 1.2mm, y: 1.8mm),
  stroke: 0.35pt + rule,
  align: (left, left, right, left, right, right),
  table.header(
    [#eyebrow[ROLE]],
    [#eyebrow[CJK]],
    [#eyebrow[RATIO]],
    [#eyebrow[LATIN]],
    [#eyebrow[RATIO]],
    [#eyebrow[Δ]],
  ),
  ..styles.map(style => {
    let pair = best(style)
    (
      [#text(weight: 700)[#style]],
      [#pair.at("cjk")],
      [#ratio(pair.at("cjk_ratio"))],
      [#pair.at("latin")],
      [#ratio(pair.at("latin_ratio"))],
      [#ratio(pair.at("script_difference"))],
    )
  }).flatten(),
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[READING]
  #v(2mm)
  #text(size: 8.7pt)[
    TARGET은 수치 후보라는 뜻이며 구조 승인과 같지 않습니다. 마지막 열의 Δ는 한글과
    Latin의 Regular 대비 회색도 차이입니다. 아래 페이지에서 가는 획 분리, 굵은 획 접합,
    counter 손실을 크기별로 확인합니다.
  ]
]

#pagebreak()

// Page 2 — lower range
#title(
  [Thin과 Light: 실제로 가벼워지는 지점],
  note: [Thin은 18 pt 이상 display, Light는 10–11 pt 보조 본문을 기준으로 봅니다. 수치는 raster coverage / Regular입니다.],
)

#v(4mm)
#eyebrow[THIN / AUTO OFFSET LADDER]
#v(2mm)
#for label in ("Thin −26 auto", "Thin −28 auto", "Thin −30 auto", "Thin −32 auto") [
  #let item = cjk(label)
  #grid(
    columns: (28mm, 1fr, 24mm),
    row-gutter: 1mm,
    [#eyebrow[#label]],
    [#text(font: item.at("family"), size: 19pt)[느 스 기 가 · 흙 뿳 휇 률]],
    [#text(size: 7.5pt)[#ratio(item.at("raster_coverage_ratio")) · #status(item)]],
  )
  #v(2.2mm)
]

#v(3mm)
#eyebrow[THIN / AUTO VS RETAIN]
#v(2mm)
#grid(
  columns: (26mm, 1fr, 1fr),
  column-gutter: 5mm,
  row-gutter: 3mm,
  [#eyebrow[OFFSET]], [#eyebrow[AUTO]], [#eyebrow[RETAIN]],
  ..("28", "30", "32").map(offset => (
    [#eyebrow[−#offset]],
    [#text(font: cjk("Thin −" + offset + " auto").at("family"), size: 22pt)[뿳 휇 흙 뿔 률]],
    [#text(font: cjk("Thin −" + offset + " retain").at("family"), size: 22pt)[뿳 휇 흙 뿔 률]],
  )).flatten(),
)

#v(7mm)
#eyebrow[LIGHT / AUTO OFFSET LADDER]
#v(2mm)
#for label in ("Light −10 auto", "Light −12 auto", "Light −14 auto", "Light −16 auto") [
  #let item = cjk(label)
  #grid(
    columns: (28mm, 1fr, 24mm),
    [#eyebrow[#label]],
    [#text(font: item.at("family"), size: 16pt)[반복적 건조 스트레스와 회복 속도]],
    [#text(size: 7.5pt)[#ratio(item.at("raster_coverage_ratio")) · #status(item)]],
  )
  #v(2mm)
]

#pagebreak()

// Page 3 — upper range
#title(
  [Medium·SemiBold·Bold: 위계가 생기는 간격],
  note: [Medium과 SemiBold를 충분히 벌리고, Bold 후보는 104% Hangul advance를 microfont 단계부터 반영했습니다.],
)

#v(4mm)
#for (style, labels) in (
  ("MEDIUM", ("Medium +10 auto", "Medium +12 auto", "Medium +14 auto", "Medium +16 auto")),
  ("SEMIBOLD", ("SemiBold +20 auto", "SemiBold +22 auto", "SemiBold +24 auto", "SemiBold +26 auto")),
) [
  #eyebrow[#style]
  #v(1.8mm)
  #for label in labels [
    #let item = cjk(label)
    #grid(
      columns: (32mm, 1fr, 25mm),
      [#eyebrow[#label]],
      [#text(font: item.at("family"), size: 17pt)[자하연 연구 기록 · 흙 뿔 률]],
      [#text(size: 7.5pt)[#ratio(item.at("raster_coverage_ratio")) · #status(item)]],
    )
    #v(1.8mm)
  ]
  #v(4mm)
]

#line(length: 100%, stroke: 0.45pt + rule)
#v(4mm)
#eyebrow[BOLD / AUTO VS RETAIN]
#v(2mm)
#grid(
  columns: (20mm, 1fr, 1fr, 21mm),
  column-gutter: 4mm,
  row-gutter: 3.2mm,
  [#eyebrow[OFFSET]], [#eyebrow[AUTO]], [#eyebrow[RETAIN]], [#eyebrow[RATIO A/R]],
  ..("28", "30", "32", "34").map(offset => {
    let automatic = cjk("Bold +" + offset + " auto")
    let retain = cjk("Bold +" + offset + " retain")
    (
      [#eyebrow[+#offset]],
      [#text(font: automatic.at("family"), size: 20pt)[뺨 뺌 뺄 뽑 뼒 뼮]],
      [#text(font: retain.at("family"), size: 20pt)[뺨 뺌 뺄 뽑 뼒 뼮]],
      [#text(size: 7.2pt)[#ratio(automatic.at("raster_coverage_ratio")) / #ratio(retain.at("raster_coverage_ratio"))]],
    )
  }).flatten(),
)

#pagebreak()

// Page 4 — ExtraBold exploration
#title(
  [ExtraBold: Bold 위의 display 후보],
  note: [선택된 Bold +28 retain을 구조 비교 기준으로 삼습니다. 104/108은 Hangul advance 비율입니다.],
)

#v(3mm)
#grid(
  columns: (18mm, 1fr, 1fr, 1fr, 1fr),
  column-gutter: 3mm,
  [#eyebrow[OFFSET]],
  [#eyebrow[AUTO 104]],
  [#eyebrow[AUTO 108]],
  [#eyebrow[RETAIN 104]],
  [#eyebrow[RETAIN 108]],
)
#v(2mm)
#for offset in ("36", "38", "40", "42", "44") [
  #grid(
    columns: (18mm, 1fr, 1fr, 1fr, 1fr),
    column-gutter: 3mm,
    [#eyebrow[+#offset]],
    ..(("auto", "104"), ("auto", "108"), ("retain", "104"), ("retain", "108")).map(pair => {
      let item = cjk("ExtraBold +" + offset + " " + pair.at(0) + " " + pair.at(1) + "%")
      [
        #text(font: item.at("family"), size: 14pt)[뼒 뼮 뿔 흙]
        #linebreak()
        #text(size: 6.8pt, fill: gray)[#ratio(item.at("raster_coverage_ratio")) · gap #ratio(item.at("hangul_pair_spacing").at("minimum")) · #status(item)]
      ]
    }),
  )
  #v(3mm)
]

#v(4mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(4mm)
#eyebrow[LATIN SOURCE LADDER]
#v(2mm)
#grid(
  columns: (25mm, 1fr, 22mm),
  row-gutter: 2mm,
  ..audit.at("latin").filter(item => item.at("style") == "ExtraBold").map(item => (
    [#eyebrow[W#str(item.at("weight"))]],
    [#text(font: item.at("family"), size: 15pt)[A Á À Â Ä Å · HAMBURGEFONTS]],
    [#text(size: 7.5pt)[#ratio(item.at("raster_coverage_ratio"))]],
  )).flatten(),
)

#pagebreak()

// Page 5 — selected mixed-script ladder
#title(
  [선택한 production 조합의 실제 계단],
  note: [Regular는 현재 production font 그대로이고 나머지 여섯 단계는 proof 검토 후 선택한 조합입니다.],
)

#v(5mm)
#grid(
  columns: (25mm, 1fr),
  row-gutter: 4.2mm,
  [#eyebrow[THIN]], [#mixed-best("Thin", size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
  [#eyebrow[LIGHT]], [#mixed-best("Light", size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
  [#eyebrow[REGULAR]], [#text(size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
  [#eyebrow[MEDIUM]], [#mixed-best("Medium", size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
  [#eyebrow[SEMIBOLD]], [#mixed-best("SemiBold", size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
  [#eyebrow[BOLD]], [#mixed-best("Bold", size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
  [#eyebrow[EXTRABOLD]], [#mixed-best("ExtraBold", size: 19pt)[자하연 Research 24 h · 흙 뿔 률]],
)

#v(8mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(5mm)
#eyebrow[ROLE SIZES]
#v(2mm)
#grid(
  columns: (21mm, 1fr),
  row-gutter: 3.2mm,
  [#text(size: 7pt, fill: gray)[LIGHT 10 PT]], [#mixed-best("Light", size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum oxygen 17.2 µm]],
  [#text(size: 7pt, fill: gray)[REGULAR 10 PT]], [#text(size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum oxygen 17.2 µm]],
  [#text(size: 7pt, fill: gray)[MEDIUM 10 PT]], [#mixed-best("Medium", size: 10pt)[반복적 건조 스트레스와 회복 속도 · minimum oxygen 17.2 µm]],
  [#text(size: 7pt, fill: gray)[SEMIBOLD 12 PT]], [#mixed-best("SemiBold", size: 12pt)[기공 회복과 유전자 발현 시점 · Research result]],
  [#text(size: 7pt, fill: gray)[BOLD 14 PT]], [#mixed-best("Bold", size: 14pt)[기공 회복과 유전자 발현 시점 · Research result]],
  [#text(size: 7pt, fill: gray)[EXTRABOLD 18 PT]], [#mixed-best("ExtraBold", size: 18pt)[자하연 연구 기록 · Research result]],
  [#text(size: 7pt, fill: gray)[THIN 24 PT]], [#mixed-best("Thin", size: 24pt)[자하연 연구 기록]],
)

#pagebreak()

// Page 6 — Latin source ladders
#title(
  [Roboto Serif source coordinates],
  note: [모든 후보는 opsz 14, wdth 91과 현재 Jaha Latin geometry를 사용하며 Thin은 GRAD 후보도 비교합니다.],
)

#v(4mm)
#for style in styles [
  #let items = audit.at("latin").filter(item => item.at("style") == style)
  #eyebrow[#style]
  #v(1.6mm)
  #grid(
    columns: (30mm, 1fr, 22mm),
    row-gutter: 1.8mm,
    ..items.map(item => (
      [#eyebrow[W#str(item.at("weight"))#if item.at("grade") != 0 [ · G#str(item.at("grade"))]]],
      [#text(font: item.at("family"), size: 15pt)[HAMBURGEFONTS minimum oxygen]],
      [#text(size: 7.5pt)[#ratio(item.at("raster_coverage_ratio"))]],
    )).flatten(),
  )
  #v(5mm)
]

#pagebreak()

// Page 7 — structural flags and figures
#title(
  [구조 기록과 숫자 간격],
  note: [S/M/C는 64 ppem foreground split, merge, counter loss 기록 수입니다. Thin–Bold는 Regular, ExtraBold는 선택 Bold가 비교 기준입니다.],
)

#v(4mm)
#eyebrow[SELECTED CJK STRUCTURE]
#v(2mm)
#table(
  columns: (25mm, 42mm, 22mm, 22mm, 22mm, 22mm),
  inset: (x: 1.5mm, y: 1.7mm),
  stroke: 0.35pt + rule,
  table.header(
    [#eyebrow[ROLE]], [#eyebrow[CJK]], [#eyebrow[RATIO]],
    [#eyebrow[S]], [#eyebrow[M]], [#eyebrow[C]],
  ),
  ..styles.map(style => {
    let item = cjk(best(style).at("cjk"))
    (
      [#text(weight: 700)[#style]],
      [#item.at("label")],
      [#ratio(item.at("raster_coverage_ratio"))],
      [#str(item.at("foreground_splits").filter(record => record.at("ppem") == 64).len())],
      [#str(item.at("foreground_merges").filter(record => record.at("ppem") == 64).len())],
      [#str(item.at("counter_losses").filter(record => record.at("ppem") == 64).len())],
    )
  }).flatten(),
)

#v(8mm)
#eyebrow[TABULAR FIGURES / FINAL 520-UNIT CELL]
#v(2mm)
#grid(
  columns: (28mm, 1fr, 23mm),
  row-gutter: 3mm,
  [#eyebrow[REGULAR]], [#text(size: 17pt)[00 · 100 · 200 · 700 · 1000]], [#text(size: 7.5pt)[CONTROL]],
  ..styles.map(style => {
    let item = cjk(best(style).at("cjk"))
    (
      [#eyebrow[#style]],
      [#text(font: item.at("family"), size: 17pt)[00 · 100 · 200 · 700 · 1000]],
      [#text(size: 7.5pt)[gap #ratio(item.at("zero_gap"))]],
    )
  }).flatten(),
)

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[PRODUCTION GATE]
  #v(2mm)
  #text(size: 8.7pt)[
    선택한 ExtraBold는 full-font audit에서 전체 cmap, Bold 대비 raster 순서,
    64 ppem counter, specimen 문장 쌍의 양수 간격을 다시 확인합니다.
  ]
]
