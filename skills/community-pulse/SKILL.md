---
name: community-pulse
description: Weekly read on community health — Discord joins, active channels, top contributors, themes and unanswered questions, plus Crisp support conversations and YouTube comments when connected
version: "1.1.2"
requires: cogny-mcp
author: Cogny AI
platforms: [discord, crisp, youtube]
user-invocable: true
argument-hint: ""
allowed-tools:
  # Discord MCP read tools (via Cogny MCP Proxy)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Discord__get_current_user
  - mcp__cogny__mcp__Discord__list_guilds
  - mcp__cogny__mcp__Discord__get_guild
  - mcp__cogny__mcp__Discord__list_guild_channels
  - mcp__cogny__mcp__Discord__get_channel
  - mcp__cogny__mcp__Discord__list_guild_members
  - mcp__cogny__mcp__Discord__get_channel_messages
  # Crisp support conversations (read-only)
  - mcp__cogny__mcp__Crisp__get_website_statistics
  - mcp__cogny__mcp__Crisp__list_conversations
  - mcp__cogny__mcp__Crisp__get_conversation
  - mcp__cogny__mcp__Crisp__get_conversation_messages
  # YouTube comments (read-only)
  - mcp__cogny__mcp__YouTube__get_channel
  - mcp__cogny__mcp__YouTube__list_channel_videos
  - mcp__cogny__mcp__YouTube__list_comment_threads
  - mcp__cogny__list_integrations
  # Cogny bookkeeping writes: create_ticket (Cloud) / create_finding (Solo). No integration write tools are pre-approved.
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
  - WebFetch
  - Read
  - Write
---

# Community Pulse — weekly community digest

Surface the signal in a busy Discord server. Who joined, which channels are
hot, who's contributing, what's getting asked, and what's left hanging — in
one digest you can act on in 15 minutes.

## Works with

| Job | Primary | Also answers it | What differs |
|-----|---------|-----------------|--------------|
| Members, joins, channel activity, contributors | Discord | — | Only Discord has membership and channels |
| Themes and unanswered questions | Discord (`get_channel_messages`) | Crisp (`list_conversations`, `get_conversation_messages`), YouTube (`list_comment_threads`) | Crisp is 1:1 support, so "unanswered" means `filter_state: "unresolved"`; YouTube marks `owner_replied` per thread |
| Volume trend | Discord message counts | Crisp `get_website_statistics`, YouTube comment counts | Report each source in its own row; never add them up |

Discord is the primary source and drives steps 2-6. Crisp and YouTube are optional extra sources (step 7b). If Discord isn't connected but one of the others is, run steps 7, 7b, 8 and 9 for that source only and say so in the header.

## Usage

`/community-pulse` — weekly digest of the connected Discord server (plus Crisp/YouTube if connected).

Pass a guild ID if the bot is in more than one server:

`/community-pulse 123456789012345678`

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Community Pulse needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Discord (plus Crisp or YouTube if you use them).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

If Cogny is connected but Discord isn't, say "connect Discord in Cogny" (Crisp and YouTube alone still give a partial digest).

## Prerequisites

The Discord MCP needs **two privileged intents** enabled in the Discord
Developer Portal → Bot tab → Privileged Gateway Intents:

- **Server Members Intent** — without it, `list_guild_members` returns only
  the bot itself.
- **Message Content Intent** — without it, `get_channel_messages` returns
  authors and timestamps but every `content` field comes back empty.

If the report comes back with a 1-element member list or empty message
content, this is almost always why. The skill flags the gap loudly at the top
of the output rather than silently producing misleading numbers.

The bot also needs **View Channel + Read Message History** in each channel
you want analysed — these are channel-level permissions, not intents.

## Steps

### 1. Sanity check the connection

