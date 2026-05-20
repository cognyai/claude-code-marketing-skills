---
name: gtm-monitor
description: Weekly GTM container check — new, edited and removed tags, unpublished draft changes, orphaned tags, workspace status — diffed week-over-week
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-tag-manager]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__google_tag_manager__tool_list_accounts
  - mcp__cogny__google_tag_manager__tool_list_containers
  - mcp__cogny__google_tag_manager__tool_list_tags
  - mcp__cogny__google_tag_manager__tool_list_triggers
  - mcp__cogny__google_tag_manager__tool_list_variables
  - mcp__cogny__google_tag_manager__tool_get_tag
  - mcp__cogny__google_tag_manager__tool_get_workspace_status
  - mcp__cogny__create_finding
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  - WebFetch
---

# GTM Monitor

A recurring weekly check on a Google Tag Manager container. Containers don't drift on
their own — people change them. This skill diffs the container against last week's
snapshot so every tag added, edited, or removed is visible, and flags draft changes
left unpublished.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

Designed to be scheduled weekly via `/loop` or `/schedule`.

## Prerequisites Check

If `mcp__cogny__google_tag_manager__tool_list_tags` is not available, print the Cogny
sign-up instructions (see `/gtm-audit`) and stop.

## Usage

`/gtm-monitor` — weekly change + health check on the connected container.

For a full one-time review, run `/gtm-audit`. This is the light weekly rhythm.

## Steps

### 1. Read the prior snapshot

Call `read_context_node` on `insights/gtm/monitor/latest`. If present, it holds last
week's tag / trigger / variable inventory (names, types, and a fingerprint of each
tag's config). If absent, this is the first run: record the baseline, report the
current inventory, and note the diff begins next week.

### 2. Pull the current container state

```
tool_list_tags         (account_id, container_id, workspace_id)
tool_list_triggers     (account_id, container_id, workspace_id)
tool_list_variables    (account_id, container_id, workspace_id)
tool_get_workspace_status   (account_id, container_id, workspace_id)
```

### 3. Diff against last week

Compare current vs the snapshot:
- **Added** — tags / triggers / variables that did not exist last week
- **Removed** — items that existed last week and are now gone
- **Edited** — items whose config fingerprint changed (`tool_get_tag` for detail)

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

### 5. Unpublished changes

From `tool_get_workspace_status`: if the workspace has changes not yet published, the
live site is **behind** the container. Flag it — and if those changes have been
sitting unpublished for more than a week (compare to the snapshot), say so loudly.

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

Call `write_context_node` on `insights/gtm/monitor/latest` with the full current
inventory and per-tag fingerprints so next week can diff. Also write a dated copy to
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

Action types: `tag_change_review`, `tag_fix`, `trigger_fix`,
`consent_configuration`, `publish_pending`.

## Critical rules

1. **The diff is the point.** Always compare to last week's snapshot; a bare
   inventory with no diff is not a monitor.
2. **Changes to GA4 config / Ads conversion / consent tags are critical** — verify
   every one was intentional.
3. **Lead with what changed and what's broken.** A stable week is one short line.
4. **Read-only.** Never edit or publish the container.
