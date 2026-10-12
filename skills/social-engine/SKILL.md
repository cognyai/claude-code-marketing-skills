---
name: social-engine
description: Use organic LinkedIn and X as a free creative test kitchen — listen to what people complain about and ask for, draft a week of hooks from customer language and founder opinions, schedule only what you approve, then promote the posts the algorithm picked up into paid tests
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [linkedin-organic, x-organic, youtube, brave-search, discord, crisp, cogny]
user-invocable: true
argument-hint: "[listen|hooks [<campaign-ID>]|results|schedule]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_me
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_organizations
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_organization_posts
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_post_statistics
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_organization_statistics
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_comments
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_scheduled_posts
  - mcp__cogny__mcp__X_Organic__tool_get_me
  - mcp__cogny__mcp__X_Organic__tool_get_user_posts
  - mcp__cogny__mcp__X_Organic__tool_get_posts
  - mcp__cogny__mcp__X_Organic__tool_get_mentions
  - mcp__cogny__mcp__X_Organic__tool_search_recent_posts
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_promoted_tweets
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - mcp__cogny__mcp__Discord__list_guilds
  - mcp__cogny__mcp__Discord__get_channel_messages
  - mcp__cogny__mcp__Discord__list_guild_channels
  - mcp__cogny__mcp__YouTube__get_channel
  - mcp__cogny__mcp__YouTube__get_channel_performance
  - mcp__cogny__mcp__YouTube__list_channel_videos
  - mcp__cogny__mcp__YouTube__get_videos
  - mcp__cogny__mcp__YouTube__list_comment_threads
  - mcp__cogny__mcp__YouTube__search_videos
  - mcp__cogny__mcp__Crisp__list_conversations
  - mcp__cogny__mcp__Crisp__get_conversation_messages
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Upsales__list_activities
  - mcp__cogny__mcp__Upsales__list_appointments
  # No integration write tools are pre-approved (schedule_post, create_post, create_thread prompt the user).
---

# Social Engine

Paid gets the attention, but organic is the cheapest creative testing lab ever invented.
Post ten hooks organically, see which ones the algorithm picks up, and **only then** put money
behind the winners. Your ad budget only goes to ideas that have already proved themselves.

When every brand can generate content, a real person with real opinions is the scarcest thing
on the feed. So this engine runs on the founder's own takes and the customer's own words, and
a human stays on the publish button.

**Requires:** Cogny ($9/mo) with LinkedIn Organic, X Organic and/or YouTube. Brave, Discord and
Crisp are optional listening sources. Use whichever platforms are connected and report each one
separately; never blend baselines across platforms.

**Health check:** `list_integrations` misses revoked tokens, so make one cheap read per integration
(`get_me`, `list_organizations`, `list_guilds`, …). 401, Forbidden or a scope error = 🔴 "reconnect
<integration>": name it and don't retry. **YouTube is gated on its tools existing**, not on `list_integrations`:
if YouTube is connected but `get_channel_performance` / `list_comment_threads` aren't loaded, call
`refresh_mcp_discovery` once. New tools need a client reconnect, so skip YouTube this run and mark it ⚠ "needs reconnect".

## Usage

- `/social-engine listen` — what people complain about, ask for and get excited about this week
- `/social-engine hooks` — draft next week's batch (default 10 posts)
- `/social-engine hooks BK014` — hooks for one campaign's angle
- `/social-engine results` — which hooks won, and which to promote to paid
- `/social-engine schedule` — schedule the posts the user approved

Rhythm: `listen` + `results` on Friday, `hooks` on Sunday, approve the batch, schedule.

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Social Engine needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect LinkedIn Organic, X Organic and/or YouTube.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Steps — listen

