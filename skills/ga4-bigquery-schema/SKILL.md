---
name: ga4-bigquery-schema
description: GA4 BigQuery Export Schema Reference — complete field reference, nested structures, query patterns, and performance tips
version: "1.1.1"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<query or topic>"
allowed-tools:
  - WebSearch
  - Read
  - Write
  - Bash
  # Enhanced when connected via Cogny MCP (read-only)
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_datasets
  - mcp__cogny__list_tables
  - mcp__cogny__inspect_schema
  - mcp__cogny__execute_bigquery_sql
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
---

# GA4 BigQuery Export Schema Reference

Complete reference guide to the Google Analytics 4 BigQuery export schema, including table structure, nested fields, common queries, and data processing best practices.

Full docs: https://cogny.com/docs/ga4-bigquery-export-schema

## Usage

```
/ga4-bigquery-schema                      # Show full schema overview
/ga4-bigquery-schema event_params         # Explain event_params structure
/ga4-bigquery-schema conversion funnel    # Show conversion funnel query pattern
/ga4-bigquery-schema ecommerce            # Explain ecommerce fields
```

## Instructions

You are a GA4 BigQuery schema expert. Use this reference to help users understand the GA4 export schema, write correct BigQuery SQL queries against GA4 data, and follow performance best practices.

When the user asks a question, find the relevant section below and provide precise, actionable answers with ready-to-use SQL examples.

If the user provides a specific topic as an argument, focus on that area. Otherwise, provide an overview of the schema structure.

## Works with

Works with zero accounts: every query below is copy-paste SQL. When connected:

| Job | Solo / no account | Cogny Cloud | Plus GA4 connected |
|-----|-------------------|-------------|--------------------|
| Find the export dataset | user supplies `project.analytics_ID` | `list_datasets` → `list_tables` | — |
| Check the real schema | the reference below | `inspect_schema` | — |
| Run a query | user runs it | `execute_bigquery_sql` (read-only SELECTs) | — |
| Reconcile export vs UI | — | `execute_bigquery_sql` | `tool_run_report` (same dates) |

BigQuery tools are Cloud-only (section 2 of `../marketing-engineer/references/mcp-routing.md`).
On Solo, give the SQL and stop.

### Run it on the user's data (Cloud)

If Cogny isn't connected, skip this and note what connecting adds.

1. `list_datasets`, pick the one named `analytics_<property id>`; `list_tables` to confirm
   daily `events_*` tables exist (and `events_intraday_*` if streaming is on).
2. `inspect_schema` on one daily table before writing SQL; custom `event_params` keys and
   `user_properties` vary per property.
3. Swap `project.analytics_123456789` in the chosen query for the real path, keep the
   `_TABLE_SUFFIX` filter, then `execute_bigquery_sql`.
4. **Reconcile** (GA4 connected): run `tool_run_report` (`property_id`, same `date_ranges`,
   `metrics: [eventCount, totalUsers]`, `dimensions: [eventName]`) next to the export
   count. A gap under ~2% is normal (late hits, thresholding); a larger one, or users far
   apart, usually means consent mode modelling in the UI or a broken export day (see Data
   Quality Checks). Name the source on every number.

---

## Overview

Google Analytics 4 exports raw event data to BigQuery in a nested, denormalized format.

**Daily Tables:** `analytics_PROPERTY_ID.events_YYYYMMDD`
**Intraday Tables:** `analytics_PROPERTY_ID.events_intraday_YYYYMMDD`

Each row represents a single event with nested fields for event parameters, user properties, and e-commerce data.

