---
name: utm-builder
description: UTM Parameter Strategy & Builder — naming conventions, GA4 channel grouping rules, auto-tagging, common mistakes, and BigQuery validation queries
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
  # GA4 tools (when connected via Cogny MCP)
  - mcp__cogny__google_analytics_4__tool_run_report
  - mcp__cogny__google_analytics_4__tool_get_property
  - mcp__cogny__google_analytics_4__tool_list_data_streams
  # Google Ads tools
  - mcp__cogny__google_ads__tool_execute_gaql
---

# UTM Parameter Strategy & Builder Reference

Complete guide to UTM parameter strategy, naming conventions, GA4 default channel grouping rules, auto-tagging behavior, common mistakes, and BigQuery validation queries for marketing attribution.

Full docs: https://cogny.com/docs/utm-strategy

## Usage

```
/utm-builder                          # Full UTM strategy overview
/utm-builder naming conventions       # Show naming convention rules
/utm-builder channel grouping         # GA4 default channel grouping rules
/utm-builder meta ads                 # Meta Ads UTM template
/utm-builder audit                    # BigQuery validation queries
/utm-builder build google cpc         # Generate UTM URL for Google Ads
```

## Instructions

You are a UTM strategy and marketing attribution expert. Use this reference to help users build correct UTM URLs, audit existing UTM naming conventions, understand GA4 default channel grouping rules, and validate attribution data in BigQuery.

When the user asks a question, find the relevant section below and provide precise, actionable answers. When building UTM URLs, always enforce lowercase and hyphen-separated naming conventions.

If the user provides a specific topic as an argument, focus on that area. Otherwise, provide an overview of UTM strategy fundamentals.

When connected to Cogny MCP tools, you can pull live GA4 data and Google Ads data to audit real UTM implementations.

---

## The Five UTM Parameters

| Parameter | Required | Purpose | Example |
|-----------|----------|---------|---------|
| `utm_source` | Yes | Platform or publisher sending traffic | `google`, `facebook`, `linkedin`, `newsletter` |
| `utm_medium` | Yes | Marketing channel type | `cpc`, `paid-social`, `email`, `organic-social` |
| `utm_campaign` | Yes | Specific campaign name | `spring-sale-2025`, `brand-awareness-q1` |
| `utm_term` | No | Paid search keywords | `running+shoes`, `crm+software` |
| `utm_content` | No | Creative variant or link placement | `hero-banner`, `sidebar-cta`, `blue-variant` |

### Parameter Details

**utm_source** — Where did the click physically happen?
```
utm_source=google          # Google Ads or Google organic
utm_source=facebook        # Meta Ads (Facebook/Instagram)
utm_source=linkedin        # LinkedIn Ads or organic
utm_source=klaviyo         # Email via Klaviyo
utm_source=tiktok          # TikTok Ads
utm_source=partner-blog    # A specific referral partner
```

**utm_medium** — The channel type. This is the most important parameter for GA4 default channel grouping. If utm_medium is wrong, traffic lands in the wrong channel.
```
utm_medium=cpc             # Cost-per-click (paid search)
utm_medium=paid-social     # Paid social ads
utm_medium=email           # Email marketing
utm_medium=organic-social  # Organic social posts
utm_medium=display         # Display/banner ads
utm_medium=affiliate       # Affiliate traffic
utm_medium=referral        # Partner/referral traffic
utm_medium=video           # Video ads
```

**utm_campaign** — Campaign name with consistent structure:
```
utm_campaign=spring-sale-2025
utm_campaign=brand-awareness-q1-2025
utm_campaign=retargeting-cart-abandoners
```

**utm_term** — Keyword or targeting term:
```
utm_term=running-shoes
utm_term=best-crm-software
```

**utm_content** — Creative variant or placement:
```
utm_content=hero-image-v1
utm_content=sidebar-cta
utm_content=video-30s
```

## GA4 Default Channel Grouping Rules

GA4 classifies every session into a default channel group based on `source`, `medium`, and `campaign` values. These rules determine how traffic appears in GA4 standard reports.

