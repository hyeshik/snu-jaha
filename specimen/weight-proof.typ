#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")

#set page(
  paper: "a4",
  margin: (left: 18mm, right: 18mm, top: 17mm, bottom: 17mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.8pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · WEIGHT RANGE CANDIDATE A
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.8mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.8pt, fill: gray)[RIDI +0/+8/+16/+24 · Roboto 400/466.7/533.3/600],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.4pt, lang: "ko", fill: ink)
#set par(justify: true, leading: 0.72em, first-line-indent: 1em)

#let eyebrow(body) = text(size: 7pt, weight: 700, tracking: 0.12em, fill: accent, body)

#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / STAGE 2]
  #v(4mm)
  #text(size: 25pt, weight: 700, body)
  #if note != none [
    #v(2mm)
    #text(size: 8.5pt, fill: gray, note)
  ]
  #v(5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let weight-row(label, weight, source, sample) = block(breakable: false)[
  #grid(
    columns: (27mm, 1fr),
    column-gutter: 7mm,
    [
      #eyebrow[#label]
      #v(1.2mm)
      #text(size: 7.2pt, fill: gray, source)
    ],
    [#text(size: 25pt, weight: weight, sample)],
  )
]

// Page 1 — the complete range
#align(center)[
  #eyebrow[FOUR-STYLE RANGE / CANDIDATE A]
  #v(8mm)
  #text(size: 34pt, weight: 700)[네 단계의 먹색]
  #v(3mm)
  #text(size: 15pt, weight: 400, fill: green)[A measured progression for research typography]
]

#v(9mm)
#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  column-gutter: 2.5mm,
  [#box(width: 100%, inset: 3.4mm, radius: 1.4mm, fill: wash)[
    #eyebrow[REGULAR 400]
    #v(1.6mm)
    #text(size: 10.5pt)[RIDI +0]
    #linebreak()
    #text(size: 7pt, fill: gray)[Roboto 400]
  ]],
  [#box(width: 100%, inset: 3.4mm, radius: 1.4mm, fill: wash)[
    #eyebrow[MEDIUM 500]
    #v(1.6mm)
    #text(size: 10.5pt, weight: 500)[RIDI +8]
    #linebreak()
    #text(size: 7pt, fill: gray)[Roboto 466.7]
  ]],
  [#box(width: 100%, inset: 3.4mm, radius: 1.4mm, fill: wash)[
    #eyebrow[SEMIBOLD 600]
    #v(1.6mm)
    #text(size: 10.5pt, weight: 600)[RIDI +16]
    #linebreak()
    #text(size: 7pt, fill: gray)[Roboto 533.3]
  ]],
  [#box(width: 100%, inset: 3.4mm, radius: 1.4mm, fill: wash)[
    #eyebrow[BOLD 700]
    #v(1.6mm)
    #text(size: 10.5pt, weight: 700)[RIDI +24]
    #linebreak()
    #text(size: 7pt, fill: gray)[Roboto 600]
  ]],
)

