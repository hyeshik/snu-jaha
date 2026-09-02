#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let coral = rgb("#A64B3C")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#EEF3F3")
#let paper = rgb("#FCFBF7")
#let audit = json("../build/extrabold-audit/audit.json")
#let raster-dir = "../build/extrabold-audit/rasters"

#set page(
  paper: "a4",
  margin: (left: 17mm, right: 17mm, top: 16mm, bottom: 16mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.6pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · EXTRABOLD STAGE 1
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.6mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.6pt, fill: gray)[REPRESENTATIVE GLYPHS · NOT A FULL EXTRABOLD FONT],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.72em)

#let eyebrow(body) = text(size: 6.8pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let cjk(label) = audit.at("cjk").find(item => item.at("label") == label)
#let latin(label) = audit.at("latin").find(item => item.at("label") == label)
#let cjk-font(label) = cjk(label).at("family")
#let latin-font(label) = latin(label).at("family")
#let pair-font(cjk-label, latin-label) = (cjk-font(cjk-label), latin-font(latin-label))
#let ratio(value) = str(calc.round(value * 1000) / 1000)
#let gap(value) = str(calc.round(value * 10) / 10)
#let count(item, key) = str(item.at(key).len())
#let mixed(cjk-label, latin-label, size: 18pt, body) = text(
  font: pair-font(cjk-label, latin-label),
  size: size,
  body,
)
#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / POSITIVE OUTLINE AUDIT]
  #v(3.5mm)
  #text(size: 24pt, weight: 700, body)
  #if note != none [
    #v(1.8mm)
    #text(size: 8.2pt, fill: gray, note)
  ]
  #v(4.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]
