---
name: drop-off-rescue
description: Find contacts stalled at funnel stages (abandoned cart, signed-up-but-no-trial, trial-but-no-convert), draft stage-appropriate re-engagement emails, and schedule sends via your ESP — with dedupe so weekly reruns never double-send
version: "1.0.0"
author: Cogny AI
platforms: [klaviyo, mailchimp, rule, get-a-newsletter]
user-invocable: true
argument-hint: "[weekly|audit|free]"
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
  - WebFetch
  - Bash
  - Read
  - Write
---

# Drop-off Rescue

Push stalled funnel contacts to the next step. This skill finds people who signed up but didn't convert, drafts stage-appropriate re-engagement emails, and (with an ESP MCP connected) schedules the send after explicit confirmation. Re-runnable weekly without double-sending — the skill tracks what was already sent per stage and skips contacts still inside their cooldown window.

**Works in three modes:**
- `cloud` — Cogny MCP + ESP MCP: full automation, cross-ESP dedupe, findings
- `solo` — ESP MCP only: tag-based dedupe, per-ESP automation
- `free` — no MCP: pasted CSV of stalled contacts, draft-only output (you send manually)

## Usage

```
/drop-off-rescue              # weekly rerun — default
/drop-off-rescue weekly       # same
/drop-off-rescue audit        # read-only: report stalls + what would be sent, write nothing
/drop-off-rescue free         # no MCP — paste CSV of stalled contacts
```

Designed to be scheduled weekly via `/loop` or `/schedule`. On reruns, already-nudged contacts are skipped; newly-stalled contacts are picked up; contacts that progressed get celebrated in the output.

## Step 1 — Mode detection

Probe both MCP namespaces:

1. If `mcp__cogny__<svc>__*` tools are present for at least one ESP → **cloud** mode (and record that ESP as connected).
2. Else if `mcp__<svc>__*` tools are present for at least one ESP → **solo** mode.
3. Else → **free** mode.

If the argument is `free`, force free mode regardless of what's connected.

If multiple ESPs are connected, ask the user which one to run against (or offer to run all and cross-dedupe in cloud mode).

## Step 2 — Canonical funnel stages

The skill works against a canonical stage taxonomy. The user can extend it, but these slugs drive tag names, campaign naming, and dedupe state — keep them stable across runs.

**E-commerce:**
| Slug | Meaning | Typical stall |
|------|---------|---------------|
| `browse-abandoned` | Viewed product, never added to cart | 1–3 days |
| `cart-abandoned` | Added to cart, never checked out | 1–2 days |
| `checkout-abandoned` | Started checkout, didn't submit | hours–1 day |
| `post-first-order-silent` | Made first order, no engagement since | 14–30 days |

**SaaS / trial funnel:**
| Slug | Meaning | Typical stall |
|------|---------|---------------|
| `signup` | Created account, did nothing | 1–3 days |
| `no-channel` | Signed up, no data source / integration connected | 3–7 days |
| `no-trial` | Connected a channel, hasn't started the free trial | 7 days |
| `no-client` | Trial active, hasn't connected the tool/client that uses it | 3 days |
| `no-subscription` | Trial ended, didn't convert to paid | 0–3 days after trial |
| `trial-started-inactive` | Started trial, no meaningful usage | 3–5 days |
| `trial-ended-no-convert` | Trial ended, didn't subscribe | 7 days after end |

Cogny's own Solo funnel (signup → `no-channel` → `no-trial` → `no-client` → `no-subscription`) is a good reference implementation of this taxonomy.

If the user describes a funnel with stages that don't map to these slugs, add new kebab-case slugs — just keep them stable across reruns (the slug is the dedupe key).

## Step 3 — Resolve current stage per contact

**Primary signal: ESP tags / segments.** Read contacts tagged `stage:<slug>` using the per-ESP tool:

