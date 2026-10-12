---
name: subject-line-lab
description: Mine your actual subject-line history from your connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Salesforce Marketing Cloud, Symplify, Braze), find the patterns that work for YOUR list, and generate tuned candidates
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, salesforce-marketing-cloud, symplify, braze]
user-invocable: true
argument-hint: "[campaign topic]"
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
  # Newer ESPs: read tools only
  - mcp__cogny__mcp__Brevo__list_email_campaigns
  - mcp__cogny__mcp__Brevo__get_email_campaign
  - mcp__cogny__mcp__MailerLite__list_campaigns
  - mcp__cogny__mcp__MailerLite__get_campaign
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_email_sends
  - mcp__cogny__mcp__Symplify__get_campaign_overview
  - mcp__cogny__mcp__Symplify__get_campaign_report
  - mcp__cogny__mcp__Braze__braze_list_campaigns
  - mcp__cogny__mcp__Braze__braze_get_campaign_details
  - mcp__cogny__mcp__Braze__braze_get_campaign_analytics
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

# Subject Line Lab

Stop A/B testing blind. This skill reads **your actual last 100+ sends**, finds the subject-line patterns that correlate with open rate on *your* list, and generates 20 tuned candidates for your next campaign.

**Requires:** Cogny MCP + a connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Salesforce Marketing Cloud, Symplify or Braze). [Sign up](https://cogny.com)

## Usage

`/subject-line-lab` — mine patterns and generate generic candidates
`/subject-line-lab "Black Friday doors open"` — mine patterns and generate candidates for a specific campaign topic

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`) and no Solo per-ESP tools (`mcp__klaviyo__*`, `mcp__mailchimp__*`, `mcp__rule__*`, `mcp__get_a_newsletter__*`) either, print this and stop:

```
Subject Line Lab needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Salesforce Marketing Cloud, Symplify or Braze).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Prerequisites Check

Detect which ESP is connected. Check **both** namespaces (Cloud-aggregated via `mcp__cogny__<svc>__*` and Solo/Lite per-ESP via `mcp__<svc>__*`):

- Klaviyo → `mcp__cogny__mcp__Klaviyo__*` or `mcp__klaviyo__*`
- Mailchimp → `mcp__cogny__mcp__Mailchimp__*` or `mcp__mailchimp__*`
- Rule → `mcp__cogny__mcp__Rule__*` or `mcp__rule__*`
- Get a Newsletter → `mcp__cogny__mcp__Get_a_Newsletter__*` or `mcp__get_a_newsletter__*`
- Brevo, MailerLite, Salesforce Marketing Cloud, Symplify, Braze → Cloud namespace only (`mcp__cogny__mcp__<Prefix>__*`)

On Cloud, `mcp__cogny__list_integrations` lists what is connected; treat any integration whose `health_status` isn't healthy as broken and name it.

**Health check:** `health_status` misses revoked tokens, so make one cheap read per ESP before relying on it (Klaviyo `get_account`, Mailchimp `tool_get_account_info`, Rule `tool_list_tags`, Get a Newsletter `tool_list_senders`, Brevo/MailerLite `list_*campaigns` with a limit of 1, SFMC `list_email_sends` for one day, Symplify `get_campaign_overview` for one day, Braze `braze_list_campaigns`). A 401, Forbidden or scope error means 🔴 "reconnect <integration> in Cogny": name it in the output, don't retry, and continue with the other ESPs.

**Missing tool:** if a tool named here isn't exposed by the workspace (older connections cache their tool list), call `mcp__cogny__refresh_mcp_discovery` once, then use the fallback named next to the tool for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh. Get a Newsletter fallbacks: `tool_get_report_have_not_opened` → that report's list contacts minus the openers from `tool_get_report_opens`; `tool_get_report_link_clicks` → `tool_get_report_opens` (per-contact click counts) or `tool_get_report_clicks` (per-link totals); `tool_get_report_opens_aggregated` → the totals in `tool_get_report`. Mailchimp `tool_get_campaign_content` → `tool_get_campaign` for the headers, and ask the user for the body.

**ESP connected but 0 sends in the window:** skip it with a one-line note ("Mailchimp: connected, 0 broadcast sends in the last <N> days — skipped") and run the rest.

If Cogny is connected but no ESP is, say: "Connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Salesforce Marketing Cloud, Symplify or Braze) in Cogny", and stop.

If multiple are connected, prompt the user which one to analyze (or analyze all, labeled). **Never pool sends from two ESPs into one baseline** — open-rate definitions differ (see below). Run steps 2–5 per ESP and show the results side by side.

## Works with

