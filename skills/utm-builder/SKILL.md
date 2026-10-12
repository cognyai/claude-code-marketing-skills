---
name: utm-builder
description: UTM Parameter Strategy & Builder — naming conventions, GA4 channel grouping rules, auto-tagging, common mistakes, and BigQuery validation queries
version: "1.1.3"
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
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_get_property
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_data_streams
  # Google Ads tools
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  # Other sources for a live UTM audit (when connected, read-only)
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Fathom_Analytics__list_sites
  - mcp__cogny__mcp__Fathom_Analytics__aggregate
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_cards
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
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

## Works with

Works with zero accounts: building UTMs and the naming rules need nothing connected.
For `/utm-builder audit`:

| Job | Primary | Also answered by | No account |
|-----|---------|------------------|------------|
| UTMs as they arrive on the site | GA4 `tool_run_report` | Plausible `breakdown`, Fathom Analytics `aggregate` | BigQuery queries below |
| UTMs as set in the ads | Google Ads `tool_execute_gaql` | Meta `tool_get_ads`, LinkedIn `tool_get_creatives`, X `tool_get_cards` | ask for an export |
| Fix a Meta ad set's URL tags | — | Meta `tool_update_ad_set_url_tags` (write: not pre-approved, asks first) | — |

See "Live UTM Audit" below.

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
utm_source=twitter         # X Ads or organic. GA4 still lists X as "twitter": "x" lands in Organic Search, "x.com" in Referral, "xads" in Paid Other
utm_source=klaviyo         # Email via Klaviyo
utm_source=tiktok          # TikTok Ads
utm_source=partner-blog    # A specific referral partner
```

**utm_medium** — The channel type. This is the most important parameter for GA4 default channel grouping. If utm_medium is wrong, traffic lands in the wrong channel.
```
utm_medium=cpc             # Cost-per-click (paid search)
utm_medium=paid-social     # Paid social ads (needs a social utm_source; see channel rules)
utm_medium=email           # Email marketing
utm_medium=organic-social  # Organic social posts
utm_medium=display         # Display/banner ads
utm_medium=affiliate       # Affiliate traffic
utm_medium=referral        # Partner/referral traffic
utm_medium=video           # Lands in Organic Video; for paid video use utm_source=youtube + utm_medium=cpc
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

