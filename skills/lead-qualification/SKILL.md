---
name: lead-qualification
description: Research and qualify business leads against your ICP
version: "1.1.1"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<name> <email or company>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Optional, when a Cogny workspace is connected (all read-only)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__Upsales__list_contacts
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__app-fibbler-co__get_company_engagement
  - mcp__cogny__mcp__app-fibbler-co__get_influenced_deals
---

# Lead Qualification

Research a lead or list of leads to determine ICP fit, company details, and deal potential.

## Usage

`/lead-qualification "John Smith john@company.com"` — qualify a single lead
`/lead-qualification` — then paste a list of leads

## Works with

Runs on public web research alone. If a Cogny workspace is connected, it adds first-party signals; call `mcp__cogny__list_integrations` once to see what's there. If it isn't, skip the connected rows and say what connecting adds.

| Job | Primary | Also answers it | What it adds |
|-----|---------|-----------------|--------------|
| Company, role, size | WebSearch / WebFetch | — | Always available |
| Already in the CRM? | HubSpot `search_crm_objects` | Upsales `list_contacts` / `list_accounts`; Pipedrive `list_deals(org_id)` once you know the org | Existing customer, open deal or past loss changes the next step |
| Engaging with our ads? | Fibbler `get_company_engagement` | — | LinkedIn impressions, clicks and engagements by company |

Pipedrive has no search tool here; only check it when the user gives an org id or the list is small enough to page `list_organizations`.

## Steps

### 0. Pin down the ICP
Scoring needs a target. If the user hasn't given one, ask: "Who is your ideal customer (industry, company size, region, buyer role, must-have signals like 'runs paid media')?" If they'd rather not spell it out, infer a draft from their own site: WebFetch their homepage, pricing, customers/case-studies pages, and note who the copy, logos and pricing tiers address. Show the inferred ICP in 3–5 bullets and get a yes or corrections before scoring. Score every lead against that confirmed ICP and repeat it at the top of the output.

### 1. Parse the lead(s)
Extract name, email, and company from input. If email domain is personal (gmail, hotmail, outlook, yahoo, live), flag it — personal emails are a lower-quality B2B signal.

### 2. Research each lead
For each lead, WebSearch for:
- Full name + company → LinkedIn profile, role, seniority
- Company domain → website, size, industry
- Company + "marketing" or "advertising" → whether they do paid media

### 3. Assess company fit
WebFetch the company website if found:
- What do they sell?
- How big are they? (team page, about page, funding)
- Do they run ads? Check for tracking pixels with curl (WebFetch summarises the page and drops `<script>` tags):
  ```bash
  curl -sL -A "Mozilla/5.0" "https://<company-domain>/" | grep -oiE "googletagmanager\.com/gtm\.js|gtag/js\?id=(AW|G)-[A-Z0-9]+|fbevents\.js|snap\.licdn\.com|px\.ads\.linkedin\.com|analytics\.tiktok\.com|static\.ads-twitter\.com|bat\.bing\.com|redditstatic\.com/ads|hs-scripts\.com" | sort -u
  ```
  `AW-` IDs mean Google Ads conversion tracking; `fbevents.js` = Meta Pixel; `snap.licdn.com` = LinkedIn Insight Tag; GTM alone hides what's inside it, so say "GTM present, ad pixels unknown". Also look for ad landing pages (`/lp/`, `utm_` links).
- What's their likely marketing budget?

### 3b. Enhanced when connected: first-party signals

If Cogny isn't connected, skip this and note what connecting adds (whether the lead is already a customer, has an open or lost deal, or has been engaging with your LinkedIn ads).

- **CRM match.** HubSpot: `mcp__cogny__mcp__HubSpot__search_crm_objects` on `contacts` (filter `email` EQ the lead's email) and on `companies` (filter `domain` EQ the email domain). Upsales: `list_contacts(filters: [{"field": "email", "comparator": "eq", "value": "<email>"}])`, then `list_orders(filters: [{"field": "client.id", "comparator": "eq", "value": <account id>}])` for history. Pipedrive: page `mcp__cogny__mcp__Pipedrive__list_organizations` and match on name/domain, then `list_deals` with that `org_id`. Report: existing customer, open deal, closed-lost (with reason if present), or not found.
- **Ad engagement (Fibbler).** `mcp__cogny__mcp__app-fibbler-co__get_company_engagement(company_search: "<company>", time_period: "90d")` shows whether the company has been seeing and engaging with LinkedIn ads; `get_influenced_deals` tells you if it already sits in influenced pipeline. Treat engagement as a warmth signal, not intent.

Never write to the CRM from this skill. If the user wants the lead created or updated, tell them which record to change.

### 4. Score each lead

```
ICP: [confirmed ICP, one line]
Lead: [Name] ([email])
Company: [Company] — [what they do]
Role: [Title/seniority if found]
ICP Fit: HIGH / MEDIUM / LOW / NONE

Signals:
+ [Positive signal, e.g., "Runs Google Ads"]
+ [Another positive]
+ [First-party signal, e.g., "Fibbler: 1,240 LinkedIn impressions, 9 engagements in 90d"]
- [Negative signal, e.g., "Personal email"]
- [Another negative]

Estimated deal value: [based on company size]
CRM status: [Customer / Open deal / Lost (reason) / Not in CRM / Not checked]
Next step: [specific recommendation]
```

### 5. Summary table for multiple leads

```
┌──────────────┬──────────────────┬──────────┬───────────────┐
│     Name     │     Company      │ ICP Fit  │   Next Step   │
├──────────────┼──────────────────┼──────────┼───────────────┤
│ [Lead 1]     │ [Company]        │ HIGH     │ Send proposal │
│ [Lead 2]     │ [Unknown]        │ LOW      │ Disqualify    │
└──────────────┴──────────────────┴──────────┴───────────────┘
```
