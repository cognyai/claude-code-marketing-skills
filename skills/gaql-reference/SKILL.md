---
name: gaql-reference
description: Google Ads Query Language (GAQL) Reference — complete syntax, resource types, fields, operators, date macros, and ready-to-use query patterns
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<query or topic>"
allowed-tools:
  - WebSearch
  - Read
  - Write
  - Bash
  # Google Ads tools (when connected via Cogny MCP)
  - mcp__cogny__google_ads__tool_execute_gaql
  - mcp__cogny__google_ads__tool_get_gaql_doc
  - mcp__cogny__google_ads__tool_get_reporting_view_doc
  - mcp__cogny__google_ads__tool_list_accessible_accounts
---

# Google Ads Query Language (GAQL) Reference

Complete reference for GAQL syntax, resource types, fields, operators, date macros, and common query patterns for Google Ads reporting and optimization.

Full docs: https://cogny.com/docs/gaql-reference

## Usage

```
/gaql-reference                           # Show full syntax overview
/gaql-reference search terms              # Search terms report pattern
/gaql-reference quality score             # Quality Score analysis query
/gaql-reference impression share          # Budget & impression share query
/gaql-reference geographic                # Geographic performance query
/gaql-reference change history            # Change history audit query
```

## Instructions

You are a Google Ads Query Language (GAQL) expert. Use this reference to help users write correct GAQL queries, understand resource types, choose the right fields, and avoid common pitfalls.

When the user asks a question, find the relevant section below and provide precise, actionable answers with ready-to-use GAQL examples.

If the user provides a specific topic as an argument, focus on that area. Otherwise, provide an overview of the GAQL syntax and available resources.

When the user has Cogny MCP tools available, prefer using `mcp__cogny__google_ads__tool_execute_gaql` to run queries directly and `mcp__cogny__google_ads__tool_get_gaql_doc` or `mcp__cogny__google_ads__tool_get_reporting_view_doc` for API documentation lookups.

---

## Syntax

### Formal Grammar

```
query         = SELECT field_list FROM resource_name
                [ WHERE condition_list ]
                [ ORDER BY field_name [ ASC | DESC ] ]
                [ LIMIT positive_integer ]
                [ PARAMETERS param_list ]

field_list    = field_name { , field_name }
condition_list = condition { AND condition }
condition     = field_name operator value
param_list    = param_name = param_value { , param_name = param_value }
```

### Clauses

| Clause | Required | Description |
|--------|----------|-------------|
| `SELECT` | Yes | Fields to return (resource fields, metrics, segments) |
| `FROM` | Yes | Single resource type to query |
| `WHERE` | No | Filter conditions joined by `AND` (no `OR` support) |
| `ORDER BY` | No | Sort by one field, `ASC` or `DESC` |
| `LIMIT` | No | Maximum number of rows to return |
| `PARAMETERS` | No | Query-level parameters (e.g., `include_drafts = true`) |

### Example

```sql
SELECT
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.impressions DESC
LIMIT 50
```

## Resource Types (FROM Clause)

### Campaign Management

| Resource | Description |
|----------|-------------|
| `campaign` | Campaign settings, status, bidding, budget |
| `campaign_budget` | Shared and campaign-level budgets |
| `campaign_criterion` | Campaign-level targeting criteria |
| `campaign_bid_modifier` | Bid adjustments at campaign level |
| `bidding_strategy` | Portfolio bidding strategies |

### Ad Groups & Ads

| Resource | Description |
|----------|-------------|
| `ad_group` | Ad group settings, status, targeting |
| `ad_group_ad` | Ads within ad groups (RSA, ETA, etc.) |
| `ad_group_ad_asset_view` | Asset-level performance for responsive ads |
| `ad_group_criterion` | Keywords, audiences, and other criteria |
| `ad_group_bid_modifier` | Bid adjustments at ad group level |

### Performance Views

| Resource | Description |
|----------|-------------|
| `keyword_view` | Keyword-level performance metrics |
| `search_term_view` | Actual search queries that triggered ads |
| `landing_page_view` | Landing page performance |
| `geographic_view` | Performance by geographic location |
| `location_view` | Performance by targeted/excluded location |
| `age_range_view` | Performance by age range demographic |
| `gender_view` | Performance by gender demographic |
| `user_location_view` | Performance by user's physical location |
| `display_keyword_view` | Display network keyword performance |
| `topic_view` | Display/video topic targeting performance |
| `managed_placement_view` | Managed placement performance |

