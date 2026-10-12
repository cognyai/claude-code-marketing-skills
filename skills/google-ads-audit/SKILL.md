---
name: google-ads-audit
description: Comprehensive Google Ads account audit (Microsoft Ads side by side when connected) — campaign structure, budget pacing, conversion tracking, wasted spend — across every campaign type, ranked by estimated $ impact
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads, microsoft-ads]
user-invocable: true
argument-hint: "[full|campaigns|budget|tracking|negatives]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  - mcp__cogny__mcp__Google_Ads__tool_get_reporting_view_doc
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_negative_keywords
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Google Ads Audit

A one-time, account-wide Google Ads health audit using live data via Cogny's MCP
server. Covers every campaign type, scores the account out of 100, and routes you to
the right campaign-type skill for deeper drill-down.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Campaign overview, pacing, waste | Google Ads | Microsoft Ads (`Bing_Ads` `tool_get_report`) | Bing money is account-currency units, not micros; percents are percents |
| Conversion tracking structure | Google Ads (`conversion_action`) | — | Microsoft Ads conversion goals aren't exposed; check volume only |
| Are the conversions real? | Shopify / WooCommerce orders | GA4 key events and revenue | Store = actual paid orders; Ads = attributed, modelled, can double-count |

Call `list_integrations` once. Audit Google Ads in full; if Microsoft Ads is connected,
add its overview, pacing and waste numbers as a separate block. Never sum the two.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Google Ads Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads (and Microsoft Ads, GA4, Shopify or
   WooCommerce if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` is missing, say
"connect Google Ads in Cogny" (or "reconnect Google Ads in Cogny" if it's listed but unhealthy
or a read returns 401/permission denied) and stop. Do not guess at numbers.

## Usage

`/google-ads-audit` — full account audit
`/google-ads-audit campaigns` — campaign structure + performance only
`/google-ads-audit budget` — budget pacing only
`/google-ads-audit tracking` — conversion tracking sanity only
`/google-ads-audit negatives` — account negatives + exclusions only

## Approach

This is the **account-level** audit — it finds structural problems and wasted spend
across the whole account. For campaign-type depth (asset groups, keywords, feeds,
audiences) it points you to `/pmax-audit`, `/search-campaign-audit`,
`/shopping-campaign-audit`, or `/demand-gen-audit`.

All money fields come back in micros — divide `cost_micros` etc. by 1,000,000.

An empty GAQL result (no rows, or the tool returns no output) means zero: no matching
entities or no activity in the window. Report it as 0, not as an error or missing data.

## Steps

### 1. Account discovery

```
tool_list_accessible_accounts
```

If multiple accounts are accessible, list them and ask which to audit. Then read the
account name and currency:

```sql
SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone
FROM customer
```

Report every Google Ads money figure in `customer.currency_code`.

### 2. Campaign overview by channel type (last 30 days)

```sql
SELECT customer.currency_code, campaign.name, campaign.status,
  campaign.advertising_channel_type, campaign.bidding_strategy_type,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value, metrics.clicks, metrics.impressions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

Build a per-channel-type summary (Search / Performance Max / Shopping / Display /
Video / Demand Gen): total spend, conversions, CPA, ROAS (`conversions_value / cost`).

**Microsoft Ads (if connected):** `mcp__cogny__mcp__Bing_Ads__tool_list_accounts`, then
`tool_get_campaigns` (`account_id`, `campaign_types: ["Search", "Shopping", "PerformanceMax", "Audience"]`)
and `tool_get_report` (`account_id` from `tool_list_accounts`, `report_type: "campaign"`,
`start_date`, `end_date`). Every `tool_get_report` call needs `account_id`. Build the same
per-type summary from `Spend`, `Conversions`, `Revenue`, `CampaignType`. Many accounts
import Google campaigns into Microsoft Ads; flag imported campaigns with zero conversions
or a CPA more than 2x the Google equivalent.

Flag:
- Campaigns spending >5% of account budget with **zero conversions**
- `MAXIMIZE_CONVERSIONS` / `TARGET_CPA` campaigns with <15 conversions/30d (too little
  data for the bidding strategy to learn)
- Multiple campaigns of the same type competing for the same theme (self-competition)
- Enabled campaigns with zero spend (broken, or budget/targeting starved)

### 3. Conversion tracking sanity

**You must run BOTH queries below before flagging anything in this section.**
Structure alone (which actions exist, which are `primary_for_goal`) tells you nothing
about what is actually driving the bidding signal. A "Primary" action with zero recent
volume is harmless; a "Secondary" action can be a deliberate dedup choice. Always
cross-reference the structure against actual conversion volume per action.

**3a. Structure — which conversion actions exist:**

```sql
SELECT conversion_action.name, conversion_action.status, conversion_action.type,
  conversion_action.category, conversion_action.counting_type,
  conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric
FROM conversion_action
```

**3b. Volume — which actions are actually firing (last 30 days):**

```sql
SELECT segments.conversion_action_name, segments.conversion_action_category,
  metrics.all_conversions, metrics.all_conversions_value,
  metrics.conversions, metrics.conversions_value
FROM customer
WHERE segments.date DURING LAST_30_DAYS
```

An empty result here means **0 conversions for every action** in the window. Go straight
to 3c and report it as zero volume, not as a failed query.

Then join: for every conversion action with non-trivial volume, note whether it is
Primary or Secondary, and whether `metrics.conversions` (the bidding signal) or only
`metrics.all_conversions` (the reporting signal) is counting it.

**3c. Reconcile against account totals.** Pull account-level `metrics.conversions`
and `metrics.conversions_value` for the same window — the sum across Primary actions
in 3b should match (within rounding). If it does, the `metrics.conversions` figure is
the real booking/purchase/lead action and bidding is grounded in real value. **State
this explicitly in the report before making any tracking claim.**

Flag (each must be backed by a number from 3b, not a guess from 3a):
- **No primary action has volume in the last 30 days** — bidding really is flying
  blind. (Note: a Primary action with zero recent volume is harmless, not broken.)
- A high-volume real revenue action (purchase, booking, qualified lead) is Secondary
  while a low-value proxy (page view, "Lokala åtgärder", "Detail product page view")
  is the only Primary — *that* is the "bidding on page views" pattern.
- `MANY_PER_CLICK` counting on a lead-gen action with meaningful volume (double-counts
  leads; usually should be `ONE_PER_CLICK`).
- Two near-duplicate Primary actions both firing on the same event (e.g. on-site
  booking + GA4 booking both Primary → double-counted bid signal).
- `REMOVED` / `HIDDEN` actions still receiving conversions.

**3d. Enhanced when connected: check against real sales.** For ecommerce, pull the
same 30 days from the store: Shopify `mcp__cogny__mcp__Shopify__tool_list_orders`
(`query_filter: "created_at:>=YYYY-MM-DD financial_status:paid"`, paginate with `after`)
or WooCommerce `mcp__cogny__mcp__WooCommerce__get_sales_report` (`date_min`, `date_max`).
For lead gen or as a second view, find the property with GA4 `tool_list_account_summaries`,
then `tool_run_report` (`property_id`, `date_ranges`,
`dimensions: ["sessionGoogleAdsCampaignName"]`, `metrics: ["sessions", "keyEvents", "purchaseRevenue"]`).
Keep `sessions` in the list: GA4 drops rows where every requested metric is 0, so without it
campaigns with zero key events and zero revenue vanish instead of showing as 0.
Report as a ratio, never as a correction: "Google Ads purchase value = 1.4x Shopify paid
revenue for the period." If Ads-reported purchase value exceeds total store revenue, that's
a tracking finding (double counting or a wrong value), backed by both numbers. Paid-order
counts from the store are the ground truth; GA4 and Ads both attribute.

**Do NOT flag:**
- A gap between `all_conversions` and `conversions`, by itself. That gap is just the
  pile of Secondary actions (store visits, GA4 echoes of an on-site action, local
  actions, contacts, etc.) — it is often correct and intentional. Only flag if a
  *high-value, non-duplicate* action is sitting in Secondary.
- View-through / page-view actions marked `primary_for_goal = true` if they have
  ~0 conversions in 3b — they cost nothing, so they are not polluting bidding.
- A Secondary GA4 purchase when on-site purchase/booking is Primary — that is the
  textbook dedup pattern, not a bug.

### 4. Budget pacing (last 7 days)

```sql
SELECT campaign.name, campaign.status, campaign_budget.amount_micros,
  metrics.cost_micros, metrics.impressions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND campaign.status = 'ENABLED'
```

For each campaign compute average daily spend vs daily budget.

Flag:
- Campaigns consistently capped at ~100% of daily budget while converting profitably
  (budget-limited — leaving volume on the table)
- Campaigns spending <50% of budget (delivery problem: bids, targeting, or quality)

### 5. Account negatives & exclusions

Negatives live in three places. Query all three before saying an account has none.

**Shared lists:**

```sql
SELECT shared_set.name, shared_set.type, shared_set.status, shared_set.member_count
FROM shared_set
```

**Campaign-level negatives:**

```sql
SELECT campaign.name, campaign.advertising_channel_type,
  campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE
  AND campaign.status = 'ENABLED'
```

**Ad-group-level negatives:**

```sql
SELECT campaign.name, ad_group.name,
  ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = TRUE
  AND campaign.status = 'ENABLED'
```

**Brand terms in non-brand campaigns** (keywords and the search terms from step 6):

```sql
SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
  metrics.cost_micros, metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
```

Treat a campaign as brand if its name says so (e.g. contains "brand"). In every other
campaign, match keyword text and search terms against the brand name and its common
misspellings.

Flag:
- No negatives at any of the three levels on Search campaigns
- No negative keyword lists shared across Search campaigns (campaign- or ad-group-level
  negatives only — works, but hard to maintain)
- Brand terms bidding or matching inside non-brand campaigns, with their spend (inflates
  non-brand performance and cannibalises the brand campaign); the fix is the brand name as a
  negative in non-brand campaigns
- For Performance Max / Display: missing account-level placement and content
  exclusions (brand-safety + waste risk)

Microsoft Ads: `tool_get_negative_keywords` (`account_id`, `entity_type: "Campaign"`,
`entity_ids`) covers campaign-level negatives only, not shared lists.

### 6. Wasted spend scan (last 30 days)

```sql
SELECT search_term_view.search_term, campaign.name, campaign.advertising_channel_type,
  metrics.cost_micros, metrics.conversions, metrics.clicks
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

Sum the cost of terms with **zero conversions and meaningful spend** — this is the
headline "wasted spend" number and the source of the largest `estimated_impact_usd`.

Microsoft Ads: `tool_get_report` with `account_id` and `report_type: "search_query"`; total zero-conversion
`Spend` separately and report it in the Microsoft account's currency.

### 7. Score and report

```
Google Ads Audit — [Account Name]
Health Score: X/100  ·  30-day spend: [X]  ·  Conversions: [X]  ·  CPA: [X]
[Microsoft Ads, if connected: spend · conversions · CPA, own currency, not scored]
[Ads-reported vs store/GA4 revenue ratio, if a store or GA4 is connected]

Score breakdown:
  Account structure ...... X/20
  Conversion tracking .... X/25   (weighted highest — everything depends on it)
  Budget efficiency ...... X/20
  Wasted spend control ... X/20
  Negatives & exclusions . X/15

By campaign type:
| Type          | Spend | Conv | CPA | ROAS | Drill-down skill        |
|---------------|-------|------|-----|------|-------------------------|
| Performance Max | ... | ...  | ... | ...  | /pmax-audit             |
| Search          | ... | ...  | ... | ...  | /search-campaign-audit  |
| Shopping        | ... | ...  | ... | ...  | /shopping-campaign-audit|
| Demand Gen      | ... | ...  | ... | ...  | /demand-gen-audit       |

🔴 Critical
- ...
🟡 Important
- ...
🟢 Optimization
- ...

Top 3 Actions:
1. [Highest $ impact — estimated savings/lift]
2. ...
3. ...

Run next: [the campaign-type skill for the highest-spend type]
```

### 8. Record findings

For every actionable issue, call `mcp__cogny__create_finding`:

```json
{
  "title": "$1,840/mo wasted on zero-conversion search terms",
  "body": "23 search terms spent $1,840 over 30 days with 0 conversions, led by 'free [product]' ($420) and '[competitor] alternative' ($310). Add as negative keywords and create a shared negative list.",
  "action_type": "negative_keyword",
  "expected_outcome": "Reclaim ~$1,800/mo of spend for converting queries",
  "estimated_impact_usd": 1840,
  "priority": "high"
}
```

Cloud uses `create_ticket` with the same content, fields mapped per section 2 of the routing guide.

`estimated_impact_usd` is in USD. If `customer.currency_code` isn't USD, convert the monthly
figure at a current rate and state it in the body ("SEK 18,400/mo ≈ $1,700 at 10.8 SEK/USD").
Keep the account currency everywhere else in the report.

Action types: `campaign_optimization`, `budget_adjustment`, `bidding_strategy`,
`conversion_tracking`, `negative_keyword`, `account_structure`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Conversion tracking is checked first and weighted highest.** A great account on
   broken tracking is a broken account — say so loudly.
2. **Never claim tracking is broken from structure alone.** `primary_for_goal = true`
   on an action only matters if that action *has volume*. Pull conversion volume per
   action (step 3b) and reconcile against account totals (step 3c) *before* writing
   any finding about conversion tracking, CPA basis, or bidding signal quality. If
   `metrics.conversions` reconciles to a real revenue/booking action, say so — don't
   wave at the `all_conversions` gap as if it implies missing primaries.
3. **Quote real numbers**, never benchmarks alone. "CPA is $48" beats "CPA looks high."
4. **One finding per issue**, each with a dollar figure. No vague advice.
5. This skill **reads only**. It never pauses campaigns or changes budgets. Write tools on
   any platform are used only on the user's explicit request, and the skill asks first.
6. **Platform numbers stay per platform.** Google, Microsoft and store figures are shown
   side by side in their own currencies, never added together.
