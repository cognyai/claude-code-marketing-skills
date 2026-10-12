---
name: marketing-brain
description: Build the business "brain" every marketing agent reads first — START-HERE, customer-fit, offers, voice, founder opinions, failed campaigns — by interviewing you and seeding it from your CRM (HubSpot, Pipedrive or Upsales), store (Shopify or WooCommerce) and Stripe, stored in the Cogny context tree
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [cogny, hubspot, pipedrive, upsales, shopify, woocommerce, stripe]
user-invocable: true
argument-hint: "[build|section <name>|review|promote <evidence-node>]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__get_context_tree_overview
  - mcp__cogny__browse_context_tree
  - mcp__cogny__read_context_node
  - mcp__cogny__search_context
  - mcp__cogny__write_context_node
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__Pipedrive__list_users
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__get_deal
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Upsales__list_users
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__mcp__Shopify__tool_get_shop_info
  - mcp__cogny__mcp__Shopify__tool_list_customers
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__WooCommerce__list_customers
  - mcp__cogny__mcp__WooCommerce__list_orders
  - mcp__cogny__mcp__WooCommerce__get_top_sellers_report
  - mcp__cogny__mcp__Stripe__get_stripe_account_info
  - mcp__cogny__mcp__Stripe__stripe_api_search
  - mcp__cogny__mcp__Stripe__stripe_api_details
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - WebFetch
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Marketing Brain

People spin up ten agents, get a mountain of generic copy back, and decide AI marketing
is overhyped. The agents were fine. The context was thin. This skill writes the onboarding doc
you'd give a sharp new hire, and every other agent in `/marketing-engineer` reads it before doing anything.

**Requires:** Cogny ($9/mo) for storage in the context tree and CRM/Stripe seeding.
Without Cogny, the skill writes the same files to `./brain/` locally.

## Usage

- `/marketing-brain` or `/marketing-brain build` — full build (≈60–90 min of interview, can be split)
- `/marketing-brain section voice` — (re)build one section
- `/marketing-brain review` — check every section for vagueness and staleness
- `/marketing-brain promote brain/evidence/customer-language/2026-10-06` — move a proven
  finding from evidence into company policy (human-approved)

## The six files that do most of the work

| Node | What it answers | Bad (useless to an agent) | Good |
|------|-----------------|---------------------------|------|
| `brain/START-HERE` | What we do, for whom, this quarter's priorities, where everything lives | — | One page, links to every node |
| `brain/company/customer-fit` | Who buys, who stays, who we can serve profitably, who to avoid | "SMBs" | "Shopify stores doing $1–10M/yr where the founder still does the books and has been burned by a bookkeeper before" |
| `brain/company/offers` | What we sell, price, what we may promise, what needs approval | "Great service" | "Free profitability review — may say 'in 5 business days'; may NOT promise savings %" |
| `brain/brand/voice` | How we sound, through examples | "Friendly but professional" | 3 loved pieces + why each works, 2 rejected + the exact reason |
| `brain/brand/founder-opinions` | Takes nobody else can generate | "We care about quality" | "Most agencies in our space overcharge for onboarding" |
| `brain/decisions/failed-campaigns` | Lessons that cost real money | — | "Free audit attracted companies too small to afford us (BK006, $4.2k)" |

## Local mode (no Cogny)

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this once and
continue in local mode:

```
Marketing Brain stores the brain in Cogny's context tree and seeds it from your data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your CRM (HubSpot, Pipedrive or Upsales), store (Shopify or WooCommerce) and Stripe.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: build the brain from the interview (and your website), saved as files under ./brain/.
```

**Local layout:** each node is a Markdown file at `./brain/<node path>.md`, the same paths as the
context tree: `brain/company/customer-fit` → `./brain/company/customer-fit.md`, `brain/START-HERE` →
`./brain/START-HERE.md`, `brain/evidence/customer-language/latest` →
`./brain/evidence/customer-language/latest.md`. Keep the `[[brain/...]]` wikilinks as written so the
files move into Cogny unchanged later. Tool mapping: `get_context_tree_overview` / `browse_context_tree`
→ Glob `./brain/**/*.md`; `read_context_node` → Read; `search_context` → Grep under `./brain/`;
`write_context_node` → Write (new file) or Edit (existing file).

## Steps — build

### 1. Check what exists

