---
name: creative-engine
description: Turn customer language into 8–12 genuinely different ad concepts (not 50 versions of one headline), generate the images with your real brand assets, and upload them to Meta, LinkedIn or TikTok in a PAUSED state, named with campaign ID, angle and format
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [cogny-image-gen, meta-ads, linkedin-ads, tiktok-ads, reddit-ads, x-ads, snapchat-ads]
user-invocable: true
argument-hint: "<campaign-ID> [--platform meta|linkedin|tiktok|reddit|x|snapchat] [--concepts 8] [--no-upload]"
allowed-tools:
  - Read
  - Write
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__mcp__cogny-image-gen__tool_list_brand_assets
  - mcp__cogny__mcp__cogny-image-gen__tool_list_uploads
  - mcp__cogny__mcp__cogny-image-gen__tool_analyze_media
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_facebook_pages
  - mcp__cogny__mcp__Meta_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Meta_Ads__tool_get_ad_sets
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__Meta_Ads__tool_get_ad_preview
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaigns
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_organizations
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ads
  - mcp__cogny__mcp__Reddit_Ads__tool_list_promotable_posts
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__X_Ads__tool_get_line_items
  - mcp__cogny__mcp__X_Ads__tool_get_cards
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ad_squads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_creatives
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Upsales__list_activities
  - mcp__cogny__mcp__Upsales__list_appointments
  - mcp__cogny__mcp__Discord__list_guilds
  - mcp__cogny__mcp__Discord__list_guild_channels
  - mcp__cogny__mcp__Discord__get_channel_messages
  - mcp__cogny__mcp__X_Organic__tool_get_mentions
  # No integration write tools are pre-approved (generate_image, create_*, upload_*): they prompt the user.
---

# Creative Engine

Creative is the new targeting. Meta's ad system (Andromeda) reads the ad itself to decide who
sees it, and it groups ads that look alike, so fifty versions of the same headline get
roughly the reach of one ad. Winners also burn out in two to three weeks. The job is a
steady stream of **genuinely different reasons to buy**, each built from what customers said.

**Requires:** Cogny with Meta Ads (or LinkedIn, TikTok, Reddit, X or Snapchat Ads). Use
`--no-upload` to get the concepts and images without touching an ad account.

**Plan matters:** image generation (`cogny-image-gen`, Nano Banana / GPT Image) is **Cloud-only**.
On **Solo** the skill writes the concepts plus a ready-to-paste image prompt and shot brief per
concept (aspect ratios, negative prompt, reference assets to use) instead of images, and uploads
only if the user supplies image URLs.

## Usage

- `/creative-engine BK014` — concepts + images + paused Meta ads for campaign BK014
- `/creative-engine BK014 --platform linkedin`
- `/creative-engine BK014 --no-upload` — creative pack only

The campaign must exist (`/campaign-ledger new`). Without an ID, stop and ask for one.
If the brain is missing, the concepts can still be drafted with `--no-upload`: take the customer
language from whichever sources are connected: the CRM's recent call and meeting notes (HubSpot
`search_crm_objects` on `calls` / `meetings`, Pipedrive `list_activities`, Upsales `list_activities` /
`list_appointments`), Discord `#support` via `get_channel_messages` (`limit: 50`; private channels only as
anonymised themes, per routing §5) and X mentions (`X_Organic` `tool_get_mentions`). Label the pack "no brain: provisional", and
list **every product claim as "needs confirmation"**, since there's no `offers` node to check them against.

**Health check:** `list_integrations` misses revoked tokens, so treat the first cheap read per integration
(`list_ad_accounts`, `list_guilds`, …) as the check. 401, Forbidden or a scope error = 🔴 "reconnect
<integration>": name it, don't retry. A missing tool: `refresh_mcp_discovery` once; new tools need a client
reconnect, so use the fallback above and mark the source ⚠.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this:

```
Creative Engine needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Meta Ads (or LinkedIn, TikTok, Reddit, X or Snapchat Ads); image generation needs the Cloud plan.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: draft concepts with --no-upload (no images, no ad creation).
```

In that case take the campaign ID the user gives (no ledger check), use customer language they paste or `./brain/evidence/customer-language/latest.md` from `/customer-language` local mode, run steps 1–2 only, label the pack "no Cogny: provisional" with every product claim marked "needs confirmation", and print it (or Write it to `./brain/campaigns/<ID>.md` if a local `./brain/` exists), then stop.

