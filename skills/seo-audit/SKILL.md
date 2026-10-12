---
name: seo-audit
description: Full technical + content SEO analysis — uses live Search Console + Bing data when connected
version: "1.1.2"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<url>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Search Console read-only tools (when connected via Cogny MCP)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Search_Console__tool_list_properties
  - mcp__cogny__mcp__Google_Search_Console__tool_get_search_analytics
  - mcp__cogny__mcp__Google_Search_Console__tool_get_sitemaps
  - mcp__cogny__mcp__Google_Search_Console__tool_inspect_url
  # Bing Webmaster read-only tools (when connected via Cogny MCP)
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_sites
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_traffic_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_submission_quota
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_keyword_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_link_counts
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_page_query_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_page_detail_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_issues
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_children_url_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_traffic_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_children_url_traffic_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_links
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_feeds
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_feed_details
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_traffic_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_keyword
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_related_keywords
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_settings
  # Provider discovery and recording findings (when connected via Cogny MCP)
  - mcp__cogny__list_integrations
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  # Keywords, competitors, backlinks (read-only, when connected)
  - mcp__cogny__mcp__Semrush__domain_overview
  - mcp__cogny__mcp__Semrush__domain_organic_keywords
  - mcp__cogny__mcp__Semrush__domain_organic_competitors
  - mcp__cogny__mcp__Semrush__backlinks_overview
  - mcp__cogny__mcp__Ahrefs__site_explorer_overview
  - mcp__cogny__mcp__Ahrefs__organic_keywords
  - mcp__cogny__mcp__Ahrefs__organic_competitors
  - mcp__cogny__mcp__Ahrefs__top_pages
  - mcp__cogny__mcp__Ahrefs__domain_rating
  - mcp__cogny__mcp__Ahrefs__refdomains
  - mcp__cogny__mcp__cogny-ahrefs-lite__tool_domain_rating
  # Live SERP and AI answer engines (read-only, metered in credits)
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_rank_check
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - mcp__cogny__mcp__cogny-ai-visibility__tool_check_ai_visibility
  - mcp__cogny__mcp__cogny-ai-visibility__tool_get_ai_visibility_history
  # Ecommerce catalog (read-only, when connected)
  - mcp__cogny__mcp__Shopify__tool_list_products
  - mcp__cogny__mcp__Shopify__tool_list_pages
  - mcp__cogny__mcp__Shopify__tool_list_collections
---

# SEO Audit

Perform a comprehensive SEO analysis of a website. Works with public data out of the box — and uses live Google Search Console and Bing Webmaster Tools data when connected via Cogny MCP.

## Usage

`/seo-audit example.com` — audit the given website

## Works with

Every step runs on public data (WebFetch/WebSearch) with zero accounts. Connected providers replace estimates with measured data.

| Job | Primary | Also answers it | No account |
|-----|---------|-----------------|------------|
| Queries, CTR, indexing | Google Search Console | Bing Webmaster Tools (Bing + Copilot) | WebSearch with `allowed_domains` |
| Keywords and competitors | Semrush | Ahrefs | WebSearch |
| Backlinks / authority | Ahrefs | Semrush, cogny-ahrefs-lite (DR only) | — |
| Live rank for target terms | cogny-brave-search | — | WebSearch |
| AI answer engines | cogny-ai-visibility | — | — |
| Product/collection pages | Shopify | — | sitemap.xml |

If several answer the same job, report them side by side and name the provider on every number. If a tool you expect is missing, call `mcp__cogny__refresh_mcp_discovery` once. New tools only load after the client reconnects, so use the step's fallback for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Don't loop on refresh.

## Steps

### 0. Cogny check and providers
If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this once and run steps 1-6 on public data:

```
SEO Audit can add live search data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Search Console and Bing Webmaster Tools
   (Semrush, Ahrefs or Shopify optional).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: run the full audit on public data (curl, WebFetch, WebSearch).
```

Skip each connected-only row with one line, e.g. "Search Console: not connected (connecting adds real queries, CTR and index status)".

If Cogny is connected, call `mcp__cogny__list_integrations`. Note which rows above are available and flag any integration whose `health_status` is not healthy. Then make one cheap read per integration (GSC `tool_list_properties`, Bing `tool_get_sites`): `health_status` misses revoked tokens, so a 401, Forbidden or scope error is 🔴 "reconnect <integration>", with no retry. Cogny-native servers (`cogny-brave-search`, `cogny-ai-visibility`, `cogny-ahrefs-lite`) don't appear in `list_integrations`; treat them as available if their tools load. A connected integration that fails gets "reconnect <integration> in Cogny"; one that isn't connected gets "connect <integration> in Cogny".

