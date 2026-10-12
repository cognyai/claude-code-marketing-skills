---
name: crm-sales-momentum
description: Analyze CRM pipeline momentum (HubSpot, Pipedrive or Upsales) — deal velocity, stage conversions, win/loss patterns, and stall detection
version: "1.1.2"
requires: cogny-mcp
author: Cogny AI
platforms: [hubspot, pipedrive, upsales]
user-invocable: true
argument-hint: "[full|velocity|stalls|segments]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__search_properties
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__HubSpot__search_owners
  - mcp__cogny__mcp__HubSpot__discover_hubspot_schema

  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__get_deal
  - mcp__cogny__mcp__Pipedrive__list_pipelines
  - mcp__cogny__mcp__Pipedrive__list_stages
  - mcp__cogny__mcp__Pipedrive__list_deal_fields
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Pipedrive__list_users
  - mcp__cogny__mcp__Upsales__list_opportunities
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_activities
  - mcp__cogny__mcp__Upsales__list_appointments
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__list_users
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - Bash
  - Read
  - Write
---

# CRM Sales Momentum Drivers

Analyze what is driving or stalling pipeline momentum in your CRM (HubSpot, Pipedrive or Upsales). Measures deal velocity, stage conversion rates, time-in-stage, and win/loss patterns by segment. Surfaces the deal characteristics that predict wins versus losses and identifies stuck deals.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

**Tip:** Run `/crm-icp-analysis` first to establish your ICP baseline, then use this skill to see how ICP-fit deals move through pipeline compared to non-fit deals.

## Usage

`/crm-sales-momentum` — full momentum analysis
`/crm-sales-momentum velocity` — deal velocity and stage timing only
`/crm-sales-momentum stalls` — stuck deal detection only
`/crm-sales-momentum segments` — win/loss patterns by segment only

## Works with

All three CRMs connect read-only. HubSpot is primary and has the richest stage history; the others answer most of the jobs with stated limits.

| Job | HubSpot (primary) | Pipedrive | Upsales | What differs |
|-----|-------------------|-----------|---------|--------------|
| Stage map | `get_properties` (`dealstage`, `pipeline`) | `list_pipelines`, `list_stages` | `get_metadata` (stages + probabilities) | — |
| Deals | `search_crm_objects` (`deals`) | `list_deals` (`status`, `pipeline_id`, `stage_id`) | `list_opportunities` (open), `list_orders` (won/closed) | Upsales splits open pipeline from orders |
| Time in stage | `hs_date_entered_<stage>` / `hs_time_in_<stage>` | `stage_change_time` (current stage only) | not exposed; use activity recency | Without stage history, conversion rates are a snapshot (current stage + won/lost), not a true funnel; say so |
| Rep | `search_owners`, `hubspot_owner_id` | `list_users`, `owner_id` | `list_users`, `user` | — |
| Last touch on a deal | `search_crm_objects` (`calls`, `meetings`, `notes`) | `list_activities(deal_id)` | `list_activities`, `list_appointments` (filter `client.id`) | — |

If more than one CRM is connected, score each separately and show them side by side. Never sum pipeline across CRMs or currencies.

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
CRM Sales Momentum needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your CRM (HubSpot, Pipedrive or Upsales).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Prerequisites Check

Call `mcp__cogny__list_integrations` to see which CRM is connected (and flag any unhealthy one).
`health_status` misses revoked tokens, so make one cheap read per connected CRM:
- **HubSpot:** call `mcp__cogny__mcp__HubSpot__get_user_details` and confirm read access to contacts, companies, and deals.
- **Pipedrive:** call `mcp__cogny__mcp__Pipedrive__list_pipelines`.
- **Upsales:** call `mcp__cogny__mcp__Upsales__get_metadata`.

A 401, Forbidden or "lacks scope" means 🔴 "reconnect <CRM> in Cogny"; don't retry the call. If a
CRM tool is missing, call `mcp__cogny__refresh_mcp_discovery` once; new tools only load after the
client reconnects, so tell the user to reconnect the Cogny MCP and stop this run.

