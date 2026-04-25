---
name: brand-kit
description: Build a portable brand-kit.json for the user's product — colors, typography, voice — that other skills (video, ad creative, landing page) can consume. Multiple discovery paths so it works whether the user has access to their site's source code or only a public URL or just a logo image.
version: "1.0.0"
author: Cogny AI
platforms: [hyperframes, ffmpeg]
user-invocable: true
argument-hint: "<site URL | repo path | logo path | nothing for interview>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  - Edit
  # Cogny MCP context tree — may already contain a documented brand kit / voice / palette
  - mcp__cogny__get_context_tree_overview
  - mcp__cogny__browse_context_tree
  - mcp__cogny__read_context_node
  - mcp__cogny__search_context
---

# Brand Kit

Build a `brand-kit.json` describing the user's product in a way other skills can consume — colors, type, voice, do/don't language, optional logo. Other Cogny skills (`/tiktok-launch-video`, `/reddit-launch-video`, `/linkedin-launch-video`, `/landing-page-review`, `/ad-copy-writer`) read this file when present.

The skill is built around the reality that **users don't always have access to their site's source code**. There are six paths to a kit, in priority order. Stop at the first one that yields enough.

## Usage

`/brand-kit https://example.com` — extract from a live site
`/brand-kit ~/git/our-site` — extract from a local repo (Tailwind / CSS vars)
`/brand-kit ~/Desktop/logo.png` — extract palette from a logo or screenshot
`/brand-kit ~/Desktop/homepage.png logo.png` — combine site screenshot + logo
`/brand-kit` — interview the user

## Output

