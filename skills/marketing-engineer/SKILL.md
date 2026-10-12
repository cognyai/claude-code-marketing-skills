---
name: marketing-engineer
description: Run the marketing-engineer operating system — one shared brain, ten agents, a review queue, and a weekly loop — on top of Cogny's MCPs. Sets it up, runs the weekly loop, runs one campaign end to end, and schedules the agents with guardrails enforced in the tools rather than the prompt.
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [cogny, hubspot, pipedrive, upsales, fibbler, google-ads, meta-ads, linkedin-ads, bing-ads, tiktok-ads, x-ads, reddit-ads, snapchat-ads, apple-search-ads, openai-ads, bidtheatre, search-console, bing-webmaster, semrush, ahrefs, ga4, posthog, mixpanel, growthbook, stripe, fortnox, shopify, woocommerce, linkedin-organic, x-organic, youtube, crisp, discord]
user-invocable: true
argument-hint: "[setup|week|campaign <idea>|status|schedule]"
allowed-tools:
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - mcp__cogny__cogny_status
  - mcp__cogny__list_integrations
  - mcp__cogny__get_context_tree_overview
  - mcp__cogny__browse_context_tree
  - mcp__cogny__read_context_node
  - mcp__cogny__search_context
  - mcp__cogny__write_context_node
  - mcp__cogny__list_tickets
  - mcp__cogny__get_ticket
  - mcp__cogny__create_ticket
  - mcp__cogny__list_findings
  - mcp__cogny__get_finding
  - mcp__cogny__create_finding
  - mcp__cogny__get_queue_status
  - mcp__cogny__list_automations
  - mcp__cogny__get_automation_run
  - mcp__cogny__list_scripts
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__Pipedrive__list_users
  - mcp__cogny__mcp__Upsales__list_users
  - mcp__cogny__mcp__app-fibbler-co__get_account_overview
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_account
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Search_Console__tool_list_properties
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_sites
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_organizations
  - mcp__cogny__mcp__X_Organic__tool_get_me
  - mcp__cogny__mcp__YouTube__get_channel
  - mcp__cogny__mcp__Discord__list_guilds
  - mcp__cogny__mcp__Crisp__list_conversations
  - mcp__cogny__mcp__Stripe__get_stripe_account_info
  - mcp__cogny__mcp__Fortnox__get_company_information
  - mcp__cogny__mcp__Shopify__tool_get_shop_info
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Marketing Engineer

Each agent in this playbook is a skill, and the skills share one **brain**. You
spend your time editing what the agents produce, not producing it yourself.

> The cost of an experiment keeps collapsing. Whoever runs the most good
> experiments learns fastest. Most ideas die waiting for a designer, a developer,
> an analyst and two meetings. This system removes that wait.

