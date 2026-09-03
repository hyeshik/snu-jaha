PYTHON ?= python3
FONTFORGE ?= fontforge
TYPST ?= typst

VERSION := 0.1.0
BUILD_DIR := build
DIST_DIR := dist
PROOF_DIR := proof
OUTPUT := $(DIST_DIR)/SNUJaha-Regular.otf
RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Regular.raw.otf
THIN_OUTPUT := $(DIST_DIR)/SNUJaha-Thin.otf
THIN_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Thin.raw.otf
LIGHT_OUTPUT := $(DIST_DIR)/SNUJaha-Light.otf
LIGHT_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Light.raw.otf
MEDIUM_OUTPUT := $(DIST_DIR)/SNUJaha-Medium.otf
MEDIUM_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Medium.raw.otf
SEMIBOLD_OUTPUT := $(DIST_DIR)/SNUJaha-SemiBold.otf
SEMIBOLD_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-SemiBold.raw.otf
BOLD_OUTPUT := $(DIST_DIR)/SNUJaha-Bold.otf
BOLD_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Bold.raw.otf
EXTRABOLD_OUTPUT := $(DIST_DIR)/SNUJaha-ExtraBold.otf
EXTRABOLD_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-ExtraBold.raw.otf
RIDI_MEDIUM_SOURCE := $(BUILD_DIR)/RIDIBatang-Medium-8.otf
RIDI_SEMIBOLD_SOURCE := $(BUILD_DIR)/RIDIBatang-SemiBold-16.otf
RIDI_BOLD_SOURCE := $(BUILD_DIR)/RIDIBatang-Bold-24.otf
RIDI_EXTRABOLD_SOURCE := $(BUILD_DIR)/RIDIBatang-ExtraBold-30-retain.otf
RIDI_THIN_SOURCE := $(BUILD_DIR)/RIDIBatang-Thin-20.otf
RIDI_LIGHT_SOURCE := $(BUILD_DIR)/RIDIBatang-Light-6.otf
ROBOTO_VARIABLE_SOURCE := sources/roboto-serif/RobotoSerif[GRAD,opsz,wdth,wght].ttf
ROBOTO_THIN_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight200.ttf
ROBOTO_LIGHT_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight333.ttf
ROBOTO_MEDIUM_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight467.ttf
ROBOTO_SEMIBOLD_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight533.ttf
ROBOTO_EXTRABOLD_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight633.ttf
SPECIMEN := $(PROOF_DIR)/SNUJaha-Regular-Specimen.pdf
MIXED_TEXT_PROOF := $(PROOF_DIR)/SNUJaha-Regular-Mixed-Text-Proof.pdf
BOLD_SPECIMEN := $(PROOF_DIR)/SNUJaha-Bold-Candidate-Specimen.pdf
WEIGHT_SPECIMEN := $(PROOF_DIR)/SNUJaha-Weight-Range-Specimen.pdf
LIGHTWEIGHT_AUDIT_DIR := $(BUILD_DIR)/lightweight-audit
LIGHTWEIGHT_AUDIT := $(LIGHTWEIGHT_AUDIT_DIR)/audit.json
LIGHTWEIGHT_SPECIMEN := $(PROOF_DIR)/SNUJaha-Light-Thin-Microproof.pdf
FULL_WEIGHT_AUDIT := $(BUILD_DIR)/full-weight-audit.json
FULL_WEIGHT_SPECIMEN := $(PROOF_DIR)/SNUJaha-Full-Weight-Range-Specimen.pdf
EXTRABOLD_AUDIT_DIR := $(BUILD_DIR)/extrabold-audit
EXTRABOLD_AUDIT := $(EXTRABOLD_AUDIT_DIR)/audit.json
EXTRABOLD_SPECIMEN := $(PROOF_DIR)/SNUJaha-ExtraBold-Microproof.pdf
EXTRABOLD_FULL_AUDIT := $(BUILD_DIR)/extrabold-full-audit.json
SNU_APPENDARD_DIR ?= ../snu-appendard/dist/otf
SNU_EDGE_DIR ?= ../snu-edge/instance_otf
SNU_SPROUT_DIR ?= ../snu-sprout/instance_otf
FAMILY_COMPAT_DIR := $(BUILD_DIR)/snu-family-compatibility
FAMILY_COMPAT_AUDIT := $(FAMILY_COMPAT_DIR)/audit.json
FAMILY_COMPAT_RASTER_DIR := $(FAMILY_COMPAT_DIR)/rasters
FAMILY_COMPAT_SPECIMEN := $(PROOF_DIR)/SNU-Family-Compatibility-Specimen.pdf
APPENDARD_BLEND_DIR := $(BUILD_DIR)/appendard-blend
APPENDARD_BLEND_CANDIDATE_DIR := $(APPENDARD_BLEND_DIR)/candidates
APPENDARD_BLEND_RASTER_DIR := $(APPENDARD_BLEND_DIR)/rasters
APPENDARD_BLEND_REPORT := $(APPENDARD_BLEND_DIR)/report.json
APPENDARD_BALANCE_REPORT := $(APPENDARD_BLEND_DIR)/hangul-latin-balance-2to1.json
APPENDARD_BLEND_SPECIMEN := $(PROOF_DIR)/SNU-Appendard-Blend-Regular-Candidates.pdf
APPENDARD_RESTORE_DIR := $(BUILD_DIR)/appendard-size-restore
APPENDARD_RESTORE_CANDIDATE_DIR := $(APPENDARD_RESTORE_DIR)/candidates
APPENDARD_RESTORE_REPORT := $(APPENDARD_RESTORE_DIR)/report.json
APPENDARD_RESTORE_SPECIMEN := $(PROOF_DIR)/SNU-Appendard-2to1-Size-Restore-Review.pdf
SNU_APPENDARD_REGULAR := $(SNU_APPENDARD_DIR)/SNUAppendard-Regular.otf
SNU_EDGE_REGULAR := $(SNU_EDGE_DIR)/SNUEdge-Regular.otf
SNU_SPROUT_REGULAR := $(SNU_SPROUT_DIR)/SNUSprout-Regular.otf
NANUM_SQUARE_REGULAR ?= ../snu-edge/vendor/source/NaverNanumSquare/NanumFontSetup_OTF_SQUARE/NanumSquareR.otf
LINE_SEED_KR_REGULAR ?= ../snu-sprout/original/LINESeedKR-Rg.otf

