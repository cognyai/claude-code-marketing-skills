---
name: google-ads-monitor
description: Weekly Google Ads health check — budget pacing, spend spikes, disapproved ads, conversion-tracking breaks, CPA/ROAS swings — with week-over-week deltas
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__google_ads__tool_list_accessible_accounts
  - mcp__cogny__google_ads__tool_execute_gaql
  - mcp__cogny__google_ads__tool_get_gaql_doc
  - mcp__cogny__create_finding
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  - WebFetch
---

# Google Ads Monitor

A recurring weekly check that makes sure your ads are still running smoothly. It
catches the things that break quietly — a disapproved ad, tracking that stopped
firing, a campaign that started overspending — and reports week-over-week so you see
trends, not noise.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

Designed to be scheduled weekly via `/loop` or `/schedule`.

## Prerequisites Check

If `mcp__cogny__google_ads__tool_execute_gaql` is not available, print the Cogny
sign-up instructions (see `/google-ads-audit`) and stop.

## Usage

`/google-ads-monitor` — weekly health check of the connected account.

For a deep one-time review, run `/google-ads-audit` instead. This skill is the light,
repeatable rhythm; the audit is the full teardown.

## Steps

### 1. Read the prior snapshot

Call `read_context_node` on `insights/google-ads/monitor/latest`. If it exists, it
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

### 3. Per-campaign movement

```sql
SELECT campaign.name, campaign.status, campaign.advertising_channel_type,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_7_DAYS AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

🔴 Alert if any campaign:
- Spent >40% more than the prior week
- Dropped to **zero conversions** after converting the week before
- Is capped at its daily budget every day (budget-limited)
- Stopped delivering entirely (zero impressions, still enabled)

### 4. Ad disapprovals & policy issues

```sql
SELECT ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status,
  ad_group_ad.policy_summary.review_status, campaign.name, ad_group.name
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED'
  AND ad_group_ad.policy_summary.approval_status != 'APPROVED'
```

🔴 Alert on any `DISAPPROVED` ad. 🟡 Flag `APPROVED_LIMITED` (running but throttled).

### 5. Conversion-tracking heartbeat

```sql
SELECT conversion_action.name, conversion_action.status,
  metrics.conversions, metrics.all_conversions
FROM conversion_action
WHERE segments.date DURING LAST_7_DAYS
```

🔴 Alert if a primary conversion action recorded conversions last week but **zero**
this week — tracking has almost certainly broken. This is the single most important
check in the skill.

### 6. Budget & bidding drift

Flag campaigns whose bidding strategy changed status to `LEARNING`, and any campaign
where the target CPA/ROAS is set but actual is >50% off target.

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

Call `write_context_node` on `insights/google-ads/monitor/latest` with this week's
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

Action types: `conversion_tracking`, `budget_adjustment`, `campaign_optimization`,
`policy_fix`, `bidding_strategy`.

## Critical rules

1. **Trends over snapshots.** Always report WoW deltas. A single week's number is
   noise.
2. **Lead with what's broken.** If nothing is wrong, say so in one line and keep the
   report short.
3. **Tracking break = critical, always.** It corrupts every downstream number.
4. **Read-only.** Never pause campaigns or change budgets — surface, don't act.
