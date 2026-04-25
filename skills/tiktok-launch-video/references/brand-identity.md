# Brand Identity Capture (shared reference)

How to make a launch video look like the user's brand instead of a generic stock template. Used by `/tiktok-launch-video`, `/reddit-launch-video`, and `/linkedin-launch-video`.

The goal: produce a `brand-kit.json` that the HyperFrames composition can consume as CSS variables — colors, type, voice cues. Don't ship a video with placeholder colors.

---

## Inputs (in priority order)

Try these in order — stop at the first one that yields a usable kit.

### 1. Brand kit file (preferred — zero ambiguity)

If the user has any of these in the repo, read them and skip discovery:

- `.agents/brand-kit.json` / `.claude/brand-kit.json`
- `tailwind.config.ts` / `tailwind.config.js` (look for a custom color namespace, e.g. `cogny: { ... }`)
- `src/index.css` / `src/globals.css` (look for `--primary`, `--background`, `--foreground` CSS custom properties)
- `design-tokens.json` / `tokens.json`

Map these to the kit schema (below). Don't ask the user; just confirm the result.

### 2. Site URL

If the user passed a URL (or there's one in `.agents/product-marketing-context.md`), extract the brand identity from it.

```bash
# Pull the homepage HTML and CSS
WebFetch <url>      # for the rendered page + meta
```

From the response, identify:

- **Background and foreground**: dominant body background and primary text color (look for `body { background: ... }` or computed style of `<body>`).
- **Primary / accent colors**: most-used button color, link color, or hero accent. Often surfaced as CSS variables `--primary`, `--accent`.
- **Font family**: the `font-family` declared on `body` or `html`. Strip system fallbacks; keep the first webfont.
- **Tone of voice**: read the hero headline and 2–3 body paragraphs. Note: serious/playful, technical/lay, first-person/third-person, short/long sentences.
- **Logo wordmark**: SVG / PNG. Optional — only embed if the user says yes (logos at scale read as "ad").

### 3. Interview the user

If neither of the above produces enough, ask:

1. Brand background color? (hex)
2. Brand text color? (hex)
3. Primary brand color (1 hex) and an accent if you have one?
4. Brand font family — sans, serif, mono, custom?
5. Voice in one sentence? ("Confident, technical, anti-jargon", "Warm, conversational, plain English", etc.)

Three colors and a font family are the minimum. Don't proceed without them.

---

## Brand kit schema

Save the result to `brand-kit.json` in the HyperFrames project root. The composition reads this via inlined CSS variables.

```json
{
  "name": "cogny",
  "site": "https://cogny.com",
  "colors": {
    "background": "#1f1d1d",
    "foreground": "#ede8e3",
    "primary":    "#b09acd",
    "accent":     "#c9badf",
    "muted":      "#9a9494",
    "card":       "#282525",
    "success":    "#7ec8a4",
    "warning":    "#d4a857"
  },
  "type": {
    "family":   "'JetBrains Mono', 'Fira Code', ui-monospace, monospace",
    "weight_display": 700,
    "weight_body":    500,
    "letter_spacing_display": "-0.02em"
  },
  "voice": {
    "register":   "technical, direct, anti-jargon",
    "person":     "first-person plural (we)",
    "do":         ["concrete numbers", "name the tradeoff", "name the tool"],
    "dont":       ["leverage", "unlock", "revolutionary", "next-gen"]
  },
  "logo": {
    "wordmark_url": null,
    "use_in_video": false
  }
}
```

---

## Wiring the kit into a HyperFrames composition

Inject the kit values as CSS variables at the top of `index.html`. This keeps the composition templates portable — same HTML, different brands.

```html
<style>
  :root {
    --bg:      #1f1d1d;
    --fg:      #ede8e3;
    --primary: #b09acd;
    --accent:  #c9badf;
    --muted:   #9a9494;
    --card:    #282525;
    --font-display: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
    --font-body:    var(--font-display);
  }
  body { background: var(--bg); color: var(--fg); font-family: var(--font-body); }
  .accent { color: var(--primary); }
  .muted  { color: var(--muted); }
  .card   { background: var(--card); }
</style>
```

**Important**: HyperFrames inlines fonts at compile-time, but only for fonts it can fetch. If the kit specifies a webfont, either:

1. Drop a `.woff2` into `assets/fonts/` and `@font-face` it (offline-safe), **or**
2. Use a CDN URL (Google Fonts, Bunny Fonts) — HyperFrames will inline it deterministically.

System / monospace fallbacks are always safe.

---

## Voice → composition mapping

Voice isn't just typography; it changes which beats you'd write. A quick map:

| Voice trait | Composition implication |
|-------------|-------------------------|
| Technical, anti-jargon (e.g. cogny, Linear, Vercel) | Lead with mechanism, name the stack, show real UI screenshots, no bullet-point benefits |
| Warm, plain-English (e.g. Mailchimp, Linktree) | Lead with the user feeling, illustrations or photos, friendly captions |
| Authoritative B2B (e.g. Snowflake, Workday) | Lead with the metric, third-person customer quotes, slow tweens |
| Playful / consumer (e.g. Duolingo, Notion-for-students) | Lead with the punchline, kinetic motion, emoji in captions |

Pick a voice trait *before* writing the script. Don't switch mid-video.

---

## Common mistakes

1. **Using LinkedIn blue / TikTok pink in the brand color slot** — that's the platform UI, not the brand. Buyers feel the dissonance.
2. **Webfont not embedded** — composition renders with system fallback, looks generic. Verify by opening the rendered MP4 and checking the type.
3. **Logos in every beat** — one logo lockup at the close (max), or none. Repeated logos read as "ad".
4. **Picking a brand color the platform overlay sits on** — TikTok's right rail is white text + drop shadow; if your accent is white, it disappears under the overlay.