## Steps

### 1. Load inputs (the words come first, and that's where the strategy lives)

Read:
- `brain/campaigns/<ID>`: the angle, the verbatim quotes, the offer, the evidence bar
- `brain/evidence/customer-language/latest`: clusters, objections, "words they use vs we use"
- `brain/company/offers`: **approved claims only**
- `brain/brand/voice`: the loved and rejected examples, which are the style guide
- `brain/brand/founder-opinions`: material for the founder-rant concept
- `brain/decisions/failed-campaigns` and `brain/decisions/agent-corrections`

Pull what's already running so you don't duplicate it: Meta `get_ads` with `limit: 20` and
`include_creative: false` first (thumbnails stay large even at `thumbnail_width: 0`), then fetch creatives
only for the ads whose angle you need to see (all statuses, so you see past angles too;
`status_filter: ["ACTIVE"]` matches *effective* status) + `get_insights`
(`level: "ad"`, `date_preset: "last_30d"`). Empty insights means nothing delivered, so there's no fatigue data. Note which angles exist and which are fatiguing
(frequency up, CTR down week over week). On X, `get_campaigns` then `get_line_items(campaign_ids, limit: 20)`;
unfiltered line-item calls time out.

### 2. Write 8–12 distinct concepts

Each concept is a different **reason to buy**, not a different wording. Cover at least six of these:

Slugs come from the shared list in `/campaign-ledger`.

| Format slug | Concept |
|-------------|---------|
| `pain` | The situation in the customer's exact words |
| `worked-example` | Real numbers walked through ("$2.1M store, 14% returns → …") |
| `story` | One customer's before/after (real, with permission noted) |
| `founder` | A founder opinion from founder-opinions.md, unpolished |
| `comparison` | Us vs the usual way (not vs a named competitor unless approved) |
| `myth` | A belief in the category that's wrong |
| `demo` | The product doing the thing, as a raw screenshot or flow |
| `objection` | The top objection, answered |

For each concept, give: a slug (`dinner-angle`), the format, the source quote it came from, 2–3
hooks (first line / first 2 seconds), primary text, headline, CTA, and an image or video brief.

**Diversity check:** if two concepts would read the same with the headline swapped, merge them.
Report the final count honestly; 7 real concepts beat 12 near-copies.

**Claims check:** every claim must trace to `offers`. Drop or rewrite anything that promises
what offers doesn't allow, and list what you dropped.

### 3. Make the images (Cloud; on Solo write the prompts and briefs instead)

`list_brand_assets` (product, logo and persona) and `list_uploads`. Feed **real product photos**
as `brand_asset_ids` / `reference_image_url` so the product stays accurate, and let the model
change everything around it. **For SaaS** there usually are no `product` assets: pass the logo via
`brand_asset_ids` and real UI screenshots via `reference_image_url`, and never let the model invent the UI. Call `generate_image` once per concept and placement:
- Meta feed `4:5`, Stories/Reels `9:16`; LinkedIn `1:1` or `4:5`; TikTok and Snapchat `9:16`; Reddit `1:1` or `4:5`; X `16:9` or `1:1`
- `negative_prompt`: "distorted product, fake logos, third-party logos or trademarks, misspelled text, extra fingers"
- Keep headline text out of the image unless the concept needs it (a myth card, say)

Run `analyze_media` on each output and ask explicitly: wrong product details? garbled text? **any
third-party logo or trademark** (e.g. Google, Meta, LinkedIn)? any claim that isn't in offers? Fail
the image on any yes and regenerate once. The analyzer is lenient by default, so ask each question directly. Images of AI-generated people must be labelled where the platform requires it.

For video, write the script and shot list (and an AI-actor brief for testing). Note:
**use AI actors to test scripts, then pay real people to film the winner.**

### 4. Upload paused (only after the user says yes in this session)

Show the full pack first: a concept table with thumbnails (`public_url`). Ask "Upload these N ads
paused to <account>?" Then, for Meta:

1. `list_ad_accounts`, `get_facebook_pages` (get a valid Page id; never a profile.php id). On agency
   accounts this lists many client Pages, and `can_be_promoted_by_account` may flag the wrong one.
   Pick the Page that matches the brand name **and** is the Page existing ads use (their
   `effective_object_story_id` prefix). If those disagree, ask.
