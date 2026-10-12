---
name: search-campaign-audit
description: Search campaign audit for Google Ads (with Microsoft Ads parity) — match types, quality score, negative keyword gaps, search terms, ad strength, RSA asset coverage
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
  - mcp__cogny__mcp__Google_Ads__tool_generate_keyword_ideas
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Bing_Ads__tool_get_ads
  - mcp__cogny__mcp__Bing_Ads__tool_get_keywords
  - mcp__cogny__mcp__Bing_Ads__tool_get_negative_keywords
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_search_term_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_negative_keywords
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Semrush__domain_paid_keywords
  - mcp__cogny__mcp__Semrush__phrase_related
  - mcp__cogny__mcp__Ahrefs__keywords_explorer
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Search Campaign Audit

A deep audit of your Google Ads Search campaigns — the campaign type where you still
control keywords, match types, and ads directly. Finds quality-score drags, wasted
match-type spend, negative gaps, and weak ads.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Campaigns, keywords, QS, search terms, ads | Google Ads (`Google_Ads`) | Microsoft Ads (`Bing_Ads`) | Bing money is in account currency units (not micros); percents are percents; QS components are 1–3 (below / average / above) |
| App Store search terms | — | Apple Search Ads (`Apple_Search_Ads`) | Only for app campaigns; taps and installs, not clicks and conversions |
| Landing-page conversion cross-check | Google Analytics 4 | Plausible | GA4 key events vs Ads conversions; different attribution and counting |
| Keyword gaps and competitor paid terms | Google Ads `tool_generate_keyword_ideas` | Semrush, Ahrefs | Search volumes are estimates and differ between tools |

