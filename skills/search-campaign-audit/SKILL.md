---
name: search-campaign-audit
description: Google Ads Search campaign audit — match types, quality score, negative keyword gaps, search terms, ad strength, RSA asset coverage
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

# Search Campaign Audit

A deep audit of your Google Ads Search campaigns — the campaign type where you still
control keywords, match types, and ads directly. Finds quality-score drags, wasted
match-type spend, negative gaps, and weak ads.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

If `mcp__cogny__google_ads__tool_execute_gaql` is not available, print the Cogny
sign-up instructions (see `/google-ads-audit`) and stop.

## Usage

`/search-campaign-audit` — audit every Search campaign in the account
`/search-campaign-audit Brand - Exact` — audit one campaign by name or id

## Benchmarks

| Signal | Poor | OK | Good |
|--------|------|-----|------|
| Quality Score | ≤4 | 5–6 | 7–10 |
| Ad Strength | Poor / Average | Good | Excellent |
| Search term relevance | <50% spend on intent terms | 50–75% | >75% |
| Impression share lost (rank) | >40% | 20–40% | <20% |

## Steps

### 1. Find the Search campaigns

```sql
SELECT campaign.id, campaign.name, campaign.status,
  campaign.bidding_strategy_type, campaign_budget.amount_micros,
  metrics.cost_micros, metrics.conversions, metrics.conversions_value,
  metrics.search_impression_share, metrics.search_rank_lost_impression_share,
  metrics.search_budget_lost_impression_share
FROM campaign
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

Flag campaigns losing >40% impression share to rank (quality/bids) or to budget.

### 2. Keyword performance & quality score

```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  campaign.name, ad_group.name,
  metrics.cost_micros, metrics.conversions, metrics.clicks, metrics.impressions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

Flag:
- Quality Score ≤4 on spending keywords — and read the three components to say *why*
  (`creative_quality_score` = ad relevance, `post_click_quality_score` = landing page,
  `search_predicted_ctr` = expected CTR)
- High-spend keywords with **zero conversions**
- Duplicate keywords across ad groups (internal auction competition)

### 3. Match-type mix

Aggregate spend and conversions by `match_type` (EXACT / PHRASE / BROAD).

Flag:
- Broad match taking a large share of spend with a worse CPA than exact/phrase —
  broad only works well with Smart Bidding *and* tight negatives
- Accounts that are 100% exact (likely missing volume) or 100% broad (likely bleeding)

### 4. Search term analysis

```sql
SELECT search_term_view.search_term, search_term_view.status, campaign.name,
  ad_group.name, metrics.cost_micros, metrics.conversions, metrics.clicks
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

Flag:
- Irrelevant / off-intent terms with spend — negative keyword candidates
- Converting terms with status `NONE` (not yet added as keywords) — harvest them
- The total cost of zero-conversion terms — this is the headline waste number

### 5. Negative keyword coverage

```sql
SELECT shared_set.name, shared_set.type, shared_set.member_count
FROM shared_set
WHERE shared_set.type = 'NEGATIVE_KEYWORDS'
```

Flag: no shared negative list, brand terms not negated in non-brand campaigns, and no
list of perennial junk (`free`, `jobs`, `diy`, `cheap` — adjust to the business).

### 6. Ad strength & RSA coverage

```sql
SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type,
  ad_group_ad.ad_strength, ad_group_ad.status, campaign.name,
  metrics.impressions, metrics.conversions
FROM ad_group_ad
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND ad_group_ad.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

Flag:
- Ad groups with **only one RSA** (no test running)
- `ad_group_ad.ad_strength` of `POOR` or `AVERAGE`
- Any remaining Expanded Text Ads (deprecated)
- Ad groups with zero enabled ads

### 7. Asset (extension) coverage

```sql
SELECT campaign.name, campaign_asset.field_type, campaign_asset.status
FROM campaign_asset
WHERE campaign.advertising_channel_type = 'SEARCH'
```

Flag campaigns missing sitelinks, callouts, or structured snippets — free real estate
and CTR that most accounts leave on the table.

### 8. Score and report

```
Search Campaign Audit — [Account Name]
Search Score: X/100  ·  30-day spend: [X]  ·  Conv: [X]  ·  CPA: [X]

| Campaign | Spend | Conv | CPA | Avg QS | IS lost (rank) |
|----------|-------|------|-----|--------|----------------|

🔴 Critical   — QS ≤4 on top spenders, zero-conversion keyword spend
🟡 Important  — broad-match bleed, single-RSA ad groups, missing negatives
🟢 Optimization — extensions, search-term harvesting

Top 3 Actions:
1. [Highest $ impact]
2. ...
3. ...
```

### 9. Record findings

```json
{
  "title": "Quality Score 3 on 'crm software' — $620/mo at a 2.4x CPA penalty",
  "body": "'crm software' (phrase) has QS 3: ad relevance below average, landing page below average. It spent $620 last month at $94 CPA vs $39 account average. Tighten the ad group to one theme, mirror the keyword in RSA headlines, and point it at a dedicated landing page.",
  "action_type": "keyword_optimization",
  "expected_outcome": "QS to 6+, CPC down 20-35%, CPA toward account average",
  "estimated_impact_usd": 380,
  "priority": "high"
}
```

Action types: `keyword_optimization`, `negative_keyword`, `match_type`,
`creative_refresh`, `campaign_optimization`, `bidding_strategy`.

## Critical rules

1. **Read the QS components, don't just report the number.** The fix differs for ad
   relevance vs landing page vs CTR.
2. **Zero-conversion search-term spend is the headline waste figure** — total it.
3. **Quote real numbers**: QS values, match-type splits, term costs.
4. **Read-only.** Never add negatives or pause keywords — recommend, don't act.
