---
name: cwv-audit
description: Core Web Vitals Reference — LCP, INP, CLS thresholds, root causes, optimization fixes, CrUX BigQuery queries, web-vitals library usage, and SEO impact
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<metric or topic>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Search Console tools (when connected via Cogny MCP)
  - mcp__cogny__search_console__tool_list_properties
  - mcp__cogny__search_console__tool_get_search_analytics
  - mcp__cogny__search_console__tool_inspect_url
  # GA4 tools
  - mcp__cogny__google_analytics_4__tool_run_report
  - mcp__cogny__google_analytics_4__tool_get_property
---

# Core Web Vitals Reference

Complete technical reference for Core Web Vitals (LCP, INP, CLS): thresholds, common causes, fixes, measurement tools, CrUX BigQuery queries, web-vitals library setup, and SEO ranking impact.

Full docs: https://cogny.com/docs/core-web-vitals

## Usage

```
/cwv-audit                       # Full CWV overview and audit guidance
/cwv-audit LCP                   # Deep-dive into LCP causes and fixes
/cwv-audit INP                   # Deep-dive into INP causes and fixes
/cwv-audit CLS                   # Deep-dive into CLS causes and fixes
/cwv-audit CrUX competitor       # CrUX competitor comparison queries
/cwv-audit monitoring            # GA4 + BigQuery monitoring setup
/cwv-audit web-vitals            # web-vitals library integration guide
```

## Instructions

You are a Core Web Vitals performance expert. Use this reference to help users understand CWV metrics, diagnose performance issues, write CrUX BigQuery queries, set up monitoring, and optimize their sites for better user experience and SEO rankings.

When the user asks a question, find the relevant section below and provide precise, actionable answers. If Search Console or GA4 MCP tools are available, use them to pull real data for the user's site.

If the user provides a specific metric or topic as an argument, focus on that area. Otherwise, provide an overview of all three vitals and their current thresholds.

---

## Overview

Core Web Vitals (CWV) are three user-centric performance metrics that Google uses as ranking signals in Search. They measure loading performance, interactivity, and visual stability. Every page is assessed at the 75th percentile of real-user field data.

| Metric | Full Name | Measures | Good | Needs Improvement | Poor |
|--------|-----------|----------|------|--------------------|------|
| **LCP** | Largest Contentful Paint | Loading performance | ≤ 2.5 s | ≤ 4.0 s | > 4.0 s |
| **INP** | Interaction to Next Paint | Interactivity | ≤ 200 ms | ≤ 500 ms | > 500 ms |
| **CLS** | Cumulative Layout Shift | Visual stability | ≤ 0.1 | ≤ 0.25 | > 0.25 |

A page "passes" Core Web Vitals when all three metrics meet the "Good" threshold at the 75th percentile.

---

## LCP — Largest Contentful Paint

### What It Measures

LCP reports the render time of the largest image, video, or text block visible within the viewport, relative to when the page first started loading.

### Thresholds

- **Good:** ≤ 2.5 seconds
- **Needs Improvement:** > 2.5 s and ≤ 4.0 s
- **Poor:** > 4.0 seconds

### LCP Candidate Elements

- `<img>` elements (including inside `<picture>`)
- `<image>` elements inside `<svg>`
- `<video>` elements (poster image or first displayed frame)
- Elements with `background-image` loaded via `url()` (not CSS gradients)
- Block-level elements containing text nodes or inline-level text children

The largest element may change as the page loads. The final entry before user interaction is the LCP value.

### Common Causes and Fixes

**1. Slow server response time (TTFB)**
- Use a CDN to serve content from edge locations
- Cache HTML at the edge (stale-while-revalidate)
- Pre-connect to required origins: `<link rel="preconnect" href="https://cdn.example.com">`
- Use 103 Early Hints

**2. Render-blocking resources**
- Inline critical CSS, defer non-critical stylesheets
- Defer or async non-critical JavaScript: `<script defer src="app.js">`
- Minimize CSS size, avoid `@import` in CSS

