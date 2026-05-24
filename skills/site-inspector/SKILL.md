---
name: site-inspector
description: "Comprehensive website audit: security headers, performance, SEO, accessibility, privacy, tech stack -- 121 scored checks with A+ through F grading"
version: "1.0.0"
author: Bright Interaction
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

# Site Inspector

Full website audit covering 121 scored checks across 6 categories plus technology stack detection. Produces letter grades (A+ through F) per category and an overall weighted score. Based on the Site Inspector Chrome extension by Bright Interaction.

## Usage

```
/site-inspector example.com           -- full audit
/site-inspector example.com security  -- security category only
/site-inspector example.com seo       -- SEO category only
```

## Instructions

You are a website auditor running the Site Inspector methodology. Given a URL, perform a comprehensive audit across 6 scored categories: Security, Performance, SEO, Accessibility, Privacy, and Tech Stack (info only). Then derive Quick Wins from the highest-impact failures.

Normalize the input URL: add `https://` if missing, strip trailing slashes. Use this normalized URL (`$URL`) and extract the domain (`$DOMAIN`) for all checks.

If the user specifies a single category, still collect all raw data (headers, DOM, PageSpeed) but only report that category's detailed results.

---

## Step 1: Collect raw data (run all three in parallel)

### 1a. HTTP headers and supplementary files

Run these curl commands via Bash:

```bash
# Full response headers (follow redirects, request compression)
curl -sI -L -H "Accept-Encoding: gzip, br" -H "User-Agent: Mozilla/5.0 (compatible; SiteInspector/1.0)" "$URL"

# Check supplementary files (just status codes + headers)
curl -sI "$URL/.well-known/security.txt"
curl -sI "$URL/robots.txt"
curl -sI "$URL/sitemap.xml"
curl -sI "$URL/favicon.ico"
curl -sI "$URL/llms.txt"
curl -sI "$URL/llms-full.txt"

# Cookie dump
curl -s -L -c - -H "User-Agent: Mozilla/5.0 (compatible; SiteInspector/1.0)" "$URL" -o /dev/null

# HTTP/2 check
curl -sI --http2 -H "User-Agent: Mozilla/5.0 (compatible; SiteInspector/1.0)" "$URL" 2>&1 | head -1
```

Record ALL response headers including duplicates. Note the final URL after redirects (for HTTPS check).

### 1b. Full page DOM via WebFetch

WebFetch the URL with this prompt:

> Analyze this page and return a structured report with ALL of the following. Do not summarize or skip items:
>
> **META:** Every `<meta>` tag (name, property, content). Include charset, viewport, description, robots, og:*, twitter:*.
> **TITLE:** The `<title>` tag content and character count.
> **HEADINGS:** Every heading tag (h1-h6) with its text content. Count of each level. Flag empty headings. Flag hierarchy skips (e.g. h1 then h3 with no h2).
> **LINKS:** Count of internal links (same domain), external links, empty links (no text), hash-only links (#), anchor links pointing to IDs. List any broken anchor targets.
> **IMAGES:** Total count, count missing alt, count with generic alt ("image", "photo", "logo", "banner", "icon"), count missing width/height, count with loading="lazy", image formats used (jpg, png, webp, avif, svg).
> **SCRIPTS:** Every `<script>` tag -- src URL, async/defer attributes, integrity attribute (SRI), whether it loads from a third-party domain. Flag render-blocking scripts (no async/defer, in `<head>`).
> **STYLES:** Every `<link rel="stylesheet">` -- href, integrity attribute. Every `<style>` block. Any @font-face declarations with font-display values.
> **FORMS:** Every `<input>`, `<select>`, `<textarea>` -- does it have an associated `<label>` or aria-label? Any password/email inputs missing autocomplete?
> **BUTTONS:** Any `<button>` elements without text content or aria-label.
> **ACCESSIBILITY:** Landmarks present (`<main>`, `<nav>`, `<header>`, `<footer>`, or ARIA role equivalents). Skip link present? Any elements with tabindex > 0? Any focusable elements inside aria-hidden containers? Are focus outlines removed via CSS (`outline: none` or `outline: 0` without :focus-visible replacement)?
> **STRUCTURED DATA:** All `<script type="application/ld+json">` blocks -- full content. Schema types found. For LocalBusiness: has address? For Article: has datePublished, author? For FAQPage: visible FAQ section on page? For SoftwareApplication: has aggregateRating? Any visible star ratings without schema markup?
> **COOKIES/CONSENT:** Any consent banner elements (OneTrust, CookieBot, cookie-banner, consent classes/IDs, CookieProof, Quantcast, TrustArc, Iubenda, Complianz, GDPR, cookie-notice)? Any tracking scripts (gtag, fbq, _linkedin, _tiktok, clarity, hotjar, plausible, umami, matomo, posthog, mixpanel, segment, amplitude)?
> **CONTENT:** Word count of visible text. Text-to-HTML ratio estimate. Any deprecated HTML elements (`<blink>`, `<marquee>`, `<center>`, `<font>`, `<big>`, `<strike>`)? iframe count? Plaintext email addresses exposed?
> **SOCIAL:** Open Graph tags completeness (title, description, image, type, url). Twitter Card tags (card, title, description, image). og:image dimensions if available.
> **TECH SIGNALS:** Any framework indicators: `__NEXT_DATA__`, `_next/`, `__NUXT__`, `__svelte`, `astro-island`, `_astro/`, `ng-version`, `___gatsby`, `__remix`, `data-reactroot`, `__VUE__`. Any CMS indicators: `wp-content`, `Shopify.`, `wix.com`, `squarespace`, `webflow`, `.ghost`. Any library indicators: `jQuery`, `gsap`, `three.js`, `alpine`, `htmx`, `stimulus`, `turbo`. CSS frameworks: class patterns for tailwind, bootstrap, bulma, material-ui, chakra. Build tool indicators: `webpackJsonp`, `@vite`, `parcel`. Google Fonts link tags (count font families).
> **HREFLANG:** All hreflang link tags -- languages, URLs, x-default present? Self-referencing? Host matches canonical?
> **RESOURCE HINTS:** Any `<link rel="preconnect">`, `<link rel="dns-prefetch">`, `<link rel="preload">` tags.
> **VIDEOS:** Any `<video>` elements -- do they have captions/subtitles tracks?
> **TABLES:** Any `<table>` elements -- do they have `<th>` or scope attributes?
> **PAGINATION:** Any `<link rel="prev">` or `<link rel="next">`?
> **AMP:** Any `<link rel="amphtml">`?
> **APPLE:** Any apple-touch-icon link tag?

### 1c. PageSpeed Insights API

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$URL&category=performance&strategy=mobile" | python3 -c "
import json, sys
d = json.load(sys.stdin)
lhr = d.get('lighthouseResult', {})
audits = lhr.get('audits', {})
cats = lhr.get('categories', {})

# Performance score
perf = cats.get('performance', {}).get('score', 'N/A')
print(f'PERF_SCORE: {perf}')

# Metrics
metrics = audits.get('metrics', {}).get('details', {}).get('items', [{}])[0]
for k in ['firstContentfulPaint','largestContentfulPaint','totalBlockingTime','cumulativeLayoutShift','speedIndex','interactive','observedTimeToFirstByte','observedDomContentLoaded','observedLoad']:
    print(f'{k}: {metrics.get(k, \"N/A\")}')

# Total weight
weight = audits.get('total-byte-weight', {}).get('numericValue', 'N/A')
print(f'totalByteWeight: {weight}')

# Request count
diag = audits.get('diagnostics', {}).get('details', {}).get('items', [{}])[0]
print(f'numRequests: {diag.get(\"numRequests\", \"N/A\")}')

# Render-blocking
rb = audits.get('render-blocking-resources', {}).get('details', {}).get('items', [])
print(f'renderBlockingCount: {len(rb)}')

# Image optimization
imgAudit = audits.get('modern-image-formats', {}).get('details', {}).get('items', [])
print(f'unoptimizedImages: {len(imgAudit)}')

# Uses long tasks as INP proxy
longTasks = audits.get('long-tasks', {}).get('details', {}).get('items', [])
print(f'longTaskCount: {len(longTasks)}')
"
```

If PageSpeed fails (rate limit, timeout), note "PageSpeed data unavailable" and score Performance checks as INFO instead of PASS/FAIL.

---

## Step 2: Supplementary data (run in parallel)

### 2a. Search index check

WebSearch: `site:$DOMAIN`

Note the approximate number of indexed pages from search results.

### 2b. Robots.txt content

If robots.txt returned 200 in Step 1, WebFetch `$URL/robots.txt` with prompt:
> Return the full robots.txt content. List all User-agent blocks, Disallow rules, Sitemap references. Note if any AI training bots are blocked (GPTBot, ClaudeBot, Google-Extended, PerplexityBot, Bytespider, CCBot, anthropic-ai, Amazonbot, FacebookBot, Applebot-Extended, meta-externalagent).

### 2c. Sitemap.xml check

If sitemap.xml returned 200, WebFetch `$URL/sitemap.xml` with prompt:
> Is this a valid XML sitemap? How many URLs does it contain? Is it a sitemap index pointing to other sitemaps?

---

## Step 3: Score every check

For each check, record: **PASS** (full points), **PARTIAL** (half points, rounded down), **FAIL** (0 points), or **INFO** (0 points, not scored). Calculate `earned / possible` per category.

---

### SECURITY (21 checks, 37 max points)

**Header Checks:**

| # | Check | Wt | PASS when | PARTIAL when |
|---|-------|----|-----------|--------------|
| 1 | HTTPS enforced | 2 | Final URL is `https://` | -- |
| 2 | Strict-Transport-Security | 2 | HSTS header present with `max-age >= 31536000` | Header present with shorter max-age |
| 3 | Content-Security-Policy | 3 | CSP or CSP-Report-Only header present | -- |
| 4 | X-Content-Type-Options | 1 | Header value is `nosniff` | -- |
| 5 | X-Frame-Options | 2 | Header is `DENY` or `SAMEORIGIN` | -- |
| 6 | X-XSS-Protection | 1 | Header present | -- |
| 7 | Referrer-Policy | 1 | Header present and not `unsafe-url` | -- |
| 8 | Permissions-Policy | 1 | `Permissions-Policy` or `Feature-Policy` header present | -- |
| 9 | No Server version leak | 1 | `Server` header absent or contains no version number (e.g. `nginx` ok, `nginx/1.21.3` fail) | -- |
| 10 | No X-Powered-By | 1 | `X-Powered-By` header absent | -- |
| 11 | Cross-Origin-Opener-Policy | 1 | COOP header present | -- |
| 12 | Cross-Origin-Resource-Policy | 1 | CORP header present | -- |
| 13 | Cross-Origin-Embedder-Policy | 1 | COEP header present | -- |
| 14 | X-Permitted-Cross-Domain-Policies | 1 | Header present | -- |
| 15 | No duplicate security headers | 2 | Each security header appears exactly once in raw response | -- |

**CSP Quality (scored separately from CSP presence):**

| # | Check | Wt | PASS (Strong) when | PARTIAL (Moderate) when |
|---|-------|----|-------------------|------------------------|
| 16 | CSP quality | 3 | **Strong (3 pts):** No `unsafe-inline`, no `unsafe-eval`, no wildcard `*` sources, has `frame-ancestors`, has `base-uri`, has `object-src` restricted | **Moderate (2 pts):** Has CSP but uses `unsafe-inline` OR `unsafe-eval`. **Weak (1 pt):** Has CSP with wildcards or multiple weaknesses |

If no CSP header exists, this check scores 0.

**Resource & Transport Checks:**

| # | Check | Wt | PASS when | PARTIAL when |
|---|-------|----|-----------|--------------|
| 17 | Subresource Integrity (SRI) | 2 | All third-party `<script>` and `<link rel="stylesheet">` have `integrity` attribute. If no third-party resources, auto-pass | 50%+ have integrity |
| 18 | No mixed content | 2 | No `http://` resource URLs found in page HTML (on an HTTPS page) | -- |
| 19 | Compression | 1 | `Content-Encoding` header contains `gzip`, `br`, or `compress` | -- |
| 20 | Cache headers | 1 | At least one of `Cache-Control`, `ETag`, or `Expires` header present | -- |
| 21 | security.txt | 1 | `/.well-known/security.txt` returns HTTP 200 | `/security.txt` returns 200 (non-standard location) |

**SRI exemptions:** Exempt Google Fonts (`fonts.googleapis.com`) and Google Tag Manager (`googletagmanager.com`) from SRI checks -- these serve dynamic content per browser UA, making integrity hashes impossible.

---

### PERFORMANCE (17 checks, 31 max points)

All timing values come from the PageSpeed Insights API response. If PageSpeed is unavailable, mark all Performance checks as INFO.

**Timing Metrics:**

| # | Check | Wt | PASS | PARTIAL | FAIL |
|---|-------|----|------|---------|------|
| 1 | TTFB (Time to First Byte) | 2 | < 500ms | < 800ms | >= 800ms |
| 2 | FCP (First Contentful Paint) | 2 | < 1800ms | < 3000ms | >= 3000ms |
| 3 | DOM Content Loaded | 2 | < 2500ms | < 4000ms | >= 4000ms |
| 4 | Page Load Complete | 2 | < 4000ms | < 7000ms | >= 7000ms |

**Core Web Vitals:**

| # | Check | Wt | PASS (Good) | PARTIAL (Needs Work) | FAIL (Poor) |
|---|-------|----|-------------|---------------------|-------------|
| 5 | LCP (Largest Contentful Paint) | 3 | <= 2500ms | <= 4000ms | > 4000ms |
| 6 | CLS (Cumulative Layout Shift) | 3 | <= 0.1 | <= 0.25 | > 0.25 |
| 7 | Long Tasks (INP proxy) | 2 | 0 long tasks | <= 3 long tasks | > 3 long tasks |

**Page Weight & Requests:**

| # | Check | Wt | PASS | PARTIAL | FAIL |
|---|-------|----|------|---------|------|
| 8 | Total page weight | 2 | < 1 MB | < 3 MB | >= 3 MB |
| 9 | Request count | 1 | < 50 requests | < 100 requests | >= 100 requests |

**Resource Optimization:**

| # | Check | Wt | PASS | PARTIAL | FAIL |
|---|-------|----|------|---------|------|
| 10 | Render-blocking scripts | 2 | 0 render-blocking resources | <= 2 | > 2 |
| 11 | Image optimization | 2 | All images use modern formats (WebP/AVIF) or all SVG | Some modern formats | No modern formats |
| 12 | Below-fold lazy loading | 2 | >= 80% of non-hero images have `loading="lazy"` | >= 40% | < 40% |
| 13 | Image dimensions | 1 | All `<img>` have width + height attributes | -- | Missing dimensions |
| 14 | Font-display | 2 | All @font-face rules have `font-display` set | Some have it | None |
| 15 | Google Fonts families | 1 | <= 3 font families loaded | -- | > 3 families |
| 16 | HTTP/2+ protocol | 1 | Response uses HTTP/2 or HTTP/3 | -- | HTTP/1.1 |

**Lighthouse Score:**

| # | Check | Wt | PASS | PARTIAL | FAIL |
|---|-------|----|------|---------|------|
| 17 | Lighthouse performance score | 2 | >= 90 | >= 50 | < 50 |

---

### SEO (51+ checks, 81 max points)

#### On-Page SEO (12 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 1 | Title tag present | 2 | `<title>` exists with non-empty content |
| 2 | Title length 30-60 chars | 1 | Character count between 30 and 60 |
| 3 | Title not truncated | 1 | Title <= 60 characters (won't be cut off in SERP) |
| 4 | Title starts with content | 1 | Title does not begin with `|`, `-`, `:`, or whitespace |
| 5 | Meta description present | 2 | `<meta name="description">` exists with non-empty content |
| 6 | Description length 120-160 | 1 | Character count between 120 and 160 |
| 7 | Description has CTA | 1 | Contains action words: learn, get, discover, try, start, find, explore, read, download, free, buy, compare, see, check, request, book, sign up, join, save, unlock, improve, boost, grow, create. Also Swedish: las, fa, upptack, testa, borja, hitta, utforska, ladda ner, gratis, kop, jamfor, se, kolla, boka. Also German: erfahren, entdecken, testen, starten, finden, kostenlos, kaufen, vergleichen, buchen |
| 8 | H1 tag present | 2 | At least one `<h1>` on the page |
| 9 | Single H1 | 1 | Exactly one `<h1>` (not zero, not multiple) |
| 10 | H2 subheadings present | 1 | At least one `<h2>` for content structure |
| 11 | Heading hierarchy correct | 2 | No skipped levels (e.g. H1 then H3 without H2) |
| 12 | No empty headings | 1 | No heading tags with empty or whitespace-only content |

#### Images & Alt Text (3 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 13 | Images have alt text | 2 | All `<img>` tags have `alt` attribute (empty `alt=""` for decorative is OK) |
| 14 | Images have dimensions | 1 | All `<img>` have width and height attributes |
| 15 | Descriptive alt text | 1 | No images with generic alt text ("image", "photo", "logo", "banner", "icon", "picture", "img", "untitled") |

#### Content Quality (2 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 16 | Content length | 1 | Visible text >= 300 words |
| 17 | Text-to-HTML ratio | 1 | Text comprises >= 10% of total page size |

#### Links (5 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 18 | Internal links present | 1 | At least 1 internal link (same domain) |
| 19 | External outbound links | 1 | At least 2 external links to other domains |
| 20 | No empty links | 1 | No `<a>` tags without visible text or aria-label |
| 21 | Minimal hash-only links | 1 | <= 2 links with `href="#"` only |
| 22 | No broken anchor links | 1 | All `href="#section"` links have matching `id="section"` elements on page |

#### URL Structure (4 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 23 | URL length | 1 | Path portion < 75 characters |
| 24 | URL uses hyphens | 1 | No underscores `_` in URL path (hyphens `-` are correct) |
| 25 | URL is lowercase | 1 | No uppercase letters in URL path |
| 26 | URL depth | 1 | <= 4 levels deep (count `/` separators in path) |

#### Technical SEO Basics (6 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 27 | Canonical URL present | 2 | `<link rel="canonical">` exists |
| 28 | Canonical matches URL | 1 | Canonical href matches the current page URL |
| 29 | Language declared | 1 | `<html lang="...">` attribute present with valid language code |
| 30 | Viewport meta tag | 2 | `<meta name="viewport">` present |
| 31 | Charset declared | 1 | `<meta charset="UTF-8">` or Content-Type header specifies charset |
| 32 | HTML5 DOCTYPE | 1 | `<!DOCTYPE html>` present |

#### Technical SEO Metadata (6 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 33 | Favicon | 1 | `<link rel="icon">` or `/favicon.ico` returns 200 |
| 34 | Apple Touch Icon | 1 | `<link rel="apple-touch-icon">` present |
| 35 | robots.txt valid | 2 | Returns 200, contains `User-agent` and `Disallow` directives |
| 36 | XML sitemap exists | 2 | sitemap.xml returns 200 with valid XML content |
| 37 | No duplicate meta tags | 2 | No meta tag name/property appears more than once |
| 38 | Resource hints | 1 | At least one `preconnect`, `dns-prefetch`, or `preload` link |

#### Technical SEO Advanced (8 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 39 | Not noindexed | 3 | Page does not have `<meta name="robots" content="noindex">` (FAIL is a warning, not necessarily wrong -- mark INFO if intentional) |
| 40 | No deprecated HTML | 1 | No `<blink>`, `<marquee>`, `<center>`, `<font>`, `<big>`, `<strike>` elements |
| 41 | Minimal iframes | 1 | <= 3 `<iframe>` elements on page |
| 42 | Hreflang tags present | 1 | Hreflang link tags exist (for multi-language sites). INFO/skip if single-language site |
| 43 | Hreflang self-referencing | 2 | Each page's hreflang set includes a self-referencing entry. Skip if no hreflang |
| 44 | Hreflang x-default | 1 | `hreflang="x-default"` fallback present. Skip if no hreflang |
| 45 | Hreflang host matches canonical | 2 | All hreflang URLs use the same hostname as the canonical. Skip if no hreflang |
| 46 | llms.txt (AI discoverability) | 1 | `/llms.txt` or `/llms-full.txt` returns HTTP 200 |

#### Structured Data (9 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 47 | JSON-LD structured data | 2 | At least one `<script type="application/ld+json">` block present |
| 48 | LocalBusiness: has address | 2 | If LocalBusiness or subtype schema found, it contains `address` field. Skip if no LocalBusiness |
| 49 | LocalBusiness: no invalid fields | 1 | No invalid properties like `serviceType` or `provider` on LocalBusiness. Skip if no LocalBusiness |
| 50 | SoftwareApplication: has rating | 1 | If SoftwareApplication schema found, has `aggregateRating` or `review`. Skip if no SoftwareApplication |
| 51 | Article: has datePublished | 1 | If Article/BlogPosting/NewsArticle schema found, has `datePublished`. Skip if no Article |
| 52 | Article: has author | 1 | If Article schema found, has `author`. Skip if no Article |
| 53 | FAQ: has visible content | 2 | If FAQPage schema found, page has a visible FAQ section. Skip if no FAQPage |
| 54 | Visible ratings have schema | 2 | If visible star ratings on page, matching AggregateRating or Review schema exists. Skip if no visible ratings |

For schema checks that don't apply (schema type not present), skip the check entirely -- do not count it toward the possible points.

#### Social / Open Graph (6 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 55 | Open Graph tags present | 1 | At least `og:title` meta tag found |
| 56 | OG completeness | 1 | All 5 essential OG tags present: `og:title`, `og:description`, `og:image`, `og:type`, `og:url` |
| 57 | OG image present | 1 | `og:image` meta tag has a value |
| 58 | OG image recommended size | 1 | og:image is 1200x630px (check via `og:image:width`/`og:image:height` if available, otherwise INFO) |
| 59 | Twitter Card present | 1 | `twitter:card` meta tag found |
| 60 | Twitter image present | 1 | `twitter:image` meta tag has a value |

#### Other (1 check)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 61 | No plaintext emails | 1 | No unobfuscated email addresses visible in page HTML |

#### SEO Informational (not scored)

Note these but do not score them:
- **App page detected:** If page matches 3+ of: dashboard/app URL path, < 200 words, no title, no canonical, 3+ session cookies. If detected, make SEO title/description/OG/structured-data checks INFO instead of FAIL
- **Nofollow present:** Page has `<meta name="robots" content="nofollow">`
- **Pagination:** `<link rel="prev">` or `<link rel="next">` found
- **AMP version:** `<link rel="amphtml">` found
- **Trailing slash consistency:** INFO note about trailing slash behavior

---

### ACCESSIBILITY (21 checks, 47 max points)

#### Structure & Navigation (6 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 1 | Main landmark | 2 | `<main>` element or `role="main"` present |
| 2 | Navigation landmark | 2 | `<nav>` element or `role="navigation"` present |
| 3 | Banner landmark | 1 | `<header>` element or `role="banner"` present |
| 4 | Contentinfo landmark | 1 | `<footer>` element or `role="contentinfo"` present |
| 5 | Skip navigation link | 2 | Link with text like "Skip to content/main" early in DOM targeting `#main`, `#content`, or similar |
| 6 | Page language | 2 | `<html lang="...">` with a valid BCP 47 language code |

#### Page Essentials (2 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 7 | Page title | 2 | `<title>` tag present with text content |
| 8 | Page has H1 | 2 | At least one `<h1>` heading on the page |

#### Headings (2 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 9 | Heading order | 2 | Sequential heading levels without skips (H1 -> H2 -> H3) |
| 10 | No empty headings | 1 | No heading elements with empty or whitespace-only content |

#### Images & Media (2 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 11 | Images have alt text | 3 | All `<img>` elements have `alt` attribute. Decorative images may use `alt=""` |
| 12 | Videos have captions | 2 | All `<video>` elements have `<track kind="captions">` or `<track kind="subtitles">`. Skip if no videos |

#### Forms & Interactivity (4 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 13 | Form inputs have labels | 3 | Every `<input>`, `<select>`, `<textarea>` has an associated `<label>`, `aria-label`, or `aria-labelledby`. Exempt `type="hidden"` and `type="submit"` |
| 14 | Buttons have labels | 2 | All `<button>` elements have visible text, `aria-label`, or `aria-labelledby` |
| 15 | Links have labels | 2 | All `<a>` elements have visible text, `aria-label`, or contain an image with alt text |
| 16 | Autocomplete on sensitive inputs | 1 | Password and email `<input>` elements have `autocomplete` attribute |

#### Color & Contrast (1 check)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 17 | Color contrast (WCAG AA) | 3 | Text meets 4.5:1 contrast ratio (3:1 for large text >= 18px or >= 14px bold). Note: full contrast analysis requires browser rendering. Check for obvious issues: light gray text on white, low-contrast class patterns. If unable to determine, report as INFO with note |

#### Keyboard & Focus (3 checks)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 18 | No positive tabindex | 2 | No elements have `tabindex` value greater than 0 |
| 19 | Focus indicators visible | 2 | No global `outline: none` or `outline: 0` CSS without `:focus-visible` replacement. PARTIAL if `*:focus { outline: none }` found but `:focus-visible` styles also present |
| 20 | No focusable in aria-hidden | 2 | No focusable elements (`<a>`, `<button>`, `<input>`, elements with `tabindex`) inside `aria-hidden="true"` containers |

#### Tables (1 check)

| # | Check | Wt | PASS when |
|---|-------|----|-----------|
| 21 | Table headers | 2 | All data `<table>` elements have `<th>` elements or `scope` attributes on header cells. Skip if no tables |

---

### PRIVACY (11 checks, 26 max points)

| # | Check | Wt | PASS when | PARTIAL when |
|---|-------|----|-----------|--------------|
| 1 | Consent banner present | 3 | Cookie consent mechanism detected (OneTrust, CookieBot, CookieProof, Quantcast, TrustArc, Iubenda, Complianz, cookie-banner/consent class/ID, GDPR notice, custom consent UI) | -- |
| 2 | Cookie count reasonable | 1 | <= 10 cookies set by server (from curl cookie dump) | -- |
| 3 | Session cookies security | 2 | No session/auth cookies (names containing `session`, `sess`, `auth`, `token`, `sid`, `csrf`) visible to JavaScript (i.e. they should be HttpOnly). Since curl can only see server-set cookies, check cookie flags in the Set-Cookie headers | -- |
| 4 | Third-party domains | 2 | <= 10 external domains loaded | <= 20 external domains (1 pt) |
| 5 | Tracker count | 2 | <= 2 confirmed tracking scripts (GA/GTM, Meta Pixel, LinkedIn, TikTok, Hotjar, Clarity, etc.) detected in page HTML. Only count script-based detections, not cookie-only evidence | <= 5 trackers (1 pt) |
| 6 | No pre-consent tracking | 3 | No tracking/analytics cookies set in initial response (before any consent interaction). Check: `_ga`, `_gid`, `_fbp`, `_fbc`, `_gcl_*`, `_uetvid`, `MUID`, `li_*`, `ph_*` cookies in curl dump | -- |
| 7 | Privacy policy link | 2 | Link containing "privacy" (or Swedish "integritet", or German "datenschutz") in href or anchor text, pointing to same domain | -- |
| 8 | Terms / cookie policy link | 1 | Link containing "terms", "cookie" (or Swedish "villkor", "kakor", or German "nutzungsbedingungen", "cookie-richtlinie") in href or anchor text | -- |
| 9 | DNT/GPC awareness | 1 | `Tk` response header present (Do Not Track acknowledgment) | -- |
| 10 | AI training bots blocked | 2 | robots.txt blocks >= 3 AI training bots: `GPTBot`, `ClaudeBot`, `Google-Extended`, `PerplexityBot`, `Bytespider`, `CCBot`, `anthropic-ai`, `Amazonbot`, `FacebookBot`, `Applebot-Extended`, `meta-externalagent` | 1-2 bots blocked (1 pt) |
| 11 | Cookie expiration reasonable | 1 | No cookies with expiration > 2 years. Check `Max-Age` and `Expires` in Set-Cookie headers | -- |

---

### TECH STACK DETECTION (info only, no score)

Detect technologies from HTTP headers and DOM content. Report what is found; do not score.

**Detection signals:**

| Category | Technology | Signal |
|----------|-----------|--------|
| **Hosting** | Cloudflare | `cf-ray` header |
| | Netlify | `x-nf-request-id` header or `netlify` in headers |
| | Vercel | `x-vercel-id` header |
| | AWS CloudFront | `x-amz-cf-id` header or `via` containing `cloudfront` |
| | Azure | `x-azure-ref` header |
| | Google Cloud | `via` containing `google` or `x-cloud-trace-context` |
| | Fly.io | `fly-request-id` header |
| | Render | `x-render-origin-server` header |
| | Railway | `x-railway-` headers |
| | GitHub Pages | `x-github-request-id` header or `server: GitHub.com` |
| **Server** | Nginx | `server: nginx` |
| | Apache | `server: Apache` |
| | Caddy | `server: Caddy` |
| | LiteSpeed | `server: LiteSpeed` |
| **CMS** | WordPress | `wp-content` or `wp-includes` in HTML |
| | Shopify | `Shopify.` in JS or `cdn.shopify.com` |
| | Webflow | `webflow.com` in HTML/JS |
| | Squarespace | `squarespace` in HTML/JS |
| | Wix | `wix.com` in HTML/JS |
| | Drupal | `Drupal.settings` or `drupal.js` |
| | Ghost | `ghost/` in HTML or `X-Ghost-` headers |
| | Joomla | `/media/jui/` or `Joomla!` |
| **Framework** | Next.js | `__NEXT_DATA__` or `/_next/` paths |
| | Nuxt.js | `__NUXT__` or `/_nuxt/` paths |
| | React | `data-reactroot` or `__REACT_DEVTOOLS_GLOBAL_HOOK__` |
| | Vue.js | `__VUE__` or `vue.js`/`vue.min.js` |
| | Svelte/SvelteKit | `__svelte` or `_app/` SvelteKit paths |
| | Angular | `ng-version` attribute |
| | Astro | `astro-island` elements or `_astro/` paths |
| | Gatsby | `___gatsby` or `___GatsbyContext` |
| | Remix | `__remix` or `remix` in paths |
| **CSS** | Tailwind CSS | `tailwindcss` CDN or characteristic utility classes |
| | Bootstrap | `bootstrap` in class names or CDN |
| | Bulma | `bulma` CDN or `is-` class prefix patterns |
| | Material UI | `MuiButton` or `mui` class patterns |
| | Chakra UI | `chakra-` class prefix |
| **Build** | Vite | `@vite` or `vite` in script paths |
| | Webpack | `webpackJsonp` or `webpack` in paths |
| | esbuild | `esbuild` in paths |
| | Parcel | `parcel` in paths |
| **Analytics** | Google Analytics 4 | `gtag` function or `G-` measurement ID |
| | Google Tag Manager | `googletagmanager.com/gtm.js` |
| | Meta Pixel | `fbq(` function or `facebook.com/tr` |
| | Hotjar | `hotjar.com` or `hj(` function |
| | Microsoft Clarity | `clarity.ms` |
| | LinkedIn Insight | `snap.licdn.com` |
| | TikTok Pixel | `analytics.tiktok.com` |
| | Plausible | `plausible.io` |
| | Umami | `umami` analytics script |
| | Matomo | `matomo` or `piwik` |
| | PostHog | `posthog` or `ph_` patterns |
| | Mixpanel | `mixpanel.com` |
| | Segment | `segment.com/analytics` or `analytics.js` |
| | Amplitude | `amplitude.com` |
| **Libraries** | jQuery | `jQuery` or `jquery.min.js` |
| | GSAP | `gsap` or `greensock` |
| | Three.js | `three.js` or `three.min.js` |
| | Alpine.js | `alpine` or `x-data` attributes |
| | HTMX | `htmx.org` or `hx-` attributes |
| | Stimulus | `stimulus` or `data-controller` |
| | Turbo | `@hotwired/turbo` or `turbo-frame` |
| | Lodash | `lodash` |

Report detected technologies as a table. Only report technologies for which positive signals were found.

---

### QUICK WINS (derived from all categories)

After scoring all categories, identify the top 5-10 highest-impact fixes:

1. Sort all FAIL and PARTIAL checks by weight (points lost) descending
2. For ties, prioritize by ease of fix: header additions (easy) > meta tag additions (easy) > content changes (medium) > architectural changes (hard)
3. For each quick win, include: check name, category, points lost, and a one-line actionable fix

---

## Step 4: Calculate grades

### Per-category grade

For each scored category:
1. Sum points earned / points possible = percentage
2. Exclude skipped checks (e.g. hreflang on single-language sites, schema checks for absent types) from both earned and possible
3. Map percentage to letter grade:

```
A+ = 97-100%    B+ = 87-89%    C+ = 77-79%    D+ = 67-69%
A  = 93-96%     B  = 83-86%    C  = 73-76%    D  = 63-66%
A- = 90-92%     B- = 80-82%    C- = 70-72%    D- = 60-62%
                                                F  = below 60%
```

### Overall score

Weighted average of category percentages:
- Security: 25%
- Performance: 25%
- SEO: 20%
- Accessibility: 15%
- Privacy: 15%

Apply the same letter grade scale to the overall percentage.

---

## Step 5: Output the report

Present results using this template:

```
# Site Inspector Report: $URL

**Scanned:** [date]
**Overall: [X]% ([grade])**

## Grades

| Category       | Score  | Grade |
|---------------|--------|-------|
| Security       | X/Y (Z%) | [grade] |
| Performance    | X/Y (Z%) | [grade] |
| SEO            | X/Y (Z%) | [grade] |
| Accessibility  | X/Y (Z%) | [grade] |
| Privacy        | X/Y (Z%) | [grade] |

---

## Security ([grade])

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | HTTPS | PASS/FAIL | ... |
| 2 | HSTS | PASS/FAIL | ... |
| ... | ... | ... | ... |

[Repeat table for each scored category]

---

## Tech Stack

| Category | Detected |
|----------|----------|
| Hosting | [value or "Not detected"] |
| Server | [value] |
| CMS | [value] |
| Framework | [value] |
| CSS Framework | [value] |
| Build Tool | [value] |
| Analytics | [value] |
| Libraries | [value] |

---

## Quick Wins

1. **[Check name]** ([category]) -- [X] pts -- [one-line fix]
2. **[Check name]** ([category]) -- [X] pts -- [one-line fix]
3. ...

---

*Audited with Site Inspector for Claude Code*
*Based on Site Inspector by Bright Interaction (https://brightinteraction.com)*
```

After presenting the report, ask: "Want me to save this report to a file?"

If yes, write to `site-inspector-report-[domain]-[YYYY-MM-DD].md` in the current directory.

---

## Limitations

- **Performance data** comes from Google PageSpeed Insights API (free tier, no key). May rate-limit on repeated use. If unavailable, Performance checks become INFO.
- **Cookies:** curl only captures server-set cookies, not JavaScript-set cookies. Privacy cookie counts may undercount.
- **Color contrast:** Full WCAG contrast analysis requires browser rendering. This skill checks for obvious CSS anti-patterns but cannot compute exact contrast ratios.
- **WebFetch processing:** Very large pages may be truncated. DOM analysis is based on WebFetch's processed output, not raw HTML. Some checks are best-effort approximations.
- **SRI exemptions:** Google Fonts and Google Tag Manager are exempt from SRI checks because they serve dynamic content per browser, making integrity hashes impossible.
- **App page detection:** Authenticated app pages (dashboards, admin panels) trigger adjusted scoring -- SEO content checks become informational rather than failures.