Call `mcp__cogny__list_integrations` to see which of Discord, Crisp and YouTube are connected. Its
`health_status` misses revoked tokens, so make one cheap read per connected source: Discord
`get_current_user` (also confirms the bot identity), Crisp `get_website_statistics`, YouTube `get_channel`.
A 401, `Forbidden` or scope error = 🔴 "reconnect <integration> in Cogny": name it in the header and don't retry.
For Discord that means the bot token stored in Cogny is bad: "reconnect Discord in Cogny".

If a tool you expect is missing, call `mcp__cogny__refresh_mcp_discovery` once (never loop). New tools only
load after the client reconnects, so skip that source this run and mark it ⚠ "needs reconnect".

### 2. Pick the guild

Call `list_guilds`. If exactly one guild, use it. If multiple, prefer the
guild ID passed as an argument. If none was passed and there's more than
one, list them and ask the user to specify.

Once chosen, call `get_guild(guild_id, with_counts=True)` for the baseline:

- name, owner, premium tier
- `approximate_member_count` (this is the "members" stat)
- `approximate_presence_count` (online right now)

### 3. Inventory channels

Call `list_guild_channels(guild_id)`. Bucket channels into:

- **High-signal** — channels matching `intro`, `welcome`, `feedback`,
  `support`, `showcase`, `hiring`, `general` (these usually hold the signal
  for community health)