If no CRM is connected (or every connected one is 🔴), print this and stop:

```
This skill needs a CRM. Connect HubSpot, Pipedrive or Upsales in Cogny
(Integrations → Connect), then run /crm-sales-momentum again.
Stripe (subscriptions) or Fortnox (customers, invoices), if connected, give only a payer-only
partial view (who pays, who cancels or stops buying), with no pipeline, stages or win rates.
```

## Steps

### 1. Discover pipeline structure

Get deal stage properties to understand the pipeline:

```
mcp__cogny__mcp__HubSpot__get_properties(objectType: "deals", propertyNames: ["dealstage", "pipeline"])
```

Identify:
- All pipeline stages and their order (from the `dealstage` property enum values)
- Pipeline names (if multiple pipelines exist)
- Custom deal properties relevant to segmentation

Use `search_properties` to find stage-timing properties:

```
mcp__cogny__mcp__HubSpot__search_properties(objectType: "deals", keywords: ["hs_date_entered", "hs_time_in"])
```

Also fetch owner list for rep-level analysis:

```
mcp__cogny__mcp__HubSpot__search_owners()
```

**Pipedrive:** `mcp__cogny__mcp__Pipedrive__list_pipelines()`, `list_stages(pipeline_id: <id>)` (ordered, with win probability), `list_users()` for reps, `list_deal_fields()` for custom segment fields.

**Upsales:** `mcp__cogny__mcp__Upsales__get_metadata()` for stages and their probabilities, `list_users()` for reps.

### 2. Pull deal data across all stages

Fetch deals created in the last 90 days plus recently closed:

```
mcp__cogny__mcp__HubSpot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [{"propertyName": "createdate", "operator": "GTE", "value": "<90 days ago timestamp>"}]}],
  properties: ["dealname", "dealstage", "hs_is_closed", "hs_is_closed_won", "amount", "deal_currency_code", "createdate", "closedate", "pipeline", "hubspot_owner_id", "hs_analytics_source", "dealtype", <stage timing properties from step 1>],
  sorts: [{"propertyName": "createdate", "direction": "DESCENDING"}],
  limit: 200
)
```

Check `total` count and paginate if needed to capture full dataset.

Classify outcomes with `hs_is_closed_won = true` (won) and `hs_is_closed = true AND hs_is_closed_won = false`
(lost), never with `dealstage = closedwon / closedlost`: custom pipelines use their own stage ids, so
stage-name filters miss their wins and losses.

**Pipedrive:** `mcp__cogny__mcp__Pipedrive__list_deals(updated_since: "<90 days ago, ISO-8601>", sort_by: "add_time", sort_direction: "desc", limit: 500)`, following `next_cursor`. Keep `stage_id`, `status`, `value`, `currency`, `owner_id`, `add_time`, `stage_change_time`, `won_time`, `lost_time`, `lost_reason`.

**Upsales:** `mcp__cogny__mcp__Upsales__list_opportunities(sort: "-date", limit: 1000)` for open pipeline and `list_orders(filters: [{"field": "date", "comparator": "gte", "value": "<90 days ago, YYYY-MM-DD>"}])` for closed; page with `offset`.

### 3. Deal velocity analysis

Calculate velocity metrics across the pipeline:

- **Overall velocity**: average days from deal creation to close (won and lost separately)
- **Stage-by-stage velocity**: average time in each stage
- **Stage conversion rates**: % of deals that advance from each stage to the next
- **Drop-off stages**: stages with the highest loss rate
- **Velocity trend**: compare last 30 days vs previous 30 days

Build a pipeline flow visualization:

```
Pipeline Flow (last 90 days):
[Stage 1] ──85%──> [Stage 2] ──62%──> [Stage 3] ──48%──> [Stage 4] ──71%──> [Closed Won]
  100 deals           85 deals          53 deals          25 deals         18 deals
  avg 4 days          avg 7 days        avg 12 days       avg 5 days
                       ↓ 15%             ↓ 38%             ↓ 52%           ↓ 29%
                    [Lost: 15]        [Lost: 32]        [Lost: 28]       [Lost: 7]
```

