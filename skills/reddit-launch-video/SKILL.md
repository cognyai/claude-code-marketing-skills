---
name: reddit-launch-video
description: Produce a Reddit-native 1:1 or 4:5 launch video using HyperFrames. Idiomatic Reddit feel — text-first, low-polish, sound-off, subreddit-aware. Optionally hand off to Reddit Ads to launch as a promoted post targeted to specific subreddits.
version: "1.0.0"
author: Cogny AI
platforms: [reddit-ads, hyperframes]
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
  - mcp__cogny__get_context_tree_overview
  - mcp__cogny__browse_context_tree
  - mcp__cogny__read_context_node
  - mcp__cogny__search_context
  # Optional handoff to Reddit Ads when the user wants to publish as a promoted post
  - mcp__cogny__reddit_ads__*
---

# Reddit Launch Video

Produce a Reddit-native launch video using [HyperFrames](https://hyperframes.heygen.com).

Reddit is the platform where polish *hurts* you. Ads that look like ads get downvoted, hidden, or drowned in sarcastic comments. This skill is built for the opposite — text-first, screenshot-heavy, sound-off, conversational. The closer the video looks to a normal Reddit post, the better it performs.

## Usage

`/reddit-launch-video https://example.com/launch` — pulls context from a launch page
`/reddit-launch-video "we built an open-source alternative to X"` — short brief
`/reddit-launch-video` — interview the user

## Prerequisites

```bash
node --version            # ≥ 22
ffmpeg -version | head -1 # ≥ 6
```

## Steps

### 1. Gather product context AND subreddit context

Reddit only works if you know *which subreddit* the video is meant for. The same product needs different angles for r/SaaS, r/marketing, r/programming, and r/Entrepreneur.

Try sources in order:

**1a. Local file** — `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md`.

**1b. Cogny MCP context tree** — if the `cogny` MCP server is connected:

```
mcp__cogny__get_context_tree_overview
mcp__cogny__search_context query="<product>"
mcp__cogny__read_context_node node_id="…"
```

The tree often contains the customer / community language and proof points that determine which subreddits will tolerate the post. Check it before falling back to web scraping.

**1c. Public web** — `WebFetch` the URL only if 1a/1b are empty or thin.

Then ask (don't skip — these can't be derived from any of 1a–1c):

1. Which **2–3 subreddits** is this targeting? (be specific — `r/marketing`, not "marketers")
2. What's the *honest* one-liner that subreddit would actually upvote?
3. Are you paying to promote this, or trying to seed it organically? (Determines tone — paid can be slightly more polished, organic must be near-zero polish.)
4. What's a real, concrete, non-marketing detail you can lead with? (a number, a screenshot of the actual product, a problem you hit, an open-source repo)
5. Is there a counterpoint / honest tradeoff you can name? (Reddit rewards self-awareness; "here's what it doesn't do" outperforms "here's why we're great")

If the user can't answer #4, do not proceed — the video has no Reddit-shaped truth in it.

### 1.5 Capture brand identity (lightly)

Reddit's tolerance for branding is *low* — heavy brand styling reads as "ad". Still, you want one or two cues so the video doesn't look generic.

Capture the same kit as the other channel skills (see [`references/brand-identity.md`](references/brand-identity.md)) but **dial it down** for Reddit:

- Use the brand's accent color **only** (e.g. one underline, one callout border).
- Default background stays light (`#f7f7f5`-ish) regardless of brand background — Reddit users browse in light mode, dark cards read as ad.
- Default font stays system / IBM Plex / Inter regardless of the brand's display font — display fonts read as marketing.

If the user pushes back ("but our brand uses serif headlines"), explain the tradeoff and let them decide. The composition template exposes `--accent` as a CSS variable; the rest is locked to a Reddit-native palette by design.

### 2. Pick the format

Reddit-idiomatic video formats:

| Format | When to use | Structure |
|--------|-------------|-----------|
| **Show HN-style** | Technical / dev audiences | "Built X. Stack is Y. Here's the demo. Repo / link below." |
| **Self-aware launch** | Most B2B/SaaS subs | "We built X. Here's what it does. Here's what it doesn't do (yet)." |
| **Comparison teardown** | Niche tools | "I tested [your tool] vs [3 competitors]. Here's what I found." |
| **Problem-first** | Marketing / business subs | "I had this exact problem. Here's how I solved it. (Yes, I built the tool.)" |
| **Public benchmark** | Data / dev / ML subs | "Here are the actual numbers. Methodology: X. Code: Y." |

Pick **one**. Confirm with the user.

### 3. Write the script (Reddit grammar)

- **Total length**: 20–45 seconds. Reddit tolerates longer than TikTok; don't pad to fill it.
- **Opening (0–2s)**: a flat, declarative sentence. No "what if I told you", no "POV". Reddit's tolerance for theatrics is zero.
- **Middle**: text-on-frame describing what's actually happening, paired with a screenshot or short screen-capture clip. Show the product, don't talk about it.
- **Honest beat**: at least one card that names a tradeoff, limitation, or "here's what's still rough". This card is what makes the video feel native.
- **Close**: link, repo, or "comments below". Not "tap to learn more".
- **No music** unless it's diegetic. No voiceover unless the user records one. Captions are the soundtrack.

Hand the beat sheet back to the user. **Wait for confirmation.**

### 4. Scaffold the HyperFrames project

```bash
npx -y hyperframes@latest init <product-slug>-reddit --yes
cd <product-slug>-reddit
```

Read the generated `CLAUDE.md` once for the framework rules.

### 5. Compose the video (1:1 default, 4:5 alternative)

Reddit's feed is dominated by **square (1:1) and 4:5 portrait**. 16:9 plays but feels like an outsider. 9:16 vertical works but reads as a TikTok crosspost.

Default to **1080×1080 (1:1)**. Use 1080×1350 (4:5) only if the script needs more vertical room for stacked screenshots.

Reference composition: see [`references/composition-template.html`](references/composition-template.html).

Reddit-specific styling rules:

- **Type**: 60–90px. Smaller than TikTok — Reddit users are reading, not scrolling.
- **Color**: muted. Off-white background, near-black text. Reddit's UI is light-mode by default; dark backgrounds read as "ad". A single accent color is fine; avoid neon.
- **Motion**: minimal. A slow `y` translate or `opacity` fade is plenty. Anything kinetic reads as TikTok and gets dismissed.
- **Type face**: stick to system fonts or IBM Plex Sans / Inter. Anything display-y reads as marketing.
- **Screenshots > illustrations**: a real screenshot of the product UI outperforms any motion graphic. Use `npx hyperframes capture <url>` to grab the actual UI.

### 6. Lint & render

```bash
npx hyperframes lint
npx hyperframes render --output launch.mp4
```

### 7. Sanity check

- Does it look like a normal Reddit post? Show it to the user. If the answer is "this looks like an ad", you've over-produced — rewrite simpler.
- Captions readable on a phone in light mode?
- Is there an honest / self-aware beat in it?
- Length 20–45s?

### 8. (Optional) Hand off to Reddit Ads

If the user wants to run this as a paid promoted post, Reddit's killer differentiator is **subreddit targeting**. Use it.

```
reddit_ads__tool_list_ad_accounts
reddit_ads__tool_get_targeting_options(account_id, type='subreddits', query='<topic>')
reddit_ads__tool_create_campaign(...)             # objective: CLICKS or CONVERSIONS, status: PAUSED
reddit_ads__tool_create_ad_group(
  account_id, campaign_id, name,
  goal_type='DAILY_SPEND',
  goal_value=<micros>,                            # 1_000_000 = $1.00
  target_subreddits=['marketing', 'SaaS', 'Entrepreneur']
)
# Reddit ads wrap an existing post:
reddit_ads__tool_create_post(title='...', url='https://...')   # returns t3_xxx
reddit_ads__tool_create_ad(account_id, ad_group_id, name, post_id='t3_xxx')
```

Notes:

- All amounts are in **micros** (1,000,000 = $1.00). Don't forget to multiply.
- Status is `PAUSED` by default — leave it that way and let the user activate manually after reviewing.
- Reddit charges per click/impression — set a low daily cap (~$10/day) for the first run.
- The MCP cannot upload video creatives directly; you'll need to upload `launch.mp4` via the Reddit Ads UI, then attach the post.

For organic posting: hand the user `launch.mp4` and remind them Reddit auto-detects "promotional" videos — the more it looks like a regular post, the further it travels.

## Output format

When you finish, print:

1. Path to the rendered MP4
2. The beat sheet (so the user can iterate)
3. The target subreddits and the angle chosen for each
4. (If applicable) the Reddit Ads campaign / ad group / post / ad IDs created in PAUSED state, with the targeted subreddits listed

## Common mistakes

1. **Forgetting which subreddit it's for** — generic Reddit videos die. Each cut needs a specific sub.
2. **Hype language** — "revolutionary", "game-changing", "10x". Reddit ratios these on sight.
3. **Music + voiceover + motion graphics** — every layer of polish costs you authenticity. Strip it.
4. **No tradeoff named** — Reddit's BS detector requires you to name what's *not* great about your product.
5. **CTA = "learn more"** — name the next step. "Repo:", "Comments below for questions", "Free tier link".
6. **Stretching a TikTok video to 1:1** — different grammar, different rendering. Build for Reddit, don't port.

## Related

- `/tiktok-launch-video` — same pattern for TikTok
- `/linkedin-launch-video` — same pattern for LinkedIn
- `/video-to-gif` — convert MP4 to a feed-ready GIF (Reddit comments support GIFs natively)
- `/non-commodity-content` — interview-driven content that maps well to Reddit's tone
