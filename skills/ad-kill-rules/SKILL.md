---
name: ad-kill-rules
description: Enforce a pre-declared evidence bar on every ad — after it spends enough, pause it if it misses (e.g. CTR < 1% or cost per lead over cap) across Meta, TikTok, LinkedIn, Google and Bing — as a dry-run report, an approved pause, or a scheduled pause-only Cogny script
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [meta-ads, tiktok-ads, linkedin-ads, google-ads, bing-ads, x-ads, reddit-ads, snapchat-ads, apple-search-ads, openai-ads, bidtheatre]
user-invocable: true
argument-hint: "[check|apply|schedule] [<campaign-ID>]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__get_script_sdk_reference
  - mcp__cogny__list_scripts
  - mcp__cogny__get_script_run
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ads
  - mcp__cogny__mcp__TikTok_Ads__tool_get_insights
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_analytics
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Bing_Ads__tool_get_ads
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__X_Ads__tool_get_line_items
  - mcp__cogny__mcp__X_Ads__tool_get_promoted_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_analytics
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ads
  - mcp__cogny__mcp__Reddit_Ads__tool_get_reporting
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_stats
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_report
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_account
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_campaigns
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ads
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_insights
  - mcp__cogny__mcp__Bidtheatre__list_campaigns
  - mcp__cogny__mcp__Bidtheatre__get_campaign_status
  # No integration write tools are pre-approved (pause tools included); `apply` prompts per call.
---

# Ad Kill Rules

A small script checks results every morning and pauses anything that missed the bar after a
set amount of spend. Decide the bar **before** you launch: how much spend, how many days, and
what counts as a win. Skip that and 200 ads give you 200 inconclusive experiments.

This is an exact rule, so it belongs in code rather than a model's judgment. The skill reports in
chat, and `schedule` turns it into a deterministic Cogny script that can only **pause**.

**Requires:** Cogny ($9/mo) with at least one ad platform connected.

## Usage

- `/ad-kill-rules` or `check` — dry run: what would be paused, and why
- `/ad-kill-rules apply BK014` — pause the flagged ads for one campaign (asks per batch)
- `/ad-kill-rules schedule` — create a daily pause-only script

## The rule file

Rules live in the YAML block under `## Evidence bar` in `brain/campaigns/<ID>` (written by
`/campaign-ledger new`, keyed by the campaign ID), with a default at
`brain/contracts/ad-kill-rules`. Log every pause under that folder's `## Kill log` section. If no default exists, write one with the user:

```yaml
default:
  currency: SEK          # MUST match the ad account currency (customer.currency_code / account currency)
  min_spend: 500         # in `currency`, per ad, before any judgment (~$50); rescale for your currency
  min_days: 3            # days since first impression
  min_impressions: 2000
  kill_if:
    ctr_below: 1.0       # percent, link CTR where available
    cpl_above: 1200      # cost per lead / key event in `currency`; null to skip
                         # 0 leads: broken once spend >= cpl_above (CPL is undefined, treat as infinite)
    frequency_above: 4.0 # fatigue
  protect:
    - name_contains: "_founder_"   # never auto-kill these; flag only
  max_pauses_per_run: 10
  scope: name_prefix_in_ledger     # only ads whose name starts with a ledger ID
```

Per-campaign blocks override the default. **Scope is limited to ID-named assets by design**, so
the rule never touches legacy or brand campaigns that someone else owns.

**Where the ID is matched:** Google and Bing search ads and X promoted tweets have **no ad
name**, so match the ID on the parent campaign, ad group or line item name. Match on the ad name
only on Meta, TikTok and LinkedIn.