**3. Slow resource load times**
- Preload the LCP image: `<link rel="preload" as="image" href="hero.webp">`
- Use modern formats (WebP, AVIF) with `<picture>` fallbacks
- Set `fetchpriority="high"` on the LCP `<img>`
- Use responsive images with `srcset` and `sizes`

**4. Client-side rendering delay**
- SSR or SSG the LCP content
- Pre-render critical routes
- Reduce JavaScript bundle size

**5. Web font blocking LCP text**
- Use `font-display: swap` or `font-display: optional`
- Preload the primary font file
- Subset fonts to required characters

---

## INP — Interaction to Next Paint

### What It Measures

INP measures the latency of all click, tap, and keyboard interactions throughout the page lifecycle, and reports a single value representing the worst-case interaction. It replaced FID as a Core Web Vital in March 2024.

### Thresholds

- **Good:** ≤ 200 milliseconds
- **Needs Improvement:** > 200 ms and ≤ 500 ms
- **Poor:** > 500 milliseconds

### How It Differs from FID

| | FID | INP |
|---|-----|-----|
| **Scope** | First interaction only | All interactions |
| **What it measures** | Input delay only | Full latency: input delay + processing + presentation delay |
| **Status** | Deprecated (March 2024) | Official Core Web Vital |

### Three Phases of Interaction Latency

1. **Input delay** — time from user action to event handler start
2. **Processing time** — time spent running event handlers
3. **Presentation delay** — time from handler completion to next paint

### Common Causes and Fixes

**1. Long tasks blocking the main thread**
- Break up long tasks using `scheduler.yield()` or `setTimeout(0)`
- Use `requestIdleCallback` for non-urgent work
- Move heavy computation to Web Workers

**2. Heavy JavaScript execution**
- Code-split with dynamic `import()`
- Tree-shake unused exports at build time
- Defer non-critical scripts and third-party tags

**3. Expensive event handlers**
- Debounce or throttle rapid-fire handlers
- Avoid forced synchronous layouts in handlers
- Use `content-visibility: auto` for off-screen content

**4. Large DOM and expensive rendering**
- Virtualize long lists (react-window, @tanstack/virtual)
- Use CSS `contain: layout style paint`
- Reduce DOM depth and element count

**5. Excessive re-renders in SPA frameworks**
- Memoize components (`React.memo`, `useMemo`)
- Use `startTransition` for non-urgent state updates

---

## CLS — Cumulative Layout Shift

### What It Measures

CLS measures the sum of unexpected layout shift scores during the page lifespan. A layout shift occurs when a visible element changes position without being triggered by user interaction.

### Thresholds

- **Good:** ≤ 0.1
- **Needs Improvement:** > 0.1 and ≤ 0.25
- **Poor:** > 0.25

### Session Window Calculation

1. Shifts are grouped into session windows (max 5 seconds, 1-second gap ends a window)
2. CLS = the maximum session window score
3. Each shift score = impact fraction x distance fraction

### What Counts as a Layout Shift

- Position changes NOT triggered by user input
- CSS `transform` animations do NOT count
- Shifts within 500ms of user interaction are excluded

### Common Causes and Fixes

**1. Images/videos without dimensions**

```html
<!-- GOOD -->
<img src="hero.jpg" alt="Hero" width="800" height="400">
<!-- Or use CSS aspect-ratio -->
<style>.hero-img { aspect-ratio: 16 / 9; width: 100%; }</style>
```

**2. Dynamically injected content**

```css
.ad-slot { min-height: 250px; min-width: 300px; contain: layout style paint; }
```

**3. Web fonts causing FOIT/FOUT**

```css
@font-face {
  font-family: 'Custom Font';
  src: url('custom.woff2') format('woff2');
  font-display: optional; /* eliminates layout shift entirely */
}
```

**4. Ads/embeds without reserved space**

```css
.embed-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0; overflow: hidden;
}
.embed-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
```