| ESP | Read stage tag | Apply stage tag | Schedule/send |
|-----|----------------|-----------------|---------------|
| Klaviyo | `list_profiles` filtered by segment/property `stage` | `update_profile` (properties) | campaign create + schedule |
| Mailchimp | `tool_list_members` filtered by tag | `tool_update_member` (tags) | campaign schedule |
| Rule | `tool_list_subscribers` filtered by tag | `tool_add_tag_to_subscriber` | `tool_schedule_campaign` |
| Get a Newsletter | `tool_list_contacts` filtered by tag | `tool_update_contact` (tag) | `tool_send_draft` with `time_to_send` |

**Klaviyo event-derived fallback (only when `stage:cart-abandoned` tag is absent):** query `list_events` with `metric="Added to Cart"` in the last 7 days, exclude profiles who have a subsequent `Placed Order`. Write the `stage:cart-abandoned` tag back via `update_profile` so the next run is consistent.

**Conversational fallback (any ESP, when no stage tags exist at all):**

1. Ask the user: "I don't see any `stage:*` tags on your contacts. Which of these funnel stages apply to your business?" — list the canonical slugs.
2. For each picked stage, ask: "Who is on this stage? Describe the condition — e.g. `joined list > 3 days ago AND no purchase`, or `clicked email X but never visited /signup`."
3. Translate each heuristic into the ESP's available filters (list membership, tags, date ranges, clicked links) and preview the matching count.
4. Offer (under the confirmation gate in Step 7) to apply `stage:<slug>` tags now, so future runs are fully automated.

## Step 4 — Already-sent detection (the core mechanism)

Weekly reruns must not re-send the same stage email to the same contact. The skill uses a **three-layer hybrid**:

### Layer 1 — contact tag (primary, all modes with an ESP connected)

On every successful send, write three tags to the recipient:

- `rescue-sent:<slug>:<YYYY>-W<WW>` — append-only; one per week nudged
- `rescue-last-stage:<slug>` — overwritten; always reflects the latest stage nudged (enables stage-advancement detection in one read)
- `rescue-last-sent:<YYYY-MM-DD>` — overwritten; used for cooldown math and the global 7-day anti-fatigue rule

Why tag-based primary: works in solo mode without a context tree, survives cross-machine usage, all four ESPs expose a tag-write tool, debuggable by a human in the ESP UI, bulk-clearable if something goes wrong.

### Layer 2 — ESP campaign-name convention (fallback)

Every rescue campaign is named exactly:

```
drop-off-rescue / <stage-slug> / <YYYY>-W<WW> / <variant A|B>
```

On rerun, if a contact's tags were stripped (manual edit, sync tool), `list_campaigns` / `tool_list_campaigns` / `tool_list_sent` in the last 35 days is scanned for matching names. Recipients are cross-referenced via the per-ESP report tool (`list_events`, `tool_get_report`, `tool_get_campaign_statistics`, `tool_get_report`).

**Deliberately no markers in subject or preheader** — the user-visible inbox copy stays clean.

### Layer 3 — Cogny context-tree log (cloud mode only)

Write on every send:

```
insights/drop-off-rescue/<slug>/<sha256(email)[:12]>/last-sent
  → { "week": "2026-W17", "variant": "A", "esp": "klaviyo", "ts": "2026-04-24T10:00Z" }
```

Read on the next run. This layer catches cross-ESP duplication — the same contact living in both Klaviyo and Mailchimp under the same org won't get two nudges in the same week.

### Dedupe decision

A contact is classed **"already nudged at current stage within cooldown"** if **any** of the three layers reports a hit inside the cooldown window. Cooldown defaults (printed in output, user-overridable):

| Stage | Cooldown |
|-------|----------|
| `cart-abandoned`, `checkout-abandoned` | 7d |
| `browse-abandoned`, `signup`, `no-channel` | 14d |
| `no-trial`, `no-client`, `no-subscription`, `trial-started-inactive` | 21d |
| `post-first-order-silent`, `trial-ended-no-convert` | 30d |

## Step 5 — Classify every contact (the weekly loop)

For each stage, read the full `stage:<slug>` cohort, then classify each contact:

| Class | Condition | Action this run |
|-------|-----------|-----------------|
| **New stall** | On `stage:<slug>` now, no `rescue-sent:<slug>:*` ever | Eligible — variant A |
| **Cooldown skip** | Has `rescue-sent:<slug>:<week>` inside the stage's cooldown window | Skip, count as "cooldown-skipped" |
| **Re-stall** | Past cooldown, still on `stage:<slug>`, ≤2 prior rescue sends at this stage | Eligible — variant B (tone shift) |
| **Progressed** | `rescue-last-stage` is an earlier stage than the current stage tag | Celebrate in output; nudge at new stage |
| **Regressed** | `rescue-last-stage` is a later stage than the current stage tag | Flag as anomaly, don't auto-nudge (data issue) |
| **Exhausted** | 3 prior rescue sends at this stage without progression | Apply `rescue-exhausted:<slug>`, exclude until stage changes |
| **Exited** | No stage tag at all, but has `rescue-last-stage` | Clear all `rescue-*` tags in cleanup pass |

**Hard caps (enforced regardless of per-stage cooldowns):**

- **3 nudges max per contact per stage** before they go to `rescue-exhausted:<slug>`.
- **Max one rescue email per contact per rolling 7 days across all stages.** If a contact would be hit for two stages in one week, emit only the higher-priority stage (priority order: `cart-abandoned` > `checkout-abandoned` > `browse-abandoned` > `signup` > `no-channel` > `no-trial` > `no-client` > `no-subscription` > activation-stages > `post-first-order-silent` > `trial-ended-no-convert`) and defer the other.

## Step 6 — Draft emails per stage

For every stage with ≥1 eligible contact, draft **two variants**:

- **Variant A** — direct, short, outcome-led. For first-time nudges.
- **Variant B** — value-led, longer, addresses likely objections. For re-stalls (second+ nudge at the same stage).

For every variant produce:

```
Stage: <slug>
Variant: A | B
Subject:    <≤55 chars, in brand voice>
Preheader:  <85–100 chars, extends subject, never repeats it>
Body:       <markdown>
Primary CTA: <label> → <URL with UTM: utm_source=email&utm_medium=rescue&utm_campaign=<slug>-<YYYY>WWW&utm_content=<A|B>>
```

**Tone guidance per stage:**

| Stage | Variant A tone | Variant B tone |
|-------|----------------|----------------|
| `cart-abandoned` | Quick, helpful, "still thinking about X?" | Urgency + social proof + small incentive |
| `checkout-abandoned` | "Technical hiccup? We saved your cart." | Offer + friction-remover (guest checkout, Apple Pay) |
| `browse-abandoned` | Curiosity, reference the viewed category | Content-led (buying guide, comparison) |
| `signup` / `no-channel` | Helpful, "the one step that unlocks it" | Founders' note, reply-to-me tone |
| `no-trial` / `no-client` / `no-subscription` | Clear next action + short how-to | Objection-handling ("what's holding you back?") |
| `post-first-order-silent` | Thank-you + relevant follow-up | Cross-sell + reminder of brand value |
| `trial-started-inactive` | "Here's the fastest win you can get in 5 min" | Use case + customer example |
| `trial-ended-no-convert` | "Any reason this didn't land?" | Small discount + plan recommendation |

Use the brand's actual voice — if the user has a brand URL, WebFetch it first to pick up tone. No "Dear Valued Customer" filler. One primary CTA per email.

## Step 7 — Confirmation gate (before any write)

**No MCP write tool fires before the user explicitly approves.** This applies to both tag applications (Step 3 fallback) and email sends / schedules.

For every stage that has eligible contacts, print this block verbatim and wait:

```
About to send via <ESP>. Nothing has been sent yet.

Stage:            <slug>       (<N> eligible)
Cooldown applied: <d>d         (<M> skipped as already-nudged)
Exhausted:        <K>          (hit 3-nudge cap — excluded)
Variant:          A | B        (<label — e.g. "first nudge" or "re-stall, value-led">)
Schedule:         <ISO timestamp, recipient-local>  |  immediate
Campaign name:    drop-off-rescue / <slug> / <YYYY>-WWW / <A|B>

Dry-run preview (first 3 recipients):
  1. <email>    subject: <rendered>
  2. <email>    subject: <rendered>
  3. <email>    subject: <rendered>

State writes on send:
  - tag rescue-sent:<slug>:<YYYY>-WWW  → <N> contacts
  - tag rescue-last-stage:<slug>       → <N> contacts (overwrite)
  - tag rescue-last-sent:<YYYY-MM-DD>  → <N> contacts (overwrite)
  - context-tree log (cloud mode)      → <N> entries

Reply with:
  send           → execute now via ESP MCP
  schedule <ts>  → queue for that recipient-local time
  variant B      → switch variant and reprint this block
  skip           → don't send, but log a "no-send" finding and continue
  cancel         → abort everything, no writes
```

If the ESP lacks native scheduling (today: none of the four, but guard for future gaps), return the draft plus a suggested `at`/cron string the user can run themselves.

**Before scheduling, always check for flow conflicts:** read `list_flows` / `tool_list_automations` / `tool_list_journeys`. If a native flow already targets a segment equivalent to the current stage, warn:

```
⚠️  Heads up — a native <ESP> flow already targets this segment:
    "<flow name>"  (last modified <date>, status: <active|paused>)

    Running rescue alongside it risks double-touching the contact. Options:
      [1] Pause rescue for this stage, let the native flow do the work
      [2] Pause the native flow, run rescue this week only
      [3] Proceed anyway (document the overlap)

    Which?
```

Get a Newsletter has no flow object, so this check is skipped there.

## Step 8 — Consent & suppression guards

Before any send:

- **Drop contacts with `consent:marketing = false`** (or the ESP equivalent: unsubscribed, cleaned, bounced, or on a suppression list).
- **Drop contacts in an active `rescue-exhausted:<slug>` state**.
- **Drop contacts with a `do-not-contact` / `gdpr-suppressed` tag** regardless of stage.
- In free mode, the pasted CSV must include a `consent` column; rows with `false`/`no`/`0` are dropped with a console warning.

If >10% of the eligible list is dropped for consent reasons, surface this at the top of the output — it usually means the user's list hygiene needs attention and a `/revenue-audit` or `/winback-engine` run first.

## Step 9 — Free mode (no MCP)

Triggered when neither `mcp__cogny__*` nor any `mcp__<esp>__*` resolves, or when the user passes `free` explicitly.

1. Ask the user to paste a CSV with columns: `email,stage,stalled_since,consent` (stage must be a slug from Step 2; `stalled_since` is ISO date; `consent` is `true`/`false`).
2. Ask for brand name + one-line brand voice (same lightweight discovery as `/welcome-series`). Optionally ask for a brand URL to WebFetch.
3. Draft both variants per stage.
4. Output a manual-send bundle:
   - One `.csv` of eligible contacts per stage (filtered for consent)
   - Drafted email copy (markdown + HTML) per variant per stage
   - A copy-paste subject/preheader table
5. **No state is persisted.** The user owns dedupe — output explicitly calls this out.
6. End with the upsell:

```
───────────────────────────────
Ready to stop managing this by hand?

Connect your ESP via Cogny MCP and the next run will:
  • Dedupe against what you've already sent
  • Apply rescue-sent:* tags automatically
  • Schedule the send directly in your ESP after your confirmation

→ https://cogny.com
───────────────────────────────
```

## Step 10 — Output format

```
Drop-off rescue — <ESP or "free mode"> — week <YYYY>-W<WW>
Mode: cloud | solo | free

Funnel movement since last run:
  new stalls:        +<N>
  progressions:      +<N>     (<stage_a> → <stage_b>: N; <stage_c> → <stage_d>: N)
  regressions:       <N>
  exited funnel:     <N>
  newly exhausted:   <N>

Consent drops: <N>  (<pct>% of eligible — <OK | run /revenue-audit>)

──────────────────────────────────────────────────────
Stage: cart-abandoned
  Eligible: <N>   Cooldown-skip: <M>   Exhausted: <K>
  Suggested variant: A     Send window: Tue–Thu, 10am recipient-local

  Top 10 eligible contacts:
  | email               | stalled since | prior nudges |
  |---------------------|---------------|--------------|
  | ...                 | 2026-04-21    | 0            |

  Email draft — variant A:
    Subject:    ...
    Preheader:  ...
    Body:       ...
    CTA:        [label] → <URL with UTM>

  Email draft — variant B:
    ...

  [confirmation block from Step 7]

──────────────────────────────────────────────────────
Stage: no-channel
  ...
```

