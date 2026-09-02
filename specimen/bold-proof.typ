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
      SNU JAHA · BOLD CANDIDATE A
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.8mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.8pt, fill: gray)[RIDIBatang +24 · Roboto Serif 14pt SemiBold 600],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.4pt, lang: "ko", fill: ink)
#set par(justify: true, leading: 0.7em, first-line-indent: 1em)

#let eyebrow(body) = text(size: 7pt, weight: 700, tracking: 0.12em, fill: accent, body)

#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / STAGE 1]
  #v(4mm)
  #text(size: 25pt, weight: 700, body)
  #if note != none [
    #v(2mm)
    #text(size: 8.5pt, fill: gray, note)
  ]
  #v(5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let comparison(label, weight, sample, note) = block(breakable: false)[
  #grid(
    columns: (29mm, 1fr),
    column-gutter: 7mm,
    [
      #eyebrow[#label]
      #v(1.2mm)
      #text(size: 7.2pt, fill: gray, note)
    ],
    [#text(size: 28pt, weight: weight, sample)],
  )
]

// Page 1 — role and first impression
#align(center)[
  #eyebrow[BOLD CANDIDATE A / STATIC OTF]
  #v(8mm)
  #text(size: 34pt, weight: 700)[굵기의 첫 번째 제안]
  #v(3mm)
  #text(size: 15pt, weight: 400, fill: green)[A conservative bold for research hierarchy]
]

#v(9mm)
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 3mm,
  [#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
    #eyebrow[CJK SOURCE]
    #v(2mm)
    #text(size: 12pt, weight: 700)[RIDIBatang +24]
    #v(1mm)
    #text(size: 7.5pt, fill: gray)[advance 유지 · 보수적 합성 증량]
  ]],
  [#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
    #eyebrow[LATIN SOURCE]
    #v(2mm)
    #text(size: 12pt, weight: 700)[Roboto Serif 600]
    #v(1mm)
    #text(size: 7.5pt, fill: gray)[14pt optical size · SemiBold]
  ]],
  [#box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
    #eyebrow[OUTPUT ROLE]
    #v(2mm)
    #text(size: 12pt, weight: 700)[Bold / 700]
    #v(1mm)
    #text(size: 7.5pt, fill: gray)[제목 · 소제목 · 제한적 강조]
  ]],
)

#v(9mm)
#comparison(
  "REGULAR 400",
  400,
  [자하연의 연구 기록  Recovery kinetics 24 h],
  [현재 기준],
)
#v(6mm)
#comparison(
  "BOLD 700",
  700,
  [자하연의 연구 기록  Recovery kinetics 24 h],
  [후보 A],
)

#v(9mm)
#box(width: 100%, inset: 6mm, radius: 1.8mm, fill: wash)[
  #text(size: 17pt, weight: 700)[
    반복적 건조 스트레스가 식물의 회복 속도에 미치는 영향
  ]
  #v(2mm)
  #text(size: 10.5pt, weight: 400)[
    Repeated drought exposure alters recovery kinetics and transcriptomic response.
  ]
]

#pagebreak()

// Page 2 — outline and counter stress tests
#title(
  [획과 속공간의 스트레스 테스트],
  note: [같은 글자를 Regular와 Bold로 반복해 세리프 팽창, 속공간 폐쇄, 라틴과 숫자의 먹색을 비교합니다.],
)

