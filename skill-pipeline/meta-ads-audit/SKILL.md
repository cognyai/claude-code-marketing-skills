---
name: meta-ads-audit
description: Meta Ads audit — audience analysis, creative fatigue, budget pacing, lead quality
version: "1.1.0"
author: Cogny AI
requires: cogny-mcp
platforms: [meta-ads, tiktok-ads, snapchat-ads, reddit-ads, x-ads, fibbler]
user-invocable: true
argument-hint: "[full|audiences|creatives|budget]"
allowed-tools:
  # Meta Ads read tools (update_* tools ask first, never pre-approved)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Meta_Ads__tool_get_ad_sets
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__Meta_Ads__tool_get_custom_audiences
  - mcp__cogny__mcp__Meta_Ads__tool_get_pixels
  # Same audit on other paid social (read-only)
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_campaigns
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ads
  - mcp__cogny__mcp__TikTok_Ads__tool_get_insights
  - mcp__cogny__mcp__TikTok_Ads__tool_get_audiences
  - mcp__cogny__mcp__TikTok_Ads__tool_get_pixels
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ad_squads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_stats
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_segments
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_pixels
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ads
  - mcp__cogny__mcp__Reddit_Ads__tool_get_reporting
  - mcp__cogny__mcp__Reddit_Ads__tool_get_custom_audiences
  - mcp__cogny__mcp__Reddit_Ads__tool_get_conversion_events
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__X_Ads__tool_get_line_items
  - mcp__cogny__mcp__X_Ads__tool_get_promoted_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_analytics
  - mcp__cogny__mcp__X_Ads__tool_get_tailored_audiences
  - mcp__cogny__mcp__X_Ads__tool_get_web_event_tags
  # B2B lead quality (read-only)
  - mcp__cogny__mcp__app-fibbler-co__get_meta_ads_campaign_analytics
  - mcp__cogny__mcp__app-fibbler-co__get_deal_attribution_summary
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Meta Ads Audit

Comprehensive Meta Ads (Facebook + Instagram) account audit using live data via Cogny's MCP server.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

Meta is primary. The same audit (structure, fatigue, audiences, pacing) runs on any other paid social account the workspace has connected.

| Job | Meta (primary) | TikTok | Snapchat | Reddit | X |
|-----|----------------|--------|----------|--------|---|
| Accounts | `tool_list_ad_accounts` | `tool_list_advertisers` | `tool_list_organizations` → `tool_list_ad_accounts(organization_id)` | `tool_list_ad_accounts` | `tool_list_ad_accounts` |
| Structure | `tool_get_campaigns`, `tool_get_ad_sets`, `tool_get_ads` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads` (`advertiser_id`) | `tool_get_campaigns`, `tool_get_ad_squads`, `tool_get_ads` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads` | `tool_get_campaigns`, `tool_get_line_items`, `tool_get_promoted_tweets` (`account_id`) |
| Performance | `tool_get_insights(level, date_preset)` | `tool_get_insights(start_date, end_date, level: "AUCTION_CAMPAIGN" / "AUCTION_ADGROUP" / "AUCTION_AD")` | `tool_get_stats(entity_id, start_time, end_time, level)` | `tool_get_reporting(start_date, end_date, level)` | `tool_get_analytics(entity, entity_ids, start_time, end_time)` |
| Audiences / tracking | `tool_get_custom_audiences`, `tool_get_pixels` | `tool_get_audiences`, `tool_get_pixels` | `tool_list_segments`, `tool_list_pixels` | `tool_get_custom_audiences`, `tool_get_conversion_events` | `tool_get_tailored_audiences`, `tool_get_web_event_tags` |
| B2B lead quality | Fibbler `get_meta_ads_campaign_analytics` | — | — | — | — |

