---
name: crm-icp-analysis
description: Analyze HubSpot CRM data to build a data-driven Ideal Customer Profile from closed-won deals, contacts, and companies
version: "1.0.0"
author: Cogny AI
platforms: [hubspot]
user-invocable: true
argument-hint: "[full|companies|contacts|deals]"
allowed-tools:
  - mcp__cogny__hubspot__*
  - mcp__cogny__create_finding
  - Bash
  - Read
  - Write
---

# CRM ICP Analysis

Build a data-driven Ideal Customer Profile by analyzing closed-won deals, associated contacts, and companies in your HubSpot CRM. Identifies patterns in industries, company sizes, job titles, deal sizes, sales cycles, and lead sources that predict revenue.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Usage

`/crm-icp-analysis` — full ICP analysis across all dimensions
`/crm-icp-analysis companies` — company firmographic analysis only
`/crm-icp-analysis contacts` — buyer persona analysis only
`/crm-icp-analysis deals` — deal pattern analysis only

## Prerequisites Check

Call `mcp__cogny__hubspot__get_user_details` to verify CRM access. Confirm read access to contacts, companies, and deals. If access is missing:

```
This skill requires HubSpot CRM access via Cogny's MCP server.
Sign up at https://cogny.com/agent and connect your HubSpot account.
```

## Steps

### 1. Discover available properties

Before querying data, understand what fields exist:

```
hubspot__get_properties(objectType: "deals")
hubspot__get_properties(objectType: "companies")
hubspot__get_properties(objectType: "contacts")
```

Identify key properties for analysis:
- **Deals:** dealstage, amount, closedate, createdate, pipeline, dealtype, hs_analytics_source
- **Companies:** industry, numberofemployees, annualrevenue, city, state, country, type
- **Contacts:** jobtitle, hs_persona, lifecyclestage, hs_analytics_source

Note any custom properties that look ICP-relevant (e.g., custom industry fields, company tier, segment tags).

### 2. Analyze closed-won deals

Search for closed-won deals to establish the revenue baseline:

```
hubspot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": "closedwon"}]}],
  properties: ["dealname", "amount", "closedate", "createdate", "pipeline", "dealtype", "hs_analytics_source"],
  sorts: [{"propertyName": "closedate", "direction": "DESCENDING"}],
  limit: 200
)
```

Check the `total` count — paginate if needed to capture full dataset.

Calculate:
- **Total closed-won deals** and **total revenue**
- **Average deal size** (mean and median)
- **Deal size distribution**: bucket into tiers (e.g., <$5K, $5-25K, $25-100K, $100K+)
- **Average sales cycle length**: days from createdate to closedate
- **Sales cycle by deal size tier**
- **Win rate by pipeline** (if multiple pipelines exist)
- **Lead source breakdown**: which sources produce closed-won deals

Also search closed-lost for comparison:

```
hubspot__search_crm_objects(
  objectType: "deals",
  filterGroups: [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": "closedlost"}]}],
  properties: ["dealname", "amount", "closedate", "createdate", "pipeline", "hs_analytics_source"],
  limit: 200
)
```

Compare closed-won vs closed-lost to identify discriminating patterns.

### 3. Analyze winning companies

Fetch companies associated with closed-won deals. Use `get_crm_objects` with deal IDs to get associations, then batch-fetch the associated companies:

```
hubspot__get_crm_objects(
  objectType: "companies",
  objectIds: [<associated company IDs>],
  properties: ["name", "industry", "numberofemployees", "annualrevenue", "city", "state", "country", "type", "domain"]
)
```

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
hubspot__get_crm_objects(
  objectType: "contacts",
  objectIds: [<associated contact IDs>],
  properties: ["jobtitle", "hs_persona", "lifecyclestage", "hs_analytics_source", "email", "firstname", "lastname"]
)
```

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
Data basis: [N] closed-won deals, [N] companies, [N] contacts
Period: [earliest close date] to [latest close date]
Total revenue analyzed: $[X]

═══════════════════════════════════════════════════
IDEAL CUSTOMER PROFILE
═══════════════════════════════════════════════════

Company Firmographics:
  Industry:        [Top 1-3 industries] ([X]% of wins)
  Employee Count:  [Range] (sweet spot: [X-Y])
  Annual Revenue:  $[Range]
  Geography:       [Top regions]

Buyer Persona:
  Primary Buyer:   [Title cluster] ([X]% of deals)
  Secondary Buyer: [Title cluster] ([X]% of deals)
  Seniority:       [Level] and above
  Function:        [Department]

Deal Characteristics:
  Average Deal Size:    $[X] (median: $[Y])
  Sweet Spot Range:     $[X] - $[Y]
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
Deal Size Potential|  10%   | $[X]+ = match
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

For EVERY actionable ICP insight, call `mcp__cogny__create_finding`:

```json
{
  "title": "ICP sweet spot: SaaS companies 200-1000 employees close at 2.3x average rate",
  "body": "Analysis of 87 closed-won deals shows SaaS companies with 200-1000 employees have a 42% win rate vs 18% overall. Average deal size $45K, 34-day sales cycle. These companies represent only 23% of pipeline but 51% of revenue. Recommend: prioritize this segment in outbound and ad targeting.",
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