**5. Late-loading banners/cookie bars**
- Use `position: fixed` or `sticky` so they overlay without shifting content

---

## Measurement Tools

### Field Data (Real Users)

| Tool | Description |
|------|-------------|
| **CrUX** | 28-day rolling data via BigQuery, API, and PageSpeed Insights |
| **Search Console CWV report** | Groups URLs by Good/Needs Improvement/Poor |
| **PageSpeed Insights (field section)** | CrUX 75th percentile values per URL/origin |
| **web-vitals library** | Measures CWV in real browsers, send to any endpoint |

### Lab Data (Synthetic)

| Tool | Description |
|------|-------------|
| **Lighthouse** | Simulated LCP and CLS (not INP) |
| **Chrome DevTools Performance panel** | Full flame charts for all three metrics |
| **WebPageTest** | Multi-step tests with filmstrips and waterfalls |

**Important:** Lab tools cannot fully measure INP. Always validate with field data.

### JavaScript APIs

```javascript
// Observe LCP
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  console.log('LCP:', entries[entries.length - 1].startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });

// Observe CLS
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) console.log('Shift:', entry.value);
  }
}).observe({ type: 'layout-shift', buffered: true });

// Observe INP (Event Timing API)
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.interactionId) console.log('Interaction:', entry.duration, 'ms');
  }
}).observe({ type: 'event', buffered: true, durationThreshold: 16 });
```

---

## web-vitals Library

### Installation

```bash
npm install web-vitals
```

### Basic Usage

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

### Send to GA4

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToGA4(metric) {
  gtag('event', metric.name, {
    value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
    event_category: 'Web Vitals',
    event_label: metric.id,
    non_interaction: true,
  });
}

onLCP(sendToGA4);
onINP(sendToGA4);
onCLS(sendToGA4);
```

### Send to Custom Endpoint

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name, value: metric.value, rating: metric.rating,
    delta: metric.delta, id: metric.id, page: window.location.pathname,
  });
  if (navigator.sendBeacon) navigator.sendBeacon('/api/vitals', body);
  else fetch('/api/vitals', { body, method: 'POST', keepalive: true });
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### Attribution Builds

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals/attribution';

onLCP((metric) => {
  console.log('LCP element:', metric.attribution.element);
  console.log('TTFB:', metric.attribution.timeToFirstByte);
  console.log('Resource load delay:', metric.attribution.resourceLoadDelay);
  console.log('Element render delay:', metric.attribution.elementRenderDelay);
});

onINP((metric) => {
  console.log('Target:', metric.attribution.interactionTarget);
  console.log('Input delay:', metric.attribution.inputDelay);
  console.log('Processing:', metric.attribution.processingDuration);
  console.log('Presentation delay:', metric.attribution.presentationDelay);
});

onCLS((metric) => {
  console.log('Largest shift target:', metric.attribution.largestShiftTarget);
  console.log('Largest shift value:', metric.attribution.largestShiftValue);
  console.log('Load state:', metric.attribution.loadState);
});
```

---

## CrUX BigQuery Queries

### CWV Scores by Origin

```sql
SELECT
  origin,
  form_factor.name AS device,
  ROUND(SAFE_DIVIDE(
    SUM(IF(lcp.start < 2500, lcp.density, 0)), SUM(lcp.density)
  ), 4) AS lcp_good_pct,
  ROUND(SAFE_DIVIDE(
    SUM(IF(inp.start < 200, inp.density, 0)), SUM(inp.density)
  ), 4) AS inp_good_pct,
  ROUND(SAFE_DIVIDE(
    SUM(IF(cls.start < 0.1, cls.density, 0)), SUM(cls.density)
  ), 4) AS cls_good_pct
FROM `chrome-ux-report.all.202501`,
  UNNEST(largest_contentful_paint.histogram.bin) AS lcp,
  UNNEST(interaction_to_next_paint.histogram.bin) AS inp,
  UNNEST(cumulative_layout_shift.histogram.bin) AS cls
WHERE origin = 'https://www.example.com'
GROUP BY origin, device
ORDER BY device
```