| Channel | Medium Must Match |
|---------|-------------------|
| **Direct** | source = `(direct)` AND medium is `(not set)` or `(none)` |
| **Organic Search** | medium = `organic` |
| **Paid Search** | medium matches `^(cpc\|ppc\|paidsearch)$` |
| **Display** | medium matches `^(display\|cpm\|banner)$` |
| **Paid Social** | medium matches `^(paid-social\|paidsocial\|paid_social)$` |
| **Organic Social** | medium matches `^(social\|social-network\|social-media\|sm\|organic-social)$` |
| **Email** | medium = `email` |
| **Affiliates** | medium = `affiliate` |
| **Referral** | medium = `referral` |
| **Audio** | medium = `audio` |
| **SMS** | medium matches `^(sms\|sms_message)$` |
| **Video** | medium matches `^(video\|youtube)$` |
| **Cross-network** | campaign name contains `cross-network` |
| **Unassigned** | Does not match any rule above |

**Critical:** If `utm_medium` does not match any pattern above, traffic falls into **Unassigned**.

## GA4 Source/Medium Mapping in BigQuery

UTM values appear in multiple locations in the GA4 BigQuery export:

| UTM Parameter | BigQuery Location | Scope |
|---------------|-------------------|-------|
| `utm_source` | `traffic_source.source` | User (first-touch) |
| `utm_medium` | `traffic_source.medium` | User (first-touch) |
| `utm_campaign` | `traffic_source.name` | User (first-touch) |
| `utm_source` | Event param `source` on `session_start` | Session |
| `utm_medium` | Event param `medium` on `session_start` | Session |
| `utm_campaign` | Event param `campaign` on `session_start` | Session |

**Session-level source/medium query:**
```sql
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'source') as session_source,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'medium') as session_medium,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'campaign') as session_campaign,
  COUNT(*) as sessions
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'session_start'
GROUP BY 1, 2, 3
ORDER BY sessions DESC
```

## Naming Conventions

### Rules

1. **Lowercase everything.** GA4 is case-sensitive. `Facebook` and `facebook` are separate sources.
2. **Use hyphens as word separators.** Not spaces (become `%20`) or special characters.
3. **No special characters.** Stick to `a-z`, `0-9`, and `-`.
4. **Be specific but concise.** `paid-social` not `ps`.
5. **Include time identifiers in campaigns.** `spring-sale-2025` not `spring-sale`.

### Recommended Taxonomy

| Parameter | Convention | Examples |
|-----------|-----------|---------|
| `utm_source` | Platform name, lowercase | `google`, `facebook`, `linkedin`, `klaviyo` |
| `utm_medium` | Channel type matching GA4 rules | `cpc`, `paid-social`, `email`, `display` |
| `utm_campaign` | `name-date` or `name-quarter` | `spring-sale-2025`, `retarget-cart-q1` |
| `utm_term` | Keyword or targeting | `running-shoes`, `brand-keyword` |
| `utm_content` | Creative variant or placement | `video-30s-v2`, `hero-banner`, `cta-red` |

## UTM Templates by Channel

### Google Ads (Search)
```
?utm_source=google&utm_medium=cpc&utm_campaign={campaign_name}&utm_term={keyword}&utm_content={ad_variant}
```

### Google Ads (Display)
```
?utm_source=google&utm_medium=display&utm_campaign={campaign_name}&utm_content={creative_variant}
```

### Meta Ads (Facebook/Instagram)
```
utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}
```
Meta dynamic parameters: `{{campaign.name}}`, `{{campaign.id}}`, `{{adset.name}}`, `{{adset.id}}`, `{{ad.name}}`, `{{ad.id}}`, `{{placement}}`, `{{site_source_name}}`.

### LinkedIn Ads
```
utm_source=linkedin&utm_medium=paid-social&utm_campaign={{CAMPAIGN_NAME}}&utm_content={{CREATIVE_NAME}}
```
LinkedIn macros: `{{CAMPAIGN_ID}}`, `{{CAMPAIGN_NAME}}`, `{{CAMPAIGN_GROUP_ID}}`, `{{CAMPAIGN_GROUP_NAME}}`, `{{CREATIVE_ID}}`, `{{CREATIVE_NAME}}`.

