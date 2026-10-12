---
name: winback-engine
description: Find dormant subscribers, segment by historical value, draft personalized winback emails per tier, and identify suppression candidates
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, drip, salesforce-marketing-cloud, braze, shopify, woocommerce, stripe]
user-invocable: true
argument-hint: "[aggressive|standard|conservative]"
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
  # Newer ESPs and stores: read tools only (writes ask first)
  - mcp__cogny__mcp__Brevo__list_contacts
  - mcp__cogny__mcp__Brevo__get_contact
  - mcp__cogny__mcp__Brevo__list_contact_lists
  - mcp__cogny__mcp__MailerLite__list_subscribers
  - mcp__cogny__mcp__MailerLite__get_subscriber
  - mcp__cogny__mcp__MailerLite__list_groups
  - mcp__cogny__mcp__MailerLite__list_segments
  - mcp__cogny__mcp__Drip__list_subscribers
  - mcp__cogny__mcp__Drip__get_subscriber
  - mcp__cogny__mcp__Drip__list_tags
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_data_extensions
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_data_extension_fields
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_data_extension_rows
  - mcp__cogny__mcp__Braze__braze_list_segments
  - mcp__cogny__mcp__Braze__braze_get_segment_details
  - mcp__cogny__mcp__Braze__braze_get_segment_analytics
  - mcp__cogny__mcp__Shopify__tool_list_customers
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - mcp__cogny__write_context_node
  # Cogny Solo / Lite (per-ESP direct) namespace
  - mcp__klaviyo__*
  - mcp__mailchimp__*
  - mcp__rule__*
  - mcp__get_a_newsletter__*
  - Bash
  - Read
  - Write
---

# Winback Engine

Turn dormant subscribers back into customers. This skill scans your connected ESP for inactive subscribers, segments them by historical value, drafts a personalized winback series per tier, and flags who you should suppress before they tank your deliverability.

**Requires:** Cogny MCP + a connected ESP. [Sign up](https://cogny.com)

The output is a complete, ready-to-run winback campaign — not a report.

## Usage

`/winback-engine` — standard mode (60-day dormancy threshold)
`/winback-engine aggressive` — 30-day threshold (acts earlier, bigger list)
`/winback-engine conservative` — 90-day threshold (only chronic dormants)

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Winback Engine needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Drip, Salesforce Marketing Cloud or Braze); Shopify, WooCommerce or Stripe adds purchase value.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Prerequisites Check

Detect connected ESP (same pattern as subject-line-lab; on Cloud, `mcp__cogny__list_integrations`). If Cogny is connected but no ESP is, say "connect your ESP in Cogny" and stop. Also note whether a store (Shopify, WooCommerce) or, for SaaS, Stripe is connected — it supplies purchase data for ESPs that have none.

**Health check:** `health_status` misses revoked tokens, so make one cheap read per integration before relying on it (e.g. Mailchimp `tool_get_account_info`, Get a Newsletter `tool_list_senders`, Klaviyo `get_account`, Shopify `tool_list_customers` with a small page, Stripe `stripe_api_read` `GetSubscriptions` with `limit: 1`). A 401, Forbidden or scope error means 🔴 "reconnect <integration> in Cogny": name it, don't retry, and continue with what remains.

**Missing tool:** if a tool named here isn't exposed by the workspace, call `mcp__cogny__refresh_mcp_discovery` once, use the fallback named next to the tool for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh. Get a Newsletter fallbacks: `tool_get_report_have_not_opened` → that report's list contacts minus the openers from `tool_get_report_opens`; `tool_get_report_link_clicks` → `tool_get_report_opens` (per-contact click counts) or `tool_get_report_clicks` (per-link totals); `tool_get_report_opens_aggregated` → the totals in `tool_get_report`. Mailchimp `tool_get_campaign_content` → `tool_get_campaign` for the headers, and ask the user for the body.

**ESP connected but 0 sends in the window:** skip it with a one-line note ("Rule: connected, 0 sends in the last <threshold> days — no engagement to tier; see step 2 for never-mailed contacts").

## Works with

