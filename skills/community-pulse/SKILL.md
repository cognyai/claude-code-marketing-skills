---
name: community-pulse
description: Weekly read on Discord community health — joins, active channels, top contributors, themes, and unanswered questions
version: "1.0.0"
author: Cogny AI
platforms: [discord]
user-invocable: true
argument-hint: ""
allowed-tools:
  # Discord MCP read tools (via Cogny MCP Proxy)
  - mcp__cogny__discord__get_current_user
  - mcp__cogny__discord__list_guilds
  - mcp__cogny__discord__get_guild
  - mcp__cogny__discord__list_guild_channels
  - mcp__cogny__discord__get_channel
  - mcp__cogny__discord__list_guild_members
  - mcp__cogny__discord__get_channel_messages
  # Findings (premium / cloud-tier)
  - mcp__cogny__create_finding
  - WebFetch
  - Read
  - Write
---

# Community Pulse — Discord weekly digest

Surface the signal in a busy Discord server. Who joined, which channels are
hot, who's contributing, what's getting asked, and what's left hanging — in
one digest you can act on in 15 minutes.

## Usage

`/community-pulse` — weekly digest of the connected Discord server.

Pass a guild ID if the bot is in more than one server:

`/community-pulse 123456789012345678`

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

Call `mcp__cogny__discord__get_current_user` to confirm the bot identity.
If this fails with an authentication error, the bot token in the cogny
warehouse is bad — reconnect at `app.cogny.com/warehouse/<id>/settings/api`.

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

1. Call `get_channel_messages(channel_id, limit=100)` — most recent batch.
2. From that batch:
   - Count messages with `timestamp` in the last 7 days
   - Count messages in days 8–14 (for the WoW)
   - Unique authors this week
   - Most-recent message timestamp
3. If the earliest message in the batch is still within 7 days, paginate one
   more page with `before=<earliest message id>`. Stop after 200 messages
   per channel.
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
   / concerning).
4. Flag **unanswered questions** — messages ending in "?" with no replies in
   the sampled thread. These are unmet needs.

If `content` is empty everywhere, skip this step and write a one-line note:
*"Topic analysis unavailable — enable Message Content Intent on the bot in
the Discord Developer Portal."*

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
- #help  "How do I …" — @member, 2 days ago

Recommended Actions
1. Welcome @member1, @member2, @member3 in #general
   Why: 3 lurkers became active this week
   Owner: community manager · Done when: posted by EOW
2. …
```

### 10. Record findings (cloud tier only)

If `mcp__cogny__create_finding` is available, file each recommended action
as a finding so they show up in the warehouse's action queue:

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
   Don't paste full message bodies unless the message is already pinned or
   the author is the workspace owner.
6. **Read-only by default.** Do not call `send_message` (it's not in the
   allowed-tools list). The digest is for the user to act on, not for the
   bot to broadcast.
7. **Trends over snapshots.** Single-week numbers are noise; week-over-week
   deltas are signal. Always include the comparison.
8. **Actions over observations.** Step 8 is the point of the skill. If you
   wrote 8 paragraphs of analysis without 3 clear next steps, you over-
   analyzed — cut.
