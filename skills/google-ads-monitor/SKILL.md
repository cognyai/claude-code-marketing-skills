---
name: google-ads-monitor
description: Weekly Google Ads health check (plus Microsoft Ads, Apple Search Ads and ChatGPT ads when connected) — budget pacing, spend spikes, disapproved ads, conversion-tracking breaks, CPA/ROAS swings — with week-over-week deltas
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads, microsoft-ads, apple-search-ads, openai-ads]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Bing_Ads__tool_get_ads
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_report
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_account
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_campaigns
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_insights
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_conversion_insights
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  - WebFetch
---

# Google Ads Monitor

A recurring weekly check that makes sure your ads are still running smoothly. It
catches the things that break quietly — a disapproved ad, tracking that stopped
firing, a campaign that started overspending — and reports week-over-week so you see
trends, not noise.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

Designed to be scheduled weekly via `/loop` or `/schedule`.

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Spend, conversions, CPA/ROAS WoW | Google Ads | Microsoft Ads (`Bing_Ads`), Apple Search Ads, ChatGPT ads (`OpenAI_Ads`) | Google cost is micros; Bing/OpenAI money is account-currency units; Apple reports taps and installs |
| Disapprovals | Google Ads (`policy_summary`) | Microsoft Ads (`tool_get_ads` editorial status) | Apple and OpenAI: check campaign/ad status only |
| Tracking heartbeat | Google Ads `conversion_action` | GA4 key events; Shopify / WooCommerce orders | Platform conversions are attributed; store orders are the ground truth for "did sales really stop" |