| ESP (Prefix) | Subscribers + engagement | Purchase / LTV | Suppression write (asks first) | Coverage |
|--------------|--------------------------|----------------|--------------------------------|----------|
| Klaviyo (`Klaviyo`) | `list_profiles`, `get_profile` | `list_events` (Placed Order metric) | `unsubscribe_profiles` | Full |
| Mailchimp (`Mailchimp`) | `tool_list_members` | store join | `tool_update_member` | Full, engagement-tiered |
| Rule (`Rule`) | `tool_list_subscribers`, `tool_list_suppressions` | store join | `tool_update_subscriber` | Full, engagement-tiered |
| Get a Newsletter (`Get_a_Newsletter`) | `tool_list_contacts` (**no engagement fields**) + `tool_get_report_opens` (paged, per report) to rebuild engagement | store join | `tool_update_contact` / `tool_delete_contact` | Partial: last-engaged is rebuilt from recent reports only, so it can't see engagement older than the reports you page through |
| Brevo (`Brevo`) | `list_contacts` (`modified_since`), `get_contact` (per-contact `statistics` with open/click events) | store join | `update_contact` (`email_blacklisted: true`) | Full, but last-engaged needs one `get_contact` per contact — sample if the list is large |
| MailerLite (`MailerLite`) | `list_subscribers` (`filter_status: "active"`): lifetime `opens_count`, `clicks_count`, `open_rate`, `subscribed_at` | store join | `upsert_subscriber` (`status: "unsubscribed"`) | No last-open date: tier on lifetime rates + tenure, and say so |
| Drip (`Drip`) | `list_subscribers` (`status: "active"`, `tags`) | subscriber `lifetime_value` (when a store integration feeds Drip) | `unsubscribe_from_all` | No per-subscriber last-open date; use `lifetime_value` + tags |
| Salesforce Marketing Cloud (`Salesforce_Marketing_Cloud`) | `list_data_extensions` → `get_data_extension_fields` → `get_data_extension_rows` (`row_filter`) on an engagement or customer data extension | same, if the data extension holds orders | none in the MCP; hand over the list | Only if such a data extension exists; rows are PII, fetch only what's needed |
| Braze (`Braze`) | `braze_list_segments` → `braze_get_segment_details` / `braze_get_segment_analytics` (sizes only) | — | none in the MCP | **Partial:** sizes existing lapsed segments; can't list users, so tiers and the suppression list are recommendations to build in Braze |
| Symplify, Drip broadcasts | — | — | — | Symplify has no bulk contact read (only `get_contact` by id), so winback isn't possible there |

**Store join (any ESP):** `mcp__cogny__mcp__Shopify__tool_list_customers` returns `numberOfOrders` and `amount_spent` per customer email; WooCommerce `list_orders` (`after`, `status: "completed"`) gives order history. For SaaS, Stripe `stripe_api_read` `GetSubscriptions` (`status: "all"`) gives active vs cancelled customers and `GetInvoices` (`status: "paid"`) the billed total per customer (LTV); treat cancelled subscribers as past purchasers. Join on lowercased email to turn engagement-only tiers into value tiers. If Stripe's `email`/`customer_email` comes back `[REDACTED]` (a restricted key), skip the Stripe join and say so ("Stripe emails redacted by the restricted key: tiers stay engagement-only"). Page Stripe with `limit` 20–25 and `starting_after` (a 100-row page is ~370KB). Name the source ("LTV from Shopify"), use the store currency, and never mix ESP-attributed revenue with store revenue.

## Steps

### 1. Define dormancy thresholds

| Mode | Dormant | Deep dormant | Suppress candidate |
|------|---------|--------------|-------------------|
| aggressive | 30+ days no open | 90+ days no open | 180+ days no open/click, no purchase |
| standard | 60+ days | 180+ days | 365+ days no engagement |
| conservative | 90+ days | 270+ days | 540+ days |

### 2. Pull subscriber data

From the connected ESP, pull every active subscriber with:
- Subscribe date
- Last open date + last click date (take max as last_engaged)
- Total historical opens / clicks
- Signup source / list
- Tags / segments
- Email domain (gmail, yahoo, hotmail, corporate)

**Purchase / LTV data — Klaviyo, Drip (`lifetime_value`), or a connected store.** The cogny-mcp-proxy exposes purchase data in Klaviyo (via `list_events` filtered to the "Placed Order" metric, summing the `value` field per profile) and Drip. With Shopify or WooCommerce connected, use the store join above for any ESP. Otherwise Mailchimp, Rule, Get a Newsletter, Brevo and MailerLite are **engagement-only** — they do not expose:
- Total spend / LTV
- Order count
- AOV
- Last order date

**Get a Newsletter engagement rebuild:** `tool_list_contacts` returns no open or click fields. Rebuild them per contact: list the sends in the window with `tool_list_sent` (each row has subject, send time and `report_id`), skip test sends (under 10 recipients or "test" in the subject), then page through `tool_get_report_opens` for each `report_id` (each row: email, opens, clicks). A contact's last_engaged is the send time of the latest report they appear in; lifetime opens/clicks are the sums. `tool_get_report_opens` returns **only openers**, so "mailed but never opened" has to be derived: use `tool_get_report_have_not_opened` if the workspace exposes it; otherwise take the contacts on the lists that send targeted (`tool_get_sent`, matched against each contact's `lists`) whose `created` is before the send time, minus that report's openers. Cover at least the deep-dormant threshold (e.g. 180 days in standard mode) and state the date range, because engagement older than the oldest report read is invisible.

