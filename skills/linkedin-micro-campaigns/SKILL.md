---
name: linkedin-micro-campaigns
description: Create precision-targeted LinkedIn ad campaigns for specific ICP segments — translates CRM data to LinkedIn targeting
version: "1.0.0"
author: Cogny AI
platforms: [hubspot, linkedin-ads]
user-invocable: true
argument-hint: "<ICP description or segment>"
allowed-tools:
  # HubSpot CRM tools (for ICP data extraction)
  - mcp__cogny__hubspot__*
  # LinkedIn Ads tools
  - mcp__cogny__linkedin_ads__*
  # Findings
  - mcp__cogny__create_finding
  - Bash
  - Read
  - Write
---

# LinkedIn Micro Campaigns

Create highly targeted LinkedIn ad campaigns for specific ICP segments. Translates your Ideal Customer Profile (from CRM data or manual input) into precision LinkedIn targeting criteria, estimates audience sizes, and builds campaign groups with campaigns and creatives.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

**Tip:** Run `/crm-icp-analysis` first to generate a data-driven ICP, then feed the output into this skill. You can also run `/crm-sales-momentum` to identify which segments close fastest and target those specifically.

## Usage

`/linkedin-micro-campaigns "VP Marketing at SaaS companies, 200-1000 employees"` — create campaigns from a description
`/linkedin-micro-campaigns` — pull ICP from HubSpot CRM data automatically

## Prerequisites Check

Verify LinkedIn Ads access (required):

```
linkedin_ads__tool_list_ad_accounts
```

If HubSpot is also connected (for automatic ICP extraction), verify:

```
hubspot__get_user_details
```

If LinkedIn Ads is not available:

```
This skill requires Cogny's LinkedIn Ads MCP server.
Sign up at https://cogny.com/agent and connect your LinkedIn Ads account.

HubSpot is optional — if connected, ICP data is extracted automatically.
Without HubSpot, provide your ICP description as an argument.
```

## Steps

### 1. Establish ICP targeting inputs

**If ICP description is provided as argument**, parse it for:
- Job titles / functions / seniority
- Industries
- Company sizes
- Geographic targets
- Any other targeting dimensions mentioned

**If no argument is provided and HubSpot is connected**, extract ICP from CRM:

Pull closed-won deal data to identify top-performing segments:

```
hubspot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": "closedwon"}]}],
  properties: ["dealname", "amount", "closedate"],
  sorts: [{"propertyName": "closedate", "direction": "DESCENDING"}],
  limit: 50
)
```

Fetch associated companies and contacts to extract:
- **Top industries** from winning companies
- **Company size bands** from winning companies
- **Job titles and seniority** from buyer contacts
- **Geographies** from winning companies

Group into 2-3 distinct micro-segments based on the data (e.g., "Enterprise Marketing Leaders", "Mid-Market Sales Directors", "Startup Founders").

### 2. Translate ICP to LinkedIn targeting facets

For each micro-segment, map ICP dimensions to LinkedIn targeting entities.

**Job Titles** — search for exact LinkedIn targeting entities:
```
linkedin_ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:titles", query: "<title from ICP>")
```

**Job Functions:**
```
linkedin_ads__tool_get_targeting_facets()
```
Then search within job functions for relevant matches.

**Seniorities:**
```
linkedin_ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:seniorities", query: "<level>")
```

**Industries:**
```
linkedin_ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:industries", query: "<industry from ICP>")
```

**Company Sizes:**
```
linkedin_ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:staffCountRanges", query: "<size range>")
```

**Locations:**
```
linkedin_ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:locations", query: "<geo from ICP>")
```