### CWV by Page Type (URL-level)

```sql
SELECT
  url,
  form_factor.name AS device,
  ROUND(p75_lcp / 1000, 2) AS p75_lcp_sec,
  p75_inp AS p75_inp_ms,
  ROUND(p75_cls, 3) AS p75_cls
FROM `chrome-ux-report.materialized.device_summary`
WHERE origin = 'https://www.example.com'
  AND url LIKE '%/product/%'
  AND date = (SELECT MAX(date) FROM `chrome-ux-report.materialized.device_summary`)
ORDER BY p75_lcp DESC
LIMIT 50
```

### Trending CWV Over Time

```sql
SELECT
  yyyymm,
  ROUND(SAFE_DIVIDE(
    SUM(IF(lcp.start < 2500, lcp.density, 0)), SUM(lcp.density)
  ), 4) AS lcp_good_pct,
  ROUND(SAFE_DIVIDE(
    SUM(IF(inp.start < 200, inp.density, 0)), SUM(inp.density)
  ), 4) AS inp_good_pct,
  ROUND(SAFE_DIVIDE(
    SUM(IF(cls.start < 0.1, cls.density, 0)), SUM(cls.density)
  ), 4) AS cls_good_pct
FROM `chrome-ux-report.all.*`,
  UNNEST(largest_contentful_paint.histogram.bin) AS lcp,
  UNNEST(interaction_to_next_paint.histogram.bin) AS inp,
  UNNEST(cumulative_layout_shift.histogram.bin) AS cls
WHERE origin = 'https://www.example.com'
  AND _TABLE_SUFFIX BETWEEN '202401' AND '202501'
  AND form_factor.name = 'phone'
GROUP BY yyyymm
ORDER BY yyyymm
```

### Competitor Comparison

```sql
WITH origins AS (
  SELECT origin FROM UNNEST([
    'https://www.yoursite.com',
    'https://www.competitor-a.com',
    'https://www.competitor-b.com'
  ]) AS origin
)
SELECT
  o.origin, form_factor.name AS device,
  ROUND(SAFE_DIVIDE(
    SUM(IF(lcp.start < 2500, lcp.density, 0)), SUM(lcp.density)
  ), 4) AS lcp_good_pct,
  ROUND(SAFE_DIVIDE(
    SUM(IF(inp.start < 200, inp.density, 0)), SUM(inp.density)
  ), 4) AS inp_good_pct,
  ROUND(SAFE_DIVIDE(
    SUM(IF(cls.start < 0.1, cls.density, 0)), SUM(cls.density)
  ), 4) AS cls_good_pct
FROM origins o
INNER JOIN `chrome-ux-report.all.202501` crux ON crux.origin = o.origin,
  UNNEST(largest_contentful_paint.histogram.bin) AS lcp,
  UNNEST(interaction_to_next_paint.histogram.bin) AS inp,
  UNNEST(cumulative_layout_shift.histogram.bin) AS cls
WHERE form_factor.name = 'phone'
GROUP BY o.origin, device
ORDER BY o.origin, device
```

---

## SEO Impact

### Page Experience Ranking Signal

CWV are part of Google's page experience signals alongside HTTPS, mobile-friendliness, and no intrusive interstitials.

- CWV act as a **tiebreaker** — when relevance and quality are equal, better CWV may rank higher
- CWV are **not a dominant signal** — they do not override strong content or backlinks
- Google uses **field data from CrUX** at the 75th percentile (not lab scores)
- **Mobile CWV** affect mobile rankings; **desktop CWV** affect desktop rankings

### Optimization Priority

Optimize for mobile first — it typically has the strictest constraints due to lower processing power and slower networks.

---

## Optimization Patterns

### Image Optimization

