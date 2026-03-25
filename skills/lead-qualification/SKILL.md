---
name: lead-qualification
description: Research and qualify business leads against your ICP
version: "1.0.0"
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
---

# Lead Qualification

Research a lead or list of leads to determine ICP fit, company details, and deal potential.

## Usage

`/lead-qualification "John Smith john@company.com"` — qualify a single lead
`/lead-qualification` — then paste a list of leads

## Steps

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
- Do they run ads? (check for tracking pixels, ad landing pages)
- What's their likely marketing budget?

### 4. Score each lead

```
Lead: [Name] ([email])
Company: [Company] — [what they do]
Role: [Title/seniority if found]
ICP Fit: HIGH / MEDIUM / LOW / NONE

Signals:
+ [Positive signal, e.g., "Runs Google Ads"]
+ [Another positive]
- [Negative signal, e.g., "Personal email"]
- [Another negative]

Estimated deal value: [based on company size]
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