.PHONY: all sources build thin-build light-build medium-build semibold-build bold-build extrabold-build full-build verify thin-verify light-verify medium-verify semibold-verify bold-verify extrabold-verify verify-all weight-range-audit extrabold-full-audit specimen bold-specimen weight-specimen lightweight-audit extrabold-audit family-specimen compatibility-specimen appendard-blend-specimen appendard-balance-audit appendard-size-restore-review mixed-text-proof test clean

all: specimen

sources:
	./scripts/download_sources.sh

build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang sources/ridibatang/RIDIBatang.otf \
		--roboto-serif sources/roboto-serif/RobotoSerif14pt-Regular.ttf \
		--output "$(RAW_OUTPUT)" \
		--style Regular
	$(PYTHON) scripts/finalize_font.py \
		--input "$(RAW_OUTPUT)" \
		--ridibatang sources/ridibatang/RIDIBatang.otf \
		--output "$(OUTPUT)" \
		--kern-scale 0.895 \
		--style Regular
	$(PYTHON) scripts/verify_font.py "$(OUTPUT)"

thin-build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py \
		--input '$(ROBOTO_VARIABLE_SOURCE)' \
		--output "$(ROBOTO_THIN_SOURCE)" \
		--weight 200
	$(FONTFORGE) -lang=py -script scripts/build_ridi_weight.py \
		--input sources/ridibatang/RIDIBatang.otf \
		--output "$(RIDI_THIN_SOURCE)" \
		--offset -20 \
		--figure-x-scale 1.046667
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang "$(RIDI_THIN_SOURCE)" \
		--roboto-serif "$(ROBOTO_THIN_SOURCE)" \
		--output "$(THIN_RAW_OUTPUT)" \
		--style Thin
	$(PYTHON) scripts/finalize_font.py \
		--input "$(THIN_RAW_OUTPUT)" \
		--ridibatang "$(RIDI_THIN_SOURCE)" \
		--output "$(THIN_OUTPUT)" \
		--kern-scale 0.895 \
		--style Thin
	$(PYTHON) scripts/verify_font.py "$(THIN_OUTPUT)"

