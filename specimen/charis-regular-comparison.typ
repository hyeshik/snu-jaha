#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let coral = rgb("#A64B3C")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let audit = json("../build/charis-comparison/audit.json")
#let current = audit.at("fonts").at("roboto")
#let candidate = audit.at("fonts").at("charis")
#let ridi = audit.at("fonts").at("ridibatang")
#let source = audit.at("fonts").at("charis_source")
#let comparison = audit.at("comparison")
#let pct(value) = str(calc.round(value * 1000) / 10) + "%"
#let unit(value) = str(calc.round(value * 10) / 10)
#let glyph(font, character) = font.at("glyphs").at(character)

#set page(
  paper: "a4",
  margin: (left: 16mm, right: 16mm, top: 15mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.4pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · REGULAR LATIN SOURCE A/B
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.5mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.4pt, fill: gray)[RIDIBatang Hangul · Regular 400 · identical text and size],
      text(size: 6.8pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.3pt, lang: "ko", fill: ink)
#set par(leading: 0.72em)

#let eyebrow(body, color: accent) = text(size: 6.7pt, weight: 700, tracking: 0.11em, fill: color, body)
#let title(body, note: none) = block(breakable: false)[
  #eyebrow[REGULAR 400 / CONTROLLED SOURCE COMPARISON]
  #v(2.8mm)
  #text(size: 23pt, weight: 700, body)
  #if note != none [
    #v(1.5mm)
    #text(size: 8.1pt, fill: gray, note)
  ]
  #v(3.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let metric(label, value, note: none) = box(width: 100%, inset: 4mm, radius: 1.4mm, fill: wash)[
  #eyebrow(label)
  #v(1.4mm)
  #text(size: 16pt, weight: 700)[#value]
  #if note != none [#v(0.8mm) #text(size: 6.8pt, fill: gray, note)]
]

#let ab-row(label, size, body) = block(breakable: false)[
  #grid(
    columns: (19mm, 1fr),
    column-gutter: 5mm,
    [#eyebrow(label)],
    [
      #text(font: "SNU Jaha", size: size, body)
      #v(1.3mm)
      #text(font: "SNU Jaha Latin Alt", size: size, body)
    ],
  )
]

// Page 1 — immediate A/B
#title(
  [Roboto Serif와 Charis 7.000],
  note: [한글·기본 숫자는 동일합니다. 첫 줄은 현재 Roboto Serif, 둘째 줄은 세로 위치를 보정한 Charis 후보입니다.],
)

#v(4mm)
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 5mm,
  metric([LATIN WIDTH], pct(comparison.at("charis_advance_vs_roboto")), note: [현재 합성본 대비 total advance]),
  metric([INK DENSITY], pct(comparison.at("charis_coverage_vs_roboto")), note: [현재 합성본 대비 vector coverage]),
  metric([UNCHANGED], [#audit.at("hangul_mismatch_count") / #audit.at("figure_mismatch_count")], note: [한글 mismatch / 숫자 mismatch]),
)

#v(6mm)
#box(width: 100%, inset: 4mm, radius: 1.4mm, stroke: 0.5pt + rule)[
  #grid(
    columns: (30mm, 1fr),
    row-gutter: 1.5mm,
    [#eyebrow[CURRENT]], [#text(font: "SNU Jaha", size: 10pt)[Roboto Serif · x 0.895 · y 0.936 · shift −11]],
    [#eyebrow[CANDIDATE]], [#text(font: "SNU Jaha Latin Alt", size: 10pt)[Charis 7.000 · x 1.000 · y 1.005 · shift −7]],
  )
]

#v(6mm)
#ab-row([30 PT], 30pt, [환경 Research 기록과 Recovery 24 h])
#v(5mm)
#ab-row([20 PT], 20pt, [자하연의 minimum oxygen response · 31.2%])
#v(4mm)
#ab-row([13 PT], 13pt, [식물환경 관측은 2–8 h 구간의 transcript abundance를 비교했다.])
#v(4mm)
#ab-row([10 PT], 10pt, [반복적 drought exposure 뒤 Fv/Fm은 0.781 ± 0.014였고 recovery constant는 6.3 h였다.])

#pagebreak()

// Page 2 — long mixed reading
#title(
  [긴 혼합문장의 폭과 호흡],
  note: [동일한 9.6 pt, 행간, 문단 폭입니다. 줄바꿈 차이는 라틴 advance 변화에서만 생깁니다.],
)

