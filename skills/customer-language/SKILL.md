---
name: customer-language
description: Mine your CRM's call notes, meeting notes, support tickets and lost-deal reasons (HubSpot, Pipedrive or Upsales), support chats (Crisp), community threads (Discord) and YouTube comments for the exact words customers use to describe their problems — clustered, counted by distinct company (CRM) or distinct person (community), with labelled quotes — and write a weekly customer-language report every other marketing agent builds from
version: "1.2.3"
author: Cogny AI
requires: cogny-mcp
platforms: [hubspot, pipedrive, upsales, crisp, discord, youtube, x-organic, cogny]
user-invocable: true
argument-hint: "[days=7|30|all] [--segment <industry or tier>] [--source crm|support|community|youtube|files]"
allowed-tools:
  - Bash
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__HubSpot__search_properties
  - mcp__cogny__mcp__Pipedrive__list_users
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__get_deal
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Upsales__list_users
  - mcp__cogny__mcp__Upsales__list_activities
  - mcp__cogny__mcp__Upsales__list_appointments
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_accounts
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__mcp__Crisp__list_conversations
  - mcp__cogny__mcp__Crisp__get_conversation_messages
  - mcp__cogny__mcp__Discord__get_current_user
  - mcp__cogny__mcp__Discord__list_guilds
  - mcp__cogny__mcp__Discord__get_guild
  - mcp__cogny__mcp__Discord__list_guild_channels
  - mcp__cogny__mcp__Discord__get_channel
  - mcp__cogny__mcp__Discord__list_guild_members
  - mcp__cogny__mcp__Discord__get_channel_messages
  - mcp__cogny__mcp__YouTube__get_channel
  - mcp__cogny__mcp__YouTube__list_channel_videos
  - mcp__cogny__mcp__YouTube__list_comment_threads
  - mcp__cogny__mcp__X_Organic__tool_get_me
  - mcp__cogny__mcp__X_Organic__tool_get_mentions
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__search_context
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - Read
  - Glob
  - Write
  - Edit
---

# Customer Language

The first agent to build, because every other agent builds from what it finds. Its
job is to pull out the **exact words** customers use for their problems. People buy the
situation, not the feature. "I'm tired of taking calls during dinner" beats "automated scheduling" every time.

**Requires:** Cogny ($9/mo) with at least one source connected:

| Source | Integration | What it gives |
|--------|-------------|---------------|
| CRM calls, meetings, notes | HubSpot, Pipedrive or Upsales | Pre-purchase pain, objections, triggers (rep paraphrase) |
| Support chats | Crisp | Post-purchase pain **in the customer's own typed words** |
| Community | Discord | Questions and complaints in their own words |
| Video comments | YouTube | What viewers ask and push back on |
| Mentions | X Organic | Public complaints and questions aimed at the brand |
| Transcripts | local files | The best quotes; export 20–50 calls from Gong, the Fathom call recorder, or Zoom into `./brain/evidence/calls/*.txt|md` |

The `Fathom_Analytics` integration in Cogny is Fathom **web analytics**, not the Fathom call
recorder, so transcripts still come from local exports or a HubSpot transcript property.
Use every source that's connected and report them separately, then cluster across them.
Never use `runcloser` as a source, even when it's connected.

**No CRM connected?** Fall back in this order and say which CRM would have added pre-purchase
pain: Crisp (support, verbatim) → Discord (community, verbatim) → YouTube comments → X mentions →
local transcripts in `./brain/evidence/calls/`. If Cogny is connected but none of these is available, print "Connect a CRM
(HubSpot, Pipedrive or Upsales), Crisp or Discord in Cogny, or export call transcripts to
`./brain/evidence/calls/`", and stop without writing a report.

**No Cogny at all** (no `mcp__cogny__*` tools: no `list_integrations`, no `cogny_status`): print this.
If `./brain/evidence/calls/` has transcripts (Glob `./brain/evidence/calls/*.{txt,md}`), continue in
local mode (below); otherwise stop without writing a report.

```
Customer Language needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect a CRM (HubSpot, Pipedrive or Upsales), Crisp, Discord, YouTube or X Organic.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: run it on call transcripts exported to ./brain/evidence/calls/*.txt|md
(local mode; the report is written under ./brain/).
```

## Local mode (transcripts only, no Cogny)

