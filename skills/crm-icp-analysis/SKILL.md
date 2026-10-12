---
name: crm-icp-analysis
description: Analyze CRM data (HubSpot, Pipedrive or Upsales) to build a data-driven Ideal Customer Profile from closed-won deals, contacts, and companies
version: "1.1.2"
requires: cogny-mcp
author: Cogny AI
platforms: [hubspot, pipedrive, upsales]
user-invocable: true
argument-hint: "[full|companies|contacts|deals]"
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
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Pipedrive__list_persons
  - mcp__cogny__mcp__Pipedrive__list_pipelines
  - mcp__cogny__mcp__Pipedrive__list_stages
  - mcp__cogny__mcp__Pipedrive__list_deal_fields
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_opportunities
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__list_contacts
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__mcp__Upsales__list_leads
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - Bash
  - Read
  - Write
---

# CRM ICP Analysis

Build a data-driven Ideal Customer Profile by analyzing closed-won deals, associated contacts, and companies in your CRM (HubSpot, Pipedrive or Upsales). Identifies patterns in industries, company sizes, job titles, deal sizes, sales cycles, and lead sources that predict revenue.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Usage

`/crm-icp-analysis` — full ICP analysis across all dimensions
`/crm-icp-analysis companies` — company firmographic analysis only
`/crm-icp-analysis contacts` — buyer persona analysis only
`/crm-icp-analysis deals` — deal pattern analysis only

## Works with

All three CRMs connect read-only. HubSpot is primary; the steps show the Pipedrive and Upsales calls where they differ.

| Job | HubSpot (primary) | Pipedrive | Upsales | What differs |
|-----|-------------------|-----------|---------|--------------|
| Field definitions | `get_properties`, `search_properties` | `list_deal_fields`, `list_stages` | `get_metadata` | Pipedrive custom fields are hash keys; Upsales custom fields are `custom.<id>` |
| Won / lost deals | `search_crm_objects` (`deals`, `hs_is_closed_won` / `hs_is_closed`) | `list_deals(status: "won" / "lost")` | `list_orders` (probability 100 = won, 0 = lost) | Pipedrive uses `won_time` / `lost_time`; Upsales uses the order `date` |
| Companies | `get_crm_objects` (`companies`) | `list_organizations` | `list_accounts` | Industry and employee count are standard in HubSpot, usually custom elsewhere |
| Buyers | `get_crm_objects` (`contacts`) | `list_persons` | `list_contacts` | Job title may be missing or custom; say so instead of guessing seniority |
| Lead source | `hs_analytics_source` | custom field, if any | custom field or `list_leads` source | Often absent outside HubSpot; then skip that dimension and its scoring weight |