```sql
-- View table schema
SELECT
  column_name,
  data_type,
  description
FROM `project.analytics_123456789.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name LIKE 'events_%'
ORDER BY ordinal_position
```

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `event_date` | STRING | Date when the event was logged (YYYYMMDD format) |
| `event_timestamp` | INTEGER | Time when the event was logged (microseconds since Unix epoch) |
| `event_name` | STRING | Name of the event (e.g., 'page_view', 'purchase') |
| `event_params` | ARRAY\<STRUCT\> | Array of event parameters |
| `event_previous_timestamp` | INTEGER | Timestamp of previous event by this user |
| `event_value_in_usd` | FLOAT | Value of the event in USD |
| `event_bundle_sequence_id` | INTEGER | Sequential ID of the event bundle |
| `event_server_timestamp_offset` | INTEGER | Timestamp offset between collection and server |
| `user_id` | STRING | User ID set via setUserId API |
| `user_pseudo_id` | STRING | Pseudonymous ID for the user (cookie-based) |
| `user_properties` | ARRAY\<STRUCT\> | Array of user properties |
| `user_first_touch_timestamp` | INTEGER | First time user visited (microseconds) |
| `user_ltv` | STRUCT | User lifetime value information |
| `device` | STRUCT | Device information |
| `geo` | STRUCT | Geographic information |
| `app_info` | STRUCT | App information (mobile apps) |
| `traffic_source` | STRUCT | First-touch source that acquired the **user** (never changes) |
| `collected_traffic_source` | STRUCT | UTMs / click IDs collected on **this event** |
| `session_traffic_source_last_click` | STRUCT | Last-click attributed **session** source (manual, Google Ads, CM360, DV360, SA360) |
| `stream_id` | STRING | Numeric ID of the data stream |
| `platform` | STRING | Platform (web, ios, android) |
| `ecommerce` | STRUCT | E-commerce transaction data |
| `items` | ARRAY\<STRUCT\> | Array of item (product) details |

## Nested Structures

### event_params

Event parameters stored as key-value pairs:

```sql
STRUCT<
  key STRING,
  value STRUCT<
    string_value STRING,
    int_value INT64,
    float_value FLOAT64,
    double_value FLOAT64
  >
>
```

**Common event parameters:**

| Key | Type | Description |
|-----|------|-------------|
| `page_location` | string | Full URL of the page |
| `page_title` | string | Title of the page |
| `page_referrer` | string | Referrer URL |
| `engagement_time_msec` | int | Engagement time in milliseconds |
| `session_engaged` | int | Whether session was engaged (1/0) |
| `ga_session_id` | int | Session ID |
| `ga_session_number` | int | Session number for user |

**Example — extract event params:**

```sql
SELECT
  event_name,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') as page_location,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_title') as page_title,
  (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'engagement_time_msec') as engagement_time
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'page_view'
LIMIT 100
```

### user_properties

User properties stored as key-value pairs:

```sql
STRUCT<
  key STRING,
  value STRUCT<
    string_value STRING,
    int_value INT64,
    float_value FLOAT64,
    double_value FLOAT64,
    set_timestamp_micros INT64
  >
>
```

**Example — extract user properties:**

```sql
SELECT
  user_pseudo_id,
  (SELECT value.string_value FROM UNNEST(user_properties) WHERE key = 'user_type') as user_type,
  (SELECT value.string_value FROM UNNEST(user_properties) WHERE key = 'plan_level') as plan_level
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY user_pseudo_id, user_type, plan_level
LIMIT 100
```

### device

```sql
STRUCT<
  category STRING,              -- desktop, mobile, tablet
  mobile_brand_name STRING,     -- Apple, Samsung, etc.
  mobile_model_name STRING,     -- iPhone 12, Galaxy S21, etc.
  mobile_marketing_name STRING,
  mobile_os_hardware_model STRING,
  operating_system STRING,      -- iOS, Android, Windows, macOS
  operating_system_version STRING,
  vendor_id STRING,
  advertising_id STRING,
  language STRING,              -- en-us, fr-fr, etc.
  is_limited_ad_tracking STRING,
  time_zone_offset_seconds INT64,
  browser STRING,               -- Chrome, Safari, Firefox
  browser_version STRING,
  web_info STRUCT<
    browser STRING,
    browser_version STRING,
    hostname STRING
  >
>
```

**Example — device breakdown:**

```sql
SELECT
  device.category as device_category,
  device.operating_system,
  device.browser,
  COUNT(*) as event_count,
  COUNT(DISTINCT user_pseudo_id) as users
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1, 2, 3
ORDER BY event_count DESC
```

### geo

```sql
STRUCT<
  continent STRING,     -- Americas, Europe, Asia, etc.
  sub_continent STRING, -- Northern Europe, Western Asia, etc.
  country STRING,       -- United States, United Kingdom, etc.
  region STRING,        -- California, England, etc.
  metro STRING,         -- Metro area
  city STRING
>
```

**Example — geographic breakdown:**

```sql
SELECT
  geo.country,
  geo.city,
  COUNT(DISTINCT user_pseudo_id) as users,
  COUNT(*) as events
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1, 2
ORDER BY users DESC
LIMIT 100
```

### traffic_source

`traffic_source` is the source that **first acquired the user**. It doesn't change on later
visits and isn't populated in intraday tables. Use it for user acquisition, never for
session or campaign attribution.

```sql
STRUCT<
  name STRING,   -- First-touch campaign name
  medium STRING, -- First-touch medium (organic, cpc, referral, etc.)
  source STRING  -- First-touch source (google, facebook.com, etc.)
