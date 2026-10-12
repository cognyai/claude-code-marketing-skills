---
name: performance-memo
description: The Monday memo a sharp analyst would write — joins spend on every ad platform to qualified calls, deals, revenue, refunds and churn per campaign ID, catches cheap customers who churn, and ends every line in a decision — keep, kill, change or test
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [fibbler, hubspot, pipedrive, upsales, stripe, fortnox, shopify, woocommerce, abicart, litium, google-ads, meta-ads, linkedin-ads, bing-ads, tiktok-ads, x-ads, reddit-ads, snapchat-ads, apple-search-ads, openai-ads, bidtheatre, ga4, plausible, posthog, mixpanel, growthbook]
user-invocable: true
argument-hint: "[week|month] [--compare]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__mcp__app-fibbler-co__get_deal_attribution_summary
  - mcp__cogny__mcp__app-fibbler-co__get_cross_channel_performance
  - mcp__cogny__mcp__app-fibbler-co__get_influenced_deals
  - mcp__cogny__mcp__app-fibbler-co__get_deal_campaign_breakdown
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__Stripe__stripe_api_search
  - mcp__cogny__mcp__Stripe__stripe_api_details
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__mcp__Fortnox__list_invoices
  - mcp__cogny__mcp__Fortnox__list_customers
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_analytics
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__TikTok_Ads__tool_get_insights
  - mcp__cogny__mcp__X_Ads__tool_get_analytics
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_reporting
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_stats
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_account_spend
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_account
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_insights
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_conversion_insights
  - mcp__cogny__mcp__Bidtheatre__list_campaigns
  - mcp__cogny__mcp__Bidtheatre__get_report
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Plausible__aggregate
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_opportunities
  - mcp__cogny__mcp__Upsales__list_appointments
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__Shopify__tool_list_customers
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__mcp__WooCommerce__list_order_refunds
  - mcp__cogny__mcp__Abicart__get_sales_summary
  - mcp__cogny__mcp__Litium__get_sales_summary
  - mcp__cogny__mcp__PostHog__list_projects
  - mcp__cogny__mcp__PostHog__list_insights
  - mcp__cogny__mcp__PostHog__get_insight
  - mcp__cogny__mcp__Mixpanel__list_funnels
  - mcp__cogny__mcp__Mixpanel__get_funnel
  - mcp__cogny__mcp__Mixpanel__get_retention
  - mcp__cogny__mcp__GrowthBook__list_experiments
  - mcp__cogny__mcp__GrowthBook__get_experiment_results
---

# Performance Memo

Every Monday, a short memo the way a sharp analyst would write it:

> "The profitability-review page converted at 4%, and half those leads were too small to serve.
> The dinner ad has the lowest cost per qualified call. Retargeting has spent $3,000 and produced
> two sales conversations."

**Every line ends in a decision for you: keep, kill, change or test.** It follows the money all
the way through to retention, refunds and profit, because a campaign that brings in cheap customers who
churn in sixty days looks great on a dashboard and quietly loses you money.

**Requires:** Cogny ($9/mo). It's best with `/campaign-ledger` running. Without IDs it falls back
in this order, labelling the confidence of every line:
1. **Campaign IDs** in the ledger (high)
2. **fibbler** channel-level attribution (medium). Needs fibbler with two paid channels; it refuses or returns zeros otherwise.
   If fibbler refuses, returns zeros **or fails auth** (401 / `Forbidden`), drop to tier 3 and name it in "Data problems".
3. **Platform-reported conversions + GA4 by `sessionSourceMedium`** (low). Always cross-check: if a
   platform claims conversions GA4 can't see (e.g. X sign-ups while GA4 shows untagged
   `t.co / referral` with 0 key events), that mismatch is a memo line in itself.

Without a campaign evidence bar, use a default: **conclusive only with ≥10 conversions and ≥14 days**.

## Usage

- `/performance-memo` — last 7 days vs prior 7, plus 90-day outcomes for anything that's closing
- `/performance-memo month --compare`

Schedule: Monday 07:30, after `/customer-language` and `/campaign-ledger sync`.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Performance Memo needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ad platforms plus a CRM or Stripe (fibbler and GA4 help with attribution).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Steps

### 1. Load context

`brain/campaigns/ledger`, every live campaign folder (for its **evidence bar**),
`brain/company/customer-fit` (to judge lead quality), `brain/experiments/log`, and last week's memo.

### 2. Spend and delivery (by campaign ID where possible)

