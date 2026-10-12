---
name: revenue-audit
description: Audit an email marketing program for revenue leaks — missing flows, dormant high-value subscribers, under-segmentation, promo gaps, stale automations — ranked by estimated $ impact
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, drip, salesforce-marketing-cloud, symplify, braze, shopify, woocommerce, abicart, litium, stripe, google-analytics-4, plausible]
user-invocable: true
argument-hint: ""
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
  - mcp__cogny__mcp__Brevo__list_contacts
  - mcp__cogny__mcp__Brevo__list_contact_lists
  - mcp__cogny__mcp__MailerLite__list_campaigns
  - mcp__cogny__mcp__MailerLite__get_campaign
  - mcp__cogny__mcp__MailerLite__list_subscribers
  - mcp__cogny__mcp__MailerLite__list_groups
  - mcp__cogny__mcp__MailerLite__list_segments
  - mcp__cogny__mcp__Drip__list_workflows
  - mcp__cogny__mcp__Drip__get_workflow
  - mcp__cogny__mcp__Drip__list_campaigns
  - mcp__cogny__mcp__Drip__get_campaign
  - mcp__cogny__mcp__Drip__list_subscribers
  - mcp__cogny__mcp__Drip__list_event_actions
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_journeys
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_journey
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_journey_email_performance
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_email_sends
  - mcp__cogny__mcp__Symplify__list_journeys
  - mcp__cogny__mcp__Symplify__get_campaign_overview
  - mcp__cogny__mcp__Braze__braze_list_canvases
  - mcp__cogny__mcp__Braze__braze_get_canvas_details
  - mcp__cogny__mcp__Braze__braze_get_canvas_summary
  - mcp__cogny__mcp__Braze__braze_list_campaigns
  - mcp__cogny__mcp__Braze__braze_get_campaign_analytics
  - mcp__cogny__mcp__Braze__braze_list_segments
  - mcp__cogny__mcp__Braze__braze_get_segment_analytics
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__Shopify__tool_list_customers
  - mcp__cogny__mcp__Shopify__tool_list_abandoned_checkouts
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__Abicart__get_sales_summary
  - mcp__cogny__mcp__Litium__get_sales_summary
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Plausible__aggregate
  - mcp__cogny__mcp__Plausible__breakdown
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

# Revenue Audit

The "email growth consultant in a box." Scans your connected ESP for the revenue sitting on the table and ranks every finding by estimated dollar impact, so you know exactly what to fix first.

