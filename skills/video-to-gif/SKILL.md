---
name: video-to-gif
description: Convert an MP4 (e.g. a HyperFrames render or a screen recording) to a high-quality GIF using FFmpeg's two-pass palette method. Picks the right preset for the target surface — Slack/DMs/Twitter/email/Reddit/GitHub — so you don't ship a 40MB GIF to a 5MB inbox.
version: "1.0.0"
author: Cogny AI
platforms: [ffmpeg]
user-invocable: true
argument-hint: "<input.mp4> [target: slack|twitter|reddit|email|github|web]"
allowed-tools:
  - Bash
  - Read
  - Write
---

# Video to GIF

Convert a video (MP4, MOV, WebM) to a GIF that's **actually small** and **actually looks good** on the surface you're posting to. Pairs naturally with `/tiktok-launch-video`, `/reddit-launch-video`, and `/linkedin-launch-video` for sharing renders in places where MP4 isn't supported (Slack threads, X cards, GitHub READMEs, transactional emails).

GIF is a terrible video format — but it's everywhere, so we use FFmpeg's two-pass `palettegen` / `paletteuse` flow to make it look as good as the format allows.

## Usage

`/video-to-gif launch.mp4` — interactive, asks the target
`/video-to-gif launch.mp4 slack` — Slack-tuned
`/video-to-gif launch.mp4 reddit` — Reddit-comment-tuned
`/video-to-gif launch.mp4 github` — GitHub README–tuned
`/video-to-gif launch.mp4 twitter` — X / Twitter–tuned
`/video-to-gif launch.mp4 email` — transactional / newsletter–tuned

## Prerequisites

```bash
ffmpeg -version | head -1   # must exist
ffprobe -version | head -1
```

If FFmpeg isn't installed:

```bash
# macOS
brew install ffmpeg
# Debian/Ubuntu
sudo apt install ffmpeg
```

## Steps

### 1. Inspect the source

Run `ffprobe` to get the source's duration, dimensions, and frame rate. You need these to pick the right preset and to warn the user before producing something that won't fit.

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of default=noprint_wrappers=1 <input>
```

Capture: source width, source height, source duration (seconds), source fps.

### 2. Pick the preset

If the user passed a target, use the matching preset. Otherwise ask. Each preset is tuned to the surface's actual size limits and aesthetic norms:

| Preset | Width | FPS | Loop | Why |
|--------|------:|----:|------|-----|
| **slack** | 480 | 12 | yes | 50MB upload cap; threads scroll fast; readability > smoothness |
| **twitter** | 480 | 15 | yes | 15MB GIF cap; auto-converted to MP4 above the cap, kills the loop |
| **reddit** | 600 | 15 | yes | 100MB cap but image-host sidebar dies past 20MB |
| **github** | 720 | 15 | yes | 10MB README cap; over the cap GitHub silently drops the file |
| **email** | 480 | 10 | yes | 5MB Gmail clip threshold; many ESPs strip animation past 1MB |
| **web** | 800 | 18 | yes | Generic fallback for landing pages and product blogs |

**Rules of thumb:**

- If source is < 6 seconds, you can usually bump fps by ~3 without breaking the size budget.
- If source is > 12 seconds, drop fps by 2–3 and consider trimming.
- Never upscale — if source width is below the preset width, keep source width.
- Strip audio (GIF can't carry it) — saves a step and removes accidental noise from screen captures.

### 3. Two-pass palette render (this is the only correct way)

A single-pass GIF render produces banded, dithered, oversized garbage. The right approach is two passes:

1. Generate an optimal 256-color palette from the source.
2. Apply that palette with Floyd-Steinberg dithering.

The pipeline is FFmpeg's `palettegen` filter feeding `paletteuse`. Do it as a single command using filter splits:

```bash
ffmpeg -y -i "<input>" \
  -vf "fps=<FPS>,scale=<WIDTH>:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=floyd_steinberg" \
  -loop 0 \
  "<output.gif>"
