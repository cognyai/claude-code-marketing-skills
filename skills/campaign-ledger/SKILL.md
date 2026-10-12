---
name: campaign-ledger
description: Give every campaign an ID and carry it everywhere — allocate IDs, audit ad/email/UTM naming across Google, Meta, LinkedIn, Bing, TikTok and X, and keep one ledger joining spend → leads → deals → revenue per campaign ID
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [google-ads, bing-ads, apple-search-ads, openai-ads, meta-ads, linkedin-ads, tiktok-ads, x-ads, reddit-ads, snapchat-ads, bidtheatre, ga4, plausible, klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, hubspot, pipedrive, upsales, fibbler]
user-invocable: true
argument-hint: "[init|new <name>|audit|sync|show <ID>]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__list_datasets
  - mcp__cogny__execute_bigquery_sql
  - mcp__cogny__get_script_sdk_reference
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaigns
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_analytics
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_campaigns
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ads
  - mcp__cogny__mcp__TikTok_Ads__tool_get_insights
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__X_Ads__tool_get_line_items
  - mcp__cogny__mcp__X_Ads__tool_get_promoted_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_cards
  - mcp__cogny__mcp__X_Ads__tool_get_analytics
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ads
  - mcp__cogny__mcp__Reddit_Ads__tool_get_reporting
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ad_squads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_stats
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_account_spend
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_account
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_campaigns
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ads
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_insights
  - mcp__cogny__mcp__Bidtheatre__list_advertisers
  - mcp__cogny__mcp__Bidtheatre__list_campaigns
  - mcp__cogny__mcp__Bidtheatre__get_campaign
  - mcp__cogny__mcp__Bidtheatre__get_report
  - mcp__cogny__mcp__Mailchimp__tool_list_campaigns
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_sent
  - mcp__cogny__mcp__Klaviyo__list_campaigns
  - mcp__cogny__mcp__Rule__tool_list_campaigns
  - mcp__cogny__mcp__Brevo__list_email_campaigns
  - mcp__cogny__mcp__MailerLite__list_campaigns
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__get_deal
  - mcp__cogny__mcp__Pipedrive__list_deal_fields
  - mcp__cogny__mcp__Upsales__list_orders
  - mcp__cogny__mcp__Upsales__list_leads
  - mcp__cogny__mcp__Upsales__list_campaigns
  - mcp__cogny__mcp__Upsales__get_metadata
  - mcp__cogny__mcp__app-fibbler-co__get_cross_channel_performance
  - mcp__cogny__mcp__app-fibbler-co__get_deal_campaign_breakdown
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
---

# Campaign Ledger

The unglamorous part, and the most valuable thing in the whole setup. Most companies can
tell you clicks by campaign and revenue by customer, and very few can connect the two. Give
every campaign an ID, put it in every name, and keep one table: **ID, spend, leads,
qualified calls, deals, revenue, churn.** Then agents can answer the question that matters:
*which marketing brought in customers who paid and stayed?*

**Requires:** Cogny ($9/mo). Works with whichever ad platforms are connected.

## Usage

- `/campaign-ledger init` — choose a prefix, audit current naming, create the ledger
- `/campaign-ledger new "dinner angle"` — allocate the next ID and create its campaign folder
- `/campaign-ledger audit` — find assets that break the naming convention
- `/campaign-ledger sync` — refresh spend + outcomes per ID (daily)
- `/campaign-ledger show BK014` — one campaign, end to end

## The convention

```
Campaign ID   <PREFIX><NNN>                     BK014
Ad name       <ID>_<angle>_<format>_v<n>        BK014_dinner-angle_ugc_v2
Ad set/group  <ID>_<audience>                   BK014_shopify-1to10m
Platform camp <ID>_<objective>_<short-name>     BK014_leads_profit-review
UTM           utm_campaign=<id-lowercase>_<slug>&utm_content=<angle>_<format>_v<n>
Email/news    <ID> — <subject idea>
CRM deal      note or property "campaign_id: BK014"
```

