---
name: conversion-debug
description: Conversion Tracking Debugger — diagnose discrepancies across GTM, GA4, Google Ads & Meta Pixel with live API access, BigQuery validation queries, and troubleshooting flowcharts
version: "1.1.2"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<issue or topic>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # GTM tools
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_triggers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_tag
  - mcp__cogny__mcp__Google_Tag_Manager__tool_search_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_workspace_status
  # GA4 tools
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_google_ads_links
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_realtime_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_data_streams
  # Google Ads tools
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  # Meta tools
  - mcp__cogny__mcp__Meta_Ads__tool_get_pixels
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  # Other ad platforms (when connected)
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_conversions
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_analytics
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_pixels
  - mcp__cogny__mcp__TikTok_Ads__tool_get_insights
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_conversion_events
  - mcp__cogny__mcp__Reddit_Ads__tool_get_reporting
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_pixels
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_stats
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_web_event_tags
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__X_Ads__tool_get_analytics
  # Ground truth and site health (when connected)
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__Microsoft_Clarity__get_live_insights
  - mcp__cogny__mcp__PostHog__list_projects
  - mcp__cogny__mcp__PostHog__list_insights
  - mcp__cogny__mcp__PostHog__get_insight
  - mcp__cogny__mcp__Mixpanel__run_segmentation
  - mcp__cogny__mcp__Stripe__stripe_api_read
---

# Conversion Tracking Debugger

Debug conversion tracking across GTM, GA4, Google Ads, and Meta Pixel. Diagnose discrepancies, find duplicate conversions, validate enhanced conversions, audit Consent Mode v2, and run BigQuery validation queries.

Full docs: https://cogny.com/docs/conversion-tracking-debugger

## Usage

```
/conversion-debug                          # Full debugging overview
/conversion-debug duplicate conversions    # Diagnose duplicate purchases
/conversion-debug consent mode             # Consent Mode v2 audit
/conversion-debug meta vs ga4              # Cross-platform discrepancy analysis
/conversion-debug enhanced conversions     # Validate enhanced conversion setup
/conversion-debug server-side tagging      # Server-side GTM overview
/conversion-debug value wrong              # Debug incorrect conversion values
```

## Instructions

You are a conversion tracking debugging expert. Use this reference and the available MCP tools to help users diagnose and fix conversion tracking issues across GTM, GA4, Google Ads, and Meta Pixel.

When the user asks a question, find the relevant section below and provide precise, actionable answers. When MCP tools are available, use them to pull live data from the user's accounts to validate findings.

If the user provides a specific topic as an argument, focus on that area. Otherwise, ask what platform or issue they need help with.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this once,
then answer from the reference below:

```
Conversion Debug can read your live tracking setup through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Tag Manager, Google Analytics 4, Google Ads,
   Meta Ads and your store or Stripe (any subset works).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: use the flowcharts, browser checks (GTM Preview, DevTools,
Events Manager Test Events) and the BigQuery validation SQL below.
```

Skip every live-data step with one line, e.g. "Reconciliation table: not connected (connecting
adds side-by-side counts from GA4, Ads and your store)". If Cogny is connected but an
integration isn't, say "connect <X> in Cogny"; if it's connected but fails, "reconnect <X> in Cogny".

## Works with

Works with zero accounts (reference, flowcharts, SQL). Each connected source adds one
column to the reconciliation table (see "Cross-Platform Reconciliation"):

| Job | Primary | Also answered by |
|-----|---------|------------------|
| Ground truth (real orders) | Shopify `tool_list_orders` | WooCommerce `list_orders` / `get_sales_report`; BigQuery queries below |
| Ground truth (sign-ups, SaaS) | PostHog `list_insights` → `get_insight` | Mixpanel `run_segmentation` |
| Ground truth (revenue, SaaS) | Stripe `stripe_api_read` (`GetInvoices`, `GetSubscriptions`) | — |
| Site analytics count | GA4 `tool_run_report` | — |
| Tag config | GTM `tool_list_tags`, `tool_get_tag` | — |
| Ad-platform conversions | Google Ads `tool_execute_gaql` | Meta, Microsoft Ads, LinkedIn, TikTok, Reddit, Snapchat, X |
| Pixel / tag exists and is active | Meta `tool_get_pixels` | TikTok `tool_get_pixels`, LinkedIn `tool_get_conversions`, Reddit `tool_get_conversion_events`, Snapchat `tool_list_pixels`, X `tool_get_web_event_tags` |
| Site broke vs tracking broke | — | Microsoft Clarity `get_live_insights` |

**When MCP tools are available, follow this diagnostic approach:**