#v(7mm)
#grid(
  columns: (25mm, 1fr),
  row-gutter: 5mm,
  [#eyebrow[REGULAR]], [#text(size: 24pt, weight: 400)[가나다라마바사 아자차카타파하]],
  [#eyebrow[BOLD]], [#text(size: 24pt, weight: 700)[가나다라마바사 아자차카타파하]],
  [#eyebrow[REGULAR]], [#text(size: 26pt, weight: 400)[흙 뿔 률 쫓 빛 뫼 람 활 괄]],
  [#eyebrow[BOLD]], [#text(size: 26pt, weight: 700)[흙 뿔 률 쫓 빛 뫼 람 활 괄]],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(6mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 10mm,
  [
    #eyebrow[LATIN / REGULAR]
    #v(2mm)
    #text(size: 21pt, weight: 400)[HAMBURGEFONTS]
    #text(size: 18pt, weight: 400)[minimum oxygen gradient]
    #v(4mm)
    #eyebrow[LATIN / BOLD]
    #v(2mm)
    #text(size: 21pt, weight: 700)[HAMBURGEFONTS]
    #text(size: 18pt, weight: 700)[minimum oxygen gradient]
  ],
  [
    #eyebrow[FIGURES / REGULAR]
    #v(2mm)
    #text(size: 22pt, weight: 400)[0123456789]
    #linebreak()
    #text(size: 14pt, weight: 400)[31.2% · 4.8 × 10⁶ · −2.7°C]
    #linebreak()
    #text(size: 12pt, weight: 400)[00 · 100 · 200 · 700 · 1000]
    #v(4mm)
    #eyebrow[FIGURES / BOLD]
    #v(2mm)
    #text(size: 22pt, weight: 700)[0123456789]
    #linebreak()
    #text(size: 14pt, weight: 700)[31.2% · 4.8 × 10⁶ · −2.7°C]
    #linebreak()
    #text(size: 12pt, weight: 700)[00 · 100 · 200 · 700 · 1000]
  ],
)

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[SMALL-SIZE COUNTER CHECK]
  #v(2.5mm)
  #grid(
    columns: (18mm, 1fr),
    row-gutter: 2mm,
    [#text(size: 7pt, fill: gray)[9 PT]], [#text(size: 9pt, weight: 700)[흙과 뿔의 복잡한 속공간 · minimum 17.2 µm · 2026-09-02]],
    [#text(size: 7pt, fill: gray)[11 PT]], [#text(size: 11pt, weight: 700)[흙과 뿔의 복잡한 속공간 · minimum 17.2 µm · 2026-09-02]],
    [#text(size: 7pt, fill: gray)[14 PT]], [#text(size: 14pt, weight: 700)[흙과 뿔의 복잡한 속공간 · minimum 17.2 µm]],
  )
]

#pagebreak()

// Page 3 — hierarchy in an academic page
#title(
  [학술 문서의 위계와 강조],
  note: [Bold는 본문 전체가 아니라 제목, 절 제목, 핵심 결과처럼 제한된 위치에서 사용합니다.],
)

#v(6mm)
#text(size: 20pt, weight: 700)[
  반복적 건조 경험이 기공 회복과 유전자 발현 시점에 미치는 영향
]
#v(2mm)
#text(size: 11pt, weight: 400, fill: green)[
  Repeated drought exposure shifts stomatal recovery and gene-expression timing
]
#v(3mm)
#text(size: 8pt, fill: gray)[김자하 · Minseo Park · 관악 식물환경연구실 · 2 September 2026]

#v(7mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #text(size: 14pt, weight: 700)[1. 서론]
    #v(2.8mm)
    수분 부족은 식물의 생장과 탄소 동화를 동시에 제한한다. 잎의 water potential이
    감소하면 guard cell의 turgor가 변하고 stomatal conductance가 낮아진다. 본
    연구는 repeated mild drought가 회복 곡선의 시간 상수를 바꾸는지 검정했다.

    #v(3mm)
    #text(weight: 700)[핵심 가설은 반복 처리군의 초기 회복 속도가 더 빠르다는 것이다.]
    이를 위해 48개체를 control, single-stress, repeated-stress 집단으로 나누고
    0, 2, 8, 24, 48, 72 h에 생리 지표와 RNA abundance를 측정했다.

    #v(5mm)
    #text(size: 14pt, weight: 700)[2. 주요 결과]
    #v(2.8mm)
    재급수 8 h 뒤 Fv/Fm은 repeated-stress에서 #text(weight: 700)[0.781 ± 0.014],
    single-stress에서 0.742 ± 0.021이었다. 차이는 유의했으며
    #text(weight: 700)[_p_ = 0.0006]이었다.
  ],
  [
    #box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
      #eyebrow[KEY FINDING]
      #v(2mm)
      #text(size: 15pt, weight: 700)[회복 시간 6.3 h]
      #v(1.5mm)
      #text(size: 8.5pt)[single-stress 10.8 h보다 4.5 h 짧았다.]
    ]

    #v(6mm)
    #text(size: 12pt, weight: 700)[RESULTS AT A GLANCE]
    #v(2mm)
    #grid(
      columns: (1fr, auto),
      row-gutter: 2.2mm,
      [Plants], [#text(weight: 700)[48]],
      [RNA-seq reads], [#text(weight: 700)[4.8 × 10⁶]],
      [Differential genes], [#text(weight: 700)[612]],
      [False discovery rate], [#text(weight: 700)[< 0.05]],
    )

    #v(6mm)
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(4mm)
    #text(size: 12pt, weight: 700)[3. 결론]
    #v(2.5mm)
    반복적인 약한 건조 경험은 최대 손상량보다 #text(weight: 700)[회복의 속도와 순서]를
    바꾸었다. Bold 후보는 이처럼 짧은 제목과 핵심 수치를 강조하면서 Regular 본문의
    흐름을 방해하지 않아야 한다.
  ],
)

#v(8mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (28mm, 1fr),
  row-gutter: 3mm,
  [#eyebrow[REGULAR]], [#text(size: 13pt, weight: 400)[자하연에서 읽는 measured recovery 24 h · 31.2%]],
  [#eyebrow[BOLD]], [#text(size: 13pt, weight: 700)[자하연에서 읽는 measured recovery 24 h · 31.2%]],
)
