---
name: website-migration-audit
description: Compare a production site against a staging/redesign version — SEO parity, content integrity, missing pages, and launch readiness
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<production-url> <staging-url>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # BigQuery for Search Console data (when connected via Cogny MCP)
  - mcp__cogny__list_datasets
  - mcp__cogny__list_tables
  - mcp__cogny__inspect_schema
  - mcp__cogny__execute_bigquery_sql
  # Search Console tools (when connected via Cogny MCP)
  - mcp__cogny__search_console__tool_list_properties
  - mcp__cogny__search_console__tool_get_search_analytics
  - mcp__cogny__search_console__tool_get_sitemaps
  - mcp__cogny__search_console__tool_inspect_url
  # Bing Webmaster read-only tools (when connected via Cogny MCP)
  - mcp__cogny__bing_webmaster__tool_get_sites
  - mcp__cogny__bing_webmaster__tool_get_traffic_stats
  - mcp__cogny__bing_webmaster__tool_get_crawl_stats
  - mcp__cogny__bing_webmaster__tool_get_crawl_issues
  - mcp__cogny__bing_webmaster__tool_get_url_info
  - mcp__cogny__bing_webmaster__tool_get_page_stats
---

# Website Migration Audit

Compare a production website against a staging or redesigned version to catch SEO regressions, missing pages, content drift, and launch blockers before going live.

Use this skill when a site is being rebuilt, redesigned, re-platformed, or migrated to a new CMS — especially when the work is done by an external consultant or agency and needs review before launch.

## Usage

```
/website-migration-audit example.com staging.example.com
/website-migration-audit example.com staging.example.com --deep
```

## Instructions

You are a website migration QA specialist. Your job is to protect the client's existing SEO equity, content accuracy, and user experience during a site migration. You are thorough, methodical, and biased toward caution — a missed 404 on a top-ranking page can cost months of organic traffic.

When both URLs are provided, run the full audit below. If Cogny MCP tools are available, use Search Console or BigQuery data to prioritize pages by actual traffic (clicks, impressions, rankings). Without MCP, fall back to sitemap crawling and public data.

---

## Steps

### 1. Identify top SEO pages on the production site

**With Cogny MCP (preferred):** Query Search Console or BigQuery for the top 25 pages by clicks over the last 3 months. Record clicks, impressions, CTR, and average position for each.

```sql
-- Example: BigQuery Search Console export
SELECT
  url,
  SUM(clicks) AS total_clicks,
  SUM(impressions) AS total_impressions,
  ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) AS ctr_pct,
  ROUND(SAFE_DIVIDE(SUM(sum_position), SUM(impressions)), 1) AS avg_position
FROM `searchconsole.searchdata_url_impression`
WHERE data_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  AND search_type = 'WEB'
GROUP BY url
ORDER BY total_clicks DESC
LIMIT 25
```

**Without MCP:** Fetch `/sitemap.xml` from the production site and extract all URLs. Use WebSearch `site:example.com` to estimate which pages have the most visibility.

Classify pages into priority tiers:
- **Critical** (top 5 by clicks) — any issue is a launch blocker
- **High** (top 6-15) — issues should be fixed before launch
- **Medium** (top 16-25) — issues should be fixed within first week
- **Standard** (all remaining) — verify they exist, spot-check content

### 2. URL parity check

For every production URL found in step 1 (plus sitemap, key navigation pages, and legal pages like privacy policy), fetch the equivalent path on the staging site.

Record the HTTP status:
- **200** — page exists, proceed to content comparison
- **301/302** — note the redirect target, verify it's intentional
- **404** — **flag as blocker** if Critical/High tier, warning if Medium/Standard
- **500** — flag as blocker regardless of tier

Present results as a table:

```
URL Parity Check: [production] vs [staging]

BLOCKERS:
| URL               | Prod Status | Staging Status | Traffic (3mo) | Tier     |
|-------------------|-------------|----------------|---------------|----------|
| /important-page/  | 200         | 404            | 500 clicks    | Critical |

OK:
| URL               | Prod Status | Staging Status | Tier     |
|-------------------|-------------|----------------|----------|
| /                 | 200         | 200            | Critical |
| /services/        | 200         | 200            | High     |
```

Also check:
- Trailing slash consistency (if production uses trailing slashes, staging must too)
- Case sensitivity (URLs should match case exactly)
- Query parameter handling

### 3. SEO element comparison

For all Critical and High tier pages, fetch both production and staging versions and compare:

**Title tags:**
- Must match exactly (or be intentionally improved)
- Flag any missing titles, duplicates, or significant changes

**H1 tags:**
- Each page should have exactly one H1
- Content should match or be intentionally improved
- Flag missing H1s or multiple H1s

**Meta descriptions:**
- Compare content, flag if removed
- Note if production is missing them too (common — not a regression)

**Canonical tags:**
- Each staging page should have `<link rel="canonical">` pointing to the production URL
- Flag self-referencing canonicals pointing to the staging domain

**Meta robots:**
- Staging should have `noindex` to prevent Google from indexing it
- Verify this will be removed before launch

**Heading hierarchy:**
- Compare H1 > H2 > H3 structure
- Flag skipped heading levels (e.g., H1 directly to H4)

