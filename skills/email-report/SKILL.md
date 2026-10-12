---
name: email-report
description: Auto-generate the weekly or monthly email performance report in three formats — Slack update, CEO email, board-deck section — from real ESP data
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, drip, salesforce-marketing-cloud, symplify, braze, shopify, woocommerce, abicart, litium, stripe, google-analytics-4, plausible]
user-invocable: true
argument-hint: "[weekly|monthly] [slack|ceo|deck|all]"
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
  # Newer ESPs, stores and analytics: read tools only
  - mcp__cogny__mcp__Brevo__list_email_campaigns
  - mcp__cogny__mcp__Brevo__get_email_campaign
  - mcp__cogny__mcp__Brevo__list_contact_lists
  - mcp__cogny__mcp__Brevo__get_smtp_report
  - mcp__cogny__mcp__MailerLite__list_campaigns
  - mcp__cogny__mcp__MailerLite__get_campaign
  - mcp__cogny__mcp__MailerLite__list_groups
  - mcp__cogny__mcp__MailerLite__list_subscribers
  - mcp__cogny__mcp__Drip__list_campaigns
  - mcp__cogny__mcp__Drip__get_campaign
  - mcp__cogny__mcp__Drip__list_workflows
  - mcp__cogny__mcp__Drip__list_subscribers
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_email_sends
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_journey_email_performance
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_triggered_sends
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_triggered_send_summary
  - mcp__cogny__mcp__Symplify__get_campaign_overview
  - mcp__cogny__mcp__Symplify__get_campaign_report
  - mcp__cogny__mcp__Symplify__list_journeys
  - mcp__cogny__mcp__Braze__braze_list_campaigns
  - mcp__cogny__mcp__Braze__braze_get_campaign_details
  - mcp__cogny__mcp__Braze__braze_get_campaign_analytics
  - mcp__cogny__mcp__Braze__braze_list_canvases
  - mcp__cogny__mcp__Braze__braze_get_canvas_summary
  - mcp__cogny__mcp__Braze__braze_list_email_unsubscribes
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__Abicart__get_sales_summary
  - mcp__cogny__mcp__Litium__get_sales_summary
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Plausible__aggregate
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
  - Bash
  - Read
  - Write
---

# Email Report

The 3-hour tax every email marketer pays: pulling last period's numbers, charting the trend, explaining the variance, and writing commentary in the right voice for the audience. This skill does it in one command and outputs three versions — Slack ping, CEO email, board deck section — so you can ship the one your stakeholder needs.

**Requires:** Cogny MCP + a connected ESP. [Sign up](https://cogny.com)

## Usage

`/email-report` — monthly report, all three formats (default)
`/email-report weekly` — last 7 days
`/email-report monthly ceo` — monthly, only the CEO email
`/email-report weekly slack` — weekly, only the Slack update

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Email Report needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Drip, Salesforce Marketing Cloud, Symplify or Braze); a store, Stripe or GA4 adds revenue context.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

When Cogny is connected but no ESP is, say "connect your ESP in Cogny" and stop; a connected integration that fails its health check gets "reconnect <integration> in Cogny".

## Prerequisites Check

Detect connected ESP (on Cloud, `mcp__cogny__list_integrations`; name any unhealthy integration as broken). If none, stop and prompt. Also note which store (Shopify, WooCommerce, Abicart, Litium), billing source (Stripe, for SaaS) and web analytics (GA4, Plausible) are connected — they supply revenue and email-driven sessions.

**Health check:** `health_status` misses revoked tokens, so make one cheap read per integration before relying on it (e.g. Mailchimp `tool_get_account_info`, Get a Newsletter `tool_list_senders`, Klaviyo `get_account`, GA4 `tool_run_report` for one day, Stripe `stripe_api_read` `GetSubscriptions` with `limit: 1`). A 401, Forbidden or scope error means 🔴 "reconnect <integration> in Cogny": name it, don't retry, and report from the rest.