The brain is plain files at `./brain/<node path>.md` (same paths as the context tree, see `/marketing-brain`).
- **Transcript header.** Each file should start with:
  ```
  Company: <name>
  Kind: sales|onboarding|support|vendor|partner|internal
  Date: YYYY-MM-DD
  ```
  If a field is missing, infer it from the content (date from the filename or the text, else the file's
  modified time) and label it `(inferred)` in the report's source list. Exclude vendor, partner and internal
  as usual; count distinct `Company:` values.
- **Window.** `days=7|30` filters on the header `Date` (inferred dates included, labelled); `all` takes every file.
- **Context (step 1):** Read `./brain/START-HERE.md`, `./brain/company/customer-fit.md`,
  `./brain/decisions/agent-corrections.md` and `./brain/evidence/customer-language/latest.md` if they exist.
- **Report (step 6):** Write `./brain/evidence/customer-language/<YYYY-MM-DD>.md` and overwrite
  `./brain/evidence/customer-language/latest.md` with the same content. Sources line: `files F`.
- **Mismatches (step 7):** append each review item to `./brain/evidence/review-queue.md` (create it if
  missing) as `- [ ] YYYY-MM-DD [ME:customer-language] Review: customers keep saying X — offers says Y`
  followed by the quotes, instead of a ticket.
- **Corrections (step 8):** append to `./brain/decisions/agent-corrections.md`.
- Skip the CRM, Crisp, Discord, YouTube and X steps and the health checks.

## Usage

- `/customer-language` — last 7 days (the weekly run)
- `/customer-language all` — the last 200 engagements (first build / baseline)
- `/customer-language 30 --segment "ecommerce"` — one industry or ICP tier

Schedule: Monday 07:00, before `/performance-memo`.

## Where customer words live in HubSpot

| Source | Object | Text properties | Good for |
|--------|--------|-----------------|----------|
| Sales calls | `calls` | `hs_call_body` (notes), `hs_call_title`, `hs_call_duration`, `hs_call_status`, `hs_call_disposition`, `hs_timestamp` | Pain, objections, triggers |
| Meetings | `meetings` | `hs_meeting_body`, `hs_internal_meeting_notes`, `hs_meeting_title`, `hs_meeting_outcome`, `hs_meeting_start_time` | Discovery and demo notes |
| Notes | `notes` | `hs_note_body`, `hs_timestamp` | Rep write-ups after calls |
| Support | `tickets` | `subject`, `content`, `hs_pipeline_stage`, `createdate` | Post-purchase pain, refund drivers |
| Lost deals | `deals` | `closed_lost_reason`, `closed_won_reason`, `dealname` | Objections in the rep's words |

Before the first run, call `search_properties` on `calls` and `meetings` with keywords
`["transcript","summary","recording"]`. If the portal stores a transcript or AI-summary
property (Conversation Intelligence, or a Gong/Fathom sync), **use it first**, because it holds
the customer's own words. Rep notes are paraphrases.

## Other sources

**Pipedrive** (`Pipedrive`): `list_activities` (`updated_since`, `done: true`; cursor-paginated)
gives calls and meetings with `subject` and `note`; tie them to companies with `org_id`
(`list_organizations`) and to deals with `deal_id`. Lost reasons are on `get_deal` (`lost_reason`)
for deals from `list_deals(status: "lost")`.

**Upsales** (`Upsales`): `list_activities` (calls, to-dos) and `list_appointments` (meetings)
with `notes` / `description`, filtered by date via
`filters=[{"field": "date", "comparator": "gte", "value": "<YYYY-MM-DD>"}]`. Companies are
`client.id` → `list_accounts`. Lost orders are `list_orders` with `probability = 0`, and the reason
field is a custom field (find it once with `get_metadata`). Keep `limit` ≤ 100, because responses are large.

**Crisp** (`Crisp`): needs the `website_id`. Ask once and store it in `brain/contracts/crm-layer`.
`list_conversations(website_id, page_number)` (newest first), then
`get_conversation_messages(website_id, session_id)` and keep messages whose `from` is `user`. These are
**verbatim** customer words. Count distinct people (`session_id` → profile email domain → company).