If more than one CRM is connected, run the analysis per CRM and present them side by side. Never pool deal amounts across CRMs or currencies; each deal carries its own currency.

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
CRM ICP Analysis needs your marketing data through Cogny's MCP gateway.

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
(Integrations → Connect), then run /crm-icp-analysis again.
Stripe (subscriptions) or Fortnox (customers, invoices), if connected, give only a payer-only
partial view (who pays, at what price, who cancels or stops buying), with no firmographics,
personas or win rates; /marketing-brain can seed from them in the meantime.
```

## Steps

### 1. Discover available properties

Before querying data, understand what fields exist:

```
mcp__cogny__mcp__HubSpot__get_properties(objectType: "deals")
mcp__cogny__mcp__HubSpot__get_properties(objectType: "companies")
mcp__cogny__mcp__HubSpot__get_properties(objectType: "contacts")
```

Identify key properties for analysis:
- **Deals:** dealstage, hs_is_closed_won, hs_is_closed, amount, deal_currency_code, closedate, createdate, pipeline, dealtype, hs_analytics_source
- **Companies:** industry, numberofemployees, annualrevenue, city, state, country, type
- **Contacts:** jobtitle, hs_persona, lifecyclestage, hs_analytics_source

Note any custom properties that look ICP-relevant (e.g., custom industry fields, company tier, segment tags).

**Pipedrive:** `mcp__cogny__mcp__Pipedrive__list_deal_fields()` decodes deal custom-field keys; `list_pipelines` and `list_stages` give the stage map. Organization fields have no definitions tool, so ask the user which keys hold industry and employee count.

**Upsales:** `mcp__cogny__mcp__Upsales__get_metadata()` lists custom fields, currencies and stages. Look for custom fields holding industry, size or segment.

### 2. Analyze closed-won deals

Search for closed-won deals to establish the revenue baseline. Filter on `hs_is_closed_won`, not
`dealstage = closedwon`: custom pipelines use their own stage ids, so a stage filter misses their wins.

```
mcp__cogny__mcp__HubSpot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [{"propertyName": "hs_is_closed_won", "operator": "EQ", "value": "true"}]}],
  properties: ["dealname", "amount", "deal_currency_code", "closedate", "createdate", "pipeline", "dealstage", "dealtype", "hs_analytics_source"],
  sorts: [{"propertyName": "closedate", "direction": "DESCENDING"}],
  limit: 200
)
```

Check the `total` count — paginate if needed to capture full dataset.

Calculate:
- **Total closed-won deals** and **total revenue**
- **Average deal size** (mean and median)
- **Deal size distribution**: bucket into tiers per currency (e.g., <5K, 5-25K, 25-100K, 100K+ [ccy])
- **Average sales cycle length**: days from createdate to closedate
- **Sales cycle by deal size tier**
- **Win rate by pipeline** (if multiple pipelines exist)
- **Lead source breakdown**: which sources produce closed-won deals

Also search closed-lost for comparison (`hs_is_closed = true` AND `hs_is_closed_won = false`, which covers every pipeline):

```
mcp__cogny__mcp__HubSpot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [
    {"propertyName": "hs_is_closed", "operator": "EQ", "value": "true"},
    {"propertyName": "hs_is_closed_won", "operator": "EQ", "value": "false"}
  ]}],
  properties: ["dealname", "amount", "deal_currency_code", "closedate", "createdate", "pipeline", "dealstage", "hs_analytics_source"],
  limit: 200
)
```

Compare closed-won vs closed-lost to identify discriminating patterns.

**Pipedrive:** `mcp__cogny__mcp__Pipedrive__list_deals(status: "won", limit: 500)` and again with `status: "lost"`; follow `next_cursor` until it is null. Use `value` + `currency`, `add_time` → `won_time` for the cycle, and `lost_reason` on lost deals (a direct anti-ICP signal HubSpot often lacks).

**Upsales:** `mcp__cogny__mcp__Upsales__list_orders(sort: "-date", limit: 1000)` and page with `offset` until `metadata.total`. Split by stage probability (100 = won, 0 = lost); use `value` + `currency` and the order `date`. Upsales has no created-date-to-close field on orders, so derive cycle length from the linked opportunity's dates if present, otherwise mark it N/A.

### 3. Analyze winning companies

Fetch companies associated with closed-won deals. Use `get_crm_objects` with deal IDs to get associations, then batch-fetch the associated companies:

```
mcp__cogny__mcp__HubSpot__get_crm_objects(
  objectType: "companies",
  objectIds: [<associated company IDs>],
  properties: ["name", "industry", "numberofemployees", "annualrevenue", "city", "state", "country", "type", "domain"]
)
```

**Pipedrive:** `list_organizations` (page with `cursor`) and keep the `org_id`s from won deals. **Upsales:** `list_accounts(filters: [{"field": "id", "comparator": "in", "value": [<client ids from orders>]}])`.

Build firmographic profile:
- **Industry breakdown**: rank industries by deal count and total revenue
- **Company size distribution**: by employee count bands (1-50, 51-200, 201-1000, 1000+)
- **Revenue range**: annual revenue bands of winning companies
- **Geography**: country, state/region concentration
- **Company type**: customer, partner, prospect categorization

Flag:
- Industries that appear in >20% of closed-won deals (core ICP)
- Company size sweet spots (highest win rate bands)
- Geographic clusters

### 4. Analyze buyer personas

Fetch contacts associated with closed-won deals, then batch-fetch:

```
mcp__cogny__mcp__HubSpot__get_crm_objects(
  objectType: "contacts",
  objectIds: [<associated contact IDs>],
  properties: ["jobtitle", "hs_persona", "lifecyclestage", "hs_analytics_source"]
)
```

**Pipedrive:** `list_persons(org_id: <id>)` per winning organization (or the deal's `person_id`). **Upsales:** `list_contacts(filters: [{"field": "client.id", "comparator": "in", "value": [<client ids>]}])`.

Build buyer persona profile:
- **Job title clustering**: group similar titles (e.g., "VP Marketing", "Head of Marketing", "Marketing Director" = Marketing Leadership)
- **Seniority distribution**: C-level, VP, Director, Manager, Individual Contributor
- **Functional area**: Marketing, Sales, Product, Engineering, Finance, Operations
- **Number of contacts per deal**: single-threaded vs multi-threaded deals
- **Lead source by persona**: how different personas find you

Flag:
- Dominant buyer persona (>30% of closed-won contacts)
- Multi-threaded deals that win at higher rates
- Personas that correlate with larger deal sizes

### 5. Cross-dimensional analysis

Combine insights across deals, companies, and contacts:

- **Best segment**: Industry + Company Size + Persona that produces highest win rate
- **Highest-value segment**: combination that produces largest average deal size
- **Fastest-closing segment**: combination with shortest sales cycle
- **Lead source efficiency**: which sources produce best-fit leads (not just most leads)
- **Anti-ICP patterns**: segments with low win rates or high loss rates

### 6. Output ICP definition

```
CRM ICP Analysis
CRM: [HubSpot / Pipedrive / Upsales]
Data basis: [N] closed-won deals, [N] companies, [N] contacts
Period: [earliest close date] to [latest close date]
Total revenue analyzed: [X] [currency]

