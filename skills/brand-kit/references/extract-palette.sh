#!/usr/bin/env bash
# Extract a brand palette from any image (logo, screenshot, brand asset).
# No external deps beyond FFmpeg, which the video skills already require.
#
# Usage:
#   ./extract-palette.sh <input.png> [N]
#
#   N = max colors to extract (default 6)
#
# Output: one hex code per line, sorted by palette frequency, deduped.

set -euo pipefail

IN="${1:?usage: $0 <input> [max_colors]}"
N="${2:-6}"

if [[ ! -f "$IN" ]]; then
  echo "error: file not found: $IN" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "error: ffmpeg not installed" >&2
  exit 1
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# 1. palettegen — quantizes the image down to up to 256 colors.
#    stats_mode=single = work on a single still frame.
ffmpeg -y -i "$IN" \
  -vf "palettegen=max_colors=${N}:reserve_transparent=0:stats_mode=single" \
  -frames:v 1 -update 1 "$TMPDIR/palette.png" 2>/dev/null

# 2. Re-encode the palette image as PPM so we can read raw RGB bytes
#    without a PNG decoder. PPM (P6) header is:
#       P6\n<W> <H>\n<MAX>\n
#    For palettegen's 16x16 output: "P6\n16 16\n255\n" = 13 bytes.
#    `tail -c +14` skips the header and leaves raw RGB triplets.
ffmpeg -y -i "$TMPDIR/palette.png" -c:v ppm -f image2 -update 1 - 2>/dev/null \
  | tail -c +14 \
  | xxd -c 3 -p \
  | awk '!seen[$0]++' \
  | head -n "$N" \
  | awk '{print "#" toupper($1)}'
