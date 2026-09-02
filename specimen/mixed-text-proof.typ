#let ink = rgb("#182236")
#let accent = rgb("#174D7A")
#let green = rgb("#2B6D65")
#let gray = rgb("#657080")
#let rule = rgb("#D7DEE6")
#let wash = rgb("#F1F5F5")
#let paper = rgb("#FCFBF7")

#set page(
  paper: "a4",
  margin: (left: 18mm, right: 18mm, top: 17mm, bottom: 17mm),
  fill: paper,
  header: context align(right)[
    #text(size: 6.8pt, tracking: 0.08em, fill: gray)[
      SNU JAHA · MIXED-SCRIPT SCIENTIFIC READING PROOF
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.45pt + rule)
    #v(1.8mm)
    #grid(
      columns: (1fr, auto),
      text(size: 6.8pt, fill: gray)[synthetic manuscript · not experimental evidence],
      text(size: 7pt, fill: accent)[#counter(page).display("01")],
    )
  ],
)
#set text(font: "SNU Jaha", size: 9.25pt, lang: "ko", fill: ink)
#set par(justify: true, leading: 0.70em, first-line-indent: 1em)

#let section(number, ko, en) = block(above: 3.8mm, below: 3.4mm, breakable: false)[
  #line(length: 100%, stroke: 0.45pt + rule)
  #v(2mm)
  #grid(
    columns: (12mm, 1fr),
    text(size: 7.5pt, weight: 700, fill: accent)[#number],
    [
      #text(size: 14pt, weight: 700)[#ko]
      #h(2mm)
      #text(size: 8pt, tracking: 0.06em, fill: green)[#en]
    ],
  )
]

#let subsection(number, ko, en) = block(above: 2.5mm, below: 2.5mm, breakable: false)[
  #text(size: 9.5pt, weight: 700, fill: accent)[#number #h(1.5mm) #ko]
  #h(1.5mm)
  #text(size: 7.2pt, tracking: 0.04em, fill: gray)[#en]
]

#let stat(label, value) = box(
  inset: (x: 3mm, y: 1.8mm),
  radius: 1.2mm,
  fill: wash,
  [#text(size: 6.8pt, weight: 700, fill: green)[#label] #h(1.5mm) #text(size: 8.6pt)[#value]],
)

// Page 1 — title, abstract, introduction, methods
#align(center)[
  #text(size: 8pt, tracking: 0.14em, weight: 700, fill: accent)[RESEARCH ARTICLE / TYPOGRAPHIC SIMULATION]
  #v(4mm)
  #text(size: 20pt, weight: 700)[
    반복적 건조 스트레스가 식물의 회복 속도와
    전사체 반응에 미치는 영향
  ]
  #v(2mm)
  #text(size: 11pt, fill: green)[
    Repeated drought exposure alters recovery kinetics and transcriptomic response
  ]
  #v(4mm)
  #text(size: 8.5pt)[김자하 · Minseo Park · J. H. Lee · 관악 식물환경연구실]
  #v(1mm)
  #text(size: 7.5pt, fill: gray)[Correspondence: #raw("jaha.lab@example.edu") · Received 2 September 2026]
]

#v(5mm)
#box(width: 100%, inset: 5mm, radius: 1.5mm, fill: wash)[
  #set par(first-line-indent: 0em, leading: 0.65em)
  #text(size: 7.3pt, weight: 700, tracking: 0.12em, fill: accent)[ABSTRACT]
  #v(1.5mm)
  #text(size: 8.7pt)[
    식물이 짧은 건조를 반복해서 경험하면 이후의 수분 결핍에 더 빠르게 대응하는
    drought memory가 형성될 수 있다. 본 연구에서는 생육 21일째의 _Arabidopsis
    thaliana_ 48개체를 control, single-stress, repeated-stress의 세 집단으로 나누고,
    토양 volumetric water content를 31.2%에서 9.5%까지 낮춘 뒤 72 h 동안 회복을
    추적했다. 잎 온도, stomatal conductance, chlorophyll fluorescence, 상대수분함량과
    RNA abundance를 0, 2, 8, 24, 48, 72 h에 측정하였다. 반복 처리군은 재급수 8 h
    뒤 Fv/Fm이 0.781 ± 0.014로 회복되어 단회 처리군의 0.742 ± 0.021보다 높았다
    (Welch’s _t_ = 4.21, _p_ = 0.0006). RNA sequencing에서는 sample당 평균
    4.8 × 10⁶ reads를 확보했고, 612 genes가 false discovery rate 0.05에서 차등
    발현되었다. 특히 _RD29A_, _DREB2A_, _HSP70_의 early response가 2–8 h 구간에서
    강화되었다. These results suggest that repeated mild stress changes both
    physiological recovery and the timing of gene regulation rather than simply
    increasing response amplitude.
  ]
  #v(1.5mm)
  #text(size: 7.5pt, fill: gray)[Keywords: drought memory · recovery kinetics · RNA-seq · mixed-effects model · Arabidopsis]
]