### Email
```
?utm_source={esp_name}&utm_medium=email&utm_campaign={email_campaign_name}&utm_content={link_placement}
```

### Organic Social
```
?utm_source={platform}&utm_medium=organic-social&utm_campaign={post_theme}&utm_content={post_variant}
```

### Influencer
```
?utm_source=creator-{name}&utm_medium=paid-social&utm_campaign=influencer-{campaign}-{date}&utm_content={platform}-{format}
```

### Affiliate
```
?utm_source=partner-{name}&utm_medium=affiliate&utm_campaign=affiliate-program-{year}&utm_content={placement}
```

## Auto-Tagging vs Manual Tagging

### Google Ads (gclid)
- Auto-tagging appends `gclid` to every click URL
- GA4 attributes the session to Google Ads automatically with campaign, ad group, keyword data
- Source/medium set to `google / cpc` automatically
- **If both gclid and UTMs present, GA4 prioritizes gclid** — UTMs are ignored for GA4 attribution

**When you still need UTMs with Google Ads:**
- CRM systems that parse UTM parameters (HubSpot, Salesforce)
- Third-party analytics tools (Mixpanel, Amplitude)
- Cross-platform dashboards that cannot read gclid
- Custom BigQuery attribution models using `page_location`

### Meta Ads (fbclid)
- GA4 does **not** natively parse `fbclid` for attribution
- Without UTMs, Meta traffic appears as `facebook.com / referral` or `l.facebook.com / referral`
- **You must use UTM parameters** for correct Meta Ads attribution in GA4

### LinkedIn Ads
- LinkedIn Insight Tag tracks conversions but does not provide click-level GA4 attribution
- **You must use UTM parameters** for correct LinkedIn Ads attribution in GA4

### When to Use Both
- Google Ads + CRM integration: gclid feeds GA4, UTMs feed CRM
- Cross-platform dashboards that need UTMs
- Custom BigQuery attribution models

**Warning:** For Google Ads, ensure "Allow manual tagging to override auto-tagging" is **unchecked** in GA4 settings unless you specifically want UTMs to override gclid.

## Common UTM Mistakes

### 1. Inconsistent Naming
GA4 treats each unique string as a separate source:
```
utm_source=Facebook       # WRONG: capital F
utm_source=facebook       # CORRECT
utm_source=fb             # WRONG: abbreviation
```

### 2. UTMs on Internal Links
Adding UTMs to links within your own site resets session source and inflates session counts. Never do this:
```html
<!-- WRONG -->
<a href="/pricing?utm_source=homepage&utm_medium=banner">Pricing</a>
```

### 3. Missing utm_medium
Without utm_medium, traffic falls into Unassigned:
```
# BAD: No medium
?utm_source=facebook&utm_campaign=spring-sale

# GOOD: Medium present
?utm_source=facebook&utm_medium=paid-social&utm_campaign=spring-sale
```

### 4. URL-Encoded Special Characters
```
# BAD
utm_campaign=Spring Sale 2025    # Becomes Spring%20Sale%202025

# GOOD
utm_campaign=spring-sale-2025
```

### 5. UTMs on Organic/SEO Pages
Never add UTM parameters to pages search engines crawl — splits page authority and creates duplicate content.

### 6. Not Including Date in Campaign Names
```
# BAD: Cannot distinguish quarters
utm_campaign=brand-search

# GOOD: Time-scoped
utm_campaign=brand-search-q1-2025
```

## BigQuery Validation Queries

### All Unique Source/Medium Combinations
```sql
SELECT
  traffic_source.source,
  traffic_source.medium,
  COUNT(DISTINCT user_pseudo_id) as users,
  MIN(PARSE_DATE('%Y%m%d', event_date)) as first_seen,
  MAX(PARSE_DATE('%Y%m%d', event_date)) as last_seen
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1, 2
ORDER BY users DESC
```

