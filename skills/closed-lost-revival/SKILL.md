---
name: closed-lost-revival
description: Re-read every lost deal in your CRM (HubSpot, Pipedrive or Upsales; Salesforce via the CRM layer) with its calls, meetings and notes, replace "not interested" with the real reason plus a reopen condition, then watch for those conditions — a shipped feature, a renewal date, a champion moving, the account coming back to your site — and draft a personal note that quotes the original conversation
version: "1.2.3"
author: Cogny AI
requires: cogny-mcp
platforms: [hubspot, pipedrive, upsales, fibbler, stripe, brave-search, cogny]
user-invocable: true
argument-hint: "[build|watch|match <campaign-ID>|shipped \"<feature>\"]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__search_context
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__HubSpot__search_owners
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
  - mcp__cogny__mcp__app-fibbler-co__get_account_overview
  - mcp__cogny__mcp__app-fibbler-co__get_influenced_deals
  - mcp__cogny__mcp__app-fibbler-co__get_warm_accounts
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_news
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - mcp__cogny__mcp__Stripe__get_stripe_account_info
  - mcp__cogny__mcp__Stripe__stripe_api_details
  - mcp__cogny__mcp__Stripe__stripe_api_read
  - WebFetch
  - Bash
---

# Closed-Lost Revival

This is the agent that pays for all the others. "Not interested" is a lazy summary of a real
conversation. Re-read each lost deal, record the **actual reason** and a **reopen
condition**, and then watch for the condition:

- "Needed SSO" → the day the changelog says SSO shipped, they get a personal note quoting their call.
- "Went with a competitor, contract renews in March" → show up in January.
- "Champion left the company" → congratulate them at the new company and reintroduce yourself.

Most companies have a pile of unfinished revenue sitting in their own CRM.

**Requires:** Cogny ($9/mo) with a CRM connected: HubSpot, Pipedrive or Upsales (Salesforce and
others: see the CRM layer in `/marketing-engineer`). The steps below are written for HubSpot.
"Pipedrive and Upsales" says what changes for those CRMs. Fibbler is optional and adds
ad-engagement signals.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Closed-Lost Revival needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect a CRM: HubSpot, Pipedrive or Upsales (Stripe and fibbler optional).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Prerequisites

1. Call `list_integrations`. This skill needs a CRM: **HubSpot, Pipedrive or Upsales**.
2. Make one cheap read on the CRM: HubSpot `get_user_details`, Pipedrive `list_users`, Upsales
   `list_users(limit: 1)`. If fibbler is connected, `get_account_overview`. A 401, Forbidden or
   "lacks scope" means 🔴 "reconnect <integration> in Cogny"; don't retry it. A broken fibbler only
   drops the ad-engagement signals; a broken CRM stops the run.
3. If a CRM tool is missing, call `refresh_mcp_discovery` once. New tools only appear after the
   client reconnects, so tell the user to reconnect the Cogny MCP and stop this run.