```

Notes on the filter chain:

- `fps=<FPS>` first — so palette is generated from the actual frames you'll keep.
- `scale=<WIDTH>:-1` keeps aspect; `-1` rounds the height. Use `-2` for codecs that need even dimensions (not needed for GIF, but harmless).
- `flags=lanczos` is the best general-purpose downscaler.
- `stats_mode=diff` weights moving regions higher when picking palette colors — sharper text, cleaner UI, less banding.
- `dither=floyd_steinberg` is the best default. For UI / sharp edges with no gradients, try `dither=bayer:bayer_scale=3` instead — slightly larger files but no dither noise on flat colors.
- `-loop 0` = infinite loop. Use `-loop 1` to play once. (For Slack and Twitter, infinite loop is what users expect.)

### 4. Render and verify

Run the command. Then verify:

```bash
# Check the file size
ls -lh "<output.gif>"

# Check the GIF's actual dimensions and frame count
ffprobe -v error -count_frames -select_streams v:0 \
  -show_entries stream=width,height,nb_read_frames \
  -of default=noprint_wrappers=1 "<output.gif>"
```

If the file is larger than the preset's surface cap (see table above), do **one** of:

1. Drop FPS by 2–3 and re-render (best quality preserved).
2. Drop width by ~80px and re-render (text may get harder to read).
3. Trim the source first (`-ss <start> -t <duration>`) and re-render.

Don't mix all three — change one variable at a time so you know what helped.

### 5. (Optional) Trim before converting

If the source is long, trim *before* the palette pass — the palette will be more accurate and the file smaller.

```bash
# Take 8 seconds starting at 2.5s in
ffmpeg -y -ss 2.5 -t 8 -i "<input>" -c copy "<input>.trimmed.mp4"
# then run the two-pass palette command on .trimmed.mp4
```

`-ss` *before* `-i` is keyframe-fast but slightly imprecise. For frame-accurate trims, put `-ss` *after* `-i` (slower).

### 6. Hand the file back

Print:

1. Path to the output GIF
2. Final size on disk
3. Final dimensions and frame count
4. Surface cap status: "fits Slack (50MB) ✓" / "exceeds GitHub README cap (10MB), retry with fps=12 ✗"

## One-liners (for when the user knows what they want)

```bash
# Slack-tuned (480px / 12fps)
ffmpeg -y -i in.mp4 -vf "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=floyd_steinberg" -loop 0 out.gif

# Twitter-tuned (480px / 15fps)
ffmpeg -y -i in.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=floyd_steinberg" -loop 0 out.gif

# GitHub README-tuned (720px / 15fps)
ffmpeg -y -i in.mp4 -vf "fps=15,scale=720:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=floyd_steinberg" -loop 0 out.gif

# Email-tuned (480px / 10fps, single loop)
ffmpeg -y -i in.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=floyd_steinberg" -loop 0 out.gif
```

## Common mistakes

1. **Single-pass GIF render** — `ffmpeg -i in.mp4 out.gif` produces ugly, oversized output. Always use the palette pipeline.
2. **Upscaling** — never scale GIFs *up*; they go from "bad" to "extremely bad". Match or downscale only.
3. **High FPS for talking-head content** — anything above 18fps is wasted on a GIF; drop to 12–15fps and put the bytes into resolution instead.
4. **Including audio** — GIF can't carry it. If you need audio, the surface supports MP4 and you should ship MP4 instead.
5. **Long GIFs (> 15s)** — if you need 30+ seconds, you probably need MP4 or WebP, not GIF. Ask the user if a different format works.
6. **Sending a 40MB GIF to email** — most ESPs strip the animation past 1MB, leaving the recipient with a static first frame. Use the email preset or fall back to a static PNG hero with a link.

## Related

- `/tiktok-launch-video`, `/reddit-launch-video`, `/linkedin-launch-video` — produce the source MP4 this skill converts
- `/welcome-series`, `/winback-engine` — places where a small embedded GIF lifts engagement