**Discord** (`Discord`): `list_guilds` → `list_guild_channels` → `get_channel_messages` on public
support, feedback and general channels. Verbatim; count distinct authors, not messages.
- **Skip private channels.** A channel is private when its `permission_overwrites` (or its parent
  category's) has an entry with `id == guild_id` that denies `VIEW_CHANNEL` (bit 1024). Never quote
  them; at most use them as anonymised themes.
- **Exclude bots and staff.** Drop messages where `author.bot` is true, plus staff ids: the bot
  itself (`get_current_user`), the guild `owner_id` (`get_guild`), and members holding admin or
  moderator roles (`list_guild_members`; store the staff role ids in `brain/contracts/crm-layer`).
- **Page by snowflake.** `get_channel_messages` has no date filter. Call it with `limit: 50` (each
  message carries the full author object) and page backwards with `before` = the oldest message id
  until messages fall outside the window.
- A `Forbidden` on one channel means the bot can't read it: list it as "not readable" and continue.

**X** (`X_Organic`): `tool_get_mentions(start_time: <window start>, max_results: 100)`, paging with
`pagination_token` (from `next_token`) while results are still in the window, for posts
aimed at the brand. Verbatim and public; drop the brand's own posts (`tool_get_me` id). X reads are billed per call.

**YouTube** (`YouTube`): `list_channel_videos` on the brand's channel, then
`list_comment_threads(video: <id>)` for the 10 most recent videos (or
`list_comment_threads(channel: …, search_terms: <pain phrase>)`). Verbatim, but anonymous: label
the kind as `public` and don't count them as customers.

## What to expect in real data

- **Most CRM text is the rep's paraphrase**, not the customer's words. Label every line
  `[verbatim]` (a transcript, or text in quotation marks attributed to the customer),
  `[paraphrase]` (rep notes) or `[translated]` (non-English source summarised in English). Never
  present a paraphrase as a quote.
- **Empty or junk engagements:** calls with no body, `hs_call_duration` < 60000 ms,
  `hs_call_disposition` = no answer / left voicemail, or notes like "LVM" or "no show". Count
  them as **empty** and list the counts, but don't analyse them.
- **Attribution:** resolve each engagement to its **company** through its associations
  (`get_crm_objects` with associations to `companies` and `contacts`). Count **distinct
  companies**. Engagements with no associated company or contact are "unattributed", reported
  but not counted toward clusters.
- **Call kind:** tag each engagement as `sales` (associated deal still open or not yet won),
  `onboarding` / `support` (company `lifecyclestage = customer`, or a ticket), `vendor` (someone
  pitching *us*), `partner`, or `internal`. **Exclude vendor, partner and internal** from every count.
  Report pain from before purchase and after purchase separately.
- **Product bugs aren't objections.** "Export is broken" and "no dark mode" go in a
  "Product feedback" section. Objections are about buying: price, sign-off, trust, timing, fit.
- **Large pulls.** Page through `search_crm_objects` with `after` (≤100 per page), request only the
  properties above, and process saved results with `jq` if a response spills to a file.
- Strip email addresses and phone numbers from any quoted text.

## Steps

### 1. Check sources, then load context

Call `list_integrations` and run **only the sources that are connected** (or picked with
`--source`). Make one cheap read per source: HubSpot `get_user_details` (read scopes on calls,
meetings, notes, tickets, deals, companies), Pipedrive / Upsales `list_users`, Crisp
`list_conversations` page 1, Discord `list_guilds`, YouTube `get_channel`, X `tool_get_me`. A 401,
Forbidden or "lacks scope" means 🔴 "reconnect <integration> in Cogny"; don't retry it. If a tool
is missing, call `refresh_mcp_discovery` once, then use the next source in the fallback order for
this run and mark it ⚠ "needs reconnect". If no CRM is connected, skip the CRM steps below and use the
fallback order in "Requires".

Read `brain/START-HERE`, `brain/company/customer-fit` and
`brain/decisions/agent-corrections`, and apply every correction. Read
`brain/evidence/customer-language/latest` for last week's clusters.

### 2. Pull engagements

**CRM branch (only if a CRM is connected).** For HubSpot, for each source in the table, `search_crm_objects` with a filter on its date property
(`hs_timestamp` for calls and notes, `hs_meeting_start_time` for meetings, `createdate` for
tickets, `closedate` for deals with `dealstage` in the lost stages from `get_properties(deals, dealstage)`)
within the window, sorted descending, up to 200 per source.

**If the window is empty**, say "no engagements in the last N days (latest: <date>)", show volume
by month, and offer a 30-day or `all` run rather than writing an empty report.

For `--segment`, keep engagements whose associated company matches `industry` or the ICP tier
property (`hs_ideal_customer_profile`) if the portal uses it.

For Pipedrive, Upsales, Crisp, Discord, YouTube and X, pull the same window as described in
"Other sources".

Record: total engagements per source, empty, unattributed, and counts by kind.

### 3. Extract problem statements

From each usable engagement, extract every statement of **pain, desire, fear, workaround, or
trigger**, plus every buying objection. For each one keep:
- text, labelled verbatim / paraphrase / translated
- type: pain / desire / fear / workaround / trigger / objection
- source object + id, date, company id (or "unattributed"), kind

### 4. Cluster and count

Group statements into clusters that describe the **same situation**. Name each cluster in
**the customer's words**, never marketing language:
- ✅ "I can't tell if I actually made money after returns, shipping and fees"
- ❌ "Profitability visibility challenges"

Count distinct sources of a statement, never mentions. One chatty customer saying it six times is one.
This is the most common error in round one. Keep two columns:
- **Companies**: distinct companies, for CRM sources (calls, meetings, notes, tickets, lost reasons).
- **People**: distinct people, for verbatim community sources (Discord authors, Crisp sessions /
  profiles, YouTube commenters, X accounts), which rarely resolve to a company.

A cluster qualifies for the top list when **either** count is ≥ 2. A cluster with ≤1 company and
≤1 person is `thin`. Never add the two columns together (a person may also be a company's contact).
Rank by companies first, then people.

### 5. Compare to last week

Mark each cluster as 🆕 new, ↑ rising, → steady or ↓ fading, against `latest`.

### 6. Write the report

`write_context_node` at `brain/evidence/customer-language/<YYYY-MM-DD>` and overwrite
`brain/evidence/customer-language/latest` with the same content.

```markdown
# Customer language — week of YYYY-MM-DD
Sources: <CRM> calls C · meetings M · notes N · tickets T · lost-deal reasons L · Crisp chats S · Discord D · YouTube comments Y · X mentions XM · files F
Skipped: <not connected / 🔴 reconnect / ⚠ needs reconnect, by name>
Usable: U (empty E, unattributed A) · kinds: sales S / onboarding O / support P (vendor/partner/internal excluded: X)
Verbatim share: 12% of statements (the rest are rep paraphrases). More transcripts would improve quality.

## Top problem clusters (by distinct companies, then people)
### 1. "<cluster name in their words>" — 11 companies · 4 people 🆕
- "transcript line" — call <id>, <date> [verbatim]
- "rep's note" — meeting <id>, <date> [paraphrase]
- "fragment" — call <id>, <date> [translated]
Situation: <when it hurts, one line>
Use as: headline / ad hook / sales opener → "<suggested line using their words>"

## Objections (by distinct companies)
| Objection (their words) | Companies | People | Stage it appears | Handled in offers? |

## Triggers mentioned ("what made you look now?")
## Words they use vs words we use
| They say | We say | Note |
## Post-purchase pain (support tickets, onboarding)
## Product feedback (route to product, not marketing)
## Thin signals (≤1 company and ≤1 person — watch, don't act)

Failures: <sources that errored or were capped, or "none">
```

### 7. Flag mismatches, don't fix them

If a top cluster contradicts `brain/company/customer-fit` or `brain/company/offers`, file **one**
review item per mismatch (`create_ticket` on Cloud, else `create_finding`): "[ME:customer-language] Review: customers keep saying X — offers says Y",
with the quotes in the body and `execution_target: "manual"`. Never edit company/ yourself.

If the verbatim share is under ~10% for two weeks running, file one ticket recommending call
transcripts in HubSpot (Conversation Intelligence or a Gong/Fathom sync). It's the biggest
quality lever for this agent.

### 8. Ask for corrections (interactive runs)

End with: "Which of these clusters is wrong or mislabeled?" Write each correction to
`brain/decisions/agent-corrections` as a rule, e.g. "Onboarding calls about setup friction are not
acquisition pain; exclude them from top clusters." Expect the first version to be about 70% right. After
three or four rounds it reads calls better than most of the team.

## Recording findings

Detect the plan from the tools that exist: use `create_ticket` first when it exists (Cloud), and
`create_finding` only when it doesn't (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Distinct companies (CRM) or distinct people (community), not mentions.** Either can qualify a cluster.
2. **Their words, not ours.** Cluster names must be sayable by a customer.
3. **Label verbatim / paraphrase / translated.** Most CRM text is a rep's paraphrase.
4. **List every empty, failed or capped source.**
5. **Evidence only.** Writes go to `brain/evidence/`; never to `company/` or `brand/`.
6. **Read-only on the CRM.** No personal data in outputs beyond what's needed to trace a quote (object id, date).