**Requires:** Cogny MCP + a connected ESP. [Sign up](https://cogny.com)

This is the skill to run once per quarter, or whenever you inherit an email program and need to know where to start.

## Usage

`/revenue-audit` — full audit of the connected ESP

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this:

```
Revenue Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Drip, Salesforce Marketing Cloud, Symplify or Braze), plus your store (Shopify, WooCommerce, Abicart, Litium) or Stripe for revenue.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: paste your last 90 days of email revenue (total and per campaign/flow) plus your campaign stats export, and get a provisional audit from that.
```

With pasted revenue, run only the checks the pasted data supports (typically 1, 3, 4, 5 and 9), label every $ figure "pasted by user", mark the rest "skipped — needs a connected ESP", skip steps 5–6 (no findings, no context tree) and stop after the output. When Cogny is connected but no ESP is, say "connect your ESP in Cogny".

## Prerequisites Check

Detect connected ESP (check both `mcp__cogny__<svc>__*` and `mcp__<svc>__*` namespaces). If the user has multiple connected, run against each and produce separate reports.

## Works with

On Cloud, `mcp__cogny__list_integrations` shows what's connected; name any unhealthy integration as broken.

**Health check:** `health_status` misses revoked tokens, so make one cheap read per integration before relying on it (e.g. Mailchimp `tool_get_account_info`, Get a Newsletter `tool_list_senders`, Klaviyo `get_account`, Shopify `tool_list_orders` with a 1-day filter, Stripe `stripe_api_read` `GetSubscriptions` with `limit: 1`, GA4 `tool_run_report` for one day). A 401, Forbidden or scope error means 🔴 "reconnect <integration> in Cogny": name it, don't retry, and audit with what remains.

**Missing tool:** if a tool named here isn't exposed by the workspace, call `mcp__cogny__refresh_mcp_discovery` once, use the fallback named next to the tool for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh. Get a Newsletter fallbacks: `tool_get_report_have_not_opened` → that report's list contacts minus the openers from `tool_get_report_opens`; `tool_get_report_link_clicks` → `tool_get_report_opens` (per-contact click counts) or `tool_get_report_clicks` (per-link totals); `tool_get_report_opens_aggregated` → the totals in `tool_get_report`. Mailchimp `tool_get_campaign_content` → `tool_get_campaign` for the headers, and ask the user for the body.

**ESP connected but 0 sends in the window:** skip the send-based checks (3, 4, 5, 9) for that ESP with a one-line note ("Get a Newsletter: connected, 0 sends in the last 90 days — send checks skipped") and still run the list checks (6, 8 and the never-mailed lists in Check 4).

**Revenue data availability (cogny-mcp-proxy as of this writing):**

| ESP | Has flows/automations? | Has purchase/revenue data? |
|-----|------------------------|----------------------------|
| Klaviyo | ✓ (`list_flows`) | ✓ (via `list_events` with metric="Placed Order", `value` field) |
| Mailchimp | ✓ (`tool_list_automations`) | ✗ — engagement only |
| Rule | ✓ (`tool_list_journeys`) | ✗ — engagement only |
| Get a Newsletter | ✗ — no flow concept exists | ✗ — engagement only |
| Brevo | ✗ — automations not exposed | ✗ — engagement only |
| MailerLite | ✗ — automations not exposed | ✗ — engagement only |
| Drip | ✓ (`list_workflows`, `get_workflow`) | Partial — subscriber `lifetime_value`; event names via `list_event_actions` |
| Salesforce Marketing Cloud | ✓ (`list_journeys`, `get_journey`, `get_journey_email_performance`) | Conversions count only |
| Symplify | ✓ names only (`list_journeys`) | ✓ conversion `amount` per delivery (`get_campaign_overview`) |
| Braze | ✓ (`braze_list_canvases`, `braze_get_canvas_details`, `braze_get_canvas_summary`) | ✓ Braze-attributed revenue in campaign/Canvas analytics |

**Real revenue beats ESP-attributed revenue.** If a store is connected, use it as the denominator for every ESP:

| Store (Prefix) | Revenue (90d) | AOV, repeat rate | Abandoned carts |
|----------------|---------------|------------------|-----------------|
| Shopify (`Shopify`) | `tool_list_orders` (`query_filter: "created_at:>=YYYY-MM-DD financial_status:paid"`) | `tool_list_customers` (`numberOfOrders`, `amount_spent`) | `tool_list_abandoned_checkouts` |
| WooCommerce (`WooCommerce`) | `get_sales_report` (`date_min`, `date_max`) | `list_orders` (`after`, `status: "completed"`) | not exposed |
| Abicart (`Abicart`) | `get_sales_summary` (`start_date`, `end_date`, `group_by: "month"`) | `avg_order_value_inc_vat` in the summary | not exposed |
| Litium (`Litium`) | `get_sales_summary` (`start_date`, `end_date`, `group_by: "month"`) | same | not exposed |
| Stripe (`Stripe`, SaaS) | `stripe_api_read` `GetInvoices` (`status: "paid"`, `created` in the 90 days) minus `GetRefunds` | `GetSubscriptions` (`status: "all"`): active count, MRR, cancellations in the window | not applicable |

Stripe list calls: use `limit` 20–25 and page with `starting_after` (a 100-row page is ~370KB). `GetSubscriptions` has no `canceled_at` filter, so for cancellations in the window list `status: "canceled"` and filter `canceled_at` client-side.

For SaaS businesses Stripe is the revenue source: use it wherever this skill says store revenue, and read "AOV" as average invoice / ARPA and "repeat rate" as renewal rate.

Email's share of that revenue comes from, in order: the ESP's own attribution (Klaviyo, Braze, Symplify), GA4 `tool_run_report` (`purchaseRevenue` with `sessionDefaultChannelGroup` = `Email`), or the user. Name the source on every $ figure and use the store's currency. Without any of these, revenue estimates must be either (a) supplied by the user (paste historical email revenue), or (b) flagged as "engagement uplift only" with no dollar figures.

## Steps

### 1. Establish baseline context

Pull once and reference throughout:
- Total active subscribers
- Average open rate + CTR (last 90 days)
- **Klaviyo only:** Total email revenue (last 90 days) via `list_events` with `metric="Placed Order"`, summed `value` field, filtered to events attributed to email campaigns. This is the denominator for every % impact claim.
- **Klaviyo only:** Average AOV (total revenue / order count in period)
- **Store or Stripe connected (any ESP):** total store revenue, order count and AOV for the same 90 days (Shopify / WooCommerce / Abicart / Litium, or Stripe for SaaS, see Works with), plus GA4 email-channel revenue if connected. Show ESP-attributed, GA4 and store figures as separate lines.
- List growth rate (last 90 days)
- Active flows / automations / journeys and their performance (Klaviyo / Mailchimp / Rule only — Get a Newsletter has no equivalent)
- Last 90 days of campaign sends

**If the ESP has no revenue data and no store or GA4 is connected:** prompt the user for their approximate 90-day email revenue (or let them skip it). If they skip, use **estimated value per subscriber per month** = (industry benchmark $0.10–$2.00 depending on vertical) as a rough denominator, and clearly label every revenue estimate as "based on industry benchmark, not your actual data."

### 2. Run the nine checks

For each check, output: **finding title + estimated $ lift + evidence + recommended fix**.

#### Check 1 — Missing core flows / automations / journeys

Map "flow" to the right concept per ESP:

| ESP | Object | Tool |
|-----|--------|------|
| Klaviyo | Flow | `list_flows` + `get_flow` |
| Mailchimp | Automation / Customer Journey | `tool_list_automations` + `tool_get_automation` |
| Rule | Journey | `tool_list_journeys` |
| Get a Newsletter | **No equivalent** — skip this check and note the limitation |
| Drip | Workflow | `list_workflows` + `get_workflow` |
| Salesforce Marketing Cloud | Journey | `list_journeys` + `get_journey` (entry source, goals) + `get_journey_email_performance` |
| Symplify | Journey | `list_journeys` (names only; judge coverage by name and say so) |
| Braze | Canvas | `braze_list_canvases` + `braze_get_canvas_details` + `braze_get_canvas_summary` |
| Brevo, MailerLite | **Not exposed** by the MCP — ask the user which automations run, or skip and note it |

**Abandoned cart sizing with real data:** if Shopify is connected, count `tool_list_abandoned_checkouts` for the last 30 days and their total value (`total_price`). Use that instead of "cart sessions × conv rate" in the evidence line.

The highest-ROI flows and their typical revenue contribution in healthy ecom programs (Klaviyo benchmarks):

| Flow | Typical % of email revenue | Trigger |
|------|---------------------------|---------|
| Welcome series | 3–7% | New subscriber |
| Abandoned cart | 5–12% | Cart created, not checked out |
| Browse abandonment | 1–3% | Product viewed, no cart |
| Post-purchase | 2–5% | Order placed |
| Winback | 1–4% | No engagement in 60-120d |
| Replenishment | 2–6% (consumables only) | Predicted reorder date |
| Birthday / anniversary | 0.5–2% | Date token match |
| VIP / thank-you | 1–3% | Top-tier LTV crossed |

For each missing or disabled flow, estimate lift: `total_email_revenue × benchmark_%` as the annualized $ left on the table (Klaviyo). For Mailchimp/Rule/Get a Newsletter without revenue data, frame the impact as engagement uplift (e.g., "typically adds X–Y% to total email engagement volume") and skip the dollar estimate unless the user provided a revenue baseline.

#### Check 2 — Dormant high-value subscribers (Klaviyo only)

Segment current active list by:
- **Ever purchased** × **engaged in last 60 days**

Pull purchase history via `list_events` with `metric="Placed Order"`. Group by `profile_id`, take max `value` sum per profile as LTV. Cross-reference against `list_profiles` last-engaged date.

Count subscribers who have purchased at least once but haven't opened/clicked in 60+ days. Estimate:
`count × avg_AOV × 3% reactivation rate × 2 orders/year = annualized recoverable revenue`

**Purchase data from the store:** for any ESP, join Shopify `tool_list_customers` (`numberOfOrders` > 0, `amount_spent`), WooCommerce `list_orders`, or (SaaS) Stripe `GetSubscriptions` customers with a cancelled or past-due subscription to the ESP's subscribers on lowercased email. If Stripe's `email`/`customer_email` comes back `[REDACTED]` (a restricted key), skip the Stripe join and say so ("Stripe emails redacted by the restricted key: no subscriber match"); Stripe totals still work as context. Drip's subscriber `lifetime_value` works directly.

**For Mailchimp / Rule / Get a Newsletter / Brevo / MailerLite with no store connected:** purchase data is not exposed. Degrade this check to "dormant deeply-engaged subscribers" — pull subscribers with high historical open+click counts who haven't engaged in 60+ days, present as engagement-uplift opportunity without a dollar figure.

#### Check 3 — Under-segmented broadcasts
Scan last 90 days of campaign sends. For each campaign, check if it was sent to:
- **"All subscribers" / full list** (bad default)
- **A meaningful segment** (engaged, purchased, category-preference, geography)

Flag any campaign sent to >80% of list where segmentation would plausibly apply. Estimate lift: `(segment_ctr - broadcast_ctr) / broadcast_ctr × revenue_of_that_campaign × number_of_similar_sends_per_year`.

#### Check 4 — Promo calendar gaps
Build a 90-day send calendar from actual sends. Look for:
- **Weeks with zero broadcasts** (dead zones)
- **Dead zones around proven peak buying windows** (BFCM, Mother's Day, back-to-school — vertical-specific)
- **Over-send weeks** (>4 broadcasts to the same segment in 7 days — fatigue risk)
- **Never-mailed lists:** compare every list/audience/group (Mailchimp `tool_list_audiences`, Get a Newsletter `tool_list_lists` + `tool_get_list`, Rule `tool_list_tags`, Brevo `list_contact_lists`, MailerLite `list_groups`) with the lists the sends targeted (Mailchimp `tool_get_campaign` `recipients.list_id`; Get a Newsletter `tool_get_sent`). A list with contacts that has never received a send is a finding on its own (e.g. "191-contact list never mailed"): those people opted in and heard nothing. Route them to `/welcome-series`; estimate value only from the store or Stripe base, otherwise "engagement uplift only".

For dead zones during peak windows, estimate: `avg revenue per send × N missing sends`.

#### Check 5 — Flow decay
For every active flow, check:
- **Last modified date** — flag if >6 months
- **Open/CTR trend** — flag if the flow's rolling 30-day rate is >20% below the flow's historical rate

Recommend: refresh subject lines, update product references, re-evaluate offer.

#### Check 6 — Suppression leaks
Count subscribers who have:
- No open in 180+ days
- No click in 180+ days
- No purchase in 365+ days (if ecom)

Sending to these hurts deliverability. Quantify the deliverability drag: "Removing these X subscribers typically lifts overall open rate by 1-3pp on remaining list, which compounds to ~Y% revenue lift across all future sends."

#### Check 7 — Post-purchase upsell / cross-sell gap (Klaviyo only)

Purchase-data-dependent — runs for Klaviyo (`list_events` with `metric="Placed Order"`), or any ESP when Shopify / WooCommerce orders are connected (repurchase cadence from `tool_list_orders` / `list_orders` grouped by customer email).

For brands with purchase data:
- Does a post-purchase flow exist? (Check 1)
- Does it include category-appropriate upsell or accessory recommendations?
- What's the 30-day repurchase rate? If <15%, post-purchase is underbuilt.

Estimate: `customers_per_month × current_repurchase_rate_gap × avg_AOV`.

**Without Klaviyo or a connected store:** skip this check with a one-line note ("skipped — no purchase data exposed by this ESP's MCP; connect Shopify/WooCommerce or paste purchase data manually").

#### Check 8 — List capture inference
Compare list growth rate to benchmarks:
- Ecom site with steady traffic: 2–5% monthly list growth is healthy
- <1% monthly growth = under-capturing

If growth is weak, flag: "Your site traffic vs. your list growth implies a capture rate of X%. Industry benchmark is 2-5%." Recommend: exit-intent popup, post-purchase capture, content offer gate.

Traffic (enhanced when connected): GA4 `tool_run_report` (`metrics: ["totalUsers"]`, 90 days, **no dimensions**: summing channel or source rows double-counts users who arrived through several channels) or Plausible `aggregate` (`metrics: ["visitors"]`). New subscribers: Drip `list_subscribers` (`subscribed_after`), MailerLite `list_subscribers` (`subscribed_at`), or the ESP's list counts. Name both sources in the evidence line.

#### Check 9 — Over-reliance on discounting
Scan subject lines and body content of broadcasts for % off / $ off / "sale" / "discount" / promo codes. (Mailchimp body: `tool_get_campaign_content`; if it's missing, fall back to `tool_get_campaign` `settings.subject_line` + `preview_text` and scan those only, marked ⚠.) If >60% of broadcasts lead with a discount:
- Flag as margin leak + audience training (they wait for sales)
- Recommend: content-led sends, product drops, exclusivity, early access

Estimate: margin recovery = `current_margin × (promo_share_reduction × conversion_retention)`.

### 3. Rank every finding by estimated $ impact

Bucket into 🔴 High (>5% of annual email revenue or >$10k/yr), 🟡 Medium ($1k–$10k/yr), 🟢 Optimization (<$1k/yr or hard to quantify).

### 4. Output

```
Revenue Audit: <brand> via <ESP>
Period analyzed: <date range>
Total email revenue (90d): $<X>     Implied annualized: $<Y>

Estimated annual revenue left on the table: $<Z>   (<Z/Y>% of current)

────────────────────────────────────────────────────
🔴 HIGH IMPACT — start here
────────────────────────────────────────────────────

1. Missing abandoned cart flow
   Est. lift: $<X>/yr   (7% of email revenue benchmark)
   Evidence: No flow with trigger "cart created, not converted" in <ESP>.
             Current cart sessions on connected store = <N>/month at
             <conv rate>%. Industry abandoned-cart flow recovery ≈ 10–15%.
   Fix: Build 3-email cart flow (1h / 24h / 48h). I can draft this now — run
        /welcome-series and tell it "abandoned cart" or ask me to generate.

2. <N> dormant high-value subscribers (LTV > $<X>)
   Est. lift: $<X>/yr
   Evidence: <N> past purchasers with avg LTV $<Y>, no engagement in 60+ days.
             At 3% reactivation × 2 orders/year × $<AOV> AOV.
   Fix: Run /winback-engine for a tiered winback series.

3. ...

────────────────────────────────────────────────────
🟡 MEDIUM IMPACT
────────────────────────────────────────────────────

4. ...

────────────────────────────────────────────────────
🟢 OPTIMIZATION
────────────────────────────────────────────────────

7. ...

────────────────────────────────────────────────────
Suggested 90-day plan
────────────────────────────────────────────────────
Month 1: <high-impact items 1-2>. Est revenue unlock: $<X>.
Month 2: <high-impact item 3 + medium 1>. Est: $<Y>.
Month 3: <remaining>. Est: $<Z>.

Total 90-day estimated unlock: $<X+Y+Z>.
```

### 5. Record every item

Every finding in the output is also recorded in Cogny, so the dashboard has the same ranked list the user just saw. On Cloud call `create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `create_finding`:

```json
{
  "title": "Missing abandoned cart flow (est. +$<X>/yr)",
  "body": "<evidence + fix>",
  "action_type": "flow_build",
  "expected_outcome": "Recover 10-15% of abandoned carts",
  "estimated_impact_usd": <annualized impact>,
  "priority": "high"
}
```

### 6. Save the audit summary

Persist to context tree under `insights/email/revenue-audit/<date>` so the next audit can show progress:
- "Last audit: 2026-01-15 — identified $120k/yr unlock; 2 items now implemented."

### 7. Offer next steps

```
Next steps I can help with right now:

  /welcome-series          — draft any missing flow
  /winback-engine          — execute #2 (dormant high-value)
  /subject-line-lab        — lift open rates on existing broadcasts
  /email-report weekly     — start tracking progress against this audit

Or: ask me to draft a specific flow by name.
```

## Notes

- **Benchmarks are rough.** Real uplift depends on list quality, brand, vertical, and offer. Always frame estimates as "reasonable industry range" not "guaranteed."
- Don't double-count. If "missing abandoned cart" and "post-purchase gap" both hit, check that the benchmark assumptions aren't overlapping.
- **ESP-specific check coverage (cogny-mcp-proxy):**
  - Klaviyo: all 9 checks run with dollar estimates.
  - Mailchimp: Checks 1, 3, 4, 5, 6, 8, 9 run normally. Checks 2 and 7 degrade to "engagement-only" framing.
  - Rule: same as Mailchimp.
  - Get a Newsletter: Check 1 is skipped (no flow concept). Checks 2 and 7 are skipped (no purchase data). The remaining checks (3, 4, 5, 6, 8, 9) run on engagement data only.
  - Brevo, MailerLite: like Get a Newsletter (automations not exposed, so Checks 1 and 5 need the user's input); campaign stats come from `get_email_campaign` / `get_campaign`.
  - Drip: Checks 1, 2 (via `lifetime_value`), 6, 8 run; Checks 3, 4, 9 have no broadcast history in the MCP; Check 5 has no per-email rates.
  - Salesforce Marketing Cloud: Checks 1, 3, 4, 5, 9 run (`list_email_sends`, journeys). Journey numbers are lifetime, so Check 5 compares emails within a journey, not over time.
  - Symplify: Checks 3, 4, 9 run from `get_campaign_overview`; Check 1 by journey name only.
  - Braze: Checks 1, 4, 5 run (Canvases + campaign analytics, max 100 days per call); Checks 2 and 6 use segment sizes only.
  - **Any ESP + Shopify/WooCommerce (or Stripe for SaaS):** Checks 2 and 7 run with real purchase data, and every $ estimate uses store (or Stripe) revenue as the base.
- **Several ESPs connected:** separate reports, as above. Store revenue is shared, so attribute it once — don't claim the same store revenue as each ESP's base.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