**Missing tool:** if a tool named here isn't exposed by the workspace, call `mcp__cogny__refresh_mcp_discovery` once, use the fallback named next to the tool for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh. Get a Newsletter fallbacks: `tool_get_report_have_not_opened` → that report's list contacts minus the openers from `tool_get_report_opens`; `tool_get_report_link_clicks` → `tool_get_report_opens` (per-contact click counts) or `tool_get_report_clicks` (per-link totals); `tool_get_report_opens_aggregated` → the totals in `tool_get_report`. Mailchimp `tool_get_campaign_content` → `tool_get_campaign` for the headers, and ask the user for the body.

**ESP connected but 0 sends in the window:** skip that ESP's campaign section with a one-line note ("Rule: connected, 0 sends in <period>") and keep its list-size numbers. If **no** ESP sent anything in the period, see "Zero sends in the period" in step 2.

## Works with

| ESP (Prefix) | Campaigns + metrics | Flows / journeys | List size + growth | ESP-attributed revenue |
|--------------|---------------------|------------------|--------------------|------------------------|
| Klaviyo (`Klaviyo`) | `list_campaigns`, `get_campaign_values_report` | `list_flows`, `get_flow` | `list_profiles` | ✓ (`get_campaign_values_report` with `conversion_metric_id` = Placed Order) |
| Mailchimp (`Mailchimp`) | `tool_list_campaigns`, `tool_get_report` | `tool_list_automations`, `tool_get_automation` | `tool_get_audience` | ✗ |
| Rule (`Rule`) | `tool_list_campaigns`, `tool_get_campaign_statistics` | `tool_list_journeys` | `tool_list_subscribers` | ✗ |
| Get a Newsletter (`Get_a_Newsletter`) | `tool_list_sent`, `tool_get_report` (one report per sent mail) | — | `tool_list_lists` (`active_subscribers_count` per list) | ✗ |
| Brevo (`Brevo`) | `list_email_campaigns` (`status: "sent"`), `get_email_campaign` (stats are in the campaign's `statistics`) | not exposed | `list_contact_lists` (subscriber counts per list) | ✗. `get_smtp_report` (`start_date`, `end_date`) is **transactional** mail only: report it as its own line |
| MailerLite (`MailerLite`) | `list_campaigns` (`filter_status: "sent"`), `get_campaign` (`stats`) | not exposed | `list_groups` (active counts), `list_subscribers` | ✗ |
| Drip (`Drip`) | `list_campaigns`, `get_campaign` (Email Series: subscriber counts, no per-email open/click rates) | `list_workflows` | `list_subscribers` (`subscribed_after`) for new subs | ✗ (subscriber `lifetime_value` is LTV, not period revenue) |
| Salesforce Marketing Cloud (`Salesforce_Marketing_Cloud`) | `list_email_sends` (`start_date`, `end_date`): per-send rates + window totals | `get_journey_email_performance`, `get_triggered_send_summary` — **lifetime totals, no date filter** | not exposed | conversions count only |
| Symplify (`Symplify`) | `get_campaign_overview` (`start`, `end`), `get_campaign_report` | `list_journeys` (names only) | not exposed | ✓ conversion `amount` per delivery |
| Braze (`Braze`) | `braze_list_campaigns` → `braze_get_campaign_analytics` (`length` ≤ 100, `ending_at`; daily, email channel only) | `braze_list_canvases` → `braze_get_canvas_summary` | `braze_list_email_unsubscribes` (`start_date`, `end_date`) for unsubs; list size not exposed | ✓ Braze-attributed revenue |

**Revenue from the store and analytics (enhanced when connected):**

| Source | Tool | What it is |
|--------|------|------------|
| Shopify | `tool_list_orders` (`query_filter: "created_at:>=YYYY-MM-DD created_at:<YYYY-MM-DD"`, page with `after`) | All store orders in the window (context, not email revenue) |
| WooCommerce | `get_sales_report` (`date_min`, `date_max`) | Store sales totals |
| Abicart / Litium | `get_sales_summary` (`start_date`, `end_date`, `group_by: "week"`) | Orders + revenue per period, base currency |
| GA4 | `tool_run_report` (`dimensions: ["sessionCampaignName"]`, `metrics: ["sessions","keyEvents","purchaseRevenue"]`, `dimension_filter` on `sessionDefaultChannelGroup` = `Email`) | Email-driven sessions and last-click revenue |
| Plausible | `breakdown` (`dimension: "visit:utm_campaign"`, `filters: [["is","visit:utm_medium",["email"]]]`) | Email-driven visits and goal conversions |
| Stripe (SaaS) | `stripe_api_read`: `GetInvoices` (paid, `created` in the window), `GetSubscriptions` (new: `created` in the window; cancelled: there is no `canceled_at` filter, so list `status: "canceled"` and keep rows whose `canceled_at` falls in the window client-side), `GetRefunds`. Use `limit` 20–25 and page with `starting_after` (a 100-row page is ~370KB) | Billed revenue, new subscriptions and churn for SaaS businesses; use it where a store would supply revenue |

Report ESP-attributed revenue, GA4 email revenue and store (or Stripe) revenue as **separate labeled lines**. They use different attribution windows and never add up.

## Steps

### 1. Define the period and read the previous report

| Mode | Current window | Comparison |
|------|----------------|------------|
| weekly | last 7 days | prior 7 days + 4-week rolling avg |
| monthly | last 30 days | prior 30 days + 12-week rolling avg |

State the exact date ranges up front.

Call `read_context_node` with `path: "insights/email/reports/<weekly|monthly>/latest"`. If it exists, it holds the previous report's narrative and key numbers: use them in "What happened" ("this matches the trend from last month" / "this reverses the dip we flagged"). If it doesn't exist, this is the first run for that mode; say so.

### 2. Pull the data

**Per-ESP tool adapter.** The right tool depends on which ESP is connected:

| Data | Klaviyo | Mailchimp | Rule | Get a Newsletter |
|------|---------|-----------|------|------------------|
| Campaign list | `list_campaigns` | `tool_list_campaigns` | `tool_list_campaigns` | `tool_list_sent` |
| Campaign metrics | `get_campaign` + `list_events` (metric-filtered) | `tool_get_report` | `tool_get_campaign_statistics` | `tool_get_report` |
| Automation / flow list | `list_flows` | `tool_list_automations` | `tool_list_journeys` | **not available** |
| Flow metrics | `get_flow` | `tool_get_automation` | `tool_list_journeys` (limited) | **not available** |
| Subscriber list size | `list_profiles` (count) | `tool_get_audience` | `tool_list_subscribers` (count) | `tool_list_lists` → sum of `active_subscribers_count` (not the `tool_list_contacts` count, which includes inactive contacts) |
| Revenue per send | ✓ via `list_events` with `metric="Placed Order"` | **not available** | **not available** | **not available** |

**Get a Newsletter:** `tool_list_sent` rows carry subject, send time and `report_id`, so `tool_get_sent` isn't needed. Its `delivered` equals `sent_to` even when mails bounced, so use `sent_to − bounced` as the delivered denominator. Exclude test sends (under 10 recipients, or "test" in the subject).

For Brevo, MailerLite, Drip, Salesforce Marketing Cloud, Symplify and Braze, use the tools in **Works with** above. Pull each ESP's numbers separately; if several are connected, the report gets one metrics column per ESP, never a blended total.

For the current window AND the comparison window, pull:

**Campaign broadcasts:**
- Each campaign's subject, send date, recipient count, opens, unique opens, clicks, unique clicks, unsubs, bounces.
- **Revenue attributed — Klaviyo, Braze, Symplify.** For Klaviyo, fetch "Placed Order" events scoped to the send window and attribute by campaign (or `get_campaign_values_report` with `revenue_per_recipient`). Braze returns revenue in `braze_get_campaign_analytics`; Symplify returns conversion `amount` per delivery. For the other ESPs, omit ESP-attributed revenue and use GA4/Plausible email-driven revenue or conversions if connected, labeled as such.

**Flows / automations — varies by ESP:**
- Klaviyo: flow name, triggered volume, revenue per flow (via events).
- Mailchimp: automation name, sends, opens, clicks (no revenue).
- Rule: journey name + limited metrics.
- Drip: workflow names from `list_workflows`; Email Series subscriber counts from `get_campaign`.
- Salesforce Marketing Cloud: `get_journey_email_performance` — lifetime numbers, so show them as "since launch", never as this period's change.
- Symplify: `list_journeys` gives names only; journey performance isn't exposed.
- Braze: Canvas name + `braze_get_canvas_summary` for the window (revenue included).
- Brevo, MailerLite: automations aren't exposed; skip and say so.
- Get a Newsletter: **no flow object exists.** Skip this section; use a "recurring sends" proxy if the user has a newsletter cadence.

**List-level metrics:**
- List size at period start vs end
- New subscribers in period
- Unsubscribes in period
- Net change + growth rate

**Zero sends in the period:** if no connected ESP sent a broadcast in the current window, don't compute rates (they'd be 0/0). Output a short report instead: "No email sends in <period> (last send: <date>, <ESP>)", the list-size change, any flow/journey numbers that exist, and the store/Stripe/GA4 context lines. Flag the gap as a finding if the previous report showed a regular cadence.

