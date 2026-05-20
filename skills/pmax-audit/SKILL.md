---
name: pmax-audit
description: Performance Max campaign audit — asset group strength, asset coverage, search themes, audience signals, brand exclusions, channel distribution
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

# Performance Max Audit

A deep audit of your Performance Max campaigns. PMax hides most of its levers — this
skill pulls the ones the API still exposes (asset groups, asset coverage, search
themes, audience signals, exclusions, channel mix) and flags what's leaking spend.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

If `mcp__cogny__google_ads__tool_execute_gaql` is not available, print the Cogny
sign-up instructions (see `/google-ads-audit`) and stop.

## Usage

`/pmax-audit` — audit every Performance Max campaign in the account
`/pmax-audit Holiday Retail` — audit one campaign by name or id

## Why PMax needs its own audit

PMax is a black box compared to Search. There are no keywords and no per-placement
bids. The few real levers — **asset group ad strength, asset coverage, search themes,
audience signals, and exclusions** — are what this skill inspects, because they are
the only things you can actually change.

## Steps

### 1. Find the Performance Max campaigns

```sql
SELECT campaign.id, campaign.name, campaign.status,
  campaign.bidding_strategy_type, campaign.maximize_conversion_value.target_roas,
  campaign.target_cpa.target_cpa_micros, campaign_budget.amount_micros,
  metrics.cost_micros, metrics.conversions, metrics.conversions_value
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### 2. Asset group health

```sql
SELECT asset_group.id, asset_group.name, asset_group.status,
  asset_group.ad_strength, campaign.name,
  metrics.cost_micros, metrics.conversions, metrics.conversions_value
FROM asset_group
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND segments.date DURING LAST_30_DAYS
```

Flag:
- Ad strength `POOR` or `AVERAGE` on any spending asset group
- Campaigns with a **single asset group** (no audience/theme segmentation)
- Asset groups with status `REMOVED`/`PAUSED` still configured but campaign starved

### 3. Asset coverage per group

```sql
SELECT asset_group.name, asset_group_asset.field_type,
  asset_group_asset.performance_label, asset_group_asset.status,
  asset.id, asset.type
FROM asset_group_asset
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

For each asset group, count assets by `field_type` and compare to Google's max slots:

| Field type | Recommended | Max |
|------------|-------------|-----|
| HEADLINE | 11+ | 15 |
| LONG_HEADLINE | 5 | 5 |
| DESCRIPTION | 5 | 5 |
| MARKETING_IMAGE (1.91:1) | 4+ | 20 |
| SQUARE_MARKETING_IMAGE | 4+ | 20 |
| PORTRAIT_MARKETING_IMAGE | 2+ | 20 |
| LOGO | 1+ | 5 |
| YOUTUBE_VIDEO | 1+ | 5 |

Flag:
- Any group below the recommended count for headlines, images, or video
- **No video asset** — Google auto-generates a low-quality one if you skip it
- Assets with `performance_label = LOW` that should be replaced
- Only one image aspect ratio (limits inventory: blocks whole channels)

### 4. Search themes & audience signals

```sql
SELECT asset_group.name, asset_group_signal.search_theme.text,
  asset_group_signal.audience.audience
FROM asset_group_signal
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

Flag:
- Asset groups with **no audience signal** — PMax starts cold, wastes budget learning
- No search themes set (up to 25 allowed — they steer the Search surface)
- Search themes that overlap your brand terms (inflates brand cannibalization)

### 5. Search category insight (where spend actually goes)

```sql
SELECT campaign_search_term_insight.category_label,
  metrics.clicks, metrics.conversions, metrics.conversions_value
FROM campaign_search_term_insight
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.clicks DESC
LIMIT 50
```

Flag categories with high clicks and zero conversions — candidates for **negative
keywords** (PMax negatives are set at the account level, or via support).

### 6. Brand exclusions & new-customer goal

```sql
SELECT campaign.name, campaign.brand_guidelines_enabled,
  campaign.customer_acquisition_setting.optimization_mode
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

Flag:
- No brand exclusion list — PMax happily spends on your own brand searches
- New-customer acquisition goal not configured (for accounts that want growth, not
  just remarketing-flavored conversions)
- Final URL expansion ON with no URL exclusions (PMax can send traffic anywhere on
  the domain)

### 7. Listing groups (retail PMax only)

If the campaign has a Merchant Center feed:

```sql
SELECT asset_group.name, asset_group_listing_group_filter.type,
  asset_group_listing_group_filter.case_value.product_type.value
FROM asset_group_listing_group_filter
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

Flag everything dumped into one "All products" node — no way to prioritize
high-margin SKUs. Recommend `/shopping-campaign-audit` for full feed analysis.

### 8. Score and report

```
Performance Max Audit — [Account Name]
PMax Score: X/100  ·  30-day spend: [X]  ·  Conv: [X]  ·  ROAS: [X.Xx]

Per campaign / asset group:
| Campaign | Asset group | Ad strength | Signal? | Video? | Spend | ROAS |
|----------|-------------|-------------|---------|--------|-------|------|

🔴 Critical   — broken signals, POOR ad strength, no brand exclusion
🟡 Important  — thin assets, missing video, no search themes
🟢 Optimization — add aspect ratios, expand headlines

Top 3 Actions:
1. [Highest $ impact]
2. ...
3. ...
```

### 9. Record findings

```json
{
  "title": "PMax 'Holiday Retail' has no audience signal — slow, expensive learning",
  "body": "Asset group 'Gifts' spends $90/day with no audience signal attached. PMax is exploring blind. Add a signal from converting customers (customer match list or your top-converting segment) to speed up learning.",
  "action_type": "audience_refinement",
  "expected_outcome": "Faster learning, lower CPA within 2-3 weeks",
  "estimated_impact_usd": 1200,
  "priority": "high"
}
```

Action types: `asset_optimization`, `audience_refinement`, `negative_keyword`,
`campaign_optimization`, `bidding_strategy`, `brand_exclusion`.

## Critical rules

1. **Asset strength and audience signals are the real levers.** Spend the audit
   there, not on metrics you can't influence.
2. **Always check brand exclusions.** Unexcluded brand traffic is the most common
   PMax money leak.
3. **Quote real numbers** — ad strength label, asset counts, category clicks.
4. **Read-only.** Surface issues; never edit asset groups.
