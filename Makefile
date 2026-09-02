PYTHON ?= python3
FONTFORGE ?= fontforge
TYPST ?= typst

VERSION := 0.1.0
BUILD_DIR := build
DIST_DIR := dist
PROOF_DIR := proof
OUTPUT := $(DIST_DIR)/SNUJaha-Regular.otf
RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Regular.raw.otf
MEDIUM_OUTPUT := $(DIST_DIR)/SNUJaha-Medium.otf
MEDIUM_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Medium.raw.otf
SEMIBOLD_OUTPUT := $(DIST_DIR)/SNUJaha-SemiBold.otf
SEMIBOLD_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-SemiBold.raw.otf
BOLD_OUTPUT := $(DIST_DIR)/SNUJaha-Bold.otf
BOLD_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Bold.raw.otf
RIDI_MEDIUM_SOURCE := $(BUILD_DIR)/RIDIBatang-Medium-8.otf
RIDI_SEMIBOLD_SOURCE := $(BUILD_DIR)/RIDIBatang-SemiBold-16.otf
RIDI_BOLD_SOURCE := $(BUILD_DIR)/RIDIBatang-Bold-24.otf
ROBOTO_VARIABLE_SOURCE := sources/roboto-serif/RobotoSerif[GRAD,opsz,wdth,wght].ttf
ROBOTO_MEDIUM_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight467.ttf
ROBOTO_SEMIBOLD_SOURCE := $(BUILD_DIR)/RobotoSerif14pt-Weight533.ttf
SPECIMEN := $(PROOF_DIR)/SNUJaha-Regular-Specimen.pdf
MIXED_TEXT_PROOF := $(PROOF_DIR)/SNUJaha-Regular-Mixed-Text-Proof.pdf
BOLD_SPECIMEN := $(PROOF_DIR)/SNUJaha-Bold-Candidate-Specimen.pdf
WEIGHT_SPECIMEN := $(PROOF_DIR)/SNUJaha-Weight-Range-Specimen.pdf

.PHONY: all sources build medium-build semibold-build bold-build verify medium-verify semibold-verify bold-verify verify-all specimen bold-specimen weight-specimen mixed-text-proof test clean

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

verify:
	$(PYTHON) scripts/verify_font.py "$(OUTPUT)"

medium-verify:
	$(PYTHON) scripts/verify_font.py "$(MEDIUM_OUTPUT)"

semibold-verify:
	$(PYTHON) scripts/verify_font.py "$(SEMIBOLD_OUTPUT)"

bold-verify:
	$(PYTHON) scripts/verify_font.py "$(BOLD_OUTPUT)"

verify-all: verify medium-verify semibold-verify bold-verify

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

mixed-text-proof: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/mixed-text-proof.typ "$(MIXED_TEXT_PROOF)"

test:
	$(PYTHON) -m unittest discover -s tests

clean:
	rm -rf "$(BUILD_DIR)" "$(DIST_DIR)" "$(SPECIMEN)" "$(BOLD_SPECIMEN)" "$(WEIGHT_SPECIMEN)" "$(MIXED_TEXT_PROOF)" "$(PROOF_DIR)"/*.png
