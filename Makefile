PYTHON ?= python3
FONTFORGE ?= fontforge
TYPST ?= typst

VERSION := 0.1.0
BUILD_DIR := build
DIST_DIR := dist
PROOF_DIR := proof
OUTPUT := $(DIST_DIR)/SNUJaha-Regular.otf
RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Regular.raw.otf
BOLD_OUTPUT := $(DIST_DIR)/SNUJaha-Bold.otf
BOLD_RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Bold.raw.otf
RIDI_BOLD_SOURCE := $(BUILD_DIR)/RIDIBatang-Bold-24.otf
SPECIMEN := $(PROOF_DIR)/SNUJaha-Regular-Specimen.pdf
MIXED_TEXT_PROOF := $(PROOF_DIR)/SNUJaha-Regular-Mixed-Text-Proof.pdf
BOLD_SPECIMEN := $(PROOF_DIR)/SNUJaha-Bold-Candidate-Specimen.pdf

.PHONY: all sources build bold-build verify bold-verify specimen bold-specimen mixed-text-proof test clean

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

bold-verify:
	$(PYTHON) scripts/verify_font.py "$(BOLD_OUTPUT)"

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

mixed-text-proof: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/mixed-text-proof.typ "$(MIXED_TEXT_PROOF)"

test:
	$(PYTHON) -m unittest discover -s tests

clean:
	rm -rf "$(BUILD_DIR)" "$(DIST_DIR)" "$(SPECIMEN)" "$(BOLD_SPECIMEN)" "$(MIXED_TEXT_PROOF)" "$(PROOF_DIR)"/*.png