0. Health check: `list_integrations`, then one cheap read per integration you'll use (GTM
   `tool_list_accounts`, `tool_list_ad_accounts`, Stripe `GetSubscriptions` with `limit: 1`).
   `health_status` misses revoked tokens, so a 401, Forbidden or scope error is 🔴 "reconnect
   <integration>"; don't retry it. If a tool named here is missing, call `refresh_mcp_discovery`
   once; new tools only load after the client reconnects, so drop that column for this run and
   mark it ⚠ "needs reconnect".
1. Use GTM tools (`tool_list_accounts` → `tool_list_containers` → `tool_list_workspaces` for the
   IDs) to inspect tags, triggers, and workspace status
2. Use GA4 tools to check conversion events, run reports, and verify data streams. Find the
   property with `tool_list_account_summaries` (each account lists its `property_summaries`; ask
   if several match the site), and use that `property_id` for every GA4 call
3. Use Google Ads tools to query conversion action status and performance
4. Use Meta (and any other connected ad platform) to check pixel configuration and compare conversion counts
5. Cross-reference findings against the store's orders to identify the root cause
   (see "Cross-Platform Reconciliation")

---

## The Conversion Tracking Stack

Understanding data flow is the first step to debugging:

```
User Action (click, form submit, purchase)
        |
        v
+-------------------+
|   Website / App   |
|   (dataLayer)     |
+-------------------+
        |
        v
+-------------------+       +-------------------+
|  Google Tag       | ----> |  GA4              |
|  Manager (GTM)    |       |  (Measurement     |
|                   |       |   Protocol)       |
|  - GA4 Config Tag |       +-------------------+
|  - GA4 Event Tag  |               |
|  - Google Ads Tag |               v
|  - Meta Pixel Tag |       +-------------------+
+-------------------+       |  BigQuery Export  |
        |                   |  (daily/intraday) |
        |                   +-------------------+
        |
        +----------> +-------------------+
        |            |  Google Ads       |
        |            |  (Conversion      |
        |            |   Tracking)       |
        |            +-------------------+
        |
        +----------> +-------------------+
                     |  Meta Pixel       |
                     |  + Conversions    |
                     |    API (CAPI)     |
                     +-------------------+
```

**Key data flow points:**

1. **dataLayer push** -- Website pushes event data to `window.dataLayer`
2. **GTM triggers** -- Tags fire based on trigger conditions matching dataLayer events
3. **Network requests** -- Each tag sends a separate HTTP request to its destination
4. **Platform processing** -- Each platform processes, deduplicates, and attributes independently
5. **BigQuery export** -- GA4 exports raw events to BigQuery (daily ~5 AM property timezone)

## Cross-Platform Reconciliation (enhanced when connected)

