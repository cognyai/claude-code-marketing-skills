---
name: seo-monitor
description: Monitor SEO rankings, queries, and indexing via Search Console and/or Bing Webmaster Tools MCP
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [search-console, bing-webmaster]
user-invocable: true
argument-hint: "[overview|queries|pages|indexing]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  # Search Console (read-only)
  - mcp__cogny__mcp__Google_Search_Console__tool_list_properties
  - mcp__cogny__mcp__Google_Search_Console__tool_get_search_analytics
  - mcp__cogny__mcp__Google_Search_Console__tool_get_sitemaps
  - mcp__cogny__mcp__Google_Search_Console__tool_inspect_url
  # Bing Webmaster Tools (read-only)
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_sites
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_traffic_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_issues
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_info
  # Live rank + AI answer-engine trend (read-only)
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_rank_check
  - mcp__cogny__mcp__cogny-ai-visibility__tool_get_ai_visibility_history
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
  - Bash
---

# SEO Monitor

Monitor your website's search performance using live Google Search Console data via Cogny's MCP server.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | What differs |
|-----|---------|-----------------|--------------|
| Queries, pages, CTR, position | Google Search Console | Bing Webmaster Tools | Bing data covers Bing and Copilot; positions and CTR are not comparable across engines, so report them side by side |
| Indexing / crawl health | GSC (`tool_inspect_url`, `tool_get_sitemaps`) | Bing (`tool_get_crawl_issues`, `tool_get_crawl_stats`) | GSC inspects one URL at a time; Bing lists issues site-wide |
| Spot-check a rank today | cogny-brave-search | — | Independent index, 1 credit per call |
| AI answer-engine trend | cogny-ai-visibility history | — | Only prompts already checked (e.g. by `/seo-audit`); reading history is free |

## Prerequisites Check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
SEO Monitor needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Search Console and/or Bing Webmaster Tools.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: run /seo-audit <url> for a one-time audit on public data.
```

Otherwise call `mcp__cogny__list_integrations`. You need **Google Search Console or Bing Webmaster Tools** (either is enough; both is better). Flag any whose `health_status` is not healthy, then make one cheap read per integration (GSC `tool_list_properties`, Bing `tool_get_sites`): a 401, Forbidden or scope error is 🔴 "reconnect <integration>", with no retry. `health_status` misses revoked tokens. Cogny-native servers (`cogny-brave-search`, `cogny-ai-visibility`) don't appear in `list_integrations`; treat them as available if their tools load.

If a Bing tool listed here is missing (older connections cache a short list without `tool_get_query_stats` / `tool_get_page_stats`), call `mcp__cogny__refresh_mcp_discovery` once. New tools only load after the client reconnects, so for this run use `tool_get_traffic_stats` (site-level daily clicks and impressions; use its average position only if the rows include one, otherwise report Bing position as n/a) instead, mark Bing ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh.

If neither is connected, say "connect Google Search Console or Bing Webmaster Tools in Cogny" and stop.

## Usage

`/seo-monitor` — full overview
`/seo-monitor queries` — top queries and ranking changes
`/seo-monitor pages` — top pages performance
`/seo-monitor indexing` — indexing status and issues

## Steps

**GSC lag rule:** Search Console data lags about 3 days. Every GSC window ends **3 days ago** (e.g. current = the 28 days ending today − 3, previous = the 28 days before that), or the latest days read as a false drop. Keep `row_limit` at 500 or less; bigger query pulls get very large.

### 1. Query Performance (last 28 days)
- **GSC:** `mcp__cogny__mcp__Google_Search_Console__tool_get_search_analytics` with `site_url`, `start_date`, `end_date`, `dimensions: ["query"]`; run again for the previous 28 days.
- **Bing:** `mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_stats` (`site_url`). It returns weekly rows; split them into the two periods yourself. If it isn't loaded, fall back to `tool_get_traffic_stats` (`site_url`) for site-level totals only and mark Bing queries ⚠ "needs reconnect". It returns one row per day over a long history: keep only the rows whose date falls in the current and previous windows (same dates as GSC), sum clicks and impressions per window, and report the two totals, never the raw rows. Bing position: the rows' average if present, otherwise n/a.

Pull top queries by clicks:
- Query text, clicks, impressions, CTR, average position
- Compare vs previous 28 days: which queries are rising/falling?

### 2. Page Performance
GSC: same call with `dimensions: ["page"]`. Bing: `tool_get_page_stats` (`site_url`); if it isn't loaded, report Bing pages as ⚠ "needs reconnect" (the `tool_get_traffic_stats` totals from step 1 still stand).

Top pages by clicks:
- URL, clicks, impressions, CTR, avg position
- Identify pages losing traffic (position drops)
- Find pages with high impressions but low CTR (title/description optimization opportunities)

### 3. Ranking Changes
Compare current vs previous period:
- New queries appearing (opportunities)
- Queries losing position (threats)
- Queries near page 1 (positions 11-20 — quick wins)
- **Optional spot-check:** for the 3-5 biggest movers, `mcp__cogny__mcp__cogny-brave-search__tool_brave_rank_check` (`domain`, `query`, `country`) to confirm today's position outside Google
- **Optional AI trend:** `mcp__cogny__mcp__cogny-ai-visibility__tool_get_ai_visibility_history` (`brand`, `days: 90`). Report mention rate per engine only if history exists; don't start new paid checks here

### 4. Indexing Status
GSC: `tool_get_sitemaps` for which sitemaps are submitted, when they were last read, and their errors/warnings. Its `indexed` count comes back 0 because the API doesn't fill it, so **don't report "submitted vs indexed"** from it. Do compare each sitemap's `submitted` count with the live sitemap's URL count:

```bash
curl -sL -A "Mozilla/5.0" "<sitemap path from tool_get_sitemaps>" | grep -o '<loc>' | wc -l
```

For a sitemap index, count the `<loc>` entries of each child sitemap and sum. A gap of more than ~10% means Google last read an older version (check `lastDownloaded`) or the sitemap changed since; flag it 🟡 and suggest resubmitting (a write, so ask first). Instead sample `tool_inspect_url` on 10–20 URLs (new pages, falling pages, and a few from each sitemap) and report "N/M sampled URLs indexed" with each failing URL's `coverageState`. Bing: `tool_get_crawl_issues` and `tool_get_crawl_stats`.

Check:
- Indexed share of the sampled URLs (GSC) and Bing's crawled/indexed counts
- Pages with indexing errors
- Pages excluded from indexing
- New pages discovered

### 5. Report

```
SEO Monitor: [Site]
Period: [dates]

Search Performance (Google Search Console | Bing Webmaster, side by side):
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

Writes (`Google_Search_Console__tool_submit_sitemap`, `Bing_Webmaster_Tools__tool_submit_url`) are never pre-approved. Ask first, e.g. "Submit the 4 new URLs to Bing?"

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