Present as a comparison table per page.

### 4. Content integrity check

For all Critical and High tier pages, compare:

**Text content:**
- Body text should match or be intentionally updated
- Flag missing sections, truncated content, or placeholder text
- Watch for lorem ipsum, "TODO", or template artifacts

**Contact information:**
- Phone numbers must match exactly
- Email addresses must match exactly
- Physical address must match exactly
- Business hours must match exactly

**Pricing and offers:**
- Any pricing displayed must match production exactly
- Package names, descriptions, and prices
- Discount percentages, tax deduction info

**Images:**
- All production images should be present on staging
- Flag broken images (src returning 404)
- Check that alt text is preserved

**CTAs and forms:**
- All call-to-action buttons present
- Button text matches
- Links point to correct destinations
- Forms have all required fields

### 5. Navigation and site structure

**Header:**
- Logo links to homepage
- Menu items match production
- Dropdown/submenu structure preserved
- Mobile menu works (check viewport meta tag)

**Footer:**
- All footer links present and working
- Contact information matches
- Legal links present (privacy policy, terms)
- Social media links correct

**Internal linking:**
- Cross-links between pages preserved
- No links pointing to staging domain (should use relative paths or production domain)
- No broken internal links

### 6. Technical checks

**Sitemap:**
- `/sitemap.xml` exists and is valid
- Contains all indexable pages
- No 404 URLs listed
- URLs use production domain (not staging)

**Robots.txt:**
- `/robots.txt` exists
- Does not block important resources
- References sitemap

**HTTPS:**
- All pages load over HTTPS
- No mixed content (HTTP resources on HTTPS page)

**Performance (spot check):**
- Staging is not significantly slower than production
- No large unoptimized images
- No render-blocking resources missing

**Language and locale:**
- `<html lang="...">` attribute matches production
- Character encoding correct (Swedish characters, accents, etc.)

### 7. Functional testing

- [ ] Contact form submits successfully
- [ ] Cookie consent banner appears and functions
- [ ] Phone numbers are clickable (`tel:` links) on mobile
- [ ] External links open correctly
- [ ] 404 page exists and is helpful

### 8. Generate the audit report

Present findings as a structured report:

```
Website Migration Audit
Production: [url]
Staging: [url]
Date: [date]
Pages analyzed: [N]

LAUNCH READINESS: [BLOCKED / READY WITH WARNINGS / READY]

━━━ BLOCKERS (must fix before launch) ━━━

[B1] Missing page: /important-page/
     Traffic: 500 clicks/3mo, avg position 4.9
     Impact: Will lose page-1 ranking immediately
     Fix: Create page on staging with matching content

[B2] ...

━━━ WARNINGS (should fix before launch) ━━━

[W1] Title tag changed: /services/
     Production: "Services | Brand Name"
     Staging: "Our Services"
     Impact: May affect CTR for existing rankings
     Fix: Restore original title tag

[W2] ...

━━━ SEO SCORECARD ━━━

| Check                    | Status | Details                          |
|--------------------------|--------|----------------------------------|
| URL parity               | X/Y OK | [N] pages missing                |
| Title tags               | X/Y OK | [N] changed                      |
| H1 tags                  | X/Y OK | [N] missing or changed           |
| Meta descriptions        | X/Y OK | [N] removed                      |
| Canonical tags           | X/Y OK | [N] missing or wrong             |
| Contact info             | PASS   | All matching                     |
| Pricing                  | PASS   | All matching                     |
| Images                   | X/Y OK | [N] broken                       |
| Internal links           | X/Y OK | [N] broken                       |
| Sitemap                  | PASS   | [N] URLs                         |
| Robots.txt               | PASS   |                                  |
| HTTPS                    | PASS   |                                  |

━━━ PRE-LAUNCH CHECKLIST ━━━

Before switching DNS / going live:
- [ ] All blockers resolved
- [ ] Remove noindex tags from staging
- [ ] Update canonical URLs to production domain
- [ ] Verify sitemap references production URLs
- [ ] Submit updated sitemap to Google Search Console
- [ ] Set up 301 redirects for any changed URLs
- [ ] Verify analytics tracking (GA4 / GTM) is installed
- [ ] Take baseline screenshots of top pages in Google Cache

━━━ POST-LAUNCH MONITORING (first 4 weeks) ━━━

Week 1:
- Monitor Search Console for crawl errors daily
- Check indexed page count hasn't dropped
- Verify top pages still appear in search results
- Monitor 404 errors in server logs

Week 2-4:
- Compare click/impression data week-over-week
- Check average position for key pages
- Verify no new crawl issues
- Monitor Core Web Vitals in Search Console
```

## Deeper Analysis with Live Data

If Cogny MCP is connected, this skill automatically enhances the audit with:

**Google Search Console / BigQuery:** actual traffic data to prioritize pages by real-world SEO impact — clicks, impressions, CTR, and average position.

**Bing Webmaster Tools:** Bing-specific crawl issues, indexing status, and traffic data.

Connect your accounts via [Cogny](https://cogny.com) ($9/mo per channel), then re-run the audit for traffic-weighted prioritization.

For ongoing monitoring after launch, use `/seo-monitor`.
