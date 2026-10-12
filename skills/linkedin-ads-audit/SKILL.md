---
name: linkedin-ads-audit
description: Full LinkedIn Ads account audit — campaign structure, targeting, creative performance, spend efficiency
version: "1.1.2"
requires: cogny-mcp
author: Cogny AI
platforms: [linkedin-ads, fibbler, hubspot, pipedrive, upsales]
user-invocable: true
argument-hint: ""
allowed-tools:
  # LinkedIn Ads read-only tools
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign_groups
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaigns
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_analytics
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_conversions
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_targeting_facets
  - mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_audience_counts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_company_engagement
  # Fibbler (B2B attribution, read-only)
  - mcp__cogny__mcp__app-fibbler-co__get_campaign_performance
  - mcp__cogny__mcp__app-fibbler-co__get_deal_campaign_breakdown
  - mcp__cogny__mcp__app-fibbler-co__get_deal_attribution_summary
  - mcp__cogny__mcp__app-fibbler-co__get_audience_titles
  - mcp__cogny__mcp__app-fibbler-co__get_company_engagement
  # CRM account lists for target-account coverage (read-only)
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__list_integrations
  # Findings
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - Bash
  - Read
  - Write
---

# LinkedIn Ads Audit

Perform a comprehensive LinkedIn Ads account audit using live data from the connected LinkedIn Ads MCP.

## Usage

`/linkedin-ads-audit` — audit the connected LinkedIn Ads account

## Works with

LinkedIn Ads is required; everything else sharpens the verdict. Call `mcp__cogny__list_integrations` once and name any unhealthy integration in the report.

| Job | Primary | Also answers it | What differs |
|-----|---------|-----------------|--------------|
| Structure, targeting, creatives, spend | LinkedIn Ads | — | No substitute; this skill audits LinkedIn only |
| Pipeline / revenue per campaign | Fibbler (`app-fibbler-co`) | LinkedIn `tool_get_conversions` + analytics | Fibbler matches campaigns to CRM deals (impression-matched influence, not last click); LinkedIn only sees on-platform conversions |
| Who the ads reached (titles) | Fibbler `get_audience_titles` | LinkedIn `tool_get_analytics` with `pivot: "MEMBER_JOB_TITLE"` | Fibbler adds whether each title is currently included/excluded; LinkedIn's demographic pivots return impressions, clicks and engagements only (no cost) |
| Target-account coverage (ABM) | LinkedIn `tool_get_company_engagement` + CRM account list | HubSpot, Pipedrive or Upsales as the list source; Fibbler `get_company_engagement` if the LinkedIn tool is missing | Matching is done by the tool (page slug → domain → name); LinkedIn drops companies with <3 events, so absence isn't proof of no exposure |

## Failure handling

- **Health check first.** `list_integrations` can read `healthy` for a revoked LinkedIn token. Step 1's `tool_list_ad_accounts` is the cheap read: if it (or any later LinkedIn call) returns 401, "unauthorized", Forbidden or a scope error, mark LinkedIn Ads 🔴 and **stop the audit**. Don't retry the call and don't run the remaining steps on partial data.
- **Report the reconnect steps:** in Cogny, open Integrations → LinkedIn Ads → Reconnect, sign in with a LinkedIn user who has at least a Campaign Manager or Viewer role on the ad account, then re-run `/linkedin-ads-audit`.
- **File one ticket** for the broken connection (Cloud: `create_ticket`, title "[Critical] Reconnect LinkedIn Ads — token revoked", `expected_outcome` "LinkedIn Ads reads succeed and the audit can run"; Solo: `create_finding`). One ticket per run, not one per failed call.
- **Fibbler is an enhancement, not a fallback.** It can't replace LinkedIn's structure, targeting, creative or spend data, so a broken LinkedIn connection is never "audited via Fibbler". Its only stand-in role is the company-engagement read below.
- **Missing tool:** if `tool_get_company_engagement` isn't exposed by the workspace (older connections cache their tool list), call `mcp__cogny__refresh_mcp_discovery` once, then use Fibbler `get_company_engagement` for this run if Fibbler is connected, and mark the source ⚠ "needs reconnect". Without Fibbler, skip target-account coverage with a one-line note. Never loop on refresh.
- Other integrations (Fibbler, HubSpot, Pipedrive, Upsales) failing a first read: name them 🔴 "reconnect <integration>" in the report, skip their enhancement, and continue.

