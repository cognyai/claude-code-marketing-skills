---
name: tiktok-launch-video
description: Produce a 9:16 TikTok-native launch video for a product, feature, or campaign using HyperFrames. Idiomatic TikTok pacing, burned-in captions, hook-in-1s structure. Optionally hand off to TikTok Ads to launch as a Spark/in-feed ad.
version: "1.0.0"
author: Cogny AI
platforms: [tiktok-ads, hyperframes]
user-invocable: true
argument-hint: "<product URL or short brief>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  - Edit
  # Optional handoff to TikTok Ads when the user wants to publish as an ad
  - mcp__cogny__tiktok_ads__*
---

# TikTok Launch Video

Produce a TikTok-native launch video using [HyperFrames](https://hyperframes.heygen.com) — programmatic HTML/CSS video, deterministic, agent-friendly.

This skill is opinionated: it forces the **TikTok grammar** (9:16, hook < 1s, burned-in captions, fast cuts, native text overlays) instead of porting a 16:9 landscape video to vertical.

## Usage

`/tiktok-launch-video https://example.com/launch` — pulls context from a launch page
`/tiktok-launch-video "we're shipping AI brand guardrails for marketers"` — short brief
`/tiktok-launch-video` — interview the user

## Prerequisites

Run once on this machine:

```bash
node --version            # ≥ 22
ffmpeg -version | head -1 # ≥ 6
```

If either fails, ask the user to install Node 22+ and FFmpeg before continuing.

## Steps

### 1. Gather product context

If `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`) exists, read it first. Otherwise:

- If a URL was passed, `WebFetch` the page and extract: product name, value prop, core benefit, target user, one concrete proof point (number, customer, before/after).
- If a brief was passed, use it. Ask only for what's missing from the **TikTok hook checklist** below.

**TikTok hook checklist** (what you actually need before you can write the script):

1. Who is the target viewer in 5 words? (e.g. "B2B marketers running paid ads")
2. What pattern interrupt opens the video? (POV, reveal, contrarian claim, demo flash, "wait for it")
3. What's the *one* claim or moment that makes someone stop scrolling?
4. What's the proof? (a number, a screenshot, a customer name, a before/after)
5. What's the CTA? (link in bio, comment a keyword, search the product, follow)

Don't proceed without all five. If you're guessing, ask.

### 1.5 Capture brand identity

Make this look like the user's brand, not a stock template. Ask for one of:

- A **site URL** (we'll extract colors / fonts / voice from the page)
- A **repo path** containing `tailwind.config.*` or `globals.css` with CSS variables
- An existing `brand-kit.json` (`.agents/brand-kit.json` / `.claude/brand-kit.json` / project root)
- Manual input: 3 hex colors (background, text, primary) + a font family + a one-sentence voice description

Produce a `brand-kit.json` with at minimum: `colors.background`, `colors.foreground`, `colors.primary`, `colors.accent`, `type.family`, `voice.register`. Save it to the HyperFrames project root.

For full schema, extraction patterns, and voice → composition mapping see [`references/brand-identity.md`](references/brand-identity.md).

The composition template reads these as CSS variables (`--bg`, `--fg`, `--primary`, `--accent`, `--font-display`) — so once the kit is wired, the same template renders on-brand for any user.

### 2. Pick the idiomatic format

Don't invent a format. Pick one of these — all are proven on TikTok and map cleanly to HyperFrames:

| Format | When to use | Structure |
|--------|-------------|-----------|
| **POV** | Relatable role-based pain | "POV: you're a [role]" → pain → punchline reveal of product |
| **Build-in-public** | Founder/early launches | "I built X in Y days because Z" → quick demo → result |
| **Contrarian take** | Strong opinion, category creation | "Everyone says X. They're wrong because Y" → demo |
| **Before / After** | Workflow improvement | "This used to take 4 hours" → cut → "Now it takes 30 seconds" |
| **List-tease** | Multi-feature reveal | "3 things [tool] does that no one talks about" → 1, 2, 3 → CTA |

Pick **one**. Confirm with the user before writing.

### 3. Write the script (TikTok grammar)

Write a beat sheet, not prose. Each beat is one card or moment. Constraints:

- **Total length**: 9–22 seconds. Default to **15s** unless the user explicitly wants longer.
- **Beat 1 (0.0–1.0s)**: Hook. Big text. No logo. No intro. The viewer must not swipe.
- **Beats 2–N**: ~1.0–2.5s each. Every beat earns its time or gets cut.
- **Final beat (last 1.5–2s)**: CTA. Concrete verb. Not "learn more" — "Search [name] on TikTok", "Comment WAITLIST", "Tap the link".
- **Captions**: Every spoken word is burned in as text. Max 6 words per caption card.
- **Voice / register**: First person, conversational, no marketing voice. Read it out loud — if it sounds like a press release, rewrite.

Hand the beat sheet back to the user and **wait for confirmation** before composing. One round of revisions is normal.

### 4. Scaffold the HyperFrames project

Use the CLI. Don't try to handcraft `package.json`.

```bash
# In the user's working directory, or a videos/ subdirectory if they prefer
npx -y hyperframes@latest init <product-slug>-tiktok --yes
cd <product-slug>-tiktok
```

This creates `index.html`, `meta.json`, `hyperframes.json`, plus `CLAUDE.md` / `AGENTS.md` with framework rules. Read `CLAUDE.md` once — it documents the `data-*` attribute conventions and the `window.__timelines` registration this skill depends on.

### 5. Compose the video (9:16, kinetic)

Edit `index.html` to be a 1080×1920 composition. The pattern below is the minimum viable TikTok-native composition — adapt the copy, keep the structure.

Key rules (these come from HyperFrames, do not skip):

- Every timed element needs `class="clip"` plus `data-start`, `data-duration`, `data-track-index`.
- The composition root has `data-composition-id`, `data-width`, `data-height`, `data-duration`.
- Animations go on a paused GSAP timeline registered as `window.__timelines["<composition-id>"]`.
- No `Date.now()`, no `Math.random()`, no `fetch()` — renders must be deterministic.

Reference composition: see [`references/composition-template.html`](references/composition-template.html).

A few TikTok-specific styling rules to follow:

- **Type**: 110–160px for hooks, 70–90px for body captions. Bold, tight letter-spacing.
- **Safe area**: keep the bottom 320px and top 220px clear — that's where TikTok's UI sits.
- **Color**: high contrast. Black background + white text + one accent (cyan, lime, or magenta). Avoid pastels.
- **Motion**: every card enters with a 0.25–0.4s `y` or `scale` tween. Cuts are hard, not crossfades.
- **No stock footage feel**: if the script calls for "demo", capture the actual product UI (`hyperframes capture <url>`) and crop into the 9:16 frame instead of using a generic stock clip.

### 6. Lint

```bash
npx hyperframes lint
```

Fix every error. Warnings are usually safe but read them.

### 7. Render

```bash
npx hyperframes render --output launch.mp4
```

A 15s composition typically renders in 30–90 seconds depending on the machine. Output is H.264 MP4, 1080×1920, 30fps.

### 8. Sanity-check before declaring done

Open the file, scrub through it once. Then check:

- Hook is fully visible by **0.8s**?
- Captions readable at the size they'll be viewed (phone, no sound)?
- Nothing important in the bottom 320px?
- CTA is on screen for ≥ 1.5s at the end?
- Total length between 9 and 22 seconds?

If any check fails, edit and re-render. Do not ship a video that fails any of the above.

### 9. (Optional) Hand off to TikTok Ads

If the user wants to run this as a paid in-feed ad (not an organic post), use the TikTok Ads MCP to set up the campaign skeleton. Don't auto-launch.

```
tiktok_ads__tool_list_advertisers
tiktok_ads__tool_get_pixels(advertiser_id)              # confirm tracking
tiktok_ads__tool_create_campaign(...)                   # objective: TRAFFIC or VIDEO_VIEWS, status: DISABLE
tiktok_ads__tool_create_ad_group(...)                   # placement: TIKTOK only; daily budget; status: DISABLE
# Upload the rendered MP4 manually in TikTok Ads Manager — the MCP doesn't currently
# upload creatives. Then:
tiktok_ads__tool_create_ad(...)                         # status: DISABLE
```

All entities should be created `DISABLE`. Print a summary and tell the user exactly which IDs to enable in TikTok Ads Manager once they've reviewed the creative.

For organic posting: just hand them `launch.mp4` and tell them to upload via the TikTok app (organic uploads are not API-supported).

## Output format

When you finish, print:

1. Path to the rendered MP4
2. The beat sheet you used (so the user can iterate)
3. One-line summary of length, format chosen, and aspect ratio
4. (If applicable) the TikTok Ads campaign / ad group / ad IDs created in DISABLE state

## Common mistakes

1. **16:9 footage stretched to 9:16** — re-shoot or use HyperFrames overlays. Don't stretch.
2. **Logo intro** — TikTok punishes anything that looks like a TV ad. The hook is the first frame.
3. **Voiceover with no captions** — 80%+ of TikTok is watched muted. Captions or it doesn't exist.
4. **Generic CTA** — "learn more" never works on TikTok. Tell the viewer the exact next action.
5. **Over-rendering** — 4K output makes no difference; TikTok recompresses to ~720p anyway.
6. **Putting the CTA only at the end** — half of viewers are gone by then. Restate the offer at ~60% of runtime too.

## Related

- `/reddit-launch-video` — same pattern for Reddit's idiomatic format
- `/linkedin-launch-video` — same pattern for LinkedIn
- `/video-to-gif` — convert the rendered MP4 into a feed-ready GIF
- `/ad-copy-writer` — generate the headline / caption that ships *with* the video