**Unconnected senders (GA4):** compare the GA4 email `sessionCampaignName` values with the connected ESPs' sends in the window. A campaign with email sessions that matches no ESP send means email is going out from a sender Cogny can't see (another ESP, a CRM, a product mailer). List those campaigns with their sessions and say "sent from an unconnected tool; connect it to include it in the report".

### 3. Compute the report metrics

For each window, compute:

| Metric | Calc | Why it matters |
|--------|------|----------------|
| Sends | total emails delivered | Volume sanity check |
| Open rate | unique opens / delivered | Subject/preheader effectiveness (MPP-distorted) |
| CTR | unique clicks / delivered | True engagement |
| CTOR | unique clicks / unique opens | Content effectiveness (MPP-resilient) |
| Unsub rate | unsubs / delivered | List health signal |
| Bounce rate | bounces / sent | Deliverability signal |
| Revenue per send | ecom revenue / delivered (if available) | The only metric execs actually care about |
| List growth rate | (ending - starting) / starting | Acquisition health |

Show **absolute value + % change vs prior period + % change vs rolling baseline**.

### 4. Identify movers

Rank campaigns in the current window by open rate, CTR, and revenue. Identify:
- **Top performer** — best campaign by revenue (or by CTOR if no revenue data)
- **Worst performer** — bottom by revenue/CTOR
- **Anomaly** — campaign whose metrics are >2σ from the user's typical baseline (surprise hit or surprise flop)