### Conversion & Attribution

| Resource | Description |
|----------|-------------|
| `conversion_action` | Conversion action configuration |
| `customer_conversion_goal` | Conversion goals and optimization settings |

### Account & Extensions

| Resource | Description |
|----------|-------------|
| `customer` | Account-level settings |
| `asset` | Account assets (sitelinks, callouts, images) |
| `asset_group` | Performance Max asset groups |
| `asset_group_asset` | Assets within asset groups |

### Change History

| Resource | Description |
|----------|-------------|
| `change_status` | Recent changes to account entities |
| `change_event` | Detailed change history with old/new values |

## Common Fields

### Campaign Fields

| Field | Type | Description |
|-------|------|-------------|
| `campaign.id` | INT64 | Unique campaign ID |
| `campaign.name` | STRING | Campaign name |
| `campaign.status` | ENUM | `ENABLED`, `PAUSED`, `REMOVED` |
| `campaign.advertising_channel_type` | ENUM | `SEARCH`, `DISPLAY`, `SHOPPING`, `VIDEO`, `PERFORMANCE_MAX` |
| `campaign.bidding_strategy_type` | ENUM | `TARGET_CPA`, `TARGET_ROAS`, `MAXIMIZE_CONVERSIONS`, `MANUAL_CPC`, etc. |
| `campaign.campaign_budget` | RESOURCE | Budget resource name |
| `campaign.start_date` | DATE | Campaign start date |
| `campaign.end_date` | DATE | Campaign end date |
| `campaign.serving_status` | ENUM | `SERVING`, `NONE`, `ENDED`, `PENDING`, `SUSPENDED` |
| `campaign.target_cpa.target_cpa_micros` | INT64 | Target CPA in micros |
| `campaign.target_roas.target_roas` | DOUBLE | Target ROAS as a ratio |

### Ad Group Fields

| Field | Type | Description |
|-------|------|-------------|
| `ad_group.id` | INT64 | Unique ad group ID |
| `ad_group.name` | STRING | Ad group name |
| `ad_group.status` | ENUM | `ENABLED`, `PAUSED`, `REMOVED` |
| `ad_group.type` | ENUM | `SEARCH_STANDARD`, `DISPLAY_STANDARD`, `SHOPPING_PRODUCT_ADS`, etc. |
| `ad_group.cpc_bid_micros` | INT64 | Default CPC bid in micros |
| `ad_group.target_cpa_micros` | INT64 | Ad group-level target CPA |

### Ad Fields

| Field | Type | Description |
|-------|------|-------------|
| `ad_group_ad.ad.id` | INT64 | Unique ad ID |
| `ad_group_ad.ad.type` | ENUM | `RESPONSIVE_SEARCH_AD`, `EXPANDED_TEXT_AD`, etc. |
| `ad_group_ad.ad.final_urls` | STRING (repeated) | Landing page URLs |
| `ad_group_ad.status` | ENUM | `ENABLED`, `PAUSED`, `REMOVED` |
| `ad_group_ad.ad.responsive_search_ad.headlines` | MESSAGE (repeated) | RSA headline assets |
| `ad_group_ad.ad.responsive_search_ad.descriptions` | MESSAGE (repeated) | RSA description assets |
| `ad_group_ad.policy_summary.approval_status` | ENUM | `APPROVED`, `DISAPPROVED`, etc. |

### Keyword & Criterion Fields

| Field | Type | Description |
|-------|------|-------------|
| `ad_group_criterion.criterion_id` | INT64 | Criterion ID |
| `ad_group_criterion.keyword.text` | STRING | Keyword text |
| `ad_group_criterion.keyword.match_type` | ENUM | `BROAD`, `PHRASE`, `EXACT` |
| `ad_group_criterion.status` | ENUM | `ENABLED`, `PAUSED`, `REMOVED` |
| `ad_group_criterion.quality_info.quality_score` | INT32 | Quality Score (1-10) |
| `ad_group_criterion.quality_info.creative_quality_score` | ENUM | `BELOW_AVERAGE`, `AVERAGE`, `ABOVE_AVERAGE` |
| `ad_group_criterion.quality_info.post_click_quality_score` | ENUM | Landing page experience |
| `ad_group_criterion.quality_info.search_predicted_ctr` | ENUM | Expected CTR |
| `ad_group_criterion.effective_cpc_bid_micros` | INT64 | Effective CPC bid |
| `ad_group_criterion.position_estimates.first_page_cpc_micros` | INT64 | Estimated first page CPC |

