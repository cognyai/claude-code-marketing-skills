---
name: shopping-campaign-audit
description: Google Ads Shopping / retail audit (feed cross-checked against Shopify or WooCommerce when connected) — product feed coverage, listing-group granularity, zero-impression products, bidding, top wasted spend
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads, microsoft-ads, shopify, woocommerce]
user-invocable: true
argument-hint: "[campaign name or id]"
allowed-tools:
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  - mcp__cogny__mcp__Google_Ads__tool_get_reporting_view_doc
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Shopify__tool_list_products
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__list_products
  - mcp__cogny__mcp__WooCommerce__get_sales_report
  - mcp__cogny__mcp__WooCommerce__get_top_sellers_report
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - WebSearch
---

# Shopping Campaign Audit

A deep audit of your Shopping and retail campaigns — feed coverage, listing-group
structure, products that never get impressions, and where the spend is leaking.
Covers standard Shopping campaigns and the Shopping side of Performance Max.

**Requires:** Cogny Agent subscription ($9/mo) — [Sign up](https://cogny.com)

## Works with

| Job | Primary | Also answers it | Differences to state |
|-----|---------|-----------------|----------------------|
| Product-level spend and ROAS | Google Ads (`shopping_performance_view`) | — | Microsoft Ads tools give campaign-level Shopping data only |
| Shopping campaign totals | Google Ads | Microsoft Ads (`Bing_Ads`, campaign type `Shopping`) | Bing money is account-currency units, not micros |
| Catalog truth: active, in stock, priced | Shopify (`tool_list_products`) | WooCommerce (`list_products`) | Store IDs ≠ feed item IDs; join on SKU or variant ID |
| Real revenue per product | Shopify (`tool_list_orders`) | WooCommerce (`get_top_sellers_report`, `get_sales_report`) | Store = paid orders across all channels; Ads = attributed |

Call `list_integrations` once. Without a store, the audit runs on Google Ads alone.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Shopping Campaign Audit needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Ads (plus Microsoft Ads, Shopify or
   WooCommerce if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` is missing, say
"connect Google Ads in Cogny" (or "reconnect Google Ads in Cogny" if it's listed but unhealthy
or a read returns 401/permission denied) and stop.

This skill audits the **Google Ads** side of retail. It cannot see Merchant Center
disapprovals directly — where a feed problem is suspected it says so and tells you to
check Merchant Center.

## Usage

`/shopping-campaign-audit` — audit every Shopping + retail PMax campaign
`/shopping-campaign-audit Shopping - All Products` — audit one campaign

## Steps

Google Ads money fields are micros (divide by 1,000,000). An empty GAQL result (no rows, or
the tool returns no output) means zero: no matching entities or no activity in the window.
Report it as 0, not as an error.

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

Confirm which campaigns have a Merchant Center feed attached:

```sql
SELECT campaign.id, campaign.name, campaign.advertising_channel_type,
  campaign.shopping_setting.merchant_id, campaign.shopping_setting.feed_label
FROM campaign
WHERE campaign.advertising_channel_type IN ('SHOPPING', 'PERFORMANCE_MAX')
  AND campaign.status != 'REMOVED'
```

Treat a PMax campaign as retail only if `merchant_id` is set (non-zero). Report the
Merchant Center ID(s), and flag Shopping campaigns pointing at different merchant IDs or
feed labels than expected.

If there are no SHOPPING campaigns and no PMax campaign with a `merchant_id`, report
"no retail campaigns" (and Microsoft Ads Shopping totals, if any) and stop. Skip steps 2 onward.

**Microsoft Ads (if connected):** `tool_get_campaigns` (`account_id`,
`campaign_types: ["Shopping", "PerformanceMax"]`) and `tool_get_report`
(`account_id` from `tool_list_accounts`, `report_type: "campaign"`, `campaign_ids`). Report spend, conversions and revenue in
its own block; product-level depth is Google-only here.

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

**Enhanced when connected: real sales.** Shopify `tool_list_orders` (`query_filter:
"created_at:>=YYYY-MM-DD financial_status:paid"`) or WooCommerce
`get_top_sellers_report` (`date_min`, `date_max`). Bestsellers in the store that get little
Shopping spend are scale candidates; products Ads says convert well but rarely sell in the
store point to attribution or tracking issues. Compare totals as a ratio
("Ads conversion value = 0.6x store paid revenue"), never as a corrected ROAS.

### 3. Feed coverage — products that never run

```sql
SELECT segments.product_item_id, segments.product_title,
  metrics.impressions, metrics.clicks
FROM shopping_performance_view
WHERE segments.date DURING LAST_30_DAYS
```

`shopping_performance_view` only returns products that had impressions, so this query
**cannot find zero-impression products** on its own: it gives the list of products that ran.
Finding the ones that never ran needs the full catalog to compare against, from the store
(Shopify / WooCommerce, below) or from Merchant Center. Without a store connected, report
"products with impressions: N", say the zero-impression count needs the catalog, and tell
the user to check Merchant Center → Products → "Not eligible / Disapproved".

Products in the catalog but absent here are usually disapproved, out of stock, missing
required attributes, or priced uncompetitively.

**Enhanced when connected: check against the store catalog.**
- Shopify: `mcp__cogny__mcp__Shopify__tool_list_products` (`status: "ACTIVE"`,
  `first: 250`, paginate with `after`). Shopify feed IDs usually look like
  `shopify_<country>_<productId>_<variantId>`; match on the variant ID or SKU.
- WooCommerce: `mcp__cogny__mcp__WooCommerce__list_products` (`status: "publish"`,
  `per_page`, `page`); match on `sku` or product ID.

Catalog products absent from the query above are the zero-impression products. Split them
into **in stock and active in the store** (a real problem, the expensive one) and **out of
stock or draft** (expected). For the first group, Ads data can't tell "disapproved or not
eligible" from "never reached the feed"; Merchant Center shows which. Also flag
spending products that are out of stock or archived in the store: that's spend on clicks
that can't convert.

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
- Of the zero-impression products: N active + in stock in [Shopify/WooCommerce] (fix these)
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

Cloud uses `create_ticket` with the same content, fields mapped per section 2 of the routing guide.

Action types: `feed_optimization`, `listing_group`, `bidding_strategy`,
`campaign_optimization`, `negative_keyword`.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Feed coverage first.** Products that never run are revenue you've already paid
   to build campaigns around.
2. **Be honest about Merchant Center's blind spot** — name it, don't fake it.
3. **Quote real numbers**: coverage %, wasted spend, ROAS by product type.
4. **Read-only.** Recommend bid and exclusion changes; never make them. Store write tools
   (`tool_update_product`, `update_product`) are never called by this audit; if the user
   asks for a fix, the skill asks first.
5. **Store and Ads numbers stay side by side.** Name the source on every figure.