GA4 classifies every session into a default channel group from its `source`, `medium` and
`campaign`. Rules below are for manually tagged (UTM) traffic. Google's page lists the
channels alphabetically and doesn't document an evaluation order, so read the table as
conditions, not a ranked list; when a combination looks ambiguous, check where it actually
lands in GA4. Source: [Google's definitions](https://support.google.com/analytics/answer/9756891).
Google Ads auto-tagged traffic is classified by ad network / campaign type instead.

"Paid medium" below means medium matches `^(.*cp.*|ppc|retargeting|paid.*)$`
(so `cpc`, `cpm`, `paid-social`, `paidsocial`, `paid_social`, `ppc`, `retargeting` all count).
**Source categories** (search, social, video, shopping sites) are Google's own lists,
downloadable from the help page. Common entries: search `google`, `bing`, `yahoo`, `duckduckgo`,
`baidu`, `yandex`, `ecosia`; social `facebook`, `fb`, `instagram`, `ig`, `linkedin`, `lnkd.in`,
`twitter`, `t.co`, `reddit`, `tiktok` (and subdomains like `business-api.tiktok.com`), `pinterest`, `snapchat`; video `youtube`, `vimeo`,
`twitch`; shopping `shopping`, `igshopping`, `google shopping`.

| Channel | Rule |
|---------|------|
| **Direct** | source = `(direct)` AND medium is `(not set)` or `(none)` |
| **Cross-network** | campaign name contains `cross-network` |
| **Paid Shopping** | (source is a shopping site OR campaign matches `^(.*(([^a-df-z]\|^)shop\|shopping).*)$`) AND paid medium |
| **Paid Search** | source is a **search** site AND paid medium |
| **Paid Social** | source is a **social** site AND paid medium |
| **Paid Video** | source is a **video** site AND paid medium |
| **Display** | medium is `display`, `banner`, `expandable`, `interstitial` or `cpm` |
| **Paid Other** | paid medium, but the source is in none of the lists above |
| **Organic Shopping** | source is a shopping site OR campaign matches the shop/shopping regex |
| **Organic Social** | source is a social site OR medium is `social`, `social-network`, `social-media`, `sm`, `social network`, `social media` |
| **Organic Video** | source is a video site OR medium matches `^(.*video.*)$` |
| **Organic Search** | source is a search site OR medium = `organic` |
| **AI Assistant** | medium = `ai-assistant` (GA4 also sets it when the referrer is a known AI assistant) |
| **Referral** | medium is `referral`, `app` or `link` |
| **Email** | source or medium is `email`, `e-mail`, `e_mail` or `e mail` |
| **Affiliates** | medium = `affiliate` |
| **Audio** | medium = `audio` |
| **SMS** | source or medium = `sms` |
| **Mobile Push Notifications** | medium ends with `push`, or contains `mobile` or `notification`, or source = `firebase` |
| **Unassigned** | matches none of the above |

**Critical:**
- A paid medium alone isn't enough. `cpc` only becomes Paid Search with a search source and
  Paid Social with a social source. Live proof: `utm_source=xads&utm_medium=cpc` landed in
  **Paid Other**, because `xads` isn't on Google's social list. Use `twitter`, `facebook`,
  `linkedin`, `tiktok`: names Google recognises. **Not `x`**: live GA4 data puts `x / organic` in
  Organic Search and `x.com / referral` in Referral, while `twitter / cpc` and `twitter / paid` land in
  Paid Social.
- Payment and login referrers (`checkout.stripe.com`, OAuth providers) get classified as channels
  (Stripe even lands in Organic Shopping). Add them to GA4's unwanted-referrals list.
- `cpm` matches the paid-medium regex, so `facebook / cpm` is Paid Social, not Display.
- `organic-social` is **not** an Organic Social medium; it only lands there because the source
  is a social site. With an unknown source it's Unassigned.
- A medium that matches no rule, with a source on no list, falls into **Unassigned**.

## GA4 Source/Medium Mapping in BigQuery

UTM values appear in multiple locations in the GA4 BigQuery export:

| UTM Parameter | BigQuery Location | Scope |
|---------------|-------------------|-------|
| `utm_source` | `traffic_source.source` | User (first-touch) |
| `utm_medium` | `traffic_source.medium` | User (first-touch) |
| `utm_campaign` | `traffic_source.name` | User (first-touch) |
| `utm_source` / `utm_medium` / `utm_campaign` / `utm_term` / `utm_content` / `utm_id` | `collected_traffic_source.manual_source` / `manual_medium` / `manual_campaign_name` / `manual_term` / `manual_content` / `manual_campaign_id` | Event (as collected) |
| (attributed) | `session_traffic_source_last_click.manual_campaign.{source, medium, campaign_name}` (or `.cross_channel_campaign.*`) | Session, last click |

Prefer these documented columns over the undocumented `source` / `medium` / `campaign`
event params on `session_start`. They're the export's official home for UTMs (older
export days may lack them; fall back to the event params there).

**Session-level source/medium query:**
```sql
SELECT
  collected_traffic_source.manual_source as session_source,
  collected_traffic_source.manual_medium as session_medium,
  collected_traffic_source.manual_campaign_name as session_campaign,
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

## Live UTM Audit (enhanced when connected)

If Cogny isn't connected, skip this and note what connecting adds.

Call `list_integrations` once and use whichever is healthy. `health_status` misses revoked
tokens, so make one cheap read per integration (`tool_list_ad_accounts`, GA4 `tool_get_property`):
a 401, Forbidden or scope error is 🔴 "reconnect <integration>", with no retry. If a tool named
here is missing, call `refresh_mcp_discovery` once; new tools only load after the client
reconnects, so skip that row this run and mark it ⚠ "needs reconnect". Last 30 days.

**What arrives on the site**

| Provider | Call |
|----------|------|
| GA4 | `tool_run_report` (`property_id`, `dimensions: [sessionSourceMedium, sessionCampaignName]`, `metrics: [sessions, keyEvents]`), plus one run with `dimensions: [sessionDefaultChannelGroup]` for the `Unassigned` share |
| Plausible | `breakdown` (`site_id`, `dimension`: `visit:utm_source`, then `visit:utm_medium`, then `visit:utm_campaign`; `date_range: 30d`) |
| Fathom Analytics | `list_sites` → `aggregate` (`entity: pageview`, `entity_id: <site id>`, `aggregates: visits`, `field_grouping: utm_campaign`, `date_from`, `date_to`) |

Flag, with the session count for each:
- Same source in several spellings (`Facebook`, `facebook`, `fb`, `facebook.com`)
- Uppercase or spaces in any value
- Mediums GA4 doesn't map to a channel (`paid_social`, `social-paid`), which land in `Unassigned`
- Campaigns with no date or quarter
- Your own domain as a source (UTMs on internal links)

**What the ads send**

| Platform | Call | Where the UTMs live |
|----------|------|---------------------|
| Google Ads | `tool_execute_gaql`: `SELECT campaign.name, campaign.tracking_url_template, campaign.final_url_suffix FROM campaign WHERE campaign.status = 'ENABLED'` | tracking template / final URL suffix (auto-tagging usually makes UTMs unnecessary) |
| Meta | `tool_list_ad_accounts` → `tool_get_ads` (`ad_account_id`, `include_creative: true`, `limit` ≤ 20, `thumbnail_width: 0`, `thumbnail_height: 0`; page by `campaign_id` / `ad_set_id` for more) | `url_tags` and `destination_url` on each ad's creative |
| LinkedIn | `tool_list_ad_accounts` → `tool_get_creatives` (`ad_account_id`, `status_filter: ["ACTIVE"]`) | the landing-page / click URL in each creative's `content` |
| X | `tool_list_ad_accounts` → `tool_get_cards` (`account_id`) | the card's website URL |

Ads with no UTMs on Meta, LinkedIn or X show up as `referral` in GA4, and a source GA4 doesn't
recognise (e.g. `xads`) lands in Paid Other. Give each broken ad the corrected template from
"UTM Templates by Channel". Fixing a Meta ad set with `tool_update_ad_set_url_tags`
(`ad_set_id`, `url_tags`) is a write, so it's not in this skill's allowed tools: show the new
string and ask first.

Name the provider on every number; Plausible counts visitors, GA4 counts sessions.

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

Approximates Google's manual-traffic rules (see the table above). The source lists are
abbreviated; extend the regexes from Google's downloadable source-category list for your traffic.

```sql
WITH t AS (
  SELECT
    LOWER(IFNULL(traffic_source.source, '')) AS src,
    LOWER(IFNULL(traffic_source.medium, '')) AS med,
    LOWER(IFNULL(traffic_source.name, '')) AS camp,
    user_pseudo_id
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                          AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
), c AS (
  SELECT *,
    REGEXP_CONTAINS(med, r'^(.*cp.*|ppc|retargeting|paid.*)$') AS paid_med,
    REGEXP_CONTAINS(src, r'^(google|bing|yahoo|duckduckgo|baidu|yandex|ecosia|naver|seznam)(\..*)?$|(^|\.)(google|bing|search\.yahoo|duckduckgo)\.') AS search_src,
    REGEXP_CONTAINS(src, r'^(facebook|fb|m\.facebook\.com|l\.facebook\.com|instagram|ig|linkedin|lnkd\.in|twitter|t\.co|reddit|pinterest|snapchat|quora|threads)(\.com)?$')
      OR REGEXP_CONTAINS(src, r'(^|\.)tiktok(\.com)?$') AS social_src,
    REGEXP_CONTAINS(src, r'^(youtube|m\.youtube\.com|vimeo|twitch|dailymotion|wistia)(\.com|\.tv)?$') AS video_src,
    REGEXP_CONTAINS(src, r'^(shopping|igshopping|google shopping|shopping\.google\.com)$')
      OR REGEXP_CONTAINS(camp, r'^(.*(([^a-df-z]|^)shop|shopping).*)$') AS shop
  FROM t
)
SELECT
  src AS source,
  med AS medium,
  CASE
    WHEN src = '(direct)' AND med IN ('', '(not set)', '(none)') THEN 'Direct'
    WHEN STRPOS(camp, 'cross-network') > 0 THEN 'Cross-network'
    WHEN shop AND paid_med THEN 'Paid Shopping'
    WHEN search_src AND paid_med THEN 'Paid Search'
    WHEN social_src AND paid_med THEN 'Paid Social'
    WHEN video_src AND paid_med THEN 'Paid Video'
    WHEN med IN ('display', 'banner', 'expandable', 'interstitial', 'cpm') THEN 'Display'
    WHEN paid_med THEN 'Paid Other'
    WHEN shop THEN 'Organic Shopping'
    WHEN social_src OR med IN ('social', 'social-network', 'social-media', 'sm', 'social network', 'social media') THEN 'Organic Social'
    WHEN video_src OR REGEXP_CONTAINS(med, r'video') THEN 'Organic Video'
    WHEN search_src OR med = 'organic' THEN 'Organic Search'
    WHEN med = 'ai-assistant' THEN 'AI Assistant'
    WHEN med IN ('referral', 'app', 'link') THEN 'Referral'
    WHEN src IN ('email', 'e-mail', 'e_mail', 'e mail') OR med IN ('email', 'e-mail', 'e_mail', 'e mail') THEN 'Email'
    WHEN med = 'affiliate' THEN 'Affiliates'
    WHEN med = 'audio' THEN 'Audio'
    WHEN src = 'sms' OR med = 'sms' THEN 'SMS'
    WHEN ENDS_WITH(med, 'push') OR STRPOS(med, 'mobile') > 0 OR STRPOS(med, 'notification') > 0 OR src = 'firebase' THEN 'Mobile Push Notifications'
    ELSE 'Unassigned'
  END AS predicted_channel_group,
  COUNT(DISTINCT user_pseudo_id) AS users
FROM c
GROUP BY 1, 2, 3
ORDER BY users DESC
```

### Find Internal UTM Pollution
```sql
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') as landing_page,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_referrer') as referrer,
  collected_traffic_source.manual_source as session_source,
  collected_traffic_source.manual_medium as session_medium,
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
  collected_traffic_source.manual_source as source,
  collected_traffic_source.manual_campaign_name as campaign,
  COUNT(*) as sessions
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
                        AND FORMAT_DATE('%Y%m%d', CURRENT_DATE() - 1)
  AND event_name = 'session_start'
  AND collected_traffic_source.manual_source IS NOT NULL
  AND collected_traffic_source.manual_source != '(direct)'
  AND (
    collected_traffic_source.manual_medium IS NULL
    OR collected_traffic_source.manual_medium IN ('(not set)', '(none)', '')
  )