#let article(font-name, label, color) = [
  #eyebrow(label, color: color)
  #v(2mm)
  #set text(font: font-name, size: 9.6pt)
  #set par(justify: true, leading: 0.72em, first-line-indent: 1em)

  반복적 건조 처리는 재급수 뒤 stomatal conductance와 photosystem II efficiency의 회복 속도를 바꾸었다.
  Control 16개체와 treatment 32개체를 0, 2, 8, 24, 48, 72 h에 측정했으며, soil water content는
  31.2%에서 9.5%까지 감소했다. Repeated-stress의 Fv/Fm은 8 h에 0.781 ± 0.014였고,
  single-stress는 0.742 ± 0.021이었다. Estimated time constant는 각각 6.3 h와 10.8 h였으며
  bootstrap difference의 95% CI는 −6.9–−2.2 h였다.

  RNA sequencing에서는 sample당 4.2–5.4 × 10⁶ reads를 얻었고 median mapping rate는 94.7%였다.
  Differential expression 기준은 absolute log₂ fold change ≥ 0.7, adjusted _p_ < 0.05로 정했다.
  총 612 genes가 기준을 만족했으며 _RD29A_, _DREB2A_, _HSP70_의 peak time은 반복 처리군에서
  3.8–5.4 h 앞당겨졌다. These observations support a timing-based model of drought memory rather than
  a simple increase in response amplitude.

  혼합 본문에서는 영어가 한글보다 넓다는 사실 자체보다, 한두 단어가 문장 속에서 별도의 회색 띠처럼 보이는지가 중요하다.
  Character spacing이 지나치게 느슨하면 English terminology가 문단의 리듬을 끊고, 반대로 너무 조밀하면 serif가 뭉쳐 보인다.
  두 후보의 줄 수, 오른쪽 rag, 숫자와 단위 주변의 공백, 소문자 counter를 함께 비교한다.
]

#grid(
  columns: (1fr, 1fr),
  column-gutter: 10mm,
  article("SNU Jaha", [ROBOTO SERIF / CURRENT], accent),
  article("SNU Jaha Latin Alt", [CHARIS 7 / CANDIDATE], green),
)

#v(6mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(4mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 10mm,
  [#eyebrow[CURRENT LINE] #v(1.5mm) #text(font: "SNU Jaha", size: 13pt)[환경 HAMBURGEFONTS minimum oxygen 0127]],
  [#eyebrow[CANDIDATE LINE] #v(1.5mm) #text(font: "SNU Jaha Latin Alt", size: 13pt)[환경 HAMBURGEFONTS minimum oxygen 0127]],
)

#pagebreak()

// Page 3 — character texture and metrics
#title(
  [글자 크기·baseline·획 무게],
  note: [대표 글자의 실제 outline bounds와 advance를 1000 UPM 단위로 비교합니다.],
)