**Last send older than the dormancy threshold:** if the ESP's most recent send is older than the dormant threshold, every contact is dormant by default. That says nothing about the people; it means the program stopped sending. Say so up front, tier only contacts who were actually mailed, and treat the cadence gap as the main finding.

**Never-mailed contacts:** contacts created after the last send (Get a Newsletter: `tool_list_contacts` with `created_gt` = last send time), or on lists no send has targeted, have never received an email. They aren't dormant, so keep them out of the tiers and the suppression list: count them separately and route them to `/welcome-series`.

**Per-ESP tool adapter:**

| ESP | Subscriber list | Purchase history | Suppression write |
|-----|-----------------|------------------|-------------------|
| Klaviyo | `list_profiles` (+ `get_profile` for detail) | `list_events` with `metric="Placed Order"` — use `value` field per profile for LTV | `unsubscribe_profiles` |
| Mailchimp | `tool_list_members` (filter `status=subscribed`) | **Not available** | `tool_update_member` (status=unsubscribed) |
| Rule | `tool_list_subscribers` | **Not available** | `tool_update_subscriber` / `tool_list_suppressions` |
| Get a Newsletter | `tool_list_contacts` + `tool_get_report_opens` (engagement rebuild above) | **Not available** | `tool_delete_contact` or `tool_update_contact` |
| Brevo | `list_contacts` + `get_contact` | **Not available** (store join) | `update_contact` (`email_blacklisted`) |
| MailerLite | `list_subscribers` | **Not available** (store join) | `upsert_subscriber` (`status`) |
| Drip | `list_subscribers` | `lifetime_value` on the subscriber | `unsubscribe_from_all` |
| SFMC | `get_data_extension_rows` | only if a data extension holds it | not exposed |
| Braze | segment sizes only | not exposed per user | not exposed |

### 3. Segment into tiers

**If Klaviyo, Drip with `lifetime_value`, or any ESP + store join (has purchase data):** cross-cut by **engagement recency** × **historical value**:

| Tier | Criteria | Tone | Offer |
|------|----------|------|-------|
| **A — High value dormant** | Dormant + LTV ≥ top quartile OR past purchaser | Personal, apologetic, premium | Strong (20% off, free shipping, exclusive access). This is real money. |
| **B — Medium value dormant** | Dormant + some past engagement or 1 purchase | Warm, value-forward | Moderate (10–15% off, bundle, content) |
| **C — Low engagement dormant** | Dormant + never purchased + low engagement history | Direct, honest | Last-chance offer or content-only |
| **D — Suppression candidates** | Deep dormant + no purchase + no recent engagement | Final email only | "We're removing you unless..." |

**If engagement-only (Mailchimp / Rule / Get a Newsletter / Brevo / MailerLite with no store connected):** tier by **engagement depth** instead. LTV-based tiering falls back to:

| Tier | Criteria | Tone | Offer |
|------|----------|------|-------|
| **A — Deep engaged dormant** | Dormant now, but historically high open+click rate (top quartile of clicks) | Personal, "we miss you" | Strong offer or exclusive content |
| **B — Casual dormant** | Dormant, moderate historical engagement | Warm, value-forward | Modest offer |
| **C — Low engagement dormant** | Dormant, few lifetime opens/clicks | Direct, honest | Content-only or re-opt-in ask |
| **D — Suppression candidates** | Deep dormant, minimal lifetime engagement | Final email only | Goodbye |

Revenue estimates in the output should be omitted for engagement-only ESPs, or marked `estimated_impact_usd: null` on findings with a note that the user can pair with their own LTV data to size the opportunity.

Output the tier sizes before drafting:

```
Winback candidates: <total>
├─ Tier A (high-value dormant):   <count> subscribers (est. revenue: $<X>)
├─ Tier B (medium):               <count>
├─ Tier C (low engagement):       <count>
└─ Tier D (suppression):          <count>  ← do not keep sending to these

Never mailed (not tiered):        <count>  → run /welcome-series
```

**Revenue estimate for Tier A/B:** `count × historical AOV × expected reactivation rate` (use 3-5% for Tier A, 1-2% for Tier B).

### 4. Draft a 3-email winback series per tier

