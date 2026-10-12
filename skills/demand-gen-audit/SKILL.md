---
name: demand-gen-audit
description: Google Ads Demand Gen audit — audience strategy, creative format diversity, creative freshness, placements, CPA vs goal
version: "1.1.2"
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
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Demand Gen Audit

A deep audit of your Demand Gen campaigns — Google's visual, social-style campaign
type running across Discover, Gmail, YouTube feeds and Shorts. Demand Gen lives or
dies on audiences and creative, so that's where this audit spends its time.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Audiences, creative formats, ad strength | Google Ads | — | Google-only levers |
| Same-job campaign totals | Google Ads (Demand Gen) | Microsoft Ads (`Bing_Ads`, campaign type `Audience`) | Bing money is account-currency units; Microsoft Audience Network inventory, not YouTube |
| Post-click quality | Google Analytics 4 | — | GA4 engaged sessions and key events per campaign; GA4 attribution ≠ Ads |
| Prospecting CPA benchmark | — | Meta Ads (`tool_get_insights`) | Meta counts link clicks and conversions differently; compare CPA, never sum |

Call `list_integrations` once. Everything beyond Google Ads is optional context.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Demand Gen Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads (plus Microsoft Ads, GA4 or Meta Ads
   if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` is missing, say
"connect Google Ads in Cogny" (or "reconnect Google Ads in Cogny" if it's listed but unhealthy
or a read returns 401/permission denied) and stop.

## Usage

`/demand-gen-audit` — audit every Demand Gen campaign in the account
`/demand-gen-audit Prospecting - Q2` — audit one campaign by name or id

## Why Demand Gen needs its own audit

Demand Gen has no keywords and no search intent. It's an interruption channel — you
win by showing the right **audience** the right **creative**. The audit checks
audience strategy, creative format spread, creative fatigue, and whether CPA is
tracking toward goal.

## Steps

Google Ads money fields are micros (divide by 1,000,000). An empty GAQL result (no rows, or
the tool returns no output) means zero: no matching entities or no activity in the window.
Report it as 0, not as an error.

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

If this returns no rows, also check for paused or idle ones (same query without the date
filter, `campaign.status != 'REMOVED'`). If there are still none, report "no Demand Gen
campaigns in this account" and stop; suggest `/google-ads-audit` for the account as a whole.

Compute CPA and compare to the campaign's target CPA. Flag campaigns running >50%
over target.

**Microsoft Ads (if connected):** `tool_get_campaigns` (`account_id`,
`campaign_types: ["Audience"]`) and `tool_get_report` (`account_id` from `tool_list_accounts`,
`report_type: "campaign"`, `campaign_ids`). Show Microsoft Audience campaigns as their own row block with CPA in the
account's currency.

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

Pull each enabled ad for the last 30 days, then for the prior 30 (the 30 days before
`LAST_30_DAYS`, as a `BETWEEN` range):

```sql
SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type,
  metrics.impressions, metrics.clicks, metrics.ctr, metrics.conversions
FROM ad_group_ad
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND ad_group_ad.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

```sql
SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type,
  metrics.impressions, metrics.clicks, metrics.ctr, metrics.conversions
FROM ad_group_ad
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND ad_group_ad.status = 'ENABLED'
  AND segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

Join on `ad_group_ad.ad.id`. An ad present in the prior window was already live 30+ days ago;
compare CTR and conversion rate between the windows (ignore ads under ~1,000 impressions in
either window). Flag:
- Ads live >60 days with a falling CTR (classic fatigue)
- Ad groups where every ad launched the same day and none has refreshed since

### 5. Placement & exclusions

Spend by surface:

```sql
SELECT campaign.name, segments.ad_network_type, metrics.impressions, metrics.clicks,
  metrics.cost_micros, metrics.conversions
FROM campaign
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND segments.date DURING LAST_30_DAYS
```

Top placements, where Google reports them:

```sql
SELECT campaign.name, detail_placement_view.display_name,
  detail_placement_view.placement_type, detail_placement_view.target_url,
  metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM detail_placement_view
WHERE campaign.advertising_channel_type = 'DEMAND_GEN'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

Google exposes little placement detail for Demand Gen, so this second query is often empty
even when the campaign served. Then judge from the surface split above, and mark the
exclusion check **manual**: "Check Tools → Content suitability and the campaign's placement
report in the Google Ads UI." Don't claim exclusions are missing from an empty result.

Flag:
- No content/placement exclusions — Demand Gen can serve next to anything
- Conversions concentrated in one surface while budget spreads evenly (consider
  surface-specific campaigns)

### 6. Conversion goal alignment

Demand Gen is upper/mid funnel. Flag campaigns optimizing to a hard bottom-funnel
action (purchase) with too few conversions to learn — a softer goal (lead, signup,
add-to-cart) often suits the funnel stage better.

### 6b. Enhanced when connected: post-click quality and benchmark

- **GA4:** `tool_list_account_summaries` for the property, then `tool_run_report` (`property_id`, `date_ranges`,
  `dimensions: ["sessionGoogleAdsCampaignName"]`,
  `metrics: ["sessions", "engagementRate", "keyEvents"]`). A Demand Gen campaign with cheap
  clicks but an engagement rate far below the site's paid-search average is buying
  accidental taps (often Shorts/Discover placements); that supports a placement finding.
- **Meta Ads:** `tool_list_ad_accounts`, then `tool_get_insights` (`ad_account_id`,
  `level: "campaign"`, `time_range_since`, `time_range_until`) for prospecting campaigns.
  Put the Meta prospecting CPA next to Demand Gen's as context for budget decisions.
  Different conversion definitions: label both, don't declare a winner on CPA alone.

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

Cloud uses `create_ticket` with the same content, fields mapped per section 2 of the routing guide.

Action types: `creative_refresh`, `audience_refinement`, `campaign_optimization`,
`bidding_strategy`, `placement_exclusion`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Audiences and creative are the whole game.** Demand Gen has no keyword lever —
   spend the audit there.
2. **Always check for video.** Image-only Demand Gen leaves the best inventory unused.
3. **Quote real numbers**: format counts, audience types, CPA vs target.
4. **Read-only.** Recommend audience and creative changes; never make them. Write tools
   (`tool_add_audience_to_ad_group`, `tool_update_ad_status`) are used only on the user's
   request, and the skill asks first.
5. **Cross-platform numbers are context, not totals.** Each in its own currency and definition.