### Search Term Fields

| Field | Type | Description |
|-------|------|-------------|
| `search_term_view.search_term` | STRING | Actual user search query |
| `search_term_view.status` | ENUM | `ADDED`, `EXCLUDED`, `ADDED_EXCLUDED`, `NONE` |

### Metrics

| Field | Type | Description |
|-------|------|-------------|
| `metrics.impressions` | INT64 | Number of impressions |
| `metrics.clicks` | INT64 | Number of clicks |
| `metrics.cost_micros` | INT64 | Cost in micros (divide by 1,000,000) |
| `metrics.ctr` | DOUBLE | Click-through rate |
| `metrics.average_cpc` | DOUBLE | Average CPC in micros |
| `metrics.average_cpm` | DOUBLE | Average CPM in micros |
| `metrics.conversions` | DOUBLE | Conversions |
| `metrics.conversions_value` | DOUBLE | Total conversion value |
| `metrics.cost_per_conversion` | DOUBLE | Cost per conversion in micros |
| `metrics.all_conversions` | DOUBLE | All conversions (including cross-device) |
| `metrics.all_conversions_value` | DOUBLE | All conversions value |
| `metrics.view_through_conversions` | INT64 | View-through conversions |
| `metrics.search_impression_share` | DOUBLE | Search impression share (0.0-1.0) |
| `metrics.search_top_impression_share` | DOUBLE | Top impression share |
| `metrics.search_absolute_top_impression_share` | DOUBLE | Absolute top impression share |
| `metrics.search_budget_lost_impression_share` | DOUBLE | IS lost to budget |
| `metrics.search_rank_lost_impression_share` | DOUBLE | IS lost to rank |
| `metrics.interaction_rate` | DOUBLE | Interaction rate |
| `metrics.interactions` | INT64 | Interactions |
| `metrics.video_views` | INT64 | Video views |
| `metrics.video_view_rate` | DOUBLE | Video view rate |
| `metrics.invalid_clicks` | INT64 | Invalid clicks filtered by Google |

### Segments

| Field | Type | Description |
|-------|------|-------------|
| `segments.date` | DATE | Date (YYYY-MM-DD) |
| `segments.day_of_week` | ENUM | `MONDAY` through `SUNDAY` |
| `segments.month` | DATE | First day of the month |
| `segments.quarter` | DATE | First day of the quarter |
| `segments.year` | INT32 | Year |
| `segments.hour` | INT32 | Hour of day (0-23) |
| `segments.device` | ENUM | `DESKTOP`, `MOBILE`, `TABLET`, `OTHER` |
| `segments.ad_network_type` | ENUM | `SEARCH`, `SEARCH_PARTNERS`, `CONTENT`, `YOUTUBE_SEARCH`, `YOUTUBE_WATCH` |
| `segments.slot` | ENUM | `TOP`, `OTHER` |
| `segments.conversion_action` | RESOURCE | Conversion action resource name |
| `segments.conversion_action_name` | STRING | Conversion action name |
| `segments.conversion_action_category` | ENUM | Conversion action category |
| `segments.click_type` | ENUM | `URL_CLICKS`, `CALLS`, `SITELINKS`, etc. |
| `segments.keyword.info.text` | STRING | Keyword text (in search_term_view) |
| `segments.keyword.info.match_type` | ENUM | Keyword match type |

## WHERE Clause Operators

### Comparison Operators

| Operator | Example |
|----------|---------|
| `=` | `campaign.status = 'ENABLED'` |
| `!=` | `campaign.status != 'REMOVED'` |
| `>` | `metrics.impressions > 100` |
| `<` | `metrics.ctr < 0.02` |
| `>=` | `metrics.clicks >= 10` |
| `<=` | `metrics.cost_micros <= 5000000` |

### Set Operators

