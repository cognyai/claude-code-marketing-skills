---
name: ga4-bigquery-schema
description: GA4 BigQuery Export Schema Reference — complete field reference, nested structures, query patterns, and performance tips
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<query or topic>"
allowed-tools:
  - WebSearch
  - Read
  - Write
  - Bash
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
| `traffic_source` | STRUCT | Traffic source information |
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

```sql
STRUCT<
  name STRING,   -- Traffic source name (google, facebook, etc.)
  medium STRING, -- Traffic medium (organic, cpc, referral, etc.)
  source STRING  -- Traffic source (google, facebook.com, etc.)
>
```

**Example — traffic source performance:**

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
  COUNT(DISTINCT CONCAT(user_pseudo_id,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'))) as sessions,
  SAFE_DIVIDE(
    COUNT(DISTINCT CONCAT(user_pseudo_id,
      (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'))),
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
user_activity AS (
  SELECT user_pseudo_id, DATE(TIMESTAMP_MICROS(event_timestamp)) as activity_date
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  GROUP BY user_pseudo_id, activity_date
)

SELECT
  cohort_date,
  DATE_DIFF(activity_date, cohort_date, DAY) as days_since_cohort,
  COUNT(DISTINCT c.user_pseudo_id) as cohort_size,
  COUNT(DISTINCT a.user_pseudo_id) as active_users,
  SAFE_DIVIDE(COUNT(DISTINCT a.user_pseudo_id), COUNT(DISTINCT c.user_pseudo_id)) as retention_rate
FROM cohorts c
LEFT JOIN user_activity a USING(user_pseudo_id)
WHERE DATE_DIFF(activity_date, cohort_date, DAY) IN (0, 1, 7, 14, 30, 60, 90)
GROUP BY 1, 2
ORDER BY 1 DESC, 2
```

## Performance Best Practices

### Partition Pruning — always use _TABLE_SUFFIX

```sql
-- GOOD: Uses partition pruning
WHERE _TABLE_SUFFIX BETWEEN '20250101' AND '20250131'

-- BAD: Scans all partitions
WHERE event_date BETWEEN '20250101' AND '20250131'
```

### Clustering — filter by event_name

GA4 tables are clustered by `event_name`. Always include an `event_name` filter when possible.

### Materialized Views

Create materialized views for frequently accessed aggregations:

```sql
CREATE MATERIALIZED VIEW `project.analytics_123456789.daily_summary`
AS
SELECT
  event_date,
  traffic_source.source,
  traffic_source.medium,
  device.category,
  COUNT(DISTINCT user_pseudo_id) as users,
  COUNT(*) as events,
  COUNTIF(event_name = 'purchase') as purchases,
  SUM(CASE WHEN event_name = 'purchase' THEN ecommerce.purchase_revenue_in_usd END) as revenue
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY))
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