>
```

For session attribution use:

- `collected_traffic_source` — what was on the event itself: `manual_source`,
  `manual_medium`, `manual_campaign_name`, `manual_term`, `manual_content`,
  `manual_campaign_id`, `gclid`, `dclid`, `srsltid`.
- `session_traffic_source_last_click` — GA4's last-click session attribution:
  `manual_campaign.{source, medium, campaign_name, ...}`,
  `google_ads_campaign.{customer_id, campaign_id, campaign_name, ad_group_name, ...}`,
  `cross_channel_campaign.{source, medium, campaign_name, ...}`.

```sql
-- Sessions by last-click session source/medium
SELECT
  session_traffic_source_last_click.cross_channel_campaign.source AS source,
  session_traffic_source_last_click.cross_channel_campaign.medium AS medium,
  COUNT(DISTINCT CONCAT(user_pseudo_id, '-',
    CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING))) AS sessions
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'session_start'
GROUP BY 1, 2
ORDER BY sessions DESC
```

**Example — first-touch (user acquisition) performance:**

```sql
SELECT
  traffic_source.source,
  traffic_source.medium,
  COUNT(DISTINCT user_pseudo_id) as users,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) as purchasers,
  SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END),
    COUNT(DISTINCT user_pseudo_id)
  ) as conversion_rate
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1, 2
ORDER BY users DESC
```

### ecommerce

```sql
STRUCT<
  total_item_quantity INT64,
  purchase_revenue_in_usd FLOAT64,
  purchase_revenue FLOAT64,
  refund_value_in_usd FLOAT64,
  refund_value FLOAT64,
  shipping_value_in_usd FLOAT64,
  shipping_value FLOAT64,
  tax_value_in_usd FLOAT64,
  tax_value FLOAT64,
  unique_items INT64,
  transaction_id STRING
>
```

**Example — revenue analysis:**

```sql
SELECT
  DATE(TIMESTAMP_MICROS(event_timestamp)) as date,
  COUNT(DISTINCT ecommerce.transaction_id) as transactions,
  SUM(ecommerce.purchase_revenue_in_usd) as revenue,
  AVG(ecommerce.purchase_revenue_in_usd) as avg_order_value
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'purchase'
  AND ecommerce.transaction_id IS NOT NULL
GROUP BY 1
ORDER BY 1 DESC
```

### items

```sql
STRUCT<
  item_id STRING,
  item_name STRING,
  item_brand STRING,
  item_variant STRING,
  item_category STRING,
  item_category2 STRING,
  item_category3 STRING,
  item_category4 STRING,
  item_category5 STRING,
  price_in_usd FLOAT64,
  price FLOAT64,
  quantity INT64,
  item_revenue_in_usd FLOAT64,
  item_revenue FLOAT64,
  item_refund_in_usd FLOAT64,
  item_refund FLOAT64,
  coupon STRING,
  affiliation STRING,
  location_id STRING,
  item_list_id STRING,
  item_list_name STRING,
  item_list_index STRING,
  promotion_id STRING,
  promotion_name STRING,
  creative_name STRING,
  creative_slot STRING
>
```

**Example — product performance:**

```sql
SELECT
  item.item_name,
  item.item_category,
  SUM(item.quantity) as total_quantity,
  SUM(item.item_revenue_in_usd) as total_revenue,
  COUNT(DISTINCT ecommerce.transaction_id) as transactions
FROM `project.analytics_123456789.events_*`,
  UNNEST(items) as item
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'purchase'
GROUP BY 1, 2
ORDER BY total_revenue DESC
LIMIT 100
```

## Common Query Patterns

### Sessions and Users

```sql
SELECT
  DATE(TIMESTAMP_MICROS(event_timestamp)) as date,
  COUNT(DISTINCT user_pseudo_id) as users,
  COUNT(DISTINCT CONCAT(user_pseudo_id, '-',
    CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING)))) as sessions,
  SAFE_DIVIDE(
    COUNT(DISTINCT CONCAT(user_pseudo_id, '-',
      CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING)))),
    COUNT(DISTINCT user_pseudo_id)
  ) as sessions_per_user
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1
ORDER BY 1 DESC
```

### Page Views

```sql
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') as page_location,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_title') as page_title,
  COUNT(*) as page_views,
  COUNT(DISTINCT user_pseudo_id) as unique_users,
  AVG((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'engagement_time_msec')) / 1000 as avg_engagement_seconds
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'page_view'
GROUP BY 1, 2
ORDER BY page_views DESC
LIMIT 100
```

### Conversion Funnel

```sql
WITH funnel_steps AS (
  SELECT
    user_pseudo_id,
    COUNTIF(event_name = 'page_view') as step_1_landing,
    COUNTIF(event_name = 'view_item') as step_2_product_view,
    COUNTIF(event_name = 'add_to_cart') as step_3_add_to_cart,
    COUNTIF(event_name = 'begin_checkout') as step_4_checkout,
    COUNTIF(event_name = 'purchase') as step_5_purchase
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  GROUP BY user_pseudo_id
)

