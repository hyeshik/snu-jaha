#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
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
    #text(size: 6.6pt, tracking: 0.08em, fill: gray)[SNU JAHA · UPPER-WEIGHT MICROFONT REVIEW]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.6mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.6pt, fill: gray)[SELECTED +28/+36 · PREVIOUS +32/+44],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.2pt, lang: "ko", fill: ink)
#set par(leading: 0.76em)

#let eyebrow(body) = text(size: 6.8pt, weight: 700, tracking: 0.12em, fill: accent, body)
#let ratio(value) = str(calc.round(value * 1000) / 1000)
#let cjk(label) = audit.at("cjk").find(item => item.at("label") == label)
#let latin(label) = audit.at("latin").find(item => item.at("label") == label)
#let title(body, note: none) = block[
  #eyebrow[WEIGHT DEVELOPMENT / FOCUSED COMPARISON]
  #v(3.5mm)
  #text(size: 24pt, weight: 700, body)
  #if note != none [#v(1.8mm) #text(size: 8.2pt, fill: gray, note)]
  #v(4.5mm)
  #line(length: 100%, stroke: 0.55pt + rule)
]
#let cjk-row(label, note) = {
  let item = cjk(label)
  block(breakable: false)[
    #grid(
      columns: (35mm, 1fr, 31mm),
      column-gutter: 4mm,
      [#eyebrow[#label] #v(1mm) #text(size: 6.8pt, fill: gray)[#note]],
      [#text(font: item.at("family"), size: 20pt)[자하연 연구 · 뿔 뼒 뼮 뾂 흙]],
      [#text(size: 7.2pt)[coverage #ratio(item.at("raster_coverage_ratio")) #linebreak() gap #ratio(item.at("hangul_pair_spacing").at("minimum"))]],
    )
  ]
}
#let mixed-row(label, cjk-label, latin-label) = {
  let c = cjk(cjk-label)
  let l = latin(latin-label)
  block(breakable: false)[
    #grid(
      columns: (31mm, 1fr, 34mm),
      column-gutter: 4mm,
      [#eyebrow[#label] #v(1mm) #text(size: 6.7pt, fill: gray)[#cjk-label #linebreak() #latin-label]],
      [#text(font: (c.at("family"), l.at("family")), size: 18pt)[자하연 Research 24 h · 뿔 뼒 뼮]],
      [#text(size: 7.2pt)[CJK #ratio(c.at("raster_coverage_ratio")) #linebreak() Latin #ratio(l.at("raster_coverage_ratio")) #linebreak() Δ #ratio(calc.abs(c.at("raster_coverage_ratio") - l.at("raster_coverage_ratio")))]],
    )
  ]
}

#title(
  [SemiBold–Bold–ExtraBold 간격 다시 보기],
  note: [선택된 +28/+36 production과 이전 +32/+44 구성을 대표 glyph의 CJK coverage와 실제 형태로 비교합니다.],
)

#v(5mm)
#cjk-row("SemiBold +22 auto", [production control])
#v(5mm)
#cjk-row("Bold +28 retain", [selected production · 104%])
#v(5mm)
#cjk-row("Bold +32 retain", [previous production · 104%])
#v(5mm)
#cjk-row("ExtraBold +36 retain 104%", [new candidate · spacing reject])
#v(5mm)
#cjk-row("ExtraBold +36 retain 108%", [selected production · reviewed topology])
#v(5mm)
#cjk-row("ExtraBold +44 retain 108%", [previous production])

#v(7mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[READING]
  #v(2mm)
  #text(size: 8.7pt)[
    Coverage는 Regular 대비 128 ppem raster ink / advance입니다. 같은 +36 outline도
    108% cell에서는 문장 회색도가 낮아지고 글자 사이 공간이 늘어납니다.
  ]
]

#pagebreak()

#title(
  [혼합문장으로 보는 두 개의 완화안],
  note: [각 CJK 후보에 가장 가까운 Roboto Serif 구간을 배치했습니다. 수치는 최종 선택이 아니라 육안 비교를 위한 pairing입니다.],
)

#v(5mm)
#mixed-row([SEMIBOLD CONTROL], "SemiBold +22 auto", "SemiBold wght 565")
#v(5mm)
#mixed-row([BOLD SELECTED], "Bold +28 retain", "Bold wght 610")
#v(5mm)
#mixed-row([BOLD PREVIOUS], "Bold +32 retain", "Bold wght 645")
#v(5mm)
#mixed-row([EXTRA SELECTED], "ExtraBold +36 retain 108%", "ExtraBold wght 660")
#v(5mm)
#mixed-row([EXTRA +36 / 104], "ExtraBold +36 retain 104%", "ExtraBold wght 680")
#v(5mm)
#mixed-row([EXTRA PREVIOUS], "ExtraBold +44 retain 108%", "ExtraBold wght 725")

#v(8mm)
#line(length: 100%, stroke: 0.45pt + rule)
#v(5mm)
#eyebrow[SAME-SIZE LADDER / 24 PT]
#v(2mm)
#grid(
  columns: (25mm, 1fr),
  row-gutter: 3mm,
  [#eyebrow[600]], [#text(font: (cjk("SemiBold +22 auto").at("family"), latin("SemiBold wght 565").at("family")), size: 24pt)[자하연 Research]],
  [#eyebrow[700 SELECTED]], [#text(font: (cjk("Bold +28 retain").at("family"), latin("Bold wght 610").at("family")), size: 24pt)[자하연 Research]],
  [#eyebrow[800 SELECTED]], [#text(font: (cjk("ExtraBold +36 retain 108%").at("family"), latin("ExtraBold wght 660").at("family")), size: 24pt)[자하연 Research]],
  [#eyebrow[800 REJECT]], [#text(font: (cjk("ExtraBold +36 retain 104%").at("family"), latin("ExtraBold wght 680").at("family")), size: 24pt)[자하연 Research]],
)

#v(7mm)
#box(width: 100%, inset: 4.5mm, radius: 1.5mm, fill: wash)[
  #eyebrow[AUDIT FLAGS]
  #v(1.5mm)
  #text(size: 7.6pt)[
    +36 / 104%: minimum gap −11.1, non-positive spacing 887 / 6,400 → reject.\
    +36 / 108%: minimum gap +26.9. Microfont-stage 64 ppem flags in ‘뼮’ and ‘휇’ do not reproduce after the complete production transform.
  ]
]
