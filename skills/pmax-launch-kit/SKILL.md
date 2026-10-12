---
name: pmax-launch-kit
description: Build a complete Performance Max campaign from a brand URL — asset group copy, search themes, audience signals, image/video shot list, settings — ready to paste into Google Ads
version: "1.1.1"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<brand url>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Google_Ads__tool_generate_keyword_ideas
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_list_audience_segments
  - mcp__cogny__mcp__Semrush__phrase_related
  - mcp__cogny__mcp__Semrush__domain_paid_keywords
  - mcp__cogny__mcp__Ahrefs__keywords_explorer
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_audiences
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_top_sellers_report
  - mcp__cogny__mcp__GrowthBook__list_experiments
  - mcp__cogny__mcp__GrowthBook__get_experiment_results
---

# Performance Max Launch Kit

Give it a brand URL and get back everything you need to build a Performance Max
campaign — every headline, description, search theme, audience signal, plus an
image/video shot list and the campaign settings. No account connection required;
this works entirely from the public website.

## Usage

`/pmax-launch-kit cogny.com` — build a launch kit for that brand
`/pmax-launch-kit example.com/product-x` — focus the kit on one product or category

## Works with

Runs with zero accounts. If a Cogny workspace is connected (`list_integrations`), these
sharpen the kit:

| Job | Without accounts | Enhanced when connected (primary first) |
|-----|------------------|------------------------------------------|
| Search themes | Website + `WebSearch` | Google Ads `tool_generate_keyword_ideas` · Semrush `phrase_related`, `domain_paid_keywords` · Ahrefs `keywords_explorer` |
| Asset group split | Site navigation | Shopify `tool_list_orders` or WooCommerce `get_top_sellers_report` (what actually sells) |
| Audience signals | Generic segment advice | GA4 `tool_list_audiences` (existing first-party lists) · Google Ads `tool_list_audience_segments` |
| Copy angles | Site and reviews | GrowthBook `list_experiments`, `get_experiment_results` (headlines/offers already tested) |

## Steps

### 1. Read the brand

`WebFetch` the URL (and 2–4 key pages: product, pricing, about, a category page).
`WebSearch` the brand name for positioning and review language. Extract:

- What is sold, and the single clearest value proposition
- Who buys it (audience, use cases, pain points)
- Proof points — numbers, awards, named customers, guarantees
- Price band and offer (free trial, free shipping, discount)
- Brand voice — words the site uses, tone, what it avoids
- The conversion action (purchase, signup, lead, demo, install)

If the site is thin or unreachable, ask the user for a one-paragraph description
rather than inventing facts.

**Enhanced when connected:** if GrowthBook is connected, `list_experiments` and
`get_experiment_results` (`experiment_id`) for past landing-page or offer tests. Lead the
copy with the winning angle and don't re-propose a losing one; cite the experiment.

### 2. Decide the asset group structure

One asset group per distinct audience or product line. For most brands start with
1–2 asset groups. Name each by the theme it targets (e.g. "Solo founders",
"Agencies"). With a store connected, base the split on the last 90 days' top sellers
(Shopify `tool_list_orders` with `query_filter: "created_at:>=YYYY-MM-DD financial_status:paid"`,
or WooCommerce `get_top_sellers_report` with `date_min`, `date_max`), not on site navigation. Each asset group gets its own copy, themes, and signal — never reuse one
set of copy across different audiences.

**Different conversion goals → separate campaigns, not asset groups.** Conversion
goals are set per campaign (account-default or campaign-specific), never per asset
group, and budget and bidding are shared across a campaign's asset groups. If one
audience should drive purchases and another demo requests or leads, or the two need
different tROAS/tCPA targets, propose one PMax campaign per goal, each with its own
asset groups.

### 3. Write the asset group copy

For **each** asset group, produce exactly:

**Headlines — 15, each ≤30 characters.** Mix: value props, the offer, social proof,
features, light CTAs. Vary openings. Count every character.

**Long headlines — 5, each ≤90 characters.** Full thoughts that stand alone — these
show where the format has room.

**Descriptions — 5 total: 1 short (≤60 characters) + 4 standard (≤90 characters).**
Each makes a complete point; at least one names the offer, one names proof.

