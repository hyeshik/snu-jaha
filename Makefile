PYTHON ?= python3
FONTFORGE ?= fontforge
TYPST ?= typst

VERSION := 0.1.0
BUILD_DIR := build
DIST_DIR := dist
PROOF_DIR := proof
OUTPUT := $(DIST_DIR)/SNUJaha-Regular.otf
RAW_OUTPUT := $(BUILD_DIR)/SNUJaha-Regular.raw.otf
SPECIMEN := $(PROOF_DIR)/SNUJaha-Regular-Specimen.pdf
MIXED_TEXT_PROOF := $(PROOF_DIR)/SNUJaha-Regular-Mixed-Text-Proof.pdf

.PHONY: all sources build verify specimen mixed-text-proof test clean

all: specimen

sources:
	./scripts/download_sources.sh

build: sources
	mkdir -p "$(BUILD_DIR)" "$(DIST_DIR)"
	$(FONTFORGE) -lang=py -script scripts/build_jaha.py \
		--ridibatang sources/ridibatang/RIDIBatang.otf \
		--roboto-serif sources/roboto-serif/RobotoSerif14pt-Regular.ttf \
		--output "$(RAW_OUTPUT)"
	$(PYTHON) scripts/finalize_font.py \
		--input "$(RAW_OUTPUT)" \
		--ridibatang sources/ridibatang/RIDIBatang.otf \
		--output "$(OUTPUT)" \
		--kern-scale 0.895
	$(PYTHON) scripts/verify_font.py "$(OUTPUT)"

verify:
	$(PYTHON) scripts/verify_font.py "$(OUTPUT)"

specimen: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		--font-path sources/ridibatang \
		--font-path sources/roboto-serif \
		specimen/specimen.typ "$(SPECIMEN)"

mixed-text-proof: build
	mkdir -p "$(PROOF_DIR)"
	$(TYPST) compile \
		--font-path "$(DIST_DIR)" \
		specimen/mixed-text-proof.typ "$(MIXED_TEXT_PROOF)"

test:
	$(PYTHON) -m unittest discover -s tests

clean:
	rm -rf "$(BUILD_DIR)" "$(DIST_DIR)" "$(SPECIMEN)" "$(MIXED_TEXT_PROOF)" "$(PROOF_DIR)"/*.png
