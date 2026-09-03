#let ink = rgb("#17243B")
#let snu = rgb("#0F4C81")
#let pond = rgb("#277A73")
#let mist = rgb("#E8F1F0")
#let lilac = rgb("#EEEAF5")
#let gray = rgb("#667085")
#let pale = rgb("#D9E1E8")
#let paper = rgb("#FBFAF6")

#set page(
  paper: "a4",
  flipped: true,
  margin: (x: 18mm, y: 14mm),
  fill: paper,
  footer: context align(right)[
    #text(size: 7.5pt, fill: gray)[SNU JAHA REGULAR 0.1.0  ·  #counter(page).display("01")]
  ],
)
#set text(font: "SNU Jaha", lang: "ko", fill: ink)
#set par(leading: 0.62em, justify: true)

#let eyebrow(body) = text(size: 7.5pt, weight: 700, tracking: 0.16em, fill: snu, body)
#let title(body, note: none) = block(breakable: false)[
  #eyebrow[TYPE SPECIMEN / SNU JAHA]
  #v(2mm)
  #text(size: 26pt, body)
  #if note != none {
    v(1.5mm)
    text(size: 9pt, fill: gray, note)
  }
  #v(3.5mm)
  #line(length: 100%, stroke: 0.6pt + pale)
  #v(4.5mm)
]

#let chip(label, value) = box(
  inset: (x: 4mm, y: 2.4mm),
  radius: 1.5mm,
  fill: mist,
  [#text(size: 7pt, weight: 700, fill: pond)[#label] #h(2mm) #text(size: 9pt)[#value]],
)

// Cover
#v(7mm)
#eyebrow[SEOUL NATIONAL UNIVERSITY / TYPE FAMILY]
#v(14mm)
#text(size: 64pt, tracking: -0.035em)[SNU Jaha]
#v(1mm)
#text(size: 30pt, fill: pond)[자하연의 잔잔한 흐름을 글자에 담다]
#v(10mm)
#line(length: 76mm, stroke: 2pt + pond)
#v(11mm)
#grid(
  columns: (1.1fr, 0.9fr),
  column-gutter: 22mm,
  [
    #text(size: 19pt)[
      리디바탕의 또렷한 한글과
      Roboto Serif의 단단한 라틴
    ]
    #v(5mm)
    #text(size: 10pt, fill: gray)[
      장문 독서와 연구 문서를 위한 한글·라틴 세리프 조합입니다.
      일곱 굵기와 native italic을 갖춘 14개 정적 스타일로 완성했습니다.
    ]
  ],
  [
    #chip("KOREAN", "RIDIBatang")
    #v(2.5mm)
    #chip("LATIN", "Roboto Serif 14pt")
    #v(2.5mm)
    #chip("BUILD", "OpenType/CFF · 7 weights × 2 postures")
  ],
)

#pagebreak()

// Reading texture
#title([긴 문장에서 드러나는 호흡], note: [화면용 바탕체의 선명함과 본문용 라틴 세리프의 리듬을 한 문단에서 확인합니다.])
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 10mm,
  [
    #eyebrow[8.5 PT / COMPACT]
    #v(2mm)
    #text(size: 8.5pt)[
      자하연은 관악산의 계곡물이 머무는 작은 연못이다. 물가의 나무와 돌,
      계절마다 달라지는 빛은 캠퍼스 한가운데 느린 시간을 만든다. 연구자는
      관찰한 현상을 기록하고, 가설을 세우며, 데이터와 문장을 오가면서 생각을
      다듬는다. A clear typeface should support that process without calling
      attention to itself.
    ]
  ],
  [
    #eyebrow[10.5 PT / READING]
    #v(2mm)
    #text(size: 10.5pt)[
      좋은 본문 글꼴은 한글과 Latin alphabet 가운데 어느 한쪽만 도드라지지
      않게 한다. 단어의 형태는 또렷해야 하지만 문장 전체의 흐름은 부드러워야
      한다. SNU Jaha는 논문 초고, 연구노트, 강의자료처럼 한국어 문장 사이에
      English terms와 숫자가 자주 등장하는 문서를 위해 만들어졌다.
    ]
  ],
  [
    #eyebrow[13 PT / OPEN]
    #v(2mm)
    #text(size: 13pt)[
      서로 다른 글자가
      같은 물결을 이루도록

      Read slowly,
      think deeply.
    ]
  ],
)
#v(9mm)
#box(width: 100%, inset: 6mm, radius: 2mm, fill: lilac)[
  #text(size: 16pt)[
    “관찰은 질문을 만들고, 질문은 새로운 관찰을 부른다.”
    #h(5mm) The quick brown fox jumps over 13 lazy dogs.
  ]
]

#pagebreak()

