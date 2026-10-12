---
name: drop-off-rescue
description: Find contacts stalled at funnel stages (abandoned cart, signed-up-but-no-trial, trial-but-no-convert), draft stage-appropriate re-engagement emails, and schedule sends via your ESP — with dedupe so weekly reruns never double-send
version: "1.1.2"
requires: cogny-mcp
author: Cogny AI
platforms: [klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, drip, salesforce-marketing-cloud, symplify, braze, shopify, woocommerce, stripe]
user-invocable: true
argument-hint: "[weekly|audit|free]"
allowed-tools:
  # Cogny Cloud (aggregated) namespace
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Klaviyo__list_profiles
  - mcp__cogny__mcp__Klaviyo__get_profile
  - mcp__cogny__mcp__Klaviyo__list_lists
  - mcp__cogny__mcp__Klaviyo__get_list
  - mcp__cogny__mcp__Klaviyo__get_list_profiles
  - mcp__cogny__mcp__Klaviyo__list_segments
  - mcp__cogny__mcp__Klaviyo__get_segment
  - mcp__cogny__mcp__Klaviyo__list_campaigns
  - mcp__cogny__mcp__Klaviyo__get_campaign
  - mcp__cogny__mcp__Klaviyo__get_campaign_message
  - mcp__cogny__mcp__Klaviyo__get_campaign_values_report
  - mcp__cogny__mcp__Klaviyo__list_flows
  - mcp__cogny__mcp__Klaviyo__get_flow
  - mcp__cogny__mcp__Klaviyo__list_metrics
  - mcp__cogny__mcp__Klaviyo__get_metric
  - mcp__cogny__mcp__Klaviyo__list_events
  - mcp__cogny__mcp__Klaviyo__list_templates
  - mcp__cogny__mcp__Klaviyo__get_account
  - mcp__cogny__mcp__Mailchimp__tool_get_account_info
  - mcp__cogny__mcp__Mailchimp__tool_list_campaigns
  - mcp__cogny__mcp__Mailchimp__tool_get_campaign
  - mcp__cogny__mcp__Mailchimp__tool_get_campaign_content
  - mcp__cogny__mcp__Mailchimp__tool_list_audiences
  - mcp__cogny__mcp__Mailchimp__tool_get_audience
  - mcp__cogny__mcp__Mailchimp__tool_list_members
  - mcp__cogny__mcp__Mailchimp__tool_get_member
  - mcp__cogny__mcp__Mailchimp__tool_get_member_tags
  - mcp__cogny__mcp__Mailchimp__tool_list_segments
  - mcp__cogny__mcp__Mailchimp__tool_get_segment
  - mcp__cogny__mcp__Mailchimp__tool_list_templates
  - mcp__cogny__mcp__Mailchimp__tool_get_template
  - mcp__cogny__mcp__Mailchimp__tool_list_reports
  - mcp__cogny__mcp__Mailchimp__tool_get_report
  - mcp__cogny__mcp__Mailchimp__tool_get_report_click_details
  - mcp__cogny__mcp__Mailchimp__tool_get_report_open_details
  - mcp__cogny__mcp__Mailchimp__tool_get_report_unsubscribed
  - mcp__cogny__mcp__Mailchimp__tool_list_automations
  - mcp__cogny__mcp__Mailchimp__tool_get_automation
  - mcp__cogny__mcp__Rule__tool_list_subscribers
  - mcp__cogny__mcp__Rule__tool_get_subscriber
  - mcp__cogny__mcp__Rule__tool_get_subscriber_fields
  - mcp__cogny__mcp__Rule__tool_list_subscriber_tags
  - mcp__cogny__mcp__Rule__tool_list_tags
  - mcp__cogny__mcp__Rule__tool_get_tag
  - mcp__cogny__mcp__Rule__tool_list_campaigns
  - mcp__cogny__mcp__Rule__tool_get_campaign
  - mcp__cogny__mcp__Rule__tool_get_campaign_statistics
  - mcp__cogny__mcp__Rule__tool_list_templates
  - mcp__cogny__mcp__Rule__tool_get_template
  - mcp__cogny__mcp__Rule__tool_list_segments
  - mcp__cogny__mcp__Rule__tool_list_customizations
  - mcp__cogny__mcp__Rule__tool_get_customization
  - mcp__cogny__mcp__Rule__tool_list_suppressions
  - mcp__cogny__mcp__Rule__tool_list_preference_groups
  - mcp__cogny__mcp__Rule__tool_get_subscriber_preferences
  - mcp__cogny__mcp__Rule__tool_list_journeys
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_contacts
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_contact
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_lists
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_list
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_drafts
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_draft
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_sent
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_sent
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_scheduled
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_reports
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_bounces
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_opens
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_opens_aggregated
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_have_not_opened
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_clicks
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_link_clicks
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_unsubscriptions
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_attributes
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_subscriptions
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_senders
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_sender
  # Newer ESPs and stores: read tools only (tag writes and sends ask first)
  - mcp__cogny__mcp__Brevo__list_contacts
  - mcp__cogny__mcp__Brevo__get_contact
  - mcp__cogny__mcp__Brevo__list_contact_lists
  - mcp__cogny__mcp__Brevo__get_list
  - mcp__cogny__mcp__Brevo__list_contact_attributes
  - mcp__cogny__mcp__Brevo__list_email_campaigns
  - mcp__cogny__mcp__MailerLite__list_subscribers
  - mcp__cogny__mcp__MailerLite__get_subscriber
  - mcp__cogny__mcp__MailerLite__list_groups
  - mcp__cogny__mcp__MailerLite__get_group
  - mcp__cogny__mcp__MailerLite__list_campaigns
  - mcp__cogny__mcp__Drip__list_subscribers
  - mcp__cogny__mcp__Drip__get_subscriber
  - mcp__cogny__mcp__Drip__list_tags
  - mcp__cogny__mcp__Drip__list_workflows
  - mcp__cogny__mcp__Drip__list_campaigns
  - mcp__cogny__mcp__Drip__list_event_actions
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_journeys
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_data_extensions
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_data_extension_fields
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_data_extension_rows
  - mcp__cogny__mcp__Symplify__list_journeys
  - mcp__cogny__mcp__Braze__braze_list_canvases
  - mcp__cogny__mcp__Braze__braze_list_segments
  - mcp__cogny__mcp__Braze__braze_get_segment_analytics
  - mcp__cogny__mcp__Shopify__tool_list_abandoned_checkouts
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__Shopify__tool_list_customers
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  # Cogny Solo / Lite (per-ESP direct) namespace
  - mcp__klaviyo__*
  - mcp__mailchimp__*
  - mcp__rule__*
  - mcp__get_a_newsletter__*
  - WebFetch
  - Bash
  - Read
  - Write