#section("1", [서론], [INTRODUCTION])

수분 부족은 식물의 생장과 탄소 동화를 동시에 제한하는 주요 환경 요인이다. 잎의
water potential이 감소하면 guard cell의 turgor가 변하고, stomata가 닫히면서
CO₂ 유입량과 transpiration rate가 함께 감소한다. 짧은 스트레스가 끝난 뒤 토양
수분은 수 시간 안에 회복될 수 있지만, photosystem II efficiency와 biomass
accumulation은 같은 속도로 돌아오지 않는다. 따라서 “회복”을 하나의 종료 시점으로
정의하기보다 여러 생리 지표가 서로 다른 time constant를 갖는 동적 과정으로
분석할 필요가 있다.

최근 연구는 이전 스트레스의 흔적이 chromatin accessibility, metabolite pool,
protein phosphorylation에 남을 수 있다고 제안한다. 이른바 stress priming 또는
drought memory는 다음 스트레스에서 반응 개시 시간을 앞당기지만, 그 효과의 크기와
지속 시간은 처리 강도에 따라 크게 달라진다. 예를 들어 6 h의 mild dehydration은
방어 유전자 발현을 촉진할 수 있으나, leaf relative water content가 55% 아래로
떨어지는 severe treatment는 회복 이후에도 growth penalty를 남긴다. 기존 결과가
일관되지 않은 이유 중 하나는 sampling interval이 24 h 이상으로 넓어 초기
2–8 h의 변화를 놓쳤기 때문이다.

본 연구의 첫 번째 목적은 repeated mild drought가 재급수 뒤 생리 회복 곡선을
변화시키는지 검정하는 것이다. 두 번째 목적은 physiological phenotype과
transcript abundance 사이의 시간 지연을 정량화하는 것이다. 우리는 반복 처리군의
stomatal conductance가 더 빨리 회복되며, early-response genes의 peak time이
앞당겨질 것이라고 가정했다. 분석은 treatment × time interaction을 포함한
linear mixed-effects model로 수행했고, 개체와 growth tray를 random intercept로
두었다.

#section("2", [재료와 방법], [MATERIALS AND METHODS])

#subsection("2.1", [생육 조건과 건조 처리], [GROWTH CONDITIONS])

종자는 4°C 암조건에서 72 h 층적 처리한 뒤 peat:vermiculite = 3:1 기질에
파종하였다. 식물은 22.0 ± 0.6°C, relative humidity 58 ± 4%, 12 h light/12 h dark
조건에서 키웠다. 광량은 canopy 높이에서 180 µmol photons m⁻² s⁻¹였고, 각 pot에는
매일 09:00에 Hoagland solution 12 mL를 공급했다. 모든 측정은 zeitgeber time
ZT2–ZT6 사이에 수행해 circadian variation을 줄였다.

Control은 토양 수분을 30–33%로 유지했다. Single-stress는 day 21에 관수를
중단하여 30 h 뒤 9–11%에 도달하게 했고, repeated-stress는 day 14와 day 18에
각각 8 h의 mild drought를 경험한 뒤 day 21에 같은 최종 처리를 받았다. Pot
mass는 0.1 g 정밀도의 balance로 30 min마다 기록했고, target water content에
도달한 시점을 treatment time 0 h로 정의했다.

#pagebreak()

// Page 2 — methods and results
#section("2", [재료와 방법], [MATERIALS AND METHODS · CONTINUED])

#subsection("2.2", [생리 지표와 현미경 측정], [PHYSIOLOGY AND IMAGING])

Chlorophyll fluorescence는 20 min dark adaptation 후 imaging fluorometer로
측정하였다. Maximum quantum yield는 Fv/Fm = (Fm − F₀)/Fm으로 계산했고,
non-photochemical quenching은 NPQ = (Fm − Fm′)/Fm′로 산출했다. Gas exchange는
leaf chamber 6 cm², flow rate 500 µmol s⁻¹, reference CO₂ 420 µmol mol⁻¹에서
기록하였다. Stomatal conductance가 0.05 mol H₂O m⁻² s⁻¹ 아래인 측정은 chamber
leak test를 반복한 뒤 확정했다.