Call `list_integrations` once. Run steps 2–6 for every connected ad platform and report
each in its own block. Never add spend across platforms or currencies.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Google Ads Monitor needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads (plus Microsoft Ads, Apple Search
   Ads, ChatGPT ads, GA4, Shopify, WooCommerce or Stripe if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but no search ad platform (`Google_Ads`, `Bing_Ads`, `Apple_Search_Ads`,
`OpenAI_Ads`) is, say "connect Google Ads (or another search ad platform) in Cogny" and stop.
A platform that is listed but unhealthy, or whose first read returns 401/permission denied,
gets "reconnect <platform> in Cogny" and is skipped. With Google Ads missing, run the other
platforms' branches and skip the GAQL queries.

## Usage

`/google-ads-monitor` — weekly health check of the connected account.

For a deep one-time review, run `/google-ads-audit` instead. This skill is the light,
repeatable rhythm; the audit is the full teardown.

## Steps

Google Ads money fields are micros (divide by 1,000,000). An empty GAQL result (no rows, or
the tool returns no output) means zero: no matching rows or no activity in the window. Report
it as 0, not as an error.

### 1. Read the prior snapshot

Call `read_context_node` on `insights/google-ads/monitor/latest` (and
`insights/microsoft-ads/monitor/latest`, `insights/apple-search-ads/monitor/latest`,
`insights/openai-ads/monitor/latest` for the other connected platforms). If it exists, it
holds last week's metrics — every number this week is reported as a delta against it.
If it does not exist, this is the first run: report absolute numbers and note that
deltas start next week.

### 2. Account-level performance (last 7d vs prior 7d)

```sql
SELECT metrics.cost_micros, metrics.conversions, metrics.conversions_value,
  metrics.clicks, metrics.impressions
FROM customer
WHERE segments.date DURING LAST_7_DAYS
```

Repeat with a `BETWEEN` range for the prior 7 days. Compute WoW deltas for spend,
conversions, CPA, ROAS, CTR.

**Other platforms, same two 7-day windows:**

| Platform | Call | Notes |
|----------|------|-------|
| Microsoft Ads | `mcp__cogny__mcp__Bing_Ads__tool_get_report` (`account_id`, `report_type: "campaign"`, `start_date`, `end_date`) | `Spend`, `Conversions`, `Revenue`, `ReturnOnAdSpend`; `Ctr` is a percent |
| Apple Search Ads | `tool_list_acls` → `tool_get_campaigns` → `tool_get_campaign_report` (`org_id`, `campaign_id`, `start_date`, `end_date`, `granularity: "TOTAL"`) | Per campaign; installs and cost per install |
| ChatGPT ads | `mcp__cogny__mcp__OpenAI_Ads__tool_get_insights` (`aggregation_level: "campaign"`, `start_date`, `end_date`) and `tool_get_conversion_insights` | `end_date` must be a completed day |

### 3. Per-campaign movement

```sql
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

Prior week, same campaigns (dates are the 7 days before `LAST_7_DAYS`, i.e. 14 to 8 days ago):

```sql
SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD' AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

Join the two on `campaign.id`. A campaign missing from one week had no activity that week (0).

**Delivery gaps** (daily rows for the current week):

```sql
SELECT campaign.name, segments.date, metrics.impressions, metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND campaign.status = 'ENABLED'
```

Days with zero impressions come back as **missing rows**, not as rows with 0. Compare each
enabled campaign's dates against all 7 days of the window; every absent date is a delivery gap.

🔴 Alert if any campaign:
- Spent >40% more than the prior week
- Dropped to **zero conversions** after converting the week before
- Is capped at its daily budget every day (budget-limited)
- Stopped delivering entirely (zero impressions, still enabled)
- Had delivery gaps: one or more days with zero impressions while enabled (🟡 for a single
  day, 🔴 for two or more, or the most recent days)

Apply the same alerts to the other platforms' campaign rows. Microsoft Ads budget limits
show as `ImpressionLostToBudgetPercent`.

### 4. Ad disapprovals & policy issues

```sql
SELECT ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status,
  ad_group_ad.policy_summary.review_status, campaign.name, ad_group.name
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED'
  AND campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'
  AND ad_group_ad.policy_summary.approval_status != 'APPROVED'
```

🔴 Alert on any `DISAPPROVED` ad. 🟡 Flag `APPROVED_LIMITED` (running but throttled).

**Microsoft Ads:** for the top-spending campaigns, `tool_get_ad_groups` then `tool_get_ads`
(`account_id`, `ad_group_id`) and flag ads whose editorial status is not approved.

### 5. Conversion-tracking heartbeat

`conversion_action` rejects `metrics.conversions` (PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE).
Get per-action volume from `customer`, segmented by action:

```sql
SELECT segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM customer
WHERE segments.date DURING LAST_7_DAYS
```

Repeat with the prior week's `BETWEEN` range. An action absent from the result had 0
conversions; an empty result means 0 for every action. To see which actions are primary
(and get a row for each, zeros included), use `all_conversions` on `conversion_action`:

```sql
SELECT conversion_action.name, conversion_action.status,
  conversion_action.primary_for_goal, metrics.all_conversions
FROM conversion_action
WHERE segments.date DURING LAST_7_DAYS
```

🔴 Alert if a primary conversion action recorded conversions last week but **zero**
this week — tracking has almost certainly broken. This is the single most important
check in the skill.

🔴 Also alert if **every primary conversion action is at 0 in both weeks** while GA4 key
events, store orders or Stripe payments are above 0 for the same weeks. That isn't a new
break, so the WoW check above misses it, but Smart Bidding has no signal and every CPA is
meaningless. Run the confirmation reads below even when both Ads weeks are 0.

**Confirm it before alerting.** If GA4 is connected, find the property with
`tool_list_account_summaries`, then run `tool_run_report` (`property_id`,
`date_ranges` for both weeks, `dimensions: ["eventName"]`, `metrics: ["eventCount", "keyEvents"]`).
Keep `eventCount`: GA4 drops rows where every requested metric is 0, so an event whose key
events fell to zero would otherwise vanish instead of showing as 0. If a
store is connected, compare orders: Shopify `tool_list_orders` (`query_filter:
"created_at:>=YYYY-MM-DD"`) or WooCommerce `get_sales_report` (`date_min`, `date_max`).
For SaaS, count Stripe payments with `mcp__cogny__mcp__Stripe__stripe_api_read`
(`GetInvoices` or `GetSubscriptions`, filtered to each week's `created` range).
Ads conversions at zero while GA4 events or store orders held steady = the Ads tag broke.
Both at zero = the site or checkout broke, which is worse. Microsoft Ads: a campaign whose
`Conversions` went from >0 to 0 with steady clicks gets the same alert (UET tag).

### 6. Budget & bidding drift

```sql
SELECT campaign.name, campaign.bidding_strategy_type,
  campaign.bidding_strategy_system_status,
  campaign.target_cpa.target_cpa_micros, campaign.target_roas.target_roas,
  metrics.cost_micros, metrics.conversions, metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND campaign.status = 'ENABLED'
```

Flag campaigns whose `bidding_strategy_system_status` is a `LEARNING_*` value (compare with
last week's snapshot to spot a new learning phase), `LIMITED_*` or `MISCONFIGURED_*`, and any
campaign where the target CPA/ROAS is set (non-zero) but actual is >50% off target. Portfolio
strategies keep their targets on `bidding_strategy`, not on the campaign, so a 0 target here
can mean "set at portfolio level".

### 7. Output

```
Google Ads Monitor — [Account Name]
Week of [YYYY-MM-DD] – [YYYY-MM-DD]

⚠️  Needs attention this week
- [Critical/important items first, or "Nothing — account is running clean."]

Performance (7d vs prior 7d)
- Spend ........ $X,XXX  (+/-X% WoW)
- Conversions .. XXX     (+/-X% WoW)
- CPA .......... $XX     (+/-X% WoW)
- ROAS ......... X.Xx    (+/-X% WoW)

Campaign movers
| Campaign | Type | Spend (WoW) | Conv (WoW) | Note |
|----------|------|-------------|------------|------|

Disapproved / limited ads: [N]
Conversion tracking: [OK / BROKEN — details]

Recommended actions
1. ...
2. ...
```

### 8. Save this week's snapshot

Call `write_context_node` on `insights/google-ads/monitor/latest` (and the matching
`insights/<platform>/monitor/latest` node for each other platform) with this week's
metrics (spend, conversions, CPA, ROAS, per-campaign figures, disapproval count) so
next week can compute deltas. Also write a dated copy to
`insights/google-ads/monitor/<YYYY-MM-DD>` for history.

### 9. Record findings — selectively

Only file a `create_finding` for genuine problems (disapprovals, tracking breaks,
spend spikes, budget-limited profitable campaigns) — **not** routine numbers. A clean
week should produce zero findings.

```json
{
  "title": "Conversion tracking stopped — 'Lead Form Submit' at 0 this week",
  "body": "'Lead Form Submit' recorded 41 conversions last week, 0 this week, while clicks held steady. The tag or GTM trigger has likely broken. Check the GA4/Ads conversion tag.",
  "action_type": "conversion_tracking",
  "expected_outcome": "Tracking restored; Smart Bidding gets accurate signal again",
  "estimated_impact_usd": 0,
  "priority": "critical"
}
```

Cloud uses `create_ticket` with the same content, fields mapped per section 2 of the routing guide.

Action types: `conversion_tracking`, `budget_adjustment`, `campaign_optimization`,
`policy_fix`, `bidding_strategy`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Trends over snapshots.** Always report WoW deltas. A single week's number is
   noise.
2. **Lead with what's broken.** If nothing is wrong, say so in one line and keep the
   report short.
3. **Tracking break = critical, always.** It corrupts every downstream number.
4. **Read-only.** Never pause campaigns or change budgets — surface, don't act. Pause
   tools (`tool_update_campaign_status`, Bing `tool_update_campaign`) are used only on the
   user's explicit request, and the skill asks first.
5. **One block per platform, each in its own currency.** No blended totals.