```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero" width="1200" height="600"
       fetchpriority="high" decoding="async">
</picture>

<!-- Responsive images -->
<img src="hero-800.webp" alt="Hero"
     srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
     sizes="(max-width: 600px) 400px, (max-width: 900px) 800px, 1200px"
     loading="lazy" decoding="async" width="1200" height="600">
```

**Key rule:** Never lazy-load the LCP image. Set `fetchpriority="high"` on it instead.

### Font Optimization

```html
<link rel="preload" as="font" type="font/woff2" href="/fonts/main.woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Main Font';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153;
}
```

### JavaScript Optimization

```html
<script defer src="/js/app.js"></script>
<script async src="https://analytics.example.com/tag.js"></script>
```

```javascript
// Dynamic import for code splitting
const Chart = await import('./components/Chart.js');

// Non-urgent work
requestIdleCallback(() => { initializeAnalytics(); });
```

### CSS Optimization

```css
/* Limit recalculation scope */
.card { contain: layout style paint; }

/* Skip rendering off-screen content */
.below-fold { content-visibility: auto; contain-intrinsic-size: 0 500px; }
```

### Third-Party Script Management

- Load non-critical third-party scripts after `window.load`
- Use `<link rel="preconnect">` for required third-party origins
- Use server-side tagging where possible
- Audit third-party impact with Chrome DevTools Coverage tab

---

## GA4 + BigQuery Monitoring Setup

### Send CWV to GA4

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals/attribution';

function sendToGA4(metric) {
  gtag('event', metric.name, {
    value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
    event_category: 'Web Vitals',
    event_label: metric.id,
    metric_rating: metric.rating,
    debug_target: metric.attribution?.interactionTarget
      || metric.attribution?.element
      || metric.attribution?.largestShiftTarget
      || '(not set)',
    non_interaction: true,
  });
}

onLCP(sendToGA4);
onINP(sendToGA4);
onCLS(sendToGA4);
```

### Query CWV from GA4 BigQuery Export

```sql
WITH vitals AS (
  SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) AS date,
    event_name AS metric_name,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value') AS metric_value,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'metric_rating') AS rating,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'debug_target') AS debug_target,
    device.category AS device_type
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND event_name IN ('LCP', 'INP', 'CLS')
)
SELECT
  date, metric_name, device_type,
  COUNT(*) AS samples,
  APPROX_QUANTILES(metric_value, 100)[OFFSET(75)] AS p75,
  COUNTIF(rating = 'good') / COUNT(*) AS good_pct,
  COUNTIF(rating = 'poor') / COUNT(*) AS poor_pct
FROM vitals
GROUP BY date, metric_name, device_type
ORDER BY date DESC, metric_name, device_type
```

### Identify Worst Pages

```sql
WITH page_vitals AS (
  SELECT
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') AS page,
    event_name AS metric_name,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value') AS metric_value,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'metric_rating') AS rating,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'debug_target') AS debug_target
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND event_name IN ('LCP', 'INP', 'CLS')
)
SELECT
  REGEXP_EXTRACT(page, r'^https?://[^/]+(/.*)') AS path,
  metric_name,
  COUNT(*) AS samples,
  APPROX_QUANTILES(metric_value, 100)[OFFSET(75)] AS p75,
  COUNTIF(rating = 'poor') / COUNT(*) AS poor_pct,
  APPROX_TOP_COUNT(debug_target, 3) AS top_debug_targets
FROM page_vitals
WHERE page IS NOT NULL
GROUP BY path, metric_name
HAVING samples >= 50
ORDER BY poor_pct DESC
LIMIT 50
```

## Resources

- **web.dev Core Web Vitals:** https://web.dev/articles/vitals
- **CrUX documentation:** https://developer.chrome.com/docs/crux/
- **web-vitals library:** https://github.com/GoogleChrome/web-vitals
- **CrUX BigQuery cookbook:** https://developer.chrome.com/docs/crux/bigquery/
- **PageSpeed Insights:** https://pagespeed.web.dev/
- **Full Cogny Docs:** https://cogny.com/docs/core-web-vitals
