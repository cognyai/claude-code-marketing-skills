---
name: ga4-audit
description: Google Analytics 4 configuration and data-quality audit — key events, data streams, custom dimensions, attribution, retention, PII, Ads link, BigQuery export
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-analytics-4, plausible, fathom-analytics, simple-analytics, shopify, woocommerce]
user-invocable: true
argument-hint: "[full|config|events|data-quality]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_get_property
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_data_streams
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_custom_dimensions
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_custom_metrics
  - mcp__cogny__mcp__Google_Analytics_4__tool_get_metadata
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_google_ads_links
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Plausible__aggregate
  - mcp__cogny__mcp__Fathom_Analytics__aggregate
  - mcp__cogny__mcp__Simple_Analytics__stats
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# GA4 Audit

A one-time audit of a Google Analytics 4 property — configuration *and* data quality.
GA4 collects data the moment the tag fires, but most properties quietly leak trust:
unmarked key events, PII in parameters, no Ads link, `(not set)` traffic. This skill
finds those before they corrupt a quarter of reporting.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answered by (enhanced when connected) |
|-----|---------|---------------------------------------------|
| Property config, key events, dimensions, Ads link | GA4 | — (only GA4 has a config API) |
| Fix a missing / noisy key event (asks first, if exposed) | GA4 `tool_mark_key_event`, `tool_unmark_key_event` | GA4 UI (Admin → Events → Mark as key event) when the tools aren't exposed |
| Parameters the tags send | GTM `tool_list_tags` | — (ask the user for the tracking plan) |
| Consent / ad-blocker gap | GA4 users | Plausible `aggregate`, Fathom `aggregate`, Simple Analytics `stats` |
| Purchase capture rate | GA4 `purchase` count | Shopify `tool_list_orders`, WooCommerce `get_sales_report` |

Cookieless tools (Plausible, Fathom, Simple) and the store count what GA4 misses, so they
turn "data quality" from guesswork into a measured gap.

## Prerequisites Check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
GA4 Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Analytics 4 (Google Tag Manager optional).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny: GA4's configuration is only readable through its API.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Analytics_4__tool_get_property` isn't, say
"connect Google Analytics 4 in Cogny" and stop.

**Health check:** call `list_integrations`, then `tool_list_account_summaries` as the cheap read
(and GTM `tool_list_accounts` if GTM is connected). `health_status` misses revoked tokens, so a 401,
Forbidden or scope error is 🔴 "reconnect <integration>"; don't retry it. If a tool named here is
missing, call `refresh_mcp_discovery` once; new tools only load after the client reconnects, so use
the step's fallback for this run and mark it ⚠ "needs reconnect".

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

Record: time zone, currency, industry category, and property type.

**Data retention: not verifiable via API — ask the user.** `tool_get_property` has no
retention field. Ask them to check Admin → Data collection and modification → Data retention,
and flag it if it's at the 2-month default (it should be 14 months so year-over-year
exploration works). Mark it "unverified" in the report until they confirm.

### 2. Data streams

```
tool_list_data_streams   (property_id)
```

Flag:
- Multiple web streams for one site (splits data, double-counts users)
- Missing iOS/Android streams for a business that has apps
- Enhanced measurement settings: **not verifiable via API — ask the user** (the stream
  response has no enhanced-measurement data). Infer what you can from the event list in step 3
  (`scroll`, `file_download`, `view_search_results`, `video_start`, `form_start` present or
  absent), and label it as inferred.

### 3. Key events (conversions)

```
tool_list_conversion_events   (property_id)
tool_run_report   (property_id,
  date_ranges: [{"startDate": "30daysAgo", "endDate": "yesterday"}],
  dimensions: ["eventName"], metrics: ["eventCount", "keyEvents"])
```

The report shows which events actually fire and which key events recorded anything. Step 2's
enhanced-measurement inference reads from it.

Flag:
- **No key events configured** — Ads bidding and GA4 reporting both lose their anchor
- Key events marked on noisy automatic events (`page_view`, `scroll`) — inflates the
  conversion count and misleads everyone
- Obvious business goals *not* marked as key events (e.g. `generate_lead`, `purchase`,
  `sign_up`)
- More than ~10–15 key events — when everything is a conversion, nothing is

Fix (write, asks first, **if available**): `tool_mark_key_event` (`property_id`, `event_name`,
`counting_method`: `ONCE_PER_EVENT` or `ONCE_PER_SESSION`) for a real goal that isn't
marked, `tool_unmark_key_event` (`property_id`, `event_name`) for a noisy one. Takes effect
for new data only. Unmarking also removes it from any Ads import; say so before asking.
These tools exist in the proxy but aren't exposed on every workspace. If they don't load, don't
refresh in a loop: tell the user to mark/unmark the event in the GA4 UI (Admin → Events →
toggle "Mark as key event") and give them the exact event name, case-sensitive.

### 4. Custom dimensions & metrics

```
tool_list_custom_dimensions   (property_id)
tool_list_custom_metrics      (property_id)
tool_get_metadata             (property_id)
```

`tool_get_metadata` returns ~121k characters (every standard field). Don't read it whole: when
the result is saved to a file, filter it with jq, e.g.
`jq -r '.dimensions[] | select(.apiName | startswith("customEvent:") or startswith("customUser:")) | .apiName'`.