// Character and features
#title([문자와 숫자의 표정], note: [RIDIBatang의 기본 숫자와 Roboto Serif의 라틴·키릴 문자·OpenType 대체 기능을 함께 확인합니다.])
#grid(
  columns: (33mm, 1fr),
  row-gutter: 4mm,
  [#eyebrow[HANGUL]], [#text(size: 21pt)[가나다라마바사 아자차카타파하 한글 자하연]],
  [#eyebrow[LATIN]], [#text(size: 21pt)[ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz]],
  [#eyebrow[NUMBERS]], [#text(size: 21pt)[0123456789  2026.09.02  ₩1,234,567  37.5%]],
  [#eyebrow[CYRILLIC]], [#text(size: 19pt)[АБВГДЕЖЗИЙ  абвгдежзий]],
  [#eyebrow[SYMBOLS]], [#text(size: 19pt)[← ↑ → ↓  ± × ÷ ≠ ≤ ≥ ∞  © ® ™  ( ) [ ] { }]],
)
#v(8mm)
#line(length: 100%, stroke: 0.6pt + pale)
#v(6mm)
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 10mm,
  [
    #eyebrow[DEFAULT / TABULAR]
    #v(2mm)
    #text(size: 20pt)[0123456789]
    #v(1mm)
    #text(size: 9pt, fill: gray)[RIDIBatang 윤곽 · 520-unit tabular lining figures]
  ],
  [
    #eyebrow[OLDSTYLE / ONUM]
    #v(2mm)
    #text(size: 20pt, features: ("onum",))[0123456789]
    #v(1mm)
    #text(size: 9pt, fill: gray)[명시적으로 선택하는 Roboto Serif 대체 숫자]
  ],
  [
    #eyebrow[LIGATURE / FRACTION]
    #v(2mm)
    #text(size: 20pt)[office efficient]
    #h(3mm)
    #text(size: 20pt, features: ("frac",))[1/2  3/4]
    #v(1mm)
    #text(size: 9pt, fill: gray)[liga · frac · kern · mark 기능 계승]
  ],
)
#v(2.5mm)
#grid(
  columns: (31mm, 1fr),
  row-gutter: 1.2mm,
  [#eyebrow[HYPHEN + FIGURE]], [#text(size: 14pt)[-0 -1 -2 -3 -4 -5 -6 -7 -8 -9]],
  [#eyebrow[EN DASH + FIGURE]], [#text(size: 14pt)[–0 –1 –2 –3 –4 –5 –6 –7 –8 –9]],
  [#eyebrow[EM DASH + FIGURE]], [#text(size: 14pt)[—0 —1 —2 —3 —4 —5 —6 —7 —8 —9]],
  [#eyebrow[MINUS + FIGURE]], [#text(size: 14pt)[−0 −1 −2 −3 −4 −5 −6 −7 −8 −9]],
)

#pagebreak()

// Source comparison
#title([세 원본을 정확히 구분한 비교], note: [각 행은 지정한 서로 다른 family name으로 렌더링합니다. 한글·기본 숫자와 라틴의 출처를 눈으로 확인합니다.])

#let row(label, font-name, sample, note) = block(breakable: false)[
  #grid(
    columns: (38mm, 1fr),
    column-gutter: 8mm,
    [
      #eyebrow[#label]
      #v(1.5mm)
      #text(size: 7.5pt, fill: gray)[#font-name]
    ],
    [
      #text(font: font-name, size: 22pt, sample)
      #v(1.2mm)
      #text(size: 8pt, fill: gray, note)
    ],
  )
  #v(2.5mm)
  #line(length: 100%, stroke: 0.5pt + pale)
  #v(2.5mm)
]

#row(
  "SNU JAHA",
  "SNU Jaha",
  [자하연에서 읽는 Hamburgefonts 0123456789],
  [합성 결과 · RIDIBatang 한글·기본 숫자 + 축소·정렬한 Roboto Serif 14pt Latin],
)
#row(
  "RIDI SOURCE",
  "RIDIBatang",
  [자하연에서 읽는 Hamburgefonts 0123456789],
  [한글 원본과 원래 포함된 라틴],
)
#row(
  "ROBOTO SOURCE",
  "Roboto Serif 14pt",
  [Hamburgefonts 0123456789  Sphinx of black quartz],
  [라틴 원본 · 변형 전 14pt optical-size Regular],
)

#v(2mm)
#box(width: 100%, inset: 6mm, radius: 2mm, fill: mist)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 9mm,
    [#eyebrow[GEOMETRY] #v(1.5mm) #text(size: 11pt)[Roboto wdth 91 · outline × 0.895 · advance × 0.889] ],
    [#eyebrow[VERTICAL ALIGN] #v(1.5mm) #text(size: 11pt)[height × 0.936 · shift −11] ],
    [#eyebrow[FIGURE POLICY] #v(1.5mm) #text(size: 11pt)[RIDI default 0–9 · Roboto alternates] ],
  )
]
