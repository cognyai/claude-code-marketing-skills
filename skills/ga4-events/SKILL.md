---
name: ga4-events
description: GA4 Event Implementation Reference — complete event taxonomy, parameter lists, implementation patterns (gtag.js, GTM, Measurement Protocol), and validation techniques
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<event name, category, or topic>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # GA4 tools (when connected via Cogny MCP)
  - mcp__cogny__google_analytics_4__tool_list_account_summaries
  - mcp__cogny__google_analytics_4__tool_get_property
  - mcp__cogny__google_analytics_4__tool_list_custom_dimensions
  - mcp__cogny__google_analytics_4__tool_list_custom_metrics
  - mcp__cogny__google_analytics_4__tool_list_conversion_events
  - mcp__cogny__google_analytics_4__tool_list_data_streams
  - mcp__cogny__google_analytics_4__tool_get_metadata
  - mcp__cogny__google_analytics_4__tool_run_report
  - mcp__cogny__google_analytics_4__tool_run_realtime_report
---

# GA4 Event Implementation Reference

Complete reference for implementing Google Analytics 4 events: automatically collected, enhanced measurement, recommended, and custom events with exact parameter lists, code examples, and validation techniques.

Full docs: https://cogny.com/docs/ga4-event-implementation

## Usage

```
/ga4-events                          # Show event model overview
/ga4-events purchase                 # Show purchase event parameters and code
/ga4-events ecommerce                # Full e-commerce event funnel reference
/ga4-events enhanced measurement     # Enhanced measurement events list
/ga4-events custom events            # Custom event naming rules and limits
/ga4-events validation               # DebugView, Realtime, and BigQuery checks
/ga4-events gtm                      # GTM dataLayer implementation patterns
/ga4-events measurement protocol     # Server-side Measurement Protocol examples
```

## Instructions

You are a GA4 event implementation expert. Use this reference to help users implement, audit, and validate GA4 events correctly. Provide precise, copy-paste-ready code examples.

When the user asks a question, find the relevant section below and provide actionable answers with ready-to-use code. If GA4 MCP tools are available, use them to inspect the user's actual property configuration (custom dimensions, data streams, conversion events) for context-aware advice.

If the user provides a specific event name or topic as an argument, focus on that area. Otherwise, provide an overview of the event model.

---

## Event Model Overview

GA4 uses an event-based data model where **everything is an event**. Unlike Universal Analytics hit types (pageview, event, transaction), GA4 has a single concept: events with parameters.

| Concept | Universal Analytics | GA4 |
|---------|-------------------|-----|
| Data model | Hit-based (pageview, event, transaction) | Event-based (everything is an event) |
| Event structure | Category / Action / Label / Value | Event name + parameters (key-value pairs) |
| Sessions | Server-defined, 30-min timeout | Derived from `session_start` event |
| Pageviews | Dedicated hit type | `page_view` event with `page_location` parameter |
| E-commerce | Enhanced Ecommerce plugin | Built-in recommended events with items array |
| Custom data | Custom dimensions/metrics (index-based) | Event parameters + custom dimensions/metrics (name-based) |

Every GA4 event has:
- **Event name**: String identifier (e.g., `page_view`, `purchase`)
- **Event parameters**: Key-value pairs (e.g., `page_location`, `transaction_id`)
- **User properties**: Persistent user attributes (e.g., `membership_tier`)

## Automatically Collected Events

Collected automatically with no configuration. Cannot be disabled.

### Web

| Event | Trigger | Key Parameters |
|-------|---------|----------------|
| `first_visit` | First time user visits (new cookie) | None |
| `session_start` | New session begins (30-min timeout) | `ga_session_id`, `ga_session_number` |
| `page_view` | Every page load (or `history.pushState` in SPAs) | `page_location`, `page_title`, `page_referrer` |
| `user_engagement` | Page in focus for 1+ second with interaction | `engagement_time_msec` |

### Mobile (Firebase SDK)

