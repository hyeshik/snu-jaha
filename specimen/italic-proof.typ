#let ink = rgb("#17243B")
#let blue = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")

#set page(
  paper: "a4",
  margin: (left: 17mm, right: 17mm, top: 16mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.6pt, tracking: 0.08em, fill: gray)[SNU JAHA · UPRIGHT + NATIVE ITALIC]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.6mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.6pt, fill: gray)[ROBOTO SERIF ITALIC W91 · X .895 · A .889 · POSTURE-SPECIFIC FIGURES],
      text(size: 7pt, fill: blue)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.5pt, lang: "ko", fill: ink)
#set par(justify: true, leading: 0.82em)

#let eyebrow(body) = text(size: 6.8pt, weight: 700, tracking: 0.12em, fill: blue, body)
#let title(body, note: none) = block[
  #eyebrow[ITALIC FAMILY PROOF]
  #v(3mm)
  #text(size: 24pt, weight: 700, body)
  #if note != none [#v(1.8mm) #text(size: 8.2pt, fill: gray, note)]
  #v(4mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]
#let pair(label, weight) = block(breakable: false)[
  #grid(
    columns: (20mm, 1fr),
    column-gutter: 4mm,
    [#eyebrow[#label]],
    [
      #text(size: 15.5pt, weight: weight)[환경 Research 24 h · Hamburgefontsiv]
      #linebreak()
      #text(size: 15.5pt, weight: weight, style: "italic")[환경 Research 24 h · Hamburgefontsiv]
    ],
  )
]

#title(
  [일곱 굵기의 upright와 italic],
  note: [italic에서는 라틴과 기본 숫자가 모두 Roboto Serif의 native italic이고, 한글만 RIDIBatang 계열의 upright 형태를 유지합니다.],
)
#v(5mm)
#pair([THIN 100], 100)
#v(3mm)
#pair([LIGHT 300], 300)
#v(3mm)
#pair([REGULAR 400], 400)
#v(3mm)
#pair([MEDIUM 500], 500)
#v(3mm)
#pair([SEMIBOLD 600], 600)
#v(3mm)
#pair([BOLD 700], 700)
#v(3mm)
#pair([EXTRABOLD 800], 800)
#v(6mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[POSTURE CHECK]
  #v(2mm)
  #text(size: 23pt, weight: 400)[관찰과 해석 / Observation and inference]
  #v(1mm)
  #text(size: 23pt, weight: 400, style: "italic")[관찰과 해석 / Observation and inference]
]

#pagebreak()