**Business name — ≤25 characters.**

**Calls to action** — suggest 2–3 fitting the conversion (Get started, Sign up, Shop
now, Get a quote).

Show each list in a table with a character count column so nothing is over the limit.

### 4. Search themes — up to 50

List up to 50 search themes per asset group (Google Ads limit; aim for 15–25 strong ones rather than padding to 50): the queries this audience actually types.
Cover branded-adjacent, category, problem-phrased, and competitor-alternative themes.
Do **not** include the brand's own name (PMax already captures brand search; a brand
theme just inflates cannibalization). Mark any theme that risks pulling junk traffic.

**Enhanced when connected:** validate themes with real demand. Google Ads
`tool_generate_keyword_ideas` (`customer_id`, `page_url` or `seed_keywords`,
`geo_target_ids`); else Semrush `phrase_related` (`phrase`, `database`) or Ahrefs
`keywords_explorer` (`keywords`, `country`). Semrush `domain_paid_keywords` (`domain`) on a
competitor shows what they already pay for. Add a volume column and name its source;
volumes differ between tools.

### 5. Audience signals

Recommend a signal per asset group — signals speed up learning, they don't restrict:

- **Your data** — customer match lists, website visitors, converters (best signal)
- **Custom segments** — by search behavior, competitor sites, in-market URLs
- **Interests & demographics** — only as a fallback when no first-party data exists

Be specific: name the in-market / affinity segments and the kind of custom segment to
build.

**Enhanced when connected:** GA4 `tool_list_audiences` (`property_id`) and Google Ads
`tool_list_audience_segments` show which first-party lists already exist; recommend those
by name instead of "build a converters list".

### 6. Image & video shot list

PMax needs real creative. Provide a shot list, not files:

- **Images** — landscape 1.91:1, square 1:1, portrait 4:5. List 5–8 specific shots
  (product in use, lifestyle, before/after, team, UI). Logos: 1:1 and 4:1.
- **Video** — at least one 10s+ vertical video. Give a simple script outline (hook,
  value, proof, CTA). Note that skipping video makes Google auto-generate a weak one.

### 7. Campaign settings & guidance

Recommend:
- **Conversion goal** — the action from Step 1; advise on account-default vs
  campaign-specific goals
- **New customer acquisition** — value-new-customers-higher vs new-customers-only,
  with the trade-off
- **Bidding** — Maximize Conversions (lead gen) or Maximize Conversion Value +
  optional tROAS (ecommerce); start without a target until there's data
- **Budget** — at least ~10–15× target CPA per day so the campaign can learn
- **Final URL expansion** — on with URL exclusions, or off, and why
- **Brand exclusions** — recommend a brand exclusion list so PMax doesn't buy your
  own brand traffic
- A starter **negative keyword** list (account-level) for obvious junk

### 8. Output

Deliver as a single ready-to-use document:

```
Performance Max Launch Kit — [Brand]

Campaign settings
- Objective / conversion goal: ...
- Bidding: ...  | Budget: ...
- New customer acquisition: ...
- Final URL expansion: ...  | Brand exclusions: ...

Asset Group 1 — [name]
Headlines (15)         | table with char counts
Long headlines (5)     | table with char counts
Descriptions (5)       | table with char counts
Business name: ...
Search themes (≤50): ...
Audience signal: ...
Image shot list: ...
Video script outline: ...

Asset Group 2 — [name]
...

Account negatives (starter list): ...
```

End with a 3-step "what to do next" so a non-expert can actually launch it.

## Critical rules

1. **Respect every character limit.** Headlines ≤30, long headlines ≤90,
   descriptions ≤60/≤90, business name ≤25. Show counts so it's verifiable.
2. **Write in the brand's voice**, using its real value props — do not invent
   features, numbers, or customers.
3. **Never put the brand name in search themes.**
4. **Always recommend a video asset and a brand exclusion list** — the two things
   most launches skip.
5. **Build, don't launch.** With Google Ads connected, the kit can be created live
   (`tool_create_campaign`, `tool_create_asset_group`, created paused) only if the user
   asks, and the skill asks first.
6. This is a build kit, not an audit. To review a *live* PMax campaign, use
   `/pmax-audit` (requires Cogny MCP).