**First run:** if neither `brain/contracts/ad-kill-rules` nor a ledger exists, the scope is
empty and the skill does nothing. Say so, and tell the user to run `/campaign-ledger init` and
write the rule file first.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Ad Kill Rules needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect at least one ad platform (Meta, TikTok, LinkedIn, Google, Bing, X, Reddit, Snapchat, Apple Search Ads, OpenAI Ads or Bidtheatre).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny: the rule file, the ads and the pause all live there.
```

## Steps — check

1. Read the rules and `brain/campaigns/ledger` (the list of live IDs). **Health check:** `list_integrations`,
   then each platform's account call (Google `tool_list_accessible_accounts`, Bing `tool_list_accounts`,
   X `tool_list_ad_accounts`, OpenAI Ads `tool_get_ad_account`, Meta/LinkedIn/Reddit `tool_list_ad_accounts`,
   TikTok `tool_list_advertisers`) as the cheap read. 401, Forbidden or a scope error = 🔴 "reconnect
   <integration>": name it in the output and don't retry. A missing tool: `refresh_mcp_discovery` once; new tools
   need a client reconnect, so skip that platform this run and mark it ⚠.
2. For each platform, pull ad-level data for the period since each ad's first delivery (cap 30 days):
   - **Meta**: `get_ads` (use `effective_status`, not `status`; an ad can be `ACTIVE` under a
     `CAMPAIGN_PAUSED` or `ADSET_PAUSED` parent) and `get_insights` `level: "ad"`,
     `date_preset: "last_30d"` (ctr, spend, impressions, frequency, actions). Empty insights means nothing delivered.
   - **TikTok**: `get_insights` `level: "AUCTION_AD"`, metrics `spend,impressions,clicks,ctr,conversion,cost_per_conversion,frequency`
   - **LinkedIn**: `get_analytics` by creative
   - **Google**: GAQL
     ```sql
     SELECT ad_group_ad.ad.id, ad_group.id, ad_group.name, campaign.name, customer.currency_code,
       metrics.cost_micros, metrics.impressions, metrics.ctr, metrics.conversions
     FROM ad_group_ad
     WHERE segments.date DURING LAST_30_DAYS AND ad_group_ad.status = 'ENABLED'
       AND ad_group.status = 'ENABLED' AND campaign.status = 'ENABLED'
     ```
     **`metrics.ctr` is a fraction (0.0439 = 4.39%), so multiply by 100** before comparing to
     `ctr_below`. Otherwise every ad looks like a kill. Get first-delivery dates with a second
     query segmented by `segments.date` (`metrics.impressions > 0`) and take the min date per ad.
   - **Bing**: `get_report` `report_type: "ad"`, with `aggregation: "Daily"` for first-delivery
     dates. Percent columns are already percents.
   - **X**: `get_campaigns`, then `get_line_items(campaign_ids, limit: 20)` (unfiltered calls time out),
     then `get_promoted_tweets` → `get_analytics` `entity: "PROMOTED_TWEET"` (at most 20 `entity_ids` per call: batch). Line items have no
     `effective_status`, and `servable` reads false even under running campaigns, so "active" means
     campaign `effective_status == "RUNNING"` plus line item `entity_status == "ACTIVE"`. CTR = all
     `clicks` ÷ impressions × 100 (`url_clicks` is often 0 or empty). `conversion_leads` is an alias of
     `conversion_sign_ups`, so count only one of them.
   - **Reddit**: `tool_get_ads(ad_account_id)` (status `ACTIVE`) and
     `tool_get_reporting(ad_account_id, start_date, end_date, level: "ad", time_granularity: "DAY")`
   - **Snapchat**: `tool_list_organizations` → `tool_list_ad_accounts` → `tool_get_ads`, then
     `tool_get_stats(entity_id: <ad id>, start_time, end_time, level: "ad")` per ad (cap at 50 ads)
   - **ChatGPT ads (OpenAI Ads)**: `tool_get_campaigns` → `tool_get_ad_groups` → `tool_get_ads(ad_group_id)`,
     and `tool_get_insights(aggregation_level: "ad", start_date, end_date, time_granularity: "daily")`
     (accepts `hourly|daily|monthly|none`). `ctr` is a fraction, so multiply by 100 as on Google.
   - **Apple Search Ads**: there are no creatives to kill. The unit is the **ad group**:
     `tool_get_ad_groups(org_id, campaign_id)` + `tool_get_campaign_report`. Apply the CPA/CPT rules
     only (CTR means tap-through rate here).
   - **Bidtheatre**: report-only. There's no pause tool in the catalog, so flag kills for a human
     (`list_campaigns`, `get_campaign_status` for pacing).
3. Keep only ads that are **actually delivering**: the ad, its ad set/ad group and its campaign are all
   active (Meta `effective_status == "ACTIVE"`; X as above), and the ID matches a live ledger ID per the rule above.
   Convert every money figure to the rule file's `currency`, or stop if the currencies differ and no rate is given.
4. Classify each ad:
   - ⏳ **Learning**: below min_spend, min_days or min_impressions. No verdict.
   - ✅ **Passing**
   - 🔴 **Kill**: met the minimums and broke a `kill_if` rule
   - 🟡 **Protected**: would be killed but matches `protect`, so flag it for a human
5. Guard: if a kill would leave an ad set or ad group with **zero active ads**, downgrade it to 🟡 and say so.
   Count only siblings with impressions > 0 in the window (an "active" ad that never delivers doesn't keep
   the group alive). Count siblings from the same pull (Google `ad_group.id`; Meta `get_ads` by `adset_id`; TikTok
   `get_ads` by `adgroup_id`; Reddit `ad_group_id`; Snapchat `ad_squad_id`; OpenAI Ads `ad_group_id`).
   An empty ad set can reset learning or stop delivery entirely.

```
Kill check — YYYY-MM-DD (dry run)
Checked 46 ads on Meta, TikTok, Google · skipped: LinkedIn (auth error)
🔴 Kill (6) — would save ~$85/day
| Ad | Platform | Spend | Days | CTR | CPL | Rule broken |
🟡 Needs a human (2)
⏳ Learning (19) · ✅ Passing (19)
```

## Steps — apply

Run `check`, show the kill list, and ask once for the batch. Then call the platform's pause tool
for each ad:

| Platform | Pause tool | Value |
|----------|-----------|-------|
| Meta | `Meta_Ads/tool_update_ad_status` | `"PAUSED"` |
| TikTok | `TikTok_Ads/tool_update_ad_status` | `"DISABLE"` |
| Google | `Google_Ads/tool_update_ad_status` | `"PAUSED"` |
| Microsoft | `Bing_Ads/tool_update_ad_status(account_id, ad_group_id, ad_id, status, ad_type)` | `"Paused"`; `ad_group_id` from the ad report, `ad_type` = the ad's `Type` from `tool_get_ads(ad_group_id)` (e.g. `ResponsiveSearch`) |
| LinkedIn | `LinkedIn_Ads/tool_update_creative_status` | `"PAUSED"` |
| X | `X_Ads/tool_update_promoted_tweet_status` | `entity_status: "PAUSED"` |
| Reddit | `Reddit_Ads/tool_update_ad_status(ad_account_id, ad_id, status)` | `"PAUSED"` |
| Snapchat | `Snapchat_Ads/tool_update_ad_status(ad_account_id, ad_id, status)` | `"PAUSED"` |
| ChatGPT ads | `OpenAI_Ads/tool_update_ad_status(ad_id, status)` | `"paused"` (lowercase) |
| Apple Search Ads | `Apple_Search_Ads/tool_update_ad_group(org_id, campaign_id, ad_group_id, status)` | `"PAUSED"` |
| Bidtheatre | none, so file a review item | — |

Read the tool's schema before the first call; value casing differs per platform. **Only ever pause.** Respect `max_pauses_per_run`.

Afterwards, log every pause in `brain/campaigns/<ID>` (`## Kill log`: ad, metric at kill, date),
and record the pauses: Cloud `create_ticket` with `already_done: true` and `result`, so Cogny
measures the impact; Solo `create_finding` then `update_finding_status` to done.

