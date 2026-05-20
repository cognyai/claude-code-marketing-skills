---
name: shopping-campaign-audit
description: Google Ads Shopping / retail audit — product feed coverage, listing-group granularity, zero-impression products, bidding, top wasted spend
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads]
user-invocable: true
argument-hint: "[campaign name or id]"
allowed-tools:
  - mcp__cogny__google_ads__tool_list_accessible_accounts
  - mcp__cogny__google_ads__tool_execute_gaql
  - mcp__cogny__google_ads__tool_get_gaql_doc
  - mcp__cogny__google_ads__tool_get_reporting_view_doc
  - mcp__cogny__create_finding
  - WebFetch
  - WebSearch
---

# Shopping Campaign Audit

A deep audit of your Shopping and retail campaigns — feed coverage, listing-group
structure, products that never get impressions, and where the spend is leaking.
Covers standard Shopping campaigns and the Shopping side of Performance Max.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com/agent)

## Prerequisites Check

If `mcp__cogny__google_ads__tool_execute_gaql` is not available, print the Cogny
sign-up instructions (see `/google-ads-audit`) and stop.

This skill audits the **Google Ads** side of retail. It cannot see Merchant Center
disapprovals directly — where a feed problem is suspected it says so and tells you to
check Merchant Center.

## Usage

`/shopping-campaign-audit` — audit every Shopping + retail PMax campaign
`/shopping-campaign-audit Shopping - All Products` — audit one campaign

## Steps

### 1. Find the retail campaigns

```sql
SELECT campaign.id, campaign.name, campaign.status,
  campaign.advertising_channel_type, campaign.bidding_strategy_type,
  campaign_budget.amount_micros, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value
FROM campaign
WHERE campaign.advertising_channel_type IN ('SHOPPING', 'PERFORMANCE_MAX')
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

For PMax campaigns, confirm a Merchant Center feed is attached before treating them
as retail.

### 2. Product-level performance

```sql
SELECT segments.product_item_id, segments.product_title,
  segments.product_type_l1, segments.product_brand,
  metrics.cost_micros, metrics.conversions, metrics.conversions_value,
  metrics.clicks, metrics.impressions
FROM shopping_performance_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

Compute:
- **Wasted spend** — sum the cost of products with spend and zero conversions
- **The 80/20** — what share of products drive 80% of revenue
- **ROAS spread** — best vs worst product type

Flag:
- High-spend, zero-conversion products (bid them down or exclude)
- Product types where ROAS is below account break-even

### 3. Feed coverage — products that never run

```sql
SELECT segments.product_item_id, segments.product_title,
  metrics.impressions, metrics.clicks
FROM shopping_performance_view
WHERE segments.date DURING LAST_30_DAYS
```

Products with **zero impressions** are usually disapproved, out of stock, missing
required attributes, or priced uncompetitively. Flag the count and tell the user to
cross-check Merchant Center → Products → "Not eligible / Disapproved".

### 4. Listing-group granularity

```sql
SELECT ad_group.name, ad_group_criterion.listing_group.type,
  ad_group_criterion.listing_group.case_value.product_type.value,
  ad_group_criterion.cpc_bid_micros, campaign.name
FROM product_group_view
WHERE campaign.advertising_channel_type = 'SHOPPING'
```

Flag:
- Everything in one "All products" node — no way to bid up winners or down losers
- A unit (`UNIT` type) catching far too many SKUs to bid meaningfully
- Bestsellers and clearance stock sharing the same bid

### 5. Bidding & priority

Flag:
- Manual CPC on a large catalog (unmanageable — Smart Bidding or PMax fits better)
- Target ROAS set far from achievable ROAS (starves or overspends the campaign)
- Standard Shopping and retail PMax both enabled for the same products (PMax wins the
  auction — the Shopping campaign is just paying for reporting)

### 6. Campaign structure

Flag:
- No separation of brand vs non-brand, or bestsellers vs long-tail
- A single catch-all campaign — fine to start, but it caps optimization

### 7. Score and report

```
Shopping Campaign Audit — [Account Name]
Shopping Score: X/100  ·  30-day spend: [X]  ·  ROAS: [X.Xx]

Catalog health:
- Products with impressions: X of Y (Z% coverage)
- Wasted spend (0-conversion products): $X,XXX
- Top product type by ROAS: ... | Worst: ...

🔴 Critical   — zero-coverage catalog share, big zero-conversion spend
🟡 Important  — flat listing groups, bidding mismatch, PMax/Shopping overlap
🟢 Optimization — split out bestsellers, brand vs non-brand

Top 3 Actions:
1. [Highest $ impact]
2. ...
3. ...
```

### 8. Record findings

```json
{
  "title": "31% of catalog gets zero impressions — likely feed disapprovals",
  "body": "412 of 1,330 active products had zero impressions in 30 days. This is almost always Merchant Center disapprovals or missing attributes (GTIN, image, price). Check Merchant Center → Products for the disapproval reasons; fixing them unlocks inventory you're already paying to advertise around.",
  "action_type": "feed_optimization",
  "expected_outcome": "More eligible products in the auction, higher revenue at the same budget",
  "estimated_impact_usd": 2200,
  "priority": "high"
}
```

Action types: `feed_optimization`, `listing_group`, `bidding_strategy`,
`campaign_optimization`, `negative_keyword`.

## Critical rules

1. **Feed coverage first.** Products that never run are revenue you've already paid
   to build campaigns around.
2. **Be honest about Merchant Center's blind spot** — name it, don't fake it.
3. **Quote real numbers**: coverage %, wasted spend, ROAS by product type.
4. **Read-only.** Recommend bid and exclusion changes; never make them.