**Requires:** Cogny ($9/mo) — [Sign up](https://cogny.com). Every agent reads
from Cogny's managed MCPs. Free skills in this repo still work without it.

## The system at a glance

| # | Agent (skill) | Reads | Writes | Cadence |
|---|---------------|-------|--------|---------|
| 0 | `/marketing-brain` | You (interview), CRM won/lost deals (HubSpot / Pipedrive / Upsales), store orders (Shopify / WooCommerce), Stripe | `brain/company/*`, `brain/brand/*` (human-approved) | Once, then on every rejection |
| 1 | `/customer-language` | CRM calls/meetings/notes, Crisp chats, Discord, YouTube comments, local transcripts | `brain/evidence/customer-language/*` | Mon 07:00 |
| 2 | `/campaign-ledger` | Google, Microsoft, Meta, LinkedIn, TikTok, X, Reddit, Snapchat, Apple Search, ChatGPT ads, Bidtheatre; GA4; CRM; fibbler | `brain/campaigns/ledger` | Daily |
| 3 | `/buying-triggers` | fibbler warm accounts, CRM accounts (HubSpot / Pipedrive / Upsales), Upsales site visits, Brave News | `brain/evidence/triggers/*`, draft outreach | Tue + Thu |
| 4 | `/search-demand` | Search Console, Bing Webmaster, Semrush / Ahrefs, AI visibility, Brave | `brain/evidence/search/*`, page briefs | Wed |
| 5 | `/creative-engine` | Brain + customer language + brand assets | Images (Cloud) or briefs (Solo), **paused** ads on Meta / LinkedIn / TikTok / Reddit / X / Snapchat | On demand |
| 6 | `/ad-kill-rules` | Ad-level insights on every platform | Pauses losers (the only write) | Daily 08:00 |
| 7 | `/closed-lost-revival` | CRM lost deals + their calls/notes (HubSpot / Pipedrive / Upsales) | `brain/evidence/closed-lost/*`, draft notes | Weekly |
| 8 | `/social-engine` | LinkedIn / X / YouTube organic stats, X search, Brave, Crisp, Discord | Draft posts (scheduled only after a yes) | Sun batch |
| 9 | `/performance-memo` | Ledger + fibbler + CRM + Stripe/Fortnox + store revenue + PostHog/Mixpanel + GrowthBook | `brain/memos/performance/*` | Mon 07:30 |

Build them **one at a time**. Get `/customer-language` reliable before adding the next.
A confused workflow running every morning gives you a reliable supply of confusion.

## Shared conventions (every agent in this system follows these)

### The brain lives in the Cogny context tree

```
brain/
  START-HERE                       ← every agent reads this first
  company/customer-fit             ← who buys, who stays, who you can serve profitably
  company/offers                   ← what you sell, price, allowed claims, claims needing approval
  brand/voice                      ← 3 loved examples + why, 2 rejected + why
  brand/founder-opinions           ← strong takes nobody else can generate
  decisions/failed-campaigns       ← lessons that cost real money
  decisions/agent-corrections      ← every fix you made to an agent's judgment
  evidence/customer-language/      ← latest + dated reports
  evidence/triggers/               ← buying-trigger shortlists
  evidence/search/                 ← question inventory, AI-visibility snapshots
  evidence/closed-lost/            ← ledger of real loss reasons + reopen conditions
  evidence/social/                 ← listening digests, organic hook results
  campaigns/ledger                 ← one row per campaign ID
  campaigns/<ID>                   ← the campaign folder: quotes, offer, assets, results
  experiments/log                  ← tested / why / result / next
  contracts/<agent>                ← each agent's job description + guardrails
  memos/performance/               ← Monday memos
```

**The one rule that keeps the brain healthy:** agents write to `evidence/`,
`campaigns/`, `experiments/` and `memos/`. Only a human moves something into
`company/` or `brand/`. An agent may *propose* an edit to those nodes as a ticket, but
must never write it unless the user says yes in the current session. Otherwise one
agent's hunch quietly becomes company policy.

### Campaign IDs travel everywhere

Format: `<PREFIX><NNN>` (e.g. `BK014`). The ID goes in:
- UTM: `utm_campaign=bk014_<slug>`
- Every ad name: `BK014_<angle>_<format>_v<n>` (e.g. `BK014_dinner-angle_ugc_v2`)
- Every email/newsletter name and every scheduled organic post's tracking link
- The deal in the CRM: a `campaign_id` deal property in HubSpot (ask a HubSpot admin to create it), otherwise the contact's original-source UTM (`hs_analytics_source_data_2`)

`/campaign-ledger` owns ID allocation and the naming audit.

### The review queue: tickets (Cloud) or findings (Solo)

Anything that needs a human decision becomes a review item. On **Cloud** that's `create_ticket`
(`execution_target: "manual"`), and the queue is read with `list_tickets`. On **Solo** it's
`create_finding` (put the urgency in `priority` and the category in `action_type`), and the queue
is read with `list_findings`. Use whichever tool the workspace has; the field mapping is in
`references/mcp-routing.md` section 2. Solo caps findings at 100, so merge stale ones before filing more. Each ticket must be decidable in **under a minute**:
- **Title:** the decision ("Approve: dinner-angle ads for BK014 (3 ads, paused)")
- **Body:** what changes, what it touches, and the evidence (quote + source)
- **expected_outcome:** measurable, with the evidence bar
- **estimated_cost_usd + cost_cadence + cost_type:** whenever approving it activates spend

Never use tickets for routine numbers. A quiet week should produce a short queue.

**Title prefix:** every review item an agent in this system files starts with `[ME:<agent>]`
(e.g. `[ME:creative-engine] Approve: …`), on either plan. The workspace queue also holds platform,
support and automation items, so `week` mode filters `list_tickets` / `list_findings` on this prefix.

### Guardrails live in the tools, not the prompt

"Always ask before sending" is only a suggestion to a model. Real guardrails:
1. **Read-only by default.** Every agent starts with read tools only.
2. **Create paused, never active.** Ads are created with `status: PAUSED`. Budgets stay with the human.
3. **Draft, never send.** Outreach and newsletters are drafts. Organic posts are scheduled only after an explicit yes.
4. **Scheduled agents get grants, not trust.** When scheduling via `create_automation`,
   grant only the specific write tools needed, pinned with `constraints` (e.g. pin
   `status: "PAUSED"` on `update_ad_status` so the kill-switch can pause but never activate).
5. **Exact rules are code, judgment is model.** Spend caps, suppression lists, dedupe and
   CTR thresholds go in `create_script` (deterministic JS). Fit and tone are judgment calls for the model.
6. **"Done" means every source was checked, and any failure was reported.** An agent that says "HubSpot
   returned 3 empty call notes today" is worth ten that quietly skip them. Every output node ends
   with a `Failures:` line (or `Failures: none`), which `status` mode reads.

### Real-data rules (learned from live runs; every agent follows these)

1. **Big responses spill to a file.** CRM searches with many properties, GSC at 5,000 rows and
   Stripe lists can return 100k–400k characters. Page HubSpot searches with `after`
   (≤100 per page) and request only the properties you need. When a result is saved to a file,
   process it with `jq` or a short script instead of reading it whole, and prefer smaller limits.
2. **Never sum across currencies.** Ad accounts may be SEK, Stripe may mix usd/sek/eur. Report in
   each account's currency (read it from the platform: `customer.currency_code`, account
   currency), and state any FX rate used. Some CRM amounts are in minor units (49900 = 499.00),
   so sanity-check against the price list.