Read `brain/company/customer-fit` for the category terms and competitors. If it's missing, take
pain phrases from the latest customer-language report, or from whichever sources are connected: CRM call
and meeting notes (HubSpot `search_crm_objects` on `calls` / `meetings`, Pipedrive `list_activities`, Upsales
`list_activities` / `list_appointments`), Discord `#support` and X mentions (`get_mentions`). Ask the user for competitors.

- **X**: `search_recent_posts` for the category pain phrases (take them from customer-language clusters),
  competitor names, and competitor + switching words (alternative, switched, cancel), using
  `-is:retweet`, `max_results: 50`, `sort_order: "relevancy"`. Also run `get_mentions` for our own account.
- **Reddit and forums**: `brave_search` `site:reddit.com <pain phrase>` with freshness `pw`, plus
  review sites for competitors (G2, Capterra, Trustpilot) with freshness `pm`.
- **Own community**: Discord `list_guilds` → `list_guild_channels` → `get_channel_messages` (`limit: 50`) on
  public channels (support, feedback, general or their equivalents). A channel is **private** when its
  `permission_overwrites` (or its parent category's) has an entry with `id == guild_id` that denies
  `VIEW_CHANNEL` (bit 1024). **Never quote private channels** in posts or drafts; use them only as anonymised
  themes. Skip `author.bot` and staff. A `Forbidden` on a channel means "not readable": list it and continue.
- **Own comments**: LinkedIn `get_comments` on our last 10 posts; YouTube
  `list_comment_threads(channel: <our channel>, order: "time")` for questions under our videos.
- **YouTube category search**: `search_videos(query: <pain phrase>, published_after: <30 days ago>,
  order: "viewCount")`, then `list_comment_threads(video: <id>, search_terms: <pain phrase>)` on the top
  3 to hear the audience in their own words.
- **Support chats**: Crisp `list_conversations(website_id)` → `get_conversation_messages` for
  recurring questions (themes only, never quoted publicly; the `website_id` is in `brain/contracts/crm-layer`).

Write `brain/evidence/social/<YYYY-MM-DD>-listening`:
- Complaints (with links), requests, excitement, recurring questions
- **Threads where we can genuinely help**: link + a draft reply that answers the question
  first, mentions the product only if directly relevant, and discloses affiliation. The
  user posts these themselves. On Reddit especially, a useful answer from a real person beats any
  ad, and a spammy one gets you banned.

## Steps — hooks

### 1. Inputs

Read `brain/brand/founder-opinions`, `brain/brand/voice`, `brain/evidence/customer-language/latest`,
the latest listening digest, and `brain/evidence/social/hook-results` (what won before). For
an ID, also read `brain/campaigns/<ID>`.

Pull recent performance to learn the account's baseline:
- **LinkedIn**: `list_organizations` may return several Pages. Pick the one matching the brand,
  or ask. `get_organization_posts` skips sponsored posts, so page with `next_start` until you have
  ~30 organic posts or run out. Posts already carry stats, so call `get_post_statistics` only for
  posts missing them. LinkedIn's engagement rate counts clicks and is wild on tiny reach, so set a
  floor (e.g. ≥200 impressions) before using a post in the baseline.
- **X**: `get_me` → `get_user_posts` (`exclude_replies: true`) → `get_posts` with `include_private_metrics: true`
  **only for post ids from the last 30 days** (private metrics don't exist for older posts). Then clean the baseline,
  because one promoted post with millions of impressions makes the median meaningless:
  - **Promoted posts:** X Organic has no promoted flag. If `X_Ads` is connected, `tool_list_ad_accounts` →
    `tool_get_promoted_tweets` with `limit: 1000` (the default 100 truncates silently; if the count equals
    the limit, re-query) and drop every post whose id matches a promoted `tweet_id`. Without X Ads, say
    the baseline may include promoted posts.
  - **Self-thread replies:** `exclude_replies` still returns them, so drop posts whose `in_reply_to_user_id`
    equals `get_me`'s `id`.

- **YouTube**: `get_channel_performance(channel, published_after: <90 days ago>)` gives cadence and
  median views server-side. `list_channel_videos` + `get_videos` for per-video views, likes and comments.
  Shorts and long-form videos have different baselines, so split them by duration.

Use smaller n if that's all there is, and state n next to every baseline.

### 2. Draft the batch

Ten posts by default, spread across formats that scale without a face:

| Format | Built from |
|--------|------------|
| Founder take | One opinion from founder-opinions, kept spiky |
| Customer-words post | A top language cluster, quoted |
| Worked example | Real numbers (only numbers the business has verified) |
| Carousel / document | A list-shaped idea (use `/li-carousel` if installed) |
| Myth | A category belief that's wrong |
| Question / poll | An open question from listening |
| Short video script | A hook that won as text, recut as a 30–45 s YouTube Short / Reel (script + shot list) |

Each post gets a `hook_id` (`<ID or ORG>_<angle>_<format>_h<n>`) and a tracking link with
`utm_campaign=<id>_<slug>&utm_content=<hook_id>`. If `/li-human` is installed, run every draft
through it. Otherwise strip em dashes and filler words yourself.

**Label AI-generated people and scenes** wherever the platform asks.

### 3. Queue for approval

One review item (Cloud `create_ticket`, Solo `create_finding`): "[ME:social-engine] Approve: N organic posts for week of …" with every post, its platform,
the proposed slot, and the hook_id. Save the batch at `brain/evidence/social/<YYYY-MM-DD>-batch`.
For `hooks <ID>`, also write `## Social hooks` in `brain/campaigns/<ID>`: the hook_ids, formats (slugs
from the shared list in `/campaign-ledger`) and a link to the batch node.

## Steps — schedule

Only for posts the user explicitly approved in this session. Show the final list and ask
once: "Schedule these N posts?" Then:
- LinkedIn: `schedule_post` (`author: "me"` or the Page URN, `scheduled_for` ISO with offset)
- X: **X Organic has no scheduling tool.** Either post at the approved time on the user's
  instruction (`create_post`/`create_thread`), or leave the post as a copy-ready block (or schedule a
  Claude Code `/schedule` run that posts it, if the user wants that).
- YouTube: there's no upload tool, so deliver the script and shot list for the user to film and upload.

Confirm with `list_scheduled_posts`. Never publish anything that wasn't approved.

## Steps — results

After 3–7 days, pull stats for each `hook_id` (LinkedIn `get_post_statistics`, X `get_posts`, YouTube `get_videos`).
If no posts carry hook_ids yet (first run), report the baseline plus the top and bottom organic posts
of the last 30 days, with a guess at why, and say hook tracking starts with the next batch.
Compare each post to the account's own baseline (median of up to 30 organic posts from the **last
90 days**, with n stated; older posts make the baseline meaningless), not to vanity numbers:

```
Hook results — week of YYYY-MM-DD
Baseline (median): LinkedIn 1,450 impr · 2.1% eng | X 820 impr · 1.4% eng
| hook_id | Platform | Impr vs base | Eng. rate | Link clicks | Verdict |
🏆 Promote to paid: <hook_ids ≥2× baseline on engagement AND clicks>
```

X `url_link_clicks` is null on posts without a link, so the clicks half of that rule can't fire there. For
link-less X posts, use engagements + `user_profile_clicks` as the clicks signal and say so in the table.

Append winners and losers to `brain/evidence/social/hook-results` with one line on *why* each
probably won. For each winner, file one ticket: "[ME:social-engine] Promote: <hook_id> → paid test", which hands
over to `/creative-engine <ID>` with the winning hook as concept #1.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **A human approves every post.** Draft freely and publish nothing without a yes.
2. **Founder and customer words over generic content.**
3. **Help first in communities.** Disclose affiliation, never astroturf, never auto-post replies.
4. **Compare to the account's own baseline.**
5. **Winners graduate to paid.** That's the whole point of the test kitchen.
