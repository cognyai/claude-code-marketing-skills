---
name: ga4-audit
description: Google Analytics 4 configuration and data-quality audit — key events, data streams, custom dimensions, attribution, retention, PII, Ads link, BigQuery export
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-analytics-4]
user-invocable: true
argument-hint: "[full|config|events|data-quality]"
allowed-tools:
  - mcp__cogny__google_analytics_4__tool_list_account_summaries
  - mcp__cogny__google_analytics_4__tool_get_property
  - mcp__cogny__google_analytics_4__tool_list_data_streams
  - mcp__cogny__google_analytics_4__tool_list_conversion_events
  - mcp__cogny__google_analytics_4__tool_list_custom_dimensions
  - mcp__cogny__google_analytics_4__tool_list_custom_metrics
  - mcp__cogny__google_analytics_4__tool_get_metadata
  - mcp__cogny__google_analytics_4__tool_run_report
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# GA4 Audit

A one-time audit of a Google Analytics 4 property — configuration *and* data quality.
GA4 collects data the moment the tag fires, but most properties quietly leak trust:
unmarked key events, PII in parameters, no Ads link, `(not set)` traffic. This skill
finds those before they corrupt a quarter of reporting.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

If `mcp__cogny__google_analytics_4__tool_get_property` is not available:

```
This skill requires Cogny's Google Analytics 4 MCP server.

1. Sign up at https://cogny.com/agent
2. Connect your GA4 property
3. Add Cogny to your .mcp.json (see the repo README)
4. Restart Claude Code
```

Stop here if the tools are missing.

## Usage

`/ga4-audit` — full property audit
`/ga4-audit config` — property + stream + link settings only
`/ga4-audit events` — events, key events, custom dimensions only
`/ga4-audit data-quality` — `(not set)`, PII, anomaly checks only

## Steps

### 1. Property discovery

```
tool_list_account_summaries
tool_get_property        (property_id)
```

Record: time zone, currency, industry category, **data retention setting**, and
property type. Flag data retention left at the 2-month default — it should be 14
months so year-over-year exploration works.

### 2. Data streams

```
tool_list_data_streams   (property_id)
```

Flag:
- Multiple web streams for one site (splits data, double-counts users)
- Enhanced measurement off, or measuring events the team doesn't actually want
- Missing iOS/Android streams for a business that has apps

### 3. Key events (conversions)

```
tool_list_conversion_events   (property_id)
```

Flag:
- **No key events configured** — Ads bidding and GA4 reporting both lose their anchor
- Key events marked on noisy automatic events (`page_view`, `scroll`) — inflates the
  conversion count and misleads everyone
- Obvious business goals *not* marked as key events (e.g. `generate_lead`, `purchase`,
  `sign_up`)
- More than ~10–15 key events — when everything is a conversion, nothing is

### 4. Custom dimensions & metrics

```
tool_list_custom_dimensions   (property_id)
tool_list_custom_metrics      (property_id)
tool_get_metadata             (property_id)
```

Flag:
- Event parameters collected by the tag but **never registered** as custom dimensions
  (the data is invisible in reports) — compare `get_metadata` against what the streams
  send
- Approaching the 50 event-scoped / 25 user-scoped dimension limits
- High-cardinality registered dimensions (timestamps, IDs) — they cause `(other)` rows

### 5. Traffic & data-quality report

```
tool_run_report   (property_id, last 30 days,
  dimensions: sessionDefaultChannelGroup, sessionSource, sessionMedium,
  metrics: sessions, conversions, totalUsers)
```

Flag:
- A large `Unassigned` or `(not set)` share — broken UTMs or tagging gaps
  (point the user to `/utm-builder`)
- A `Direct` share above ~40% — usually lost referrer data or missing tags
- Self-referrals (your own domain as a source) — needs an unwanted-referral filter
- Internal traffic visible in reports — no internal-traffic filter applied

### 6. PII & policy check

Scan event and parameter names from `get_metadata` for anything that could carry
personal data — `email`, `phone`, `user_email`, full names, raw addresses in
parameters or in the page path / query string.

🔴 PII in GA4 violates Google's policy and risks the property being deleted. Flag it
as critical and name the exact parameter.

### 7. Integrations

Flag:
- **No Google Ads link** — conversions can't flow to Ads for bidding (check with the
  user; the link isn't always API-visible)
- No BigQuery export — recommend it for any property that wants raw-data analysis
  (`/ga4-bigquery-schema` covers the schema)
- Search Console not linked

### 8. Score and report

```
GA4 Audit — [Property Name]
GA4 Health Score: X/100

Score breakdown:
  Configuration ...... X/20   (streams, retention, time zone)
  Key events ......... X/25   (the reporting + bidding anchor)
  Custom dimensions .. X/15
  Data quality ....... X/25   ((not set), Direct, self-referrals)
  Compliance ......... X/15   (PII, internal traffic)

🔴 Critical   — PII collected, no key events, retention at 2 months
🟡 Important  — unregistered dimensions, high (not set), no Ads link
🟢 Optimization — BigQuery export, enhanced measurement tuning

Top 3 Actions:
1. [Highest impact]
2. ...
3. ...
```

### 9. Record findings

```json
{
  "title": "Email address captured in GA4 'page_location' — policy violation",
  "body": "The checkout-success URL includes ?email=… and GA4 stores it in page_location and page_path. Google policy prohibits PII in Analytics and can delete the property. Strip the parameter at the tag, or redact it before the event fires.",
  "action_type": "data_quality",
  "expected_outcome": "PII removed from collection; property compliant",
  "estimated_impact_usd": 0,
  "priority": "critical"
}
```

Action types: `tracking_configuration`, `conversion_setup`, `data_quality`,
`custom_dimension`, `integration`, `compliance`.

## Critical rules

1. **PII is always critical.** Flag it loudly and name the parameter.
2. **Key events are the anchor** — for GA4 reporting and for Ads bidding. Weight them.
3. **Quote real numbers**: retention months, `(not set)` %, dimension counts.
4. **Read-only.** Never change property settings — surface and recommend.
