---
name: meta-ads-audit
description: Meta Ads audit — audience analysis, creative fatigue, budget pacing, lead quality
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [meta-ads]
user-invocable: true
argument-hint: "[full|audiences|creatives|budget]"
allowed-tools:
  - mcp__cogny__meta_ads__*
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# Meta Ads Audit

Comprehensive Meta Ads (Facebook + Instagram) account audit using live data via Cogny's MCP server.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

Verify `mcp__cogny__meta_ads__tool_list_ad_accounts` is available. If not:

```
This skill requires Cogny's Meta Ads MCP server.
Sign up at https://cogny.com/agent and connect your Meta Ads account.
```

## Usage

`/meta-ads-audit` — full audit
`/meta-ads-audit audiences` — audience analysis only
`/meta-ads-audit creatives` — creative performance only
`/meta-ads-audit budget` — budget pacing only

## Full Audit Steps

### 1. Account Discovery
```
meta_ads__tool_list_ad_accounts
```

### 2. Campaign Overview (last 30 days)
```
meta_ads__tool_get_campaigns(ad_account_id, status_filter: ["ACTIVE"])
meta_ads__tool_get_insights(ad_account_id, level: "campaign", date_preset: "last_30d")
```

### 3. Ad Set Analysis
```
meta_ads__tool_get_ad_sets(ad_account_id)
meta_ads__tool_get_insights(ad_account_id, level: "adset", date_preset: "last_30d")
```

Check: audience overlap, frequency saturation, demographic breakdown

### 4. Creative Performance
```
meta_ads__tool_get_ads(ad_account_id)
meta_ads__tool_get_insights(ad_account_id, level: "ad", date_preset: "last_30d")
```

Flag: fatigue (frequency > 3), low CTR, single-creative ad sets

### 5. Audience Health
```
meta_ads__tool_get_custom_audiences(ad_account_id)
meta_ads__tool_get_pixels(ad_account_id)
```

Check: audience sizes, stale audiences, pixel health

### 6. Budget Pacing
Compare daily budget vs actual spend for last 7 days. Flag:
- Under-pacing (< 70% of budget)
- Over-pacing (> 110% of budget)
- Budget waste on non-converting campaigns

### 7. Report

```
Meta Ads Audit: [Account Name]
Health Score: X/100

Account Overview (30d):
Spend: [X] | Reach: [X] | Leads: [X] | CPL: [X]

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