Flag:
- Event parameters collected by the tag but **never registered** as custom dimensions
  (the data is invisible in reports). With GTM connected, `tool_list_tags` on the live
  workspace and collect the event parameter names the GA4 event tags send; any parameter with
  no matching `customEvent:<name>` dimension is unregistered. Without GTM, ask the user for
  the tracking plan and say the check is partial
- Approaching the 50 event-scoped / 25 user-scoped dimension limits
- High-cardinality registered dimensions (timestamps, IDs) — they cause `(other)` rows

### 5. Traffic & data-quality report

```
tool_run_report   (property_id, last 30 days,
  dimensions: sessionDefaultChannelGroup, sessionSource, sessionMedium,
  metrics: sessions, keyEvents, totalUsers)
```

Use `keyEvents`, not the deprecated `conversions` metric. If `run_report` times out with
`order_bys`, retry once without them and sort the rows yourself.

Flag:
- A large `Unassigned` or `(not set)` share — broken UTMs or tagging gaps
  (point the user to `/utm-builder`)
- A `Direct` share above ~40% — usually lost referrer data or missing tags
- Self-referrals (your own domain as a source) — needs an unwanted-referral filter
- Login and payment referrers (`accounts.google.com`, `checkout.stripe.com`, `paypal.com`,
  OAuth providers such as `login.microsoftonline.com`, `github.com/login`, `appleid.apple.com`) —
  they steal credit for the conversion from the real source; add them to the unwanted-referral list
- Internal traffic visible in reports — no internal-traffic filter applied

### 5b. Cross-check against other sources (enhanced when connected)

Call `list_integrations` once. For each healthy source, compare the same 30 days:

| Source | Call | Compare with GA4 | Flag when |
|--------|------|------------------|-----------|
| Plausible | `aggregate` (`site_id`, `metrics: [visitors, visits]`, `date_range: 30d`) | `totalUsers`, `sessions` | GA4 is >30% lower: consent banner or blockers dropping data |
| Fathom Analytics | `aggregate` (`entity: pageview`, `entity_id: <site id>`, `aggregates: visits,uniques`, `date_from`, `date_to`) | same | same |
| Simple Analytics | `stats` (`hostname`, `start`, `end`) | same | same |
| Shopify | `tool_list_orders` (`query_filter: "created_at:>=YYYY-MM-DD"`) | `purchase` event count | GA4 purchases <85% of orders, or above 100% (duplicate firing) |
| WooCommerce | `get_sales_report` (`date_min`, `date_max`) | `purchase` count, `totalRevenue` | same |

Report each source's number next to GA4's, named. Don't expect a match: cookieless tools
count visitors differently. A gap you can measure goes in the Data quality score; deep
reconciliation belongs in `/conversion-debug`.

### 6. PII & policy check

Scan event and parameter names from `get_metadata` for anything that could carry
personal data — `email`, `phone`, `user_email`, full names, raw addresses in
parameters or in the page path / query string.

Then query the URLs themselves; names alone miss PII in query strings. This found real email
addresses and magic-link tokens in a live run:

```
tool_run_report   (property_id, last 90 days,
  dimensions: ["pageLocation"], metrics: ["screenPageViews"], limit: 50,
  dimension_filter: {"orGroup": {"expressions": [
    {"filter": {"fieldName": "pageLocation", "stringFilter": {"matchType": "CONTAINS", "value": "email="}}},
    {"filter": {"fieldName": "pageLocation", "stringFilter": {"matchType": "CONTAINS", "value": "%40"}}},
    {"filter": {"fieldName": "pageLocation", "stringFilter": {"matchType": "CONTAINS", "value": "@"}}},
    {"filter": {"fieldName": "pageLocation", "stringFilter": {"matchType": "CONTAINS", "value": "token"}}}]}})
```

Any row is a finding. Redact the values when you quote them (show the path and parameter
name, never the address or token).

🔴 PII in GA4 violates Google's policy and risks the property being deleted. Flag it
as critical and name the exact parameter.

### 7. Integrations

```
tool_list_google_ads_links   (property_id)
```

Flag:
- **No Google Ads link** — conversions can't flow to Ads for bidding (an empty result
  means no link on this property; confirm with the user if they import via another property)
- BigQuery export and Search Console link: **not verifiable via API — ask the user**
  (the API exposes neither link). Ask them to check Admin → Product links. Recommend BigQuery
  export for any property that wants raw-data analysis (`/ga4-bigquery-schema` covers the
  schema). Mark both "unverified" in the report until confirmed

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

On Cloud, `create_ticket` takes the same content with the fields mapped per section 2 of
the routing guide.

Action types: `tracking_configuration`, `conversion_setup`, `data_quality`,
`custom_dimension`, `integration`, `compliance`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **PII is always critical.** Flag it loudly and name the parameter.
2. **Key events are the anchor** — for GA4 reporting and for Ads bidding. Weight them.
3. **Quote real numbers**: `(not set)` %, dimension counts. Settings the API can't read
   (retention, enhanced measurement, BigQuery and Search Console links) are "unverified", never guessed.
4. **Read-only by default.** The only writes are `tool_mark_key_event` /
   `tool_unmark_key_event`, only when the workspace exposes them, and only after the user says
   yes to the exact event. Otherwise point to the GA4 UI.
5. **Name the source on every cross-check number.** Never average GA4 with Plausible or the store.