═══════════════════════════════════════════════════
IDEAL CUSTOMER PROFILE
═══════════════════════════════════════════════════

Company Firmographics:
  Industry:        [Top 1-3 industries] ([X]% of wins)
  Employee Count:  [Range] (sweet spot: [X-Y])
  Annual Revenue:  [Range] [ccy]
  Geography:       [Top regions]

Buyer Persona:
  Primary Buyer:   [Title cluster] ([X]% of deals)
  Secondary Buyer: [Title cluster] ([X]% of deals)
  Seniority:       [Level] and above
  Function:        [Department]

Deal Characteristics:
  Average Deal Size:    [X] [ccy] (median: [Y] [ccy])
  Sweet Spot Range:     [X] - [Y] [ccy]
  Average Sales Cycle:  [N] days
  Best Lead Sources:    [Source 1], [Source 2]

Win Rate Analysis:
  Overall Win Rate:     [X]%
  Best Segment Rate:    [X]% ([segment description])
  Worst Segment Rate:   [X]% ([segment description])

═══════════════════════════════════════════════════
ICP FIT SCORING MODEL
═══════════════════════════════════════════════════

Dimension          | Weight | Criteria
───────────────────|────────|─────────────────────────
Industry           |  25%   | [Top industries] = match
Company Size       |  20%   | [Range] employees = match
Seniority          |  20%   | [Level]+ = match
Job Function       |  15%   | [Functions] = match
Deal Size Potential|  10%   | [X]+ [ccy] = match
Lead Source        |  10%   | [Sources] = match

Scoring: 80-100 = Strong fit | 60-79 = Moderate fit | <60 = Weak fit

═══════════════════════════════════════════════════
ANTI-ICP (AVOID)
═══════════════════════════════════════════════════

- [Pattern 1 that predicts losses]
- [Pattern 2 that predicts losses]
- [Pattern 3 that predicts losses]

Top 3 Actions:
1. [Highest-impact recommendation]
2. [Second recommendation]
3. [Third recommendation]
```

### 7. Record findings

For EVERY actionable ICP insight, record one review item. Detect the plan from the tools that
exist: on **Cloud** (`create_ticket` exists) call `mcp__cogny__create_ticket` first, with
`execution_target: "manual"` and the fields mapped per section 2 of the routing guide. Only on
**Solo** (no `create_ticket`) call `mcp__cogny__create_finding`:

```json
{
  "title": "ICP sweet spot: SaaS companies 200-1000 employees close at 2.3x average rate",
  "body": "Analysis of 87 closed-won deals shows SaaS companies with 200-1000 employees have a 42% win rate vs 18% overall. Average deal size 45K [ccy], 34-day sales cycle. These companies represent only 23% of pipeline but 51% of revenue. Recommend: prioritize this segment in outbound and ad targeting.",
  "action_type": "icp_refinement",
  "expected_outcome": "Increase win rate by focusing pipeline on high-fit segments",
  "estimated_impact_usd": 5000,
  "priority": "high"
}
```

Action types for ICP analysis:
- `icp_refinement` — ICP definition updates, scoring model changes
- `targeting_refinement` — ad/outbound targeting changes based on ICP
- `pipeline_optimization` — sales process changes for specific segments
- `lead_source_optimization` — invest more in high-ICP-fit lead sources
- `disqualification_rule` — anti-ICP patterns to filter out early

## Recording findings

Use `create_ticket` first when the workspace has it (Cloud), and `create_finding` only when it doesn't (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