light-build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py \
		--input '$(ROBOTO_VARIABLE_SOURCE)' \
		--output "$(ROBOTO_LIGHT_SOURCE)" \
		--weight 333.333
	$(FONTFORGE) -lang=py -script scripts/build_ridi_weight.py \
		--input sources/ridibatang/RIDIBatang.otf \
		--output "$(RIDI_LIGHT_SOURCE)" \
		--offset -6 \
		--figure-x-scale 1.014
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang "$(RIDI_LIGHT_SOURCE)" \
		--roboto-serif "$(ROBOTO_LIGHT_SOURCE)" \
		--output "$(LIGHT_RAW_OUTPUT)" \
		--style Light
	$(PYTHON) scripts/finalize_font.py \
		--input "$(LIGHT_RAW_OUTPUT)" \
		--ridibatang "$(RIDI_LIGHT_SOURCE)" \
		--output "$(LIGHT_OUTPUT)" \
		--kern-scale 0.895 \
		--style Light
	$(PYTHON) scripts/verify_font.py "$(LIGHT_OUTPUT)"

medium-build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py \
		--input '$(ROBOTO_VARIABLE_SOURCE)' \
		--output "$(ROBOTO_MEDIUM_SOURCE)" \
		--weight 466.667
	$(FONTFORGE) -lang=py -script scripts/build_ridi_weight.py \
		--input sources/ridibatang/RIDIBatang.otf \
		--output "$(RIDI_MEDIUM_SOURCE)" \
		--offset 8 \
		--figure-x-scale 0.981333
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang "$(RIDI_MEDIUM_SOURCE)" \
		--roboto-serif "$(ROBOTO_MEDIUM_SOURCE)" \
		--output "$(MEDIUM_RAW_OUTPUT)" \
		--style Medium
	$(PYTHON) scripts/finalize_font.py \
		--input "$(MEDIUM_RAW_OUTPUT)" \
		--ridibatang "$(RIDI_MEDIUM_SOURCE)" \
		--output "$(MEDIUM_OUTPUT)" \
		--kern-scale 0.895 \
		--style Medium
	$(PYTHON) scripts/verify_font.py "$(MEDIUM_OUTPUT)"

semibold-build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py \
		--input '$(ROBOTO_VARIABLE_SOURCE)' \
		--output "$(ROBOTO_SEMIBOLD_SOURCE)" \
		--weight 533.333
	$(FONTFORGE) -lang=py -script scripts/build_ridi_weight.py \
		--input sources/ridibatang/RIDIBatang.otf \
		--output "$(RIDI_SEMIBOLD_SOURCE)" \
		--offset 16 \
		--figure-x-scale 0.962667
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang "$(RIDI_SEMIBOLD_SOURCE)" \
		--roboto-serif "$(ROBOTO_SEMIBOLD_SOURCE)" \
		--output "$(SEMIBOLD_RAW_OUTPUT)" \
		--style SemiBold
	$(PYTHON) scripts/finalize_font.py \
		--input "$(SEMIBOLD_RAW_OUTPUT)" \
		--ridibatang "$(RIDI_SEMIBOLD_SOURCE)" \
		--output "$(SEMIBOLD_OUTPUT)" \
		--kern-scale 0.895 \
		--style SemiBold
	$(PYTHON) scripts/verify_font.py "$(SEMIBOLD_OUTPUT)"