Run `/campaign-ledger sync` logic, or read the ledger if it was synced today. Compute explicit
windows: this week = the 7 full days ending yesterday, prior week = the 7 days before that.
Get account IDs first (`list_accessible_accounts`, `list_ad_accounts`, `list_accounts`, `list_advertisers`).
These double as the **health check**: `list_integrations` misses revoked tokens, so treat a 401, Forbidden
or scope error on that cheap read as 🔴 "reconnect <integration>", name it, and don't retry. If an expected tool
is missing, `refresh_mcp_discovery` once; new tools need a client reconnect, so use the fallback and mark the source ⚠.
- Google: GAQL on `campaign` with `customer.currency_code`, `segments.date BETWEEN '<start>' AND '<end>'`
  for each window, and `AND metrics.impressions > 0`
- Meta `get_insights` `level: "campaign"` with `time_range_since/until`. No output at all means no delivery, not an error.
- LinkedIn `get_analytics`; Bing `get_report` with start/end dates; TikTok `get_insights`
- X: `get_campaigns` for the IDs, then `get_analytics` with `granularity: "TOTAL"`
- Reddit `tool_get_reporting(ad_account_id, start_date, end_date, level: "campaign")`
- Snapchat `tool_get_stats(entity_id: <campaign id>, start_time, end_time, level: "campaign")` per campaign
- Apple Search Ads `tool_get_account_spend(org_id, start_date, end_date)`, plus `tool_get_campaign_report` for the top campaigns
- ChatGPT ads (OpenAI Ads) `tool_get_insights(aggregation_level: "campaign", start_date, end_date)` and
  `tool_get_conversion_insights` for conversions
- Bidtheatre: the most recent `get_report` the user has, because creating a report is a write (ask first)

Report spend in each account's currency. **Never sum across currencies** unless you state the FX rate.

### 3. Leads and lead quality

- GA4 `run_report` (property id from `list_account_summaries`): key events by `sessionCampaignName`, last
  7 days vs prior 7. If key events are near zero **site-wide** (about 1 a week or fewer) while traffic is
  normal, report "GA4 conversion tracking looks broken" under Data problems. Don't judge campaigns on it. Without GA4:
  Plausible `breakdown(site_id, dimension: "visit:utm_campaign", metrics: ["visitors","events"])`
  with goal filters.
- HubSpot `contacts` created in each window (`createdate`), with `hs_analytics_source`,
  `hs_analytics_source_data_1`, `hs_analytics_source_data_2` (original `utm_campaign` for paid
  traffic), `lifecyclestage` and associated company firmographics. This is the lead count by source
  and campaign, and it can be matched to campaign IDs.
- HubSpot `deals` created in the window (`createdate`), with the `campaign_id` deal property if it
  exists, otherwise the associated contact's original source. Dedupe by company and report raw vs unique.
  Anything that can't be matched is marked unattributed. For each lead, check it against
  `customer-fit`. **Too small** or **wrong segment** gets counted separately, because a page that converts at 4%
  with half the leads unserviceable converts at 2%.
- HubSpot `meetings` in the window (`hs_meeting_start_time`, `hs_meeting_outcome = COMPLETED`)
  associated with new contacts or deals: qualified calls held. Exclude vendor, partner and internal meetings.
- **Pipedrive** instead: `list_deals(updated_since)` filtered by `add_time` in the window, and
  `list_activities(done: true)` of type meeting for qualified calls. **Upsales** instead: `list_orders` /
  `list_opportunities` with `filters=[{"field":"regDate","comparator":"gte","value":…}]`, and `list_appointments`
  for meetings. Check field names once with `get_metadata`.
- **Self-serve products:** activation is the lead-quality signal. PostHog (`list_projects` →
  `list_insights(search: "activation")` → `get_insight`) or Mixpanel (`list_funnels` → `get_funnel`, `get_retention`)
  gives activation rate by `utm_campaign` / initial referrer when the insight breaks down by it. Say when it doesn't.

### 4. Pipeline and revenue

- fibbler `get_deal_attribution_summary` (`time_period: "90d"`, `compare: true`): pipeline, revenue,
  ROAS, cost per opportunity. Use `newDealsCreated` for pipeline and `wonDealsCount` for revenue,
  never `totalInfluencedDeals` as the headline.
- fibbler `get_cross_channel_performance` (`time_period: "90d"`): per-channel cost per influenced deal.
  **Use `totals` for deduplicated counts.** Per-channel deal counts overlap and can't be summed.
  LinkedIn is impression-matched and Google is click-matched, so they aren't like for like. Say so.
- HubSpot open pipeline: `deals` with `hs_is_closed = false`, grouped by `dealstage` (labels from
  `get_properties(deals, dealstage)`) and `deal_currency_code`. Never add up currencies. Pass
  `crm: "hubspot"` to the fibbler tools.

### 5. Retention, refunds, profit (the part dashboards miss)