| Event | Trigger | Key Parameters |
|-------|---------|----------------|
| `first_open` | First app open after install | `previous_gmp_app_id`, `updated_with_analytics` |
| `session_start` | New session begins | `ga_session_id`, `ga_session_number` |
| `screen_view` | Screen transition | `firebase_screen`, `firebase_screen_class`, `firebase_screen_id` |
| `user_engagement` | App in foreground 1+ second | `engagement_time_msec` |
| `app_update` | App updated and launched | `previous_app_version` |
| `app_remove` | App removed (Android only) | None |
| `os_update` | OS updated | `previous_os_version` |

### Auto-attached Parameters (every event)

`language`, `page_location`, `page_referrer`, `page_title`, `screen_resolution`, `ga_session_id`, `ga_session_number`, `engagement_time_msec`

## Enhanced Measurement Events

Collected automatically when enabled in **Admin > Data Streams > Enhanced Measurement**. Each can be toggled individually.

| Event | Trigger | Key Parameters |
|-------|---------|----------------|
| `scroll` | User scrolls past 90% of page | `percent_scrolled` (always 90) |
| `click` | Outbound link click | `link_url`, `link_domain`, `link_classes`, `link_id`, `outbound` |
| `view_search_results` | URL contains search query parameter | `search_term` |
| `video_start` | YouTube embed starts playing | `video_url`, `video_title`, `video_provider`, `video_current_time`, `visible` |
| `video_progress` | YouTube video reaches 10/25/50/75% | Same as `video_start` plus `video_percent` |
| `video_complete` | YouTube video reaches end | Same as `video_start` |
| `file_download` | Click on file link (pdf, xls, doc, zip, etc.) | `file_name`, `file_extension`, `link_url`, `link_text`, `link_domain` |
| `form_start` | First interaction with a form | `form_id`, `form_name`, `form_destination` |
| `form_submit` | Form submitted | `form_id`, `form_name`, `form_destination`, `form_submit_text` |

**Note:** Video tracking only works with YouTube embeds using `enablejsapi=1`.

## Recommended Events — All Properties

| Event | Parameters |
|-------|-----------|
| `login` | `method` (STRING) |
| `sign_up` | `method` (STRING) |
| `share` | `method` (STRING), `content_type` (STRING), `item_id` (STRING) |
| `search` | `search_term` (STRING) |
| `select_content` | `content_type` (STRING), `content_id` (STRING) |

```javascript
gtag('event', 'login', { method: 'Google' });
gtag('event', 'sign_up', { method: 'Email' });
gtag('event', 'search', { search_term: 'running shoes' });
```

## Recommended Events — E-commerce

Implement in order for full funnel reporting.

### view_item_list
```javascript
gtag('event', 'view_item_list', {
  item_list_id: 'category_123',
  item_list_name: 'Running Shoes',
  items: [{
    item_id: 'SKU_123', item_name: 'Trail Runner Pro', item_brand: 'RunCo',
    item_category: 'Shoes', item_category2: 'Running', item_variant: 'Blue',
    price: 129.99, currency: 'USD', index: 0,
    item_list_id: 'category_123', item_list_name: 'Running Shoes'
  }]
});
```

### select_item
```javascript
gtag('event', 'select_item', {
  item_list_id: 'category_123', item_list_name: 'Running Shoes',
  items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', index: 0 }]
});
```

### view_item
```javascript
gtag('event', 'view_item', {
  currency: 'USD', value: 129.99,
  items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro', item_brand: 'RunCo',
    item_category: 'Shoes', item_variant: 'Blue', price: 129.99, currency: 'USD', quantity: 1 }]
});
```

### add_to_cart
```javascript
gtag('event', 'add_to_cart', {
  currency: 'USD', value: 129.99,
  items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', quantity: 1 }]
});
```

### remove_from_cart
```javascript
gtag('event', 'remove_from_cart', {
  currency: 'USD', value: 129.99,
  items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', quantity: 1 }]
});
```

### view_cart
```javascript
gtag('event', 'view_cart', {
  currency: 'USD', value: 259.98,
  items: [
    { item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', quantity: 1 },
    { item_id: 'SKU_456', item_name: 'Road Runner Elite', price: 149.99, currency: 'USD', quantity: 1 }
  ]
});
```