#v(8mm)
#weight-row([REGULAR 400], 400, [본문 · 기준], [자하연의 연구 기록  Recovery kinetics 24 h])
#v(4.5mm)
#weight-row([MEDIUM 500], 500, [도입 · 완만한 강조], [자하연의 연구 기록  Recovery kinetics 24 h])
#v(4.5mm)
#weight-row([SEMIBOLD 600], 600, [소제목 · 핵심 수치], [자하연의 연구 기록  Recovery kinetics 24 h])
#v(4.5mm)
#weight-row([BOLD 700], 700, [제목 · 강한 위계], [자하연의 연구 기록  Recovery kinetics 24 h])

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.6mm, stroke: 0.5pt + rule)[
  #eyebrow[TABULAR FIGURES / 560 UNITS THROUGHOUT]
  #v(2mm)
  #grid(
    columns: (auto, 1fr),
    column-gutter: 5mm,
    row-gutter: 1.8mm,
    [#text(size: 7pt, fill: gray)[400]], [#text(size: 12pt, weight: 400)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
    [#text(size: 7pt, fill: gray)[500]], [#text(size: 12pt, weight: 500)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
    [#text(size: 7pt, fill: gray)[600]], [#text(size: 12pt, weight: 600)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
    [#text(size: 7pt, fill: gray)[700]], [#text(size: 12pt, weight: 700)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
  )
]

#pagebreak()

// Page 2 — counters, sizes, and scripts
#title(
  [크기와 구조의 연속성],
  note: [복잡한 한글, 라틴 대소문자, tabular 숫자를 같은 조건에서 비교합니다.],
)

#v(6mm)
#grid(
  columns: (24mm, 1fr),
  row-gutter: 3.6mm,
  [#eyebrow[400]], [#text(size: 23pt, weight: 400)[흙 뿔 률 쫓 빛 뫼 람 활 괄]],
  [#eyebrow[500]], [#text(size: 23pt, weight: 500)[흙 뿔 률 쫓 빛 뫼 람 활 괄]],
  [#eyebrow[600]], [#text(size: 23pt, weight: 600)[흙 뿔 률 쫓 빛 뫼 람 활 괄]],
  [#eyebrow[700]], [#text(size: 23pt, weight: 700)[흙 뿔 률 쫓 빛 뫼 람 활 괄]],
)

#v(6mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[HANGUL / 11 PT]
    #v(2mm)
    #text(size: 11pt, weight: 400)[반복적 건조 스트레스와 회복 속도]
    #linebreak()
    #text(size: 11pt, weight: 500)[반복적 건조 스트레스와 회복 속도]
    #linebreak()
    #text(size: 11pt, weight: 600)[반복적 건조 스트레스와 회복 속도]
    #linebreak()
    #text(size: 11pt, weight: 700)[반복적 건조 스트레스와 회복 속도]
  ],
  [
    #eyebrow[LATIN / 11 PT]
    #v(2mm)
    #text(size: 11pt, weight: 400)[Minimum oxygen gradient 24 h]
    #linebreak()
    #text(size: 11pt, weight: 500)[Minimum oxygen gradient 24 h]
    #linebreak()
    #text(size: 11pt, weight: 600)[Minimum oxygen gradient 24 h]
    #linebreak()
    #text(size: 11pt, weight: 700)[Minimum oxygen gradient 24 h]
  ],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[SMALL-SIZE CHECK / 9 PT]
  #v(2mm)
  #grid(
    columns: (15mm, 1fr),
    row-gutter: 1.8mm,
    [#text(size: 7pt, fill: gray)[400]], [#text(size: 9pt, weight: 400)[흙과 뿔의 속공간 · recovery 17.2 µm · 2026-09-02]],
    [#text(size: 7pt, fill: gray)[500]], [#text(size: 9pt, weight: 500)[흙과 뿔의 속공간 · recovery 17.2 µm · 2026-09-02]],
    [#text(size: 7pt, fill: gray)[600]], [#text(size: 9pt, weight: 600)[흙과 뿔의 속공간 · recovery 17.2 µm · 2026-09-02]],
    [#text(size: 7pt, fill: gray)[700]], [#text(size: 9pt, weight: 700)[흙과 뿔의 속공간 · recovery 17.2 µm · 2026-09-02]],
  )
]

#v(7mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[CAPS / STEM COLOR]
    #v(2mm)
    #text(size: 17pt, weight: 400)[HAMBURGEFONTS]
    #linebreak()
    #text(size: 17pt, weight: 500)[HAMBURGEFONTS]
    #linebreak()
    #text(size: 17pt, weight: 600)[HAMBURGEFONTS]
    #linebreak()
    #text(size: 17pt, weight: 700)[HAMBURGEFONTS]
  ],
  [
    #eyebrow[FIGURES / REPEATED FORMS]
    #v(2mm)
    #text(size: 16pt, weight: 400)[001122334455]
    #linebreak()
    #text(size: 16pt, weight: 500)[001122334455]
    #linebreak()
    #text(size: 16pt, weight: 600)[001122334455]
    #linebreak()
    #text(size: 16pt, weight: 700)[001122334455]
  ],
)

#pagebreak()

// Page 3 — a proposed document hierarchy
#title(
  [학술 문서에서의 역할 분담],
  note: [400은 본문, 500은 도입과 완만한 강조, 600은 절 제목, 700은 문서 제목에 배치했습니다.],
)

#v(6mm)
#text(size: 21pt, weight: 700)[
  반복적 건조 경험이 기공 회복과 유전자 발현 시점에 미치는 영향
]
#v(2mm)
#text(size: 11.5pt, weight: 500, fill: green)[
  Repeated drought exposure shifts stomatal recovery and gene-expression timing
]
#v(3mm)
#text(size: 8pt, fill: gray)[김자하 · Minseo Park · 관악 식물환경연구실 · 2 September 2026]

#v(7mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #text(size: 14pt, weight: 600)[1. 서론]
    #v(2.8mm)
    #text(weight: 500)[수분 부족은 식물의 생장과 탄소 동화를 동시에 제한한다.] 잎의
    water potential이 감소하면 guard cell의 turgor가 변하고 stomatal
    conductance가 낮아진다. 본 연구는 repeated mild drought가 회복 곡선의 시간
    상수를 바꾸는지 검정했다.

    #v(3mm)
    핵심 가설은 반복 처리군의 초기 회복 속도가 더 빠르다는 것이다. 이를 위해
    48개체를 control, single-stress, repeated-stress 집단으로 나누고 0, 2, 8,
    24, 48, 72 h에 생리 지표와 RNA abundance를 측정했다.

    #v(5mm)
    #text(size: 14pt, weight: 600)[2. 주요 결과]
    #v(2.8mm)
    재급수 8 h 뒤 Fv/Fm은 repeated-stress에서 #text(weight: 500)[0.781 ± 0.014],
    single-stress에서 0.742 ± 0.021이었다. 차이는 유의했으며
    #text(weight: 600)[_p_ = 0.0006]이었다.
  ],
  [
    #box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
      #eyebrow[KEY FINDING / 600]
      #v(2mm)
      #text(size: 15pt, weight: 600)[회복 시간 6.3 h]
      #v(1.5mm)
      #text(size: 8.5pt)[single-stress 10.8 h보다 4.5 h 짧았다.]
    ]

    #v(6mm)
    #text(size: 12pt, weight: 600)[RESULTS AT A GLANCE]
    #v(2mm)
    #grid(
      columns: (1fr, auto),
      row-gutter: 2.2mm,
      [Plants], [#text(weight: 500)[48]],
      [RNA-seq reads], [#text(weight: 500)[4.8 × 10⁶]],
      [Differential genes], [#text(weight: 500)[612]],
      [False discovery rate], [#text(weight: 500)[< 0.05]],
    )

    #v(6mm)
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(4mm)
    #text(size: 12pt, weight: 600)[3. 결론]
    #v(2.5mm)
    반복적인 약한 건조 경험은 최대 손상량보다 #text(weight: 500)[회복의 속도와 순서]를
    바꾸었다. 네 weight는 강한 표시보다 문서의 세밀한 위계를 만드는 데 우선 사용한다.
  ],
)

#v(8mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (25mm, 1fr),
  row-gutter: 2.2mm,
  [#eyebrow[400]], [#text(size: 11pt, weight: 400)[본문과 긴 문장 · measured recovery 24 h · 31.2%]],
  [#eyebrow[500]], [#text(size: 11pt, weight: 500)[도입과 완만한 강조 · measured recovery 24 h · 31.2%]],
  [#eyebrow[600]], [#text(size: 11pt, weight: 600)[절 제목과 핵심 결과 · measured recovery 24 h · 31.2%]],
  [#eyebrow[700]], [#text(size: 11pt, weight: 700)[문서 제목과 강한 위계 · measured recovery 24 h · 31.2%]],
)
