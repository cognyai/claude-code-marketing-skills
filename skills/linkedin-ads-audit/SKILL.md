---
name: linkedin-ads-audit
description: Full LinkedIn Ads account audit — campaign structure, targeting, creative performance, spend efficiency
version: "1.0.0"
author: Cogny AI
platforms: [linkedin-ads]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__linkedin_ads__*
  - mcp__cogny__create_finding
  - mcp__cogny__list_findings
  - mcp__cogny__update_finding
  - WebFetch
  - Bash
  - Read
  - Write
---

# LinkedIn Ads Audit

Perform a comprehensive LinkedIn Ads account audit using live data from the connected LinkedIn Ads MCP.

## Usage

`/linkedin-ads-audit` — audit the connected LinkedIn Ads account

## Benchmarks

Use these LinkedIn Ads benchmarks for scoring:

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| CTR | <0.3% | 0.4-0.6% | >0.8% |
| CPC | >$10 | $5-8 | <$4 |
| CPM | >$40 | $25-35 | <$20 |
| Conversion Rate | <1% | 2-4% | >5% |
| Engagement Rate | <0.3% | 0.5-1% | >1.5% |

## Steps

### 1. List accessible ad accounts

Query available ad accounts. If multiple exist, note which is active.

### 2. Campaign overview

Get all campaigns (active + recently paused). For each:
- Status, objective, budget type (daily/lifetime)
- Date range and total spend
- Key metrics: impressions, clicks, CTR, CPC, conversions

Flag:
- Campaigns spending >30% of budget with CTR below 0.3%
- Paused campaigns that were performing well (CTR >0.6%)
- Campaigns running >90 days without optimization

### 3. Spend efficiency analysis

Across all active campaigns:
- Total monthly spend vs results
- CPC trend (last 30 vs previous 30 days)
- Cost per conversion by campaign
- Budget utilization (actual spend vs allocated)

Flag:
- Campaigns with CPC >$10 (above LinkedIn average)
- Budget underspend (<70% utilization) or overspend
- Rising CPC trends (>20% increase MoM)

### 4. Targeting review

For each active campaign, analyze:
- Audience size (too narrow <10K or too broad >1M)
- Job title/function targeting specificity
- Industry and company size filters
- Geographic targeting
- Audience expansion settings

Flag:
- Overlapping audiences between campaigns
- Overly broad targeting (no job title/function filters)
- Missing exclusions (existing customers, competitors)

### 5. Creative performance

Analyze ad creatives across campaigns:
- Format breakdown (single image, carousel, video, text)
- Per-creative CTR and engagement rate
- Ad copy length and CTA effectiveness
- Creative age (days since launch)

Flag:
- Creatives running >60 days (fatigue risk)
- Single-format campaigns (no A/B testing)
- Low-performing creatives (CTR <0.2%) still active
- Missing formats (no video if budget >$5K/mo)

### 6. Conversion tracking

Check:
- Insight Tag installation status
- Conversion event definitions
- Attribution window settings
- Lead gen form completion rates (if using lead gen)

Flag:
- Missing or misconfigured conversion tracking
- Low form completion rates (<10%)
- No offline conversion import

### 7. Budget pacing

For each campaign:
- Daily/monthly spend rate vs target
- Projected end-of-month spend
- Day-of-week performance patterns

Flag:
- Campaigns pacing >20% over or under budget
- Weekend spend on B2B campaigns (usually wasteful)

### 8. Report findings

Present as a scored audit:

```
LinkedIn Ads Audit
Score: X/100

Campaign Structure: X/20
- [PASS/FAIL] Campaign organization
- [PASS/FAIL] Objective alignment
- [PASS/FAIL] Budget allocation

Targeting: X/20
- [PASS/FAIL] Audience specificity
- [PASS/FAIL] Audience overlap
- [PASS/FAIL] Exclusions

Creative: X/20
- [PASS/FAIL] Format diversity
- [PASS/FAIL] Creative freshness
- [PASS/FAIL] A/B testing

Performance: X/20
- [PASS/FAIL] CPC vs benchmark
- [PASS/FAIL] CTR vs benchmark
- [PASS/FAIL] Conversion rate

Tracking & Budget: X/20
- [PASS/FAIL] Conversion tracking
- [PASS/FAIL] Budget pacing
- [PASS/FAIL] Attribution setup

Top 3 Actions:
1. [Highest impact fix]
2. [Second highest]
3. [Third highest]
```

### 9. Record findings

For EVERY actionable issue found, call `mcp__cogny__create_finding`:

```json
{
  "title": "High CPC on 'Decision Makers' campaign ($12.40 vs $5-8 benchmark)",
  "body": "Campaign targeting C-suite titles with single image ads. CPC is 55% above LinkedIn average. Recommend: 1) Test carousel format 2) Narrow to VP+ titles only 3) Add company size >500 filter",
  "action_type": "campaign_optimization",
  "expected_outcome": "Reduce CPC to <$8 within 2 weeks",
  "estimated_impact_usd": 800,
  "priority": "high"
}
```

Action types for LinkedIn Ads:
- `campaign_optimization` — budget, bidding, pacing changes
- `targeting_refinement` — audience, exclusion, geo changes
- `creative_refresh` — new ads, format tests, copy updates
- `conversion_tracking` — pixel, events, attribution fixes
- `audience_management` — overlap, expansion, exclusion updates