`get_context_tree_overview`, then `browse_context_tree` on `brain/`. **Local:** Glob `./brain/**/*.md`
and Read each match (age from its `Last reviewed` line). If nodes exist, show
their age and length and ask which ones to rebuild. Never overwrite a human-written node
without showing the diff and getting a yes.

### 2. Seed from data (so the interview starts from facts)

**Check what's connected first.** Call `list_integrations`, then make one cheap read per source
you'll use: HubSpot `get_user_details`, Pipedrive / Upsales `list_users`, Shopify `tool_get_shop_info`,
Stripe `stripe_api_read` `GetSubscriptions {limit: 1}` (restricted keys can't call `get_stripe_account_info`, so don't use it as the probe). A 401, Forbidden or "lacks scope" means 🔴 "reconnect <integration>
in Cogny"; don't retry it. If a tool is missing, call `refresh_mcp_discovery` once, then skip that
source for this run and mark it ⚠ "needs reconnect" (new tools appear only after the client
reconnects). If Cogny isn't available at all, skip seeding and go straight to the interview, writing
to `./brain/`.

**No CRM connected** (no healthy HubSpot, Pipedrive or Upsales): say so once ("No CRM connected:
connect HubSpot, Pipedrive or Upsales in Cogny to seed who-buys from won deals"). Seed from Stripe
(who pays, who stays, who cancels) and the website (offers) only, label customer-fit "seeded from
Stripe + website, no CRM", and leave the who-buys firmographics (industry, size, revenue) and
who-to-avoid for the interview.

- **HubSpot won deals → companies**: `search_crm_objects` on `deals` with `hs_is_closed_won = true`
  (last 24 months), then their associated `companies` (`industry`, `numberofemployees`,
  `annualrevenue`, `country`, `hs_analytics_source`, `hs_ideal_customer_profile` if set). Group them to see
  who actually buys, and compare against `lifecyclestage = customer` companies that are still active. If
  `/crm-icp-analysis` has run, read its output too. These become *drafts* of customer-fit, not the final text.
- **HubSpot lost deals**: `hs_is_closed = true AND hs_is_closed_won = false`. Group `closed_lost_reason`
  (skip duplicate/test noise) as raw material for failed-campaigns and "who to avoid".
- **Pipedrive** instead: won deals `list_deals(status: "won")` and lost deals `list_deals(status: "lost")`
  (cursor-paginated; `get_deal` for `lost_reason`), organizations via `list_organizations`.
  **Upsales** instead: `list_orders` with `probability = 100` (won) or `0` (lost), and accounts via
  `list_accounts`; find custom fields and stages with `get_metadata`.
- **Store** (ecommerce, if Shopify or WooCommerce is connected): who buys and who comes back.
  Shopify `tool_get_shop_info` (currency), `tool_list_customers` (`numberOfOrders`, `amountSpent`),
  `tool_list_orders(query_filter: "created_at:>=<12 months ago>")`. WooCommerce `list_customers`,
  `list_orders(after)`, `get_top_sellers_report`. Compute the repeat-purchase rate, the median order
  value, the top products of repeat buyers vs one-time buyers, and the share of revenue from the top 20% of
  customers. For a store, "who stays" means repeat buyers.
- **Data hygiene before drawing conclusions:** dedupe won deals by company id (one customer can
  have several deals), group amounts by `deal_currency_code` and never add up different
  currencies, and treat stale ICP text stored in the CRM as a hypothesis to test against who
  actually pays. If every lost deal is noise, say so plainly and leave "who to avoid" for the interview.
- **Stripe** (if connected): `stripe_api_read` with `GetSubscriptions` (`status: "all"`) for
  counts by price (`items.data[].price.unit_amount` + currency) and `status: "canceled"` for
  `canceled_at` and `cancellation_details` (tenure = canceled_at − start_date). Use
  `stripe_api_details` to confirm an operation's parameters before calling it. If `GetPrices` /
  `GetProducts` return Forbidden (restricted key), map unit amounts to plans using the pricing
  page. The point is to answer "who stays?", not just "who buys?".
  - **Big pages.** A `GetSubscriptions` page runs to ~370k characters. Page with `limit` (≤100) and
    `starting_after` = the last subscription id while `has_more` is true, let each page spill to a
    file, and aggregate with `jq` (counts by price and currency, tenure, cancellation reasons).
    Never read a page whole into context.
  - **Trials aren't churn.** A canceled subscription whose `ended_at == trial_end` never paid:
    count it as a **trial-only cancellation**, separately from churn. Churn is paying subscriptions
    that ended after the trial. Report both numbers.
- The website (WebFetch the homepage and pricing page) for the offers the company currently claims publicly.

Report what came from where. If a source fails, name it and continue.

### 3. Interview, one section at a time

Ask one question at a time and push back on adjectives. Each section needs specific
answers before you write it:

**customer-fit**
- Describe your three best customers. What did they have in common *before* they bought?
- Who bought and churned? What was true about them?
- Who do you lose money serving? What's the cutoff (size, budget, stage, tooling)?
- Who refers your best customers? (Accountants, agencies, communities…)

**offers**
- List every offer with its price. For each: what may we promise? What must never be said?
- Which claims need someone's sign-off, and whose?

**voice**
- Paste three ads/emails/posts you loved. For each, say in one sentence why it works.
- Paste two you rejected, and the exact reason ("promises results in 30 days; we can't guarantee that").
- Words we never use.

**founder-opinions** (budget the most time here; it's the unfair advantage)
- What does everyone in your category get wrong?
- What would you tell a friend about your competitors, off the record?
- What do you believe about the customer that they don't believe yet?
- Ask for at least 10 opinions. Keep the founder's phrasing verbatim.

**failed-campaigns**
- What did you try that cost real money and didn't work? What did you learn?
- Which channel brings leads that don't close?

### 4. Write the nodes

`write_context_node` for each (local: Write `./brain/<node path>.md`, or Edit if it exists), using `[[brain/...]]` wikilinks between them. Each node
starts with a line `Owner: human · Last reviewed: YYYY-MM-DD`.

Then write `brain/START-HERE`:

```markdown
# START HERE
We help [specific customer] [get specific outcome] by [mechanism].
This quarter: 1) … 2) … 3) …
Read next: [[brain/company/customer-fit]] · [[brain/company/offers]] · [[brain/brand/voice]]
· [[brain/brand/founder-opinions]] · [[brain/decisions/failed-campaigns]]
Fresh evidence: [[brain/evidence/customer-language/latest]]
Rule: agents write to evidence/, campaigns/, experiments/, memos/. Only humans edit company/ and brand/.
```

Also create empty `brain/decisions/agent-corrections` and `brain/experiments/log`.

### 5. Vagueness check before finishing

Run `review` (below) on what you just wrote. Don't finish while any section fails.

## Steps — review

Read every node (local: Glob `./brain/**/*.md`, then Read). For each node, flag:
- 🔴 **Adjective-only** sections: "friendly", "professional", "high quality", "SMBs", "innovative"
- 🔴 **No examples** in voice (needs ≥3 loved, ≥2 rejected, each with a reason)
- 🟡 **Stale**: `Last reviewed` older than 90 days, or contradicted by newer evidence
  (search `brain/evidence/` for findings that conflict; local: Grep `./brain/evidence/`)
- 🟡 **Unbounded claims** in offers: a promise with no "may not say" counterpart
- 🟡 **Contradicted by data**: compare customer-fit against who actually pays and stays (Stripe,
  won deals), and offers against the live website. An old CRM ICP that disagrees with the paying
  customer base is a finding, not a source of truth. With no Stripe and no CRM connected (always
  the case in local mode), print this check as "skipped: no Stripe/CRM" and still compare offers
  against the live website
- 🟡 **Number claims without an approver** (e.g. "+12% ROAS"): every number needs a source and an owner

Print a short scorecard and the top three fixes.

## Steps — promote

Agents only write evidence. When a finding has held for several weeks (e.g. the same
customer phrase has topped the language report for three weeks running), `promote`:
1. Read the evidence node and the target `company/` or `brand/` node (local: Read
   `./brain/evidence/....md` and `./brain/company/....md`; the argument may be the node path or the file path).
2. Show the exact proposed edit as a diff.
3. Write it only after the user says yes (local: Edit the target file), and append "Promoted from [[evidence-node]] on <date>".

## Critical rules

1. **Examples over adjectives.** If the user answers with an adjective, ask for an example.
2. **Founder's words verbatim.** Don't polish founder-opinions into marketing copy.
3. **Never write `company/` or `brand/` without an in-session yes.**
4. **Every claim in offers has a "may not say" twin.**
