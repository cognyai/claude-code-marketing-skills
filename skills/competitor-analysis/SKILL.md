---
name: competitor-analysis
description: Research competitor positioning, ads, pricing, and market gaps
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<company or URL>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
---

# Competitor Analysis

Research a competitor or market to understand positioning, pricing, strengths, and gaps.

## Usage

`/competitor-analysis hubspot.com` — analyze a specific competitor
`/competitor-analysis "marketing automation tools"` — analyze a market category

## Steps

### 1. Identify the competitive set
If given a company: WebSearch for "[company] competitors" and "[company] vs"
If given a category: WebSearch for "best [category] 2025" and "[category] comparison"

Build a list of 4-6 key competitors.

### 2. Analyze each competitor's positioning
For each competitor, WebFetch their homepage and key pages:
- **Tagline/headline**: How do they position themselves?
- **Target audience**: Who are they selling to?
- **Key features**: What do they emphasize?
- **Pricing**: What's the price point and model?
- **Social proof**: Customer logos, testimonials, case studies

### 3. Analyze their search presence
WebSearch for key terms in the market:
- Who ranks #1-3 for the main category keywords?
- What content strategy are they using? (blog, comparison pages, tools)
- Are they running Google Ads on brand/competitor terms?

### 4. Identify market gaps
Compare across all competitors:
- What features does everyone offer vs. unique differentiators?
- What pricing tier is underserved?
- What audience segment is ignored?
- What messaging angle is nobody using?

### 5. Report

```
Competitive Analysis: [Company/Market]

Competitive Landscape:
┌─────────────┬───────────────────┬──────────────┬───────────┐
│  Competitor  │    Positioning     │   Pricing    │ Strength  │
├─────────────┼───────────────────┼──────────────┼───────────┤
│ [Company 1] │ [tagline]         │ [price]      │ [key USP] │
│ [Company 2] │ [tagline]         │ [price]      │ [key USP] │
│ [Company 3] │ [tagline]         │ [price]      │ [key USP] │
└─────────────┴───────────────────┴──────────────┴───────────┘

Search Dominance:
- [keyword 1]: [who ranks #1]
- [keyword 2]: [who ranks #1]
- [keyword 3]: [who ranks #1]

Market Gaps:
1. [Gap description + opportunity]
2. [Gap description + opportunity]
3. [Gap description + opportunity]

Positioning Recommendation:
[Specific positioning advice based on gaps found]
```
