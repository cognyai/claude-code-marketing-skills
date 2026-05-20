---
name: gtm-audit
description: Google Tag Manager container audit — tag health, orphaned and paused tags, duplicate GA4 config, trigger coverage, Consent Mode, naming, workspace hygiene
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-tag-manager]
user-invocable: true
argument-hint: "[full|tags|triggers|consent]"
allowed-tools:
  - mcp__cogny__google_tag_manager__tool_list_accounts
  - mcp__cogny__google_tag_manager__tool_list_containers
  - mcp__cogny__google_tag_manager__tool_list_tags
  - mcp__cogny__google_tag_manager__tool_list_triggers
  - mcp__cogny__google_tag_manager__tool_list_variables
  - mcp__cogny__google_tag_manager__tool_get_tag
  - mcp__cogny__google_tag_manager__tool_get_trigger
  - mcp__cogny__google_tag_manager__tool_get_variable
  - mcp__cogny__google_tag_manager__tool_get_workspace_status
  - mcp__cogny__google_tag_manager__tool_search_tags
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# GTM Audit

A one-time audit of a Google Tag Manager container. GTM rarely fails loudly — it fails
as a duplicate GA4 tag double-counting conversions, a tag with no trigger that never
fires, or analytics tags firing before consent. This skill reads the container and
finds those.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

If `mcp__cogny__google_tag_manager__tool_list_containers` is not available:

```
This skill requires Cogny's Google Tag Manager MCP server.

1. Sign up at https://cogny.com/agent
2. Connect your GTM account
3. Add Cogny to your .mcp.json (see the repo README)
4. Restart Claude Code
```

Stop here if the tools are missing.

## Usage

`/gtm-audit` — full container audit
`/gtm-audit tags` — tag health only
`/gtm-audit triggers` — trigger coverage only
`/gtm-audit consent` — Consent Mode wiring only

## Steps

### 1. Account & container discovery

```
tool_list_accounts
tool_list_containers   (account_id)
```

If multiple containers exist, ask which to audit. Note the container type (web vs
server) — this audit targets web containers.

### 2. Tag inventory

```
tool_list_tags         (account_id, container_id, workspace_id)
```

For tags that need detail, call `tool_get_tag`. Bucket every tag by type (GA4 config,
GA4 event, Google Ads conversion, Google Ads remarketing, Floodlight, custom HTML,
third-party).

Flag:
- **Paused tags** still sitting in the container (dead weight, or accidentally off)
- **More than one GA4 configuration tag** for the same Measurement ID — the classic
  double-counting bug
- Multiple tags sending the same event to the same destination
- Custom HTML tags doing what a native tag template should do (fragile, slow)
- Google Ads conversion tags with no conversion label / ID set

### 3. Trigger coverage

```
tool_list_triggers     (account_id, container_id, workspace_id)
```

Cross-reference every tag's `firingTriggerId` against the trigger list.

Flag:
- **Tags with no firing trigger** — they will never fire (orphaned)
- **Triggers attached to no tag** — dead triggers
- All Pages triggers on conversion or event tags (should fire on a specific event)
- Click / form triggers with no conditions (fire on every click — noisy, wrong data)

### 4. Variable hygiene

```
tool_list_variables    (account_id, container_id, workspace_id)
```

Flag:
- Data Layer Variables referenced by tags but **not defined**
- Defined variables referenced by nothing (clutter)
- No version of the consent-state variables if Consent Mode is expected

### 5. Consent Mode v2

Inspect tags and the container setup for Consent Mode wiring.

Flag:
- **Analytics / Ads tags firing with no consent check** — a compliance and data risk
  in the EEA and UK
- No consent initialization (default `denied` state) before tags load
- `ad_storage` / `analytics_storage` / `ad_user_data` / `ad_personalization` not all
  handled

### 6. GA4 wiring correctness

For each GA4 event tag (`tool_get_tag`):

Flag:
- Event tags **not referencing the GA4 config tag** (or no config tag at all)
- Event names that break GA4 rules — uppercase, spaces, reserved prefixes, >40 chars
  (cross-reference the `/ga4-events` conventions)
- Ecommerce event tags not reading the `ecommerce` object from the data layer
- Missing parameters on key conversion events (`value`, `currency`, `transaction_id`)

### 7. Naming & workspace status

```
tool_get_workspace_status   (account_id, container_id, workspace_id)
```

Flag:
- **Unpublished changes** sitting in the workspace — live site is behind the container
- No naming convention (`GA4 - Event - purchase` style) — unmaintainable at scale
- Many open workspaces (merge-conflict risk)

### 8. Score and report

```
GTM Audit — [Container Name]
Container Health Score: X/100

Score breakdown:
  Tag health ......... X/25   (duplicates, orphans, paused)
  Trigger coverage ... X/20
  GA4 wiring ......... X/20
  Consent Mode ....... X/20
  Hygiene ............ X/15   (naming, variables, workspace)

Inventory: X tags · X triggers · X variables  ·  Unpublished changes: [yes/no]

🔴 Critical   — duplicate GA4 config, tags firing before consent
🟡 Important  — orphaned tags, bad event names, missing parameters
🟢 Optimization — naming, unused variables, custom HTML to native

Top 3 Actions:
1. [Highest impact]
2. ...
3. ...
```

### 9. Record findings

```json
{
  "title": "Two GA4 configuration tags for G-XXXX — every page view counted twice",
  "body": "'GA4 - Config' and 'GA4 Base (old)' both load Measurement ID G-XXXX on All Pages. GA4 is counting every page_view and session twice, inflating traffic and deflating conversion rate. Pause the older tag and republish.",
  "action_type": "tag_fix",
  "expected_outcome": "Accurate GA4 traffic and conversion-rate numbers",
  "estimated_impact_usd": 0,
  "priority": "critical"
}
```

Action types: `tag_fix`, `trigger_fix`, `consent_configuration`,
`container_hygiene`, `ga4_wiring`.

## Critical rules

1. **Duplicate GA4 config tags and pre-consent firing are always critical** — they
   corrupt data and create compliance exposure.
2. **An orphaned tag fires nothing** — say which tags are dead and why.
3. **Quote real numbers**: tag/trigger/variable counts, the specific tag names.
4. **Read-only.** Never edit or publish the container — surface and recommend.
