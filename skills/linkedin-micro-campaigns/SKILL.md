---
name: linkedin-micro-campaigns
description: Create precision-targeted LinkedIn ad campaigns for specific ICP segments — translates CRM data to LinkedIn targeting
version: "1.1.1"
requires: cogny-mcp
author: Cogny AI
platforms: [hubspot, pipedrive, upsales, fibbler, linkedin-ads]
user-invocable: true
argument-hint: "<ICP description or segment>"
allowed-tools:
  # CRM tools for ICP data extraction (all read-only)

  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Pipedrive__list_persons
  - mcp__cogny__mcp__Pipedrive__list_deal_fields
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__list_contacts
  - mcp__cogny__mcp__Upsales__get_metadata
  # Fibbler (warm accounts, titles that engage; read-only)
  - mcp__cogny__mcp__app-fibbler-co__get_warm_accounts
  - mcp__cogny__mcp__app-fibbler-co__get_audience_titles
  - mcp__cogny__mcp__app-fibbler-co__get_deal_campaign_breakdown
  # LinkedIn Ads read tools (create_* tools ask first, never pre-approved)
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign_groups
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaigns
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_targeting_facets
  - mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_audience_counts
  - mcp__cogny__list_integrations
  # Findings
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - Bash
  - Read
  - Write
---

# LinkedIn Micro Campaigns

Create highly targeted LinkedIn ad campaigns for specific ICP segments. Translates your Ideal Customer Profile (from CRM data or manual input) into precision LinkedIn targeting criteria, estimates audience sizes, and builds campaign groups with campaigns and creatives.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

**Tip:** Run `/crm-icp-analysis` first to generate a data-driven ICP, then feed the output into this skill. You can also run `/crm-sales-momentum` to identify which segments close fastest and target those specifically.

## Usage

`/linkedin-micro-campaigns "VP Marketing at SaaS companies, 200-1000 employees"` — create campaigns from a description
`/linkedin-micro-campaigns` — pull ICP from connected CRM data automatically

## Works with

| Job | Primary | Also answers it | What differs |
|-----|---------|-----------------|--------------|
| Closed-won segments (ICP input) | HubSpot (`search_crm_objects`) | Pipedrive (`list_deals` `status: "won"` + `list_organizations`, `list_persons`), Upsales (`list_orders` + `list_accounts`, `list_contacts`) | Industry and size fields are custom in Pipedrive (decode with `list_deal_fields`) and often custom in Upsales (`get_metadata`); job titles may be sparse outside HubSpot |
| Titles that already engage | Fibbler `get_audience_titles` | — | Shows titles reached and whether they're targeted today |
| Accounts warming up (ABM seed) | Fibbler `get_warm_accounts` | — | Companies engaging but not yet deals in the CRM; a signal, not intent |
| Targeting, sizing, creation | LinkedIn Ads | — | Required; every `create_*` call asks first |

If several CRMs are connected, build segments per CRM and show them side by side; never pool deal values in different currencies.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop
before calling anything else:

```
LinkedIn Micro Campaigns needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect LinkedIn Ads (required), plus HubSpot,
   Pipedrive or Upsales and Fibbler if you use them.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts` is missing,
say "connect LinkedIn Ads in Cogny" and stop. A CRM is optional: with one connected the ICP
is extracted automatically; without one, the ICP comes from the argument.

## Prerequisites Check

Call `mcp__cogny__list_integrations` once to see which CRM (HubSpot, Pipedrive, Upsales) and
Fibbler are connected, then verify LinkedIn Ads access (required) and note the account currency:

```
mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
```

For HubSpot, also verify with `mcp__cogny__mcp__HubSpot__get_user_details`.

## Failure handling

- **LinkedIn Ads health check.** `list_integrations` can read `healthy` for a revoked LinkedIn
  token. If `tool_list_ad_accounts` (or any later LinkedIn call) returns 401, "unauthorized",
  Forbidden or a scope error, mark LinkedIn Ads 🔴 and **stop**. Don't retry the call and don't
  build segments on partial data.