Angle and format are in the name so that a month later "the dinner angle beat the price
angle" is a usable lesson, whereas "video_final_7 won" is trivia.

**Format slugs (the one shared list).** `/creative-engine` and `/social-engine` use these too:
`pain`, `worked-example`, `story`, `founder`, `comparison`, `myth`, `demo`, `objection`,
`customer-words`, `question`, `static`, `carousel`, `ugc`, `short-video`. Add a new slug here
first, then use it.

Regex the audit uses: `^([A-Z]{2,4}\d{3})_([a-z0-9-]+)_([a-z0-9-]+)_v\d+$` for ads,
`^([A-Z]{2,4}\d{3})_` for everything else.

**Where the ID can live per platform.** Google/Bing responsive search ads, Apple Search Ads and X
promoted tweets have **no ad name** (`ad_group_ad.ad.name` is `""`). On those platforms the ID goes
on the campaign and ad group / line item, and the angle goes in `utm_content`. Apply the ad-name
regex on Meta, TikTok, LinkedIn, Reddit, Snapchat and ChatGPT-ads (OpenAI Ads) ads.
Bidtheatre campaigns carry the ID in the campaign name.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Campaign Ledger needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ad platforms (and email, analytics and CRM, if you want the ledger to reach revenue).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny. The naming convention above still works by hand.
```

## Steps — init

1. Ask for a 2–4 letter prefix (default: initials of the brand).
2. Run **audit** (below) to see how far current naming is from the convention.
3. Create `brain/campaigns/ledger` with the header table (below) and `next_id: <PREFIX>001`.
4. Offer to backfill: group currently running platform campaigns into logical campaigns,
   propose IDs, and file **one** ticket listing the rename map. Never rename assets yourself.
   Renaming resets nothing on the platforms, but it's still the user's call.

## Steps — new

1. Read `brain/campaigns/ledger`. **If it doesn't exist, run `init` first.** Take `next_id` and increment it.
2. Read the ad accounts' currency (`customer.currency_code`, Meta/X account currency). The evidence
   bar is written in that currency, never in an assumed `$`.
3. Create `brain/campaigns/<ID>`. This is the **canonical campaign folder**; every agent writes only
   to its own section, and a skipped agent writes one line saying why:

````markdown
# <ID> — <name>
Status: planning · Owner: <user> · Created: YYYY-MM-DD
## Why (customer words) — copied verbatim from [[brain/evidence/customer-language/latest]]
Source: customers | prospects | community | ad repliers   ← say who said it; ad repliers aren't customers
## Offer — link to approved entry in [[brain/company/offers]] (or the pending offer ticket)
## Audience — from [[brain/company/customer-fit]]
## Evidence bar (decided BEFORE launch; /ad-kill-rules reads this block)
```yaml
<ID>:
  currency: SEK          # the ad account currency
  min_spend: ___         # per ad, before any judgment
  min_days: ___
  min_impressions: ___
  kill_if:
    ctr_below: ___       # percent
    cpl_above: ___       # cost per lead/key event in `currency`; null to skip
  win_metric: "___"      # e.g. "cost per qualified call < 400 SEK"