### begin_checkout
```javascript
gtag('event', 'begin_checkout', {
  currency: 'USD', value: 259.98, coupon: 'SUMMER20',
  items: [
    { item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', quantity: 1 },
    { item_id: 'SKU_456', item_name: 'Road Runner Elite', price: 149.99, currency: 'USD', quantity: 1 }
  ]
});
```

### add_shipping_info
```javascript
gtag('event', 'add_shipping_info', {
  currency: 'USD', value: 259.98, coupon: 'SUMMER20', shipping_tier: 'Express',
  items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', quantity: 1 }]
});
```

### add_payment_info
```javascript
gtag('event', 'add_payment_info', {
  currency: 'USD', value: 259.98, coupon: 'SUMMER20', payment_type: 'Credit Card',
  items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro', price: 129.99, currency: 'USD', quantity: 1 }]
});
```

### purchase
```javascript
gtag('event', 'purchase', {
  transaction_id: 'T12345',  // REQUIRED — unique transaction ID
  value: 259.98,             // REQUIRED — total value
  currency: 'USD',           // REQUIRED — ISO 4217
  tax: 20.80,
  shipping: 9.99,
  coupon: 'SUMMER20',
  items: [
    { item_id: 'SKU_123', item_name: 'Trail Runner Pro', affiliation: 'Online Store',
      coupon: 'ITEM10OFF', discount: 13.00, item_brand: 'RunCo', item_category: 'Shoes',
      item_category2: 'Running', item_variant: 'Blue', price: 129.99, currency: 'USD', quantity: 1 },
    { item_id: 'SKU_456', item_name: 'Road Runner Elite', affiliation: 'Online Store',
      item_brand: 'RunCo', item_category: 'Shoes', price: 149.99, currency: 'USD', quantity: 1 }
  ]
});
```

**Critical:** `purchase` requires `transaction_id`, `value`, and `currency`. GA4 deduplicates by `transaction_id` within 72 hours.

### refund
```javascript
// Full refund
gtag('event', 'refund', { transaction_id: 'T12345', value: 259.98, currency: 'USD' });

// Partial refund
gtag('event', 'refund', {
  transaction_id: 'T12345', value: 129.99, currency: 'USD',
  items: [{ item_id: 'SKU_123', price: 129.99, currency: 'USD', quantity: 1 }]
});
```

## Recommended Events — Lead Generation

### generate_lead
```javascript
gtag('event', 'generate_lead', { currency: 'USD', value: 50.00 });
```

## Recommended Events — Gaming

| Event | Parameters |
|-------|-----------|
| `earn_virtual_currency` | `virtual_currency_name` (STRING), `value` (NUMBER) |
| `spend_virtual_currency` | `virtual_currency_name` (STRING), `value` (NUMBER), `item_name` (STRING) |
| `level_up` | `level` (NUMBER), `character` (STRING) |
| `post_score` | `score` (NUMBER, required), `level` (NUMBER), `character` (STRING) |
| `tutorial_begin` | None |
| `tutorial_complete` | None |
| `unlock_achievement` | `achievement_id` (STRING, required) |

```javascript
gtag('event', 'earn_virtual_currency', { virtual_currency_name: 'Coins', value: 100 });
gtag('event', 'spend_virtual_currency', { virtual_currency_name: 'Coins', value: 50, item_name: 'Power Boost' });
gtag('event', 'level_up', { level: 5, character: 'Warrior' });
gtag('event', 'post_score', { score: 15000, level: 5, character: 'Warrior' });
gtag('event', 'tutorial_begin');
gtag('event', 'tutorial_complete');
gtag('event', 'unlock_achievement', { achievement_id: 'first_blood' });
```

## Item Parameter Reference

The `items` array supports these parameters per item:

| Parameter | Type | Description |
|-----------|------|-------------|
| `item_id` | STRING | SKU/ID (recommended) |
| `item_name` | STRING | Display name (recommended) |
| `affiliation` | STRING | Store or affiliation |
| `coupon` | STRING | Item-level coupon |
| `discount` | NUMBER | Discount amount |
| `index` | NUMBER | Position in list |
| `item_brand` | STRING | Brand name |
| `item_category` | STRING | Primary category |
| `item_category2`-`5` | STRING | Category levels 2-5 |
| `item_list_id` | STRING | List ID |
| `item_list_name` | STRING | List name |
| `item_variant` | STRING | Variant (color, size) |
| `location_id` | STRING | Physical location |
| `price` | NUMBER | Item price |
| `currency` | STRING | ISO 4217 code |
| `quantity` | NUMBER | Quantity |
| `promotion_id` | STRING | Promotion ID |
| `promotion_name` | STRING | Promotion name |
| `creative_name` | STRING | Promotion creative |
| `creative_slot` | STRING | Creative slot |

At least one of `item_id` or `item_name` is required. Max 200 items per event.

## Custom Events

Use when no automatically collected, enhanced measurement, or recommended event fits.

### Naming Rules

- Max **40 characters**
- Must start with alphabetic character
- Only `[a-zA-Z][a-zA-Z0-9_]*`
- **Case sensitive** — `Add_To_Cart` and `add_to_cart` are different events
- Cannot use reserved prefixes: `firebase_`, `google_`, `ga_`
- Cannot use reserved event names (e.g., `first_visit`, `session_start`, `app_install`, `in_app_purchase`, etc.)

### Limits

| Limit | Value |
|-------|-------|
| Unique event names per property | 500 |
| Parameters per event | 25 |
| Parameter name length | 40 characters |
| Parameter value (string) | 100 characters |
| User property name length | 24 characters |
| User property value (string) | 36 characters |
| User properties per project | 25 |

### Examples

```javascript
gtag('event', 'newsletter_signup', {
  newsletter_type: 'weekly_digest', signup_location: 'footer'
});

gtag('event', 'feature_used', {
  feature_name: 'export_csv', feature_category: 'data_tools', plan_tier: 'pro'
});

gtag('event', 'article_read', {
  article_id: 'post_12345', article_category: 'technology', read_time_seconds: 245
});
```

## Custom Dimensions and Metrics

Register event parameters or user properties for reporting in **Admin > Custom definitions**.

### Scoping

| Scope | Source | Use Case |
|-------|--------|----------|
| Event-scoped dimension | Event parameter | Page/action attributes |
| User-scoped dimension | User property | Persistent user attributes |
| Custom metric | Event parameter (numeric) | Numeric aggregation |

### Quotas

| Resource | Standard | Analytics 360 |
|----------|----------|---------------|
| Event-scoped custom dimensions | 50 | 125 |
| User-scoped custom dimensions | 25 | 100 |
| Custom metrics | 50 | 125 |

Processing time: 24-48 hours for standard reports (immediate in Realtime/DebugView).

```javascript
// Set user properties
gtag('set', 'user_properties', {
  membership_tier: 'gold', signup_date: '2025-01-15'
});
```

## GTM dataLayer Implementation

```javascript
// Custom event
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  event: 'newsletter_signup',
  newsletter_type: 'weekly_digest',
  signup_location: 'footer'
});

// E-commerce — ALWAYS clear ecommerce first
window.dataLayer.push({ ecommerce: null });
window.dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: 'T12345', value: 259.98, currency: 'USD',
    tax: 20.80, shipping: 9.99, coupon: 'SUMMER20',
    items: [{ item_id: 'SKU_123', item_name: 'Trail Runner Pro',
      item_brand: 'RunCo', item_category: 'Shoes', price: 129.99, quantity: 1 }]
  }
});
```

## Measurement Protocol (Server-Side)

```bash
POST https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET

{
  "client_id": "abc123.def456",
  "events": [{
    "name": "offline_purchase",
    "params": {
      "transaction_id": "OFFLINE_T789",
      "value": 250.00,
      "currency": "USD"
    }
  }]
}
```

