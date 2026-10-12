---
name: landing-page-review
description: CRO review of a landing page with specific conversion recommendations
version: "1.1.1"
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
  # Optional, when Cogny MCP is connected (all read-only)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Microsoft_Clarity__get_live_insights
  - mcp__cogny__mcp__Microsoft_Clarity__get_insights_history
  - mcp__cogny__mcp__Microsoft_Clarity__get_api_quota
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Plausible__query
  - mcp__cogny__mcp__GrowthBook__list_experiments
  - mcp__cogny__mcp__GrowthBook__get_experiment_results
---

# Landing Page Review

Analyze a landing page for conversion optimization — messaging, layout, trust signals, and CTA effectiveness.

## Usage

`/landing-page-review example.com/pricing` — review the given page

## Works with

The review runs on the public page with zero accounts. Connected analytics turn opinions into measured problems.

| Job | Primary | Also answers it | No account |
|-----|---------|-----------------|------------|
| Conversion rate of this page, by device and source | GA4 (`tool_run_report`) | Plausible (`breakdown`, `query`) | — (score from heuristics) |
| Where visitors get stuck (scroll, rage/dead clicks, quickbacks) | Microsoft Clarity (`get_live_insights`) | — | — |
| What was already A/B tested here | GrowthBook (`list_experiments`, `get_experiment_results`) | — | Ask the user |

If GA4 and Plausible are both connected, show both rates side by side; they count sessions and visitors differently.

## Steps

### 1. Fetch and analyze the page
Use WebFetch to load the URL. Extract:
- Headline and subheadline text
- CTA buttons (text, placement, count)
- Value proposition clarity
- Above-the-fold content
- Page structure (sections, flow)

### 2. Evaluate messaging
Score each element:
- **Headline clarity** (1-10): Does it immediately communicate what you get?
- **Value prop specificity** (1-10): Numbers > vague claims
- **CTA strength** (1-10): Action-oriented, specific, visible
- **Social proof** (1-10): Testimonials, logos, stats
- **Urgency/scarcity** (1-10): Reason to act now

### 3. Check trust signals
Look for:
- Customer logos or testimonials
- Security badges / certifications
- Pricing transparency
- Contact information
- Privacy policy / terms links
- Case studies or results

### 4. Analyze form/CTA friction
If there's a form:
- Number of fields (fewer = higher conversion)
- Field labels and placeholder text
- Submit button text (specific > generic)
- Error handling
- Privacy reassurance near form

### 5. Mobile assessment
From the fetched HTML you can check:
- Mobile viewport meta tag (`curl -sL <url> | grep -i 'name="viewport"'`; WebFetch can't see `<head>`)
- Content readability on small screens (font sizes and line lengths in the CSS, if inline)

Touch target sizes and whether the CTA sits above the fold need a rendered page. WebFetch and curl can't measure them. Run the URL through PageSpeed Insights (https://pagespeed.web.dev, Lighthouse flags "Touch targets" / "tap targets"), or open it in a browser's device mode at 375px wide. If neither is possible, mark both "not measured (needs a browser)" instead of scoring them.

### 5a. Measure load time
Step 7 scores load speed, so measure it rather than guess:

```bash
curl -sL -o /dev/null -w "ttfb=%{time_starttransfer}s total=%{time_total}s html=%{size_download}B redirects=%{num_redirects}\n" "<url>"
# Rough page weight: HTML + the scripts, styles and images it references
curl -sL "<url>" | grep -oE '(src|href)="[^"]+\.(js|css|png|jpe?g|webp|avif|svg)[^"]*"' | head -40
```

Fetch the largest few assets with the same `-w "%{size_download}"` call and sum them. Report "TTFB X s, HTML Y KB, ~Z KB total across N requests (curl, no JS execution)". Over 1 s TTFB or ~3 MB total weight costs load-speed points. For field data (real users), use `/cwv-audit`.

### 5b. Measured behavior (enhanced when connected)
If Cogny isn't connected, skip this and note what connecting adds: real conversion rates by device and source (GA4/Plausible), where visitors get stuck (Clarity), and what was already tested (GrowthBook).

Call `mcp__cogny__list_integrations` once and skip whatever isn't connected.

- **GA4:** `mcp__cogny__mcp__Google_Analytics_4__tool_run_report` with `property_id`, `date_ranges` (last 28 days), `dimensions: ["landingPagePlusQueryString", "deviceCategory", "sessionSourceMedium"]`, `metrics: ["sessions", "engagementRate", "keyEvents", "sessionKeyEventRate"]`, filtered to the page path. Check `tool_list_conversion_events` so you know which key events count.
- **Plausible:** `mcp__cogny__mcp__Plausible__breakdown` (`site_id`, `dimension: "visit:entry_page"`, `metrics: ["visitors", "bounce_rate", "conversion_rate"]`, `date_range: "30d"`). Conversion rate needs a goal filter, e.g. `filters: [["is", "event:goal", ["Signup"]]]`.
- **Clarity:** call `mcp__cogny__mcp__Microsoft_Clarity__get_api_quota` first (10 requests/day), then `get_live_insights` with `num_of_days: 3`, `dimensions: ["URL", "Device"]`, `metrics: ["Scroll Depth", "Rage Click Count", "Dead Click Count", "Quickback Click"]`. Dead clicks on a non-link element or a scroll depth that ends above the CTA are direct evidence for a top-5 change. Heatmaps and recordings aren't in the API; tell the user where to look in Clarity.
- **GrowthBook:** `mcp__cogny__mcp__GrowthBook__list_experiments`, then `get_experiment_results` for any experiment on this page. Don't recommend a variant that already lost.

Mobile vs desktop gaps from this data take priority over heuristic scores in step 7.

### 6. Competitive comparison
WebSearch for 2-3 competitors and briefly compare:
- How do their landing pages differ?
- What trust signals do they use?
- How is their CTA different?

### 7. Report

```
Landing Page Review: [URL]
Conversion Score: X/100

Messaging: X/30
- Headline: [score] — [specific feedback]
- Value prop: [score] — [specific feedback]
- CTA: [score] — [specific feedback]

Trust: X/30
- Social proof: [score]
- Credibility signals: [score]
- Transparency: [score]

UX: X/20
- Form friction: [score]
- Mobile: [score]
- Load speed: [score] — TTFB [X]s, ~[Y] KB, [N] requests (curl)

Differentiation: X/20
- vs [Competitor 1]: [comparison]
- vs [Competitor 2]: [comparison]

Measured (if connected; name the source on every number):
[If nothing is connected: "Measured: not connected. Connecting GA4/Plausible, Clarity or GrowthBook adds real conversion rates, friction data and past test results."]
- Conversion rate: [X]% desktop / [Y]% mobile (GA4 or Plausible)
- Clarity: [N] rage clicks, [N] dead clicks on [element], avg scroll depth [X]%
- Already tested: [experiment, result] (GrowthBook)

Top 5 Changes (in priority order):
1. [Specific change with expected impact]
2. ...
3. ...
4. ...
5. ...
```
