---
name: buying-triggers
description: Find accounts where something just happened that creates demand — funding, hiring, new locations, launches, rising ad engagement — skip anyone already in your pipeline, and draft outreach only when "this event creates this problem, and we solve it this way" comes out sharp
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [fibbler, hubspot, pipedrive, upsales, brave-search, cogny]
user-invocable: true
argument-hint: "[<campaign-ID>] [--channel linkedin|google|meta] [--limit 25]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__search_context
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__mcp__app-fibbler-co__get_account_overview
  - mcp__cogny__mcp__app-fibbler-co__get_warm_accounts
  - mcp__cogny__mcp__app-fibbler-co__get_company_engagement
  - mcp__cogny__mcp__app-fibbler-co__get_customer_journey
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__Pipedrive__list_users
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__get_deal
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Pipedrive__list_persons
  - mcp__cogny__mcp__Pipedrive__list_stages
  - mcp__cogny__mcp__Upsales__list_users
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_opportunities
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__list_contacts
  - mcp__cogny__mcp__Upsales__list_activities
  - mcp__cogny__mcp__Upsales__list_appointments
  - mcp__cogny__mcp__Upsales__list_visits
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_news
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - WebFetch
---

# Buying Triggers

Some moments create demand overnight: a company opens a second location, starts selling
wholesale, raises a round and posts five sales jobs, or launches on a new marketplace.
This agent watches for those moments in accounts that fit you. It reaches out only when it
can finish one sentence sharply:

> **"This event creates this problem, and our product solves it in this specific way."**

If the sentence comes out mushy, the account waits. That filter is what makes outreach
read as good timing instead of spam.

**Requires:** Cogny ($9/mo) with app-fibbler-co and/or a CRM (HubSpot, Pipedrive or Upsales;
Salesforce and others: see the CRM layer in `/marketing-engineer`). Brave
Search is included in Cogny.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Buying Triggers needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect app-fibbler-co and/or a CRM (HubSpot, Pipedrive or Upsales).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Prerequisites

1. Call `list_integrations` and note which pool sources are connected: app-fibbler-co, HubSpot,
   Pipedrive, Upsales.
2. `health_status` misses revoked tokens, so make **one cheap read** per source: fibbler
   `get_account_overview`, HubSpot `get_user_details`, Pipedrive `list_users`, Upsales
   `list_users(limit: 1)`. A 401, Forbidden, "unauthorized" or "lacks scope" means 🔴
   "reconnect <integration> in Cogny": drop that source for this run and **don't retry** it.
3. Brave Search is Cogny-native and doesn't appear in `list_integrations`; treat it as available if
   its tools load. If it's missing, accounts can't be checked for triggers: say so in `Failures:`.
4. If a tool is missing, call `refresh_mcp_discovery` once. New tools only load after the client
   reconnects, so drop that source for this run and mark it ⚠ "needs reconnect".
5. **No usable pool source** (no healthy fibbler and no healthy CRM): write
   `brain/evidence/triggers/<date>` with `Pool: 0` and the Failures, write
   `## Trigger accounts — skipped: <reason>` in the campaign folder if an ID was given, print this, and stop.

   ```
   Buying triggers needs accounts to watch. In Cogny, connect (or reconnect) at least one of:
     • app-fibbler-co — companies engaging with your ads
     • a CRM: HubSpot, Pipedrive or Upsales — your target accounts
   Then run /buying-triggers again.
   ```

## Usage

- `/buying-triggers` — this week's shortlist
- `/buying-triggers BK014` — only triggers that fit campaign BK014's angle
- `/buying-triggers --channel google` — warm accounts from Google Ads site visits

Schedule: Tuesday and Thursday mornings.

## Steps

### 1. Load the brain

Read `brain/company/customer-fit`, `brain/company/offers`, `brain/brand/voice`,
`brain/decisions/agent-corrections`, and the campaign folder if an ID was given. Build
the **trigger list** for this business from customer-fit and from the "Triggers mentioned"
section of `brain/evidence/customer-language/latest`. Default triggers to check:

| Trigger | Why it creates demand | How to detect |
|---------|----------------------|---------------|
| Funding round | New budget, growth targets, hiring | Brave News `"<company>"` (name only), freshness `pm`; classify the hits |
| Hiring spree in a relevant function | The work you automate is being staffed | Brave Search `site:<careers domain> OR "<company>" hiring <role>` |
| New location / market / marketplace | Ops and reporting get messier | Same Brave News results; company site pages |
| Leadership change in the buyer role | New owner, new tools in the first 90 days | Same Brave News results |
| Integration partner ships something | A new capability changes the buyer's workflow | Partner changelog (WebFetch) |
| Engagement spike with our ads | They're already paying attention | fibbler `get_warm_accounts` (`isNew`, `trendPct`) |

### 2. Build the candidate pool

- **fibbler `get_warm_accounts`** (`time_period: "30d"`, each channel, `limit: 25`). The
  30d → 60d → 90d ladder is **only for 0 rows**: if a channel returns 0 rows, retry with `60d`, then
  `90d`. An auth error, Forbidden or "unauthorized" is not an empty result: mark the channel 🔴
  "reconnect fibbler in Cogny" and don't retry it at any window. If it refuses with "add-on is not
  enabled", mark that channel ⚪ and continue. These are companies heating up on your ads that are *not yet deals* in the CRM.
  Treat warmth as a correlation signal and never call it intent. Discount rows where engagements
  equal impressions on a tiny count (e.g. 8/8), which looks like one person or a bot, not an account.
- **HubSpot target accounts**: `search_crm_objects` on `companies` that match customer-fit
  (`industry`, `numberofemployees`, `annualrevenue`, `country`), or with `hs_ideal_customer_profile`
  tier 1–2 if the portal uses ICP tiers, or `hs_is_target_account = true`. Exclude
  `lifecyclestage = customer`. Sanity-check that each company is plausibly a buyer; firmographic
  filters alone let odd fits through.

- **Pipedrive**: `list_organizations` (cursor-paginated). Keep organizations with no open or won deal
  (`list_deals(org_id, status: "open")` / `"won"`) that match customer-fit. Organization custom fields come
  back as hashed keys, so ask the user once which keys hold size and industry, and store that in `brain/contracts/crm-layer`.
- **Upsales**: `list_accounts` filtered on customer-fit fields; `list_visits` adds accounts that visited the
  site in the last 14 days, a first-party warmth signal fibbler can't see. Exclude accounts with won orders.

Pass the CRM to fibbler (`crm: "hubspot"` or `"pipedrive"`) so its own exclusion uses the right CRM;
for Upsales fibbler can't exclude CRM deals, so step 3 is the only filter.

If the pool is **0** after this step (fibbler and the CRM returned nothing usable), stop: write
the shortlist node with `Pool: 0` and the failures, print the setup steps from Prerequisites, and
don't run Brave.

Dedupe by **company domain** (HubSpot `domain`; fibbler rows carry a domain or name). Fall back to
normalized company name (lowercase, strip AB/Aktiebolag/Inc/Ltd/GmbH) only when there's no domain.

### 3. Remove anyone the team is already talking to

For each candidate company in HubSpot (match by domain):
- Drop it if it has an **open deal**: `search_crm_objects` on `deals` with `hs_is_closed = false` and
  `associations.company = <companyId>`. fibbler already excludes CRM deals for its own rows when
  `crm: "hubspot"` is passed. Check anyway for companies from other sources.
- Drop it if anyone there was touched in the last 14 days (`notes_last_contacted`,
  `hs_last_sales_activity_timestamp` on the company or its contacts).
- For the contact you'd write to, drop them if `hs_email_optout = true`, `hs_lead_status` is
  unqualified / do-not-contact, or they've unsubscribed from sales email.