bold-build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(FONTFORGE) -lang=py -script scripts/build_ridi_weight.py \
		--input sources/ridibatang/RIDIBatang.otf \
		--output "$(RIDI_BOLD_SOURCE)" \
		--offset 24 \
		--figure-x-scale 0.944
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang "$(RIDI_BOLD_SOURCE)" \
		--roboto-serif sources/roboto-serif/RobotoSerif14pt-SemiBold.ttf \
		--output "$(BOLD_RAW_OUTPUT)" \
		--style Bold
	$(PYTHON) scripts/finalize_font.py \
		--input "$(BOLD_RAW_OUTPUT)" \
		--ridibatang "$(RIDI_BOLD_SOURCE)" \
		--output "$(BOLD_OUTPUT)" \
		--kern-scale 0.895 \
		--style Bold
	$(PYTHON) scripts/verify_font.py "$(BOLD_OUTPUT)"

extrabold-build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py \
		--input '$(ROBOTO_VARIABLE_SOURCE)' \
		--output "$(ROBOTO_EXTRABOLD_SOURCE)" \
		--weight 633.333
	$(FONTFORGE) -lang=py -script scripts/build_ridi_weight.py \
		--input sources/ridibatang/RIDIBatang.otf \
		--output "$(RIDI_EXTRABOLD_SOURCE)" \
		--offset 30 \
		--counter retain \
		--figure-x-scale 0.93
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang "$(RIDI_EXTRABOLD_SOURCE)" \
		--roboto-serif "$(ROBOTO_EXTRABOLD_SOURCE)" \
		--output "$(EXTRABOLD_RAW_OUTPUT)" \
		--style ExtraBold
	$(PYTHON) scripts/finalize_font.py \
		--input "$(EXTRABOLD_RAW_OUTPUT)" \
		--ridibatang "$(RIDI_EXTRABOLD_SOURCE)" \
		--output "$(EXTRABOLD_OUTPUT)" \
		--kern-scale 0.895 \
		--style ExtraBold
	$(PYTHON) scripts/verify_font.py "$(EXTRABOLD_OUTPUT)"

full-build: thin-build light-build build medium-build semibold-build bold-build extrabold-build

verify:
	$(PYTHON) scripts/verify_font.py "$(OUTPUT)"

thin-verify:
	$(PYTHON) scripts/verify_font.py "$(THIN_OUTPUT)"

light-verify:
	$(PYTHON) scripts/verify_font.py "$(LIGHT_OUTPUT)"

medium-verify:
	$(PYTHON) scripts/verify_font.py "$(MEDIUM_OUTPUT)"

semibold-verify:
	$(PYTHON) scripts/verify_font.py "$(SEMIBOLD_OUTPUT)"

bold-verify:
	$(PYTHON) scripts/verify_font.py "$(BOLD_OUTPUT)"

extrabold-verify:
	$(PYTHON) scripts/verify_font.py "$(EXTRABOLD_OUTPUT)"

verify-all: thin-verify light-verify verify medium-verify semibold-verify bold-verify extrabold-verify

weight-range-audit: thin-build light-build build
	$(PYTHON) scripts/audit_weight_range.py \
		--thin "$(THIN_OUTPUT)" \
		--light "$(LIGHT_OUTPUT)" \
		--regular "$(OUTPUT)" \
		--output "$(FULL_WEIGHT_AUDIT)"

extrabold-full-audit: build bold-build extrabold-build
	$(PYTHON) scripts/audit_extrabold_full.py \
		--regular "$(OUTPUT)" \
		--bold "$(BOLD_OUTPUT)" \
		--extrabold "$(EXTRABOLD_OUTPUT)" \
		--output "$(EXTRABOLD_FULL_AUDIT)"

specimen: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		--font-path sources/ridibatang \
		--font-path sources/roboto-serif \
		specimen/specimen.typ "$(SPECIMEN)"