---

# Drop-off Rescue

Push stalled funnel contacts to the next step. This skill finds people who signed up but didn't convert, drafts stage-appropriate re-engagement emails, and (with an ESP MCP connected) schedules the send after explicit confirmation. Re-runnable weekly without double-sending — the skill tracks what was already sent per stage and skips contacts still inside their cooldown window.

**Works in three modes:**
- `cloud` — Cogny MCP + ESP MCP: full automation, cross-ESP dedupe, findings
- `solo` — ESP MCP only: tag-based dedupe, per-ESP automation
- `free` — no MCP: pasted CSV of stalled contacts, draft-only output (you send manually)

## Usage

```
/drop-off-rescue              # weekly rerun — default
/drop-off-rescue weekly       # same
/drop-off-rescue audit        # read-only: report stalls + what would be sent, write nothing
/drop-off-rescue free         # no MCP — paste CSV of stalled contacts
```

Designed to be scheduled weekly via `/loop` or `/schedule`. On reruns, already-nudged contacts are skipped; newly-stalled contacts are picked up; contacts that progressed get celebrated in the output.

## Works with

| ESP (Prefix) | Read stage cohort | Write stage / rescue state (asks first) | Send / schedule (asks first) | Flow-conflict check |
|--------------|-------------------|------------------------------------------|------------------------------|---------------------|
| Klaviyo (`Klaviyo`) | `list_profiles`, `get_segment` | `update_profile` | `create_campaign` | `list_flows` |
| Mailchimp (`Mailchimp`) | `tool_list_members` (no tag filter: filter on each member's tags client-side, or use the tag's static segment from `tool_list_segments`), `tool_get_member_tags` | `tool_update_member_tags` | `tool_create_campaign` → `tool_schedule_campaign` | `tool_list_automations` |
| Rule (`Rule`) | `tool_list_subscribers`, `tool_list_subscriber_tags` | `tool_add_subscriber_tags`, `tool_remove_subscriber_tag` | `tool_schedule_campaign` | `tool_list_journeys` |
| Get a Newsletter (`Get_a_Newsletter`) | `tool_list_contacts` + `tool_get_contact` (no tags: stage = list membership or a `STAGE` attribute) | `tool_update_contact` (`attributes`; `lists` only with the full list set, see Layer 1), `tool_create_attribute` / `tool_create_list` for setup | `tool_send_draft` (`time_to_send`) | — (no flows) |
| Brevo (`Brevo`) | `get_list` / `list_contacts` (no tags: stage = list membership or a contact attribute) | `add_contacts_to_list`, `update_contact` (`attributes`) | `create_email_campaign` (`recipients`, `scheduled_at`) | not exposed — ask the user |
| MailerLite (`MailerLite`) | `list_groups` → `list_subscribers` + `get_subscriber` (groups per subscriber) | `assign_subscriber_to_group` (groups stand in for tags) | `create_campaign` → `schedule_campaign` | not exposed — ask the user |
| Drip (`Drip`) | `list_subscribers` (`tags: "stage:<slug>"`) — native tag filter | `apply_tag`, `remove_tag` | `subscribe_to_campaign` / `start_subscriber_on_workflow` | `list_workflows` |
| Salesforce Marketing Cloud (`Salesforce_Marketing_Cloud`) | `get_data_extension_rows` (`row_filter`) on a stage data extension | none in the MCP | none — draft-only | `list_journeys` |
| Symplify (`Symplify`) | no bulk contact read | none | none — draft-only | `list_journeys` |
| Braze (`Braze`) | `braze_list_segments` → `braze_get_segment_analytics` (cohort **size** only, no members) | none | none — draft-only | `braze_list_canvases` |