Call `list_integrations` once. Pull the **same date range** (last 7 complete days, in each
account's time zone) from every healthy source and build one table, one column per
source. Never sum columns; each platform attributes its own way.

| Source | Call | Conversion count |
|--------|------|------------------|
| Shopify (truth) | `tool_list_orders` (`query_filter: "created_at:>=YYYY-MM-DD financial_status:paid"`, page with `after`) | paid orders |
| WooCommerce (truth) | `get_sales_report` (`date_min`, `date_max`), or `list_orders` (`after`, `before`, `status: completed`) | orders |
| PostHog (SaaS truth) | `list_projects` → `list_insights` (`project_id`, `search: "signup"`) → `get_insight` | product sign-up event |
| Mixpanel (SaaS truth) | `run_segmentation` (`event`: the sign-up event, `from_date`, `to_date`) | product sign-up event |
| Stripe (SaaS revenue truth) | `stripe_api_read` `GetInvoices` (`status: "paid"`, `created` in the window, `limit: 20`; invoices are large, so page with `starting_after: <last id>` while `has_more`) and `GetSubscriptions` (`status: "all"`, `created` in the window) | paid invoices / new subscriptions, and their amount |
| GA4 | `tool_run_report` (`dimensions: [eventName]`, `metrics: [eventCount, keyEvents, totalRevenue]`) | `purchase` / lead event |
| Google Ads | `tool_execute_gaql`: `SELECT segments.conversion_action_name, metrics.conversions, metrics.all_conversions FROM customer WHERE segments.date DURING LAST_7_DAYS` | per action |
| Meta | `tool_list_ad_accounts` → `tool_get_insights` (`ad_account_id`, `level: account`, `date_preset: last_7d`) | `actions` (purchase / lead) |
| Microsoft Ads | `tool_list_accounts` → `tool_get_report` (`account_id`, `report_type: campaign`, `start_date`, `end_date`) | Conversions |
| LinkedIn | `tool_get_analytics` (`ad_account_id`, `start_date`, `end_date`, `pivot: ACCOUNT`) | conversions |
| TikTok | `tool_get_insights` (`advertiser_id`, `start_date`, `end_date`, `level: AUCTION_ADVERTISER`, `metrics: conversion`) | conversion |
| Reddit | `tool_get_reporting` (`ad_account_id`, `start_date`, `end_date`, `fields`: the `KEY_CONVERSION_*` set) | key conversions |
| Snapchat | `tool_list_organizations` → `tool_list_ad_accounts` → `tool_get_stats` (`entity_id`: ad account, `level`, `start_time`, `end_time`, `fields`) | conversion fields |
| X | `tool_get_campaigns` → `tool_get_analytics` (`account_id`, `entity: CAMPAIGN`, `start_time`, `end_time` as ISO 8601 at midnight, `granularity: TOTAL`). First call with `metric_groups: [BILLING]` on campaigns whose flight overlaps the window (max 20 `entity_ids` per call), then pass **only the IDs that spent** (`billed_charge_local_micro` > 0) with `metric_groups: [WEB_CONVERSION]` | `conversion_purchases` / `conversion_sign_ups` |

**Empty output means zero, not an error.** An empty GAQL result means no conversions recorded
in the window; empty Meta insights means no delivery (no spend) in the window. Write 0 in the
table. Only an actual error message (401, scope, `PROHIBITED_METRIC`, …) makes a cell "not read".

Read it like this:
- **GA4 `sign_up` far below PostHog / Mixpanel sign-ups:** the web tag misses the
  success state (SPA route, redirect to the app domain); the product event is the truth.
- **GA4 < store by >15%:** tag misses orders (consent, blockers, thank-you page skipped by
  payment redirects). **GA4 > store:** duplicate firing; run "Find Duplicate Transaction IDs".
- **Ad platform > store:** that platform counts view-through, modelled or every-conversion;
  normal for Meta/TikTok, a bug if it exceeds total orders across all channels.
- **X conversions > GA4's site-wide count for the same event:** X can't have caused more
  conversions than the site recorded from every channel. Suspect view-through or
  attribution-window inflation (X counts post-view and long post-engagement windows by
  default); compare post-engagement only, and don't treat X's number as incremental.
- **SaaS:** Stripe paid invoices / new subscriptions are the revenue truth; compare GA4
  `purchase` / sign-up revenue and ad-platform conversion values against them.
- **Google Ads = 0 but GA4 > 0** for the same event: see "Google Ads = 0 but GA4 > 0" below.
- **Ad platform at 0 with spend:** read the pixel row: TikTok `tool_get_pixels`, LinkedIn
  `tool_get_conversions`, Reddit `tool_get_conversion_events`, Snapchat `tool_list_pixels`,
  X `tool_get_web_event_tags` (inactive / no recent activity = tag not firing).
- **Everything dropped at once, store too:** the site broke, not tracking. Clarity
  `get_live_insights` (`num_of_days: 3`, `metrics: [Script Error Count, Error Click Count,
  Dead Click Count]`, `dimensions: [URL]`) on the checkout or form pages confirms it.

Name the source on every number and use each account's currency.

## Common Discrepancies and Why

### GA4 vs Google Ads Conversion Count Differences

GA4 and Google Ads will almost never match. This is expected.

| Factor | GA4 | Google Ads |
|--------|-----|------------|
| **Attribution model** | Data-driven (cross-channel) | Data-driven (Google channels only) |
| **Counting method** | Configurable: once per session or once per event | Configurable: one or every conversion |
| **Conversion window** | Default 30 days | Default 30 days (up to 90 days) |
| **Cross-device** | Google Signals + User-ID | Google account sign-in |
| **View-through** | Not counted by default | Included for Display/Video (1-day default) |
| **Data freshness** | 24-72h processing lag | Conversions appear within hours |
| **Modeled conversions** | Behavioral modeling for consent gaps | Conversion modeling for unobserved |

Typical variance: 5-20% is normal. Over 20% warrants investigation.

**MCP diagnostic approach:**

```
1. GA4: tool_list_conversion_events → check which events are marked as conversions
2. GA4: tool_run_report → pull conversion counts by date
3. Google Ads: tool_execute_gaql → query conversion_action metrics
4. Compare the numbers and identify the gap source
```

### Google Ads = 0 but GA4 > 0

GA4 records the event but Google Ads shows no conversions for it. That's not attribution
variance, it's a broken link. Check these in order and stop at the first that fails:

| # | Cause | How to check (connected) | Without Cogny |
|---|-------|--------------------------|---------------|
| 1 | GA4 key event isn't imported into Ads, or GA4 isn't linked | GA4 `tool_list_google_ads_links` (`property_id`): empty = no link. Google Ads `tool_execute_gaql`: `SELECT conversion_action.name, conversion_action.type, conversion_action.status FROM conversion_action WHERE conversion_action.type IN ('GOOGLE_ANALYTICS_4_CUSTOM', 'GOOGLE_ANALYTICS_4_PURCHASE')`: no `ENABLED` row for the event = not imported. Also confirm the event is a key event (`tool_list_conversion_events`) | GA4 Admin → Product links → Google Ads; Ads → Goals → Conversions → Summary |
| 2 | Auto-tagging (gclid) is off | `SELECT customer.auto_tagging_enabled FROM customer` → `false` | Ads → Admin → Account settings → Auto-tagging; click an ad and check the landing URL for `gclid=` |
| 3 | Conversion Linker missing (GTM-tagged sites using an `AW-` tag) | GTM `tool_list_tags`: no tag with `type: gclidw`, or one that doesn't fire on All Pages | `document.cookie` has no `_gcl_aw` after an ad click |
| 4 | Event-name case mismatch (`first_login` sent, `FirstLogin` is the key event / import) | Compare GTM tag `eventName` (or, when it is `{{Event}}`, the trigger's `customEventFilter` value) with the key-event and import names, case-sensitively; `/gtm-audit` Step 6c does this | GA4 DebugView event name vs Admin → Events |
| 5 | The import is a Secondary action | `SELECT conversion_action.name, conversion_action.primary_for_goal, metrics.all_conversions FROM conversion_action WHERE segments.date DURING LAST_30_DAYS`: `primary_for_goal = false` with `all_conversions` > 0 counts only in "All conv.", never in Conversions | Ads → Goals → the action's "Action optimization" says Secondary |

Also rule out the normal causes before calling it broken: imports take up to 24h after the GA4
event, and Ads only counts conversions it can attribute to a Google ad click in the window (GA4
counts every channel). GA4 > 0 from paid search sessions (`sessionGoogleAdsCampaignName`) with
Ads at 0 rules those out.

### Meta Pixel vs GA4 Differences

| Factor | Meta | GA4 |
|--------|------|-----|
| **Click-through window** | 7 days (default) | 30 days (default) |
| **View-through** | 1-day included by default | Not counted by default |
| **Attribution** | Last-touch within Meta | Data-driven cross-channel |
| **Deduplication** | `eventID` for browser+CAPI dedup | `transaction_id` parameter |
| **Cross-device** | Facebook login graph | Google Signals + User-ID |

**Why Meta often reports higher:** View-through conversions. User sees Meta ad, doesn't click, later converts via Google search. Meta counts it; GA4 attributes to organic/CPC.

### GTM Firing but GA4 Not Receiving

1. **Consent Mode blocking** -- Tag fires but sends no data when consent denied
2. **Ad blockers** -- ~25-30% of users block `google-analytics.com` requests
3. **Race conditions** -- Page unloads before request completes (form submits, outbound links)
4. **Measurement ID mismatch** -- Wrong `G-XXXXXXX` in the tag config
5. **Data filters** -- GA4 property filters hiding or altering events
6. **Draft vs published** -- GTM Preview uses draft; live site uses published version

### Duplicate Conversions

The most expensive tracking bug. Common causes:

1. **Missing `transaction_id`** -- GA4 cannot deduplicate without a unique ID
2. **Double-firing tags** -- Multiple tags sending the same conversion
3. **Thank-you page reloads** -- User refreshes the confirmation page
4. **Back button** -- User navigates back to confirmation
5. **Missing CAPI dedup** -- Meta Pixel and CAPI both fire without matching `eventID`

Prevention:

```javascript
// dataLayer push with transaction_id for deduplication
window.dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: 'T-12345',  // REQUIRED for dedup
    value: 99.99,
    currency: 'USD',
    items: [/* ... */]
  }
});
```

```javascript
// Prevent duplicate pushes on page reload
if (!window.sessionStorage.getItem('purchase_tracked_T-12345')) {
  window.dataLayer.push({
    event: 'purchase',
    ecommerce: { transaction_id: 'T-12345', value: 99.99, currency: 'USD' }
  });
  window.sessionStorage.setItem('purchase_tracked_T-12345', 'true');
}
```

## Debugging Checklist by Platform

### Google Tag Manager (GTM)

**Preview Mode Inspection:**
- Correct workspace/container version active?
- Trigger event appears in the timeline?
- Tag shows as "Fired"?
- No unexpected duplicate tags firing?

**Trigger Conditions:**
- Event name matches `dataLayer.push({ event: '...' })` exactly (case-sensitive)?
- All filter conditions correct?
- No blocking triggers preventing fire?

**Variable Values (in Preview mode):**
- `transaction_id` populated and unique?
- `value` and `currency` present and correct types?
- Custom JS variables returning expected values?

**dataLayer Inspection:**

```javascript
// View full dataLayer
console.table(window.dataLayer);

// Filter for purchase events
window.dataLayer.filter(e => e.event === 'purchase');

// Check ecommerce data
window.dataLayer.filter(e => e.event === 'purchase').map(e => e.ecommerce);
```

**Network Request Verification (DevTools > Network):**
- `google-analytics.com/g/collect` -- GA4
- `googleads.g.doubleclick.net/pagead/conversion` -- Google Ads
- `facebook.com/tr` -- Meta Pixel

**MCP diagnostic:**

```
tool_list_tags → see all tags in the container
tool_search_tags → find conversion-related tags
tool_get_tag → inspect specific tag configuration
tool_list_triggers → verify trigger setup
tool_get_workspace_status → check for unpublished changes
```

### GA4

**DebugView:**

```javascript
// Enable debug mode
gtag('config', 'G-XXXXXXX', { debug_mode: true });
```

Then GA4 > Admin > DebugView: verify events, parameters, user properties.

**Realtime Reports:**
- Event count incrementing on trigger?
- Conversions card shows the event?

**MCP diagnostic:**

```
tool_list_conversion_events → verify which events are marked as conversions
tool_run_realtime_report → check real-time event data
tool_run_report → pull historical conversion data by date
tool_list_data_streams → verify stream configuration
```

**BigQuery Validation:**

```sql
-- Check conversion events in BigQuery
SELECT
  event_name,
  COUNT(*) as event_count,
  COUNT(DISTINCT user_pseudo_id) as unique_users,
  MIN(TIMESTAMP_MICROS(event_timestamp)) as earliest,
  MAX(TIMESTAMP_MICROS(event_timestamp)) as latest
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
  AND event_name IN ('purchase', 'generate_lead', 'sign_up', 'add_to_cart', 'begin_checkout')
GROUP BY event_name
ORDER BY event_count DESC
```

### Google Ads

**Conversion Action Status:**
- "Recording conversions" (green) = working
- "No recent conversions" = tag installed but not firing or data delayed
- "Tag inactive" = no hits in 7+ days
- "Unverified" = tag never detected

**MCP diagnostic:**

```
tool_execute_gaql →
  SELECT
    conversion_action.name,
    conversion_action.status,
    conversion_action.type,
    conversion_action.tag_snippets,
    metrics.all_conversions,
    metrics.all_conversions_value
  FROM conversion_action
  WHERE segments.date DURING LAST_7_DAYS

tool_get_gaql_doc → look up conversion_action fields
```

`metrics.conversions` / `conversions_value` are prohibited on the `conversion_action` resource
(`PROHIBITED_METRIC`); use `all_conversions` there. For the primary-goal `conversions` count per
action, query `FROM customer` with `segments.conversion_action_name` (as in the reconciliation
table). An empty result means zero conversions in the window.

**Google Tag Verification:**

```javascript
// Check gtag is loaded
typeof gtag === 'function'  // Should be true

// Check conversion linker cookie
document.cookie.split(';').filter(c => c.includes('_gcl'))
```

### Meta Pixel

**Events Manager Test Events:**
- Enter website URL, perform conversion, verify event appears
- Check event parameters (value, currency, content_ids)
- Check Event Match Quality score (aim for 6+)

**CAPI Deduplication:**
Both browser Pixel and CAPI events must share the same `eventID`:

```javascript
// Browser-side
fbq('track', 'Purchase', {
  value: 99.99,
  currency: 'USD',
  content_ids: ['SKU-123'],
  content_type: 'product'
}, { eventID: 'purchase_T-12345' });
```

```bash
# Server-side CAPI
curl -X POST \
  "https://graph.facebook.com/v24.0/PIXEL_ID/events?access_token=TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "event_name": "Purchase",
      "event_time": 1700000000,
      "event_id": "purchase_T-12345",
      "action_source": "website",
      "user_data": {
        "em": ["HASHED_EMAIL"],
        "client_ip_address": "1.2.3.4",
        "client_user_agent": "Mozilla/5.0..."
      },
      "custom_data": {
        "value": 99.99,
        "currency": "USD",
        "content_ids": ["SKU-123"]
      }
    }]
  }'
```

Graph API versions expire about two years after release (v18 no longer works). Check the latest
version at https://developers.facebook.com/docs/graph-api/changelog and use it.

**MCP diagnostic:**

```
tool_get_pixels → verify pixel configuration
tool_get_insights → pull conversion data for comparison with GA4/Google Ads
```

## BigQuery Validation Queries

### Count Conversions by Day (Compare to GA4 UI)

```sql
SELECT
  PARSE_DATE('%Y%m%d', event_date) as date,
  event_name,
  COUNT(*) as total_events,
  COUNT(DISTINCT user_pseudo_id) as unique_users,
  COUNT(DISTINCT
    CONCAT(user_pseudo_id, '-',
      CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING))
  ) as unique_sessions
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name IN ('purchase', 'generate_lead', 'sign_up')
GROUP BY 1, 2
ORDER BY 1 DESC, 2
```

Small differences (1-5%) between BigQuery and GA4 UI are normal due to thresholding, sampling, and modeled conversions (present in UI, absent in BigQuery).

### Find Duplicate Transaction IDs

```sql
WITH purchase_events AS (
  SELECT
    PARSE_DATE('%Y%m%d', event_date) as date,
    user_pseudo_id,
    (SELECT value.string_value FROM UNNEST(event_params)
     WHERE key = 'transaction_id') as transaction_id,
    TIMESTAMP_MICROS(event_timestamp) as event_time,
    ecommerce.purchase_revenue_in_usd as revenue
  FROM `project.analytics_PROPERTY_ID.events_*`
  WHERE _TABLE_SUFFIX BETWEEN
    FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND event_name = 'purchase'
)

SELECT
  transaction_id,
  COUNT(*) as occurrence_count,
  COUNT(DISTINCT user_pseudo_id) as distinct_users,
  MIN(event_time) as first_occurrence,
  MAX(event_time) as last_occurrence,
  TIMESTAMP_DIFF(MAX(event_time), MIN(event_time), SECOND) as seconds_between,
  SUM(revenue) as total_revenue_recorded,
  MAX(revenue) as actual_revenue
FROM purchase_events
WHERE transaction_id IS NOT NULL
GROUP BY transaction_id
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC
```

```sql
-- Find purchases with NULL transaction_id (cannot be deduplicated)
SELECT
  PARSE_DATE('%Y%m%d', event_date) as date,
  COUNT(*) as purchases_without_txn_id,
  SUM(ecommerce.purchase_revenue_in_usd) as revenue_at_risk
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'purchase'
  AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') IS NULL
GROUP BY 1
ORDER BY 1 DESC
```

### Check Conversion Event Parameters Completeness

```sql
SELECT
  event_name,
  param.key,
  COUNT(*) as events_with_param,
  COUNT(DISTINCT user_pseudo_id) as users_with_param,
  COUNTIF(param.value.string_value IS NOT NULL) as has_string_value,
  COUNTIF(param.value.int_value IS NOT NULL) as has_int_value,
  COUNTIF(param.value.float_value IS NOT NULL) as has_float_value
FROM `project.analytics_PROPERTY_ID.events_*`,
  UNNEST(event_params) as param
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name IN ('purchase', 'generate_lead', 'sign_up', 'begin_checkout')
GROUP BY 1, 2
ORDER BY 1, events_with_param DESC
```

```sql
-- Check required ecommerce fields on purchase events
SELECT
  PARSE_DATE('%Y%m%d', event_date) as date,
  COUNT(*) as total_purchases,
  COUNTIF(ecommerce.transaction_id IS NOT NULL) as has_transaction_id,
  COUNTIF(ecommerce.purchase_revenue_in_usd > 0) as has_revenue,
  COUNTIF(ecommerce.total_item_quantity > 0) as has_quantity,
  COUNTIF(ARRAY_LENGTH(items) > 0) as has_items,
  ROUND(SAFE_DIVIDE(
    COUNTIF(
      ecommerce.transaction_id IS NOT NULL
      AND ecommerce.purchase_revenue_in_usd > 0
      AND ARRAY_LENGTH(items) > 0
    ), COUNT(*)
  ) * 100, 1) as pct_fully_complete
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'purchase'
GROUP BY 1
ORDER BY 1 DESC
```

### Validate Enhanced Conversions Data

```sql
SELECT
  PARSE_DATE('%Y%m%d', event_date) as date,
  event_name,
  COUNT(*) as total_events,
  COUNTIF(user_id IS NOT NULL) as has_user_id,
  COUNTIF(
    (SELECT value.string_value FROM UNNEST(user_properties) WHERE key = 'email') IS NOT NULL
    OR (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'user_data_email') IS NOT NULL
  ) as has_email_signal,
  COUNTIF(
    (SELECT value.string_value FROM UNNEST(user_properties) WHERE key = 'phone') IS NOT NULL
    OR (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'user_data_phone') IS NOT NULL
  ) as has_phone_signal
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name IN ('purchase', 'generate_lead', 'sign_up')
GROUP BY 1, 2
ORDER BY 1 DESC, 2
```

### Cross-Reference Expected vs Actual Events

```sql
WITH expected_events AS (
  SELECT event_name FROM UNNEST([
    'purchase', 'add_to_cart', 'begin_checkout', 'view_item',
    'generate_lead', 'sign_up', 'add_payment_info', 'add_shipping_info'
  ]) as event_name
),
actual_events AS (
  SELECT
    event_name,
    COUNT(*) as event_count,
    MAX(TIMESTAMP_MICROS(event_timestamp)) as last_seen
  FROM `project.analytics_PROPERTY_ID.events_*`
  WHERE _TABLE_SUFFIX BETWEEN
    FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  GROUP BY event_name
)

SELECT
  e.event_name,
  COALESCE(a.event_count, 0) as event_count,
  a.last_seen,
  CASE
    WHEN a.event_count IS NULL THEN 'MISSING - never received'
    WHEN a.last_seen < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 48 HOUR) THEN 'STALE - no events in 48h'
    ELSE 'OK'
  END as status
FROM expected_events e
LEFT JOIN actual_events a USING(event_name)
ORDER BY
  CASE WHEN a.event_count IS NULL THEN 0 WHEN a.last_seen < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 48 HOUR) THEN 1 ELSE 2 END,
  e.event_name
```

## Consent Mode v2

### How It Affects Conversion Tracking

Google Consent Mode v2 (required in EEA since March 2024) controls data collection based on user consent.

**Required signals:**

| Signal | Controls |
|--------|----------|
| `analytics_storage` | GA4 cookies and full measurement |
| `ad_storage` | Google Ads cookies and conversion measurement |
| `ad_user_data` | Sending user data to Google for advertising |
| `ad_personalization` | Remarketing and personalized advertising |

**Behavior:**
- `granted` -- Full data collection, cookies set, user-level data sent
- `denied` -- Cookieless pings, Google models conversions (appear in UI, NOT in BigQuery)

### Implementation

```javascript
// Set defaults BEFORE GTM snippet
gtag('consent', 'default', {
  analytics_storage: 'denied',
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  wait_for_update: 500
});

// Update on user choice (called by CMP)
gtag('consent', 'update', {
  analytics_storage: 'granted',
  ad_storage: 'granted',
  ad_user_data: 'granted',
  ad_personalization: 'granted'
});
```

### Implementation Checklist

- Default consent set BEFORE GTM snippet loads?
- All four v2 signals configured?
- CMP calls `gtag('consent', 'update', ...)` on user choice?
- GTM built-in consent checks enabled?
- `wait_for_update` set (500ms recommended)?
- Consent persists across pages?
- Denied state: cookieless pings sent (`gcs=G100` in Network tab)?
- Granted state: full measurement resumes?

### BigQuery: Consent Impact Analysis

```sql
SELECT
  PARSE_DATE('%Y%m%d', event_date) as date,
  COUNT(*) as total_events,
  COUNTIF(privacy_info.analytics_storage = 'Yes') as analytics_granted,
  COUNTIF(privacy_info.analytics_storage = 'No') as analytics_denied,
  COUNTIF(privacy_info.analytics_storage IS NULL) as consent_not_set,
  COUNTIF(privacy_info.ads_storage = 'No') as ads_denied,
  ROUND(SAFE_DIVIDE(
    COUNTIF(privacy_info.analytics_storage = 'No'),
    COUNT(*)
  ) * 100, 1) as pct_analytics_denied
FROM `project.analytics_PROPERTY_ID.events_*`
WHERE _TABLE_SUFFIX BETWEEN
  FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
  AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1
ORDER BY 1 DESC
```

`privacy_info.analytics_storage` is `Yes` / `No` when Consent Mode sends a state and NULL when it
doesn't. A large `consent_not_set` share means Consent Mode isn't wired; a missing session ID or
`user_pseudo_id` is not a reliable consent signal.

## Enhanced Conversions

### What Data Is Sent

Hashed first-party customer data sent alongside conversion tags for better matching.

| Field | Format | Required |
|-------|--------|----------|
| Email | SHA-256 hashed, lowercase, trimmed | At least one of: email, phone, or name+address |
| Phone | SHA-256 hashed, E.164 format | Optional but recommended |
| First/Last name | SHA-256 hashed, lowercase | Optional |
| Address fields | SHA-256 hashed | Optional |
| Country | ISO 3166-1 alpha-2, unhashed | Optional |

### Setup via GTM (dataLayer method)

```javascript
window.dataLayer.push({
  event: 'purchase',
  user_data: {
    email: 'user@example.com',       // Auto-hashed by GTM
    phone_number: '+11234567890',
    address: {
      first_name: 'John',
      last_name: 'Doe',
      street: '123 Main St',
      city: 'New York',
      region: 'NY',
      postal_code: '10001',
      country: 'US'
    }
  },
  ecommerce: {
    transaction_id: 'T-12345',
    value: 99.99,
    currency: 'USD'
  }
});
```

### Setup via gtag.js

```javascript
gtag('set', 'user_data', {
  email: 'user@example.com',
  phone_number: '+11234567890',
  address: {
    first_name: 'John', last_name: 'Doe',
    street: '123 Main St', city: 'New York',
    region: 'NY', postal_code: '10001', country: 'US'
  }
});
```

### Validation Checklist

- Google Ads > Conversions > Diagnostics > Enhanced Conversions status = "Recording"?
- Match rate visible after 48-72h?
- GTM Preview: "User-provided data" tab shows hashed values?
- Network request contains `em=` (hashed email)?

## Server-Side Tagging

### Benefits

1. **Ad blocker resistance** -- First-party domain, not blocked
2. **Longer cookie lifetime** -- 2+ years vs 7 days (ITP)
3. **Reduced page weight** -- Fewer browser scripts
4. **Data control** -- Inspect/modify before sending to vendors
5. **Better consent** -- Single enforcement point

### Architecture

```
Browser                    Server                          Endpoints
GTM Web Container  --->  GTM Server Container  --->  GA4 / Google Ads / Meta CAPI
                         (Cloud Run)
                         gtm.yourdomain.com
```

### First-Party Domain Setup

```javascript
// GA4 Config tag: set server container URL
gtag('config', 'G-XXXXXXX', {
  server_container_url: 'https://gtm.yourdomain.com'
});
```

```
# DNS: CNAME to Cloud Run service
gtm.yourdomain.com  CNAME  your-cloud-run-service.run.app
```

## Troubleshooting Flowcharts

### Conversions Not Showing Up

```
Tag installed? --NO--> Install tag. Publish GTM container.
  |YES
  v
Tag fires in GTM Preview? --NO--> Check trigger: event name exact match?
  |YES                              Conditions met? Blocking triggers?
  v
Network request in DevTools? --NO--> Consent Mode blocking?
  |YES                                Ad blocker? CSP blocking?
  v
Request returning 200/204? --NO--> Check endpoint URL, measurement ID, credentials.
  |YES
  v
Platform-specific:
- GA4: Wait 24-48h. Check DebugView. Check data filters.
- Google Ads: Wait 24h. Check conversion action status. Is it "Primary"?
- Meta: Check Events Manager > Test Events. Check event match quality.
```

### Conversion Count Mismatch

```
Difference > 20%? --NO--> Normal variance. Document baseline.
  |YES
  v
Which platform shows MORE?
- Google Ads > GA4: Counting "every"? View-through? Longer window? Modeled?
- GA4 > Google Ads: All channels vs Google-only? Action set to Primary?
  Google Ads at 0 while GA4 > 0? Not variance: run "Google Ads = 0 but GA4 > 0".
- Meta > GA4: View-through included? iOS modeling?
- GA4 > Meta: Ad blockers? No CAPI? Low match quality?
  |
  v
Run BigQuery validation queries to get ground truth,
or compare with store orders (Shopify / WooCommerce) if connected.
```

### Conversion Value Wrong

```
Value always 0/NULL? --YES--> Check: 'value' in dataLayer? 'currency' present?
  |NO                          value is number not string? Variable mapping?
  v
Value consistently wrong? --YES--> Static value override? Currency conversion?
  |NO
  v
Value doubled? --YES--> Duplicate events. Multiple tags. Double dataLayer push.
  |NO
  v
Check: tax/shipping included? cents vs dollars? string formatting? locale?
```

## Quick Reference: dataLayer Examples

### E-Commerce Purchase

```javascript
window.dataLayer.push({ ecommerce: null });  // Clear previous
window.dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: 'T-12345',
    value: 99.99,
    tax: 8.50,
    shipping: 5.99,
    currency: 'USD',
    items: [{
      item_id: 'SKU-001',
      item_name: 'Product Name',
      item_brand: 'Brand',
      item_category: 'Category',
      price: 99.99,
      quantity: 1
    }]
  }
});
```

### Lead Generation

```javascript
window.dataLayer.push({
  event: 'generate_lead',
  value: 50.00,
  currency: 'USD',
  lead_source: 'contact_form'
});
```

### gtag.js Direct (No GTM)

```javascript
// Google Ads conversion
gtag('event', 'conversion', {
  send_to: 'AW-XXXXXXXXX/CONVERSION_LABEL',
  value: 99.99,
  currency: 'USD',
  transaction_id: 'T-12345'
});

// GA4 purchase
gtag('event', 'purchase', {
  transaction_id: 'T-12345',
  value: 99.99,
  currency: 'USD',
  items: [{ item_id: 'SKU-001', item_name: 'Product', price: 99.99, quantity: 1 }]
});
```

## Resources

- **GA4 Conversion Setup:** https://support.google.com/analytics/answer/9267568
- **Google Ads Conversion Tracking:** https://support.google.com/google-ads/answer/6095821
- **Enhanced Conversions:** https://support.google.com/google-ads/answer/9888656
- **Consent Mode:** https://developers.google.com/tag-platform/security/guides/consent
- **Meta Conversions API:** https://developers.facebook.com/docs/marketing-api/conversions-api
- **GTM Server-Side Tagging:** https://developers.google.com/tag-platform/tag-manager/server-side
- **Full Cogny Docs:** https://cogny.com/docs/conversion-tracking-debugger