| Operator | Example |
|----------|---------|
| `IN` | `campaign.status IN ('ENABLED', 'PAUSED')` |
| `NOT IN` | `campaign.advertising_channel_type NOT IN ('VIDEO', 'DISPLAY')` |
| `CONTAINS ANY` | `campaign.labels CONTAINS ANY ('customers/123/labels/456')` |
| `CONTAINS ALL` | `campaign.labels CONTAINS ALL ('..label1..', '..label2..')` |
| `CONTAINS NONE` | `campaign.labels CONTAINS NONE ('customers/123/labels/456')` |

### String Operators

| Operator | Example |
|----------|---------|
| `LIKE` | `campaign.name LIKE '%Brand%'` |
| `NOT LIKE` | `campaign.name NOT LIKE '%Test%'` |

### Null Checks

| Operator | Example |
|----------|---------|
| `IS NULL` | `ad_group_criterion.quality_info.quality_score IS NULL` |
| `IS NOT NULL` | `ad_group_criterion.quality_info.quality_score IS NOT NULL` |

### Range Operators

| Operator | Example |
|----------|---------|
| `BETWEEN` | `segments.date BETWEEN '2025-01-01' AND '2025-01-31'` |
| `DURING` | `segments.date DURING LAST_30_DAYS` |

### Date Macros (DURING)

| Macro | Description |
|-------|-------------|
| `TODAY` | Today only |
| `YESTERDAY` | Yesterday only |
| `LAST_7_DAYS` | Last 7 days (not including today) |
| `LAST_14_DAYS` | Last 14 days |
| `LAST_30_DAYS` | Last 30 days |
| `LAST_BUSINESS_WEEK` | Monday-Friday of previous week |
| `THIS_WEEK_MON_TODAY` | Monday of this week through today |
| `THIS_WEEK_SUN_TODAY` | Sunday of this week through today |
| `THIS_MONTH` | First day of this month through today |
| `LAST_MONTH` | Entire previous month |

## Common Query Patterns

### Campaign Performance Report

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  campaign.bidding_strategy_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion
FROM campaign
WHERE campaign.status != 'REMOVED'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### Search Terms Report (Negative Keyword Identification)

```sql
SELECT
  search_term_view.search_term,
  search_term_view.status,
  segments.keyword.info.text,
  segments.keyword.info.match_type,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM search_term_view
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
  AND metrics.impressions > 10
ORDER BY metrics.cost_micros DESC
LIMIT 1000
```

Filter for high-cost, zero-conversion terms to build negative keyword lists.

### Quality Score Analysis

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM keyword_view
WHERE campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND ad_group_criterion.quality_info.quality_score IS NOT NULL
  AND segments.date DURING LAST_30_DAYS
ORDER BY ad_group_criterion.quality_info.quality_score ASC
```

### Landing Page Performance

```sql
SELECT
  landing_page_view.unexpanded_final_url,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM landing_page_view
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
  AND metrics.clicks > 0
ORDER BY metrics.clicks DESC
LIMIT 100
```

### Device Breakdown

```sql
SELECT
  campaign.name,
  segments.device,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
ORDER BY campaign.name, segments.device
```

### Geographic Performance

```sql
SELECT
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion
FROM geographic_view
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
  AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

### Ad Copy Performance (RSA Asset-Level)

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad.final_urls,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions
FROM ad_group_ad
WHERE campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
  AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.impressions DESC
```

Asset-level performance:

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad_asset_view.field_type,
  ad_group_ad_asset_view.performance_label,
  asset.text_asset.text,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions
FROM ad_group_ad_asset_view
WHERE campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
ORDER BY ad_group_ad_asset_view.performance_label DESC, metrics.impressions DESC
```

### Budget Utilization / Impression Share

```sql
SELECT
  campaign.name,
  campaign.campaign_budget,
  campaign_budget.amount_micros,
  campaign.bidding_strategy_type,
  metrics.impressions,
  metrics.cost_micros,
  metrics.search_impression_share,
  metrics.search_top_impression_share,
  metrics.search_absolute_top_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND campaign.advertising_channel_type = 'SEARCH'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.search_budget_lost_impression_share DESC
```

### Conversion Action Breakdown