Tool names omit the `mcp__cogny__mcp__<Prefix>__` part. What differs:
- **Frequency** is returned by Meta, TikTok (`frequency` metric) and Reddit (`FREQUENCY` field). On Snapchat and X, request reach/uniques fields if available, otherwise judge fatigue by CTR decay over time instead.
- **Units:** Reddit and Snapchat budgets and bids are in micros (÷ 1,000,000); check whether a spend field is micros before reporting it. X analytics needs explicit `entity_ids`.
- **Conversions** use each platform's own pixel and attribution window; don't compare CPL across platforms as if it were the same event.
- Every account has its own currency. With several platforms connected, report one section per platform side by side and never sum spend or leads across them.

## Prerequisites Check

Call `mcp__cogny__list_integrations`. If Meta Ads is connected, run the steps below. If only TikTok, Snapchat, Reddit or X is connected, run the same steps with that platform's tools from the table and title the report with the platform name. If none is connected:

```
This skill requires a paid social integration (Meta, TikTok, Snapchat, Reddit or X Ads) via Cogny's MCP server.
Sign up at https://cogny.com and connect your ad account.
```

## Usage

`/meta-ads-audit` — full audit
`/meta-ads-audit audiences` — audience analysis only
`/meta-ads-audit creatives` — creative performance only
`/meta-ads-audit budget` — budget pacing only

## Full Audit Steps

### 1. Account Discovery
```
mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
```

### 2. Campaign Overview (last 30 days)
```
mcp__cogny__mcp__Meta_Ads__tool_get_campaigns(ad_account_id, status_filter: ["ACTIVE"])
mcp__cogny__mcp__Meta_Ads__tool_get_insights(ad_account_id, level: "campaign", date_preset: "last_30d")
```

### 3. Ad Set Analysis
```
mcp__cogny__mcp__Meta_Ads__tool_get_ad_sets(ad_account_id)
mcp__cogny__mcp__Meta_Ads__tool_get_insights(ad_account_id, level: "adset", date_preset: "last_30d")
```

Check: audience overlap, frequency saturation, demographic breakdown

### 4. Creative Performance
```
mcp__cogny__mcp__Meta_Ads__tool_get_ads(ad_account_id)
mcp__cogny__mcp__Meta_Ads__tool_get_insights(ad_account_id, level: "ad", date_preset: "last_30d")
```

Flag: fatigue (frequency > 3), low CTR, single-creative ad sets

### 5. Audience Health
```
mcp__cogny__mcp__Meta_Ads__tool_get_custom_audiences(ad_account_id)
mcp__cogny__mcp__Meta_Ads__tool_get_pixels(ad_account_id)
```

Check: audience sizes, stale audiences, pixel health

### 5b. Lead quality (enhanced when Fibbler is connected)
For B2B lead-gen accounts, Meta's leads say nothing about whether they became pipeline.
```
mcp__cogny__mcp__app-fibbler-co__get_meta_ads_campaign_analytics(time_period: "90d")
mcp__cogny__mcp__app-fibbler-co__get_deal_attribution_summary(source: "META_ADS", time_period: "90d")
```
Flag campaigns with cheap CPL but no influenced pipeline, and a high `untaggedVisits` count (missing UTMs caps attribution). Fibbler's "engagements" are not conversions, and its pipeline is influence, not credit; show it next to Meta's numbers, never added to them.

### 6. Budget Pacing
Compare daily budget vs actual spend for last 7 days. Flag:
- Under-pacing (< 70% of budget)
- Over-pacing (> 110% of budget)
- Budget waste on non-converting campaigns

### 7. Report

```
[Meta / TikTok / Snapchat / Reddit / X] Ads Audit: [Account Name] ([currency])
Health Score: X/100

Account Overview (30d):
Spend: [X] | Reach: [X] | Leads: [X] | CPL: [X]
Influenced pipeline (Fibbler, if connected): [X]

Active Campaigns: [N]
Top Performer: [Campaign] — [CPL/ROAS]
Worst Performer: [Campaign] — [why]

Issues Found: [N]
- [Critical] ...
- [High] ...

Top 3 Actions:
1. ...
2. ...
3. ...
```

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../../skills/marketing-engineer/references/mcp-routing.md`.