GROUP BY 1, 2
ORDER BY sessions DESC
```

## Spreadsheet Builder Formula

Google Sheets formula to generate UTM URLs from columns (A=URL, B=source, C=medium, D=campaign, E=term, F=content):
```
=A2&IF(ISNUMBER(FIND("?",A2)),"&","?")&"utm_source="&ENCODEURL(B2)&"&utm_medium="&ENCODEURL(C2)&"&utm_campaign="&ENCODEURL(D2)&IF(E2<>"","&utm_term="&ENCODEURL(E2),"")&IF(F2<>"","&utm_content="&ENCODEURL(F2),"")
```

It appends with `&` when the URL already has a query string (`?`) and `?` otherwise, and
URL-encodes each value. If a URL has a `#fragment`, strip it first or put the UTMs before the
`#`, since anything after `#` never reaches the server or GA4.

## Resources

- **Google UTM Builder:** https://ga-dev-tools.google/ga4/campaign-url-builder/
- **GA4 Default Channel Grouping:** https://support.google.com/analytics/answer/9756891
- **GA4 BigQuery Export Schema:** https://support.google.com/analytics/answer/7029846
- **Google Ads Auto-Tagging:** https://support.google.com/google-ads/answer/3095550
- **Meta URL Parameters:** https://www.facebook.com/business/help/1016122818401732
- **Full Cogny Docs:** https://cogny.com/docs/utm-strategy
