---
name: gtm-audit
description: Google Tag Manager container audit — tag health, orphaned and paused tags, duplicate GA4 config, trigger coverage, Consent Mode, naming, workspace hygiene
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-tag-manager, google-analytics-4, meta-ads, tiktok-ads, linkedin-ads, reddit-ads, snapchat-ads, x-ads, segment]
user-invocable: true
argument-hint: "[full|tags|triggers|consent]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_triggers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_variables
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_tag
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_trigger
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_variable
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_workspace_status
  - mcp__cogny__mcp__Google_Tag_Manager__tool_search_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__mcp__Google_Tag_Manager__tool_audit_container_privacy
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_data_streams
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_pixels
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_pixels
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_conversions
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_conversion_events
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_pixels
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_web_event_tags
  - mcp__cogny__mcp__Segment__list_sources
  - mcp__cogny__mcp__Segment__list_destinations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# GTM Audit

A one-time audit of a Google Tag Manager container. GTM rarely fails loudly — it fails
as a duplicate GA4 tag double-counting conversions, a tag with no trigger that never
fires, or analytics tags firing before consent. This skill reads the container and
finds those.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Enhanced when connected |
|-----|---------|-------------------------|
| Container inventory, triggers, variables | GTM | — (GTM is the only tag manager in Cogny) |
| Consent / privacy scan | GTM `tool_audit_container_privacy` | — |
| Are the Measurement IDs real? | GTM tag config | GA4 `tool_list_data_streams` |
| Are pixel / conversion IDs current? | GTM tag config | Google Ads, Meta, TikTok, LinkedIn, Reddit, Snapchat, X (Step 6b) |
| Do event names match key events / Ads imports? | GTM tag config | GA4 `tool_list_conversion_events`, Google Ads `conversion_action` (Step 6c) |
| Double sending via a CDP | — | Segment `list_destinations` |

