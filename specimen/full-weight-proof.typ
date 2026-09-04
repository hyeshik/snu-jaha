#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let coral = rgb("#A64B3C")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let extrabold-audit = json("../build/extrabold-full-audit.json")
#let ratio(value) = str(calc.round(value * 1000) / 1000)
#let unit(value) = str(calc.round(value * 10) / 10)

#set page(
  paper: "a4",
  margin: (left: 17mm, right: 17mm, top: 16mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.6pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · COMPLETE SEVEN-WEIGHT UPRIGHT RANGE
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.6mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.6pt, fill: gray)[RIDI −28R/−12/+0/+14/+22/+28R/+36R · ROBOTO W91 · X .895 · A .889],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.3pt, lang: "ko", fill: ink)
#set par(justify: true, leading: 0.74em, first-line-indent: 1em)

#let eyebrow(body) = text(size: 6.8pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / FULL-FONT PROOF]
  #v(3.5mm)
  #text(size: 24pt, weight: 700, body)
  #if note != none [
    #v(1.8mm)
    #text(size: 8.2pt, fill: gray, note)
  ]
  #v(4.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]

#let range-row(label, weight, source, role) = block(breakable: false)[
  #grid(
    columns: (25mm, 1fr, 30mm),
    column-gutter: 5mm,
    [
      #eyebrow[#label]
      #v(1mm)
      #text(size: 6.8pt, fill: gray, source)
    ],
    [#text(size: 20pt, weight: weight)[자하연 Research 24 h]],
    [#text(size: 7.2pt, fill: gray, role)],
  )
]

// Page 1 — complete range
#align(center)[
  #eyebrow[SEVEN STATIC STYLES / 100–800]
  #v(7mm)
  #text(size: 31pt, weight: 800)[일곱 단계의 연구 서체]
  #v(2.5mm)
  #text(size: 13.5pt, weight: 300, fill: green)[Thin · Light · Regular · Medium · SemiBold · Bold · ExtraBold]
]

