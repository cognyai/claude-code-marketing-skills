---
name: linkedin-launch-video
description: Produce a LinkedIn-native 1:1 (or 16:9) launch video using HyperFrames. Caption-first, sound-off, B2B register, anti-corporate-jargon. Optionally hand off to LinkedIn Ads to launch as a sponsored content campaign with ICP-aligned targeting.
version: "1.1.1"
author: Cogny AI
platforms: [linkedin-ads, linkedin-organic, x-organic, hyperframes]
user-invocable: true
argument-hint: "<product URL or short brief>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  - Edit
  # Cogny MCP context tree — richer product context than public scraping
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__get_context_tree_overview
  - mcp__cogny__browse_context_tree
  - mcp__cogny__read_context_node
  - mcp__cogny__search_context
  # Optional handoff (read tools only; create/upload/post tools ask first)
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_targeting_facets
  - mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_audience_counts
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_organizations
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_organization_posts
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_post_statistics
---

# LinkedIn Launch Video

Produce a LinkedIn-native launch video using [HyperFrames](https://hyperframes.heygen.com).

LinkedIn's autoplay is muted, the feed is scrolled in 2-second chunks, and the audience is allergic to either extreme — too corporate (sounds like a 2010 SaaS press release) or too TikTok (looks unprofessional in front of buyers). This skill targets the middle: caption-driven, conversational founder/operator voice, real numbers, no jargon.

## Usage

`/linkedin-launch-video https://example.com/launch` — pulls context from a launch page
`/linkedin-launch-video "we're shipping inbound CRM scoring for B2B sales teams"` — short brief
`/linkedin-launch-video` — interview the user

## Works with

Making the video needs no accounts. Publishing is optional, and every publish call asks first.

| Job | Primary | Also answers it | What differs |
|-----|---------|-----------------|--------------|
| Run as sponsored content | LinkedIn Ads | — | Created `PAUSED`; the creative is a `DRAFT` until the user activates it |
| Post organically | LinkedIn Organic (company Page) | X Organic | Personal profiles still out-reach Pages; X takes the same MP4 (≤ 512 MB) |
| What past video posts did (optional) | LinkedIn Organic `tool_get_organization_posts` + `tool_get_post_statistics` | — | Use to pick length and hook style before scripting |

## Prerequisites

```bash
node --version            # ≥ 22
ffmpeg -version | head -1 # ≥ 6
```

## Steps

### 1. Gather product context AND ICP context

LinkedIn videos die when the audience is "everyone". They work when the first frame names the role.

Try sources in order:

**1a. Local file** — `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md`.

**1b. Cogny MCP context tree** — if the `cogny` MCP server is connected:

```
mcp__cogny__get_context_tree_overview
mcp__cogny__search_context query="ICP" / query="<product>"
mcp__cogny__read_context_node node_id="…"
```

The tree usually contains the actual ICP definition (role, seniority, industry, ARR band) and the most-recent shipped feature — both load-bearing for LinkedIn-grade specificity. Check it before public scraping.

**1c. Public web** — `WebFetch` the URL only if 1a/1b are empty.

Then ask:

1. Who is this for, by **role and seniority**? ("Heads of Demand Gen at B2B SaaS, $5–50M ARR")
2. What is the *expensive* problem they have right now? (cost, time, headcount)
3. What's the proof point — a customer name, a metric, a screenshot, a benchmark?
4. Who is the on-screen voice? (Founder? Operator? Customer? No-face / text-only is also valid on LinkedIn.)
5. What's the conversion goal? (Signup, demo, follow, comment, reshare)

If the role / proof / goal are vague, push back before writing. LinkedIn ROI lives or dies on these three.

### 1.5 Capture brand identity

Make this look like the user's brand. LinkedIn's audience is buyers — generic stock styling reads as "untrusted vendor".

Ask for one of: site URL, repo path with `tailwind.config.*` / CSS variables, an existing `brand-kit.json`, or manual input (3 hex + font + voice). Save the result as `brand-kit.json` in the HyperFrames project root.

For full schema, extraction patterns, and voice → composition mapping see [`references/brand-identity.md`](references/brand-identity.md).

LinkedIn-specific brand notes:

- **Avoid LinkedIn blue (#0a66c2)** as the brand accent — it merges with the platform UI and the video reads as a chrome screenshot.
- **Avoid the same accent the platform overlays use** — LinkedIn places white profile names with drop shadow on the top-15%; ensure your accent reads under that.
- **Display fonts are fine here** (unlike Reddit) — LinkedIn is the channel where serif headlines and editorial typography land best.

The composition template reads `--bg`, `--fg`, `--primary`, `--accent`, `--font-display` as CSS variables — wire them from your kit and the template's structure stays.

### 2. Pick the format

LinkedIn-idiomatic video formats that work in 2025–2026:

| Format | When to use | Structure |
|--------|-------------|-----------|
| **Founder-to-camera** | Authentic launches | Founder face + burned-in captions; explain the why, the how, the proof |
| **Numbers carousel** | Data-led launches | Stat → context → stat → context → stat → "want the breakdown? comment X" |
| **Customer quote** | Mid/late-stage social proof | Real screenshot of customer message → product clip → CTA |
| **"Here's what we shipped"** | Feature releases | Plain title → 3 short clips with captions → release-notes-style CTA |
| **Anti-pattern teardown** | Thought leadership / category creation | "Most teams do X. It doesn't work because Y. Here's what we built instead." |

Pick **one**. Confirm with the user.

### 3. Write the script (LinkedIn grammar)

- **Total length**: 30–75 seconds. The sweet spot is **45s**. Anything over 90s gets clipped.
- **Hook (0–3s)**: name the role, name the problem. "If you run paid for a B2B SaaS, this 30-second clip is for you."
- **Captions are the script**. LinkedIn auto-captions exist but are sloppy — burn your own in, max 8 words per card, sentence case, no all-caps.
- **No music**, or extremely subtle ambient. Voiceover optional but captions are the source of truth.
- **No "thrilled to announce"**, no "game-changer", no "next-generation". Read it out loud — if it sounds like a press release, rewrite.
- **Concrete CTA**: "Comment WAITLIST", "Tap the link to try it", "DM me 'demo'", or "Follow [name] for more". "Learn more" is dead.

Hand the beat sheet back. **Wait for confirmation.**

### 4. Scaffold the HyperFrames project

```bash
npx -y hyperframes@latest init <product-slug>-linkedin --non-interactive --resolution square
cd <product-slug>-linkedin
```

Use `--resolution landscape` instead for the 16:9 variant (step 5). There is no `--yes` flag; `--non-interactive` is what disables the prompts.

### 5. Compose the video (1:1 default, 16:9 alternative)

LinkedIn's feed is dominated by **square (1:1)**. 16:9 plays but takes ~25% less vertical space, hurting scroll-stop rate. 9:16 is supported but rarely the right call unless the asset will be repurposed for IG Reels later.

Default to **1080×1080 (1:1)**. Use 1920×1080 (16:9) only if the user is also embedding on a website / running in YouTube pre-roll.

Reference composition: see [`references/composition-template.html`](references/composition-template.html).

LinkedIn-specific styling rules:

- **Type**: 56–84px. Bigger than Reddit (because of LinkedIn's tighter line-height in feed), smaller than TikTok.
- **Color**: a single brand accent over white or off-white. Avoid LinkedIn-blue itself — feels like the platform UI bled in. Black/white with one warm accent reads as confident and not-stock.
- **Motion**: deliberate. 0.4–0.6s tweens, no bounce, no flashy easing. Buyers read this as "competent".
- **Caption block**: pin captions to the bottom 25% with a faint scrim if there's any background imagery. Top 15% should remain clean — that's where LinkedIn overlays profile name on autoplay previews.
- **Numbers > adjectives**: every claim needs a number. If you can't put a number on a card, cut the card.

### 6. Lint & render

Check dependencies first:

```bash
npx hyperframes doctor
```

If it reports FFmpeg missing, stop before rendering and tell the user to install it (`brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Debian/Ubuntu). Meanwhile, `npx hyperframes snapshot` captures key frames as PNGs without FFmpeg, so they can review the cards.

```bash
npx hyperframes lint
npx hyperframes render --output launch.mp4
```

### 7. Sanity check

- First card names the role *or* the problem within 3 seconds?
- Every claim has a number?
- Captions readable on a phone with sound off?
- No buzzwords (excited, thrilled, revolutionary, game-changing, leverage, synergy, unlock, supercharge, next-gen)?
- Length 30–75s?

If any check fails, edit and re-render.

### 8. (Optional) Hand off to LinkedIn Ads

If the user wants to run this as paid sponsored content, LinkedIn's edge is **B2B targeting precision**. Use it.

The MCP needs the video at a public URL. On Cloud, call `mcp__cogny__mcp__cogny-image-gen__tool_request_upload_url` and run the returned curl to get a `public_url` (asks first); otherwise ask the user for a hosted link. Then, after the user approves each write:

```
mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts                       # note the currency
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:industries", query: "<industry>")
mcp__cogny__mcp__LinkedIn_Ads__tool_get_audience_counts(ad_account_id, targeting_criteria: {...})   # confirm reach before launch

mcp__cogny__mcp__LinkedIn_Ads__tool_create_campaign_group(ad_account_id, name, status: "PAUSED")
mcp__cogny__mcp__LinkedIn_Ads__tool_create_campaign(
  ad_account_id, campaign_group_id, name,
  objective_type: "VIDEO_VIEW" | "WEBSITE_VISIT" | "LEAD_GENERATION",
  daily_budget_amount: "<amount the user stated>", daily_budget_currency: "<account currency>",
  targeting_criteria: {...}, status: "PAUSED"
)
mcp__cogny__mcp__LinkedIn_Ads__tool_upload_video(ad_account_id, video_url: "<public MP4 URL, ≤ 200 MB>", owner_urn: "urn:li:organization:<page id>")
mcp__cogny__mcp__LinkedIn_Ads__tool_create_creative(
  ad_account_id, campaign_id, author_organization_urn: "urn:li:organization:<page id>",
  commentary, image_urn: "<urn:li:video:… from upload_video>", destination_url, call_to_action_type,
  status: "DRAFT"
)
```

Notes:

- Campaign group and campaign are `PAUSED`; the creative is `DRAFT` (LinkedIn can't create creatives paused). The user activates manually after reviewing.
- Budget amounts are strings in the account's currency ("100.00" = $100).
- Use `get_audience_counts` *before* `create_campaign` — LinkedIn won't let an audience smaller than 300 ship.
- For LEAD_GENERATION, you need a Lead Gen Form ID — that's not creatable via this MCP, so create it in Campaign Manager first.

If the user has run `/crm-icp-analysis` and `/linkedin-micro-campaigns`, this skill **completes the loop** by producing the actual creative those targeted campaigns will run.

For organic posting: hand the user `launch.mp4` and recommend posting from a **personal profile** (or both personal + company page). Personal-profile organic reach on LinkedIn beats company-page reach by roughly 5–10x.

If LinkedIn Organic is connected, offer to post or schedule it on the company Page (asks first, needs the public URL): `mcp__cogny__mcp__LinkedIn_Organic__tool_schedule_post(scheduled_for, text, author: "<org URN from tool_list_organizations>", video_url, video_title)`, or `tool_create_post` with the same fields to post now. If X Organic is connected, offer `mcp__cogny__mcp__X_Organic__tool_upload_media(file_url)` then `tool_create_post(text, media_ids)` (posts publicly at once, so confirm the text first).

## Output format

When you finish, print:

1. Path to the rendered MP4
2. The beat sheet
3. The format chosen and why it fits the ICP
4. (If applicable) the LinkedIn Ads campaign group / campaign (PAUSED) and creative (DRAFT) IDs, plus the audience size estimate
5. (If applicable) the scheduled or published organic post IDs

## Common mistakes

1. **Corporate intro** — "At [Company], we believe…". Cut it. Open with the role/problem.
2. **No number on the proof card** — abstract claims ("better", "faster") are filtered out. Buyers want numbers.
3. **TikTok-style frenzy** — fast cuts and kinetic text read as junior on LinkedIn. Slow down.
4. **Buzzword bingo** — "leverage", "unlock", "revolutionary", "game-changer". Buyers ignore videos with this language.
5. **Generic CTA** — "Learn more" is dead. Use "Comment X", "DM me", "Tap link".
6. **Ignoring the muted-autoplay reality** — assume zero sound. Captions or it's invisible.

## Related

- `/tiktok-launch-video` — same pattern for TikTok
- `/reddit-launch-video` — same pattern for Reddit
- `/video-to-gif` — convert MP4 to a feed-ready GIF (LinkedIn comments don't render GIFs, but DMs do)
- `/linkedin-micro-campaigns` — pair the video with ICP-targeted campaigns
- `/linkedin-ads-audit` — diagnose existing LinkedIn campaigns before launching new creative