Flag:
- Stages where >40% of deals stall or are lost
- Stages with average time >2x the overall stage average
- Conversion rate drops of >10% compared to previous period

### 4. Stuck deal detection

Identify deals that are stalled based on time-in-stage analysis.

For each pipeline stage, calculate:
- Median time-in-stage for deals that eventually advanced
- Standard deviation of time-in-stage
- **Stall threshold**: median + 1.5x standard deviation

Flag deals currently in a stage beyond the stall threshold:

```
mcp__cogny__mcp__HubSpot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [
    {"propertyName": "dealstage", "operator": "EQ", "value": "<stage>"},
    {"propertyName": "hs_date_entered_<stage>", "operator": "LT", "value": "<stall threshold date>"}
  ]}],
  properties: ["dealname", "amount", "hubspot_owner_id", "hs_date_entered_<stage>"],
  limit: 50
)
```

For each stuck deal, fetch associated company and contacts to add context about why it might be stalled.

**Pipedrive:** for open deals, time in current stage = now − `stage_change_time`; compare it with the same threshold. Add `list_activities(deal_id: <id>, done: false)` to show whether a next step is scheduled; a stuck deal with no open activity is the priority.

**Upsales:** time in stage isn't exposed. Flag open opportunities whose account has no activity or appointment in the last 2× median cycle (`list_activities` / `list_appointments` with `filters: [{"field": "client.id", "comparator": "eq", "value": <id>}]`), and label the threshold as activity-based.

### 5. Win/loss pattern analysis by segment

Segment closed deals along multiple dimensions and compare win rates:

**By Deal Size:**
- Bucket deals into tiers and compare win rate per tier
- Identify the deal size range with highest win rate

**By Lead Source:**
- Win rate by `hs_analytics_source` (organic, paid, referral, direct, etc.); on Pipedrive/Upsales use a source custom field if one exists, otherwise skip this cut
- Average deal size by source
- Average sales cycle by source

**By Owner (Sales Rep):**
- Win rate per rep
- Average deal velocity per rep
- Average deal size per rep
- Identify top performers and what they do differently

**By Company Segment** (fetch associated companies):
- Win rate by industry
- Win rate by company size
- Win rate by geography

**By Deal Age at Stage:**
- Deals that spend <X days in each stage: win rate
- Deals that spend >X days: win rate
- Identify the "golden window" — the time-in-stage range that correlates with wins

### 6. Momentum scoring

Score overall pipeline momentum:

```
Pipeline Momentum Score: X/100

Velocity:        X/25
  [FAST/NORMAL/SLOW] Average cycle [N] days
  [UP/DOWN/FLAT] Velocity trend: [X]% change vs prior period

Flow Rate:       X/25
  [STRONG/MODERATE/WEAK] Stage conversion rates
  [IMPROVING/DECLINING/STABLE] Conversion trend
  Drop-off stage: [stage name] ([X]% loss rate)

Pipeline Health:  X/25
  [HEALTHY/AT_RISK/CRITICAL] [N] deals stuck ([X]% of active pipeline)
  [GROWING/SHRINKING/STABLE] Pipeline value: [X] [ccy] ([X]% change)
  Coverage ratio: [X]x ([pipeline value] / [target])

Predictability:  X/25
  [HIGH/MEDIUM/LOW] Win rate consistency: [X]% +/- [Y]%
  [CLEAR/MIXED/UNCLEAR] Segment patterns identified
  [STRONG/WEAK] Leading indicators reliability
```

### 7. Output momentum report