bold-specimen: build bold-build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/bold-proof.typ "$(BOLD_SPECIMEN)"

weight-specimen: build medium-build semibold-build bold-build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/weight-proof.typ "$(WEIGHT_SPECIMEN)"

lightweight-audit: build
	mkdir -p "$(LIGHTWEIGHT_AUDIT_DIR)" "$(PROOF_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W180.ttf" --weight 180
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W200.ttf" --weight 200
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W230.ttf" --weight 230
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W320.ttf" --weight 320
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W333.ttf" --weight 333.333
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W350.ttf" --weight 350
	$(FONTFORGE) -lang=py -script scripts/build_lightweight_microfonts.py \
		--ridibatang sources/ridibatang/RIDIBatang.otf \
		--latin-source 180="$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W180.ttf" \
		--latin-source 200="$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W200.ttf" \
		--latin-source 230="$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W230.ttf" \
		--latin-source 320="$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W320.ttf" \
		--latin-source 333="$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W333.ttf" \
		--latin-source 350="$(LIGHTWEIGHT_AUDIT_DIR)/Roboto-W350.ttf" \
		--output-dir "$(LIGHTWEIGHT_AUDIT_DIR)"
	$(PYTHON) scripts/audit_lightweight_candidates.py \
		--regular "$(OUTPUT)" \
		--candidate-dir "$(LIGHTWEIGHT_AUDIT_DIR)" \
		--output "$(LIGHTWEIGHT_AUDIT)"
	$(TYPST) compile \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(LIGHTWEIGHT_AUDIT_DIR)" \
		specimen/lightweight-microproof.typ "$(LIGHTWEIGHT_SPECIMEN)"

extrabold-audit: build bold-build
	mkdir -p "$(EXTRABOLD_AUDIT_DIR)" "$(PROOF_DIR)"
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(EXTRABOLD_AUDIT_DIR)/Roboto-W610.ttf" --weight 610
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(EXTRABOLD_AUDIT_DIR)/Roboto-W620.ttf" --weight 620
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(EXTRABOLD_AUDIT_DIR)/Roboto-W633.ttf" --weight 633.333
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(EXTRABOLD_AUDIT_DIR)/Roboto-W650.ttf" --weight 650
	$(PYTHON) scripts/instantiate_roboto_serif.py --input '$(ROBOTO_VARIABLE_SOURCE)' --output "$(EXTRABOLD_AUDIT_DIR)/Roboto-W667.ttf" --weight 666.667
	$(FONTFORGE) -lang=py -script scripts/build_extrabold_microfonts.py \
		--ridibatang sources/ridibatang/RIDIBatang.otf \
		--latin-source 610="$(EXTRABOLD_AUDIT_DIR)/Roboto-W610.ttf" \
		--latin-source 620="$(EXTRABOLD_AUDIT_DIR)/Roboto-W620.ttf" \
		--latin-source 633="$(EXTRABOLD_AUDIT_DIR)/Roboto-W633.ttf" \
		--latin-source 650="$(EXTRABOLD_AUDIT_DIR)/Roboto-W650.ttf" \
		--latin-source 667="$(EXTRABOLD_AUDIT_DIR)/Roboto-W667.ttf" \
		--output-dir "$(EXTRABOLD_AUDIT_DIR)"
	$(PYTHON) scripts/audit_extrabold_candidates.py \
		--regular "$(OUTPUT)" \
		--bold "$(BOLD_OUTPUT)" \
		--candidate-dir "$(EXTRABOLD_AUDIT_DIR)" \
		--output "$(EXTRABOLD_AUDIT)"
	$(PYTHON) scripts/render_extrabold_rasters.py \
		--bold "$(BOLD_OUTPUT)" \
		--candidate-dir "$(EXTRABOLD_AUDIT_DIR)" \
		--output-dir "$(EXTRABOLD_AUDIT_DIR)/rasters"
	$(TYPST) compile \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(EXTRABOLD_AUDIT_DIR)" \
		specimen/extrabold-microproof.typ "$(EXTRABOLD_SPECIMEN)"

