---
name: revenue-audit
description: Audit an email marketing program for revenue leaks — missing flows, dormant high-value subscribers, under-segmentation, promo gaps, stale automations — ranked by estimated $ impact
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter]
user-invocable: true
argument-hint: ""
allowed-tools:
  - mcp__cogny__klaviyo__*
  - mcp__cogny__mailchimp__*
  - mcp__cogny__rule__*
  - mcp__cogny__get_a_newsletter__*
  - mcp__cogny__create_finding
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
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

## Prerequisites Check

Detect connected ESP. If the user has multiple connected, run against each and produce separate reports. If the ESP has no ecom integration (Rule, Get a Newsletter without ecom), the audit runs engagement-only and revenue numbers are flagged as estimated.

## Steps

### 1. Establish baseline context

Pull once and reference throughout:
- Total active subscribers
- Average open rate + CTR (last 90 days)
- Total email revenue (last 90 days, if ecom) — this is the denominator for every % impact claim
- Average AOV (if ecom)
- List growth rate (last 90 days)
- Active flows / automations and their performance
- Last 90 days of campaign sends

If no ecom data, use **estimated value per subscriber per month** = (list revenue from user input OR industry benchmark $0.10–$2.00 depending on vertical).

### 2. Run the nine checks

For each check, output: **finding title + estimated $ lift + evidence + recommended fix**.

#### Check 1 — Missing core flows
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

For each missing or disabled flow, estimate lift: `total_email_revenue × benchmark_%` as the annualized $ left on the table.

#### Check 2 — Dormant high-value subscribers
Segment current active list by:
- **Ever purchased** × **engaged in last 60 days**

Count subscribers who have purchased at least once but haven't opened/clicked in 60+ days. Estimate:
`count × avg_AOV × 3% reactivation rate × 2 orders/year = annualized recoverable revenue`

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

#### Check 7 — Post-purchase upsell / cross-sell gap (ecom only)
For brands with purchase data:
- Does a post-purchase flow exist? (Check 1)
- Does it include category-appropriate upsell or accessory recommendations?
- What's the 30-day repurchase rate? If <15%, post-purchase is underbuilt.

Estimate: `customers_per_month × current_repurchase_rate_gap × avg_AOV`.

#### Check 8 — List capture inference
Compare list growth rate to benchmarks:
- Ecom site with steady traffic: 2–5% monthly list growth is healthy
- <1% monthly growth = under-capturing

If growth is weak, flag: "Your site traffic (if paired with analytics MCP) vs. your list growth implies a capture rate of X%. Industry benchmark is 2-5%." Recommend: exit-intent popup, post-purchase capture, content offer gate.

#### Check 9 — Over-reliance on discounting
Scan subject lines and body content of broadcasts for % off / $ off / "sale" / "discount" / promo codes. If >60% of broadcasts lead with a discount:
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

### 5. Create a finding for every item

Every finding in the output also becomes a `create_finding` in Cogny, so the dashboard has the same ranked list the user just saw:

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
- If the connected ESP is Get a Newsletter or Rule without ecom: run engagement-focused checks only (1, 3, 4, 5, 6, 9) and skip revenue checks (2, 7) with a note.