## Prerequisites Check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
GTM Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Tag Manager (GA4 and your ad platforms
   optional, to verify IDs and event names).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny: the container is only readable through the GTM API.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers` isn't, say
"connect Google Tag Manager in Cogny" and stop.

**Health check:** call `list_integrations`, then `tool_list_accounts` as the cheap read (and one
cheap read per platform used in Step 6b, e.g. `tool_list_ad_accounts`). `health_status` misses
revoked tokens, so a 401, Forbidden or scope error is 🔴 "reconnect <integration>"; don't retry
it. If a tool named here is missing, call `refresh_mcp_discovery` once; new tools only load after
the client reconnects, so mark that check ⚠ "needs reconnect" for this run.

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
server) — this audit targets web containers. Then `tool_list_workspaces` (`account_id`,
`container_id`) for the `workspace_id` every later call needs (use the Default Workspace
unless the user names another).

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

```
tool_audit_container_privacy   (account_id, container_id, workspace_id)
```

Start from its list of tags without consent triggers, third-party trackers and
cookie variables, then inspect tags and the container setup for Consent Mode wiring.

The privacy tool only counts GA4 tag types, so it misses pixels pasted into Custom HTML. Also:
- Scan every Custom HTML tag (`type: html`; the code is in the `html` parameter, so
  `tool_get_tag` if `tool_list_tags` didn't return it) for `fbq(` (Meta), `twq(` (X),
  `ttq.` (TikTok), `lintrk(` / `_linkedin_partner_id` (LinkedIn). Count each as a third-party tracker.
- Read every tag's `consentSettings.consentStatus`: `needed` (with the required consent types)
  is wired, `notNeeded` is an explicit opt-out, and `notSet` / missing means no additional consent
  check. A marketing pixel with `notSet` and an All Pages trigger is a 🔴 consent finding.

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

### 6b. IDs against the connected platforms (enhanced when connected)

Call `list_integrations` once. For each healthy platform, read the IDs it actually owns
and compare with the IDs hard-coded in GTM tags:

| Platform | Read the IDs | Matches the GTM tag's |
|----------|--------------|-----------------------|
| GA4 | `tool_list_account_summaries` → `tool_list_data_streams` (`property_id`) | Measurement ID (`G-…`) |
| Google Ads | `tool_list_accessible_accounts` → `customer_id` (digits only; ask if several) → `tool_execute_gaql` (`customer_id`): `SELECT conversion_action.name, conversion_action.type, conversion_action.status, conversion_action.tag_snippets FROM conversion_action` | Conversion ID + label |
| Meta | `tool_list_ad_accounts` → `tool_get_pixels` (`ad_account_id`) | Pixel ID |
| TikTok | `tool_list_advertisers` → `tool_get_pixels` (`advertiser_id`) | Pixel code |
| LinkedIn | `tool_list_ad_accounts` → `tool_get_conversions` (`ad_account_id`) | Partner ID / conversion IDs |
| Reddit | `tool_list_ad_accounts` → `tool_get_conversion_events` (`ad_account_id`) | Pixel ID |
| Snapchat | `tool_list_ad_accounts` → `tool_list_pixels` (`ad_account_id`) | Pixel ID |
| X | `tool_list_ad_accounts` → `tool_get_web_event_tags` (`account_id`) | Pixel / event tag IDs |

Flag:
- 🔴 A tag sending to an ID the platform doesn't list (old property, deleted pixel, another
  client's account): data goes nowhere or somewhere wrong. **Exception, GA4:** a Measurement ID
  missing from `tool_list_data_streams` is 🟡 "not listed or not accessible", not 🔴. The
  connected Google login may simply lack access to that property; ask the user to confirm it
- 🟡 A platform conversion action (status `ENABLED`) with no GTM tag behind it, unless it is
  imported from GA4 or sent server-side. Google Ads actions whose `conversion_action.type`
  starts with `GOOGLE_ANALYTICS_4_` are GA4 imports: they never have an `AW-` tag, so don't
  flag them "no AW- tag" (check them in Step 6c instead)
- 🟡 Segment `list_destinations` shows a GA4 or ad-platform destination **and** GTM fires the
  same tag: likely double counting. Ask which path is meant to be live.

Platforms that aren't connected, **or whose read returned any API error** (401, scope, quota,
GAQL error): say "IDs not verified" for their tags. An error is never evidence that an ID is wrong.

### 6c. Event names match key events and Ads imports (case-sensitive)

Collect the event name each GA4 event tag sends (`eventName` parameter). When `eventName` is
`{{Event}}` (the built-in variable that forwards the dataLayer event), the tag's own config
holds no name: take the names from its firing triggers instead (`firingTriggerId` →
`tool_get_trigger`, type `customEvent`, the `arg1` value of each condition in
`customEventFilter`, e.g. `FirstLogin`; with a regex match, list each alternative). Skipping
this misses the `first_login` vs `FirstLogin` mismatch below. Compare each name,
**exactly and case-sensitively**, with:
- GA4 `tool_list_conversion_events` (`property_id`): every key event's `eventName`
- Google Ads GA4 imports from Step 6b: actions with `type` `GOOGLE_ANALYTICS_4_CUSTOM` /
  `GOOGLE_ANALYTICS_4_PURCHASE` (the import name ends in the GA4 event name)

Flag:
- 🔴 A key event or Ads import whose name matches a GTM event only when case or separators are
  ignored (e.g. GTM sends `first_login`, GA4 key event is `FirstLogin`). GA4 event names are
  case-sensitive, so the key event never fires and the Ads import stays at zero. This was the
  root cause of dead key events in a live run.
- 🟡 A key event with no GTM tag sending it at all (unless it's an automatic or
  enhanced-measurement event, or sent from code / server-side; ask)

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
  GA4 wiring ......... X/20   (incl. key-event name matches)
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

On Cloud, `create_ticket` takes the same content with the fields mapped per section 2 of
the routing guide.

Action types: `tag_fix`, `trigger_fix`, `consent_configuration`,
`container_hygiene`, `ga4_wiring`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Duplicate GA4 config tags and pre-consent firing are always critical** — they
   corrupt data and create compliance exposure.
2. **An orphaned tag fires nothing** — say which tags are dead and why.
3. **Quote real numbers**: tag/trigger/variable counts, the specific tag names.
4. **Read-only.** Never edit or publish the container — surface and recommend. Fixes
   go through `/gtm-setup`, where every write asks first.
5. **Only call an ID wrong when the platform was read.** Unverified is not wrong.
