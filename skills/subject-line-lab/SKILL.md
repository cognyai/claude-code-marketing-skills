---
name: subject-line-lab
description: Mine your actual subject-line history from Klaviyo / Mailchimp / Rule / Get a Newsletter, find the patterns that work for YOUR list, and generate tuned candidates
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter]
user-invocable: true
argument-hint: "[campaign topic]"
allowed-tools:
  # Cogny Cloud (aggregated) namespace
  - mcp__cogny__klaviyo__*
  - mcp__cogny__mailchimp__*
  - mcp__cogny__rule__*
  - mcp__cogny__get_a_newsletter__*
  - mcp__cogny__create_finding
  - mcp__cogny__write_context_node
  - mcp__cogny__read_context_node
  # Cogny Solo / Lite (per-ESP direct) namespace
  - mcp__klaviyo__*
  - mcp__mailchimp__*
  - mcp__rule__*
  - mcp__get_a_newsletter__*
  - Bash
  - Read
  - Write
---

# Subject Line Lab

Stop A/B testing blind. This skill reads **your actual last 100+ sends**, finds the subject-line patterns that correlate with open rate on *your* list, and generates 20 tuned candidates for your next campaign.

**Requires:** Cogny MCP + a connected ESP (Klaviyo, Mailchimp, Rule, or Get a Newsletter). [Sign up](https://cogny.com)

## Usage

`/subject-line-lab` — mine patterns and generate generic candidates
`/subject-line-lab "Black Friday doors open"` — mine patterns and generate candidates for a specific campaign topic

## Prerequisites Check

Detect which ESP is connected. Check **both** namespaces (Cloud-aggregated via `mcp__cogny__<svc>__*` and Solo/Lite per-ESP via `mcp__<svc>__*`):

- Klaviyo → `mcp__cogny__klaviyo__*` or `mcp__klaviyo__*`
- Mailchimp → `mcp__cogny__mailchimp__*` or `mcp__mailchimp__*`
- Rule → `mcp__cogny__rule__*` or `mcp__rule__*`
- Get a Newsletter → `mcp__cogny__get_a_newsletter__*` or `mcp__get_a_newsletter__*`

If none are connected:

```
This skill requires a connected ESP via Cogny MCP.
Connect Klaviyo, Mailchimp, Rule, or Get a Newsletter at https://cogny.com
```

If multiple are connected, prompt the user which one to analyze (or analyze all, labeled).

## ESP tool adapter

Each ESP exposes subject-line history differently. Use the right tool per connected service:

| ESP | Send history tool | Notes |
|-----|-------------------|-------|
| Klaviyo | `list_campaigns` (channel=email) then `get_campaign` | Tools are bare-named. Use `list_events` for deeper open/click metrics. |
| Mailchimp | `tool_list_reports` then `tool_get_report` | Reports are the source of truth for opens/clicks per send. |
| Rule | `tool_list_campaigns` then `tool_get_campaign_statistics` | Statistics tool returns opens/clicks/bounces. |
| Get a Newsletter | `tool_list_sent` then `tool_get_sent` and `tool_get_report` | "Campaigns" don't exist as an object — iterate `list_sent` for subject+date, `get_report` per send for metrics. |

## Steps

### 1. Pull send history
For the connected ESP, pull the last **100 campaign sends** (or as many as available). For each, capture:
- Subject line
- Preheader (if available)
- Send date + time (recipient local time if available)
- Recipient count
- Unique opens → open rate
- Unique clicks → CTR
- Segment / list name
- Campaign type (promo, newsletter, announcement, transactional-adjacent)

Skip transactional sends and automated flow emails — they distort the signal. Focus on broadcast campaigns.

### 2. Compute baseline
- **Median open rate** across the sample
- **Mean open rate** (flag skew if mean ≠ median by >20%)
- **Sample size warning** — if <30 sends, warn the user: "small sample, patterns may be noise"

### 3. Extract subject-line features
For each subject line, tag these features (use keyword/regex heuristics — no ML needed):

**Structural:**
- Length (chars): <30 / 30-50 / 50-70 / >70
- Word count
- Title Case / Sentence case / ALL CAPS / lowercase
- Ends in `?` / `!` / `.` / no punctuation

**Content:**
- Contains emoji (count, type)
- Contains number / digit
- Contains `%` or `$` or currency (promo signal)
- Contains personalization token (`{{ first_name }}`, `[Firstname]`)
- Question vs statement vs command
- First-person ("I", "we", "my") vs second-person ("you", "your")
- Urgency words: "today", "tonight", "last chance", "ends", "hours", "don't miss"
- FOMO / scarcity: "only", "limited", "few left", "selling fast"
- Curiosity gap: starts with "why", "how", "the truth about", "what I learned"
- Benefit-led: leads with a noun describing an outcome
- Social proof: "customers", "members", a number of people

**Temporal:**
- Day of week sent
- Hour of day (bucketed: early morning / morning / midday / afternoon / evening / late)

### 4. Compute lift per feature
For each feature, compute:
- **Count in sample**
- **Mean open rate when feature is present**
- **Mean open rate when feature is absent**
- **Lift** (% difference vs non-feature baseline)
- **Significance note** — flag as "strong" if n≥10 in both groups and lift is ≥10% relative; "weak" otherwise

Rank features by absolute lift.

### 5. Identify winning patterns

Output the top 5 **positive** patterns and top 3 **negative** patterns with specific numbers:

```
Patterns that worked for your list (last 100 sends):

🟢 WINNERS
1. Subject lines ending in "?" → 34% open rate vs 21% baseline (+62%, n=14 strong)
2. Subject lines with numbers → 29% open rate vs 21% (+38%, n=22 strong)
3. Length 30-50 chars → 27% open rate vs 19% (+42%, n=31 strong)
4. First-person voice ("I", "we") → 26% open rate vs 22% (+18%, n=18 strong)
5. Sent Tue 09:00-11:00 → 28% open rate vs 22% (+27%, n=12 weak)

🔴 DRAGS
1. ALL CAPS words → 14% open rate vs 23% (-39%, n=8 weak)
2. Emoji at start → 18% open rate vs 24% (-25%, n=11 strong)
3. Urgency words ("last chance", "today only") → 16% open rate vs 22% (-27%, n=9 weak)

Your best historical subject: "<actual subject>" at <open rate>% (<date>)
Your worst: "<actual subject>" at <open rate>% (<date>)
```

### 6. Generate tuned candidates

If a campaign topic was provided, generate **20 subject line candidates** that follow the winning patterns and avoid the drags. If no topic was provided, generate 20 generic promo/newsletter candidates using your patterns.

Format:

```
Candidates for: "<topic>"
(tuned to: ends-in-?, has-number, 30-50 chars, first-person voice)

Preheader recommendation: 85-100 chars, don't duplicate subject, extend the hook.

1. "What <specific number> of our customers asked last week?" (52 chars)
   Preheader: "We pulled the top 5 questions and answered them in one place — you'll recognize #2."
2. ...
20. ...

──
A/B test plan:
- Primary variant: candidate #<N> (leans hardest into top pattern)
- Challenger: candidate #<M> (different angle to avoid pattern overfitting)
- Hold-out: your house-style baseline subject
Segment: X% / Y% / Z%
```

### 7. Persist patterns as context

Save the winning-pattern summary to Cogny's context tree for future sessions:

```json
{
  "path": "insights/email/subject-line-patterns",
  "body": "<the top 5 winners + top 3 drags, with numbers and date range>"
}
```

### 8. Create a finding

If the analysis surfaces a clear actionable insight (e.g., "50% of recent sends use emoji-at-start which is actively hurting opens"), create a finding:

```json
{
  "title": "Emoji-at-start subjects are tanking opens (-25% vs baseline)",
  "body": "11 of last 100 sends started with emoji. Avg open 18% vs 24% non-emoji baseline. Recommend: move emoji to mid-subject or drop entirely on next 10 campaigns and re-measure.",
  "action_type": "subject_line_optimization",
  "expected_outcome": "Lift average open rate by 2-4 pp",
  "estimated_impact_usd": 0,
  "priority": "medium"
}
```

## Notes

- Lift numbers are **correlational**, not causal — always surface sample size and flag weak signals.
- If the user's list is <5,000 subscribers, opens are noisy. Recommend 2-week lookback minimum and warn.
- Apple MPP inflates open rate for iOS Mail users. If open rate looks uniformly high (>40%+ across everything), the signal is degraded — note this and lean on CTR as a secondary metric.