```python
import requests, json

url = 'https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET'
payload = {
    'client_id': 'abc123.def456',
    'events': [{'name': 'offline_purchase', 'params': {
        'transaction_id': 'OFFLINE_T789', 'value': 250.00, 'currency': 'USD'
    }}]
}
response = requests.post(url, data=json.dumps(payload))
```

**Limitations:** No response validation (use debug endpoint), `client_id` must match existing GA4 cookie, events not in Realtime (30-min delay), cannot trigger `first_visit`/`session_start`.

### Validation Server

```bash
POST https://www.google-analytics.com/debug/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_API_SECRET
# Returns validation errors instead of silently accepting
```

## Validation and Debugging

### DebugView

Enable debug mode to see events in near real-time in **Admin > DebugView**:

```javascript
gtag('config', 'G-XXXXXXXXXX', { debug_mode: true });
// Or per-event:
gtag('event', 'purchase', { debug_mode: true, transaction_id: 'T12345', value: 99.99, currency: 'USD' });
```

### BigQuery Validation Queries

**Event volume audit:**
```sql
SELECT event_name, COUNT(*) as event_count, COUNT(DISTINCT user_pseudo_id) as unique_users
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY event_name ORDER BY event_count DESC
```

**Missing purchase parameters:**
```sql
SELECT 'missing_transaction_id' as issue, COUNT(*) as count
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'purchase'
  AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') IS NULL
UNION ALL
SELECT 'missing_currency', COUNT(*)
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'purchase'
  AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'currency') IS NULL
```

**Duplicate transactions:**
```sql
SELECT transaction_id, COUNT(*) as dupes
FROM (
  SELECT (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND event_name = 'purchase'
)
WHERE transaction_id IS NOT NULL
GROUP BY transaction_id HAVING COUNT(*) > 1
ORDER BY dupes DESC
```

**Naming convention audit:**
```sql
SELECT event_name, COUNT(*) as event_count,
  CASE
    WHEN LENGTH(event_name) > 40 THEN 'exceeds_40_chars'
    WHEN REGEXP_CONTAINS(event_name, r'^(firebase_|google_|ga_)') THEN 'reserved_prefix'
    WHEN NOT REGEXP_CONTAINS(event_name, r'^[a-zA-Z][a-zA-Z0-9_]*$') THEN 'invalid_characters'
    WHEN event_name != LOWER(event_name) THEN 'mixed_case_warning'
    ELSE 'valid'
  END as naming_issue
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY event_name HAVING naming_issue != 'valid'
```

**Parameter truncation check:**
```sql
SELECT event_name, ep.key, MAX(LENGTH(ep.value.string_value)) as max_len,
  COUNTIF(LENGTH(ep.value.string_value) >= 100) as at_limit
FROM `project.analytics_123456789.events_*`, UNNEST(event_params) as ep
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND ep.value.string_value IS NOT NULL
GROUP BY 1, 2 HAVING max_len >= 100
```

## Common Pitfalls

1. **Case sensitivity** — `Purchase` != `purchase`. Always use `snake_case`.
2. **String truncation at 100 chars** — URLs and long values get silently cut.
3. **Custom dimension quotas** — 50 event-scoped, 25 user-scoped (standard). Plan carefully.
4. **Duplicate purchases** — Always include `transaction_id` for dedup (72-hour window).
5. **Missing currency** — `value` without `currency` is ignored in monetization reports.
6. **Stale dataLayer** — Always push `{ ecommerce: null }` before ecommerce events in GTM.
7. **PII in parameters** — No emails, phone numbers, or names. Violates GA4 ToS.
8. **Dynamic event names** — Burns through the 500-name limit. Use parameters instead.

## Resources

- **GA4 Event Reference:** https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- **Recommended Events:** https://support.google.com/analytics/answer/9267735
- **Measurement Protocol:** https://developers.google.com/analytics/devguides/collection/protocol/ga4
- **Enhanced Measurement:** https://support.google.com/analytics/answer/9216061
- **Event Limits & Quotas:** https://support.google.com/analytics/answer/9267744
- **Full Cogny Docs:** https://cogny.com/docs/ga4-event-implementation