## Steps — schedule

**Solo** has no scripts or automations. Run `check` on a schedule with Claude Code's `/schedule` or
`/loop`, and keep `apply` manual. The rest of this section is **Cloud**.

1. `get_script_sdk_reference` and read it.
2. Write a `create_script` that:
   - reads the rules (hard-code them into the script and print them in `description`)
   - pulls ad-level insights via `cogny.mcp.call(...)` for each platform
   - applies exactly the classification above, including the empty-ad-set guard and `max_pauses_per_run`
   - pauses via the platform's status tool with the status hard-coded to `"PAUSED"`
   - stores a run log with `cogny.state.set`, and `console.log`s every decision
3. `mcp_grants`: only the pause tools for platforms in scope (e.g. `Meta Ads / update_ad_status`).
4. Create with `enabled: false`, `crontab: "0 8 * * *"`. `run_script` with `dry_run: true`, show the
   output, and only then enable after the user says yes.

If the user prefers a judgment-based run, use `create_automation` instead, with an `action_grants`
entry for `update_ad_status` **pinned via `constraints: {"status": "PAUSED"}`** so it cannot activate anything.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **The bar is decided before launch.** No rule means no kill. Report "no evidence bar" and stop.
2. **Pause only.** Never activate, delete, or change budgets.
3. **Only ID-named ads in the ledger.** Never touch anything outside scope.
4. **Never empty an ad set** automatically.
5. **Name every platform that failed** to return data. A silent skip looks like "all passing".