Save downloaded files in the session scratchpad directory if your environment gives you one (else `D=$(mktemp -d)`), not `/tmp`. The commands below write to `$D`.

### 1. Fetch and analyze the homepage
WebFetch summarises the page body and can't see `<head>`, so read head tags from the raw HTML with Bash:

```bash
curl -sL -A "Mozilla/5.0" https://example.com/ -o "$D/seo-home.html"
grep -oiE '<title[^>]*>[^<]*</title>|<meta[^>]+(name|property)="(description|robots|viewport|og:[a-z:]+|twitter:[a-z:]+)"[^>]*>|<link[^>]+rel="(canonical|alternate)"[^>]*>|<html[^>]+lang="[^"]*"' "$D/seo-home.html"
grep -o 'application/ld+json' "$D/seo-home.html" | wc -l   # JSON-LD blocks (inspect them for step 3)
```

Count JSON-LD with `grep -o … | wc -l`, not `grep -c`: minified pages put every block on one line, and `grep -c` counts lines.

Use WebFetch for the visible content (H1, copy). Check:
- Title tag (length, keyword placement)
- Meta description (length, compelling copy)
- H1 tag (single, keyword-rich)
- Open Graph / Twitter Card metadata
- Canonical URL
- Language/hreflang tags

### 2. Check technical SEO
Use curl, not WebFetch: WebFetch summarises, so it miscounts sitemap URLs and can't see `<head>` scripts.

```bash
curl -sL -A "Mozilla/5.0" https://example.com/robots.txt              # crawl rules, Sitemap: lines
curl -sL -A "Mozilla/5.0" https://example.com/sitemap.xml -o "$D/sitemap.xml"
grep -o '<loc>' "$D/sitemap.xml" | wc -l                              # URL count
grep -q '<sitemapindex' "$D/sitemap.xml" && grep -oE '<loc>[^<]+' "$D/sitemap.xml" | sed 's/<loc>//'   # an index: fetch each child and sum
perl -0ne 'print $1 if /<head[\s>](.*?)<\/head>/is' "$D/seo-home.html" | grep -oiE '<script[^>]*>'   # head scripts (no async/defer = render-blocking)
```

Use the sitemap URL from robots.txt if it isn't `/sitemap.xml`. Check:
- `/robots.txt` — crawl rules, sitemap reference
- Sitemap — exists, well-formed, number of URLs
- Page load indicators (large images, render-blocking scripts in `<head>`)
- Mobile viewport meta tag
- HTTPS enforcement

### 3. Analyze content structure
From the homepage content:
- Word count (target: 300+ for ranking pages)
- Header hierarchy (H1 → H2 → H3)
- Internal link count and structure
- Image alt text coverage
- Schema markup (JSON-LD)

### 4. Check search presence
Use WebSearch to find:
- Indexed pages, **only when neither GSC nor Bing is connected**: WebSearch ignores the `site:` operator, so pass the domain in its `allowed_domains` parameter (e.g. query "example.com", `allowed_domains: ["example.com"]`) and report how many distinct pages come back as a rough sample, not an index count. When connected, use the `tool_inspect_url` sample and Bing crawl stats below instead
- Brand name search — what appears in SERP
- Top ranking pages — what keywords they rank for
- Competitor comparison — who ranks for the same terms

**Enhanced when connected** (run what is available; each replaces a guess above):