A `brand-kit.json` written to (in priority order, whichever path makes sense for the user's setup):

1. `.agents/brand-kit.json` (if `.agents/` exists)
2. `.claude/brand-kit.json` (if `.claude/` exists)
3. `./brand-kit.json` (otherwise — current working directory)

Always print the path you wrote to so the user can move it.

## Schema

```json
{
  "name": "cogny",
  "site": "https://cogny.com",
  "logo": {
    "path": "./brand/logo-square.png",
    "use_in_video": false
  },
  "colors": {
    "background": "#1f1d1d",
    "foreground": "#ede8e3",
    "primary":    "#b09acd",
    "accent":     "#c9badf",
    "muted":      "#9a9494",
    "card":       "#282525",
    "fuchsia":    "#d4848a",
    "success":    "#7ec8a4",
    "amber":      "#d4a857"
  },
  "type": {
    "family":   "'JetBrains Mono', 'Fira Code', ui-monospace, monospace",
    "weight_display": 700,
    "weight_body":    500,
    "letter_spacing_display": "-0.02em"
  },
  "voice": {
    "register":   "technical, direct, anti-jargon, CLI-aesthetic",
    "person":     "first-person plural (we / your)",
    "do":         ["concrete numbers", "name the tradeoff", "name the tool"],
    "dont":       ["leverage", "unlock", "revolutionary", "next-gen"]
  },
  "source": "repo: ~/git/cogny/tailwind.config.ts + src/index.css",
  "captured_at": "2026-04-25"
}
```

Minimum viable kit: `colors.background`, `colors.foreground`, `colors.primary`, `type.family`, `voice.register`. Don't ship without all five.

---

## Path 0 — Cogny MCP context tree (cheapest, run first if connected)

**Use when**: the `cogny` MCP server is in `.mcp.json`. The user may have already documented their brand — voice, palette, tone — in their context tree, in which case scraping is redundant.

```
mcp__cogny__get_context_tree_overview              # see what's documented
mcp__cogny__search_context query="brand"           # palette, voice, tone, design tokens
mcp__cogny__search_context query="positioning"     # voice + register often live here
mcp__cogny__read_context_node node_id="…"
```

If the tree returns brand / palette / voice nodes, hydrate the kit from those values. Cross-check against Path 1 or 3 only if something looks stale or contradictory.

If the cogny MCP isn't connected, or the tree has nothing brand-related, fall through to Path 1.

## Path 1 — Repo with Tailwind / CSS variables (best signal)

**Use when**: the user has access to the site's source.

Look for, in order:

```bash
# Tailwind config — custom color namespaces
fd -t f 'tailwind\.config\.(ts|js|mjs|cjs)$' <repo>
# CSS custom properties (most modern stacks)
fd -t f '(globals|index|app|theme|variables)\.css$' <repo>
# Design tokens
fd -t f '(design-tokens|tokens|theme)\.json$' <repo>
```

When you find a Tailwind config, look for a custom color namespace (commonly the brand name, e.g. `cogny: {...}`):

```ts
// tailwind.config.ts (cogny example)
colors: {
  cogny: { dark: "#1f1d1d", purple: "#b09acd", secondary: "#7E69AB", light: "#c9badf" }
}
```

When you find a CSS file, grep for the canonical custom-property names:

```bash
grep -E '^\s*--(background|foreground|primary|accent|muted|card)' <css-file>
```

Map the values into the kit schema. If you find both `--primary` (HSL or hex) and a Tailwind namespace, prefer the Tailwind namespace — it's usually the explicit brand intent rather than a shadcn default.

Type detection in the same files:

```bash
grep -E "(font-family|fontFamily|--font-)" <repo>/src/**/*.{css,ts,tsx,js} 2>/dev/null | head
```

---

## Path 2 — Live site URL (works without source access)

**Use when**: the user only has a public URL.

Steps:

1. **Fetch the homepage** with `WebFetch <url>` and extract any inline `<style>` blocks and the head's stylesheet links.
2. **Fetch the main stylesheet** (the largest CSS link in the head, typically). `curl -sL <css-url> | head -c 200000` is enough — look for CSS custom properties (`--primary`, `--background`, etc.) and `@font-face` rules.
3. **Look for a manifest** at `/site.webmanifest`, `/manifest.json`, or `/manifest.webmanifest`. Manifests contain `theme_color`, `background_color`, and an icon list — gold for brand kits.
4. **Look for a favicon and a high-res logo**:
   ```bash
   curl -sL "<site>/favicon.ico" -o /tmp/favicon.ico
   curl -sL "<site>/apple-touch-icon.png" -o /tmp/touch.png
   # Or extract from <link rel="icon"> in the homepage HTML
   ```
   The largest PNG icon on the site (Apple touch icon, manifest icon) is the brand mark.
5. **Detect typography**: search the inline CSS for `font-family` declarations on `body`, `html`, or `h1`. If you see Google Fonts links in `<head>`, the family name is right there in the URL.

If the site ships a static frontend (Next.js, etc.), the bundled CSS often contains the same custom properties as the dev source — so you might still recover the full brand palette without repo access.

If you only get partial info (e.g. you got `theme_color` from the manifest but no full palette), proceed to Path 3 to fill in gaps from the logo / a screenshot.

---

## Path 3 — Logo or screenshot palette extraction (the fallback that always works)

**Use when**: the user uploads a logo image, a screenshot of their homepage, or a brand asset PNG/JPG.

The user usually has *some* image — a logo on Desktop, a slack avatar, a website screenshot. Extract a palette directly with FFmpeg:

```bash
# Generate a small palette image (max 6 distinct colors) from any image.
ffmpeg -y -i <input.png> \
  -vf "palettegen=max_colors=6:reserve_transparent=0:stats_mode=single" \
  -frames:v 1 -update 1 /tmp/_palette.png

# Read those palette colors back as hex. The PPM header is
#   P6\n<W> <H>\n255\n  → 13 bytes for the standard 16x16 palette.
ffmpeg -y -i /tmp/_palette.png -c:v ppm -f image2 -update 1 - 2>/dev/null \
  | tail -c +14 \
  | xxd -c 3 -p \
  | awk '!seen[$0]++' \
  | head -8 \
  | awk '{print "#" toupper($1)}'
```

Output for the cogny logo (gradient C on dark warm bg):

```
#1D1B1B   ← background
#5F4953   ← deep plum
#BB93B9   ← lavender (primary brand)
#CA8B9D   ← coral-pink
#D2858C   ← coral (accent)
```

**Mapping rules** — the palette is sorted by frequency, but the *role* assignment is yours to make:

- Darkest color → `colors.background` (if it covers >40% of pixels)
- Brightest non-white → `colors.foreground` (if there's no off-white, default `#fafafa`)
- Most saturated chroma → `colors.primary`
- Second most saturated → `colors.accent`

Eyeball the original image once and confirm — algorithmic role assignment gets it right ~70% of the time.

**For typography from a screenshot**: image-based font detection is unreliable. Either:

- Ask the user ("the headline font on this image is…?"), **or**
- Use a free tool like WhatTheFont or Fontspring Matcherator — show the user the URL, don't try to do it programmatically.

**Optional: semantic palette via node-vibrant** (one npm install, gives vibrant/muted/dark-vibrant/light-vibrant categories — more useful for primary/accent role mapping):

```bash
npm install -g node-vibrant
node -e "
  const Vibrant = require('node-vibrant');
  Vibrant.from(process.argv[1]).getPalette().then(p => {
    const out = {};
    for (const k of ['Vibrant','Muted','DarkVibrant','LightVibrant','DarkMuted','LightMuted']) {
      if (p[k]) out[k] = p[k].hex;
    }
    console.log(JSON.stringify(out, null, 2));
  });
" <input.png>
```

Use whichever is available. FFmpeg ships with the video skills already, so that's the default.

---

## Path 4 — Color picker / manual entry (always available)

**Use when**: nothing else worked, or the user wants to override the kit explicitly.

Ask, in this order, and accept partial answers:

1. Background hex? (the page background users see most)
2. Foreground hex? (body text color)
3. Primary brand hex? (the color a button or link uses)
4. Accent hex? (optional — if there's a second brand color)
5. Font family? ("a sans like Inter", "JetBrains Mono", etc. — best-effort, system fallbacks are fine)

Three colors and a font is enough to ship.

---

## Path 5 — Voice extraction (always run, regardless of color path)

Voice is the part of a brand kit that copy-paste tooling forgets. It changes which beats a video would write or which headlines an ad-copy skill would produce.

**Source for voice**: the homepage hero + 1–2 deeper pages (about, pricing, blog).

Steps:

1. Fetch the homepage hero text (h1, h2, the first paragraph after the hero CTA).
2. Fetch one deep page (`/about` or `/pricing` typically).
3. Read the copy and produce three fields:

```json
"voice": {
  "register": "<one-line description>",
  "do":   ["pattern 1", "pattern 2", "pattern 3"],
  "dont": ["banned word 1", "banned word 2"]
}
```

Examples (these are real, derived from each company's homepage):

| Brand | register | do | dont |
|-------|----------|----|------|
| cogny | "technical, direct, anti-jargon, CLI-aesthetic" | concrete numbers, name the tradeoff, name the tool | leverage, unlock, revolutionary, next-gen |
| Linear | "operator, opinionated, fast" | second-person, terse, build-mode language | enterprise, synergy, robust |
| Mailchimp | "warm, conversational, plain-English" | first-person, friendly contractions, clear CTAs | utilize, paradigm, leverage |

If you can't infer voice from the page (e.g. very thin homepage), ask the user for one sentence describing how they want to sound. Don't make it up.

---

## Steps (the actual flow)

1. **Detect what input the user gave you**:
   - URL → Path 2 → fall through to 3 / 5 if needed
   - Repo path → Path 1 → fall through to 5
   - Image path → Path 3 + ask for site URL or repo for voice (Path 5)
   - Nothing → Path 4 + ask if they have a logo to extract from

2. **Build the kit incrementally**. Print partial state after each step so the user can intervene:
   ```
   ◆ Brand kit (cogny)
   ✓ colors    bg=#1f1d1d  fg=#ede8e3  primary=#b09acd  accent=#c9badf
   ✓ type      JetBrains Mono / mono
   ◇ voice     pending — fetching /about for analysis…
   ```

3. **Show the user the result** before writing the file. They should approve color role assignments (background vs primary, etc.) — these are the high-leverage calls.

4. **Write `brand-kit.json`** to the most appropriate location (see Output section). If a kit already exists, diff it and ask before overwriting.

5. **Print a one-line install hint** for the consumer skills:
   ```
   Saved → .agents/brand-kit.json
   Used by: /tiktok-launch-video, /reddit-launch-video, /linkedin-launch-video,
            /ad-copy-writer, /landing-page-review
   ```

## Common mistakes

1. **Treating a single hex color as the brand** — most brands have a primary + an accent + a background-foreground pair. Three colors minimum.
2. **Shipping without voice** — colors carry brand 30%; voice carries it 70%. Don't skip Path 5.
3. **Using shadcn defaults as the brand** — if the user's CSS file has the literal shadcn `--primary: 240 5.9% 10%`, that's a placeholder not a brand. Cross-check with the homepage screenshot.
4. **Over-saturating the kit with logo gradient artifacts** — palette extraction from a gradient logo will return 4–5 transitional colors. Pick the endpoints (primary + accent), drop the in-betweens.
5. **Letting LinkedIn-blue / Twitter-blue / TikTok-pink slip into the kit** — those are platform UI colors that bleed into screenshots, not brand colors.
6. **Trusting `theme-color` blindly** — sites sometimes set `theme-color` to match the address bar of mobile Safari, which is decorative and may not match the actual brand primary.

## Related

- `/tiktok-launch-video`, `/reddit-launch-video`, `/linkedin-launch-video` — consume the kit
- `/ad-copy-writer` — uses voice rules to write platform-appropriate copy
- `/landing-page-review` — checks consistency between a landing page and the brand kit
- `/non-commodity-content` — voice extraction overlaps with this skill's interview step
