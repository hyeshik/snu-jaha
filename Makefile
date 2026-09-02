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

.PHONY: all sources build thin-build light-build medium-build semibold-build bold-build extrabold-build full-build verify thin-verify light-verify medium-verify semibold-verify bold-verify extrabold-verify verify-all weight-range-audit extrabold-full-audit specimen bold-specimen weight-specimen lightweight-audit extrabold-audit family-specimen mixed-text-proof test clean

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

mixed-text-proof: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/mixed-text-proof.typ "$(MIXED_TEXT_PROOF)"

test:
	$(PYTHON) -m unittest discover -s tests

clean:
	rm -rf "$(BUILD_DIR)" "$(DIST_DIR)" "$(SPECIMEN)" "$(BOLD_SPECIMEN)" "$(WEIGHT_SPECIMEN)" "$(LIGHTWEIGHT_SPECIMEN)" "$(EXTRABOLD_SPECIMEN)" "$(FULL_WEIGHT_SPECIMEN)" "$(MIXED_TEXT_PROOF)" "$(PROOF_DIR)"/*.png
