---
name: google-ads-audit
description: Deep Google Ads account audit — keywords, quality scores, budget pacing, search terms
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads]
user-invocable: true
argument-hint: "[full|keywords|budget|quality|search-terms]"
allowed-tools:
  - mcp__cogny__google_ads__*
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# Google Ads Audit

Comprehensive Google Ads account audit using live data via Cogny's MCP server.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

Before starting, verify you have Google Ads MCP tools available. If `mcp__cogny__google_ads__tool_execute_gaql` is not available:

```
This skill requires Cogny's Google Ads MCP server.

1. Sign up at https://cogny.com/agent
2. Connect your Google Ads account
3. Add your API key to .mcp.json
4. Restart Claude Code

See the README for setup instructions.
```

## Usage

`/google-ads-audit` — full account audit
`/google-ads-audit keywords` — keyword performance only
`/google-ads-audit budget` — budget pacing only
`/google-ads-audit quality` — quality scores only
`/google-ads-audit search-terms` — search term analysis only

## Full Audit Steps

### 1. Account Discovery
```
google_ads__tool_list_accessible_accounts
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

Flag: QS < 4, zero conversions with high spend, broad match bleeding

### 4. Search Term Analysis
```sql
SELECT search_term_view.search_term, search_term_view.status, campaign.name,
  metrics.cost_micros, metrics.conversions, metrics.clicks
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC LIMIT 30
```

Flag: irrelevant terms, high-spend zero-conversion terms, missing negatives

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

### 7. Report findings
Use `create_finding` for each actionable issue found. Include specific data, estimated impact, and recommended action.

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
