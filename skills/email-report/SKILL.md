---
name: email-report
description: Auto-generate the weekly or monthly email performance report in three formats — Slack update, CEO email, board-deck section — from real ESP data
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter]
user-invocable: true
argument-hint: "[weekly|monthly] [slack|ceo|deck|all]"
allowed-tools:
  # Cogny Cloud (aggregated) namespace
  - mcp__cogny__klaviyo__*
  - mcp__cogny__mailchimp__*
  - mcp__cogny__rule__*
  - mcp__cogny__get_a_newsletter__*
  - mcp__cogny__create_finding
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

## Prerequisites Check

Detect connected ESP. If none, stop and prompt.

## Steps

### 1. Define the period

| Mode | Current window | Comparison |
|------|----------------|------------|
| weekly | last 7 days | prior 7 days + 4-week rolling avg |
| monthly | last 30 days | prior 30 days + 12-week rolling avg |

State the exact date ranges up front.

### 2. Pull the data

**Per-ESP tool adapter.** The right tool depends on which ESP is connected:

| Data | Klaviyo | Mailchimp | Rule | Get a Newsletter |
|------|---------|-----------|------|------------------|
| Campaign list | `list_campaigns` | `tool_list_campaigns` | `tool_list_campaigns` | `tool_list_sent` |
| Campaign metrics | `get_campaign` + `list_events` (metric-filtered) | `tool_get_report` | `tool_get_campaign_statistics` | `tool_get_report` |
| Automation / flow list | `list_flows` | `tool_list_automations` | `tool_list_journeys` | **not available** |
| Flow metrics | `get_flow` | `tool_get_automation` | `tool_list_journeys` (limited) | **not available** |
| Subscriber list size | `list_profiles` (count) | `tool_get_audience` | `tool_list_subscribers` (count) | `tool_list_contacts` (count) |
| Revenue per send | ✓ via `list_events` with `metric="Placed Order"` | **not available** | **not available** | **not available** |

For the current window AND the comparison window, pull:

**Campaign broadcasts:**
- Each campaign's subject, send date, recipient count, opens, unique opens, clicks, unique clicks, unsubs, bounces.
- **Revenue attributed — Klaviyo only.** For Klaviyo, fetch "Placed Order" events scoped to the send window and attribute by campaign. For Mailchimp/Rule/Get a Newsletter, omit the revenue line entirely from the report and call it out.

**Flows / automations — varies by ESP:**
- Klaviyo: flow name, triggered volume, revenue per flow (via events).
- Mailchimp: automation name, sends, opens, clicks (no revenue).
- Rule: journey name + limited metrics.
- Get a Newsletter: **no flow object exists.** Skip this section; use a "recurring sends" proxy if the user has a newsletter cadence.

**List-level metrics:**
- List size at period start vs end
- New subscribers in period
- Unsubscribes in period
- Net change + growth rate

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
  "path": "insights/email/reports/<period label>",
  "body": "<the narrative summary + key numbers>"
}
```

Before generating the report, also read any previous report from this path to reference in the "What happened" narrative ("this matches the trend from last month" / "this reverses the dip we flagged").

### 8. Create findings for notable issues

For anything serious (unsub rate spike, deliverability drop, revenue collapse), create a finding so it lands in the dashboard — not just the report.

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
- **Don't invent revenue numbers.** Klaviyo is the only ESP in the cogny-mcp-proxy that exposes revenue data today (via "Placed Order" events with a `value` field). For Mailchimp, Rule, and Get a Newsletter, say "revenue not exposed by this ESP's MCP" and report on engagement only — or let the user paste in list-revenue so you can compute CPM/revenue-per-send on their numbers.