#grid(
  columns: (26mm, 1fr),
  row-gutter: 2.6mm,
  [#eyebrow[CURRENT]], [#text(font: "SNU Jaha", size: 20pt)[HAMBURGEFONTS minimum oxygen Hxngp]],
  [#eyebrow[CANDIDATE]], [#text(font: "SNU Jaha Latin Alt", size: 20pt)[HAMBURGEFONTS minimum oxygen Hxngp]],
  [#eyebrow[RIDI LATIN]], [#text(font: "RIDIBatang", size: 20pt)[HAMBURGEFONTS minimum oxygen Hxngp]],
  [#eyebrow[CHARIS RAW]], [#text(font: "Charis", size: 20pt)[HAMBURGEFONTS minimum oxygen Hxngp]],
)

#v(6mm)
#table(
  columns: (18mm, 21mm, 21mm, 21mm, 21mm, 21mm, 21mm),
  inset: (x: 1.4mm, y: 1.5mm),
  stroke: 0.35pt + rule,
  align: (left, right, right, right, right, right, right),
  table.header([#eyebrow[FONT]], [#eyebrow[H ADV]], [#eyebrow[H TOP]], [#eyebrow[X TOP]], [#eyebrow[G BOT]], [#eyebrow[P BOT]], [#eyebrow[INK]]),
  [Current],
  [#unit(glyph(current, "H").at("advance"))],
  [#unit(glyph(current, "H").at("bounds").at(3))],
  [#unit(glyph(current, "x").at("bounds").at(3))],
  [#unit(glyph(current, "g").at("bounds").at(1))],
  [#unit(glyph(current, "p").at("bounds").at(1))],
  [#pct(current.at("latin").at("coverage"))],
  [Candidate],
  [#unit(glyph(candidate, "H").at("advance"))],
  [#unit(glyph(candidate, "H").at("bounds").at(3))],
  [#unit(glyph(candidate, "x").at("bounds").at(3))],
  [#unit(glyph(candidate, "g").at("bounds").at(1))],
  [#unit(glyph(candidate, "p").at("bounds").at(1))],
  [#pct(candidate.at("latin").at("coverage"))],
  [RIDI Latin],
  [#unit(glyph(ridi, "H").at("advance"))],
  [#unit(glyph(ridi, "H").at("bounds").at(3))],
  [#unit(glyph(ridi, "x").at("bounds").at(3))],
  [#unit(glyph(ridi, "g").at("bounds").at(1))],
  [#unit(glyph(ridi, "p").at("bounds").at(1))],
  [#pct(ridi.at("latin").at("coverage"))],
  [Charis raw],
  [#unit(glyph(source, "H").at("advance"))],
  [#unit(glyph(source, "H").at("bounds").at(3))],
  [#unit(glyph(source, "x").at("bounds").at(3))],
  [#unit(glyph(source, "g").at("bounds").at(1))],
  [#unit(glyph(source, "p").at("bounds").at(1))],
  [#pct(source.at("latin").at("coverage"))],
)

#v(4mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 8mm,
  [
    #eyebrow[ALPHABET / 13 PT]
    #v(1.5mm)
    #grid(
      columns: (12mm, 1fr),
      row-gutter: 0.7mm,
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[ABCDEFGHIJKLM]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[ABCDEFGHIJKLM]],
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[NOPQRSTUVWXYZ]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[NOPQRSTUVWXYZ]],
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[abcdefghijklm]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[abcdefghijklm]],
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[nopqrstuvwxyz]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[nopqrstuvwxyz]],
    )
  ],
  [
    #eyebrow[SCIENTIFIC / 13 PT]
    #v(1.5mm)
    #grid(
      columns: (12mm, 1fr),
      row-gutter: 1.1mm,
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[CO₂ H₂O RNA-seq]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[CO₂ H₂O RNA-seq]],
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[Fv/Fm µm mol]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[Fv/Fm µm mol]],
      [#eyebrow[CUR]], [#text(font: "SNU Jaha", size: 13pt)[−17.2 ± 0.014 · 95% CI]],
      [#eyebrow[ALT]], [#text(font: "SNU Jaha Latin Alt", size: 13pt)[−17.2 ± 0.014 · 95% CI]],
    )
  ],
)

#pagebreak()

// Page 4 — decision page
#title(
  [교체 여부를 판단할 지점],
  note: [이 후보는 Regular만 만들었으며 production family와 다른 이름으로 설치됩니다.],
)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[ROBOTO SERIF / CURRENT]
    #v(2mm)
    #text(font: "SNU Jaha", size: 18pt)[환경과 Research 사이의 넓은 호흡]
    #v(3mm)
    #set text(font: "SNU Jaha", size: 10.5pt)
    현재 라틴은 큰 x-height와 비교적 열린 spacing으로 화면에서 또렷하다. 다만 한국어 문장에 긴 English terminology가 반복되면
    단어 폭이 한글보다 빠르게 늘어나 문단의 리듬이 라틴 중심으로 보일 수 있다.
  ],
  [
    #eyebrow([CHARIS 7 / CANDIDATE], color: green)
    #v(2mm)
    #text(font: "SNU Jaha Latin Alt", size: 18pt)[환경과 Research 사이의 좁은 호흡]
    #v(3mm)
    #set text(font: "SNU Jaha Latin Alt", size: 10.5pt)
    후보 라틴은 RIDIBatang 원본 라틴과 비슷한 폭·획 면적을 가지며 serif가 더 둥글고 단단하다. 소문자 x-height는 조금 낮고
    획은 약간 진해지므로, 긴 본문에서 한글과 먹색이 안정되는지 확인해야 한다.
  ],
)

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 7mm,
    [#eyebrow[WIDTH] #v(1.3mm) #text(size: 12pt, weight: 700)[#pct(comparison.at("charis_advance_vs_roboto"))] #v(1mm) #text(size: 7pt, fill: gray)[영문 sample total advance]],
    [#eyebrow[VERTICAL FIT] #v(1.3mm) #text(size: 12pt, weight: 700)[#unit(comparison.at("charis_bounds_rms_from_ridi").at("y")) u] #v(1mm) #text(size: 7pt, fill: gray)[RIDI 대표 글자 bounds RMS]],
    [#eyebrow[WEIGHT FIT] #v(1.3mm) #text(size: 12pt, weight: 700)[#pct(candidate.at("latin").at("coverage"))] #v(1mm) #text(size: 7pt, fill: gray)[candidate vector coverage]],
  )
]

#v(8mm)
#eyebrow[FINAL READING STRIP]
#v(2mm)
#text(font: "SNU Jaha", size: 14pt)[환경 signal integration은 24 h 뒤 baseline으로 돌아왔다.]
#v(2mm)
#text(font: "SNU Jaha Latin Alt", size: 14pt)[환경 signal integration은 24 h 뒤 baseline으로 돌아왔다.]
#v(4mm)
#text(font: "SNU Jaha", size: 14pt)[Repeated drought exposure · 기공 회복 속도 · n = 48]
#v(2mm)
#text(font: "SNU Jaha Latin Alt", size: 14pt)[Repeated drought exposure · 기공 회복 속도 · n = 48]

#v(8mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[AUDIT]
  #v(1.5mm)
  한글 11,172자와 RIDIBatang 기본 숫자는 두 합성본에서 동일합니다. 후보 family name은 OFL Reserved Font Name을 피한
  `SNU Jaha Latin Alt`이며, 원본 Charis 명칭은 출처 표시에만 사용했습니다.
]
