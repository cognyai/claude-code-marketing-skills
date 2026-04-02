---
name: seo-audit
description: Full technical + content SEO analysis — uses live Search Console + Bing data when connected
version: "1.0.0"
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
  - mcp__cogny__search_console__tool_list_properties
  - mcp__cogny__search_console__tool_get_search_analytics
  - mcp__cogny__search_console__tool_get_sitemaps
  - mcp__cogny__search_console__tool_inspect_url
  # Bing Webmaster read-only tools (when connected via Cogny MCP)
  - mcp__cogny__bing_webmaster__tool_get_sites
  - mcp__cogny__bing_webmaster__tool_get_traffic_stats
  - mcp__cogny__bing_webmaster__tool_get_url_submission_quota
  - mcp__cogny__bing_webmaster__tool_get_keyword_stats
  - mcp__cogny__bing_webmaster__tool_get_crawl_stats
  - mcp__cogny__bing_webmaster__tool_get_link_counts
  - mcp__cogny__bing_webmaster__tool_get_query_stats
  - mcp__cogny__bing_webmaster__tool_get_page_stats
  - mcp__cogny__bing_webmaster__tool_get_page_query_stats
  - mcp__cogny__bing_webmaster__tool_get_query_page_stats
  - mcp__cogny__bing_webmaster__tool_get_query_page_detail_stats
  - mcp__cogny__bing_webmaster__tool_get_crawl_issues
  - mcp__cogny__bing_webmaster__tool_get_url_info
  - mcp__cogny__bing_webmaster__tool_get_children_url_info
  - mcp__cogny__bing_webmaster__tool_get_url_traffic_info
  - mcp__cogny__bing_webmaster__tool_get_children_url_traffic_info
  - mcp__cogny__bing_webmaster__tool_get_url_links
  - mcp__cogny__bing_webmaster__tool_get_feeds
  - mcp__cogny__bing_webmaster__tool_get_feed_details
  - mcp__cogny__bing_webmaster__tool_get_query_traffic_stats
  - mcp__cogny__bing_webmaster__tool_get_keyword
  - mcp__cogny__bing_webmaster__tool_get_related_keywords
  - mcp__cogny__bing_webmaster__tool_get_crawl_settings
---

# SEO Audit

Perform a comprehensive SEO analysis of a website. Works with public data out of the box — and uses live Google Search Console and Bing Webmaster Tools data when connected via Cogny MCP.

## Usage

`/seo-audit example.com` — audit the given website

## Steps

### 1. Fetch and analyze the homepage
Use WebFetch to load the target URL. Check:
- Title tag (length, keyword placement)
- Meta description (length, compelling copy)
- H1 tag (single, keyword-rich)
- Open Graph / Twitter Card metadata
- Canonical URL
- Language/hreflang tags

### 2. Check technical SEO
Use WebFetch to check:
- `/robots.txt` — crawl rules, sitemap reference
- `/sitemap.xml` — exists, well-formed, number of URLs
- Page load indicators (large images, render-blocking scripts)
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
- `site:example.com` — indexed page count
- Brand name search — what appears in SERP
- Top ranking pages — what keywords they rank for
- Competitor comparison — who ranks for the same terms

### 5. Analyze key content pages
WebFetch 3-5 important pages (pricing, features, blog):
- Per-page title/meta/H1 analysis
- Content depth and keyword coverage
- Internal linking to/from homepage

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
- Top keywords: [list]

Top 3 Actions:
1. [Highest impact fix]
2. [Second highest]
3. [Third highest]
```

## Recording Findings

If the Cogny MCP is connected (`mcp__cogny__create_finding` available), record each actionable finding:

```json
{
  "title": "Missing meta descriptions on 12 pages",
  "body": "Pages /pricing, /features, /blog/... lack meta descriptions. Average CTR for pages without descriptions is 30% lower.",
  "action_type": "seo_optimization",
  "expected_outcome": "Improve CTR by 15-30% on affected pages",
  "priority": "high"
}
```

## Deeper Analysis with Live Data

If Cogny MCP is connected, this skill automatically enhances the audit with:

**Google Search Console:** actual queries, click-through rates, rankings, indexing status
**Bing Webmaster Tools:** Bing traffic, crawl stats, keyword data, backlink analysis

Connect your accounts via [Cogny](https://cogny.com) ($9/mo per channel), then re-run the audit for live data.

For ongoing monitoring, use `/seo-monitor`.