4. **No CRM connected:** print this and stop. Don't fall back to `runcloser` (not supported).

   ```
   Closed-lost revival needs a CRM. Connect HubSpot, Pipedrive or Upsales in Cogny
   (Integrations → Connect), then run /closed-lost-revival build again.
   ```

   **Optional partial ledger from Stripe.** If Stripe is connected, offer (don't run unasked) a
   "lost customers" ledger instead: `stripe_api_read` `GetSubscriptions` with `status: "canceled"`,
   paged with `starting_after` and aggregated with `jq` (pages are large), reading `canceled_at`,
   `cancellation_details` (`reason`, `feedback`, `comment`) and the plan price. Skip trial-only
   cancellations (`ended_at == trial_end`). Write it to `brain/evidence/closed-lost/ledger` headed
   "Partial: Stripe cancellations only, no CRM", with `comment` as the only `[verbatim]` evidence.
   These are churned customers, not lost deals, so there is no conversation to re-read and no draft notes.

## Usage

- `/closed-lost-revival build` — first pass over lost deals (last 18 months), creates the ledger
- `/closed-lost-revival watch` — weekly: check every open reopen condition
- `/closed-lost-revival shipped "SSO"` — a feature just shipped, so find everyone who asked for it
- `/closed-lost-revival match BK014` — lost prospects that campaign BK014's offer answers

## Steps — build

### 1. Pull lost deals

`get_user_details` to confirm read access. `get_properties(deals, ["dealstage","closed_lost_reason","pipeline"])`
to learn the pipelines and which stages are closed-lost, plus the options on `closed_lost_reason`
(it's often free text, sometimes a dropdown).

`search_crm_objects` on `deals`, filters `hs_is_closed = true` AND `hs_is_closed_won = false`
AND `closedate` ≥ 18 months ago. Properties: `dealname, amount, deal_currency_code, closedate,
closed_lost_reason, dealstage, pipeline, hubspot_owner_id, hs_analytics_source,
hs_analytics_source_data_1, hs_analytics_source_data_2, notes_last_contacted`. Page with `after` until done.

**Exclude** non-losses: reasons or names saying duplicate, test, merged, created in error, or
"moved to another pipeline". Report excluded counts by reason. If more than half the rows are
noise, file one ticket ("[ME:closed-lost-revival] Clean CRM: N of M lost deals are noise") and continue with the rest.

Amounts: use `deal_currency_code`. Never add amounts in different currencies together.

### 2. Re-read each deal

Cap at 50 deals per run, newest and largest first. For each deal:
- Associated **contacts** and **company** (`get_crm_objects` with associations): name, `jobtitle`,
  company `domain`, `industry`, `numberofemployees`.
- The conversation: `search_crm_objects` on `calls`, `meetings` and `notes` filtered by
  `associations.deal = <dealId>` (and by the main contact if the deal has none). Read
  `hs_call_body`, `hs_meeting_body`, `hs_internal_meeting_notes`, `hs_note_body`, and any transcript
  property (see `/customer-language`).
- If fibbler is connected, `get_influenced_deals` (`deal_filter: "lost"`, `crm: "hubspot"`) shows which campaigns touched the deal.

`closed_lost_reason` is the rep's one-liner, written at close. The notes are where the real
reason usually is. When they disagree, trust the notes and record both.

### 3. Record the real reason and a reopen condition

| Reason | Reopen condition type | Example condition |
|--------|----------------------|-------------------|
| Missing feature | `feature_shipped` | "SSO ships" |
| Timing / budget cycle | `date` | "after year-end close, 2027-01-15" |
| Chose competitor | `date` (renewal) + `signal` | "contract renews 2027-03; watch for competitor complaints" |
| Champion left / no champion | `person_moved` | "the champion lands somewhere new" |
| Price | `offer_change` | "a lower tier or annual discount exists" |
| Too small / bad fit | `none` — and add to customer-fit evidence | — |
| Unknown | `none` — flag the notes as too thin to judge | — |

Keep the **evidence**: the note or quote it came from, with object type, id and date, labelled
`[verbatim]` or `[paraphrase]`. Never invent a reason. If the record is too thin, say "unknown — notes too thin".

### 4. Write the ledger

`write_context_node` at `brain/evidence/closed-lost/ledger`:

```markdown
# Closed-lost ledger — built YYYY-MM-DD
Lost deals (18 mo): N · real losses: R · excluded as noise: X · re-read: C (capped at 50)
| Deal (id) | Company | Lost | Amount (ccy) | CRM reason | Real reason | Evidence (object, id, date) | Reopen condition | Type | Watch until | Status |

Failures: <none, or what couldn't be read>
```

Also add `brain/evidence/closed-lost/patterns`: reasons ranked by count and by lost amount (per
currency), plus the **gap between the CRM reason and the real reason**, which is a coaching
finding in itself. If "too small" or "bad fit" leads the list, file a ticket proposing a
customer-fit update. Don't make the edit yourself.

Optional: propose (as a ticket for a HubSpot admin) two custom deal properties, `reopen_condition`
and `reopen_date`, so the team sees the conditions in the CRM. This skill never writes to the CRM.

### Pipedrive and Upsales

| Step | Pipedrive (`Pipedrive`) | Upsales (`Upsales`) |
|------|-------------------------|---------------------|
| Lost deals | `list_deals(status: "lost", updated_since: <18 months ago>)`, cursor-paginated; `get_deal` for `lost_reason`, `lost_time`, `value`, `currency`, `org_id`, `person_id` | `list_orders(filters=[{"field":"probability","comparator":"eq","value":0}], sort: "-date")`; the loss-reason custom field comes from `get_metadata` |
| Company / people | `list_organizations`, `list_persons(org_id)` | `client.id` → `list_accounts`, `list_contacts(filters: client.id)` |
| The conversation | `list_activities(deal_id)`: `subject`, `note` | `list_activities` and `list_appointments` filtered by `client.id`: `notes`, `description` |
| Open deal now? | `list_deals(status: "open", org_id)` | `list_opportunities(filters: client.id)` |
| Last touch | newest `list_activities(org_id, done: true)` | newest `list_activities` / `list_appointments` for `client.id` |
| Re-engagement | fibbler `get_warm_accounts` with `crm: "pipedrive"` | `list_visits` for `client.id` (Upsales web tracking) |
| Opt-out | person `marketing_status` when present; otherwise HOLD | contact unsubscribe/active fields from `get_metadata`; otherwise HOLD |

Fibbler's `get_influenced_deals` takes `crm: "hubspot" | "salesforce" | "copper" | "attio"`, with **no
Pipedrive or Upsales**, so skip it there. Only `get_warm_accounts` accepts `crm: "pipedrive"`. For Upsales, skip fibbler.

## Steps — watch (weekly)

For each `open` row:
- `date`: is it within 45 days? → due
- `feature_shipped`: read `brain/evidence/changelog` (or WebFetch the changelog URL in START-HERE)
- `person_moved`: `brave_search` for the person's name with their new title or company. Require a
  second identifier (old company, city, photo-free profile text) to match, because names collide.
- `offer_change`: compare against `brain/company/offers`
- **Re-engagement (any row):** re-read the company and contacts and look for
  `hs_analytics_last_visit_timestamp` in the last 14 days, a new `recent_conversion_date` (form
  fill), or `hs_email_last_open_date`/`hs_email_last_click_date`. If fibbler is connected,
  `get_warm_accounts` too. Any of these bumps the priority.

Before drafting, **re-check the CRM** (HubSpot fields below; Pipedrive/Upsales equivalents in the table above) and skip the row if:
- the company has an **open deal** now (`hs_is_closed = false`), or has become a customer
  (`lifecyclestage = customer`, or a won deal under any name)
- a contact was touched in the last 14 days (`notes_last_contacted`, `hs_last_sales_activity_timestamp`)
- the contact has opted out: `hs_email_optout = true`, a "do not contact" `hs_lead_status`, or
  unsubscribed from sales email

Respecting opt-outs and contact preferences isn't optional.

## Steps — shipped "<feature>"

`search_context` and the ledger for rows whose reason or evidence mentions the feature
(and its synonyms). Each match is due now.

## Drafting the note

For every due row, write a short personal note (≤100 words) that:
1. References their original words: "Back in March you said the deal-breaker was SSO for your IT team."
   Only quote `[verbatim]` evidence as their words; paraphrase anything else.
2. States what changed, specifically.
3. Makes one low-friction ask.

Use `brain/brand/voice`. No claims outside `offers`. For `person_moved`, congratulate them
first and lead with no pitch. Address it from the original deal owner (`search_owners`).

Bundle all drafts into **one** `create_ticket` ("[ME:closed-lost-revival] Approve: N closed-lost
revival notes"), each with the deal link, the condition met, the evidence and the draft. Mark the rows
`drafted` in the ledger. After the user sends, the next run sees the new engagement in HubSpot
and marks the row `sent`.

## Steps — match <ID>

Read `brain/campaigns/<ID>`. Select ledger rows whose real reason the campaign's offer answers
(e.g. "maybe after year-end" for a year-end campaign). Draft as above and append the list to the
campaign folder under `## Closed-lost matches`. If there's no CRM or no ledger, write one line
there instead: "skipped: <reason>".

## Recording findings

Detect the plan from the tools that exist: use `create_ticket` first when it exists (Cloud), and
`create_finding` only when it doesn't (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Never invent a reason.** "Unknown" is a valid answer.
2. **Quote only verbatim evidence** as the prospect's words, with object id and date.
3. **Drafts only. Respect opt-outs. Skip open deals and customers.**
4. **Read-only on the CRM.** Proposed CRM fields go to a human as a ticket.
5. **Exclude CRM noise** and report how much there was.