**Store data for e-commerce stages (enhanced when connected, works with any ESP):**

| Stage | Shopify (`Shopify`) | WooCommerce (`WooCommerce`) |
|-------|---------------------|-----------------------------|
| `checkout-abandoned` / `cart-abandoned` | `tool_list_abandoned_checkouts` (email, `total_price`, line items, `abandonedCheckoutUrl`), minus emails with a later order in `tool_list_orders` | `list_orders` (`status: "pending"` or `"failed"`, `after`) as a proxy |
| `post-first-order-silent` | `tool_list_customers` (`numberOfOrders` = 1) + `tool_list_orders` for the order date | `list_orders` grouped by billing email |

**SaaS stages from Stripe (enhanced when connected):** `stripe_api_read` `GetSubscriptions` (`status: "all"`) gives `trialing` subscriptions (for `trial-started-inactive`) and trials that ended `canceled` or `incomplete_expired` without a paid invoice (for `no-subscription` / `trial-ended-no-convert`); `GetInvoices` (`status: "paid"`) and `GetRefunds` give the paid-plan value used for impact sizing. For SaaS, Stripe is the revenue source wherever this skill uses store orders.

Store (or Stripe) data finds the cohort; the ESP still holds consent and the rescue tags. Join on lowercased email and drop anyone the ESP marks unsubscribed. If Stripe's `email`/`customer_email` comes back `[REDACTED]` (a restricted key), skip the Stripe join and say so ("Stripe emails redacted by the restricted key: SaaS stages can't be matched to ESP contacts"); use Stripe only for impact sizing. Page Stripe with `limit` 20–25 and `starting_after` (a 100-row page is ~370KB).

## Step 0 — Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`) and no Solo per-ESP tools (`mcp__<esp>__*`) either, print this, then run free mode (Step 9):

```
Drop-off Rescue needs your marketing data through Cogny's MCP gateway to find stalled contacts and schedule sends.

1. Sign up at https://cogny.com and connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite or Drip); Shopify, WooCommerce or Stripe adds cart and trial stages.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: paste a CSV of stalled contacts (email,stage,stalled_since,consent) and get draft-only emails you send yourself (free mode).
```

If Cogny is connected but no ESP is, say "connect your ESP in Cogny" and offer free mode.

## Step 1 — Mode detection

Probe both MCP namespaces:

1. If `mcp__cogny__<svc>__*` tools are present for at least one ESP → **cloud** mode (and record that ESP as connected).
2. Else if `mcp__<svc>__*` tools are present for at least one ESP → **solo** mode.
3. Else → **free** mode.

If the argument is `free`, force free mode regardless of what's connected.

If multiple ESPs are connected, ask the user which one to run against (or offer to run all and cross-dedupe in cloud mode). On Cloud, `mcp__cogny__list_integrations` lists them; name any unhealthy integration as broken.

**Health check:** `health_status` misses revoked tokens, so make one cheap read per integration before relying on it (e.g. Mailchimp `tool_get_account_info`, Get a Newsletter `tool_list_senders`, Klaviyo `get_account`, Shopify `tool_list_orders` with a 1-day filter, Stripe `stripe_api_read` `GetSubscriptions` with `limit: 1`). A 401, Forbidden or scope error means 🔴 "reconnect <integration> in Cogny": name it, don't retry, and drop that source from this run (an ESP that fails means its stages run as drafts only).