```
## UTM base — utm_campaign=<id>_<slug>
## Assets — /creative-engine (concepts, image URLs, ad IDs)
## Search page — /search-demand page
## Social hooks — /social-engine hooks (link to the batch node)
## Closed-lost matches — /closed-lost-revival match
## Trigger accounts — /buying-triggers
## Kill log — /ad-kill-rules
## Results — /campaign-ledger sync
````

4. Append the row to the ledger and print the UTM base and naming examples for the user.

Refuse to finalize without an evidence bar. Without one, 200 ads give you 200 inconclusive experiments.

## Steps — audit

**Health check first.** `list_integrations` misses revoked tokens, so make the platform's account call
(first in each row) as a cheap read. 401, Forbidden or a scope error means 🔴 "reconnect <integration>":
report it by name and don't retry. If an expected tool is missing, call `refresh_mcp_discovery` once;
new tools only load after the client reconnects, so skip that call this run and mark the source ⚠.

For each connected platform, list active and recently active assets (last 30 days with spend):

| Platform | Calls |
|----------|-------|
| Google Ads | `list_accessible_accounts`, then GAQL `SELECT campaign.name, ad_group.name, ad_group_ad.ad.name, ad_group_ad.ad.final_urls, ad_group_ad.ad.final_url_suffix, campaign.final_url_suffix, ad_group_ad.ad.id, metrics.cost_micros FROM ad_group_ad WHERE segments.date DURING LAST_30_DAYS AND metrics.cost_micros > 0` and `SELECT customer.currency_code, customer.auto_tagging_enabled, customer.tracking_url_template, customer.final_url_suffix FROM customer`. **With `auto_tagging_enabled = true`, a missing UTM is not a defect**, because GA4 gets the campaign name via gclid. |
| Meta | `list_ad_accounts` → `get_campaigns`, `get_ads` (UTMs live in the creative's `url_tags` / `destination_url`; filter on `effective_status`), spend via `get_insights` |
| LinkedIn | `list_ad_accounts` → `get_campaigns`, `get_creatives`, spend via `get_analytics` |
| Bing | `list_accounts` → `get_campaigns` with `campaign_types: ["Search", "PerformanceMax", "Shopping", "Audience"]` (it returns Search only by default), `get_report` (report_type `ad`) |
| TikTok | `list_advertisers` → `get_campaigns`, `get_ads`, spend via `get_insights` |
| X | `list_ad_accounts` → `get_campaigns`, `get_line_items(campaign_ids, limit: 20)` (the ID goes on campaign and line item; unfiltered calls time out), `get_promoted_tweets` (no `card_uri`). Check the bare URLs in `tweet_urls` first; plain link tweets carry their UTMs there. Then `get_tweets(tweet_ids)` and read `get_cards` only for tweets that have a `card_uri`. Spend via `get_analytics` (at most 20 `entity_ids` per call: batch) |
| Reddit | `tool_list_ad_accounts` → `tool_get_campaigns(ad_account_id)`, `tool_get_ads`; spend via `tool_get_reporting(ad_account_id, start_date, end_date, level: "ad")` |
| Snapchat | `tool_list_organizations` → `tool_list_ad_accounts(organization_id)` → `tool_get_campaigns`, `tool_get_ad_squads`, `tool_get_ads`; spend via `tool_get_stats(entity_id, start_time, end_time, level)` |
| Apple Search Ads | `tool_list_acls` (org ids) → `tool_get_campaigns(org_id)`, `tool_get_ad_groups`; spend via `tool_get_campaign_report(org_id, campaign_id, start_date, end_date)` or `tool_get_account_spend` |
| ChatGPT ads (OpenAI Ads) | `tool_get_ad_account` → `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads(ad_group_id)` (creative `target_url` holds the UTM); spend via `tool_get_insights(aggregation_level, start_date, end_date)` |
| Bidtheatre | `list_advertisers` → `list_campaigns(advertiser)`, `get_campaign`; spend needs an async report: `create_report` (a write tool, so ask first) → `get_report(report_id, poll: true)` |
| Email | Klaviyo `list_campaigns`, Mailchimp `tool_list_campaigns`, Rule `tool_list_campaigns`, Get a Newsletter `tool_list_sent`, Brevo `list_email_campaigns`, MailerLite `list_campaigns`: the campaign name should start with the ID |

Report per platform, **in the account's own currency** (never mix currencies in one total
without stating the rate): % of spend on assets with a valid ID, assets with no ID, IDs that
appear on platforms but not in the ledger, and final URLs missing `utm_campaign` (unless Google
auto-tagging covers them). Then use GA4 `run_report` (property id from `list_account_summaries`) with dimensions
`sessionCampaignName, sessionSourceMedium` (last 30 days) to see which campaigns actually arrive.
Without GA4, use Plausible `breakdown(site_id, dimension: "visit:utm_campaign", date_range: "30d")`.
Exclude the placeholder values `(direct)`, `(organic)`, `(referral)`, `(not set)`,
`(ai-assistant)` and `(cross-network)`. Also flag big untagged referrers from ad platforms
(e.g. `t.co / referral` while X ads run): report it as **X ad traffic losing its campaign**.

```
Naming audit — YYYY-MM-DD
Spend with valid ID: 38% (4,210 of 11,080 SEK)
| Platform | Spend | % ID'd | Missing UTM | Top offenders |
Unknown IDs (on platform, not in ledger): BK009, BK011
```

## Steps — sync

For each ID in the ledger with status `live` or `ended < 60 days`:

1. **Spend, impressions, clicks** per platform, filtered by name prefix (GAQL `WHERE campaign.name LIKE 'BK014%'`
   or ad-name matching; Meta/TikTok `get_insights` at ad level; LinkedIn `get_analytics`; Bing `get_report`;
   X `get_analytics`; Reddit `tool_get_reporting`; Snapchat `tool_get_stats`; Apple `tool_get_campaign_report`;
   OpenAI Ads `tool_get_insights`; Bidtheatre report). Keep each platform in its own currency, and say
   so when you convert.
2. **Leads / qualified calls**: GA4 key events by `sessionCampaignName` starting with the id.
   HubSpot contacts created in the window whose `hs_analytics_source_data_2` (original
   `utm_campaign` for paid sources) or `hs_latest_source_data_2` starts with the id. Count meetings booked
   (`meetings` associated with those contacts) as qualified calls.
3. **Deals + revenue**: fibbler `get_deal_campaign_breakdown` (LinkedIn/Google) and
   `get_cross_channel_performance` (`include_campaign_spend: true`) for the deduplicated totals;
   HubSpot deals with `hs_is_closed_won = true` whose `campaign_id` deal property equals the ID (high
   confidence), or whose associated contact's original source carries it (medium). Pass `crm: "hubspot"` to fibbler.
   **Pipedrive:** won deals (`list_deals(status: "won")`) with a `campaign_id` custom field (find its
   hashed key with `list_deal_fields`). **Upsales:** `list_orders` with `probability = 100` whose campaign
   (`list_campaigns`) or lead source (`list_leads`) carries the ID; find custom fields with `get_metadata`.
4. **Churn / refunds**: for won deals, check Stripe (via `/performance-memo`) only when ≥60 days old.

Write the row back and set a `confidence` column: **high** (ID on the deal), **medium**
(fibbler influence), **low** (time-window guess). Never mix confidence levels without labelling them.

Optional, **Cloud only** (Solo has no BigQuery or scripts): if the workspace has BigQuery (`list_datasets`), offer to create a
`marketing.campaign_ledger` table and a daily `create_script` that does this sync
deterministically. Read `get_script_sdk_reference` first, create it disabled, and dry-run it.

### Ledger format (`brain/campaigns/ledger`)

```markdown
next_id: BK015
| ID | Name | Status | Start | Spend | Leads | Qual. calls | Deals | Revenue | Churned | Cost/qual call | Confidence |
|----|------|--------|-------|-------|-------|-------------|-------|---------|---------|----------------|------------|
```

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **No ID, no launch.** Every new campaign goes through `new`.
2. **Never rename or edit platform assets.** Propose the rename map as a ticket.
3. **Label attribution confidence** on every row.
4. **Don't sum fibbler per-channel deal counts.** A deal touched by two channels appears in both; use `totals`.
5. **Report every platform that failed to return data**, by name.