For each, write a one-sentence "why" hypothesis based on visible attributes (subject style, send time, segment, content type).

### 5. Explain variance

Don't just say "CTR dropped 8%." Explain it. Cross-reference:

- Did send volume change? More sends to less-engaged segments drag rate metrics even if absolute revenue is fine.
- Did the segment mix change? (All-list sends vs engaged-only)
- Did cadence change? (More sends per week → fatigue)
- Did a specific campaign drag the average? (One dud to a huge segment)
- Did list hygiene change? (Big unsub event or re-engagement deadline)
- Was there an external event? (holiday, launch, outage)

Phrase findings as **claim → evidence**:

> "Open rate dropped from 28% to 22%. Two of four sends this month went to the dormant 180-day segment (120k recipients at 14% open), which pulled the average down. If you look at engaged-segment sends only, open rate actually rose from 34% to 36%."

### 6. Generate the three outputs

#### 6.1 Slack update (≤500 chars, 3 bullets)

```
📧 Email – <period label>
• Sends: <N> ( <±>% vs prior)  |  Open: <X>% ( <±>pp)  |  CTR: <Y>% ( <±>pp)
• 🏆 Top: "<subject>" — <metric>  |  ⚠️ Watch: <one-line variance call>
• Revenue: $<X> ( <±>% vs prior)  |  List: <±>% net growth  |  Next week: <1-line plan>
```