#title(
  [라틴→한글 경계 전수 규칙],
  note: [문자·숫자의 실제 오른쪽 돌출과 한글 왼쪽 여백을 재서 최소 30-unit 광학 여백을 둡니다. 숫자 대체자와 라틴 합자도 포함합니다.],
)
#v(4mm)
#eyebrow[HIGH-RISK CAPITALS / ALL WEIGHTS]
#v(2mm)
#grid(
  columns: (18mm, 1fr),
  row-gutter: 2.2mm,
  [#eyebrow[100]], [#text(size: 14pt, weight: 100, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
  [#eyebrow[300]], [#text(size: 14pt, weight: 300, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
  [#eyebrow[400]], [#text(size: 14pt, weight: 400, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
  [#eyebrow[500]], [#text(size: 14pt, weight: 500, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
  [#eyebrow[600]], [#text(size: 14pt, weight: 600, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
  [#eyebrow[700]], [#text(size: 14pt, weight: 700, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
  [#eyebrow[800]], [#text(size: 14pt, weight: 800, style: "italic")[T환경 K환경 V환경 W환경 Y환경 J환경 A환경]],
)
#v(6mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[F FAMILY / LIGATURES]
    #v(2mm)
    #text(size: 18pt, style: "italic")[f환경 ff환경 fi환경 fl환경]
    #v(2mm)
    #text(size: 14pt, weight: 700, style: "italic")[f한 ff한 fi한 fl한]
    #v(3mm)
    #text(size: 9pt, fill: gray)[liga가 켜진 실제 조판에서 f_f, f_i, f_l 결과 글리프의 외곽까지 검사합니다.]
  ],
  [
    #eyebrow[LOWERCASE + ALTERNATES]
    #v(2mm)
    #text(size: 18pt, style: "italic")[j환경 r환경 t환경 x환경 z환경]
    #v(2mm)
    #text(size: 14pt, weight: 700, style: "italic")[j한 r한 t한 x한 z한]
    #v(3mm)
    #text(size: 9pt, fill: gray)[모든 encoded non-CJK letter에서 시작해 GSUB로 도달 가능한 대체자·합자를 함께 분류합니다.]
  ],
)
#v(3mm)
#eyebrow[FIGURES → HANGUL / NATIVE ITALIC]
#v(1.5mm)
#text(size: 15pt, style: "italic")[0환경 1환경 2환경 7환경 8환경 · 2026환경 · 95한]
#v(7mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[CONTINUOUS MIXED RUN]
  #v(2mm)
  #text(size: 16pt, style: "italic")[The TF 환경 model과 K환경 coefficient는 five-fold fit에서 유의했다.]
]

#pagebreak()

#title(
  [혼합 본문의 리듬],
  note: [이탤릭 강조가 한글 문장 속 English term, 학명, 변수명과 자연스럽게 이어지는지 확인합니다.],
)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[REGULAR / 10.5 PT]
    #v(2mm)
    2026년 봄 자하연 수계에서 수집한 48개 시료를 대상으로 dissolved oxygen,
    chlorophyll-a, nitrate concentration을 측정했다. 반복 측정 간격은 6 h였고,
    수온은 17.2–24.8 °C 범위였다. 주성분 분석에서 _temperature loading_은
    PC1의 0.781을 설명했으며, _K환경 response_는 강우 뒤 12 h부터 뚜렷해졌다.

    #v(3mm)
    선형 혼합모형은 site를 random intercept로, treatment와 time을 fixed effect로
    두었다. _F-value_ = 8.41, _p_ = 0.0037이었고 95% CI는 0.21–1.05였다.
    _T환경 transition_, _V환경 vector_, _W환경 window_처럼 기울어진 라틴이
    upright 한글 앞에 놓이는 경우에도 획이 충돌하지 않아야 한다.
  ],
  [
    #eyebrow[LIGHT / 10.5 PT]
    #v(2mm)
    #text(weight: 300)[
      Sequencing library는 sample당 평균 18.4 M reads를 확보했다. QC 이후 남은
      1,248개 feature에 Benjamini–Hochberg correction을 적용했고, adjusted
      _p_ < 0.05인 항목은 37개였다. 특히 _fl환경 module_과 _ff한 boundary_는
      합자 치환 뒤에도 일정한 optical clearance를 유지해야 한다.

      #v(3mm)
      결과는 median ± MAD로 요약했고 effect size는 0.63이었다. 이 문단은 한글
      조사 앞의 _italic term_이 지나치게 벌어지지 않으면서도 RIDIBatang의 뭉툭한
      부리와 Roboto Serif의 균일한 획이 한 호흡으로 읽히는지 보기 위한 proof다.
    ]
  ],
)
#v(8mm)
#box(width: 100%, inset: 5mm, stroke: 0.5pt + rule, radius: 1.5mm)[
  #eyebrow[SCIENTIFIC NAMES]
  #v(2mm)
  #text(size: 14pt)[_Arabidopsis thaliana_ 환경 반응 · _Escherichia coli_ 배양 37 °C · _in vivo_ 분석 24 h]
]

#pagebreak()

#title(
  [자세별 숫자와 학술 조판],
  note: [upright는 RIDIBatang B안 520-unit 숫자, italic은 주변 영문과 같은 Roboto Serif native italic 498-unit 숫자를 사용합니다.],
)
#v(4mm)
#eyebrow[UPRIGHT / RIDIBATANG 520]
#v(1.5mm)
#grid(
  columns: (20mm, 1fr),
  row-gutter: 2.2mm,
  [#eyebrow[100]], [#text(size: 14pt, weight: 100)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
  [#eyebrow[300]], [#text(size: 14pt, weight: 300)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
  [#eyebrow[400]], [#text(size: 14pt, weight: 400)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
  [#eyebrow[500]], [#text(size: 14pt, weight: 500)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
  [#eyebrow[600]], [#text(size: 14pt, weight: 600)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
  [#eyebrow[700]], [#text(size: 14pt, weight: 700)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
  [#eyebrow[800]], [#text(size: 14pt, weight: 800)[00112233445566778899 · 2026-09-03 · 17.2 µm]],
)
#v(6mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 9mm,
  [
    #eyebrow[UPRIGHT DATA]
    #v(2mm)
    #text(size: 12.5pt)[n = 1,248 · 37.5% · 0.0037 · −17.2 °C]
    #v(2mm)
    #text(size: 12.5pt)[0–1 · 1–2 · 7–8 · 10—20 · 95% CI]
  ],
  [
    #eyebrow[ITALIC DATA]
    #v(2mm)
    #text(size: 12.5pt, style: "italic")[n = 1,248 · 37.5% · 0.0037 · −17.2 °C]
    #v(2mm)
    #text(size: 12.5pt, style: "italic")[0–1 · 1–2 · 7–8 · 10—20 · 95% CI]
  ],
)
#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[FEATURE RETENTION]
  #v(2mm)
  #grid(
    columns: (1fr, 1fr, 1fr),
    [#text(size: 16pt)[0123456789] #linebreak() #text(size: 7pt, fill: gray)[upright · RIDIBatang 520]],
    [#text(size: 16pt, style: "italic")[0123456789] #linebreak() #text(size: 7pt, fill: gray)[italic · Roboto Serif 498]],
    [#text(size: 16pt, style: "italic", features: ("onum",))[0123456789] #linebreak() #text(size: 7pt, fill: gray)[italic onum · Roboto Serif]],
  )
]