#let metric-row(label, item) = (
  [#eyebrow[#label]],
  [#text(size: 8pt)[#ratio(item.at("median_ratio"))]],
  [#text(size: 8pt)[+#ratio(item.at("bold_separation"))]],
  [#text(size: 8pt)[#gap(item.at("zero_gap"))]],
  [#text(size: 8pt)[#count(item, "foreground_merges") / #count(item, "counter_losses")]],
)

// Page 1 — measured outcome
#align(center)[
  #eyebrow[STAGE 1 / 12 CJK + 5 LATIN MICROFONTS]
  #v(7mm)
  #text(size: 31pt, weight: 700)[두꺼워질수록 남겨야 할 공간]
  #v(2.5mm)
  #text(size: 13.5pt, fill: green)[ExtraBold without losing RIDIBatang's counters]
]

#v(8mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 6mm,
    [
      #eyebrow[AUTOMATIC RESULT]
      #v(1.5mm)
      #text(size: 11pt, weight: 700, fill: coral)[CJK 0 PASS]
      #v(1mm)
      #text(size: 7.4pt, fill: gray)[모든 후보에 raster 접합 또는 counter 감소 기록]
    ],
    [
      #eyebrow[MEASURED LEADER]
      #v(1.5mm)
      #text(size: 11pt, weight: 700)[+30 retain / 633]
      #v(1mm)
      #text(size: 7.4pt, fill: gray)[한글 1.493 · 라틴 1.498 · 차이 0.005]
    ],
    [
      #eyebrow[STATUS]
      #v(1.5mm)
      #text(size: 11pt, weight: 700, fill: green)[VISUAL REVIEW PASS]
      #v(1mm)
      #text(size: 7.4pt, fill: gray)[아래 접합부 확인 후 +30 retain 한 후보만 승격]
    ],
  )
]

#v(7mm)
#eyebrow[NUMERIC CJK SHORTLIST]
#v(2mm)
#grid(
  columns: (29mm, 25mm, 25mm, 25mm, 1fr),
  row-gutter: 2.4mm,
  [#text(size: 7pt, fill: gray)[CANDIDATE]],
  [#text(size: 7pt, fill: gray)[INK / REG]],
  [#text(size: 7pt, fill: gray)[Δ FROM BOLD]],
  [#text(size: 7pt, fill: gray)[00 GAP]],
  [#text(size: 7pt, fill: gray)[MERGE / COUNTER]],
  ..metric-row([+28 AUTO], cjk("+28 auto")),
  ..metric-row([+28 RETAIN], cjk("+28 retain")),
  ..metric-row([+30 AUTO], cjk("+30 auto")),
  ..metric-row([+30 RETAIN], cjk("+30 retain")),
  ..metric-row([+32 AUTO], cjk("+32 auto")),
  ..metric-row([+32 RETAIN], cjk("+32 retain")),
  ..metric-row([+36 AUTO], cjk("+36 auto")),
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[INTERPRETATION]
  #v(2mm)
  #text(size: 8.7pt)[
    +30 retain은 먹색과 한·영 균형이 가장 좋고, +32 auto는 기존 Medium–Bold 제작법을
    그대로 연장한다는 장점이 있습니다. `CJK` weight mode는 한글 결과가 auto와 같으면서
    숫자 `00` 간격만 78.3–80.0 units로 벌어져 후보에서 제외합니다.
  ]
]

#pagebreak()

// Page 2 — offset ladder
#title(
  [Auto offset: 먹색과 공간의 교환],
  note: [라틴은 모두 통과 후보 wght 633으로 고정했습니다. Bold control 아래에서 한글 offset만 비교합니다.],
)

#v(5mm)
#grid(
  columns: (22mm, 1fr),
  row-gutter: 4.3mm,
  [#eyebrow[BOLD +24]], [#text(size: 21pt, weight: 700)[느 스 기 가 · 흙 뿳 쀻 뺨 뺌 뾂 뼒 뼮]],
  [#eyebrow[+28 AUTO]], [#mixed("+28 auto", "wght 633", size: 21pt)[느 스 기 가 · 흙 뿳 쀻 뺨 뺌 뾂 뼒 뼮]],
  [#eyebrow[+30 AUTO]], [#mixed("+30 auto", "wght 633", size: 21pt)[느 스 기 가 · 흙 뿳 쀻 뺨 뺌 뾂 뼒 뼮]],
  [#eyebrow[+32 AUTO]], [#mixed("+32 auto", "wght 633", size: 21pt)[느 스 기 가 · 흙 뿳 쀻 뺨 뺌 뾂 뼒 뼮]],
  [#eyebrow[+36 AUTO]], [#mixed("+36 auto", "wght 633", size: 21pt)[느 스 기 가 · 흙 뿳 쀻 뺨 뺌 뾂 뼒 뼮]],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#eyebrow[DISPLAY-SIZE MIXED RUNS]
#v(2mm)
#grid(
  columns: (22mm, 1fr),
  row-gutter: 3.2mm,
  [#text(size: 7pt, fill: gray)[+28 / 633]], [#mixed("+28 auto", "wght 633", size: 15pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#text(size: 7pt, fill: gray)[+30 / 633]], [#mixed("+30 auto", "wght 633", size: 15pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#text(size: 7pt, fill: gray)[+32 / 633]], [#mixed("+32 auto", "wght 633", size: 15pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
  [#text(size: 7pt, fill: gray)[+36 / 633]], [#mixed("+36 auto", "wght 633", size: 15pt)[자하연의 연구 기록 · Recovery kinetics 24 h]],
)

#v(7mm)
#eyebrow[TABULAR FIGURES]
#v(2mm)
#grid(
  columns: (22mm, 1fr),
  row-gutter: 2.5mm,
  [#text(size: 7pt, fill: gray)[BOLD]], [#text(size: 15pt, weight: 700)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
  [#text(size: 7pt, fill: gray)[+30 AUTO]], [#mixed("+30 auto", "wght 633", size: 15pt)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
  [#text(size: 7pt, fill: gray)[+32 AUTO]], [#mixed("+32 auto", "wght 633", size: 15pt)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
  [#text(size: 7pt, fill: gray)[+36 AUTO]], [#mixed("+36 auto", "wght 633", size: 15pt)[00 · 100 · 200 · 700 · 1000 · 31.20%]],
)

#pagebreak()

// Page 3 — method comparison
#title(
  [같은 offset, 다른 counter 처리],
  note: [auto는 현재 가족의 방식, retain은 속공간 보존을 지시하는 방식, CJK는 한글 전용 획 판정 방식입니다.],
)

#v(5mm)
#grid(
  columns: (24mm, 1fr),
  row-gutter: 4mm,
  [#eyebrow[+30 AUTO]], [#mixed("+30 auto", "wght 633", size: 23pt)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
  [#eyebrow[+30 RETAIN]], [#mixed("+30 retain", "wght 633", size: 23pt)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
  [#eyebrow[+30 CJK]], [#mixed("+30 cjk", "wght 633", size: 23pt)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
  [#eyebrow[+32 AUTO]], [#mixed("+32 auto", "wght 633", size: 23pt)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
  [#eyebrow[+32 RETAIN]], [#mixed("+32 retain", "wght 650", size: 23pt)[뺨 뺌 뺄 뽑 뼒 뼮 쀻 흙 괄]],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 6mm,
    [#eyebrow[AUTO +30] #v(1mm) #text(size: 8pt)[ink 1.440 · 00 50.4]],
    [#eyebrow[RETAIN +30] #v(1mm) #text(size: 8pt)[ink 1.493 · 00 50.4]],
    [#eyebrow[CJK +30] #v(1mm) #text(size: 8pt)[ink 1.440 · 00 78.3]],
  )
]

#v(7mm)
#eyebrow[SMALL DISPLAY THRESHOLD]
#v(2mm)
#grid(
  columns: (22mm, 1fr),
  row-gutter: 2.5mm,
  [#text(size: 7pt, fill: gray)[12 PT]], [#mixed("+30 retain", "wght 633", size: 12pt)[반복적 건조 스트레스와 회복 속도 · 뼒 뼮 뽑]],
  [#text(size: 7pt, fill: gray)[14 PT]], [#mixed("+30 retain", "wght 633", size: 14pt)[반복적 건조 스트레스와 회복 속도 · 뼒 뼮 뽑]],
  [#text(size: 7pt, fill: gray)[18 PT]], [#mixed("+30 retain", "wght 633", size: 18pt)[반복적 건조 스트레스와 회복 속도 · 뼒 뼮 뽑]],
  [#text(size: 7pt, fill: gray)[24 PT]], [#mixed("+30 retain", "wght 633", size: 24pt)[건조 스트레스 · 뼒 뼮 뽑]],
)

#pagebreak()

// Page 4 — exact raster evidence
#title(
  [Binary raster: counter와 획 접합],
  note: [FreeType grayscale를 128에서 이진화하고 nearest-neighbor로 6배 확대한 실제 픽셀입니다. 각 strip의 글자 순서는 뺄·뼒·뽑·뼮입니다.],
)

#v(4mm)
#grid(
  columns: (23mm, 1fr, 1fr, 1fr),
  column-gutter: 4mm,
  row-gutter: 4mm,
  [#eyebrow[FONT]], [#eyebrow[24 PPEM]], [#eyebrow[32 PPEM]], [#eyebrow[64 PPEM]],
  [#eyebrow[BOLD]],
  [#image(raster-dir + "/counter-bold-24.png", width: 100%)],
  [#image(raster-dir + "/counter-bold-32.png", width: 100%)],
  [#image(raster-dir + "/counter-bold-64.png", width: 100%)],
  [#eyebrow[+30 AUTO]],
  [#image(raster-dir + "/counter-n30-auto-24.png", width: 100%)],
  [#image(raster-dir + "/counter-n30-auto-32.png", width: 100%)],
  [#image(raster-dir + "/counter-n30-auto-64.png", width: 100%)],
  [#eyebrow[+30 RETAIN]],
  [#image(raster-dir + "/counter-n30-retain-24.png", width: 100%)],
  [#image(raster-dir + "/counter-n30-retain-32.png", width: 100%)],
  [#image(raster-dir + "/counter-n30-retain-64.png", width: 100%)],
  [#eyebrow[+32 AUTO]],
  [#image(raster-dir + "/counter-n32-auto-24.png", width: 100%)],
  [#image(raster-dir + "/counter-n32-auto-32.png", width: 100%)],
  [#image(raster-dir + "/counter-n32-auto-64.png", width: 100%)],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#eyebrow[64 PPEM FOREGROUND CONNECTIONS · 괄 레 발 빽 뺄 뺌 뼒 쀻 적]
#v(2.5mm)
#grid(
  columns: (23mm, 1fr),
  row-gutter: 3mm,
  [#eyebrow[BOLD]], [#image(raster-dir + "/merge-bold-64.png", width: 100%)],
  [#eyebrow[+30 AUTO]], [#image(raster-dir + "/merge-n30-auto-64.png", width: 100%)],
  [#eyebrow[+30 RETAIN]], [#image(raster-dir + "/merge-n30-retain-64.png", width: 100%)],
  [#eyebrow[+32 AUTO]], [#image(raster-dir + "/merge-n32-auto-64.png", width: 100%)],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, stroke: 0.5pt + rule)[
  #eyebrow[READING OF THE SIGNAL]
  #v(2mm)
  #text(size: 8.5pt)[
    64 ppem에서는 속공간 자체가 사라지지 않지만, 여러 독립 자모 획이 Bold보다 일찍
    맞닿습니다. 24–32 ppem의 일부 작은 counter는 한 픽셀 줄거나 합쳐집니다. ExtraBold를
    18 pt부터 쓸지, 24 pt 이상 display로 제한할지에 직접 영향을 주는 차이입니다.
  ]
]

#pagebreak()

// Page 5 — Latin and decision paths
#title(
  [Roboto 축과 최종 승격 결과],
  note: [라틴은 wght 633이 수치 gate를 단독 통과했고, 시각 검토는 +30 retain 조합을 전체 빌드로 승격했습니다.],
)

#v(5mm)
#grid(
  columns: (24mm, 1fr, 27mm),
  row-gutter: 3mm,
  [#eyebrow[LATIN]], [#eyebrow[HAMBURGEFONTS · minimum oxygen]], [#eyebrow[INK / REG]],
  [#eyebrow[W610]], [#text(font: latin-font("wght 610"), size: 17pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("wght 610").at("median_ratio"))]],
  [#eyebrow[W620]], [#text(font: latin-font("wght 620"), size: 17pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("wght 620").at("median_ratio"))]],
  [#eyebrow[W633]], [#text(font: latin-font("wght 633"), size: 17pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("wght 633").at("median_ratio"))]],
  [#eyebrow[W650]], [#text(font: latin-font("wght 650"), size: 17pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("wght 650").at("median_ratio"))]],
  [#eyebrow[W667]], [#text(font: latin-font("wght 667"), size: 17pt)[HAMBURGEFONTS minimum oxygen]], [#text(size: 8pt)[#ratio(latin("wght 667").at("median_ratio"))]],
)

#v(7mm)
#line(length: 100%, stroke: 0.5pt + rule)
#v(5mm)
#eyebrow[MIXED-SCRIPT FINALISTS]
#v(2mm)
#grid(
  columns: (27mm, 1fr),
  row-gutter: 4mm,
  [#eyebrow[+30 AUTO / 620]], [#mixed("+30 auto", "wght 620", size: 18pt)[자하연 Recovery 24 h · 31.20%]],
  [#eyebrow[+30 RETAIN / 633]], [#mixed("+30 retain", "wght 633", size: 18pt)[자하연 Recovery 24 h · 31.20%]],
  [#eyebrow[+32 AUTO / 633]], [#mixed("+32 auto", "wght 633", size: 18pt)[자하연 Recovery 24 h · 31.20%]],
  [#eyebrow[+32 RETAIN / 650]], [#mixed("+32 retain", "wght 650", size: 18pt)[자하연 Recovery 24 h · 31.20%]],
)

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[REVIEW DECISION]
  #v(2mm)
  #grid(
    columns: (25mm, 1fr),
    row-gutter: 2.5mm,
    [#eyebrow[A · +30 RETAIN]], [먹색 일치가 가장 좋고 counter가 식별성을 유지해 full-font 후보로 승인했습니다.],
    [#eyebrow[B · +32 AUTO]], [기존 제작법과 일관됩니다. 한글은 라틴보다 0.028 가볍고 획 접합은 더 많습니다.],
    [#eyebrow[C · CUSTOM]], [두 후보가 모두 과밀하면 획 방향별 증가량 또는 문제 자모의 counter 보호가 필요합니다.],
  )
]

#v(6mm)
#text(size: 8.5pt, fill: green)[
  Stage 1 결론: 자동 hard gate는 시각 검토를 요구했고, 확대 raster 검토 뒤
  +30 retain / 633을 ExtraBold 전체 빌드로 승격했습니다.
]