**Pipedrive:** open deal = `list_deals(org_id, status: "open")`; last touch = newest
`list_activities(org_id)`; opt-out = person `marketing_status` when present.
**Upsales:** open deal = `list_opportunities(filters: client.id)`; last touch = newest
`list_activities` / `list_appointments` for `client.id`; opt-out = the contact's unsubscribe fields
(find them with `get_metadata`).

Companies not in the CRM at all (fibbler-only) can't get the opt-out check, so their drafts go on **HOLD**.
**Respecting opt-outs is a hard rule, not a judgment call.**

### 4. Check each account for fresh triggers

Cap at 40 accounts per run. For each, run **one** Brave News query on the company name alone
(`"<company>"`, freshness `pm`). Keep a hit only if the name appears in the title or description
**and** it matches the company's country, domain or industry, because name collisions are common
(an ETF ticker, a vet chain with the same name). Then classify the kept hits into the trigger types.
A **roundup or listicle** that merely mentions the company ("10 startups to watch", "best tools for
X", a funding digest naming many companies) is **not an event** about that company: drop it unless
the item itself reports a dated event for this company, and then cite the primary source.
For hiring, check the careers page when it can be found. Don't put the trigger words in the query
(`"X" raises OR funding`), because that returns generic funding news about other companies.
Record each trigger as: what, date, source URL. Only events from the **last 30 days** count.
If Brave returns an error or rate-limits, record which accounts weren't checked.

### 5. Write the one sentence

For every account with a fresh trigger, write:

`<Event> creates <specific problem>, and <product> solves it by <specific mechanism>.`

Score it as **sharp** or **mushy**:
- Sharp: names a concrete problem the customer-language report has heard, and a mechanism
  from offers. ("Launching on Amazon means three payout schedules and fee structures to reconcile; our monthly close
  reconciles all channels into one profit number.")
- Mushy: generic ("Growth creates challenges, and we help companies grow"). **These accounts wait.**

### 6. Draft outreach for sharp accounts only

A short email (if the contact has an `email` in HubSpot) or LinkedIn note that **leads with the event**, uses the customer's own words
from the language report, matches `brand/voice`, and makes one ask. ≤90 words. No claims
outside `offers`.

Drafts are not sent. Bundle them into **one** review item per run (`create_ticket` on Cloud, else `create_finding`):
- title: "[ME:buying-triggers] Approve: N trigger-based outreach drafts (week of …)"
- body: for each account, the trigger with its source link, the sentence, the draft, and the contact if known
- `execution_target: "manual"`

### 7. Save the shortlist

`write_context_node` at `brain/evidence/triggers/<YYYY-MM-DD>`:

```markdown
# Buying triggers — YYYY-MM-DD
Pool: N (fibbler warm: A · HubSpot target accounts: B) · removed (open deal / recent contact / opt-out): R
Checked: C · not checked (source failures): <list>
Failures: <🔴 reconnect / ⚠ needs reconnect / errors by source, or "none">

## Sharp (drafted)
| Company | Trigger (date, source) | Sentence | Warmth |
## Waiting (trigger found, sentence mushy)
| Company | Trigger | Why it's mushy |
## No fresh trigger
<count>
```

If a campaign ID was given, also append the sharp list under `## Trigger accounts` in
`brain/campaigns/<ID>` (or one line, "skipped: <reason>", when nothing qualified).

## Recording findings

Detect the plan from the tools that exist: use `create_ticket` first when it exists (Cloud), and
`create_finding` only when it doesn't (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **No sharp sentence, no outreach.**
2. **Never contact anyone with an open deal, recent contact, or an opt-out.**
3. **Drafts only.** Nothing is sent from this skill.
4. **Every trigger has a date and a source link.** No link means no trigger.
5. **Warmth is correlation.** Never write "they're looking to buy" from ad engagement alone.