Call `list_integrations` once, audit every connected search engine, and report them side
by side. Never sum spend across engines with different currencies.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Search Campaign Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads and/or Microsoft Ads (plus GA4,
   Plausible, Semrush or Ahrefs if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but neither `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` nor
`mcp__cogny__mcp__Bing_Ads__tool_get_report` is available, say "connect Google Ads or
Microsoft Ads in Cogny" and stop. An engine that is listed but unhealthy, or whose first read
returns 401/permission denied, gets "reconnect <engine> in Cogny". With only Microsoft Ads
connected, run the "Microsoft Ads" branch of each step.

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

Google Ads money fields are micros (divide by 1,000,000). An empty GAQL result (no rows, or
the tool returns no output) means zero: no matching entities or no activity in the window.
Report it as 0, not as an error.

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

**Microsoft Ads:** `mcp__cogny__mcp__Bing_Ads__tool_list_accounts`, then
`mcp__cogny__mcp__Bing_Ads__tool_get_campaigns` (`account_id`, `campaign_types: ["Search"]`)
and `mcp__cogny__mcp__Bing_Ads__tool_get_report` (`account_id`, `report_type: "campaign"`,
`start_date`, `end_date`). Every `tool_get_report` call below also takes that `account_id`. Impression share columns are `ImpressionSharePercent`,
`ImpressionLostToRankAggPercent` and `ImpressionLostToBudgetPercent`.

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

Quality Score 0 or null means **not scored** (too little traffic), not a bad score. Count
those keywords separately as "not scored" and leave them out of the QS ≤4 counts and the
average QS.

Flag:
- Quality Score ≤4 (1–4, excluding unscored) on spending keywords — and read the three components to say *why*
  (`creative_quality_score` = ad relevance, `post_click_quality_score` = landing page,
  `search_predicted_ctr` = expected CTR)
- High-spend keywords with **zero conversions**
- Duplicate keywords across ad groups (internal auction competition)

**Microsoft Ads:** `tool_get_report` with `report_type: "keyword"`. `QualityScore` is 1–10;
`ExpectedCtr`, `AdRelevance` and `LandingPageExperience` are 1 (below average), 2 (average)
or 3 (above average). Map them to the same three diagnoses. Match type is `BidMatchType`.

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

**Microsoft Ads:** `tool_get_report` with `report_type: "search_query"`. There is no
"added/excluded" status column, so compare `SearchQuery` against the keyword list from
`tool_get_keywords` (`account_id`, `ad_group_id`) to find harvest candidates. Terms that
waste money on Google usually waste it on Bing too; flag terms negated in one engine only.

**Apple Search Ads (app campaigns only):** `tool_list_acls` for the `org_id`, then
`tool_get_search_term_report` (`org_id`, `campaign_id`, `start_date`, `end_date`). Judge
terms by installs and cost per install, not conversions.

### 5. Negative keyword coverage

Negatives live in three places. Query all three before saying a campaign has none.

```sql
SELECT shared_set.name, shared_set.type, shared_set.member_count
FROM shared_set
WHERE shared_set.type = 'NEGATIVE_KEYWORDS'
```

```sql
SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE
  AND campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
```

```sql
SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = TRUE
  AND campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
```

Flag: no negatives at any level, no shared negative list (campaign/ad-group negatives only
are hard to maintain), brand terms bidding or matching in non-brand campaigns (check the
step 2 keywords and step 4 search terms against the brand name; give their spend),
brand terms not negated in non-brand campaigns, and no
list of perennial junk (`free`, `jobs`, `diy`, `cheap` — adjust to the business).

**Microsoft Ads:** `tool_get_negative_keywords` (`account_id`, `entity_type: "Campaign"`,
`entity_ids`). It returns negatives set on campaigns or ad groups only, not shared lists,
so say so before calling a campaign "unprotected". Apple Search Ads:
`tool_get_campaign_negative_keywords`.

### 6. Ad strength & RSA coverage

```sql
SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type,
  ad_group_ad.ad_strength, ad_group_ad.status, campaign.name,
  metrics.impressions, metrics.conversions
FROM ad_group_ad
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND campaign.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

The query above drops ads with no impressions in the window, so find empty ad groups
without a date range:

```sql
SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status
FROM ad_group
WHERE campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
```

```sql
SELECT ad_group.id, ad_group_ad.ad.id, ad_group_ad.status
FROM ad_group_ad
WHERE campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'
```

An enabled ad group whose `ad_group.id` is absent from the second result has zero enabled ads.

Flag:
- Ad groups with **only one RSA** (no test running)
- `ad_group_ad.ad_strength` of `POOR` or `AVERAGE`
- Any remaining Expanded Text Ads (deprecated)
- Ad groups with zero enabled ads

**Microsoft Ads:** `tool_get_report` with `report_type: "ad"` gives `AdStrength`, `AdType`
and `AdStatus`; `tool_get_ads` (`account_id`, `ad_group_id`) adds editorial status.

### 7. Asset (extension) coverage

Every field you filter on must also be in SELECT, so `campaign.advertising_channel_type`
and `campaign.status` are selected here:

```sql
SELECT campaign.name, campaign.advertising_channel_type, campaign.status,
  campaign_asset.field_type, campaign_asset.status
FROM campaign_asset
WHERE campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
  AND campaign_asset.status = 'ENABLED'
```

Account-level assets apply to every campaign that has none of that type of its own:

```sql
SELECT customer_asset.field_type, customer_asset.status
FROM customer_asset
WHERE customer_asset.status = 'ENABLED'
```

A campaign is covered for a type if it has it at campaign level *or* the account has it.
Flag campaigns missing sitelinks, callouts, or structured snippets at both levels — free real estate
and CTR that most accounts leave on the table.

### 7b. Enhanced when connected: landing pages and keyword gaps

- **Landing-page check (GA4 or Plausible).** For keywords with QS landing-page "below
  average", pull the final URL's sessions and key events: GA4 `tool_list_account_summaries` for the
property, then `tool_run_report`
  (`property_id`, `date_ranges`, `dimensions: ["landingPage", "sessionGoogleAdsKeyword"]`,
  `metrics: ["sessions", "keyEvents"]`) or Plausible `mcp__cogny__mcp__Plausible__breakdown` (`site_id`,
  `dimension: "visit:entry_page"`, `filters` on `visit:utm_source`). A page that converts
  paid traffic far below the site average confirms the QS diagnosis.
- **Keyword gaps.** Seed `mcp__cogny__mcp__Google_Ads__tool_generate_keyword_ideas`
  (`customer_id`, `seed_keywords` or `page_url`) with the top converting terms. If nothing
  converted in the window, seed it with the 5–10 highest-spend relevant search terms from
  step 4 (or the top-spend keywords from step 2) and say the seeds are spend-based. If Semrush
  is connected, `domain_paid_keywords` (`domain`, `database`) on 1–3 competitors shows
  terms they buy that you don't; Ahrefs `keywords_explorer` (`keywords`, `country`) gives
  volume and CPC. Report only gaps with real intent; name the source of every volume.

### 8. Score and report

```
Search Campaign Audit — [Account Name]
Search Score: X/100  ·  30-day spend: [X]  ·  Conv: [X]  ·  CPA: [X]
(one line per engine, each in its own currency: "Google Ads: SEK 41,200 · Microsoft Ads: SEK 6,900")

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

Cloud uses `create_ticket` with the same content, fields mapped per section 2 of the routing guide.

Action types: `keyword_optimization`, `negative_keyword`, `match_type`,
`creative_refresh`, `campaign_optimization`, `bidding_strategy`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Read the QS components, don't just report the number.** The fix differs for ad
   relevance vs landing page vs CTR.
2. **Zero-conversion search-term spend is the headline waste figure** — total it.
3. **Quote real numbers**: QS values, match-type splits, term costs.
4. **Read-only.** Never add negatives or pause keywords — recommend, don't act. Write tools
   (`Google_Ads` `tool_add_negative_keywords_to_campaign`, `Bing_Ads` `tool_add_negative_keywords`)
   are used only if the user asks, and the skill asks first.
5. **One row per engine.** Google and Microsoft numbers sit side by side, never summed
   across currencies; name the engine on every figure.
