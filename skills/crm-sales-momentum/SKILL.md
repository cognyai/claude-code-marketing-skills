---
name: crm-sales-momentum
description: Analyze HubSpot pipeline momentum — deal velocity, stage conversions, win/loss patterns, and stall detection
version: "1.0.0"
author: Cogny AI
platforms: [hubspot]
user-invocable: true
argument-hint: "[full|velocity|stalls|segments]"
allowed-tools:
  - mcp__cogny__hubspot__*
  - mcp__cogny__create_finding
  - Bash
  - Read
  - Write
---

# CRM Sales Momentum Drivers

Analyze what is driving or stalling pipeline momentum in your HubSpot CRM. Measures deal velocity, stage conversion rates, time-in-stage, and win/loss patterns by segment. Surfaces the deal characteristics that predict wins versus losses and identifies stuck deals.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

**Tip:** Run `/crm-icp-analysis` first to establish your ICP baseline, then use this skill to see how ICP-fit deals move through pipeline compared to non-fit deals.

## Usage

`/crm-sales-momentum` — full momentum analysis
`/crm-sales-momentum velocity` — deal velocity and stage timing only
`/crm-sales-momentum stalls` — stuck deal detection only
`/crm-sales-momentum segments` — win/loss patterns by segment only

## Prerequisites Check

Call `mcp__cogny__hubspot__get_user_details` to verify CRM access. Confirm read access to contacts, companies, and deals. If access is missing:

```
This skill requires HubSpot CRM access via Cogny's MCP server.
Sign up at https://cogny.com/agent and connect your HubSpot account.
```

## Steps

### 1. Discover pipeline structure

Get deal stage properties to understand the pipeline:

```
hubspot__get_properties(objectType: "deals", propertyNames: ["dealstage", "pipeline"])
```

Identify:
- All pipeline stages and their order (from the `dealstage` property enum values)
- Pipeline names (if multiple pipelines exist)
- Custom deal properties relevant to segmentation

Use `search_properties` to find stage-timing properties:

```
hubspot__search_properties(objectType: "deals", keywords: ["hs_date_entered", "hs_time_in"])
```

Also fetch owner list for rep-level analysis:

```
hubspot__search_owners()
```

### 2. Pull deal data across all stages

Fetch deals created in the last 90 days plus recently closed:

```
hubspot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [{"propertyName": "createdate", "operator": "GTE", "value": "<90 days ago timestamp>"}]}],
  properties: ["dealname", "dealstage", "amount", "createdate", "closedate", "pipeline", "hubspot_owner_id", "hs_analytics_source", "dealtype", <stage timing properties from step 1>],
  sorts: [{"propertyName": "createdate", "direction": "DESCENDING"}],
  limit: 200
)
```

Check `total` count and paginate if needed to capture full dataset.

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
hubspot__search_crm_objects(
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

### 5. Win/loss pattern analysis by segment

Segment closed deals along multiple dimensions and compare win rates:

**By Deal Size:**
- Bucket deals into tiers and compare win rate per tier
- Identify the deal size range with highest win rate

**By Lead Source:**
- Win rate by `hs_analytics_source` (organic, paid, referral, direct, etc.)
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
  [GROWING/SHRINKING/STABLE] Pipeline value: $[X] ([X]% change)
  Coverage ratio: [X]x ([pipeline value] / [target])

Predictability:  X/25
  [HIGH/MEDIUM/LOW] Win rate consistency: [X]% +/- [Y]%
  [CLEAR/MIXED/UNCLEAR] Segment patterns identified
  [STRONG/WEAK] Leading indicators reliability
```

### 7. Output momentum report

```
CRM Sales Momentum Analysis
Period: Last 90 days
Deals analyzed: [N] ([N] won, [N] lost, [N] active)
Pipeline value: $[X]

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
│ [Deal 1]         │ $[X]     │ [Stage]  │ [N]      │ [Rep]           │
│ [Deal 2]         │ $[X]     │ [Stage]  │ [N]      │ [Rep]           │
└──────────────────┴──────────┴──────────┴──────────┴─────────────────┘

Rep Performance:
┌──────────────────┬──────────┬───────────┬──────────┬─────────────┐
│ Rep              │ Win Rate │ Avg Cycle │ Avg Deal │ Pipeline $  │
├──────────────────┼──────────┼───────────┼──────────┼─────────────┤
│ [Rep 1]          │ [X]%     │ [N] days  │ $[X]     │ $[X]        │
│ [Rep 2]          │ [X]%     │ [N] days  │ $[X]     │ $[X]        │
└──────────────────┴──────────┴───────────┴──────────┴─────────────┘

Top 3 Actions:
1. [Highest-impact momentum fix]
2. [Second highest]
3. [Third highest]
```

### 8. Record findings

For EVERY actionable momentum insight, call `mcp__cogny__create_finding`:

```json
{
  "title": "38% of deals stall at Proposal stage — avg 18 days vs 7-day benchmark",
  "body": "32 of 85 deals entering the Proposal stage in the last 90 days have stalled or been lost. Median time-in-stage for deals that advance is 7 days, but stalled deals average 18 days. Common pattern: deals without a second contact (single-threaded) stall at 2.1x the rate. 12 deals currently stuck in Proposal worth $340K total. Recommend: implement multi-threading requirement before Proposal stage, add 10-day stall alert.",
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