```
CRM Sales Momentum Analysis
CRM: [HubSpot / Pipedrive / Upsales]
Period: Last 90 days
Deals analyzed: [N] ([N] won, [N] lost, [N] active)
Pipeline value: [X] [currency]

═══════════════════════════════════════════════════
MOMENTUM SCORE: X/100
═══════════════════════════════════════════════════

Pipeline Flow:
[Stage-by-stage flow diagram from Step 3]

Key Velocity Metrics:
  Average Sales Cycle (Won):   [N] days
  Average Sales Cycle (Lost):  [N] days
  Fastest Close:               [N] days ([deal name])
  Slowest Win:                 [N] days ([deal name])

Stage Health:
┌──────────────────┬──────────┬───────────┬──────────┬─────────────┐
│ Stage            │ Deals In │ Avg Days  │ Conv Rate│ Stuck Deals │
├──────────────────┼──────────┼───────────┼──────────┼─────────────┤
│ [Stage 1]        │ [N]      │ [N]       │ [X]%     │ [N]         │
│ [Stage 2]        │ [N]      │ [N]       │ [X]%     │ [N]         │
│ [Stage 3]        │ [N]      │ [N]       │ [X]%     │ [N]         │
│ [Stage 4]        │ [N]      │ [N]       │ [X]%     │ [N]         │
└──────────────────┴──────────┴───────────┴──────────┴─────────────┘

Win Predictors (what separates wins from losses):
1. [Predictor]: deals with [X] win at [Y]% vs [Z]% without
2. [Predictor]: deals with [X] win at [Y]% vs [Z]% without
3. [Predictor]: deals with [X] win at [Y]% vs [Z]% without

Stuck Deals Requiring Attention:
┌──────────────────┬──────────┬──────────┬──────────┬─────────────────┐
│ Deal             │ Amount   │ Stage    │ Days In  │ Owner           │
├──────────────────┼──────────┼──────────┼──────────┼─────────────────┤
│ [Deal 1]         │ [X] [ccy]│ [Stage]  │ [N]      │ [Rep]           │
│ [Deal 2]         │ [X] [ccy]│ [Stage]  │ [N]      │ [Rep]           │
└──────────────────┴──────────┴──────────┴──────────┴─────────────────┘

Rep Performance:
┌──────────────────┬──────────┬───────────┬──────────┬─────────────┐
│ Rep              │ Win Rate │ Avg Cycle │ Avg Deal │ Pipeline    │
├──────────────────┼──────────┼───────────┼──────────┼─────────────┤
│ [Rep 1]          │ [X]%     │ [N] days  │ [X] [ccy]│ [X] [ccy]   │
│ [Rep 2]          │ [X]%     │ [N] days  │ [X] [ccy]│ [X] [ccy]   │
└──────────────────┴──────────┴───────────┴──────────┴─────────────┘

Top 3 Actions:
1. [Highest-impact momentum fix]
2. [Second highest]
3. [Third highest]
```

### 8. Record findings

For EVERY actionable momentum insight, record one review item. Detect the plan from the tools that
exist: on **Cloud** (`create_ticket` exists) call `mcp__cogny__create_ticket` first, with
`execution_target: "manual"` and the fields mapped per section 2 of the routing guide. Only on
**Solo** (no `create_ticket`) call `mcp__cogny__create_finding`:

```json
{
  "title": "38% of deals stall at Proposal stage — avg 18 days vs 7-day benchmark",
  "body": "32 of 85 deals entering the Proposal stage in the last 90 days have stalled or been lost. Median time-in-stage for deals that advance is 7 days, but stalled deals average 18 days. Common pattern: deals without a second contact (single-threaded) stall at 2.1x the rate. 12 deals currently stuck in Proposal worth 340K [ccy] total. Recommend: implement multi-threading requirement before Proposal stage, add 10-day stall alert.",
  "action_type": "pipeline_optimization",
  "expected_outcome": "Reduce Proposal stage stall rate from 38% to <20%",
  "estimated_impact_usd": 8000,
  "priority": "high"
}
```

Action types for sales momentum:
- `pipeline_optimization` — stage process changes, stall interventions
- `deal_acceleration` — specific actions to unstick individual deals
- `rep_coaching` — rep-specific performance improvements
- `forecasting_improvement` — pipeline coverage, predictability fixes
- `lead_source_optimization` — invest in sources that produce faster-closing deals
- `disqualification_rule` — patterns that predict losses, filter early

## Recording findings

Use `create_ticket` first when the workspace has it (Cloud), and `create_finding` only when it doesn't (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
