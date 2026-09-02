#!/usr/bin/env bash
set -euo pipefail

RIDIBATANG_URL="https://ridicorp.com/wp-content/themes/ridicorp/css/font/RIDIBatang.otf"
ROBOTO_SERIF_URL="https://github.com/googlefonts/roboto-serif/releases/download/v1.008/RobotoSerifFonts-v1.008.zip"
RIDIBATANG_SHA256="f13a49c0815d254ac15e392953a0b056613dec08ceb378e54eeed14c4fda9a54"
ROBOTO_SERIF_SHA256="366f437312f40a0039d6719e6493d64828a982ac2734f9618f4c07c8684b6984"

DOWNLOAD_DIR="sources/downloads"
RIDI_DIR="sources/ridibatang"
ROBOTO_DIR="sources/roboto-serif"
RIDI_ARCHIVE="$DOWNLOAD_DIR/RIDIBatang.otf"
ROBOTO_ARCHIVE="$DOWNLOAD_DIR/RobotoSerifFonts-v1.008.zip"

mkdir -p "$DOWNLOAD_DIR" "$RIDI_DIR" "$ROBOTO_DIR"

download() {
    local url="$1"
    local output="$2"
    local expected="$3"
    if [[ -f "$output" ]] && printf '%s  %s\n' "$expected" "$output" | sha256sum --check --status; then
        return
    fi
    curl -fL --retry 3 --output "$output" "$url"
    printf '%s  %s\n' "$expected" "$output" | sha256sum --check
}

download "$RIDIBATANG_URL" "$RIDI_ARCHIVE" "$RIDIBATANG_SHA256"
download "$ROBOTO_SERIF_URL" "$ROBOTO_ARCHIVE" "$ROBOTO_SERIF_SHA256"

cp "$RIDI_ARCHIVE" "$RIDI_DIR/RIDIBatang.otf"
unzip -j -o "$ROBOTO_ARCHIVE" \
    ttf/RobotoSerif14pt-Regular.ttf \
    ttf/RobotoSerif14pt-SemiBold.ttf \
    'variable/RobotoSerif\[GRAD,opsz,wdth,wght\].ttf' \
    -d "$ROBOTO_DIR"

echo "Sources are ready."