| ESP (Prefix) | Send history | Per-send metrics | Subject + preheader | Definition notes |
|--------------|--------------|------------------|---------------------|------------------|
| Klaviyo (`Klaviyo`) | `list_campaigns` | `get_campaign_values_report` (`statistics: ["open_rate","click_rate","recipients"]`, `campaign_id`) | `get_campaign_message` | Open rate includes Apple MPP machine opens |
| Mailchimp (`Mailchimp`) | `tool_list_reports` | `tool_get_report` | in the report / `tool_get_campaign` | Opens include MPP |
| Rule (`Rule`) | `tool_list_campaigns` | `tool_get_campaign_statistics` | `tool_get_campaign` | |
| Get a Newsletter (`Get_a_Newsletter`) | `tool_list_sent` | `tool_get_report` (`report_id` from the `tool_list_sent` row) | `tool_list_sent` (subject is on each row; no preheader) | One report per sent mail, no campaign object. `delivered` equals `sent_to` even when mails bounced, so open rate = unique opens / (`sent_to` − `bounced`) |
| Brevo (`Brevo`) | `list_email_campaigns` (`status: "sent"`) | `get_email_campaign` (the `statistics` block) | `get_email_campaign` (`subject`, `previewText`) | Stats live on the campaign, not a report tool. Use MPP-excluded opens if the payload separates them (`appleMppOpens`) |
| MailerLite (`MailerLite`) | `list_campaigns` (`filter_status: "sent"`) | `get_campaign` (`stats`) | `get_campaign` (`emails[].subject`) | Use the rates in `stats` as returned; don't recompute from other ESPs' formulas |
| Salesforce Marketing Cloud (`Salesforce_Marketing_Cloud`) | `list_email_sends` (`start_date`, `end_date`, `max_results`) | same call: unique opens/clicks and rates per send | same call (`subject`) | Covers user-initiated and scheduled sends only. Journey emails are triggered sends; skip them like flows |
| Symplify (`Symplify`) | `get_campaign_overview` (`channel: "EMAIL"`, `start`, `end`) | same call, or `get_campaign_report` (`delivery_id`) | delivery name in the overview | If no subject field comes back, analyse the delivery name only for structure and say so |
| Braze (`Braze`) | `braze_list_campaigns` | `braze_get_campaign_analytics` (`campaign_id`, `length` ≤ 100 days, `ending_at`) — daily rows, sum within the campaign | `braze_get_campaign_details` (email message `subject`) | Max 100 days per call; page back with `ending_at`. Multichannel campaigns: use only the email channel's numbers |
| Drip (`Drip`) | — | — | — | **Not supported.** Drip's MCP exposes Email Series campaigns and workflows, not one-off broadcasts or per-email open rates |

## ESP tool adapter

Each ESP exposes subject-line history differently. Use the right tool per connected service:

| ESP | Send history tool | Notes |
|-----|-------------------|-------|
| Klaviyo | `list_campaigns` (channel=email) then `get_campaign` + `get_campaign_message` | Tools are bare-named. `get_campaign_values_report` gives open/click rate per campaign in one call; `list_events` for deeper metrics. |
| Mailchimp | `tool_list_reports` then `tool_get_report` | Reports are the source of truth for opens/clicks per send. |
| Rule | `tool_list_campaigns` then `tool_get_campaign_statistics` | Statistics tool returns opens/clicks/bounces. |
| Get a Newsletter | `tool_list_sent` then `tool_get_report` | "Campaigns" don't exist as an object. `tool_list_sent` rows already carry subject, send time and `report_id`, so `tool_get_sent` isn't needed; call `tool_get_report` per send for metrics and use `sent_to − bounced` as the denominator (its `delivered` doesn't subtract bounces). |
| Brevo | `list_email_campaigns` (`status: "sent"`) then `get_email_campaign` | Subject, preview text and statistics come from the same call. |
| MailerLite | `list_campaigns` (`filter_status: "sent"`) then `get_campaign` | `stats` holds opens/clicks; `get_campaign_activity` is per-subscriber and not needed here. |
| Salesforce Marketing Cloud | `list_email_sends` | One call returns subject + metrics per send for the window. |
| Symplify | `get_campaign_overview` then `get_campaign_report` for detail | Pre-aggregated KPIs per delivery. |
| Braze | `braze_list_campaigns` → `braze_get_campaign_details` → `braze_get_campaign_analytics` | Only campaigns with an email message; the analytics are daily, so sum them per campaign. |

## Steps

### 1. Pull send history
For the connected ESP, pull the last **100 campaign sends** (or as many as available). For each, capture:
- Subject line
- Preheader (if available)
- Send date + time (recipient local time if available)
- Recipient count
- Unique opens → open rate
- Unique clicks → CTR
- Segment / list name
- Campaign type (promo, newsletter, announcement, transactional-adjacent)

Skip transactional sends and automated flow emails — they distort the signal. Focus on broadcast campaigns. **Exclude test sends** too: recipient count under 10, a subject/name containing "test", "[TEST]", "testutskick" or "proof", or a send to a list/audience whose name contains "test", "intern", "internal" or "seed" (case-insensitive; internal seed lists can be dozens of people, so recipient count alone misses them). Report how many were excluded. (Brevo: `type: "classic"` only, never `trigger`; SFMC: never triggered sends; Braze: skip API-triggered and Canvas sends.)

### 2. Compute baseline
- **Median open rate** across the sample
- **Mean open rate** (flag skew if mean ≠ median by >20%)
- **Sample size warning** — if <30 sends, warn the user: "small sample, patterns may be noise"

### 3. Extract subject-line features
For each subject line, tag these features (use keyword/regex heuristics — no ML needed):

**Structural:**
- Length (chars): <30 / 30-50 / 50-70 / >70
- Word count
- Title Case / Sentence case / ALL CAPS / lowercase
- Ends in `?` / `!` / `.` / no punctuation

**Content:**
- Contains emoji (count, type)
- Contains number / digit
- Contains `%` or `$` or currency (promo signal)
- Contains personalization token (`{{ first_name }}`, `[Firstname]`)
- Question vs statement vs command
- First-person ("I", "we", "my") vs second-person ("you", "your")
- Urgency words: "today", "tonight", "last chance", "ends", "hours", "don't miss"
- FOMO / scarcity: "only", "limited", "few left", "selling fast"
- Curiosity gap: starts with "why", "how", "the truth about", "what I learned"
- Benefit-led: leads with a noun describing an outcome
- Social proof: "customers", "members", a number of people

**Temporal:**
- Day of week sent
- Hour of day (bucketed: early morning / morning / midday / afternoon / evening / late)

### 4. Compute lift per feature
For each feature, compute:
- **Count in sample**
- **Mean open rate when feature is present**
- **Mean open rate when feature is absent**
- **Lift** (% difference vs non-feature baseline)
- **Significance note** — flag as "strong" if n≥10 in both groups and lift is ≥10% relative; "weak" otherwise

Rank features by absolute lift.

### 5. Identify winning patterns

Output the top 5 **positive** patterns and top 3 **negative** patterns with specific numbers:

```
Patterns that worked for your list (last 100 sends):

🟢 WINNERS
1. Subject lines ending in "?" → 34% open rate vs 21% baseline (+62%, n=14 strong)
2. Subject lines with numbers → 29% open rate vs 21% (+38%, n=22 strong)
3. Length 30-50 chars → 27% open rate vs 19% (+42%, n=31 strong)
4. First-person voice ("I", "we") → 26% open rate vs 22% (+18%, n=18 strong)
5. Sent Tue 09:00-11:00 → 28% open rate vs 22% (+27%, n=12 weak)

🔴 DRAGS
1. ALL CAPS words → 14% open rate vs 23% (-39%, n=8 weak)
2. Emoji at start → 18% open rate vs 24% (-25%, n=11 strong)
3. Urgency words ("last chance", "today only") → 16% open rate vs 22% (-27%, n=9 weak)

Your best historical subject: "<actual subject>" at <open rate>% (<date>)
Your worst: "<actual subject>" at <open rate>% (<date>)
```

### 6. Generate tuned candidates

If a campaign topic was provided, generate **20 subject line candidates** that follow the winning patterns and avoid the drags. If no topic was provided, generate 20 generic promo/newsletter candidates using your patterns.

Format:

```
Candidates for: "<topic>"
(tuned to: ends-in-?, has-number, 30-50 chars, first-person voice)

Preheader recommendation: 85-100 chars, don't duplicate subject, extend the hook.

1. "What <specific number> of our customers asked last week?" (52 chars)
   Preheader: "We pulled the top 5 questions and answered them in one place — you'll recognize #2."
2. ...
20. ...

──
A/B test plan:
- Primary variant: candidate #<N> (leans hardest into top pattern)
- Challenger: candidate #<M> (different angle to avoid pattern overfitting)
- Hold-out: your house-style baseline subject
Segment: X% / Y% / Z%
```

### 7. Persist patterns as context

Save the winning-pattern summary to Cogny's context tree for future sessions:

```json
{
  "path": "insights/email/subject-line-patterns",
  "body": "<the top 5 winners + top 3 drags, with numbers and date range>"
}
```

### 8. Record the finding

If the analysis surfaces a clear actionable insight (e.g., "50% of recent sends use emoji-at-start which is actively hurting opens"), record it: on Cloud call `create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `create_finding`:

```json
{
  "title": "Emoji-at-start subjects are tanking opens (-25% vs baseline)",
  "body": "11 of last 100 sends started with emoji. Avg open 18% vs 24% non-emoji baseline. Recommend: move emoji to mid-subject or drop entirely on next 10 campaigns and re-measure.",
  "action_type": "subject_line_optimization",
  "expected_outcome": "Lift average open rate by 2-4 pp",
  "estimated_impact_usd": 0,
  "priority": "medium"
}
```

## Notes

- Lift numbers are **correlational**, not causal — always surface sample size and flag weak signals.
- If the user's list is <5,000 subscribers, opens are noisy. Recommend 2-week lookback minimum and warn.
- Apple MPP inflates open rate for iOS Mail users. If open rate looks uniformly high (>40%+ across everything), the signal is degraded — note this and lean on CTR as a secondary metric.
- **Name the ESP on every number** ("Brevo: 31% open rate"). Klaviyo, Mailchimp and Brevo count opens differently around MPP; SFMC and Symplify report their own computed rates. Compare patterns across ESPs, never raw rates.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
