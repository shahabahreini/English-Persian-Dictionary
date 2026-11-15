#!/bin/sh
# Render the README images in pipeline/site/readme/*.html to docs/assets/readme/*.png (2x, transparent corners).
# Run from the repository root. Needs Google Chrome and internet access for the web fonts.
set -e
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
SRC=pipeline/site/readme
OUT=docs/assets/readme
mkdir -p "$OUT"
render() { # name width height
  "$CHROME" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --default-background-color=00000000 --virtual-time-budget=10000 \
    --window-size="$2,$3" --screenshot="$PWD/$OUT/$1.png" "file://$PWD/$SRC/$1.html" >/dev/null 2>&1
  echo "$OUT/$1.png"
}
render hero 1280 560
render stats 1280 150
render devices 1280 390
render entry 1280 470
render v31 1280 590
render sections 1280 500
