---
name: pmax-audit
description: Performance Max campaign audit — asset group strength, asset coverage, search themes, audience signals, brand exclusions, channel distribution
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads, microsoft-ads]
user-invocable: true
argument-hint: "[campaign name or id]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  - mcp__cogny__mcp__Google_Ads__tool_get_reporting_view_doc
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Performance Max Audit

A deep audit of your Performance Max campaigns. PMax hides most of its levers — this
skill pulls the ones the API still exposes (asset groups, asset coverage, search
themes, audience signals, exclusions, channel mix) and flags what's leaking spend.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Asset groups, assets, signals, exclusions | Google Ads | — | Only Google exposes these levers |
| PMax spend, conversions, ROAS | Google Ads | Microsoft Ads (`Bing_Ads`, campaign type `PerformanceMax`) | Bing: account-currency units; compute ROAS as `Revenue` / `Spend` yourself; no asset-group data |
| Is the ROAS real? | Shopify / WooCommerce orders | GA4 (`sessionGoogleAdsCampaignName`) | Store = paid orders; PMax claims brand and remarketing conversions |

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Performance Max Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads (plus Microsoft Ads, GA4, Shopify or
   WooCommerce if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` is missing, say
"connect Google Ads in Cogny" (or "reconnect Google Ads in Cogny" if it's listed but unhealthy
or a read returns 401/permission denied) and stop. If only Microsoft Ads is
connected, run step 1's Microsoft branch and say that the asset-level audit needs Google Ads.

## Usage

`/pmax-audit` — audit every Performance Max campaign in the account
`/pmax-audit Holiday Retail` — audit one campaign by name or id

## Why PMax needs its own audit

PMax is a black box compared to Search. There are no keywords and no per-placement
bids. The few real levers — **asset group ad strength, asset coverage, search themes,
audience signals, and exclusions** — are what this skill inspects, because they are
the only things you can actually change.

## Steps

Google Ads money fields are micros (divide by 1,000,000). An empty GAQL result (no rows, or
the tool returns no output) means zero: no matching entities or no activity in the window.
Report it as 0, not as an error. Query errors come back as explicit error messages.

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

**Microsoft Ads (if connected):** `tool_list_accounts` for the `account_id`, then `tool_get_campaigns`
(`account_id`, `campaign_types: ["PerformanceMax"]`), then `tool_get_report` (`account_id`,
`report_type: "campaign"`, `campaign_ids`, `start_date`, `end_date`). Report spend, conversions and revenue as a
separate block; Microsoft PMax is often an import of the Google one, so compare CPA/ROAS
between the two and flag a gap over 2x.

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

`asset_group_asset.performance_label` was removed in API v25 (UNRECOGNIZED_FIELD). Use
`primary_status` / `primary_status_reasons` plus the asset's own metrics:

```sql
SELECT asset_group.name, asset_group_asset.field_type, asset_group_asset.status,
  asset_group_asset.primary_status, asset_group_asset.primary_status_reasons,
  asset.id, asset.type,
  metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros
FROM asset_group_asset
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND segments.date DURING LAST_30_DAYS
```

Assets with no impressions in the window drop out of this result; run it once more without
the metrics and the `segments.date` filter to count every linked asset.

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
- Assets whose `primary_status` is `NOT_ELIGIBLE` or `LIMITED` (read `primary_status_reasons`
  for why, e.g. a policy limit), and low performers: assets with impressions but a CTR or
  conversion rate far below the other assets of the same `field_type` in the group
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

`campaign_search_term_insight` accepts one campaign per query. Loop over the campaign ids
from step 1:

```sql
SELECT campaign_search_term_insight.category_label,
  metrics.clicks, metrics.conversions, metrics.conversions_value
FROM campaign_search_term_insight
WHERE segments.date DURING LAST_30_DAYS
  AND campaign_search_term_insight.campaign_id = '<id>'
ORDER BY metrics.clicks DESC
LIMIT 50
```

An empty `category_label` is the bucket of uncategorised terms, not an error.

Flag categories with high clicks and zero conversions — candidates for **negative
keywords** (PMax negatives are set at the account level, or via support).

### 6. Brand exclusions, URL expansion & new customers

`campaign.brand_guidelines_enabled` is about brand colours and fonts in generated assets, not
brand exclusions. Brand exclusions are `BRAND_LIST` campaign criteria:

```sql
SELECT campaign.name, campaign_criterion.type, campaign_criterion.negative,
  campaign_criterion.brand_list.shared_set
FROM campaign_criterion
WHERE campaign_criterion.type = 'BRAND_LIST'
  AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

A PMax campaign with no row here has no brand exclusion. Final URL expansion and other
automation settings:

```sql
SELECT campaign.name, campaign.asset_automation_settings
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

Look for the final-URL-expansion entry (e.g. `FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION`)
with `asset_automation_status: OPTED_IN`.
`campaign.customer_acquisition_setting.optimization_mode` is not recognised by the API, so
read the new-customer split from conversions instead. This segment accepts conversion metrics
only (adding `metrics.cost_micros` fails):

```sql
SELECT campaign.name, segments.new_versus_returning_customers,
  metrics.conversions, metrics.conversions_value
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND segments.date DURING LAST_30_DAYS
```

An empty result means 0 conversions in either segment. If step 1 shows conversions for the
campaign but this returns nothing, new-vs-returning isn't being measured (no customer lists
or new-customer goal), so say "not measured" rather than "0 new customers".

Flag:
- No brand exclusion list — PMax happily spends on your own brand searches
- Most conversions value from returning customers, or no new-vs-returning data at all
  (new-customer goal likely not configured), for accounts that want growth, not just
  remarketing-flavored conversions
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

### 7b. Enhanced when connected: is the ROAS real?

PMax claims credit for brand searches and returning buyers. If a store is connected, pull
paid revenue for the same 30 days (Shopify `tool_list_orders` with `query_filter:
"created_at:>=YYYY-MM-DD financial_status:paid"`; WooCommerce `get_sales_report` with
`date_min`, `date_max`) and show PMax `conversions_value` as a share of it. With GA4,
`tool_list_account_summaries` for the property, then `tool_run_report` (`dimensions: ["sessionGoogleAdsCampaignName", "newVsReturning"]`,
`metrics: ["sessions", "keyEvents", "purchaseRevenue"]`; keep `sessions`, as GA4 drops rows
where every metric is 0) shows how much PMax revenue comes from
returning users. A high returning share plus no brand exclusion makes step 6 critical.

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

Cloud uses `create_ticket` with the same content, fields mapped per section 2 of the routing guide.

Action types: `asset_optimization`, `audience_refinement`, `negative_keyword`,
`campaign_optimization`, `bidding_strategy`, `brand_exclusion`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Asset strength and audience signals are the real levers.** Spend the audit
   there, not on metrics you can't influence.
2. **Always check brand exclusions.** Unexcluded brand traffic is the most common
   PMax money leak.
3. **Quote real numbers** — ad strength label, asset counts, category clicks.
4. **Read-only.** Surface issues; never edit asset groups. Write tools such as
   `tool_add_asset_to_asset_group` are used only on the user's request, and the skill asks first.
5. **Platform and store numbers stay side by side**, each in its own currency.
