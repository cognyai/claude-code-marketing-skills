---
name: demand-gen-audit
description: Google Ads Demand Gen audit — audience strategy, creative format diversity, creative freshness, placements, CPA vs goal
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads]
user-invocable: true
argument-hint: "[campaign name or id]"
allowed-tools:
  - mcp__cogny__google_ads__tool_list_accessible_accounts
  - mcp__cogny__google_ads__tool_execute_gaql
  - mcp__cogny__google_ads__tool_get_gaql_doc
  - mcp__cogny__google_ads__tool_get_reporting_view_doc
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# Demand Gen Audit

A deep audit of your Demand Gen campaigns — Google's visual, social-style campaign
type running across Discover, Gmail, YouTube feeds and Shorts. Demand Gen lives or
dies on audiences and creative, so that's where this audit spends its time.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

If `mcp__cogny__google_ads__tool_execute_gaql` is not available, print the Cogny
sign-up instructions (see `/google-ads-audit`) and stop.

## Usage

`/demand-gen-audit` — audit every Demand Gen campaign in the account
`/demand-gen-audit Prospecting - Q2` — audit one campaign by name or id

## Why Demand Gen needs its own audit

Demand Gen has no keywords and no search intent. It's an interruption channel — you
win by showing the right **audience** the right **creative**. The audit checks
audience strategy, creative format spread, creative fatigue, and whether CPA is
tracking toward goal.

## Steps

### 1. Find the Demand Gen campaigns

```sql
SELECT campaign.id, campaign.name, campaign.status,
  campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value, metrics.clicks, metrics.impressions
FROM campaign
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

Compute CPA and compare to the campaign's target CPA. Flag campaigns running >50%
over target.

### 2. Ad group & audience strategy

```sql
SELECT ad_group.name, ad_group.status, campaign.name,
  metrics.cost_micros, metrics.conversions, metrics.clicks
FROM ad_group
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND segments.date DURING LAST_30_DAYS
```

```sql
SELECT ad_group.name, ad_group_criterion.type,
  ad_group_criterion.user_list.user_list,
  ad_group_criterion.audience.audience
FROM ad_group_criterion
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND ad_group_criterion.status = 'ENABLED'
```

Flag:
- Ad groups with **no audience** attached (running fully broad — burns budget)
- Only broad/affinity audiences, no first-party signal (customer match, website
  visitors) and no lookalike segments
- Prospecting and remarketing audiences mixed in one ad group — they need different
  creative and different bids
- A single ad group per campaign (no audience testing)

### 3. Creative format diversity

```sql
SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type,
  ad_group_ad.ad_strength, ad_group_ad.status,
  metrics.impressions, metrics.clicks, metrics.conversions
FROM ad_group_ad
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND segments.date DURING LAST_30_DAYS
```

Demand Gen ad types: single image, carousel, and video responsive. Flag:
- **Single-format** ad groups — image-only campaigns miss YouTube/Shorts inventory;
  add video
- Ad strength `POOR` / `AVERAGE`
- Fewer than 2–3 ads per ad group (nothing to optimize between)
- Zero video creative when the budget is >$3K/mo

### 4. Creative fatigue

For each enabled ad, look at the CTR / conversion-rate trend over the last 30 days vs
the prior 30. Flag:
- Ads live >60 days with a falling CTR (classic fatigue)
- Ad groups where every ad launched the same day and none has refreshed since

### 5. Placement & exclusions

Flag:
- No content/placement exclusions — Demand Gen can serve next to anything
- Conversions concentrated in one surface while budget spreads evenly (consider
  surface-specific campaigns)

### 6. Conversion goal alignment

Demand Gen is upper/mid funnel. Flag campaigns optimizing to a hard bottom-funnel
action (purchase) with too few conversions to learn — a softer goal (lead, signup,
add-to-cart) often suits the funnel stage better.

### 7. Score and report

```
Demand Gen Audit — [Account Name]
Demand Gen Score: X/100  ·  30-day spend: [X]  ·  Conv: [X]  ·  CPA vs target: [X]

| Campaign | Ad groups | Audiences | Formats | Avg ad strength | CPA |
|----------|-----------|-----------|---------|-----------------|-----|

🔴 Critical   — no audiences, no conversions, CPA far over target
🟡 Important  — single-format creative, fatigue, no first-party signal
🟢 Optimization — add lookalikes, placement exclusions, creative refresh

Top 3 Actions:
1. [Highest $ impact]
2. ...
3. ...
```

### 8. Record findings

```json
{
  "title": "Demand Gen 'Prospecting - Q2' runs image-only — missing YouTube & Shorts",
  "body": "All 4 ads in the campaign are single-image. Demand Gen serves video inventory on YouTube feed and Shorts that image ads can't reach. The campaign spends $110/day. Add 2-3 vertical video creatives to open that inventory.",
  "action_type": "creative_refresh",
  "expected_outcome": "Access to video inventory; lower CPM and broader reach",
  "estimated_impact_usd": 900,
  "priority": "medium"
}
```

Action types: `creative_refresh`, `audience_refinement`, `campaign_optimization`,
`bidding_strategy`, `placement_exclusion`.

## Critical rules

1. **Audiences and creative are the whole game.** Demand Gen has no keyword lever —
   spend the audit there.
2. **Always check for video.** Image-only Demand Gen leaves the best inventory unused.
3. **Quote real numbers**: format counts, audience types, CPA vs target.
4. **Read-only.** Recommend audience and creative changes; never make them.