family-specimen: full-build weight-range-audit extrabold-full-audit
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--root . \
		--font-path "$(DIST_DIR)" \
		specimen/full-weight-proof.typ "$(FULL_WEIGHT_SPECIMEN)"
	$(TYPST) compile --ppi 96 \
		--root . \
		--font-path "$(DIST_DIR)" \
		specimen/full-weight-proof.typ "$(PROOF_DIR)/SNUJaha-Full-Weight-Range-96-{p}.png"
	$(TYPST) compile --ppi 144 \
		--root . \
		--font-path "$(DIST_DIR)" \
		specimen/full-weight-proof.typ "$(PROOF_DIR)/SNUJaha-Full-Weight-Range-144-{p}.png"
	$(TYPST) compile --ppi 300 \
		--root . \
		--font-path "$(DIST_DIR)" \
		specimen/full-weight-proof.typ "$(PROOF_DIR)/SNUJaha-Full-Weight-Range-300-{p}.png"

compatibility-specimen: full-build
	mkdir -p "$(FAMILY_COMPAT_DIR)" "$(FAMILY_COMPAT_RASTER_DIR)" "$(PROOF_DIR)"
	$(PYTHON) scripts/audit_snu_family_compatibility.py \
		--jaha-dir "$(DIST_DIR)" \
		--appendard-dir "$(SNU_APPENDARD_DIR)" \
		--edge-dir "$(SNU_EDGE_DIR)" \
		--sprout-dir "$(SNU_SPROUT_DIR)" \
		--output "$(FAMILY_COMPAT_AUDIT)"
	$(PYTHON) scripts/render_snu_family_baselines.py \
		--jaha-dir "$(DIST_DIR)" \
		--appendard-dir "$(SNU_APPENDARD_DIR)" \
		--edge-dir "$(SNU_EDGE_DIR)" \
		--sprout-dir "$(SNU_SPROUT_DIR)" \
		--output-dir "$(FAMILY_COMPAT_RASTER_DIR)"
	$(TYPST) compile \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(SNU_APPENDARD_DIR)" \
		--font-path "$(SNU_EDGE_DIR)" \
		--font-path "$(SNU_SPROUT_DIR)" \
		specimen/snu-family-compatibility-proof.typ "$(FAMILY_COMPAT_SPECIMEN)"
	$(TYPST) compile --ppi 144 \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(SNU_APPENDARD_DIR)" \
		--font-path "$(SNU_EDGE_DIR)" \
		--font-path "$(SNU_SPROUT_DIR)" \
		specimen/snu-family-compatibility-proof.typ "$(PROOF_DIR)/SNU-Family-Compatibility-144-{p}.png"

appendard-blend-specimen: build
	mkdir -p "$(APPENDARD_BLEND_CANDIDATE_DIR)" "$(APPENDARD_BLEND_RASTER_DIR)" "$(PROOF_DIR)"
	$(PYTHON) scripts/build_appendard_fit_candidates.py \
		--jaha "$(OUTPUT)" \
		--edge "$(SNU_EDGE_REGULAR)" \
		--sprout "$(SNU_SPROUT_REGULAR)" \
		--appendard "$(SNU_APPENDARD_REGULAR)" \
		--output-dir "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		--report "$(APPENDARD_BLEND_REPORT)"
	$(PYTHON) scripts/render_appendard_fit_baselines.py \
		--jaha "$(OUTPUT)" \
		--edge "$(SNU_EDGE_REGULAR)" \
		--sprout "$(SNU_SPROUT_REGULAR)" \
		--appendard "$(SNU_APPENDARD_REGULAR)" \
		--candidate-dir "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		--output-dir "$(APPENDARD_BLEND_RASTER_DIR)"
	$(TYPST) compile \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(SNU_APPENDARD_DIR)" \
		--font-path "$(SNU_EDGE_DIR)" \
		--font-path "$(SNU_SPROUT_DIR)" \
		--font-path "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		specimen/appendard-fit-regular-proof.typ "$(APPENDARD_BLEND_SPECIMEN)"
	$(TYPST) compile --ppi 144 \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(SNU_APPENDARD_DIR)" \
		--font-path "$(SNU_EDGE_DIR)" \
		--font-path "$(SNU_SPROUT_DIR)" \
		--font-path "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		specimen/appendard-fit-regular-proof.typ "$(PROOF_DIR)/SNU-Appendard-Blend-Regular-144-{p}.png"