SELECT
  'Landing' as step, 1 as step_number,
  COUNT(DISTINCT CASE WHEN step_1_landing > 0 THEN user_pseudo_id END) as users,
  1.0 as conversion_rate
FROM funnel_steps
UNION ALL
SELECT 'Product View', 2,
  COUNT(DISTINCT CASE WHEN step_2_product_view > 0 THEN user_pseudo_id END),
  SAFE_DIVIDE(COUNT(DISTINCT CASE WHEN step_2_product_view > 0 THEN user_pseudo_id END),
              COUNT(DISTINCT CASE WHEN step_1_landing > 0 THEN user_pseudo_id END))
FROM funnel_steps
UNION ALL
SELECT 'Add to Cart', 3,
  COUNT(DISTINCT CASE WHEN step_3_add_to_cart > 0 THEN user_pseudo_id END),
  SAFE_DIVIDE(COUNT(DISTINCT CASE WHEN step_3_add_to_cart > 0 THEN user_pseudo_id END),
              COUNT(DISTINCT CASE WHEN step_2_product_view > 0 THEN user_pseudo_id END))
FROM funnel_steps
UNION ALL
SELECT 'Checkout', 4,
  COUNT(DISTINCT CASE WHEN step_4_checkout > 0 THEN user_pseudo_id END),
  SAFE_DIVIDE(COUNT(DISTINCT CASE WHEN step_4_checkout > 0 THEN user_pseudo_id END),
              COUNT(DISTINCT CASE WHEN step_3_add_to_cart > 0 THEN user_pseudo_id END))
FROM funnel_steps
UNION ALL
SELECT 'Purchase', 5,
  COUNT(DISTINCT CASE WHEN step_5_purchase > 0 THEN user_pseudo_id END),
  SAFE_DIVIDE(COUNT(DISTINCT CASE WHEN step_5_purchase > 0 THEN user_pseudo_id END),
              COUNT(DISTINCT CASE WHEN step_4_checkout > 0 THEN user_pseudo_id END))
FROM funnel_steps
ORDER BY step_number
```

### User Acquisition

```sql
WITH first_visit AS (
  SELECT
    user_pseudo_id,
    MIN(event_timestamp) as first_visit_timestamp,
    ARRAY_AGG(
      STRUCT(traffic_source.source, traffic_source.medium, traffic_source.name)
      ORDER BY event_timestamp LIMIT 1
    )[OFFSET(0)] as first_traffic_source
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND event_name = 'first_visit'
  GROUP BY user_pseudo_id
)

SELECT
  first_traffic_source.source as acquisition_source,
  first_traffic_source.medium as acquisition_medium,
  COUNT(DISTINCT user_pseudo_id) as new_users,
  COUNT(DISTINCT CASE WHEN purchase_count > 0 THEN user_pseudo_id END) as purchasers,
  SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN purchase_count > 0 THEN user_pseudo_id END),
    COUNT(DISTINCT user_pseudo_id)
  ) as conversion_rate
FROM first_visit
LEFT JOIN (
  SELECT user_pseudo_id, COUNT(*) as purchase_count
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND event_name = 'purchase'
  GROUP BY user_pseudo_id
) purchases USING(user_pseudo_id)
GROUP BY 1, 2
ORDER BY new_users DESC
```

### Cohort Retention

```sql
WITH cohorts AS (
  SELECT
    user_pseudo_id,
    DATE(TIMESTAMP_MICROS(MIN(user_first_touch_timestamp))) as cohort_date
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  GROUP BY user_pseudo_id
),
-- Size each cohort BEFORE joining activity; counting inside the join only sees
-- users who were active on that day, which makes retention ~100%.
cohort_sizes AS (
  SELECT cohort_date, COUNT(*) as cohort_size
  FROM cohorts
  GROUP BY cohort_date
),
user_activity AS (
  SELECT user_pseudo_id, DATE(TIMESTAMP_MICROS(event_timestamp)) as activity_date
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  GROUP BY user_pseudo_id, activity_date
)