기공 크기는 abaxial epidermis의 confocal image에서 측정했다. 각 개체마다 5 fields,
field당 12–18 stomata를 segmentation하여 aperture width와 guard-cell length를
구했다. Pixel size는 0.162 µm였고, Gaussian blur sigma = 0.8 pixel을 적용한 뒤
adaptive threshold로 mask를 생성했다. 두 평가자 사이의 intraclass correlation은
ICC(2,1) = 0.93이었다.

#subsection("2.3", [RNA 추출과 정량], [RNA EXTRACTION AND SEQUENCING])

잎 80–100 mg을 liquid nitrogen에서 분쇄하고 total RNA를 column 방식으로
추출했다. RNA integrity number가 8.0 이상이고 A₂₆₀/A₂₈₀ ratio가 1.95–2.10인
시료만 library 제작에 사용했다. 각 reaction에는 RNA 500 ng을 넣었고, final
volume은 20 µL였다. Library concentration은 18.4–42.7 ng/µL 범위였으며 insert
size 중앙값은 312 bp였다. Sequencing은 paired-end 2 × 100 bp로 수행하였다.

Adapter trimming 뒤 Phred score < 20인 base를 제거했다. Reads는 reference genome
TAIR10에 정렬했고, uniquely mapped reads만 gene-level count에 포함했다. 낮은 발현의
영향을 줄이기 위해 전체 sample의 25% 이상에서 counts per million ≥ 1인 gene만
남겼다. Normalization은 trimmed mean of M-values를 사용했으며, differential
expression의 기준은 absolute log₂ fold change ≥ 0.7 및 adjusted _p_ < 0.05였다.

#subsection("2.4", [통계 분석], [STATISTICAL ANALYSIS])

연속형 변수는 mean ± standard deviation으로 표시했다. Time-series response는
restricted maximum likelihood로 추정한 mixed model로 분석했으며, denominator
degrees of freedom에는 Satterthwaite approximation을 적용했다. 다중 비교는
Benjamini–Hochberg procedure로 보정했다. Effect size는 Hedges’ _g_와 95% confidence
interval로 보고했고, 모든 검정은 two-sided였다. 분석 환경은 R 4.6.1과 Python
3.14였으며 random seed는 20260902로 고정했다.

#section("3", [결과], [RESULTS])

#subsection("3.1", [재급수 뒤 수분 상태의 회복], [WATER-STATUS RECOVERY])

처리 시작 시 세 집단의 토양 수분은 9.5–10.1%로 차이가 없었다 (_F_₂,₄₅ = 0.38,
_p_ = 0.687). 재급수 2 h 뒤 pot mass는 목표값의 97.6 ± 1.8%에 도달했지만, leaf
relative water content는 single-stress에서 71.4 ± 3.2%, repeated-stress에서
76.9 ± 2.8%로 달랐다. Treatment × time interaction은 유의했으며
(_F_₅,₂₁₀ = 6.82, _p_ < 0.0001), 가장 큰 차이는 8 h에서 관찰되었다.

회복 곡선을 RWC(t) = RWC_max − A·exp(−t/tau)로 적합했을 때 estimated time constant
tau는 repeated-stress 6.3 h, single-stress 10.8 h였다. 두 값의 bootstrap difference는
−4.5 h였고 95% CI는 [−6.9, −2.2]였다. Model fit은 각각 R² = 0.91과 0.87로,
단순한 exponential recovery가 초기 24 h 변화를 잘 설명했다.