#### 6.2 CEO email (≤250 words, narrative)

```
Subject: Email performance — <period label>

Hi <CEO first name>,

Quick update on email this <period>:

Headline: <one-sentence summary — is it good, bad, or mixed?>

What happened:
[2-3 sentences explaining volume, rate-metric movement, revenue. Tie to a
business narrative — launches, campaigns, segment focus.]

What's notable:
[1-2 sentences. Top campaign or surprise win or flagged concern.]

What's next:
[1-2 sentences. Concrete plan for next period. Pick ONE action, not five.]

Happy to dig deeper on any of this.

<signoff>
```

#### 6.3 Deck section (full)

```
EMAIL PERFORMANCE — <period label>

Summary
  <two-sentence narrative>

Key metrics
  [table: current / prior / rolling / %Δ]
  Sends, Open rate, CTR, CTOR, Unsub rate, Revenue per send, List size

Trend
  [describe what a chart should show — up-and-to-the-right, step change, etc.]

Campaign roundup
  🏆 Best:  "<subject>"
           <segment>, <recipients>, <metric wins>
  📉 Worst: "<subject>"
           <what happened>

Flow performance (if applicable)
  [table of top 3 flows by revenue, with recipient count and conv rate]

What moved the needle
  [2-3 bullets — claim → evidence]

Plan for next <period>
  [2-3 bullets — concrete, owned, measurable]
```

### 7. Save the narrative

Persist the period summary to Cogny's context tree so future `/email-report` runs have historical continuity:

```json
{
  "path": "insights/email/reports/<weekly|monthly>/latest",
  "body": "<period dates + the narrative summary + key numbers per ESP>"
}
```

Overwrite `latest` (step 1 reads it next run) and also write the same body to `insights/email/reports/<weekly|monthly>/<YYYY-MM-DD>` as the dated archive.

### 8. Create findings for notable issues

For anything serious (unsub rate spike, deliverability drop, revenue collapse, an unconnected sender), record it so it lands in the dashboard — not just the report. On Cloud call `create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `create_finding`:

```json
{
  "title": "Unsub rate doubled vs prior month (0.18% → 0.37%)",
  "body": "<which campaigns drove it, which segment, recommended fix>",
  "action_type": "list_hygiene",
  "priority": "high"
}
```

## Output defaults

- If the user didn't specify a format, output all three and label them clearly.
- Lead with the Slack version — fastest to read if they're skimming.
- Include the raw metric table at the end so the user can copy numbers out.

## Notes

- **Open rate is noisy** since Apple MPP. Always report CTR and CTOR alongside. If open rate moves >5pp but CTOR doesn't, it's probably MPP population change, not real behavior.
- For first-ever run, there's no prior period to compare to — call this out explicitly and use absolute numbers only.
- **Don't invent revenue numbers.** ESP-attributed revenue exists only for Klaviyo ("Placed Order" events with a `value` field), Braze and Symplify. For Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Drip and SFMC, say "revenue not exposed by this ESP's MCP" and use GA4/Plausible email-driven revenue, store or Stripe totals for context, or user-pasted revenue — each labeled with its source.
- **Definitions differ per ESP.** Klaviyo, Mailchimp and Brevo opens include Apple MPP machine opens unless the payload separates them; Get a Newsletter reports per sent mail; SFMC journey totals are lifetime. Name the ESP on every number and never average rates across ESPs.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