One such block per stage with eligible contacts. Stages with zero eligible (everyone cooldown-skipped or exhausted) get a one-line summary instead of a full block.

## Step 11 — Findings (cloud mode)

For each stage with eligible contacts, write a finding:

```json
{
  "title": "Drop-off rescue: <N> contacts stalled at <stage-slug>",
  "body": "<N> contacts on stage:<slug> are past their cooldown. Variant <A|B> drafted; send scheduled for <ts or 'awaiting approval'>. Previous week: <M> contacts progressed out of this stage after rescue.",
  "action_type": "rescue_campaign",
  "expected_outcome": "<e.g. 'Expect 5–10% of cart-abandoners to complete checkout within 72h'>",
  "estimated_impact_usd": <number_or_null>,
  "priority": "<high|medium|low>"
}
```

`estimated_impact_usd` is computed only when Klaviyo's `list_events` gives AOV × realistic reactivation rate (5–10% for cart stages, 2–5% for SaaS stages). For other ESPs without purchase data, set to `null` and note "engagement uplift only."

Persist the weekly summary under `insights/drop-off-rescue/<YYYY>-W<WW>/summary` so next run can diff.

## Step 12 — End-of-run tag inventory

Final output section — gives the user visibility into state sprawl:

```
rescue-* tag inventory on <ESP>:
  rescue-sent:cart-abandoned:2026-W17   → 42 contacts
  rescue-sent:no-channel:2026-W17       → 18 contacts
  rescue-last-stage:cart-abandoned      → 67 contacts
  rescue-exhausted:no-channel           → 4 contacts
  rescue-last-stage:no-channel          → 22 contacts
  (... older weeks)

Cleanup: reply "clear weeks before 2026-W14" to bulk-remove old rescue-sent:* tags.
```

## Notes

- **Only Klaviyo exposes cart/order events** through the cogny-mcp-proxy. `cart-abandoned` / `checkout-abandoned` / `post-first-order-silent` stages on Mailchimp, Rule, or Get a Newsletter rely entirely on tag-driven stage resolution — the user must be tagging contacts from their own e-com data.
- **Get a Newsletter has no flow/automation object.** The Step 7 flow-conflict check is skipped. Rescue is always scheduled as individual drafts via `tool_send_draft` with `time_to_send`.
- **Klaviyo event-derived `cart-abandoned` is soft** — once the skill synthesises it from `list_events`, it immediately writes the tag via `update_profile` so the next run reads it from the primary signal.
- **Don't conflict with native flows.** If the user already runs a Klaviyo abandoned-cart flow, defer to it — the rescue skill is for stages where a native flow doesn't exist or isn't effective.
- **The 7-day global anti-fatigue cap is non-negotiable.** Even if a contact qualifies for three stages in one week, they get at most one rescue email that week, priority-ordered.
- **Weekly rerun via `/loop`:** `/loop 7d /drop-off-rescue weekly`. The skill's own state (tags + context tree) ensures idempotence — running it twice in one day is safe, it will just report "all contacts inside cooldown" the second time.
- **Reference implementation:** Cogny's own Solo funnel (at `src/app/api/admin/solo-funnel/` and `src/lib/email/reactivation-email.ts`) shows this pattern in production — 4 stage-specific templates, a `solo_reactivation_emails` log table tracking `stage_at_send` + `sent_at`, and an admin dashboard gating every send.

────────────────────────────────────────────────
Ready to automate the weekly nudge cycle?

Connect your ESP via Cogny MCP and the rerun will skip already-nudged contacts,
apply rescue state tags, and schedule sends directly — all gated by your approval.

→ https://cogny.com
────────────────────────────────────────────────