- **Reconnect steps:** in Cogny, open Integrations → LinkedIn Ads → Reconnect, sign in with a
  LinkedIn user who has at least a Campaign Manager role on the ad account (creating campaigns
  needs more than Viewer), then re-run `/linkedin-micro-campaigns`.
- **Unhealthy Fibbler or CRM** (listed as not healthy, or its first read returns 401,
  Forbidden or a scope error): say "reconnect <integration> in Cogny", skip that source, and
  continue with the rest. On a 5xx or timeout, retry once, then mark it ⚠ and continue.
- **No argument and no usable CRM:** ask for the ICP as an argument (e.g.
  `/linkedin-micro-campaigns "VP Marketing at SaaS companies, 200-1000 employees, Nordics"`)
  and stop. Don't invent an ICP.

## Steps

### 1. Establish ICP targeting inputs

**If ICP description is provided as argument**, parse it for:
- Job titles / functions / seniority
- Industries
- Company sizes
- Geographic targets
- Any other targeting dimensions mentioned

**If no argument is provided and a CRM is connected**, extract ICP from it. HubSpot (primary):

Pull closed-won deal data to identify top-performing segments:

```
mcp__cogny__mcp__HubSpot__search_crm_objects(
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

**Pipedrive instead:** `mcp__cogny__mcp__Pipedrive__list_deals(status: "won", sort_by: "update_time", sort_direction: "desc", limit: 100)`, then `list_organizations` and `list_persons` for the linked `org_id` / `person_id`. Industry and employee count are usually custom fields that come back as hash keys: decode deal fields with `list_deal_fields`; for organization fields (no definitions tool) ask the user which key is which. Values are in each deal's `currency`.

**Upsales instead:** `mcp__cogny__mcp__Upsales__list_orders(sort: "-date", limit: 200)` and keep orders at probability 100 (won); fetch companies with `list_accounts(filters: [{"field": "id", "comparator": "in", "value": [<client ids>]}])` and buyers with `list_contacts`. Use `get_metadata` to find custom industry/size fields.

**Enhanced when Fibbler is connected:**
- `mcp__cogny__mcp__app-fibbler-co__get_audience_titles(scope: "total", time_period: "90d")`: titles that already engage. Prefer them in step 2 and drop titles with high impressions and near-zero engagement.
- `mcp__cogny__mcp__app-fibbler-co__get_warm_accounts(channel: "linkedin", time_period: "90d", limit: 50)`: companies heating up but not yet in the CRM. Offer them as an ABM segment (look each up with `tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:employers", query: "<company>")`), labelled as a signal, not intent.
- `mcp__cogny__mcp__app-fibbler-co__get_deal_campaign_breakdown(group_by: "campaign", source: "LINKEDIN")`: existing campaigns already linked to pipeline, so new segments don't duplicate a working one.

Group into 2-3 distinct micro-segments based on the data (e.g., "Enterprise Marketing Leaders", "Mid-Market Sales Directors", "Startup Founders").

### 2. Translate ICP to LinkedIn targeting facets

For each micro-segment, map ICP dimensions to LinkedIn targeting entities.

**Job Titles** — search for exact LinkedIn targeting entities:
```
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:titles", query: "<title from ICP>")
```

Seniorities, company sizes and job functions **don't support typeahead**: a `query` on them
returns 400 from LinkedIn. Enumerate them once with `finder: "adTargetingFacet"` and no
`query`, then pick the matching values from the list. The default `limit` is 20; job functions
need `limit: 50` to return all of them. `tool_get_targeting_facets()` shows each
facet's `available_entity_finders` if in doubt (`TYPEAHEAD` vs `AD_TARGETING_FACET`).

**Job Functions:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:jobFunctions", finder: "adTargetingFacet", limit: 50)
```

**Seniorities:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:seniorities", finder: "adTargetingFacet")
```

**Industries:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:industries", query: "<industry from ICP>")
```

**Company Sizes:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:staffCountRanges", finder: "adTargetingFacet")
```

