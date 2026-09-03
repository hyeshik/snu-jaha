#!/usr/bin/env bash
set -euo pipefail

CHARIS_URL="https://software.sil.org/downloads/r/charis/Charis-7.000.zip"
CHARIS_SHA256="e3237b1303c5d31af8f59b1d1914886c5e873b77c71390e4742fb3bc1c187666"
OUTPUT_DIR="build/charis-comparison/source"
ARCHIVE="$OUTPUT_DIR/Charis-7.000.zip"

mkdir -p "$OUTPUT_DIR"

if [[ ! -f "$ARCHIVE" ]] || ! printf '%s  %s\n' "$CHARIS_SHA256" "$ARCHIVE" | sha256sum --check --status; then
    curl -fL --retry 3 --output "$ARCHIVE" "$CHARIS_URL"
fi
printf '%s  %s\n' "$CHARIS_SHA256" "$ARCHIVE" | sha256sum --check

unzip -j -o "$ARCHIVE" \
    Charis-7.000/Charis-Regular.ttf \
    Charis-7.000/OFL.txt \
    -d "$OUTPUT_DIR"

echo "Charis 7.000 Regular source is ready."
