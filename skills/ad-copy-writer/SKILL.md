---
name: ad-copy-writer
description: Generate ad copy variations for Google, Microsoft, Meta, LinkedIn, TikTok, Reddit, Snapchat and X Ads (plus Apple Search Ads guidance)
version: "1.1.1"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<platform> <product or URL>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Optional: read live ads so new copy doesn't repeat angles already running (read-only)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Bing_Ads__tool_get_ads
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ads
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ads
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_creatives
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_cards
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_targeting_keywords
---

# Ad Copy Writer

Generate high-converting ad copy for Google, Microsoft, Meta, LinkedIn, TikTok, Reddit, Snapchat or X Ads. Works with no accounts connected.

## Usage

`/ad-copy-writer google "project management tool"` — Google Ads copy
`/ad-copy-writer meta example.com` — Meta Ads copy from website
`/ad-copy-writer linkedin "B2B SaaS"` — LinkedIn Ads copy
`/ad-copy-writer reddit|tiktok|snapchat|x|microsoft example.com` — other platforms

## Works with

| Job | Primary | Also answers it | What differs |
|-----|---------|-----------------|--------------|
| Product and competitor research | WebFetch / WebSearch | — | Always available |
| Angles already running (enhanced when connected) | The target platform's ad MCP | Any other connected ad platform | Read-only; used to avoid repeating angles, never to edit ads |

Pulling live ads per platform (tool names omit `mcp__cogny__mcp__<Prefix>__`):

| Platform | Prefix | Read current copy |
|----------|--------|-------------------|
| Google | `Google_Ads` | `tool_execute_gaql(customer_id, query: "SELECT ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, metrics.ctr FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS")` |
| Microsoft | `Bing_Ads` | `tool_get_ad_groups` → `tool_get_ads(account_id, ad_group_id)` |
| Meta | `Meta_Ads` | `tool_get_ads(ad_account_id, status_filter: ["ACTIVE"], include_creative: true)` |
| LinkedIn | `LinkedIn_Ads` | `tool_get_creatives(ad_account_id, status_filter: ["ACTIVE"])` |
| TikTok | `TikTok_Ads` | `tool_get_ads(advertiser_id, status_filter: [...])` |
| Reddit | `Reddit_Ads` | `tool_get_ads(ad_account_id)` |
| Snapchat | `Snapchat_Ads` | `tool_list_organizations` → `tool_list_ad_accounts` → `tool_get_creatives(ad_account_id)` |
| X | `X_Ads` | `tool_get_tweets(account_id, tweet_type: "PUBLISHED")`, `tool_get_cards(account_id)` for card headlines |
| Apple Search Ads | `Apple_Search_Ads` | `tool_list_acls` → `tool_get_campaigns` → `tool_get_ad_groups` → `tool_get_targeting_keywords` (keywords, not copy) |

## Steps

### 1. Research the product
If a URL is provided, WebFetch it and extract:
- Value proposition
- Key features / benefits
- Target audience
- Pricing (if visible)
- Unique differentiators

If a description is provided, use that directly.

### 2. Research the competition
WebSearch for competitors to understand:
- What messaging angles they use
- Common claims in the space
- Price anchoring

### 2b. Enhanced when connected: read what's already running

If the target platform is connected (check `mcp__cogny__list_integrations`), pull its active ads with the tool above. List the angles, claims and CTAs already in use, and mark the top performers by the platform's own CTR where available. Then write new copy that tests *different* angles, and say which existing angle each new variation is meant to beat. If nothing is connected, skip this step.

### 3. Generate copy by platform

#### Google Ads (RSA format)
Generate 15 headlines (max 30 chars each) and 4 descriptions (max 90 chars each):

**Headlines** — mix of:
- Benefit-led: "Cut Ad Spend 40%"
- Feature-led: "AI-Powered Optimization"
- Social proof: "Trusted by 1,000+ Agencies"
- CTA: "Start Free Trial Today"
- Keyword-match: "[Primary keyword] Tool"

**Descriptions** — mix of:
- Problem/solution
- Feature list
- Social proof + CTA
- Urgency/offer

#### Meta Ads
Generate 3 variations:
- **Primary text** (50-150 chars recommended for single-image Feed ads, per Meta's Ads Guide; up to 500)
- **Headline** (27 chars recommended for single-image Feed ads; longer headlines truncate)
- **Description** (30 chars)
- **CTA button** recommendation

Angles:
1. Pain point → solution
2. Social proof → aspiration
3. Direct value prop → CTA

#### LinkedIn Ads
Generate 3 variations:
- **Intro text** (150 chars recommended to avoid truncation; 3,000 max)
- **Headline** (70 chars recommended; 200 max)
- **Description** (100 chars recommended; 300 max; shown only on LinkedIn Audience Network placements)

Angles:
1. Professional credibility
2. ROI / efficiency focus
3. Industry-specific insight

#### Microsoft Ads (RSA format)
Same limits as Google: 15 headlines (30 chars), 4 descriptions (90 chars), 2 display paths (15 chars). Reuse the Google set, but check the audience skews older and more desktop/B2B (LinkedIn profile targeting is available), so favour clarity over slang.

#### TikTok Ads
Generate 3 variations:
- **Ad text** (1–100 chars; keep under ~80 so it isn't truncated)
- **Display name** (brand, up to 40 chars)
- **CTA button** recommendation
Angles: native hook in the first line ("POV:", "I tried…"), demo/result, creator testimonial. Copy supports the video; it never explains it.

#### Reddit Ads
Generate 3 variations:
- **Headline / post title** (max 300 chars; aim for 60–120)
- **CTA button** recommendation
Angles: plain-spoken problem statement, honest comparison, "we built this because…". No hype words; Reddit users downvote ad-speak.

#### Snapchat Ads
Generate 3 variations:
- **Brand name** (max 25 chars)
- **Headline** (max 34 chars)
- **CTA** recommendation
Angles: instant benefit, offer/urgency, playful/social.

#### X Ads
Generate 3 variations:
- **Post text** (max 280 chars; a URL counts as 23)
- **Website card headline** (max 70 chars)
Angles: hot take / contrarian, number-led proof, thread-style teaser.

#### Apple Search Ads
There is no free-text ad copy: ads are built from the App Store listing (app name 30 chars, subtitle 30 chars, screenshots) and custom product pages. Instead deliver: subtitle options (30 chars), 3 custom product page themes matched to keyword groups, and the keyword groups themselves. If `Apple_Search_Ads` is connected, read live keywords with `tool_get_targeting_keywords(org_id, campaign_id, ad_group_id)` first.

### 4. Output format

Present each variation clearly labeled with character counts:

```
=== Google Ads RSA ===

Headlines (30 char max):
1. "Cut Your Ad Spend by 40%" (25)
2. "AI Marketing Automation" (24)
...

Descriptions (90 char max):
1. "Stop wasting budget on underperforming ads. Our AI optimizes your campaigns 24/7." (83)
...

=== Meta Ads ===

Variation 1 (Pain → Solution):
Primary: "..."
Headline: "..."
...
```