**Locations:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities(facet_urn: "urn:li:adTargetingFacet:locations", query: "<geo from ICP>")
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
mcp__cogny__mcp__LinkedIn_Ads__tool_get_audience_counts(ad_account_id: <id>, targeting_criteria: <targeting object>)
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
mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign_groups(ad_account_id: <id>)
mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaigns(ad_account_id: <id>, status_filter: ["ACTIVE"])
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

After user approval, create the campaign group (write tool; it asks first):

```
mcp__cogny__mcp__LinkedIn_Ads__tool_create_campaign_group(
  ad_account_id: <id>,
  name: "[ICP Segment] — Micro Campaigns",
  status: "PAUSED"
)
```

### 7. Create campaigns

For each approved micro-segment, create a campaign in PAUSED status:

```
mcp__cogny__mcp__LinkedIn_Ads__tool_create_campaign(
  ad_account_id: <id>,
  campaign_group_id: <group_id>,
  name: "[Segment Name]",
  objective_type: "LEAD_GENERATION",
  targeting_criteria: <targeting object from step 2>,
  daily_budget_amount: "<amount>",
  daily_budget_currency: "<account currency from tool_list_ad_accounts>",
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

You also need the authoring Page (`author_organization_urn`, e.g. from an existing creative or Campaign Manager) and an image: upload it with `tool_upload_image` (asks first) or pass `image_url`. Without an image the ad is text-only and the URL, headline and CTA don't render. New creatives are created as `DRAFT` (LinkedIn can't create them paused), so they won't serve until the user activates them.

Then create variations (write tool; it asks first):

**Variation A — Pain point focus:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_create_creative(
  ad_account_id: <id>,
  campaign_id: <id>,
  author_organization_urn: "urn:li:organization:<id>",
  commentary: "<Segment-specific pain point intro — 150 chars visible>",
  headline: "<Pain point headline — 70 chars max>",
  image_urn: "<urn:li:image:… from tool_upload_image>",
  destination_url: "<landing page URL>",
  call_to_action_type: "LEARN_MORE",
  status: "DRAFT"
)
```

**Variation B — Outcome focus:**
```
mcp__cogny__mcp__LinkedIn_Ads__tool_create_creative(
  ad_account_id: <id>,
  campaign_id: <id>,
  author_organization_urn: "urn:li:organization:<id>",
  commentary: "<Segment-specific outcome/result intro — 150 chars visible>",
  headline: "<Outcome headline — 70 chars max>",
  image_urn: "<urn:li:image:… from tool_upload_image>",
  destination_url: "<landing page URL>",
  call_to_action_type: "LEARN_MORE",
  status: "DRAFT"
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
│ [Segment A]          │ [N]      │ [X]       │ PAUSED   │ 2 drafts     │
│ [Segment B]          │ [N]      │ [X]       │ PAUSED   │ 2 drafts     │
│ [Segment C]          │ [N]      │ [X]       │ PAUSED   │ 2 drafts     │
├──────────────────────┼──────────┼───────────┼──────────┼──────────────┤
│ TOTAL                │ [N]      │ $[X]      │          │ [N] total    │
└──────────────────────┴──────────┴───────────┴──────────┴──────────────┘

Targeting Summary per Campaign:
[Campaign 1]: [titles] + [seniority] + [industries] + [size] + [geo]
[Campaign 2]: [titles] + [seniority] + [industries] + [size] + [geo]
[Campaign 3]: [titles] + [seniority] + [industries] + [size] + [geo]

ICP Data Source: [HubSpot / Pipedrive / Upsales / Fibbler warm accounts / Manual Input]
Deals Analyzed: [N] (if from CRM)

Next Steps:
1. Review the DRAFT creatives and update copy/images as needed
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

On Cloud, send the same content with `create_ticket`, mapping the fields per section 2 of the routing guide.

Action types for micro-campaigns:
- `campaign_creation` — new campaigns built from ICP data
- `targeting_refinement` — audience adjustments based on size/overlap
- `creative_refresh` — new ad variations for testing
- `budget_optimization` — spend reallocation across segments
- `audience_overlap` — overlap detection and exclusion recommendations

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