| Provider | Call | What it adds |
|----------|------|--------------|
| Search Console | `mcp__cogny__mcp__Google_Search_Console__tool_get_search_analytics` (`site_url`, `start_date`, `end_date`, `dimensions: ["query"]` then `["page"]`) and `tool_inspect_url` on the 3-5 key pages | Real queries, CTR, position, index status |
| Bing Webmaster | `mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_stats`, `tool_get_crawl_issues`, `tool_get_link_counts` (all take `site_url`). `tool_get_link_counts` can come back empty; fall back to the `InLinks` field of `tool_get_crawl_stats`. If the query tools aren't loaded, use `tool_get_traffic_stats` and mark ⚠ "needs reconnect" | Bing/Copilot queries, crawl errors, inbound links. `tool_get_traffic_stats` returns one row per day: add up clicks and impressions per period (e.g. last 28 days vs the 28 before) and report the totals, never the raw rows. It has no reliable position, so write Bing position as n/a unless `tool_get_query_stats` gives one |
| Semrush | `mcp__cogny__mcp__Semrush__domain_overview`, `domain_organic_keywords`, `domain_organic_competitors` (`domain`, `database` = market country code, e.g. `se`) | Keyword footprint, traffic estimate, organic competitors |
| Ahrefs | `mcp__cogny__mcp__Ahrefs__site_explorer_overview`, `organic_keywords`, `top_pages`, `organic_competitors` (`target`, `country`) | Same jobs as Semrush; plus `domain_rating`, `refdomains` for authority |
| cogny-ahrefs-lite | `mcp__cogny__mcp__cogny-ahrefs-lite__tool_domain_rating` (`target`) | DR when no Ahrefs account. Always write "Domain Rating by Ahrefs" next to the number |
| cogny-brave-search | `mcp__cogny__mcp__cogny-brave-search__tool_brave_rank_check` (`domain`, `query`, `country`, `max_results: 20`) for 3-5 target terms. Larger `max_results` returns very large payloads; not in the top 20 is "20+" | Live position from an independent index (1 credit per call) |
| cogny-ai-visibility | `mcp__cogny__mcp__cogny-ai-visibility__tool_check_ai_visibility` (`prompt` written as a buyer asks, `brand`, `domain`, `competitors`) for 2-3 prompts | Whether ChatGPT, Claude, Gemini and Perplexity mention or cite the site. Metered: limit `engines` to save credits |

Semrush and Ahrefs estimate traffic differently; never add them together.

### 5. Analyze key content pages
Fetch 3-5 important pages (pricing, features), plus the blog index **and at least 2 individual posts**: canonicals, `article` schema and dates live on the posts, not the index. Read head tags with the Step 1 curl/grep on each; WebFetch only for the body:
- Per-page title/meta/H1 analysis
- Content depth and keyword coverage
- Internal linking to/from homepage

**Ecommerce, enhanced when Shopify is connected:** pull `mcp__cogny__mcp__Shopify__tool_list_products` and `tool_list_collections` (`first: 50`) and check, across the whole catalog rather than a sample: missing or duplicate product titles/descriptions, collections with no description, draft products still linked from the sitemap. Report counts.

### 6. Report findings

Present as a scored audit:

```
SEO Audit: example.com
Score: X/100

Technical: X/25
- [PASS/FAIL] HTTPS
- [PASS/FAIL] Robots.txt
- [PASS/FAIL] Sitemap
- [PASS/FAIL] Mobile viewport
- [PASS/FAIL] Canonical URLs

On-Page: X/25
- [PASS/FAIL] Title tags
- [PASS/FAIL] Meta descriptions
- [PASS/FAIL] H1 structure
- [PASS/FAIL] Image alt text
- [PASS/FAIL] Schema markup

Content: X/25
- [PASS/FAIL] Word count
- [PASS/FAIL] Header hierarchy
- [PASS/FAIL] Internal linking

Search Presence: X/25
- Indexed pages: N
- Brand SERP: [description]
- Top keywords: [list] (source: GSC / Semrush / Ahrefs / WebSearch)
- Authority: [DR N, "Domain Rating by Ahrefs"] (if available)
- AI answer engines: mentioned in X of Y engine answers (if checked)

Top 3 Actions:
1. [Highest impact fix]
2. [Second highest]
3. [Third highest]
```

## Deeper Analysis with Live Data

If Cogny MCP is connected, this skill automatically enhances the audit with:

**Google Search Console:** actual queries, click-through rates, rankings, indexing status
**Bing Webmaster Tools:** Bing traffic, crawl stats, keyword data, backlink analysis
**Semrush / Ahrefs:** keyword footprint, organic competitors, backlinks
**cogny-brave-search / cogny-ai-visibility:** live rank checks and AI answer-engine presence

Bing writes (`tool_submit_url`, `tool_submit_content`) and GSC `tool_submit_sitemap` are not pre-approved: the skill asks first.

Connect your accounts via [Cogny](https://cogny.com) ($9/mo per channel), then re-run the audit for live data.

For ongoing monitoring, use `/seo-monitor`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
Example finding: title "Missing meta descriptions on 12 pages", body listing the URLs and the evidence, expected outcome "Improve CTR by 15-30% on affected pages", type `seo_optimization`, priority high.