2. Find or confirm the ad set named `<ID>_<audience>`. If none exists, `create_campaign` /
   `create_ad_set` with **status PAUSED** and the budget **the user states**. Never invent a budget.
   Meta budgets are in minor units of the account currency (`35000` = 350.00 SEK), so confirm the conversion with the user.
3. For each concept, `create_ad` with:
   - `name`: `<ID>_<angle>_<format>_v1` (e.g. `BK014_dinner-angle_worked-example_v1`)
   - `status`: `"PAUSED"`, always and explicitly
   - `link`: landing URL with `utm_campaign=<id>_<slug>&utm_content=<angle>_<format>_v1`
   - `image_url`: the generated `public_url`
4. `get_ad_preview` for one ad to confirm it renders.

Other platforms follow the same rules: paused, named `<ID>_<angle>_<format>_v1`, UTM'd, and asked first.

| Platform | Path (write tools prompt per call) | Paused by |
|----------|-------------------------------------|-----------|
| LinkedIn | `tool_upload_image(ad_account_id, image_url)` → `tool_create_creative(ad_account_id, campaign_id, commentary, author_organization_urn, image_urn, destination_url, name)`. `commentary` (the ad text) and `author_organization_urn` are required. With several organizations (`LinkedIn_Organic` `tool_list_organizations`, or the author on existing `tool_get_creatives` posts), pick the one matching the brand, and ask if unclear | `status: "DRAFT"` (the default; the tool maps `PAUSED` to `DRAFT`, so say DRAFT) |
| TikTok | upload the image in TikTok Ads Manager or reuse `image_ids`, then `tool_create_ad(advertiser_id, adgroup_id, ad_name, ad_format, image_ids, landing_page_url)` | `operation_status: "DISABLE"` |
| Reddit | `tool_create_post(title, url, …)` creates the promotable post (or reuse one from `tool_list_promotable_posts`) → `tool_create_ad(ad_account_id, ad_group_id, name, post_id, click_url)` | `status: "PAUSED"` (default) |
| X | **Media first:** `tool_upload_media` takes a `file_path` on the proxy host, not a URL, so a generated `public_url` can't be uploaded from Cloud. Reuse an existing `media_key` (from `tool_get_cards` components; note this ships that **old** image, not the new one) or have the user upload the new image in X Ads. Then `tool_create_card(account_id, name, components: [{type: "MEDIA", media_key}, {type: "DETAILS", title, destination: {type: "WEBSITE", url: <UTM'd URL>}}])` → `tool_create_tweet(account_id, text, card_uri, nullcast: true)` → `tool_create_promoted_tweet(account_id, line_item_id, tweet_id)` on a line item whose `entity_status` is `"PAUSED"` | line item / campaign `entity_status: "PAUSED"` (default) |
| Snapchat | no creative-upload tool: reuse an existing creative from `tool_get_creatives`, or have the user upload in Ads Manager, then `tool_create_ad(ad_account_id, ad_squad_id, name, creative_id)` | `status: "PAUSED"` (default) |

A Reddit post created with `tool_create_post` is public on the brand's profile, so show it to the
user and confirm before creating it. On X, `nullcast: true` keeps the ad tweet off the organic timeline.

### 5. Record and queue

- Write the concept table, asset URLs, ad IDs and the evidence bar into `brain/campaigns/<ID>` under `## Assets`.
- One review item, "[ME:creative-engine] Approve: N paused ads for <ID> — go live?", with the concept table, the dropped
  claims, the budget and the kill rule `/ad-kill-rules` will enforce. Cloud: `create_ticket` with `estimated_cost_usd` +
  `cost_cadence` + `cost_type: "ad_spend"`. Solo: `create_finding` with the spend written in the body.

A human hits go. This skill never sets an ad to ACTIVE.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Different reasons to buy, not different wordings.**
2. **Every claim traces to `offers`.**
3. **Real product imagery as reference.** Never let the model invent the product.
4. **PAUSED, always.** Never call `update_ad_status` with ACTIVE, and never set or raise a budget the user didn't state.
5. **Name = ID + angle + format + version**, so lessons stay reusable.
6. **Evidence bar before launch.** If the campaign folder has none, stop and ask for one.
