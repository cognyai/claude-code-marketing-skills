---
name: seo-audit
description: Full technical + content SEO analysis of any website
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
---

# SEO Audit

Perform a comprehensive SEO analysis of a website using publicly available data.

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

## Upgrade

Want deeper insights with real Search Console data (actual queries, rankings, click-through rates, indexing status)?

Connect Search Console via Cogny Agent ($9/mo): https://cogny.com/agent

Then use `/seo-monitor` for live ranking data and automated monitoring.