**Missing tool:** if a tool named here isn't exposed by the workspace, call `mcp__cogny__refresh_mcp_discovery` once, use the fallback named next to the tool for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh. Get a Newsletter fallbacks: `tool_get_report_have_not_opened` → that report's list contacts minus the openers from `tool_get_report_opens`; `tool_get_report_link_clicks` → `tool_get_report_opens` (per-contact click counts) or `tool_get_report_clicks` (per-link totals); `tool_get_report_opens_aggregated` → the totals in `tool_get_report`. Mailchimp `tool_get_campaign_content` → `tool_get_campaign` for the headers, and ask the user for the body.

**ESP connected but 0 sends in the window:** Layer 2 (send-history scan, Step 4) has nothing to read for that ESP; skip it with a one-line note ("Get a Newsletter: 0 sends in the last 35 days — send-history dedupe skipped") and rely on Layers 1 and 3.

Brevo, MailerLite, Drip, Salesforce Marketing Cloud, Symplify and Braze are Cloud-namespace only. SFMC, Symplify and Braze have no write tools in the MCP, so they always run **audit + drafts**: dedupe relies on Layer 3 (context tree) and the user sends from the ESP.

## Step 2 — Canonical funnel stages

The skill works against a canonical stage taxonomy. The user can extend it, but these slugs drive tag names, campaign naming, and dedupe state — keep them stable across runs.

**E-commerce:**
| Slug | Meaning | Typical stall |
|------|---------|---------------|
| `browse-abandoned` | Viewed product, never added to cart | 1–3 days |
| `cart-abandoned` | Added to cart, never checked out | 1–2 days |
| `checkout-abandoned` | Started checkout, didn't submit | hours–1 day |
| `post-first-order-silent` | Made first order, no engagement since | 14–30 days |

**SaaS / trial funnel:**
| Slug | Meaning | Typical stall |
|------|---------|---------------|
| `signup` | Created account, did nothing | 1–3 days |
| `no-channel` | Signed up, no data source / integration connected | 3–7 days |
| `no-trial` | Connected a channel, hasn't started the free trial | 7 days |
| `no-client` | Trial active, hasn't connected the tool/client that uses it | 3 days |
| `no-subscription` | Trial ended, didn't convert to paid | 0–3 days after trial |
| `trial-started-inactive` | Started trial, no meaningful usage | 3–5 days |
| `trial-ended-no-convert` | Trial ended, didn't subscribe | 7 days after end |

Cogny's own Solo funnel (signup → `no-channel` → `no-trial` → `no-client` → `no-subscription`) is a good reference implementation of this taxonomy.

If the user describes a funnel with stages that don't map to these slugs, add new kebab-case slugs — just keep them stable across reruns (the slug is the dedupe key).

## Step 3 — Resolve current stage per contact

**Primary signal: ESP tags / segments.** Read contacts tagged `stage:<slug>` using the per-ESP tool:

| ESP | Read stage tag | Apply stage tag | Schedule/send |
|-----|----------------|-----------------|---------------|
| Klaviyo | `list_profiles` filtered by segment/property `stage` | `update_profile` (properties) | campaign create + schedule |
| Mailchimp | `tool_list_members` (no tag filter: page with `count`/`offset` and keep members whose tags include `stage:<slug>`, or count/target the tag's static segment from `tool_list_segments`) | `tool_update_member_tags` | campaign schedule |
| Rule | `tool_list_subscribers` filtered by tag | `tool_add_subscriber_tags` | `tool_schedule_campaign` |
| Get a Newsletter (no tags) | contacts on a `stage:<slug>` list (each contact's `lists`), or with a `STAGE` attribute (`tool_get_contact`) | `tool_update_contact` (`attributes: {"STAGE": "<slug>"}`) | `tool_send_draft` with `time_to_send` |
| Brevo | `get_list` for a `stage:<slug>` list, or contacts with a `STAGE` attribute | `add_contacts_to_list` / `update_contact` (`attributes`) | `create_email_campaign` with `scheduled_at` |
| MailerLite | subscribers in a `stage:<slug>` group | `assign_subscriber_to_group` | `create_campaign` → `schedule_campaign` |
| Drip | `list_subscribers` with `tags` | `apply_tag` | `subscribe_to_campaign` (Email Series) or `start_subscriber_on_workflow` |
| SFMC / Symplify / Braze | see Works with (read-only or size-only) | — | — (draft-only) |

**Store-derived stages (any ESP, when Shopify or WooCommerce is connected and the stage tag is absent):** build `checkout-abandoned` / `cart-abandoned` from `tool_list_abandoned_checkouts` (last 7 days, excluding emails with a later order in `tool_list_orders`) and `post-first-order-silent` from `tool_list_customers`; on WooCommerce use `list_orders`. Offer (under the Step 7 gate) to write the stage tag back so the next run reads it directly. Drip accounts fed by a store integration may also have purchase events: check `list_event_actions`.

**Klaviyo event-derived fallback (only when `stage:cart-abandoned` tag is absent):** query `list_events` with `metric="Added to Cart"` in the last 7 days, exclude profiles who have a subsequent `Placed Order`. Write the `stage:cart-abandoned` tag back via `update_profile` so the next run is consistent.

**Conversational fallback (any ESP, when no stage tags exist at all):**

1. Ask the user: "I don't see any `stage:*` tags on your contacts. Which of these funnel stages apply to your business?" — list the canonical slugs.
2. For each picked stage, ask: "Who is on this stage? Describe the condition — e.g. `joined list > 3 days ago AND no purchase`, or `clicked email X but never visited /signup`."
3. Translate each heuristic into the ESP's available filters (list membership, tags, date ranges, clicked links) and preview the matching count.
4. Offer (under the confirmation gate in Step 7) to apply `stage:<slug>` tags now, so future runs are fully automated.

## Step 4 — Already-sent detection (the core mechanism)

Weekly reruns must not re-send the same stage email to the same contact. The skill uses a **three-layer hybrid**:

### Layer 1 — contact tag (primary, all modes with an ESP connected)

On every successful send, write three tags to the recipient:

- `rescue-sent:<slug>:<YYYY>-W<WW>` — append-only; one per week nudged
- `rescue-last-stage:<slug>` — overwritten; always reflects the latest stage nudged (enables stage-advancement detection in one read)
- `rescue-last-sent:<YYYY-MM-DD>` — overwritten; used for cooldown math and the global 7-day anti-fatigue rule

Why tag-based primary: works in solo mode without a context tree, survives cross-machine usage, debuggable by a human in the ESP UI, bulk-clearable if something goes wrong. Klaviyo, Mailchimp, Rule and Drip have tag writes. **Get a Newsletter has no tags** (`tool_list_attributes` returns attributes only and `tool_update_contact` takes `attributes` and `lists`, nothing else): store `RESCUE_LAST_STAGE` and `RESCUE_LAST_SENT` as contact attributes (create them once with `tool_create_attribute` if `tool_list_attributes` lacks them) and record `rescue-sent:<slug>:<week>` as one list per rescue week (`tool_create_list`). ⚠ Per the tool's own docstring, passing `lists` to `tool_update_contact` **unsubscribes the contact from every list not included**: to add a rescue-week list, send the contact's current lists (from `tool_get_contact`) plus the new one, or omit `lists` and write attributes only. Brevo has no tags either: use contact attributes (`RESCUE_LAST_STAGE`, `RESCUE_LAST_SENT`, created by the user if `list_contact_attributes` lacks them) and one list per `rescue-sent:<slug>:<week>`. MailerLite uses groups with the same names. SFMC, Symplify and Braze have no writes, so Layer 3 is their only dedupe.

### Layer 2 — ESP campaign-name convention (fallback)

Every rescue campaign is named exactly:

```
drop-off-rescue / <stage-slug> / <YYYY>-W<WW> / <variant A|B>
```

On rerun, if a contact's tags were stripped (manual edit, sync tool), `list_campaigns` / `tool_list_campaigns` / `tool_list_sent` in the last 35 days is scanned for matching names. Recipients are cross-referenced via the per-ESP report tool (`list_events`, `tool_get_report`, `tool_get_campaign_statistics`, `tool_get_report`).

**Deliberately no markers in subject or preheader** — the user-visible inbox copy stays clean.

### Layer 3 — Cogny context-tree log (cloud mode only)

Write on every send:

```
insights/drop-off-rescue/<slug>/<sha256(email)[:12]>/last-sent
  → { "week": "2026-W17", "variant": "A", "esp": "klaviyo", "ts": "2026-04-24T10:00Z" }
```

Read on the next run. This layer catches cross-ESP duplication — the same contact living in both Klaviyo and Mailchimp under the same org won't get two nudges in the same week.

### Dedupe decision

A contact is classed **"already nudged at current stage within cooldown"** if **any** of the three layers reports a hit inside the cooldown window. Cooldown defaults (printed in output, user-overridable):

| Stage | Cooldown |
|-------|----------|
| `cart-abandoned`, `checkout-abandoned` | 7d |
| `browse-abandoned`, `signup`, `no-channel` | 14d |
| `no-trial`, `no-client`, `no-subscription`, `trial-started-inactive` | 21d |
| `post-first-order-silent`, `trial-ended-no-convert` | 30d |

## Step 5 — Classify every contact (the weekly loop)

For each stage, read the full `stage:<slug>` cohort, then classify each contact:

| Class | Condition | Action this run |
|-------|-----------|-----------------|
| **New stall** | On `stage:<slug>` now, no `rescue-sent:<slug>:*` ever | Eligible — variant A |
| **Cooldown skip** | Has `rescue-sent:<slug>:<week>` inside the stage's cooldown window | Skip, count as "cooldown-skipped" |
| **Re-stall** | Past cooldown, still on `stage:<slug>`, ≤2 prior rescue sends at this stage | Eligible — variant B (tone shift) |
| **Progressed** | `rescue-last-stage` is an earlier stage than the current stage tag | Celebrate in output; nudge at new stage |
| **Regressed** | `rescue-last-stage` is a later stage than the current stage tag | Flag as anomaly, don't auto-nudge (data issue) |
| **Exhausted** | 3 prior rescue sends at this stage without progression | Apply `rescue-exhausted:<slug>`, exclude until stage changes |
| **Exited** | No stage tag at all, but has `rescue-last-stage` | Clear all `rescue-*` tags in cleanup pass |

**Hard caps (enforced regardless of per-stage cooldowns):**

- **3 nudges max per contact per stage** before they go to `rescue-exhausted:<slug>`.
- **Max one rescue email per contact per rolling 7 days across all stages.** If a contact would be hit for two stages in one week, emit only the higher-priority stage (priority order: `cart-abandoned` > `checkout-abandoned` > `browse-abandoned` > `signup` > `no-channel` > `no-trial` > `no-client` > `no-subscription` > activation-stages > `post-first-order-silent` > `trial-ended-no-convert`) and defer the other.

## Step 6 — Draft emails per stage

For every stage with ≥1 eligible contact, draft **two variants**:

- **Variant A** — direct, short, outcome-led. For first-time nudges.
- **Variant B** — value-led, longer, addresses likely objections. For re-stalls (second+ nudge at the same stage).

For every variant produce:

```
Stage: <slug>
Variant: A | B
Subject:    <≤55 chars, in brand voice>
Preheader:  <85–100 chars, extends subject, never repeats it>
Body:       <markdown>
Primary CTA: <label> → <URL with UTM: utm_source=email&utm_medium=rescue&utm_campaign=<slug>-<YYYY>WWW&utm_content=<A|B>>
```

**Tone guidance per stage:**

| Stage | Variant A tone | Variant B tone |
|-------|----------------|----------------|
| `cart-abandoned` | Quick, helpful, "still thinking about X?" | Urgency + social proof + small incentive |
| `checkout-abandoned` | "Technical hiccup? We saved your cart." | Offer + friction-remover (guest checkout, Apple Pay) |
| `browse-abandoned` | Curiosity, reference the viewed category | Content-led (buying guide, comparison) |
| `signup` / `no-channel` | Helpful, "the one step that unlocks it" | Founders' note, reply-to-me tone |
| `no-trial` / `no-client` / `no-subscription` | Clear next action + short how-to | Objection-handling ("what's holding you back?") |
| `post-first-order-silent` | Thank-you + relevant follow-up | Cross-sell + reminder of brand value |
| `trial-started-inactive` | "Here's the fastest win you can get in 5 min" | Use case + customer example |
| `trial-ended-no-convert` | "Any reason this didn't land?" | Small discount + plan recommendation |

Use the brand's actual voice — if the user has a brand URL, WebFetch it first to pick up tone. No "Dear Valued Customer" filler. One primary CTA per email.

## Step 7 — Confirmation gate (before any write)

**No MCP write tool fires before the user explicitly approves.** This applies to both tag applications (Step 3 fallback) and email sends / schedules.

For every stage that has eligible contacts, print this block verbatim and wait:

```
About to send via <ESP>. Nothing has been sent yet.

Stage:            <slug>       (<N> eligible)
Cooldown applied: <d>d         (<M> skipped as already-nudged)
Exhausted:        <K>          (hit 3-nudge cap — excluded)
Variant:          A | B        (<label — e.g. "first nudge" or "re-stall, value-led">)
Schedule:         <ISO timestamp, recipient-local>  |  immediate
Campaign name:    drop-off-rescue / <slug> / <YYYY>-WWW / <A|B>

Dry-run preview (first 3 recipients):
  1. <email>    subject: <rendered>
  2. <email>    subject: <rendered>
  3. <email>    subject: <rendered>

State writes on send:
  - tag rescue-sent:<slug>:<YYYY>-WWW  → <N> contacts
  - tag rescue-last-stage:<slug>       → <N> contacts (overwrite)
  - tag rescue-last-sent:<YYYY-MM-DD>  → <N> contacts (overwrite)
  - context-tree log (cloud mode)      → <N> entries

Reply with:
  send           → execute now via ESP MCP
  schedule <ts>  → queue for that recipient-local time
  variant B      → switch variant and reprint this block
  skip           → don't send, but log a "no-send" finding and continue
  cancel         → abort everything, no writes
```

If the ESP lacks scheduling in the MCP (today: Salesforce Marketing Cloud, Symplify and Braze have no write tools), return the draft plus the segment definition and a suggested send time the user sets up in the ESP.

**Before scheduling, always check for flow conflicts:** read `list_flows` / `tool_list_automations` / `tool_list_journeys` / Drip `list_workflows` / SFMC `list_journeys` / Symplify `list_journeys` / Braze `braze_list_canvases`. Brevo and MailerLite don't expose automations: ask the user whether an abandoned-cart or onboarding automation already runs. If a native flow already targets a segment equivalent to the current stage, warn:

```
⚠️  Heads up — a native <ESP> flow already targets this segment:
    "<flow name>"  (last modified <date>, status: <active|paused>)

    Running rescue alongside it risks double-touching the contact. Options:
      [1] Pause rescue for this stage, let the native flow do the work
      [2] Pause the native flow, run rescue this week only
      [3] Proceed anyway (document the overlap)

    Which?
```

Get a Newsletter has no flow object, so this check is skipped there. If Shopify's own abandoned-checkout emails are on, treat them as a native flow for `checkout-abandoned`.

## Step 8 — Consent & suppression guards

Before any send:

- **Drop contacts with `consent:marketing = false`** (or the ESP equivalent: unsubscribed, cleaned, bounced, or on a suppression list).
- **Drop contacts in an active `rescue-exhausted:<slug>` state**.
- **Drop contacts with a `do-not-contact` / `gdpr-suppressed` tag** regardless of stage.
- In free mode, the pasted CSV must include a `consent` column; rows with `false`/`no`/`0` are dropped with a console warning.

If >10% of the eligible list is dropped for consent reasons, surface this at the top of the output — it usually means the user's list hygiene needs attention and a `/revenue-audit` or `/winback-engine` run first.

## Step 9 — Free mode (no MCP)

Triggered when neither `mcp__cogny__*` nor any `mcp__<esp>__*` resolves, or when the user passes `free` explicitly.

1. Ask the user to paste a CSV with columns: `email,stage,stalled_since,consent` (stage must be a slug from Step 2; `stalled_since` is ISO date; `consent` is `true`/`false`).
2. Ask for brand name + one-line brand voice (same lightweight discovery as `/welcome-series`). Optionally ask for a brand URL to WebFetch.
3. Draft both variants per stage.
4. Output a manual-send bundle:
   - One `.csv` of eligible contacts per stage (filtered for consent)
   - Drafted email copy (markdown + HTML) per variant per stage
   - A copy-paste subject/preheader table
5. **No state is persisted.** The user owns dedupe — output explicitly calls this out.
6. End with the upsell:

```
───────────────────────────────
Ready to stop managing this by hand?

Connect your ESP via Cogny MCP and the next run will:
  • Dedupe against what you've already sent
  • Apply rescue-sent:* tags automatically
  • Schedule the send directly in your ESP after your confirmation

→ https://cogny.com
───────────────────────────────
```

## Step 10 — Output format

```
Drop-off rescue — <ESP or "free mode"> — week <YYYY>-W<WW>
Mode: cloud | solo | free

Funnel movement since last run:
  new stalls:        +<N>
  progressions:      +<N>     (<stage_a> → <stage_b>: N; <stage_c> → <stage_d>: N)
  regressions:       <N>
  exited funnel:     <N>
  newly exhausted:   <N>

Consent drops: <N>  (<pct>% of eligible — <OK | run /revenue-audit>)

──────────────────────────────────────────────────────
Stage: cart-abandoned
  Eligible: <N>   Cooldown-skip: <M>   Exhausted: <K>
  Suggested variant: A     Send window: Tue–Thu, 10am recipient-local

  Top 10 eligible contacts:
  | email               | stalled since | prior nudges |
  |---------------------|---------------|--------------|
  | ...                 | 2026-04-21    | 0            |

  Email draft — variant A:
    Subject:    ...
    Preheader:  ...
    Body:       ...
    CTA:        [label] → <URL with UTM>

  Email draft — variant B:
    ...

  [confirmation block from Step 7]

──────────────────────────────────────────────────────
Stage: no-channel
  ...
```

One such block per stage with eligible contacts. Stages with zero eligible (everyone cooldown-skipped or exhausted) get a one-line summary instead of a full block.

## Step 11 — Findings (cloud mode)

For each stage with eligible contacts, record a finding. On Cloud call `create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `create_finding`:

```json
{
  "title": "Drop-off rescue: <N> contacts stalled at <stage-slug>",
  "body": "<N> contacts on stage:<slug> are past their cooldown. Variant <A|B> drafted; send scheduled for <ts or 'awaiting approval'>. Previous week: <M> contacts progressed out of this stage after rescue.",
  "action_type": "rescue_campaign",
  "expected_outcome": "<e.g. 'Expect 5–10% of cart-abandoners to complete checkout within 72h'>",
  "estimated_impact_usd": <number_or_null>,
  "priority": "<high|medium|low>"
}
```

`estimated_impact_usd` is computed only from real order data × a realistic reactivation rate (5–10% for cart stages, 2–5% for SaaS stages): Shopify abandoned-checkout `total_price` (cart stages), AOV from Shopify/WooCommerce orders, Klaviyo's `list_events`, or (SaaS stages) the paid-plan value from Stripe `GetInvoices`. Name the source and convert from the store currency only if the user gives a rate. Without order data, set to `null` and note "engagement uplift only."

Persist the weekly summary under `insights/drop-off-rescue/<YYYY>-W<WW>/summary` so next run can diff.

## Step 12 — End-of-run tag inventory

Final output section — gives the user visibility into state sprawl:

```
rescue-* tag inventory on <ESP>:
  rescue-sent:cart-abandoned:2026-W17   → 42 contacts
  rescue-sent:no-channel:2026-W17       → 18 contacts
  rescue-last-stage:cart-abandoned      → 67 contacts
  rescue-exhausted:no-channel           → 4 contacts
  rescue-last-stage:no-channel          → 22 contacts
  (... older weeks)

Cleanup: reply "clear weeks before 2026-W14" to bulk-remove old rescue-sent:* tags.
```

## Notes

- **Cart/order data comes from Klaviyo events or a connected store** (SaaS trial and subscription data from Stripe). Shopify (`tool_list_abandoned_checkouts`, `tool_list_orders`) and WooCommerce (`list_orders`) resolve `cart-abandoned` / `checkout-abandoned` / `post-first-order-silent` for any ESP. Without either, those stages rely entirely on tag-driven stage resolution — the user must be tagging contacts from their own e-com data.
- **Several ESPs connected:** report each ESP's cohort and sends separately; the cross-ESP dedupe (Layer 3) prevents double nudges but counts are never added across ESPs.
- **Get a Newsletter has no flow/automation object.** The Step 7 flow-conflict check is skipped. Rescue is always scheduled as individual drafts via `tool_send_draft` with `time_to_send`.
- **Klaviyo event-derived `cart-abandoned` is soft** — once the skill synthesises it from `list_events`, it immediately writes the tag via `update_profile` so the next run reads it from the primary signal.
- **Don't conflict with native flows.** If the user already runs a Klaviyo abandoned-cart flow, defer to it — the rescue skill is for stages where a native flow doesn't exist or isn't effective.
- **The 7-day global anti-fatigue cap is non-negotiable.** Even if a contact qualifies for three stages in one week, they get at most one rescue email that week, priority-ordered.
- **Weekly rerun via `/loop`:** `/loop 7d /drop-off-rescue weekly`. The skill's own state (tags + context tree) ensures idempotence — running it twice in one day is safe, it will just report "all contacts inside cooldown" the second time.
- **Reference implementation:** Cogny's own Solo funnel (at `src/app/api/admin/solo-funnel/` and `src/lib/email/reactivation-email.ts`) shows this pattern in production — 4 stage-specific templates, a `solo_reactivation_emails` log table tracking `stage_at_send` + `sent_at`, and an admin dashboard gating every send.

────────────────────────────────────────────────
Ready to automate the weekly nudge cycle?

Connect your ESP via Cogny MCP and the rerun will skip already-nudged contacts,
apply rescue state tags, and schedule sends directly — all gated by your approval.

→ https://cogny.com
────────────────────────────────────────────────

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