#v(2.5mm)
#table(
  columns: (1.35fr, 0.85fr, 0.85fr, 0.85fr, 0.8fr),
  inset: (x: 2mm, y: 1.6mm),
  stroke: (x: none, y: 0.35pt + rule),
  align: (left, right, right, right, right),
  table.header(
    [#text(weight: 700)[Variable]],
    [#text(weight: 700)[Control]],
    [#text(weight: 700)[Single]],
    [#text(weight: 700)[Repeated]],
    [#text(weight: 700)[_p_]],
  ),
  [RWC at 8 h (%)], [88.1 ± 2.1], [80.3 ± 3.7], [86.9 ± 2.9], [0.0012],
  [Fv/Fm at 8 h], [0.806 ± 0.009], [0.742 ± 0.021], [0.781 ± 0.014], [0.0006],
  [Conductance (mol m⁻² s⁻¹)], [0.31 ± 0.04], [0.17 ± 0.05], [0.24 ± 0.04], [0.0031],
  [Leaf temperature (°C)], [22.8 ± 0.5], [25.1 ± 0.7], [24.0 ± 0.6], [0.0048],
)
#v(1.5mm)
#text(size: 7.2pt, fill: gray)[Table 1. 재급수 8 h 뒤의 생리 지표. 값은 mean ± SD, _n_ = 16 plants per treatment.]

#subsection("3.2", [기공 반응과 광합성 효율], [STOMATAL AND PHOTOCHEMICAL RESPONSE])

Repeated-stress의 stomatal aperture는 2 h에 2.84 ± 0.31 µm로 single-stress의
2.19 ± 0.28 µm보다 컸다 (_p_ = 0.002). Guard-cell length에는 차이가 없어
(_p_ = 0.41) 형태적 크기보다 opening dynamics가 달라졌음을 시사했다. 24 h 이후에는
두 처리군의 aperture가 3.10–3.25 µm로 수렴했다. Conductance recovery의 area under
the curve는 반복군에서 18.6% 높았으며 Hedges’ _g_ = 0.82였다.

Fv/Fm은 stress time 0 h에서 0.69까지 감소했다. Control은 전 기간 0.80–0.82를
유지했고, repeated-stress는 8 h부터 0.78을 넘었다. 반면 single-stress는 24 h가
되어야 0.79에 도달했다. NPQ peak는 두 처리군 모두 2 h에 나타났지만 반복군의
peak amplitude가 14.2% 낮아 excess energy dissipation 요구가 작았음을 보여주었다.

#pagebreak()

// Page 3 — transcriptome, discussion, conclusion
#set text(size: 8.8pt)
#set par(leading: 0.62em)
#section("3", [결과], [RESULTS · CONTINUED])

#subsection("3.3", [전사체 변화의 크기와 시간], [TRANSCRIPTOME TIMING])

Quality filtering 후 sample당 4.2–5.4 × 10⁶ reads가 남았고 mapping rate 중앙값은
94.7%였다. Principal component 1은 전체 variance의 38.2%를 설명하며 sampling
time을 분리했고, component 2는 16.5%를 설명하며 treatment를 구분했다. 2 h에서
repeated-stress와 single-stress의 centroid distance가 가장 컸고, 48 h 이후에는
두 집단이 control 방향으로 가까워졌다.

총 612 genes가 적어도 한 시점에서 differential expression 기준을 만족했다.
이 가운데 184 genes는 반복군에서만 유의했고, 96 genes는 두 처리군에서 방향은
같지만 peak time이 달랐다. _RD29A_ transcript는 repeated-stress에서 2 h에
6.1-fold 증가했고 single-stress에서는 8 h에 4.3-fold 증가했다. _DREB2A_와
_HSP70_도 각각 5.4 h와 3.8 h의 peak-time advance를 보였다. 반면 housekeeping
genes _ACT2_와 _UBQ10_의 coefficient of variation은 6.2% 이하로 안정적이었다.

Gene ontology enrichment에서는 response to water deprivation
(adjusted _p_ = 2.1 × 10⁻⁶), protein folding (_p_ = 4.8 × 10⁻⁴), regulation of
stomatal movement (_p_ = 0.003)이 상위 범주였다. Photosynthesis-related genes는
초기 2 h에 억제되었으나 24 h부터 baseline으로 복귀했다. Physiological recovery
index와 first principal component score의 상관은 Pearson _r_ = 0.71
(95% CI [0.55, 0.82])이었다.

#v(2mm)
#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  column-gutter: 2mm,
  stat("N", "48 plants"),
  stat("READS", "4.8 × 10⁶/sample"),
  stat("DEG", "612 genes"),
  stat("FDR", "< 0.05"),
)

#section("4", [토의], [DISCUSSION])

본 실험에서 반복적 mild drought는 최종 스트레스 직후의 손상 정도를 완전히
줄이지는 않았지만, 재급수 이후의 recovery rate를 높였다. 즉 priming의 효과는
stress tolerance 자체보다 recovery kinetics에서 더 명확했다. 이 구분은 endpoint
measurement만 사용했을 때 보이지 않는다. 72 h의 최종 Fv/Fm은 두 처리군에서
거의 같았지만, 2–24 h 구간의 trajectory와 integrated carbon-gain potential은
서로 달랐다.

Baseline이 달라진 원인은 적어도 두 층위에서 설명할 수 있다. 첫째, 반복 처리군은
기공을 더 빠르게 열어 leaf cooling과 CO₂ uptake를 회복했다. 둘째, chaperone과
dehydration-response genes의 발현 peak가 앞당겨져 damaged protein의 처리와
osmotic adjustment가 빨라졌을 가능성이 있다. 그러나 transcript abundance와
protein activity가 항상 비례하는 것은 아니므로, causality를 확정하려면 proteomics와
phosphorylation assay가 추가로 필요하다.

관찰된 4.5 h의 time-constant 차이는 통계적으로 명확했지만 생태적 의미는 환경에
따라 달라질 수 있다. Growth chamber의 vapor-pressure deficit는 1.1 ± 0.2 kPa로
안정적이었고 root volume도 320 mL pot에 제한됐다. Field condition에서는 토심,
풍속 0.2–3.0 m s⁻¹, midday temperature 18–34°C가 동시에 변하므로 같은 genotype도
다른 회복 곡선을 보일 수 있다. 특히 3회 이상의 stress cycle은 memory를 강화하기보다
cumulative damage를 만들 수 있다.

통계 모델에도 제한이 있다. 본 연구는 tray와 plant를 random effect로 포함했지만,
시간에 따른 residual correlation은 AR(1) 구조로 단순화했다. Alternative model인
Gaussian process는 leave-one-out error를 3.1% 줄였으나 parameter uncertainty가
커 해석에 사용하지 않았다. 또한 612개의 DEG 중 184개는 repeated-stress에서만
검출됐지만, 낮은 read depth 때문에 작은 fold change를 놓쳤을 가능성이 있다.

그럼에도 physiological data와 RNA-seq가 같은 시간축에서 일치했다는 점은 중요하다.
Cross-correlation analysis에서 transcriptome PC1이 conductance보다 3.2 h 먼저
변했고, lagged correlation은 _r_ = 0.78이었다. 이는 early transcriptional response가
subsequent stomatal recovery를 예측할 수 있음을 보여준다. Future work에서는
single-cell RNA sequencing과 guard-cell-specific reporter를 결합해 tissue-level
평균에 가려진 heterogeneity를 확인할 필요가 있다.

#section("5", [결론], [CONCLUSION])

반복적인 약한 건조 경험은 이후 스트레스의 최대 손상량보다 회복의 속도와 순서를
바꾸었다. Repeated-stress plants는 재급수 8 h 안에 water status, stomatal opening,
photochemical efficiency를 더 빠르게 회복했고, 주요 stress-response genes의
발현 peak도 3.8–5.4 h 앞당겨졌다. 따라서 drought memory를 평가할 때는 단일 시점의
fold change보다 시간 해상도가 높은 paired physiological and molecular measurement가
필요하다.

#v(3mm)
#box(width: 100%, inset: 4mm, radius: 1.3mm, fill: wash)[
  #set par(first-line-indent: 0em)
  #text(size: 7.4pt, weight: 700, fill: accent)[DATA AND CODE AVAILABILITY]
  #v(1mm)
  #text(size: 8.2pt)[
    이 문서는 SNU Jaha의 한글·라틴·숫자·기호 조합을 검토하기 위해 작성한 synthetic
    manuscript이며 실제 실험 결과가 아니다. Layout source와 font build는 local
    repository에 기록되어 있다. Example accession: GSE260902; analysis commit:
    7f3a21c; checksum: SHA-256 1ff92127…233d12c0.
  ]
]

#v(3mm)
#text(size: 7.3pt, weight: 700, tracking: 0.1em, fill: accent)[SELECTED REFERENCES]
#v(1mm)
#set par(first-line-indent: 0em, leading: 0.58em)
#text(size: 7.2pt, fill: gray)[
  1. Bruce TJA et al. Stressful “memories” of plants: evidence and possible mechanisms. _Plant Science_ 173, 603–608 (2007).  \
  2. Crisp PA et al. Reconsidering plant memory: intersections between stress recovery, RNA turnover, and epigenetics. _Science Advances_ 2, e1501340 (2016).  \
  3. Kim J-M et al. Acetate-mediated novel survival strategy against drought in plants. _Nature Plants_ 3, 17097 (2017).  \
  4. Fictional dataset for typographic evaluation only; values, accession, authors, and affiliations are synthetic.
]
