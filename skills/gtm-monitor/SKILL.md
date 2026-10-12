---
name: gtm-monitor
description: Weekly GTM container check — new, edited and removed tags, unpublished draft changes, orphaned tags, workspace status — diffed week-over-week
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-tag-manager, google-analytics-4, plausible, microsoft-clarity]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_triggers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_variables
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_tag
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_workspace_status
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Microsoft_Clarity__get_live_insights
  - mcp__cogny__mcp__Microsoft_Clarity__get_insights_history
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  - WebFetch
---

# GTM Monitor

A recurring weekly check on a Google Tag Manager container. Containers don't drift on
their own — people change them. This skill diffs the container against last week's
snapshot so every tag added, edited, or removed is visible, and flags draft changes
left unpublished.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

Designed to be scheduled weekly via `/loop` or `/schedule`.

## Works with

| Job | Primary | Enhanced when connected |
|-----|---------|-------------------------|
| Container diff, orphans, unpublished changes | GTM | — |
| Did a changed tag stop sending data? | — | GA4 `tool_run_report`, or Plausible `breakdown` (`event:goal`) |
| Did a new tag break the page? | — | Microsoft Clarity `get_live_insights` (Script Error Count) |

## Prerequisites Check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
GTM Monitor needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Tag Manager (GA4, Plausible or
   Microsoft Clarity optional, to check downstream impact).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny: the container is only readable through the GTM API.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags` isn't, say
"connect Google Tag Manager in Cogny" and stop.

**Health check:** call `list_integrations`, then `tool_list_accounts` as the cheap read.
`health_status` misses revoked tokens, so a 401, Forbidden or scope error is 🔴 "reconnect
Google Tag Manager"; don't retry it. If a tool named here is missing, call
`refresh_mcp_discovery` once; new tools only load after the client reconnects, so mark that
check ⚠ "needs reconnect" for this run.

## Usage

`/gtm-monitor` — weekly change + health check on the connected container.

For a full one-time review, run `/gtm-audit`. This is the light weekly rhythm.

## Steps

### 1. Read the prior snapshot

Call `read_context_node` on `insights/gtm/monitor/latest`. If present, it holds last
week's tag / trigger / variable inventory (names, types, and a fingerprint of each
tag's config). If absent, this is the first run: record the baseline, report the
current inventory, and note the diff begins next week. The snapshot also holds the
`account_id`, `container_id` and `workspace_id` used last week; reuse them in Step 2.

### 2. Pull the current container state

**Pick the container.** If the snapshot has `account_id` and `container_id`, use them, and
skip discovery. Otherwise:

```
tool_list_accounts                                  → account_id (ask if several)
tool_list_containers   (account_id)                 → container_id
```

Pick the container whose `usageContext` contains `web`. If there are several web containers, ask
which one to monitor (show name and `publicId`, e.g. `GTM-XXXX`). Server, iOS and Android
containers are out of scope here.

```
tool_list_workspaces   (account_id, container_id)   → workspace_id (snapshot's, else Default Workspace)
tool_list_tags         (account_id, container_id, workspace_id)
tool_list_triggers     (account_id, container_id, workspace_id)
tool_list_variables    (account_id, container_id, workspace_id)
tool_get_workspace_status   (account_id, container_id, workspace_id)
```

### 3. Diff against last week

Compare current vs the snapshot:
- **Added** — tags / triggers / variables that did not exist last week
- **Removed** — items that existed last week and are now gone
- **Edited** — items whose `fingerprint` changed (`tool_get_tag` for detail)

Use GTM's own `fingerprint` field on each tag, trigger and variable as its fingerprint. GTM
changes it on every edit, so don't hash the config yourself.

For every change, name the item and what changed.

🔴 Flag as critical when the change touches a measurement-critical tag:
- A GA4 configuration tag edited or removed
- A Google Ads conversion tag edited or removed
- A consent-related tag or trigger changed
- A new analytics/marketing tag added with no consent check

### 4. Standing health checks

Re-run the fast checks from `/gtm-audit`:
- Tags with **no firing trigger** (orphaned — fire nothing)
- More than one GA4 config tag for the same Measurement ID
- Paused tags that were live last week (someone turned tracking off?)

### 4b. Downstream impact (enhanced when connected)

Only when Step 3 found a changed or removed measurement-critical tag. Call
`list_integrations` once and use what is healthy:

| Check | Call | Flag |
|-------|------|------|
| Event still arriving | GA4 `tool_run_report` (`property_id`, last 7d vs prior 7d, `dimensions: [eventName]`, `metrics: [eventCount]`, filtered to the tag's event) | 🔴 event at zero or down >50% since the change |
| Same, on Plausible | `breakdown` (`site_id`, `dimension: event:goal`, `date_range` per week) | same |
| Pages breaking | Clarity `get_live_insights` (`num_of_days: 3`, `metrics: [Script Error Count, Dead Click Count]`, `dimensions: [URL]`), against last week's `get_insights_history` | 🟡 script errors up on the pages the new tag fires on |

Clarity allows 10 live requests a day per project; one call per run is enough. If nothing
is connected, say "downstream impact not verified" next to the change.

### 5. Unpublished changes

From `tool_get_workspace_status`: if the workspace has changes not yet published, the
live site is **behind** the container. Flag it — and if those changes have been
sitting unpublished for more than a week (compare to the snapshot), say so loudly.

`tool_get_workspace_status` has no timestamps. Each changed entity's `fingerprint` is a
millisecond Unix epoch of its last edit, so use it as the change date (e.g. `1760000000000` →
2025-10-09). The oldest fingerprint among unpublished changes tells you how long they've waited;
save it in the snapshot so next week can compare.

### 6. Output

```
GTM Monitor — [Container Name]
Week of [YYYY-MM-DD] – [YYYY-MM-DD]

⚠️  Needs attention this week
- [Critical/important first, or "No changes — container stable."]

Changes since last week
- Added:   [N]  — [names]
- Edited:  [N]  — [names + what changed]
- Removed: [N]  — [names]

Health
- Orphaned tags: [N]
- Duplicate GA4 config: [yes/no]
- Unpublished changes: [yes — N changes, oldest X days / no]

Inventory: X tags · X triggers · X variables

Recommended actions
1. ...
```

### 7. Save this week's snapshot

Call `write_context_node` on `insights/gtm/monitor/latest` with `account_id`,
`container_id` and `workspace_id`, plus the full current inventory (id, name, type and
GTM `fingerprint` of every tag, trigger and variable) and the oldest unpublished-change
fingerprint, so next week can diff. Also write a dated copy to
`insights/gtm/monitor/<YYYY-MM-DD>`.

### 8. Record findings — selectively

Only file a `create_finding` for genuine concerns — a measurement-critical tag
changed, an orphaned tag, changes stuck unpublished. A stable week files nothing.

```json
{
  "title": "GA4 config tag edited this week — verify it was intentional",
  "body": "'GA4 - Config' was modified since last week's snapshot: the Measurement ID field changed. If unplanned, every GA4 hit may be routing to the wrong property. Confirm with whoever owns the container and check GA4 DebugView.",
  "action_type": "tag_change_review",
  "expected_outcome": "Change confirmed intentional, or reverted",
  "estimated_impact_usd": 0,
  "priority": "high"
}
```

On Cloud, `create_ticket` takes the same content with the fields mapped per section 2 of
the routing guide.

Action types: `tag_change_review`, `tag_fix`, `trigger_fix`,
`consent_configuration`, `publish_pending`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **The diff is the point.** Always compare to last week's snapshot; a bare
   inventory with no diff is not a monitor.
2. **Changes to GA4 config / Ads conversion / consent tags are critical** — verify
   every one was intentional.
3. **Lead with what changed and what's broken.** A stable week is one short line.
4. **Read-only.** Never edit or publish the container.
