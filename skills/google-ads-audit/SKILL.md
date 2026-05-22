---
name: google-ads-audit
description: Comprehensive Google Ads account audit — campaign structure, budget pacing, conversion tracking, wasted spend — across every campaign type, ranked by estimated $ impact
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads]
user-invocable: true
argument-hint: "[full|campaigns|budget|tracking|negatives]"
allowed-tools:
  - mcp__cogny__google_ads__tool_list_accessible_accounts
  - mcp__cogny__google_ads__tool_execute_gaql
  - mcp__cogny__google_ads__tool_get_gaql_doc
  - mcp__cogny__google_ads__tool_get_reporting_view_doc
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# Google Ads Audit

A one-time, account-wide Google Ads health audit using live data via Cogny's MCP
server. Covers every campaign type, scores the account out of 100, and routes you to
the right campaign-type skill for deeper drill-down.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

Verify Google Ads MCP tools are available. If `mcp__cogny__google_ads__tool_execute_gaql`
is not available:

```
This skill requires Cogny's Google Ads MCP server.

1. Sign up at https://cogny.com/agent
2. Connect your Google Ads account
3. Add Cogny to your .mcp.json (see the repo README)
4. Restart Claude Code
```

Stop here if the tools are missing — do not guess at numbers.

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

## Steps

### 1. Account discovery

```
tool_list_accessible_accounts
```

If multiple accounts are accessible, list them and ask which to audit. Confirm the
account name and currency before continuing.

### 2. Campaign overview by channel type (last 30 days)

```sql
SELECT campaign.name, campaign.status, campaign.advertising_channel_type,
  campaign.bidding_strategy_type, campaign_budget.amount_micros,
  metrics.cost_micros, metrics.conversions, metrics.conversions_value,
  metrics.clicks, metrics.impressions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

Build a per-channel-type summary (Search / Performance Max / Shopping / Display /
Video / Demand Gen): total spend, conversions, CPA, ROAS (`conversions_value / cost`).

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

```sql
SELECT shared_set.name, shared_set.type, shared_set.status, shared_set.member_count
FROM shared_set
```

Flag:
- No negative keyword lists shared across Search campaigns
- No brand-term handling (brand traffic mixed into non-brand campaigns)
- For Performance Max / Display: missing account-level placement and content
  exclusions (brand-safety + waste risk)

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

### 7. Score and report

```
Google Ads Audit — [Account Name]
Health Score: X/100  ·  30-day spend: [X]  ·  Conversions: [X]  ·  CPA: [X]

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

Action types: `campaign_optimization`, `budget_adjustment`, `bidding_strategy`,
`conversion_tracking`, `negative_keyword`, `account_structure`.

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
5. This skill **reads only**. It never pauses campaigns or changes budgets.