Report money in the account's own currency (`tool_list_ad_accounts` returns it). The benchmarks below are USD; convert before scoring, and never add Fibbler pipeline to LinkedIn-reported conversion value.

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

### 0. Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop
before calling anything else:

```
LinkedIn Ads Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect LinkedIn Ads (plus Fibbler and HubSpot,
   Pipedrive or Upsales if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts` is missing,
say "connect LinkedIn Ads in Cogny" and stop. A revoked or broken connection is handled under
Failure handling above ("reconnect LinkedIn Ads in Cogny").

### 1. List accessible ad accounts

Call `mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts`. If multiple exist, note which is active and its currency.

Campaigns, creatives and metrics then come from `tool_get_campaign_groups`, `tool_get_campaigns` (`ad_account_id`, `status_filter: ["ACTIVE", "PAUSED"]`), `tool_get_creatives` and `tool_get_analytics` (`ad_account_id`, `start_date`, `end_date`, `pivot: "CAMPAIGN"` or `"CREATIVE"`, `time_granularity: "ALL"` or `"MONTHLY"`). Cost comes back as `costInLocalCurrency`.

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

**Enhanced when connected — who actually saw the ads:**
- Fibbler `get_audience_titles` (`scope: "by_campaign"`, `time_period: "90d"`) lists the titles reached per campaign and whether each is targeted or excluded. Flag campaigns where >30% of impressions went to titles outside the ICP.
- Without Fibbler, use `tool_get_analytics` with `pivot: "MEMBER_JOB_TITLE"` or `"MEMBER_SENIORITY"` (impressions, clicks, engagements only).

**Enhanced when connected — target-account coverage:** pull the CRM's target or open-deal companies (HubSpot `search_crm_objects` on `companies`; Pipedrive `list_organizations`; Upsales `list_accounts`) and pass them as `crm_records` (`id`, `name`, `domain`) to `mcp__cogny__mcp__LinkedIn_Ads__tool_get_company_engagement` (`ad_account_id`, `start_date`, `end_date` = the audit window). If that tool is missing, use `mcp__cogny__mcp__app-fibbler-co__get_company_engagement` instead (⚠, see Failure handling) and match its companies to the CRM list yourself. Report % of target accounts reached and engaged. If several CRMs are connected, report each list separately.

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

**Enhanced when connected — pipeline, not just clicks (Fibbler):**
1. `get_deal_attribution_summary` (`source: "LINKEDIN"`, `time_period: "last_quarter"`, `compare: true`): influenced pipeline, won revenue, cost per opportunity.
2. `get_campaign_performance` (`sort_by: "influenced_pipeline"`, `time_period: "90d"`): spend vs influenced pipeline per campaign.
3. `get_deal_campaign_breakdown` (`group_by: "campaign"`, `source: "LINKEDIN"`): which campaigns touch deals that close.

Flag campaigns with top-quartile spend and zero influenced deals in 90 days, and campaigns with poor CTR but strong influenced pipeline (don't cut those on CTR alone). Fibbler uses calendar quarters and its own period echo; quote the period it returns. Its pipeline is influence, not credit: never sum it across channels or add it to LinkedIn conversion value.

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
- [PASS/FAIL/N/A] Spend reaches pipeline (Fibbler; N/A when not connected)

Top 3 Actions:
1. [Highest impact fix]
2. [Second highest]
3. [Third highest]
```

### 9. Record findings

For EVERY actionable issue found, record it. On Cloud call `mcp__cogny__create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `mcp__cogny__create_finding`:

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

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
