---
name: winback-engine
description: Find dormant subscribers, segment by historical value, draft personalized winback emails per tier, and identify suppression candidates
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter]
user-invocable: true
argument-hint: "[aggressive|standard|conservative]"
allowed-tools:
  # Cogny Cloud (aggregated) namespace
  - mcp__cogny__klaviyo__*
  - mcp__cogny__mailchimp__*
  - mcp__cogny__rule__*
  - mcp__cogny__get_a_newsletter__*
  - mcp__cogny__create_finding
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

## Prerequisites Check

Detect connected ESP (same pattern as subject-line-lab). If none, prompt user to connect at cogny.com.

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

**Purchase / LTV data — Klaviyo only.** The cogny-mcp-proxy currently exposes purchase data for Klaviyo (via `list_events` filtered to the "Placed Order" metric, summing the `value` field per profile). Mailchimp, Rule, and Get a Newsletter in this proxy are **engagement-only** — they do not expose:
- Total spend / LTV
- Order count
- AOV
- Last order date

**Per-ESP tool adapter:**

| ESP | Subscriber list | Purchase history | Suppression write |
|-----|-----------------|------------------|-------------------|
| Klaviyo | `list_profiles` (+ `get_profile` for detail) | `list_events` with `metric="Placed Order"` — use `value` field per profile for LTV | `unsubscribe_profiles` |
| Mailchimp | `tool_list_members` (filter `status=subscribed`) | **Not available** | `tool_update_member` (status=unsubscribed) |
| Rule | `tool_list_subscribers` | **Not available** | `tool_update_subscriber` / `tool_list_suppressions` |
| Get a Newsletter | `tool_list_contacts` | **Not available** | `tool_delete_contact` or `tool_update_contact` |

### 3. Segment into tiers

**If Klaviyo (has purchase data):** cross-cut by **engagement recency** × **historical value**:

| Tier | Criteria | Tone | Offer |
|------|----------|------|-------|
| **A — High value dormant** | Dormant + LTV ≥ top quartile OR past purchaser | Personal, apologetic, premium | Strong (20% off, free shipping, exclusive access). This is real money. |
| **B — Medium value dormant** | Dormant + some past engagement or 1 purchase | Warm, value-forward | Moderate (10–15% off, bundle, content) |
| **C — Low engagement dormant** | Dormant + never purchased + low engagement history | Direct, honest | Last-chance offer or content-only |
| **D — Suppression candidates** | Deep dormant + no purchase + no recent engagement | Final email only | "We're removing you unless..." |

**If Mailchimp / Rule / Get a Newsletter (engagement-only):** tier by **engagement depth** instead. No purchase data is available from the proxy for these ESPs — LTV-based tiering falls back to:

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

### 7. Create findings

For each significant tier (A, B with >100 subscribers):

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
- **Only Klaviyo exposes purchase/LTV data** through the cogny-mcp-proxy today. Mailchimp, Rule, and Get a Newsletter fall back to the engagement-only tiering scheme above.
- **Get a Newsletter has no flow/automation object.** "Install as a flow" isn't available — winback is delivered as scheduled individual sends via `tool_send_draft` with `time_to_send`. For Klaviyo, flows install via the Klaviyo UI (the MCP exposes `list_flows`/`get_flow` for reads only, not create). For Mailchimp/Rule, automations/journeys are read-only too — so "install" means drafting campaigns and scheduling them, not creating a native automation.