- **Categories** — group containers (skip; they have no messages)
- **Voice / stage** — skip for the weekly digest
- **Private** — a channel is private when its `permission_overwrites` (or its parent category's) has an
  entry with `id == guild_id` that denies `VIEW_CHANNEL` (bit 1024). Per-customer channels are usually
  private. Analyse them for **counts and anonymised themes only**: never quote them, name their members, or
  list their messages in Top Themes or Unanswered Questions.

Cap the analysis at **30 channels** to bound runtime.

### 4. Member growth — last 7 days

Call `list_guild_members(guild_id, limit=1000)`, paginating with
`after=<last user id>` until exhausted or 5000 members fetched.

For each member, parse `joined_at` and bucket into:

- **This week** — joined in the last 7 days
- **Last week** — joined 8–14 days ago
- **Existing** — joined >14 days ago

Compute:

- Joins this week (count + list of names/IDs + first-day-of-week breakdown)
- Joins last week (for the WoW comparison)
- WoW change in absolute and %
- Spike call-out if a single day accounts for >40% of weekly joins

### 5. Channel activity

For each text channel from Step 3 (cap 30, prioritize high-signal):

1. Call `get_channel_messages(channel_id, limit=25)` — most recent batch. Each message carries the full
   author object, so keep `limit` at 20–25 (50 returned 55–105KB per channel in live runs). A `Forbidden` means the bot can't read that channel: list it as
   "not readable" and continue with the next one. Exclude `author.bot` and staff ids from every count,
   and exclude system messages (any `type` other than the default `0` or reply `19`, e.g. type 7 member joins,
   pins, boosts): they are not conversation.
2. From that batch:
   - Count messages with `timestamp` in the last 7 days
   - Count messages in days 8–14 (for the WoW)
   - Unique authors this week
   - Most-recent message timestamp
3. If the earliest message in the batch is still within 7 days, paginate
   with `before=<earliest message id>` (still `limit=25`). Stop after 200 messages
   per channel. For channels outside the high-signal bucket, keep only counts
   (timestamps, author ids), not message content.
4. Classify:

| Class | Criteria |
|---|---|
| Hot | ≥20 messages this week, ≥5 unique authors |
| Steady | 5–19 messages, ≥3 unique authors |
| Quiet | 1–4 messages |
| Dead | 0 this week, last activity >14 days ago |

### 6. Top contributors and lurker conversion

Aggregate the message samples from Step 5 by author across all channels:

- Total messages this week
- Channels they posted in
- Reactions received (sum of `reactions[].count` per message)

Then surface:

- **Top 5 contributors** — by message volume
- **Newly active members** — joined >30 days ago, ≥3 messages this week,
  zero messages in days 8–14. These are lurkers who just turned the corner.
- **At-risk regulars** — ≥10 messages in days 8–14, ≤2 messages this week.
  Going quiet — worth a check-in.

### 7. Topics and themes

If `content` is non-empty (Message Content Intent is on):

1. Group messages by channel and read the actual text.
2. Identify the **3 dominant topics**. A topic is dominant if it shows up in
   ≥5 messages or in ≥2 channels.
3. For each topic: one-sentence summary, 1–2 representative quotes
   (anonymize as "@member said: …"), sentiment (positive / neutral / mixed
   / concerning). Quotes come from public channels only; private channels
   (step 3) feed the theme counts but are never quoted.
4. Flag **unanswered questions** (public channels only) — messages ending in "?" with no replies in
   the sampled thread. These are unmet needs.

If `content` is empty everywhere, skip this step and write a one-line note:
*"Topic analysis unavailable — enable Message Content Intent on the bot in
the Discord Developer Portal."*

### 7b. Other sources (optional, when connected)

**Crisp (support conversations).** All Crisp tools need `website_id` (the Crisp website UUID: Crisp → Settings → Website settings → Setup). Ask the user once if you don't have it.

1. `mcp__cogny__mcp__Crisp__get_website_statistics` (`website_id`) for the volume baseline.
2. `mcp__cogny__mcp__Crisp__list_conversations` (`website_id`, `page_number`, 50 per page, newest first). Keep the last 14 days; stop after 4 pages.
3. For up to 30 conversations from this week, `get_conversation_messages` (`website_id`, `session_id`). Group by topic the same way as step 7.
4. **Unanswered:** `list_conversations` with `filter_state: "unresolved"` (or `"pending"`). List those older than 24h.

**YouTube (comments on your channel).** Gate this on the tools existing, not on `list_integrations`: if YouTube
is connected but `list_comment_threads` isn't loaded, follow step 1 (refresh once, skip, mark ⚠).

1. `mcp__cogny__mcp__YouTube__list_comment_threads` with no `video`/`channel` (uses the connected channel), `order: "time"`, `max_results: 50`; page with `page_token` until comments are older than 14 days.
2. Count comments this week vs last week; group into themes as in step 7.
3. **Unanswered:** threads where `owner_replied` is false and the comment is a question. Link each with its `url`.

Merge themes across sources only when the same topic shows up in more than one (e.g. "pricing confusion" in Discord #help and in Crisp). That cross-source overlap is the strongest signal in the digest; mark it.

### 8. Recommend 3–6 actions

Each action must:

- Cite the specific signal that motivated it ("joins this week dropped 38%")
- Be doable in <30 minutes (no big strategic pivots — this is a weekly rhythm)
- Have a clear owner and a clear "done" condition

Useful action shapes:

- Welcome the newly-active members by name in #general
- Re-engage at-risk regulars with a targeted DM or @mention
- Answer unanswered questions or assign them to a mod
- Revive a Dead channel with a topical question, or archive it
- Highlight the top contributor in a weekly recap
- Feed a Hot channel's signal back to product (e.g. feature-request spike)

### 9. Output

Print the report in this shape:

```
Community Pulse — <guild-name>
Week of <YYYY-MM-DD> – <YYYY-MM-DD>

⚠️  Intent gap: Message Content Intent off — topic analysis disabled.
    (Skip this line if intents are configured.)

Pulse
- Members: 1,247 (+18 WoW · +1.4%)
- Active authors: 34 (+6 WoW)
- Total messages sampled: 412 (+71 WoW)
- Online ratio: 11% (last week 9%)

Channel Activity
| Channel        | Msgs | Authors | Status |
|----------------|------|---------|--------|
| #introductions | 28   | 19      | Hot    |
| #general       | 142  | 22      | Hot    |
| #showcase      | 8    | 5       | Steady |
| #help          | 3    | 2       | Quiet  |
| #off-topic     | 0    | 0       | Dead   |

Top Contributors
1. @member (24 messages, 31 reactions, 4 channels)
…

Newly Active (lurker → contributor this week)
- @member  joined 2026-02-14, 5 messages this week, top channel #showcase
…

At-Risk Regulars (going quiet)
- @member  was 18/wk last week → 1/wk this week, top channel #general
…

Top Themes (Message Content Intent required)
1. …

Unanswered Questions
- Discord #help  "How do I …" — @member, 2 days ago
- Crisp  "Can I export …" — unresolved 3 days
- YouTube  "Does this work with …" — on "<video title>", no owner reply

Other Sources (if connected)
| Source  | This week | Last week | Unanswered |
|---------|-----------|-----------|------------|
| Crisp   | 41 convs  | 35        | 6          |
| YouTube | 58 comments | 70      | 9          |

Recommended Actions
1. Welcome @member1, @member2, @member3 in #general
   Why: 3 lurkers became active this week
   Owner: community manager · Done when: posted by EOW
2. …
```

### 10. Record findings

File each recommended action in the action queue. Use `create_ticket` if it exists (Cloud), otherwise
`create_finding` (Solo), mapping fields per the table in section 2 of
`../marketing-engineer/references/mcp-routing.md`. On `create_ticket`, `expected_outcome` is required,
the action type goes in `body` ("Type: community_engagement") and urgency prefixes the title. The
`create_finding` shape:

```json
{
  "title": "Welcome 3 newly-active members in #general",
  "body": "Lurkers @x, @y, @z each posted ≥3 messages this week after >30 days quiet. Acknowledge to lock them in.",
  "action_type": "community_engagement",
  "expected_outcome": "Each replies or reacts within 48h",
  "estimated_impact_usd": 0,
  "priority": "medium"
}
```

Action types for Discord:

- `community_engagement` — welcomes, mentions, reaching out to at-risk regulars
- `content_response` — answering unanswered questions, posting summaries
- `channel_management` — archiving dead channels, reorganising, permission fixes
- `intent_configuration` — re-enabling Server Members or Message Content Intent
- `bot_permission` — re-installing the bot with a wider permission set

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **One guild per run.** If the bot is in multiple, pick one and analyse it
   fully — don't dilute the report.
2. **Verify intents first.** If `list_guild_members` returns 1 row or all
   `content` fields are empty, flag it loudly at the top before any other
   numbers — the rest of the report will be misleading.
3. **Bucket from real timestamps**, not message position. Discord returns
   messages newest-first; verify each `timestamp` against the 7-day window.
4. **Respect the runtime caps** — 30 channels, 200 messages/channel, 5000
   members. The output is more useful than a complete one.
5. **Anonymize message content** — display name + first sentence is enough.
   Crisp conversations are private support chats: never show emails or full
   names from them, only the paraphrased question.
   Don't paste full message bodies unless the message is already pinned or
   the author is the workspace owner.
5b. **Never quote secrets.** If a message in any channel appears to contain a
   secret (API key, client secret, password, token pattern such as `sk_live_…`,
   `ghp_…`, `xoxb-…`, a JWT, or `password=`), never quote or paraphrase the
   value. Report "possible exposed secret in #<channel> on <date>; rotate it"
   without the value, and make it a top action.
6. **Read-only by default.** Do not call Discord `send_message` or Crisp
   `send_message_in_conversation` / `update_conversation_state` (none are in
   the allowed-tools list). The digest is for the user to act on, not for the
   bot to broadcast. If the user asks for a reply to be posted, show the draft
   and ask first.
7. **Trends over snapshots.** Single-week numbers are noise; week-over-week
   deltas are signal. Always include the comparison.
8. **Actions over observations.** Step 8 is the point of the skill. If you
   wrote 8 paragraphs of analysis without 3 clear next steps, you over-
   analyzed — cut.
