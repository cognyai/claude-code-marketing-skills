---
name: google-ads-audit
description: Deep Google Ads account audit — keywords, quality scores, budget pacing, search terms
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads, microsoft-ads]
user-invocable: true
argument-hint: "[full|keywords|budget|quality|search-terms]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  - mcp__cogny__mcp__Google_Ads__tool_get_reporting_view_doc
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Google Ads Audit

Comprehensive Google Ads account audit using live data via Cogny's MCP server.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Campaigns, keywords, QS, search terms, pacing | Google Ads | Microsoft Ads (`Bing_Ads` `tool_get_report`) | Bing money is account-currency units, not micros; QS components are 1–3 |
| Are the conversions real? | Shopify / WooCommerce orders | — | Store = paid orders; Ads = attributed |

Call `list_integrations` once. Report Microsoft Ads as its own block; never sum currencies.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Google Ads Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads (and Microsoft Ads, Shopify or
   WooCommerce if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` is missing, say
"connect Google Ads in Cogny" (or "reconnect Google Ads in Cogny" if it's listed but unhealthy
or a read returns 401/permission denied) and stop.

## Usage

`/google-ads-audit` — full account audit
`/google-ads-audit keywords` — keyword performance only
`/google-ads-audit budget` — budget pacing only
`/google-ads-audit quality` — quality scores only
`/google-ads-audit search-terms` — search term analysis only

## Full Audit Steps

Money fields are micros (divide by 1,000,000). An empty GAQL result (no rows, or no output)
means zero (no matching entities or no activity in the window), not an error.

### 1. Account Discovery
```
mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
```
Identify the account and confirm access.

### 2. Campaign Overview (last 30 days)
```sql
SELECT campaign.name, campaign.status, campaign.bidding_strategy_type,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.conversions,
  metrics.clicks, metrics.impressions, metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### 3. Keyword Performance
```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score, campaign.name,
  metrics.cost_micros, metrics.conversions, metrics.clicks, metrics.impressions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC LIMIT 50
```

Flag: QS 1–3, zero conversions with high spend, broad match bleeding. A Quality Score of 0
or null means "not scored" (too few impressions), not a low score; count those separately
and don't flag them.

Microsoft Ads: `mcp__cogny__mcp__Bing_Ads__tool_list_accounts` for the `account_id`, then
`mcp__cogny__mcp__Bing_Ads__tool_get_report` (`account_id`, `report_type: "keyword"`); `QualityScore`, `ExpectedCtr`, `AdRelevance`,
`LandingPageExperience` (1 = below average, 3 = above).

### 4. Search Term Analysis
```sql
SELECT search_term_view.search_term, search_term_view.status, campaign.name,
  metrics.cost_micros, metrics.conversions, metrics.clicks
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC LIMIT 30
```

Flag: irrelevant terms, high-spend zero-conversion terms, missing negatives, and brand
terms (brand name, misspellings) matching in campaigns not named as brand campaigns.

Before calling negatives "missing", check all three levels: shared lists, plus
campaign- and ad-group-level negatives:

```sql
SELECT shared_set.name, shared_set.type, shared_set.status, shared_set.member_count
FROM shared_set
```

```sql
SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE
  AND campaign.status = 'ENABLED'
```

```sql
SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = TRUE
  AND campaign.status = 'ENABLED'
```

Microsoft Ads: `tool_get_report` with `account_id` and `report_type: "search_query"`.

**Enhanced when connected:** compare 30-day Ads purchase value with the store's paid
revenue (Shopify `tool_list_orders` with `query_filter: "created_at:>=YYYY-MM-DD financial_status:paid"`,
or WooCommerce `get_sales_report` with `date_min`, `date_max`). Report the ratio; Ads value
above total store revenue is a tracking finding.

### 5. Budget Pacing
```sql
SELECT campaign.name, campaign_budget.amount_micros, metrics.cost_micros,
  metrics.impressions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND campaign.status = 'ENABLED'
```

Calculate: daily budget vs daily spend ratio per campaign

### 6. Quality Score Distribution
```sql
SELECT ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.keyword.text, campaign.name
FROM keyword_view
WHERE ad_group_criterion.quality_info.quality_score IS NOT NULL
ORDER BY ad_group_criterion.quality_info.quality_score ASC
```

Bucket scores 1–3 (flag), 4–6, 7–10, and "not scored" (0 or null, kept out of the averages).

### 7. Report findings
Use `create_finding` for each actionable issue found (Cloud: `create_ticket`, fields mapped per section 2 of the
[routing guide](../../skills/marketing-engineer/references/mcp-routing.md)). Include specific data, estimated impact, and recommended action.

Present a summary table:

```
Google Ads Audit: [Account Name]
Health Score: X/100

Campaign Performance (30d):
Total Spend: [X] | Conversions: [X] | Avg CPA: [X]

Issues Found: [N]
- [Critical] ...
- [High] ...
- [Medium] ...

Top 3 Actions:
1. [Highest impact with estimated savings]
2. ...
3. ...
```

Write tools (negatives, pauses, budgets) are never called by this audit; if the user asks
for a change, the skill asks first.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../../skills/marketing-engineer/references/mcp-routing.md`.