For each tier (A, B, C), generate 3 emails with cadence:
- **Email 1** — day 0, soft reopener ("we noticed")
- **Email 2** — day 4, value + offer
- **Email 3** — day 8, last-chance / decision

Tone by tier:

**Tier A (high-value):**
- E1: Personal note, reference last purchase by name if available. No offer yet.
- E2: Show what they're missing — new products in their category, or customer stories
- E3: Strongest offer, explicit decision framing ("if we're not a fit anymore, we'll respect that")

**Tier B (medium):**
- E1: "We miss you" + social proof
- E2: Content-led (best of what they missed) + modest offer
- E3: Offer + deadline

**Tier C (low engagement):**
- E1: Direct — "is this still useful?"
- E2: One-click re-subscribe or one-click unsubscribe (reduce friction)
- E3: Final send before suppression

For every email produce: subject, preheader, body, CTA. Same format as `/welcome-series`.

### 5. Suppression list (Tier D)

Output a block the user can act on:

```
Suppression recommendation: <count> subscribers

These haven't opened, clicked, or purchased in <threshold> days. Keeping
them on the list:
  • Hurts deliverability (low engagement = more spam placement for everyone)
  • Inflates list size → higher ESP costs
  • Distorts reporting baselines

Recommended action:
  1. Send ONE final "goodbye" email offering resubscribe
  2. After 7 days, suppress non-responders

Sample suppression email is included below.
```

Then include the goodbye email draft.

### 6. Write-mode: offer to execute

After presenting the plan, ask:

```
I can push this into your ESP as:
  [A] Drafts only (you review + launch)
  [B] Full flow installed but paused (you activate when ready)
  [C] Just give me the copy, I'll handle it

Which?
```

If the user picks A or B and the ESP MCP has write tools available, follow the **Write Action Protocol** (same as the `/cogny` skill — present the action plan, wait for approval, then execute one step at a time).

Draft-capable writes for the newer ESPs (each asks first): Brevo `create_email_campaign` (omit `scheduled_at` to keep it a draft), MailerLite `create_campaign` (then `schedule_campaign` only on approval), Drip `apply_tag` to enter an existing winback workflow. SFMC and Braze have no write tools in the MCP: deliver copy + segment definitions only (option C).

### 7. Record findings

For each significant tier (A, B with >100 subscribers), and for a never-mailed group or a stopped send cadence, record a finding. On Cloud call `create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `create_finding`:

```json
{
  "title": "Tier A winback: <N> high-value dormant subscribers, est. $<X> recoverable",
  "body": "Identified <N> past purchasers with LTV in top quartile who haven't engaged in <days> days. Avg historical AOV: $<Y>. At 4% reactivation, estimated winback revenue = $<X>. 3-email series drafted and ready to install.",
  "action_type": "winback_campaign",
  "expected_outcome": "Reactivate 3-5% of Tier A dormant, generate $<X> over 30 days",
  "estimated_impact_usd": <X>,
  "priority": "high"
}
```

And one for suppression:

```json
{
  "title": "<N> subscribers recommended for suppression",
  "body": "Deep dormant (<threshold>+ days) with no purchases. Keeping them hurts deliverability and inflates ESP cost. Recommend goodbye email + suppression after 7 days.",
  "action_type": "list_hygiene",
  "expected_outcome": "Improve overall open rate by 1-3 pp, lower ESP tier cost",
  "estimated_impact_usd": <monthly_esp_savings>,
  "priority": "medium"
}
```

## Notes

- **Never suppress before a winback attempt.** Give Tier D subscribers one last chance to re-engage.
- Apple MPP means "last open" is noisy for iPhone users. Weight **clicks** and **purchases** higher than opens when assigning tiers.
- **Purchase/LTV data** comes from Klaviyo events, Drip `lifetime_value`, a connected Shopify/WooCommerce store, or Stripe for SaaS. Without one of those, Mailchimp, Rule, Get a Newsletter, Brevo and MailerLite fall back to the engagement-only tiering scheme above.
- **Several ESPs connected:** tier each list separately and show them side by side. A person on two lists counts once per ESP; don't add tier sizes or revenue estimates across ESPs.
- **Get a Newsletter has no flow/automation object.** "Install as a flow" isn't available — winback is delivered as scheduled individual sends via `tool_send_draft` with `time_to_send`. For Klaviyo, flows install via the Klaviyo UI (the MCP exposes `list_flows`/`get_flow` for reads only, not create). For Mailchimp/Rule, automations/journeys are read-only too — so "install" means drafting campaigns and scheduling them, not creating a native automation.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
