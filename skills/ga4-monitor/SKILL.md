---
name: ga4-monitor
description: Weekly GA4 check — sessions, users, key-event conversions, revenue, channel mix — with week-over-week deltas and tracking-break alerts
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-analytics-4, plausible, fathom-analytics, simple-analytics, adobe-analytics]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_get_property
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_realtime_report
  - mcp__cogny__mcp__Plausible__aggregate
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Plausible__realtime_visitors
  - mcp__cogny__mcp__Fathom_Analytics__list_sites
  - mcp__cogny__mcp__Fathom_Analytics__list_events
  - mcp__cogny__mcp__Fathom_Analytics__aggregate
  - mcp__cogny__mcp__Fathom_Analytics__current_visitors
  - mcp__cogny__mcp__Simple_Analytics__list_websites
  - mcp__cogny__mcp__Simple_Analytics__stats
  - mcp__cogny__mcp__Simple_Analytics__referrers
  - mcp__cogny__mcp__Simple_Analytics__events
  - mcp__cogny__mcp__Adobe_Analytics__list_report_suites
  - mcp__cogny__mcp__Adobe_Analytics__list_metrics
  - mcp__cogny__mcp__Adobe_Analytics__list_dimensions
  - mcp__cogny__mcp__Adobe_Analytics__run_report
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__PostHog__list_projects
  - mcp__cogny__mcp__PostHog__list_insights
  - mcp__cogny__mcp__PostHog__get_insight
  - mcp__cogny__mcp__Mixpanel__run_segmentation
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  - WebFetch
---

# GA4 Monitor

A recurring weekly check on a GA4 property. It confirms data is still flowing, reports
traffic and conversions week-over-week, and — most importantly — catches the silent
failure mode: a key event that stopped firing because a tag broke.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

Designed to be scheduled weekly via `/loop` or `/schedule`.

## Works with

| Job | GA4 (primary) | Plausible | Fathom Analytics | Simple Analytics | Adobe Analytics |
|-----|---------------|-----------|------------------|------------------|-----------------|
| Heartbeat | `tool_run_realtime_report` | `realtime_visitors` | `current_visitors` | `stats` (start/end = today) | `run_report` on yesterday |
| Traffic WoW | `tool_run_report` | `aggregate` | `aggregate` (`entity: pageview`) | `stats` | `run_report` |
| Conversions WoW | `tool_list_conversion_events` + `tool_run_report` | `breakdown` (`event:goal`) | `list_events` + `aggregate` (`entity: event`) | `events` | `run_report` (your success-event metrics) |
| Channel mix | `tool_run_report` (`sessionDefaultChannelGroup`) | `breakdown` (`visit:source`, `visit:utm_campaign`) | `aggregate` with `field_grouping: referrer_hostname` | `referrers` | `run_report` (marketing-channel dimension) |

Fathom Analytics here is the web analytics product, not the Fathom call recorder.
Enhanced when connected, with any of them: Shopify / WooCommerce orders and PostHog /
Mixpanel sign-ups confirm whether a conversion drop is real or a tracking break (Step 4).
Several connected: run the checks on each and show them side by side, never summed.

## Prerequisites Check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
GA4 Monitor needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Analytics 4 (or Plausible, Fathom
   Analytics, Simple Analytics or Adobe Analytics).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

Otherwise call `list_integrations` once. Use every healthy web-analytics provider from the table above;
name any broken one. `health_status` misses revoked tokens, so make one cheap read per provider
(GA4 `tool_list_account_summaries`, Adobe `list_report_suites`, Fathom `list_sites`, …): a 401,
Forbidden or scope error is 🔴 "reconnect <integration>", with no retry. If a tool named here is
missing, call `refresh_mcp_discovery` once; new tools only load after the client reconnects, so
skip that check this run and mark it ⚠ "needs reconnect". If no web-analytics provider is
connected, say "connect Google Analytics 4 (or Plausible, Fathom, Simple Analytics, Adobe) in
Cogny" and stop.

## Usage

`/ga4-monitor` — weekly health check of the connected GA4 property.

For a full one-time review, run `/ga4-audit`. This is the light weekly rhythm.

## Steps

### 1. Read the prior snapshot

Call `read_context_node` on `insights/ga4/monitor/latest`. If present, it holds last
week's numbers — report every metric as a delta against it. If absent, this is the
first run: report absolutes and note deltas begin next week.

Tool blocks below are GA4. For other providers use the "Works with" row; what differs is
noted in each step.

### 2. Data-flow heartbeat

```
tool_run_realtime_report   (property_id, metrics: activeUsers)
```

If realtime shows zero active users on a site with normal traffic, tagging may be
down. Note it, but confirm against the 7-day report before alarming.

Other providers: `Plausible__realtime_visitors` (`site_id`),
`Fathom_Analytics__current_visitors` (`site_id`). Simple and Adobe have no realtime tool, so
use today's (Simple `stats`) or yesterday's (Adobe `run_report`) totals instead.

### 3. Traffic & engagement (last 7d vs prior 7d)

