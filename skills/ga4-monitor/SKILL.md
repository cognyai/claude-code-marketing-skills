---
name: ga4-monitor
description: Weekly GA4 check — sessions, users, key-event conversions, revenue, channel mix — with week-over-week deltas and tracking-break alerts
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-analytics-4]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__google_analytics_4__tool_list_account_summaries
  - mcp__cogny__google_analytics_4__tool_get_property
  - mcp__cogny__google_analytics_4__tool_list_conversion_events
  - mcp__cogny__google_analytics_4__tool_run_report
  - mcp__cogny__google_analytics_4__tool_run_realtime_report
  - mcp__cogny__create_finding
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  - WebFetch
---

# GA4 Monitor

A recurring weekly check on a GA4 property. It confirms data is still flowing, reports
traffic and conversions week-over-week, and — most importantly — catches the silent
failure mode: a key event that stopped firing because a tag broke.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

Designed to be scheduled weekly via `/loop` or `/schedule`.

## Prerequisites Check

If `mcp__cogny__google_analytics_4__tool_run_report` is not available, print the Cogny
sign-up instructions (see `/ga4-audit`) and stop.

## Usage

`/ga4-monitor` — weekly health check of the connected GA4 property.

For a full one-time review, run `/ga4-audit`. This is the light weekly rhythm.

## Steps

### 1. Read the prior snapshot

Call `read_context_node` on `insights/ga4/monitor/latest`. If present, it holds last
week's numbers — report every metric as a delta against it. If absent, this is the
first run: report absolutes and note deltas begin next week.

### 2. Data-flow heartbeat

```
tool_run_realtime_report   (property_id, metrics: activeUsers)
```

If realtime shows zero active users on a site with normal traffic, tagging may be
down. Note it, but confirm against the 7-day report before alarming.

### 3. Traffic & engagement (last 7d vs prior 7d)

```
tool_run_report   (property_id,
  date range A: last 7 days, date range B: prior 7 days,
  metrics: sessions, totalUsers, newUsers, engagementRate, averageSessionDuration)
```

Report each metric with its WoW delta.

### 4. Key-event conversions (the critical check)

```
tool_list_conversion_events   (property_id)
tool_run_report   (property_id, last 7d vs prior 7d,
  dimensions: eventName,
  metrics: eventCount, conversions, totalRevenue)
```

🔴 Alert if any key event recorded conversions last week and **zero this week** — the
tag or GTM trigger has almost certainly broken. This is the single most important
check in the skill.

🟡 Flag key events that dropped >50% WoW without an obvious traffic cause.

### 5. Channel mix

```
tool_run_report   (property_id, last 7d vs prior 7d,
  dimensions: sessionDefaultChannelGroup,
  metrics: sessions, conversions)
```

🟡 Alert on:
- A jump in `Unassigned` / `(not set)` sessions — UTMs broke somewhere
- A `Direct` spike — often a tagging or redirect problem
- A channel that fell off a cliff (campaign ended, or tracking lost)

### 6. Output

```
GA4 Monitor — [Property Name]
Week of [YYYY-MM-DD] – [YYYY-MM-DD]

⚠️  Needs attention this week
- [Critical/important first, or "Nothing — data is flowing clean."]

Traffic (7d vs prior 7d)
- Sessions ........ XX,XXX  (+/-X% WoW)
- Users ........... XX,XXX  (+/-X% WoW)
- Engagement rate . XX%     (+/-X pts WoW)

Conversions (7d vs prior 7d)
| Key event | This week | Last week | WoW | Revenue |
|-----------|-----------|-----------|-----|---------|

Channel mix
| Channel | Sessions (WoW) | Conv (WoW) |
|---------|----------------|------------|

Recommended actions
1. ...
```

### 7. Save this week's snapshot

Call `write_context_node` on `insights/ga4/monitor/latest` with this week's metrics
(sessions, users, engagement, per-key-event conversions + revenue, channel mix) so
next week can compute deltas. Also write a dated copy to
`insights/ga4/monitor/<YYYY-MM-DD>`.

### 8. Record findings — selectively

Only file a `create_finding` for genuine problems — a key event that stopped, a
channel that collapsed, a `(not set)` spike. A clean week files nothing.

```json
{
  "title": "GA4 key event 'generate_lead' dropped to 0 this week",
  "body": "'generate_lead' recorded 96 conversions last week and 0 this week while sessions held steady. The form tag or its GTM trigger has broken. Check GTM Preview on the form page and the GA4 DebugView.",
  "action_type": "tracking_break",
  "expected_outcome": "Lead tracking restored; Ads bidding gets signal again",
  "estimated_impact_usd": 0,
  "priority": "critical"
}
```

Action types: `tracking_break`, `data_quality`, `conversion_setup`,
`channel_anomaly`.

## Critical rules

1. **Trends over snapshots.** Every metric ships with a WoW delta.
2. **A key event at zero is critical** — it usually means a broken tag, and it
   corrupts Ads bidding too. Cross-check `/gtm-monitor` if GTM is connected.
3. **Lead with what's broken.** A clean week is one short paragraph.
4. **Read-only.** Surface issues; never change the property.
