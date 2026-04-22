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

Detect connected ESP (check both `mcp__cogny__<svc>__*` and `mcp__<svc>__*` namespaces). If the user has multiple connected, run against each and produce separate reports.

**Revenue data availability (cogny-mcp-proxy as of this writing):**

| ESP | Has flows/automations? | Has purchase/revenue data? |
|-----|------------------------|----------------------------|
| Klaviyo | ✓ (`list_flows`) | ✓ (via `list_events` with metric="Placed Order", `value` field) |
| Mailchimp | ✓ (`tool_list_automations`) | ✗ — engagement only |
| Rule | ✓ (`tool_list_journeys`) | ✗ — engagement only |
| Get a Newsletter | ✗ — no flow concept exists | ✗ — engagement only |

For non-Klaviyo ESPs, revenue estimates must be either (a) supplied by the user (paste historical email revenue), or (b) flagged as "engagement uplift only" with no dollar figures.

## Steps

### 1. Establish baseline context

Pull once and reference throughout:
- Total active subscribers
- Average open rate + CTR (last 90 days)
- **Klaviyo only:** Total email revenue (last 90 days) via `list_events` with `metric="Placed Order"`, summed `value` field, filtered to events attributed to email campaigns. This is the denominator for every % impact claim.
- **Klaviyo only:** Average AOV (total revenue / order count in period)
- List growth rate (last 90 days)
- Active flows / automations / journeys and their performance (Klaviyo / Mailchimp / Rule only — Get a Newsletter has no equivalent)
- Last 90 days of campaign sends

**If connected ESP is Mailchimp, Rule, or Get a Newsletter:** prompt the user for their approximate 90-day email revenue (or let them skip it). If they skip, use **estimated value per subscriber per month** = (industry benchmark $0.10–$2.00 depending on vertical) as a rough denominator, and clearly label every revenue estimate as "based on industry benchmark, not your actual data."

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

**For Mailchimp / Rule / Get a Newsletter:** purchase data is not exposed. Degrade this check to "dormant deeply-engaged subscribers" — pull subscribers with high historical open+click counts who haven't engaged in 60+ days, present as engagement-uplift opportunity without a dollar figure.

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

#### Check 7 — Post-purchase upsell / cross-sell gap (Klaviyo only)

Purchase-data-dependent — only runs for Klaviyo. Uses `list_events` with `metric="Placed Order"` to compute repurchase cadence.

For brands with purchase data:
- Does a post-purchase flow exist? (Check 1)
- Does it include category-appropriate upsell or accessory recommendations?
- What's the 30-day repurchase rate? If <15%, post-purchase is underbuilt.

Estimate: `customers_per_month × current_repurchase_rate_gap × avg_AOV`.

**For Mailchimp / Rule / Get a Newsletter:** skip this check with a one-line note ("skipped — no purchase data exposed by this ESP's MCP; rerun with Klaviyo or paste purchase data manually").

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
- **ESP-specific check coverage (cogny-mcp-proxy):**
  - Klaviyo: all 9 checks run with dollar estimates.
  - Mailchimp: Checks 1, 3, 4, 5, 6, 8, 9 run normally. Checks 2 and 7 degrade to "engagement-only" framing.
  - Rule: same as Mailchimp.
  - Get a Newsletter: Check 1 is skipped (no flow concept). Checks 2 and 7 are skipped (no purchase data). The remaining checks (3, 4, 5, 6, 8, 9) run on engagement data only.