Build the targeting criteria object for each micro-segment using AND logic:
```json
{
  "include": {
    "and": [
      {"or": {"urn:li:adTargetingFacet:titles": ["<title URNs>"]}},
      {"or": {"urn:li:adTargetingFacet:seniorities": ["<seniority URNs>"]}},
      {"or": {"urn:li:adTargetingFacet:industries": ["<industry URNs>"]}},
      {"or": {"urn:li:adTargetingFacet:staffCountRanges": ["<size URNs>"]}},
      {"or": {"urn:li:adTargetingFacet:locations": ["<location URNs>"]}}
    ]
  }
}
```

### 3. Estimate audience sizes

For each micro-segment targeting combination, check the audience size:

```
linkedin_ads__tool_get_audience_counts(ad_account_id: <id>, targeting_criteria: <targeting object>)
```

Evaluate each segment:
- **Too narrow** (<1,000): broaden titles or add related job functions
- **Narrow but viable** (1,000-10,000): good for ABM, may need higher bids
- **Sweet spot** (10,000-100,000): ideal for micro-campaigns
- **Too broad** (>300,000): add more filters to tighten

Iterate on targeting until each segment hits a viable audience size. Document adjustments made.

### 4. Check for overlap with existing campaigns

Review existing campaigns to avoid audience overlap:

```
linkedin_ads__tool_get_campaign_groups(ad_account_id: <id>)
linkedin_ads__tool_get_campaigns(ad_account_id: <id>, status_filter: "ACTIVE")
```

For each active campaign, compare targeting criteria. Flag overlaps and recommend:
- Exclude overlapping audiences
- Merge with existing campaigns if targeting is very similar
- Proceed if distinct enough

### 5. Present campaign structure for approval

**CRITICAL: Wait for user approval before creating anything.**

Present the proposed structure:

```
┌─────────────────────────────────────────────────────────────────────┐
│ PROPOSED MICRO-CAMPAIGN STRUCTURE                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Campaign Group: "[ICP Segment] — Micro Campaigns"                   │
│                                                                     │
│ ├── Campaign 1: "[Segment A Name]"                                  │
│ │   Objective: [Lead Gen / Website Visits / Engagement]             │
│ │   Targeting:                                                      │
│ │     Titles: [list]                                                │
│ │     Seniority: [level]                                            │
│ │     Industries: [list]                                            │
│ │     Company Size: [range]                                         │
│ │     Location: [geo]                                               │
│ │   Est. Audience: [N]                                              │
│ │   Daily Budget: $[X]                                              │
│ │   Bid Strategy: [strategy]                                        │
│ │                                                                   │
│ ├── Campaign 2: "[Segment B Name]"                                  │
│ │   [same structure]                                                │
│ │                                                                   │
│ └── Campaign 3: "[Segment C Name]"                                  │
│     [same structure]                                                │
│                                                                     │
│ Total Daily Budget: $[X]                                            │
│ Total Est. Audience: [N]                                            │
│ Recommended Duration: [N] weeks minimum                             │
└─────────────────────────────────────────────────────────────────────┘

Approve all? Or select specific campaigns (e.g., "1 and 2 only")
```

### 6. Create campaign group

After user approval, create the campaign group:

```
linkedin_ads__tool_create_campaign_group(
  ad_account_id: <id>,
  name: "[ICP Segment] — Micro Campaigns",
  status: "PAUSED"
)
```

### 7. Create campaigns

For each approved micro-segment, create a campaign in PAUSED status:

```
linkedin_ads__tool_create_campaign(
  ad_account_id: <id>,
  campaign_group_id: <group_id>,
  name: "[Segment Name]",
  objective_type: "LEAD_GENERATION",
  targeting_criteria: <targeting object from step 2>,
  daily_budget_amount: <amount>,
  daily_budget_currency: "USD",
  cost_type: "CPM",
  status: "PAUSED"
)
```

All campaigns are created PAUSED — the user controls when to activate.

### 8. Create creatives

For each campaign, create 2 creative variations for A/B testing.

Ask the user for:
- Landing page URL
- Any specific messaging, value props, or offers to include

Then create variations:

**Variation A — Pain point focus:**
```
linkedin_ads__tool_create_creative(
  campaign_id: <id>,
  commentary: "<Segment-specific pain point intro — 150 chars visible>",
  share_media_title: "<Pain point headline — 70 chars max>",
  share_media_description: "<Supporting detail>",
  destination_url: "<landing page URL>",
  call_to_action_type: "LEARN_MORE",
  status: "PAUSED"
)
```

**Variation B — Outcome focus:**
```
linkedin_ads__tool_create_creative(
  campaign_id: <id>,
  commentary: "<Segment-specific outcome/result intro — 150 chars visible>",
  share_media_title: "<Outcome headline — 70 chars max>",
  share_media_description: "<Supporting detail>",
  destination_url: "<landing page URL>",
  call_to_action_type: "LEARN_MORE",
  status: "PAUSED"
)
```

Creative guidelines per segment:
- **Headlines**: reference the persona's role or pain point directly
- **Intro text**: speak to the specific segment's challenges, not generic benefits
- **CTA**: match the campaign objective (LEARN_MORE for awareness, SIGN_UP for lead gen, REQUEST_DEMO for high-intent)

### 9. Output campaign summary

```
LinkedIn Micro Campaigns — Created
═══════════════════════════════════════════════════

Campaign Group: [Name] (PAUSED)
Ad Account: [Account Name]

┌──────────────────────┬──────────┬───────────┬──────────┬──────────────┐
│ Campaign             │ Audience │ Budget/day│ Status   │ Creatives    │
├──────────────────────┼──────────┼───────────┼──────────┼──────────────┤
│ [Segment A]          │ [N]      │ $[X]      │ PAUSED   │ 2 variations │
│ [Segment B]          │ [N]      │ $[X]      │ PAUSED   │ 2 variations │
│ [Segment C]          │ [N]      │ $[X]      │ PAUSED   │ 2 variations │
├──────────────────────┼──────────┼───────────┼──────────┼──────────────┤
│ TOTAL                │ [N]      │ $[X]      │          │ [N] total    │
└──────────────────────┴──────────┴───────────┴──────────┴──────────────┘

Targeting Summary per Campaign:
[Campaign 1]: [titles] + [seniority] + [industries] + [size] + [geo]
[Campaign 2]: [titles] + [seniority] + [industries] + [size] + [geo]
[Campaign 3]: [titles] + [seniority] + [industries] + [size] + [geo]

ICP Data Source: [HubSpot CRM / Manual Input]
Deals Analyzed: [N] (if from CRM)

Next Steps:
1. Review creatives and update copy/images as needed
2. Set campaign group status to ACTIVE when ready to launch
3. Monitor for 7 days before optimizing
4. Run /linkedin-ads-audit after 14 days to evaluate performance

Estimated Monthly Spend: $[X]
Estimated Monthly Reach: [N] impressions
```

### 10. Record findings

For each micro-campaign created, call `mcp__cogny__create_finding`:

```json
{
  "title": "Micro-campaign created: VP Marketing at SaaS 200-1K employees (audience: 34,200)",
  "body": "Created LinkedIn campaign targeting VP/Director Marketing at SaaS companies with 200-1000 employees in US/UK. Audience size 34,200. Daily budget $50. Based on CRM analysis showing this segment has 42% win rate and $45K avg deal size. 2 creative variations (pain point + outcome). Campaign in PAUSED status.",
  "action_type": "campaign_creation",
  "expected_outcome": "Generate 15-25 qualified leads per month at <$80 CPL",
  "estimated_impact_usd": 3000,
  "priority": "medium"
}
```

Action types for micro-campaigns:
- `campaign_creation` — new campaigns built from ICP data
- `targeting_refinement` — audience adjustments based on size/overlap
- `creative_refresh` — new ad variations for testing
- `budget_optimization` — spend reallocation across segments
- `audience_overlap` — overlap detection and exclusion recommendations