```
tool_run_report   (property_id,
  date_ranges: [{"startDate": "7daysAgo", "endDate": "yesterday"},
                {"startDate": "14daysAgo", "endDate": "8daysAgo"}],
  metrics: ["sessions", "totalUsers", "newUsers", "engagementRate", "averageSessionDuration"])
```

Pin the windows exactly like this: both are 7 full days and today's partial day is excluded, so
the delta isn't skewed. Use the same two ranges in steps 4 and 5, and the same calendar dates for
other providers. Report each metric with its WoW delta.

| Provider | Call (run twice: this week, prior week) | Metric names |
|----------|------------------------------------------|--------------|
| Plausible | `aggregate` (`site_id`, `date_range: [start, end]`) | `visitors`, `visits`, `bounce_rate`, `visit_duration` |
| Fathom | `aggregate` (`entity: pageview`, `entity_id: <site id>`, `date_from`, `date_to`) | `visits`, `uniques`, `bounce_rate`, `avg_duration` |
| Simple Analytics | `stats` (`hostname`, `start`, `end`) | pageviews, visitors |
| Adobe | `run_report` (`rsid`, `start_date`, `end_date`, `dimension: variables/daterangeday`, `metrics`) | `metrics/visits`, `metrics/visitors` |

Map "sessions" to visits and "users" to visitors. These tools have no engagement rate;
report bounce rate instead and say so.

### 4. Key-event conversions (the critical check)

```
tool_list_conversion_events   (property_id)
tool_run_report   (property_id, same two date_ranges as step 3,
  dimensions: eventName,
  metrics: eventCount, keyEvents, totalRevenue)
```

Use `keyEvents`, not the deprecated `conversions` metric. **Join the report against
`tool_list_conversion_events`**, not the other way round: a key event with zero events in both
weeks returns no row at all, so start from the key-event list and fill missing rows with 0.
A key event at 0 / 0 is 🟡 "never fires" (a dead or misnamed event; event names are
case-sensitive, so check `/gtm-audit` for a `first_login` vs `FirstLogin` mismatch).

🔴 Alert if any key event recorded conversions last week and **zero this week** — the
tag or GTM trigger has almost certainly broken. This is the single most important
check in the skill.

🟡 Flag key events that dropped >50% WoW without an obvious traffic cause.

Same check on other providers, run on each conversion:

| Provider | Conversions this week vs last | Can't check |
|----------|-------------------------------|-------------|
| Plausible | `breakdown` (`dimension: event:goal`, `metrics: [visitors, events, conversion_rate]`) per week | Which goals count as conversions (all goals do); revenue unless revenue goals exist |
| Fathom | `list_events` (`site_id`), then `aggregate` (`entity: event`, `entity_id: <event id>`) per event | Revenue unless the event carries a value |
| Simple Analytics | `events` (`hostname`, `start`, `end`) | Key-event config; revenue |
| Adobe | `run_report` with your success-event metrics (find them with `list_metrics`) | Which events are "key" lives in the report suite, not the API |

**Confirm a drop against the source of truth (enhanced when connected).** Before calling
a drop a tracking break, check the same two weeks where the conversion really happens:
Shopify `tool_list_orders` (`query_filter: "created_at:>=YYYY-MM-DD"`) or WooCommerce
`get_sales_report` (`date_min`, `date_max`) for orders; PostHog `list_insights`
(`project_id`, `search: "signup"`) → `get_insight`, or Mixpanel `run_segmentation`
(`event`, `from_date`, `to_date`) for sign-ups. Truth flat + analytics down = 🔴 tracking
break. Both down = a real demand drop; say so and skip the tracking alarm.

Only GA4 exposes a key-event config (`tool_list_conversion_events`). For the others, say in
the output that "key event" means the goals or events the user named.

### 5. Channel mix

```
tool_run_report   (property_id, same two date_ranges as step 3,
  dimensions: sessionDefaultChannelGroup,
  metrics: sessions, keyEvents)
```

🟡 Alert on:
- A jump in `Unassigned` / `(not set)` sessions — UTMs broke somewhere
- A `Direct` spike — often a tagging or redirect problem
- A channel that fell off a cliff (campaign ended, or tracking lost)

Other providers: Plausible `breakdown` (`visit:source`, and `visit:utm_campaign` for the
UTM check), Fathom `aggregate` (`field_grouping: referrer_hostname`), Simple `referrers`,
Adobe `run_report` on your marketing-channel dimension (`list_dimensions` if unsure).
These group by source rather than GA4's channel groups, so the `Unassigned` check becomes
"a jump in direct / no-referrer visits".

### 6. Output

```
GA4 Monitor — [Property Name] ([Provider])
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

Call `write_context_node` on `insights/ga4/monitor/latest` (other providers:
`insights/<provider>/monitor/latest`, e.g. `insights/plausible/monitor/latest`) with this week's metrics
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

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Trends over snapshots.** Every metric ships with a WoW delta.
2. **A key event at zero is critical** — it usually means a broken tag, and it
   corrupts Ads bidding too. Cross-check `/gtm-monitor` if GTM is connected.
3. **Lead with what's broken.** A clean week is one short paragraph.
4. **Read-only.** Surface issues; never change the property.
5. **Name the provider on every number.** Plausible visitors, Fathom uniques and GA4 users
   are counted differently; never add them together.