For customers won 60–180 days ago, attributed to a campaign ID or channel:
- **Stripe** (`stripe_api_read`):
  - `GetSubscriptions` with `status: "all"` and a `created` window (or `GetSubscriptionsSearch`) gives the
    cohort, which is the **denominator**. Churn = cohort members with `canceled_at` within 60 days of
    `start_date` ÷ cohort size. Canceled subscriptions alone can't give a rate.
  - **Trials aren't churn.** A subscription with `ended_at == trial_end` never paid: count it as a trial
    that didn't convert, report it separately, and keep it out of the churn numerator and denominator.
  - Paginate with `starting_after` (the last id of the previous page) while `has_more` is true. Each page
    is ~370k characters, so aggregate outside the main context (a subagent or Cloud script that returns only
    counts per plan and cohort month) instead of reading pages into the memo.
  - `GetRefunds` with `created.gte` for refunds.
  - Group by plan (`items.data[].price.unit_amount` + currency). Subscription metadata may come back
    `[REDACTED]`, so per-campaign churn needs a source stored somewhere readable. If it isn't, report
    churn by plan and recommend storing the campaign or UTM in checkout metadata.
- **Fortnox** (invoice-billed businesses): `list_invoices` with `filter: "unpaidoverdue"` and
  `fromdate` set to the window. Flag campaigns whose customers don't pay.
- **Stores** (ecommerce instead of subscriptions): revenue and refunds per window, in the store's
  base currency:
  - Shopify `tool_list_orders(query_filter: "created_at:>=<start> created_at:<=<end>")` for revenue
    (the tool returns no UTM fields, so attribution comes from GA4 or Plausible), and `tool_list_customers`
    for the repeat rate (`numberOfOrders > 1`).
  - WooCommerce `get_sales_report(date_min, date_max)`, `list_orders(after, before)`, `list_order_refunds(order_id)`
  - Abicart / Litium `get_sales_summary(start_date, end_date)`
  For ecommerce, "retained" means **repeat purchase within 90 days**, so compute cost per repeat customer.

Compute **cost per retained customer** = spend ÷ customers still active at 60 days. Flag any
campaign that ranks well on CPA but badly on this.

### 5b. What was already tested (optional)

GrowthBook `list_experiments(status: "stopped")` + `get_experiment_results(experiment_id)` for
experiments that ended in the window. Add winners and losers to the memo and to
`brain/experiments/log`, so no agent re-tests a settled question.

### 6. Judge against the evidence bar

For each campaign, compare against the bar in its folder. Label it **conclusive** or **not yet**
(spend, days or sample size under the bar). With fewer than ~10 conversions, say the sample is
small explicitly; don't let one lucky deal become a strategy.

### 7. Write the memo

`write_context_node` at `brain/memos/performance/<YYYY-MM-DD>`:

```markdown
# Performance memo — week of YYYY-MM-DD
Sources: Google ✅ Meta ✅ LinkedIn ✅ Bing ✅ TikTok ⚪ X ✅ Reddit ⚪ Snapchat ⚪ Apple ⚪ ChatGPT ads ⚪ · fibbler ✅ · CRM (HubSpot) ✅ · Stripe ✅ · Store ⚪ · PostHog ⚪ · GrowthBook ⚪
Attribution confidence: 62% of spend ID-tagged (high) · rest via fibbler (medium)

## The short version (≤5 lines, each ending in a decision)
1. BK014 calculator page converts 4.1%, but 48% of leads are under the $1M floor → **CHANGE**: add a revenue question to the form.
2. BK014_dinner-angle has the lowest cost per qualified call ($92) → **KEEP**, and test a founder version.
3. Retargeting (BK009): $3,020 spent, 2 sales conversations → **KILL**.
4. LinkedIn-sourced customers from Q2 churned 3× faster than search-sourced ones by day 60 → **TEST**: tighten targeting to 51–200 employees.
5. Amazon-trigger list booked 5 calls from 22 emails → **KEEP** (small sample).

## Campaign table
| ID | Spend | Leads (in-fit) | Qual. calls | Deals | Revenue | 60d churn | Cost/qual call | Cost/retained cust | Bar met? | Call |

## Channel view (fibbler, 90d, deduplicated totals)
## What changed vs last week
## Not conclusive yet
## Data problems this week
```

### 8. Queue the decisions

One `create_ticket` per **kill** or **change** (a keep needs no ticket), each with the evidence and
`estimated_impact_usd`. Interactively, walk the user through the short version and record each
call in `brain/experiments/log`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

0. **Ticket titles start with `[ME:performance-memo]`.** Amounts in `estimated_impact_usd` must be
   converted to USD; give the native amount in the body.
1. **Every line ends in keep / kill / change / test.** A number without a decision doesn't belong in the memo.
2. **Follow the money to retention.** CPA alone is not a verdict.
3. **Never sum overlapping attribution.** Use fibbler `totals`.
4. **State sample size and confidence.** "Small sample" is a finding.
5. **Name every source that failed.** A missing platform can make a week look profitable.
6. **Read-only.** Decisions go to the queue; this skill changes nothing.