SELECT
  c.cohort_date,
  DATE_DIFF(a.activity_date, c.cohort_date, DAY) as days_since_cohort,
  s.cohort_size,
  COUNT(DISTINCT a.user_pseudo_id) as active_users,
  SAFE_DIVIDE(COUNT(DISTINCT a.user_pseudo_id), s.cohort_size) as retention_rate
FROM cohorts c
JOIN user_activity a USING(user_pseudo_id)
JOIN cohort_sizes s USING(cohort_date)
WHERE DATE_DIFF(a.activity_date, c.cohort_date, DAY) IN (0, 1, 7, 14, 30, 60, 90)
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 2
```

## Performance Best Practices

### Table pruning — always use _TABLE_SUFFIX

```sql
-- GOOD: only scans the daily tables in range
WHERE _TABLE_SUFFIX BETWEEN '20250101' AND '20250131'

-- BAD: scans every daily table
WHERE event_date BETWEEN '20250101' AND '20250131'
```

### Clustering — the export tables aren't clustered

The daily `events_YYYYMMDD` tables are date-sharded and, as exported, not partitioned or
clustered, so an `event_name` filter doesn't cut bytes scanned. Cost comes from the
`_TABLE_SUFFIX` range and the columns you select. Check a property with:

```sql
SELECT column_name, clustering_ordinal_position
FROM `project.analytics_123456789.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'events_20250101' AND clustering_ordinal_position IS NOT NULL
```

For heavy reuse, copy into your own table with `PARTITION BY` / `CLUSTER BY event_name`
(see below).

### Pre-aggregated summary table (scheduled query)

A materialized view won't work here: BigQuery materialized views don't allow
non-deterministic functions like `CURRENT_DATE()`, don't support `COUNT(DISTINCT)`
(only `APPROX_COUNT_DISTINCT`), and can't sit on the `events_*` wildcard. Build a regular
table instead and refresh it with a **scheduled query** (BigQuery > Scheduled queries,
daily, after the export lands). Write it to your own dataset, not the export dataset.

```sql
-- One-off backfill; schedule the same SELECT for yesterday with "append to table"
CREATE OR REPLACE TABLE `project.reporting.ga4_daily_summary`
PARTITION BY event_date_d
CLUSTER BY source, medium
AS
SELECT
  PARSE_DATE('%Y%m%d', event_date) as event_date_d,
  session_traffic_source_last_click.cross_channel_campaign.source as source,
  session_traffic_source_last_click.cross_channel_campaign.medium as medium,
  device.category,
  COUNT(DISTINCT user_pseudo_id) as users,
  COUNT(*) as events,
  COUNTIF(event_name = 'purchase') as purchases,
  SUM(CASE WHEN event_name = 'purchase' THEN ecommerce.purchase_revenue_in_usd END) as revenue
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1, 2, 3, 4
```

## Data Quality Checks

### Check for missing export dates

```sql
WITH date_range AS (
  SELECT date
  FROM UNNEST(GENERATE_DATE_ARRAY(DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), CURRENT_DATE() - 1)) as date
),
exported_dates AS (
  SELECT DISTINCT PARSE_DATE('%Y%m%d', _TABLE_SUFFIX) as date
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
)
SELECT dr.date, 'Missing' as status
FROM date_range dr
LEFT JOIN exported_dates ed USING(date)
WHERE ed.date IS NULL
ORDER BY dr.date DESC
```

### Validate event count consistency

```sql
WITH daily_counts AS (
  SELECT
    DATE(TIMESTAMP_MICROS(event_timestamp)) as date,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_pseudo_id) as user_count
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  GROUP BY 1
)
SELECT
  date, event_count, user_count,
  AVG(event_count) OVER (ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) as avg_7day,
  event_count / NULLIF(AVG(event_count) OVER (ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING), 0) as variance_ratio
FROM daily_counts
ORDER BY date DESC
```

## Resources

- **GA4 BigQuery Export Schema:** https://support.google.com/analytics/answer/7029846
- **BigQuery Best Practices:** https://cloud.google.com/bigquery/docs/best-practices
- **GA4 Event Reference:** https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- **Full Cogny Docs:** https://cogny.com/docs/ga4-bigquery-export-schema