### Find Inconsistent Source Naming
```sql
WITH source_variants AS (
  SELECT
    LOWER(traffic_source.source) as normalized_source,
    traffic_source.source as original_source,
    COUNT(DISTINCT user_pseudo_id) as users
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
    AND traffic_source.source IS NOT NULL
  GROUP BY 1, 2
)
SELECT
  normalized_source,
  ARRAY_AGG(STRUCT(original_source, users) ORDER BY users DESC) as variants,
  COUNT(*) as variant_count
FROM source_variants
GROUP BY 1
HAVING COUNT(*) > 1
ORDER BY variant_count DESC
```

### Predict Channel Grouping Assignment
```sql
SELECT
  traffic_source.source,
  traffic_source.medium,
  CASE
    WHEN traffic_source.source = '(direct)' AND (traffic_source.medium IS NULL OR traffic_source.medium IN ('(not set)', '(none)')) THEN 'Direct'
    WHEN traffic_source.medium = 'organic' THEN 'Organic Search'
    WHEN REGEXP_CONTAINS(traffic_source.medium, r'^(cpc|ppc|paidsearch)$') THEN 'Paid Search'
    WHEN REGEXP_CONTAINS(traffic_source.medium, r'^(display|cpm|banner)$') THEN 'Display'
    WHEN REGEXP_CONTAINS(traffic_source.medium, r'^(paid-social|paidsocial|paid_social)$') THEN 'Paid Social'
    WHEN REGEXP_CONTAINS(traffic_source.medium, r'^(social|social-network|social-media|sm|social_network|social_media|organic-social)$') THEN 'Organic Social'
    WHEN traffic_source.medium = 'email' THEN 'Email'
    WHEN traffic_source.medium = 'affiliate' THEN 'Affiliates'
    WHEN traffic_source.medium = 'referral' THEN 'Referral'
    WHEN traffic_source.medium = 'audio' THEN 'Audio'
    WHEN REGEXP_CONTAINS(traffic_source.medium, r'^(sms|sms_message)$') THEN 'SMS'
    WHEN REGEXP_CONTAINS(traffic_source.medium, r'^(video|youtube)$') THEN 'Video'
    WHEN REGEXP_CONTAINS(IFNULL(traffic_source.name, ''), r'cross-network') THEN 'Cross-network'
    ELSE 'Unassigned'
  END as predicted_channel_group,
  COUNT(DISTINCT user_pseudo_id) as users
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
GROUP BY 1, 2, 3
ORDER BY users DESC
```

### Find Internal UTM Pollution
```sql
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') as landing_page,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_referrer') as referrer,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'source') as session_source,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'medium') as session_medium,
  COUNT(*) as sessions
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'session_start'
  -- Replace example.com with your domain
  AND REGEXP_CONTAINS(
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_referrer'),
    r'example\.com'
  )
  AND REGEXP_CONTAINS(
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location'),
    r'utm_'
  )
GROUP BY 1, 2, 3, 4
ORDER BY sessions DESC
```

### Find Sessions Missing utm_medium
```sql
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'source') as source,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'campaign') as campaign,
  COUNT(*) as sessions
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'session_start'
  AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'source') IS NOT NULL
  AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'source') != '(direct)'
  AND (
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'medium') IS NULL
    OR (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'medium') IN ('(not set)', '(none)', '')
  )
GROUP BY 1, 2
ORDER BY sessions DESC
```

## Spreadsheet Builder Formula

Google Sheets formula to generate UTM URLs from columns (A=URL, B=source, C=medium, D=campaign, E=term, F=content):
```
=A2&"?utm_source="&B2&"&utm_medium="&C2&"&utm_campaign="&D2&IF(E2<>"","&utm_term="&E2,"")&IF(F2<>"","&utm_content="&F2,"")
```

## Resources

- **Google UTM Builder:** https://ga-dev-tools.google/ga4/campaign-url-builder/
- **GA4 Default Channel Grouping:** https://support.google.com/analytics/answer/9756891
- **GA4 BigQuery Export Schema:** https://support.google.com/analytics/answer/7029846
- **Google Ads Auto-Tagging:** https://support.google.com/google-ads/answer/3095550
- **Meta URL Parameters:** https://www.facebook.com/business/help/1016122818401732
- **Full Cogny Docs:** https://cogny.com/docs/utm-strategy
