---
name: seo-monitor
description: Monitor SEO rankings, queries, and indexing via Search Console MCP
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [search-console]
user-invocable: true
argument-hint: "[overview|queries|pages|indexing]"
allowed-tools:
  - mcp__cogny__search_console__*
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# SEO Monitor

Monitor your website's search performance using live Google Search Console data via Cogny's MCP server.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

Verify Search Console MCP tools are available. If not:

```
This skill requires Cogny's Search Console MCP server.
Sign up at https://cogny.com/agent and connect your Search Console property.
```

## Usage

`/seo-monitor` — full overview
`/seo-monitor queries` — top queries and ranking changes
`/seo-monitor pages` — top pages performance
`/seo-monitor indexing` — indexing status and issues

## Steps

### 1. Query Performance (last 28 days)
Pull top queries by clicks:
- Query text, clicks, impressions, CTR, average position
- Compare vs previous 28 days: which queries are rising/falling?

### 2. Page Performance
Top pages by clicks:
- URL, clicks, impressions, CTR, avg position
- Identify pages losing traffic (position drops)
- Find pages with high impressions but low CTR (title/description optimization opportunities)

### 3. Ranking Changes
Compare current vs previous period:
- New queries appearing (opportunities)
- Queries losing position (threats)
- Queries near page 1 (positions 11-20 — quick wins)

### 4. Indexing Status
Check:
- Total indexed pages
- Pages with indexing errors
- Pages excluded from indexing
- New pages discovered

### 5. Report

```
SEO Monitor: [Site]
Period: [dates]

Search Performance:
Clicks: [X] ([+/-]% vs prev)
Impressions: [X] ([+/-]%)
Avg CTR: [X]% ([+/-])
Avg Position: [X] ([+/-])

Top 5 Queries:
1. [query] — pos [X], [X] clicks
...

Rising Queries (opportunity):
- [query]: position improved [X] → [Y]
...

Falling Queries (threat):
- [query]: position dropped [X] → [Y]
...

Quick Wins (position 11-20, high impressions):
- [query] at pos [X] with [Y] impressions — optimize [page URL]
...

Top 3 Actions:
1. ...
2. ...
3. ...
```