3. **CRM noise.** Expect duplicate deals and companies, test records, and deals without
   associated companies. Dedupe by HubSpot company id (or normalized domain), report raw vs unique
   counts, and exclude deals whose reason or name says duplicate, test or merged. Deal stages are
   pipeline-specific ids, so map them with `get_properties(deals, dealstage)` before counting.
4. **"Active" means delivering.** Meta: use `effective_status` (an `ACTIVE` ad under a paused
   campaign isn't live). Google: require ad, ad group and campaign `ENABLED`. X: check the parent
   campaign and line item.
5. **First run has no brain.** When a `brain/` node is missing, say so once, use the stated
   fallback (usually the CRM's call and meeting notes, or asking the user), and label the output
   "no brain: provisional".

## The CRM layer

The CRM is where customer truth lives: who bought, who was lost and why, what they said on calls,
and which campaign they came from. **HubSpot is the default.** Connect it in Cogny and every agent
uses it read-only. Bigger CRMs map onto the same jobs:

| Job | HubSpot (`search_crm_objects`) | Pipedrive (`Pipedrive`) | Upsales (`Upsales`) | Salesforce (custom MCP) |
|-----|--------------------------------|-------------------------|---------------------|-------------------------|
| Won deals | `deals`: `hs_is_closed_won = true`, `closedate`, `amount`, `deal_currency_code` | `list_deals(status: "won")`: `value`, `currency`, `won_time` | `list_orders` with `probability = 100`, `date`, `value`, `currency` | `Opportunity`: `IsWon = true`, `CloseDate`, `Amount` |
| Lost deals + reason | `deals`: `hs_is_closed = true AND hs_is_closed_won = false`, `closed_lost_reason` | `list_deals(status: "lost")`, then `get_deal` for `lost_reason`, `lost_time` | `list_orders` with `probability = 0`; reason in a custom field (find it with `get_metadata`) | `Opportunity`: `IsClosed AND NOT IsWon`, `Loss_Reason__c` |
| Open pipeline | `deals`: `hs_is_closed = false`; stage labels via `search_properties` | `list_deals(status: "open")`, `list_stages` | `list_opportunities` (probability < 100) | `Opportunity`: `IsClosed = false` |
| Call / meeting words | `calls` (`hs_call_body`), `meetings` (`hs_meeting_body`, `hs_internal_meeting_notes`), `notes` (`hs_note_body`) | `list_activities(deal_id / org_id)`: `subject`, `note` | `list_activities`, `list_appointments` (`notes`, `description`) | `Task`, `Event` (`Description`) |
| Support pain | `tickets` (`subject`, `content`) | — (use `Crisp`) | — (use `Crisp`) | `Case` |
| Accounts | `companies` (`domain`, `industry`, `numberofemployees`, `annualrevenue`, `lifecyclestage`) | `list_organizations` | `list_accounts` | `Account` |
| Opt-outs | contacts `hs_email_optout`, `hs_lead_status` | person `marketing_status` (from `list_persons`) when present | contact `active`, unsubscribed flags (via `get_metadata`) | `HasOptedOutOfEmail`, `DoNotCall` |
| Last touch | `notes_last_contacted`, `hs_last_sales_activity_timestamp` | latest `list_activities(org_id)` | latest `list_activities` / `list_appointments` filtered by `client.id` | `LastActivityDate` |
| Campaign source | contacts `hs_analytics_source_data_2` (paid `utm_campaign`), deal property `campaign_id` | deal custom field `campaign_id` (define it; see `list_deal_fields`) | `list_leads` source, `list_campaigns` | `Opportunity.CampaignId` |
| Site re-engagement | `hs_analytics_last_visit_timestamp`, `recent_conversion_date` | — | `list_visits` (Upsales web tracking) | Pardot fields |

Pipedrive lists are cursor-paginated (`limit` ≤ 500, `cursor` from `next_cursor`). Upsales uses
`limit` (≤ 1000) + `offset` and `filters=[{"field": "client.id", "comparator": "eq", "value": …}]`;
its responses can be very large, so keep `limit` small. Salesforce CRM and Attio connect through
`add_custom_mcp_server`. Map the same jobs and write the mapping to `brain/contracts/crm-layer`
so every agent uses it. Fibbler's
deal attribution (`get_influenced_deals`, `get_deal_attribution_summary`) takes
`crm: "hubspot" | "salesforce" | "copper" | "attio"`, with **no Pipedrive**; only `get_warm_accounts`
accepts `pipedrive`. On Pipedrive or Upsales, join fibbler's warm accounts to CRM deals by domain yourself.

**Read-only, always.** No agent in this system writes to the CRM. Proposed fields (e.g.
`campaign_id`, `reopen_condition`) go to a HubSpot admin as a ticket.

## Usage

- `/marketing-engineer setup` — first-time setup (Step 1–3 below)
- `/marketing-engineer week` — run the Monday review: memo, queue, keep/kill/change/test
- `/marketing-engineer campaign <idea>` — run one campaign end to end across all agents
- `/marketing-engineer status` — what's built, what's stale, what's broken
- `/marketing-engineer schedule` — put the reliable agents on a schedule with grants

## Prerequisites check

1. **Connected.** Call `cogny_status` **and** `list_integrations`. If no `mcp__cogny__*` tools exist
   (no `list_integrations`, no `cogny_status`), print this and switch to **local mode** (below):

   ```
   Marketing Engineer needs your marketing data through Cogny's MCP gateway.

   1. Sign up at https://cogny.com and connect your CRM, ad platforms, Search Console and Stripe
      (whichever you use; each agent lists what it needs).
   2. Add Cogny to .mcp.json in your project:
      {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
   3. Restart Claude Code; it opens a browser for the OAuth login on first use.

   Without Cogny you can still: run /marketing-brain and /customer-language locally
   (files under ./brain/); the other agents need Cogny.
   ```

   **Local mode.** Without Cogny you can run `/marketing-brain` and `/customer-language` locally
   (files under `./brain/<node path>.md`, e.g. `./brain/company/customer-fit.md`); the other agents
   need Cogny. `setup` runs those two (see Mode: setup) and stops; `week`, `campaign`, `status` and
   `schedule` stop after the block above. Skip steps 2–4 and the table.
2. **Plan (tier).** Detect it from the tools that exist, since `cogny_status` doesn't name it:
   **Cloud** if `create_ticket` / `list_tickets` exist, **Solo** if `create_finding` /
   `list_findings` exist. Automations and scripts are on if `list_automations` responds. Print the
   plan on the last row of the table and use it to pick the review-queue tools everywhere below.
3. **Health.** `list_integrations` `health_status` misses revoked tokens (a 401 LinkedIn Ads token
   still reads `healthy`). For each integration an agent needs, make **one cheap read**. A 401,
   Forbidden or "lacks scope" means 🔴 "reconnect <integration> in Cogny"; don't retry the same call.

   | Integration | Cheap read |
   |-------------|------------|
   | HubSpot | `get_user_details` |
   | Pipedrive / Upsales | `list_users` (Upsales: `limit: 1`) |
   | fibbler | `get_account_overview` |
   | Google / Meta / LinkedIn / Bing / TikTok / X / Reddit Ads | `tool_list_accessible_accounts` / `tool_list_ad_accounts` / `tool_list_ad_accounts` / `tool_list_accounts` / `tool_list_advertisers` / `tool_list_ad_accounts` / `tool_list_ad_accounts` |
   | Snapchat / Apple Search / ChatGPT ads | `tool_list_organizations` / `tool_list_acls` / `tool_get_ad_account` |
   | GA4 / Search Console / Bing Webmaster | `tool_list_account_summaries` / `tool_list_properties` / `tool_get_sites` |
   | LinkedIn Organic / X Organic / YouTube | `tool_list_organizations` / `tool_get_me` / `get_channel` |
   | Discord / Crisp | `list_guilds` / `list_conversations` (page 1) |
   | Stripe / Fortnox / Shopify | `stripe_api_read` `GetSubscriptions {limit: 1}` (not `get_stripe_account_info`, which restricted keys can't call) / `get_company_information` / `tool_get_shop_info` |

   Brave Search, AI Visibility, Image Gen and Ahrefs-lite are Cogny-native and don't appear in
   `list_integrations`. Treat them as available if their tools load.
4. **Missing tool.** If a tool an agent needs isn't loaded, call `refresh_mcp_discovery` once. New
   tools only appear after the client reconnects, so use that agent's fallback for this run, mark
   the source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP.

Map channels to agents and print the table:

```
Agent                Needs                                   Status
customer-language    CRM (HubSpot / Pipedrive / Upsales), Crisp, Discord, YouTube, or local transcripts   ✅ Discord · ⚪ CRM
campaign-ledger      ≥1 ad platform + GA4 or Plausible (+ CRM)    ✅ (Google, Meta, Bing, TikTok, X) · 🔴 LinkedIn: reconnect
buying-triggers      app-fibbler-co and/or CRM                    ✅ fibbler · ⚪ CRM
search-demand        Search Console (+ Bing, Semrush/Ahrefs)      ✅
creative-engine      Meta / LinkedIn / TikTok / Reddit / X / Snapchat Ads   ✅
ad-kill-rules        any ad platform with a pause tool            ✅
closed-lost-revival  CRM (HubSpot / Pipedrive / Upsales)          ⚪ connect a CRM in Cogny
social-engine        LinkedIn Organic / X Organic / YouTube        ✅
performance-memo     ledger + Stripe / Fortnox / store platform   ✅
Plan                 Solo: no BigQuery, scripts, automations, image gen · Cloud: all   (detected: Cloud)
```

If a single source is missing or broken, mark that agent ⚪ ("connect X in Cogny") or 🔴
("reconnect X in Cogny") and continue. Never fail the whole run.

## Mode: setup

**Local mode (no Cogny):** check for `./brain/START-HERE.md` (Glob `./brain/**/*.md`); if it's missing, run
the `/marketing-brain` interview, writing to `./brain/`. Then run `/customer-language` on the user's local
transcripts and have them compare it with their own memory of those calls; save corrections to
`./brain/decisions/agent-corrections.md`. Then stop: the remaining steps need Cogny.

1. **Desk.** Confirm `.mcp.json` has the Cogny server and the skills are installed.
2. **Brain.** Call `get_context_tree_overview`. If `brain/START-HERE` is missing, run the
   `/marketing-brain` interview now. Nothing else is worth building on a thin brain.
3. **Data.** Run `/campaign-ledger init` to pick a campaign-ID prefix, audit current
   naming across platforms, and create `brain/campaigns/ledger`.
4. **Contracts.** For each agent the user wants, write `brain/contracts/<agent>` using the
   template below.
5. **First agent.** Run `/customer-language` and have the user compare it with their own memory
   of those calls. Save every correction to `brain/decisions/agent-corrections`.
6. Stop there. Tell the user to add the next agent only once this report is trusted (usually 3–4 rounds).

### Contract template (`brain/contracts/<agent>`)

```markdown
# <Agent> contract
Job: <one sentence>
Reads: <sources + limits, e.g. "HubSpot calls + meetings, last 7 days, max 200">
May write: <exact nodes / draft locations>
May NOT: <e.g. send email, activate ads, edit company/*>
Evidence bar: <what must be true before it recommends something>
Done means: every source checked; failures listed by name; output saved to <node>
Escalates via: create_ticket (manual) when <condition>
Eval set: brain/contracts/<agent>/evals — 10 example inputs with expected outputs
```

## Mode: week (the Monday loop)

1. Read the latest `brain/memos/performance/*` (run `/performance-memo` if none exists for this week).
2. Read the open queue. **Cloud:** `list_tickets` has no title search and returns at most 100
   results without paging, so call it with `execution_target: "manual"` and the open statuses
   (`new`, `assigned`, `doing`, `review`) and `limit: 100` (the default is 20), then keep titles starting with `[ME:` client-side. If
   100 come back, say the queue may be truncated. **Solo:** `list_findings`, filtered the same way.
   Group them into **Approve**, **Decide** and **FYI**. (`analysis` means shipped and being
   measured; list those under FYI, not as done.)
3. For each memo line, ask the user for the call: **keep / kill / change / test**. Record it in
   `brain/experiments/log` as: date, campaign ID, decision, reason, next test.
4. For every rejection the user makes, ask why and write the answer where the next run sees it
   (customer-fit, offers, voice, failed-campaigns or agent-corrections). Propose `company/`
   and `brand/` edits and apply them only after a yes.
5. Print the week's plan, following Greg's rhythm: Mon decide, Tue–Wed build and launch, Thu sit in on sales
   and support calls, Fri review agent output and update the brain.

If the user spends most of the session fixing agent output, say so: the problem is
upstream, in the brain or the contract.

## Mode: campaign <idea>

The end-to-end run. The customer's words have to survive every step.

1. **Evidence.** Read `brain/evidence/customer-language/latest`. Find the quote cluster
   behind the idea and say **who** said it: customers, prospects, community members, or people
   replying to ads (ad repliers aren't customers). If fewer than ~3 independent customers or
   prospects said it, say so and ask whether to proceed.
2. **Offer check (a gate).** Read `brain/company/offers`. If the idea needs a new offer or claim,
   draft it and open "[ME:marketing-engineer] Approve offer: <claim> for <idea>". The human walks it
   over to whoever delivers the service and confirms the company can actually deliver it.
   **Don't fan out until the offer is approved** (in this session, or the ticket is approved). Until
   then, only `/search-demand page` and `/social-engine hooks` may draft, labelled "pending offer".
3. **ID.** `/campaign-ledger new "<name>"` → allocates e.g. `BK014` and creates `brain/campaigns/BK014`
   holding the verbatim quotes, the approved offer, the audience and the evidence bar (spend, days, win metric).
4. **Fan out.** Each agent writes its own section of `brain/campaigns/<ID>` (the canonical template
   is in `/campaign-ledger`), or one line, "skipped: <reason>", when it can't run:
   - `/creative-engine <ID>` → 3+ distinct angles, created **paused**
   - `/search-demand page <ID>` → one page brief or decision tool (calculator, checker)
   - `/closed-lost-revival match <ID>` → old prospects whose reopen condition this campaign meets
   - `/buying-triggers <ID>` → accounts with a fresh trigger that fits this angle
   - `/social-engine hooks <ID>` → organic hooks to test before paying for them
5. **Review in one sitting.** The agents file their own tickets. Add one index ticket,
   "[ME:marketing-engineer] Review bundle: <ID>", that links them in approval order (offer → creative
   → page → hooks → outreach), lists skipped agents, and states what's still missing (budget,
   screenshots, evidence bar). Cut anything that promises what `offers` doesn't allow.
6. **After launch.** `/ad-kill-rules` enforces the evidence bar and `/performance-memo` reports
   back with the ID joined from spend → calls → deals → revenue. Remind the user when the sample is still small.

## Mode: status

For each agent, read its latest output node and report its age, its last run's `Failures:`
line, and whether a contract and eval set exist. Output nodes:

| Agent | Latest output |
|-------|---------------|
| customer-language | `brain/evidence/customer-language/latest` |
| campaign-ledger | `brain/campaigns/ledger` |
| buying-triggers | newest `brain/evidence/triggers/*` |
| search-demand | `brain/evidence/search/latest` |
| creative-engine | newest `## Assets` section in `brain/campaigns/*` |
| ad-kill-rules | `## Kill log` sections in `brain/campaigns/*`, plus its script runs (`list_scripts`) |
| closed-lost-revival | `brain/evidence/closed-lost/ledger` |
| social-engine | newest `brain/evidence/social/*` |
| performance-memo | newest `brain/memos/performance/*` | Flag anything older than 2× its cadence as stale.
Also `list_automations` / `list_scripts` to show what actually runs unattended. **Flag any
existing automation whose write grants have no `constraints`** (e.g. a post or send tool that
can target anything) and any script paused after failures.

## Mode: schedule

Only for agents the user says are reliable.

`create_automation`, `update_automation` and `run_automation` are writes, so they are not in this
skill's allowed-tools: Claude Code asks before each call. Show the user the exact automation
(instructions, grants, constraints) and get a yes first.

**On Solo** there are no automations or scripts: schedule the skill itself with Claude Code's
`/schedule` (cloud routine) or `/loop` (in-session), using the same read-only discipline, and
let the skill file findings rather than act. Everything below is **Cloud**, and needs the
workspace's automations/scripts flag. For each one:

1. Confirm with the user the exact write tools and targets to grant.
2. `create_automation` with `enabled: false`, the agent's steps as `instructions`, and
   the minimum `action_grants` (with `constraints`). Read tools are inferred from granted servers;
   pass `read_tools` explicitly for agents that only read from other servers.
3. Test with `run_automation` (`dry_run: true`), inspect with `get_automation_run`, and only then enable.

Suggested grants:

| Agent | Grants |
|-------|--------|
| customer-language, search-demand, performance-memo, closed-lost-revival | none (read-only; output is context nodes + tickets) |
| ad-kill-rules | `Meta Ads/tool_update_ad_status` pinned `{"status":"PAUSED"}`; equivalent pause-only grants on TikTok, LinkedIn, Google, Bing, Reddit, Snapchat (`tool_update_ad_status`) and ChatGPT ads (`OpenAI Ads/tool_update_ad_status` pinned `{"status":"paused"}`) |
| social-engine | none. Scheduling posts stays manual. |
| buying-triggers | none (drafts land in tickets) |

Prefer deterministic `create_script` for `/ad-kill-rules` and the ledger sync, because those rules are exact.

## Critical rules

1. **Brain before agents.** Thin context produces generic slop. Fix the brain first.
2. **One agent at a time.** Each one has to earn trust before the next gets built.
3. **Humans own `company/` and `brand/`.** Agents propose; humans promote.
4. **Every campaign has an ID**, and it appears in every name.
5. **Every review item takes under a minute** and shows the change, what it touches and the evidence.
6. **Report failures by name.** Silent skips are the worst bug.

## Tool names and providers

Every tool, prefix and provider alternative is listed in
[`references/mcp-routing.md`](references/mcp-routing.md): naming (`mcp__cogny__mcp__<Prefix>__<tool>`),
what Solo vs Cloud can call, how to choose between connected providers, and "same job, different
provider" tables. If a tool you expect is missing, call `refresh_mcp_discovery`.
