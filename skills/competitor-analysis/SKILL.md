---
name: competitor-analysis
description: Research competitor positioning, ads, pricing, and market gaps
version: "1.1.1"
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
  # Optional, when Cogny MCP is connected (all read-only)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Semrush__domain_overview
  - mcp__cogny__mcp__Semrush__domain_organic_competitors
  - mcp__cogny__mcp__Semrush__domain_organic_keywords
  - mcp__cogny__mcp__Semrush__domain_paid_keywords
  - mcp__cogny__mcp__Ahrefs__organic_competitors
  - mcp__cogny__mcp__Ahrefs__organic_keywords
  - mcp__cogny__mcp__Ahrefs__top_pages
  - mcp__cogny__mcp__Ahrefs__batch_analysis
  - mcp__cogny__mcp__cogny-ahrefs-lite__tool_domain_rating
  - mcp__cogny__mcp__cogny-ai-visibility__tool_check_ai_visibility
  - mcp__cogny__mcp__cogny-ai-visibility__tool_get_ai_visibility_history
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_news
---

# Competitor Analysis

Research a competitor or market to understand positioning, pricing, strengths, and gaps.

## Usage

`/competitor-analysis hubspot.com` — analyze a specific competitor
`/competitor-analysis "marketing automation tools"` — analyze a market category

## Works with

Runs with zero accounts (WebSearch/WebFetch). Each connected provider replaces a guess with data.

| Job | Primary | Also answers it | No account |
|-----|---------|-----------------|------------|
| Who the real competitors are | Semrush `domain_organic_competitors` | Ahrefs `organic_competitors` | WebSearch "[company] competitors" |
| Organic footprint and top pages | Semrush `domain_overview`, `domain_organic_keywords` | Ahrefs `organic_keywords`, `top_pages` | WebSearch |
| Paid search: are they bidding, on what | Semrush `domain_paid_keywords` | — | Google Ads Transparency Center (adstransparency.google.com), manual |
| Authority | Ahrefs `batch_analysis` (whole set in one call) | cogny-ahrefs-lite `tool_domain_rating` | — |
| Share of voice in AI answers | cogny-ai-visibility `tool_check_ai_visibility` | — | — |
| Recent launches, funding, pricing changes | cogny-brave-search `tool_brave_news` | `tool_brave_search` | WebSearch "[competitor] news" / "announces" |

Semrush and Ahrefs estimate traffic differently: pick one per table, or show both in separate columns. Write "Domain Rating by Ahrefs" next to every DR number.

## Steps

### 1. Identify the competitive set
If given a company: WebSearch for "[company] competitors" and "[company] vs"
If given a category: WebSearch for "best [category] [current year]" (take the year from today's date, never a hardcoded one) and "[category] comparison"

Build a list of 4-6 key competitors.

**Enhanced when connected:** If Cogny isn't connected, skip this and note what connecting adds (keyword-overlap competitors from Semrush/Ahrefs). Otherwise call `mcp__cogny__list_integrations` once: `mcp__cogny__mcp__Semrush__domain_organic_competitors` (`domain`, `database` = market country code) or `mcp__cogny__mcp__Ahrefs__organic_competitors` (`target`, `country`) returns the domains that actually compete for the same keywords. Merge with the WebSearch list and say which competitors only show up in one of them (search competitors you didn't know about are often the finding).

### 2. Analyze each competitor's positioning
For each competitor, WebFetch their homepage and key pages:
- **Tagline/headline**: How do they position themselves?
- **Target audience**: Who are they selling to?
- **Key features**: What do they emphasize?
- **Pricing**: What's the price point and model?
- **Social proof**: Customer logos, testimonials, case studies
- **Recent moves:** WebSearch `"<competitor>" news`, `"<competitor>" announces`, `"<competitor>" funding OR launch OR pricing [current year]`, plus their own blog/changelog/press page via WebFetch. Keep only items with a date in the last ~3 months and cite the date.
  - *Enhanced:* if Cogny isn't connected, skip this and note what connecting adds. Otherwise `mcp__cogny__mcp__cogny-brave-search__tool_brave_news` (`query: "<competitor>"`, `freshness: "pm"`) gives dated launch, funding and pricing news from the last month

### 3. Analyze their search presence
WebSearch for key terms in the market:
- Who ranks #1-3 for the main category keywords?
- What content strategy are they using? (blog, comparison pages, tools)
- Are they running Google Ads on brand/competitor terms? WebSearch can't see ads. Check the Google Ads Transparency Center (https://adstransparency.google.com, search the advertiser name) for whether they run ads and sample creatives; it doesn't show keywords, so brand-term bidding stays **unverified** unless the user runs the search themselves or Semrush is connected.

**Enhanced when connected:** If Cogny isn't connected, skip this and note what connecting adds (keyword/traffic estimates, paid keywords, Domain Rating, AI-answer share of voice).
- **Organic:** `mcp__cogny__mcp__Semrush__domain_overview` per competitor (`domain`, `database`) for keywords and traffic; `domain_organic_keywords` (`display_limit: 50`) for what they rank on. Ahrefs: `organic_keywords` and `top_pages` (`target`, `country`) show which pages earn the traffic, which tells you their content strategy.
- **Paid:** `mcp__cogny__mcp__Semrush__domain_paid_keywords` (`domain`, `database`). Flag competitors bidding on your brand and the terms everyone bids on.
- **Authority:** `mcp__cogny__mcp__Ahrefs__batch_analysis` (`targets`: all competitor domains, `country`); without Ahrefs, `mcp__cogny__mcp__cogny-ahrefs-lite__tool_domain_rating` (`target`) per domain.
- **AI answers:** `mcp__cogny__mcp__cogny-ai-visibility__tool_check_ai_visibility` for 2-3 category prompts a buyer would type ("best [category] for [segment]"), with `brand`, `domain` and `competitors`. Each check costs credits; set `engines` to limit it. If prompts were checked before, `tool_get_ai_visibility_history` (free) shows the trend.

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

Data (if connected; name the source on every number):
[If nothing is connected: "Data: not connected. Semrush/Ahrefs add traffic, paid-keyword and authority numbers; cogny-ai-visibility adds AI-answer share of voice." and omit the table.]
| Competitor | Organic keywords / traffic (Semrush or Ahrefs) | Paid keywords (Semrush) | DR (Domain Rating by Ahrefs) | AI mention rate (cogny-ai-visibility) |

Market Gaps:
1. [Gap description + opportunity]
2. [Gap description + opportunity]
3. [Gap description + opportunity]

Positioning Recommendation:
[Specific positioning advice based on gaps found]
```