#v(8mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 6mm,
    [#eyebrow[FULL HANGUL] #v(1mm) #text(size: 10.5pt, weight: 500)[11,172 / 11,172]],
    [#eyebrow[ENCODED ORDER] #v(1mm) #text(size: 10.5pt, weight: 500)[12,656 PASS]],
    [#eyebrow[FIGURE GAPS] #v(1mm) #text(size: 10.5pt, weight: 500)[92 · 78 · 66 · 56 · 52 · 48 · 44]],
  )
]

#v(7mm)
#range-row([THIN 100], 100, [RIDI −28 retain · Roboto 100/G−10], [18 pt 이상 display])
#v(2.8mm)
#range-row([LIGHT 300], 300, [RIDI −12 · Roboto W91/250], [도입 · 보조 본문])
#v(2.8mm)
#range-row([REGULAR 400], 400, [RIDI +0 · Roboto W91/400], [연속 본문])
#v(2.8mm)
#range-row([MEDIUM 500], 500, [RIDI +14 · Roboto W91/500], [완만한 강조])
#v(2.8mm)
#range-row([SEMIBOLD 600], 600, [RIDI +22 · Roboto W91/565], [절 제목 · 핵심 수치])
#v(2.8mm)
#range-row([BOLD 700], 700, [RIDI +28 retain · Roboto W91/610], [문서 제목])
#v(2.8mm)
#range-row([EXTRABOLD 800], 800, [RIDI +36 retain · Roboto W91/660], [강한 display 제목])

#v(6mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (23mm, 1fr),
  row-gutter: 1.7mm,
  [#eyebrow[100]], [#text(size: 13.5pt, weight: 100)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
  [#eyebrow[300]], [#text(size: 13.5pt, weight: 300)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
  [#eyebrow[400]], [#text(size: 13.5pt, weight: 400)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
  [#eyebrow[500]], [#text(size: 13.5pt, weight: 500)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
  [#eyebrow[600]], [#text(size: 13.5pt, weight: 600)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
  [#eyebrow[700]], [#text(size: 13.5pt, weight: 700)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
  [#eyebrow[800]], [#text(size: 13.5pt, weight: 800)[느 스 그 노 · 흙 뿳 휇 뿔 률]],
)

#pagebreak()

// Page 2 — Light role and threshold
#title(
  [Light 300: 읽기용 경계],
  note: [10–11 pt 보조 본문에서 획의 연속성, 혼합문장 색, 복잡한 한글의 속공간을 확인합니다.],
)

#v(5mm)
#grid(
  columns: (18mm, 1fr),
  row-gutter: 2.3mm,
  [#eyebrow[9 PT]], [#text(size: 9pt, weight: 300)[반복적 건조 스트레스와 recovery 17.2 µm · 뾂 뼒 뼮 뿳 휇]],
  [#eyebrow[10 PT]], [#text(size: 10pt, weight: 300)[반복적 건조 스트레스와 recovery 17.2 µm · 뾂 뼒 뼮 뿳 휇]],
  [#eyebrow[11 PT]], [#text(size: 11pt, weight: 300)[반복적 건조 스트레스와 recovery 17.2 µm · 뾂 뼒 뼮 뿳 휇]],
  [#eyebrow[14 PT]], [#text(size: 14pt, weight: 300)[자하연 Recovery kinetics 24 h]],
  [#eyebrow[24 PT]], [#text(size: 24pt, weight: 300)[가벼운 서론과 캡션]],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[LIGHT / 11 PT PARAGRAPH]
    #v(2mm)
    #set text(weight: 300, size: 11pt)
    반복적 건조 처리는 재급수 뒤 stomatal conductance의 회복 시간을 단축했다.
    처리군 48개체에서 8 h 평균은 0.781 ± 0.014였고, 대조군은 0.742 ±
    0.021이었다. Effect size는 0.63, 95% CI는 0.21–1.05로 추정됐다.

    #v(3mm)
    RNA abundance는 2, 8, 24 h에 측정했으며 minimum read depth는
    18.4 M였다. Light는 이처럼 본문보다 한 단계 물러난 초록, 도입문, 설명문에서
    Regular와 구별되면서도 긴 문장을 견뎌야 한다.
  ],
  [
    #eyebrow[REGULAR / CONTROL]
    #v(2mm)
    #set text(weight: 400, size: 11pt)
    반복적 건조 처리는 재급수 뒤 stomatal conductance의 회복 시간을 단축했다.
    처리군 48개체에서 8 h 평균은 0.781 ± 0.014였고, 대조군은 0.742 ±
    0.021이었다. Effect size는 0.63, 95% CI는 0.21–1.05로 추정됐다.

    #v(3mm)
    RNA abundance는 2, 8, 24 h에 측정했으며 minimum read depth는
    18.4 M였다. Regular는 연속 본문의 기준 먹색이며, 왼쪽 Light와 크기·행간·폭은
    모두 같고 윤곽 무게만 다르다.
  ],
)

#v(7mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[DENSE SENTINELS / 300]
  #v(2mm)
  #text(size: 18pt, weight: 300)[뾂 뼒 뼮 뿳 휇 흙 뿔 률 쫓 빛 활 괄]
]

#pagebreak()

// Page 3 — Thin role and threshold
#title(
  [Thin 100: display의 최소 크기],
  note: [9–14 pt는 진단용입니다. 18 pt부터 구조가 의도적으로 보이는지, 24–36 pt에서 세리프가 살아 있는지 확인합니다.],
)

#v(5mm)
#grid(
  columns: (18mm, 1fr),
  row-gutter: 2.6mm,
  [#eyebrow[9 PT]], [#text(size: 9pt, weight: 100)[진단용: 흙 뿳 휇 · Recovery 17.2 µm]],
  [#eyebrow[11 PT]], [#text(size: 11pt, weight: 100)[진단용: 흙 뿳 휇 · Recovery 17.2 µm]],
  [#eyebrow[14 PT]], [#text(size: 14pt, weight: 100)[진단용: 흙 뿳 휇 · Recovery 17.2 µm]],
  [#eyebrow[18 PT]], [#text(size: 18pt, weight: 100)[자하연의 계절 변화 · Recovery 24 h]],
  [#eyebrow[24 PT]], [#text(size: 24pt, weight: 100)[식물환경 연구 기록]],
  [#eyebrow[36 PT]], [#text(size: 36pt, weight: 100)[얇고 또렷한 제목]],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[THIN / HANGUL]
    #v(2mm)
    #text(size: 27pt, weight: 100)[뾂 뼒 뼮 뿳]
    #linebreak()
    #text(size: 27pt, weight: 100)[휇 흙 뿔 률]
    #linebreak()
    #text(size: 27pt, weight: 100)[쫓 빛 활 괄]
  ],
  [
    #eyebrow[THIN / LATIN]
    #v(2mm)
    #text(size: 26pt, weight: 100)[HAMBURGE]
    #linebreak()
    #text(size: 26pt, weight: 100)[minimum]
    #linebreak()
    #text(size: 26pt, weight: 100)[oxygen 24 h]
  ],
)

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[DISPLAY APPLICATION]
  #v(3mm)
  #text(size: 31pt, weight: 100)[
    자하연 수질 변화의 장기 기록
  ]
  #v(1mm)
  #text(size: 17pt, weight: 100, fill: green)[
    A longitudinal record of water-quality change
  ]
  #v(2mm)
  #text(size: 8pt, weight: 400, fill: gray)[1996–2026 · n = 1,248 observations · median interval 7 d]
]

#pagebreak()

// Page 4 — figures, punctuation, hierarchy
#title(
  [숫자·구두점·문서 위계],
  note: [이 upright proof의 기본 U+0030–0039는 고정폭 RIDIBatang 숫자입니다. italic 기본 숫자는 별도 italic proof에서 Roboto Serif로 확인합니다.],
)

#v(3mm)
#grid(
  columns: (19mm, 1fr),
  row-gutter: 1.3mm,
  [#eyebrow[100]], [#text(size: 12pt, weight: 100)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
  [#eyebrow[300]], [#text(size: 12pt, weight: 300)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
  [#eyebrow[400]], [#text(size: 12pt, weight: 400)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
  [#eyebrow[500]], [#text(size: 12pt, weight: 500)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
  [#eyebrow[600]], [#text(size: 12pt, weight: 600)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
  [#eyebrow[700]], [#text(size: 12pt, weight: 700)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
  [#eyebrow[800]], [#text(size: 12pt, weight: 800)[00112277 · 0–1 · 1–2 · 7–8 · 10—20 · −17.2 µm]],
)

#v(3mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(2mm)
#text(size: 24pt, weight: 100)[식물환경 관측 보고서 2026]
#v(1mm)
#text(size: 21pt, weight: 800)[반복적 건조 경험과 기공 회복 속도]
#v(1.5mm)
#text(size: 12pt, weight: 300, fill: green)[Repeated drought exposure shifts stomatal recovery timing]
#v(2mm)
#text(size: 8pt, weight: 400, fill: gray)[김자하 · Minseo Park · 관악 식물환경연구실 · 2 September 2026]

#v(2mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #text(size: 14pt, weight: 600)[1. 연구 배경]
    #v(1.5mm)
    #text(size: 10pt, weight: 300)[수분 부족은 식물의 생장과 탄소 동화를 동시에 제한한다.] 잎의
    water potential이 감소하면 guard cell의 turgor가 변하고 stomatal
    conductance가 낮아진다. 본 연구는 repeated mild drought가 회복 곡선의 시간
    상수를 바꾸는지 검정했다.

    #v(2mm)
    #text(size: 14pt, weight: 600)[2. 주요 결과]
    #v(1.5mm)
    재급수 8 h 뒤 Fv/Fm은 repeated-stress에서 #text(weight: 500)[0.781 ±
    0.014], single-stress에서 0.742 ± 0.021이었다. 차이는 유의했으며
    #text(weight: 600)[_p_ = 0.0006]이었다.
  ],
  [
    #box(width: 100%, inset: 4mm, radius: 1.5mm, fill: wash)[
      #eyebrow[KEY FINDING]
      #v(1.5mm)
      #text(size: 20pt, weight: 800)[31.2%]
      #v(1mm)
      #text(size: 10pt, weight: 500)[기공 회복 시간 감소]
      #v(1mm)
      #text(size: 8pt, weight: 300, fill: gray)[95% CI 24.1–38.0% · n = 48]
    ]

    #v(3mm)
    #eyebrow[MEASUREMENT NOTE]
    #v(1mm)
    #text(size: 9pt, weight: 300)[센서 해상도 0.1 µmol m−2 s−1, sampling interval
    30 s, chamber temperature 24.0 ± 0.3 °C.]
  ],
)

#pagebreak()

// Page 5 — ExtraBold full-font role
#title(
  [ExtraBold 800: 강한 display의 상한],
  note: [RIDI Regular 원본 +36 retain, 한글 advance 108%, Roboto Serif wght 660입니다. 작은 크기는 진단용이며 18–36 pt의 제목과 핵심 수치를 우선 확인합니다.],
)

#v(4mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 6mm,
    [#eyebrow[FULL HANGUL] #v(1mm) #text(size: 10.5pt, weight: 800)[11,172 PASS]],
    [#eyebrow[COVERAGE / REGULAR] #v(1mm) #text(size: 10.5pt, weight: 800)[#ratio(extrabold-audit.at("hangul_coverage_ratio").at("median"))]],
    [#eyebrow[SCRIPT DIFFERENCE] #v(1mm) #text(size: 10.5pt, weight: 800)[#ratio(extrabold-audit.at("mixed_script_coverage_difference"))]],
  )
]

#v(6mm)
#grid(
  columns: (18mm, 1fr),
  row-gutter: 2.3mm,
  [#eyebrow[10 PT]], [#text(size: 10pt, weight: 800)[진단용: 반복적 건조 스트레스 · 뺄 뼒 뼮 뾂]],
  [#eyebrow[12 PT]], [#text(size: 12pt, weight: 800)[진단용: 반복적 건조 스트레스 · 뺄 뼒 뼮 뾂]],
  [#eyebrow[14 PT]], [#text(size: 14pt, weight: 800)[자하연 Recovery kinetics 24 h · 뺄 뼒 뼮 뾂]],
  [#eyebrow[18 PT]], [#text(size: 18pt, weight: 800)[자하연 Recovery kinetics 24 h]],
  [#eyebrow[24 PT]], [#text(size: 24pt, weight: 800)[반복적 건조와 회복]],
  [#eyebrow[36 PT]], [#text(size: 36pt, weight: 800)[강하고 또렷한 제목]],
)

#v(6mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(4mm)
#eyebrow[BOLD 700 / EXTRABOLD 800]
#v(2mm)
#grid(
  columns: (20mm, 1fr),
  row-gutter: 2.8mm,
  [#eyebrow[700]], [#text(size: 20pt, weight: 700)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
  [#eyebrow[800]], [#text(size: 20pt, weight: 800)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
  [#eyebrow[700]], [#text(size: 17pt, weight: 700)[자하연 Research 24 h · 31.20%]],
  [#eyebrow[800]], [#text(size: 17pt, weight: 800)[자하연 Research 24 h · 31.20%]],
)

#v(6mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[FULL-FONT AUDIT RESULT]
  #v(2mm)
  #text(size: 8.7pt)[
    12,656 encoded characters · 11,172 modern Hangul · representative advance 943→1018 · unexpected mismatch 0 ·
    minimum pair gap #unit(extrabold-audit.at("hangul_spacing").at("minimum_gap")) units · Bold→ExtraBold vector/raster reversal 0 · 00 gap 44 units.
    64 ppem에서 사라진 counter는 없고, 남은 counter 면적 감소는 review record로 보존했습니다.
  ]
]

#pagebreak()

// Page 6 — capital A overlap regression
#title(
  [A 접합부: 연속된 외곽선],
  note: [가로획과 사선 획의 겹침을 하나의 외곽선으로 합쳤습니다. 흰 실선이나 핀홀이 남지 않는지 굵은 weight와 악센트 변형에서 확인합니다.],
)

#v(4mm)
#grid(
  columns: (18mm, 1fr),
  row-gutter: 2.6mm,
  [#eyebrow[100]], [#text(size: 30pt, weight: 100)[A Á À Ä Å Ą Æ А]],
  [#eyebrow[300]], [#text(size: 30pt, weight: 300)[A Á À Ä Å Ą Æ А]],
  [#eyebrow[400]], [#text(size: 30pt, weight: 400)[A Á À Ä Å Ą Æ А]],
  [#eyebrow[500]], [#text(size: 30pt, weight: 500)[A Á À Ä Å Ą Æ А]],
  [#eyebrow[600]], [#text(size: 30pt, weight: 600)[A Á À Ä Å Ą Æ А]],
  [#eyebrow[700]], [#text(size: 30pt, weight: 700)[A Á À Ä Å Ą Æ А]],
  [#eyebrow[800]], [#text(size: 30pt, weight: 800)[A Á À Ä Å Ą Æ А]],
)

#v(6mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[BOLD 700 / 48 PT]
    #v(2mm)
    #text(size: 48pt, weight: 700)[AAA]
    #v(2mm)
    #text(size: 14pt, weight: 700)[AARDVARK · DATA ANALYSIS]
  ],
  [
    #eyebrow[EXTRABOLD 800 / 48 PT]
    #v(2mm)
    #text(size: 48pt, weight: 800)[AAA]
    #v(2mm)
    #text(size: 14pt, weight: 800)[환경 A/B 분석 · 24 Å]
  ],
)

#v(7mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[REGRESSION CHECK]
  #v(1.5mm)
  #text(size: 8.7pt)[완성 폰트의 `A`에 폭이 넓고 높이가 낮은 독립 crossbar contour가 남으면 자동 검사가 실패합니다. 윤곽의 외접 범위와 advance는 union 전후 동일합니다.]
]