```sql
SELECT
  campaign.name,
  segments.conversion_action_name,
  segments.conversion_action_category,
  metrics.conversions,
  metrics.conversions_value,
  metrics.all_conversions,
  metrics.all_conversions_value,
  metrics.cost_per_conversion
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
  AND metrics.conversions > 0
ORDER BY metrics.conversions DESC
```

### Change History Audit

```sql
SELECT
  change_event.change_date_time,
  change_event.change_resource_type,
  change_event.change_resource_name,
  change_event.resource_change_operation,
  change_event.changed_fields,
  change_event.old_resource,
  change_event.new_resource,
  change_event.user_email
FROM change_event
WHERE change_event.change_date_time DURING LAST_14_DAYS
  AND change_event.change_resource_type IN (
    'CAMPAIGN', 'AD_GROUP', 'AD_GROUP_AD',
    'AD_GROUP_CRITERION', 'CAMPAIGN_BUDGET'
  )
ORDER BY change_event.change_date_time DESC
LIMIT 500
```

## Gotchas and Important Notes

### cost_micros Requires Division

All cost fields are in micros (1/1,000,000 of the currency unit):

```
Actual cost = metrics.cost_micros / 1,000,000
Actual CPC  = metrics.average_cpc / 1,000,000
```

Example: `cost_micros = 5430000` means $5.43.

### Segment + Metric Compatibility

- `segments.conversion_action` — impressions/clicks repeat across each conversion action row. Do not sum them.
- `segments.click_type` — clicks and impressions fragment by click type. Summing overcounts.
- `segments.slot` — only compatible with search campaigns.
- `segments.hour` — cannot be combined with `segments.date` for some resources.
- Check the Google Ads API field compatibility matrix when in doubt.

### Date Range Requirements

- Queries with `metrics.*` fields require a date range (`segments.date DURING ...` or `BETWEEN`).
- Resource-only queries (no metrics) do not need a date range.

### Enum Values

Enum fields must use string constant names:

- **CampaignStatus:** `ENABLED`, `PAUSED`, `REMOVED`
- **AdGroupStatus:** `ENABLED`, `PAUSED`, `REMOVED`
- **AdvertisingChannelType:** `SEARCH`, `DISPLAY`, `SHOPPING`, `VIDEO`, `PERFORMANCE_MAX`, `MULTI_CHANNEL`, `LOCAL`, `SMART`, `HOTEL`, `DISCOVERY`
- **KeywordMatchType:** `BROAD`, `PHRASE`, `EXACT`
- **BiddingStrategyType:** `TARGET_CPA`, `TARGET_ROAS`, `MAXIMIZE_CONVERSIONS`, `MAXIMIZE_CONVERSION_VALUE`, `MANUAL_CPC`, `ENHANCED_CPC`, `TARGET_IMPRESSION_SHARE`
- **Device:** `DESKTOP`, `MOBILE`, `TABLET`, `CONNECTED_TV`, `OTHER`
- **QualityScoreBucket:** `BELOW_AVERAGE`, `AVERAGE`, `ABOVE_AVERAGE`

### Rate Limits

- **Standard access:** 15,000 requests/day, 1,600 operations/minute.
- **Basic access:** 10,000 requests/day.
- Use `SearchStream` for large result sets (one operation regardless of size).

### Other Pitfalls

- **No `OR`:** All WHERE conditions are AND-joined. Use `IN` or separate queries.
- **No joins:** GAQL queries operate on a single resource.
- **No `GROUP BY`:** Aggregation is implicit by selected fields + segments.
- **No aliases:** Cannot use `AS` in GAQL.
- **No arithmetic:** Calculate `cost_micros / 1000000` client-side.
- **Segment auto-grouping:** Adding a segment splits rows by that dimension.
- **Removed resources:** Excluded by default. Filter explicitly to include them.
- **PARAMETERS clause:** `include_drafts = true` for drafts, `omit_unselected_resource_names = true` to reduce response size.

## Resources

- **GAQL Grammar:** https://developers.google.com/google-ads/api/docs/query/grammar
- **Interactive Query Builder:** https://developers.google.com/google-ads/api/fields/v17/overview_query_builder
- **Resource Reference:** https://developers.google.com/google-ads/api/fields/v17/overview
- **Rate Limits:** https://developers.google.com/google-ads/api/docs/best-practices/rate-limits
- **Full Cogny Docs:** https://cogny.com/docs/gaql-reference