appendard-balance-audit: appendard-blend-specimen
	$(PYTHON) scripts/measure_hangul_latin_balance.py \
		--jaha-source sources/ridibatang/RIDIBatang.otf \
		--jaha "$(OUTPUT)" \
		--jaha-adjusted "$(APPENDARD_BLEND_CANDIDATE_DIR)/SNUJahaBlend-O2A1-Regular.otf" \
		--edge-source "$(NANUM_SQUARE_REGULAR)" \
		--edge "$(SNU_EDGE_REGULAR)" \
		--edge-adjusted "$(APPENDARD_BLEND_CANDIDATE_DIR)/SNUEdgeBlend-O2A1-Regular.otf" \
		--sprout-source "$(LINE_SEED_KR_REGULAR)" \
		--sprout "$(SNU_SPROUT_REGULAR)" \
		--sprout-adjusted "$(APPENDARD_BLEND_CANDIDATE_DIR)/SNUSproutBlend-O2A1-Regular.otf" \
		--output "$(APPENDARD_BALANCE_REPORT)"

appendard-size-restore-review: appendard-blend-specimen
	mkdir -p "$(APPENDARD_RESTORE_CANDIDATE_DIR)" "$(PROOF_DIR)"
	$(PYTHON) scripts/review_appendard_size_restore.py \
		--jaha "$(OUTPUT)" \
		--edge "$(SNU_EDGE_REGULAR)" \
		--blend-report "$(APPENDARD_BLEND_REPORT)" \
		--candidate-dir "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		--output-dir "$(APPENDARD_RESTORE_CANDIDATE_DIR)" \
		--report "$(APPENDARD_RESTORE_REPORT)"
	$(TYPST) compile \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(SNU_EDGE_DIR)" \
		--font-path "$(SNU_APPENDARD_DIR)" \
		--font-path "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		--font-path "$(APPENDARD_RESTORE_CANDIDATE_DIR)" \
		specimen/appendard-size-restore-review.typ "$(APPENDARD_RESTORE_SPECIMEN)"
	$(TYPST) compile --ppi 144 \
		--root . \
		--font-path "$(DIST_DIR)" \
		--font-path "$(SNU_EDGE_DIR)" \
		--font-path "$(SNU_APPENDARD_DIR)" \
		--font-path "$(APPENDARD_BLEND_CANDIDATE_DIR)" \
		--font-path "$(APPENDARD_RESTORE_CANDIDATE_DIR)" \
		specimen/appendard-size-restore-review.typ "$(PROOF_DIR)/SNU-Appendard-2to1-Size-Restore-144-{p}.png"

mixed-text-proof: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/mixed-text-proof.typ "$(MIXED_TEXT_PROOF)"

test:
	$(PYTHON) -m unittest discover -s tests

clean:
	rm -rf "$(BUILD_DIR)" "$(DIST_DIR)" "$(SPECIMEN)" "$(BOLD_SPECIMEN)" "$(WEIGHT_SPECIMEN)" "$(LIGHTWEIGHT_SPECIMEN)" "$(EXTRABOLD_SPECIMEN)" "$(FULL_WEIGHT_SPECIMEN)" "$(FAMILY_COMPAT_SPECIMEN)" "$(APPENDARD_BLEND_SPECIMEN)" "$(MIXED_TEXT_PROOF)" "$(PROOF_DIR)"/*.png
