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
  - mcp__cogny__klaviyo__*
  - mcp__cogny__mailchimp__*
  - mcp__cogny__rule__*
  - mcp__cogny__get_a_newsletter__*
  - mcp__cogny__create_finding
  - mcp__cogny__write_context_node
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
- Purchase history if ecom integration exists (Klaviyo, Mailchimp eComm):
  - Total spend (lifetime value)
  - Order count
  - Average order value (AOV)
  - Last order date
- Signup source / list
- Tags / segments
- Email domain (gmail, yahoo, hotmail, corporate)

### 3. Segment into tiers

Cross-cut by **engagement recency** × **historical value**:

| Tier | Criteria | Tone | Offer |
|------|----------|------|-------|
| **A — High value dormant** | Dormant + LTV ≥ top quartile OR past purchaser | Personal, apologetic, premium | Strong (20% off, free shipping, exclusive access). This is real money. |
| **B — Medium value dormant** | Dormant + some past engagement or 1 purchase | Warm, value-forward | Moderate (10–15% off, bundle, content) |
| **C — Low engagement dormant** | Dormant + never purchased + low engagement history | Direct, honest | Last-chance offer or content-only |
| **D — Suppression candidates** | Deep dormant + no purchase + no recent engagement | Final email only | "We're removing you unless..." |

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
- If purchase data isn't available (Get a Newsletter, Rule without ecom integration), tier A/B/C purely on engagement recency + depth.
