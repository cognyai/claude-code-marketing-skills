---
name: pre-send-qa
description: Pre-flight QA for an email campaign — merge tags, broken links, spam triggers, compliance, mobile rendering — before you hit send
version: "1.0.0"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter]
user-invocable: true
argument-hint: "[campaign ID | paste HTML]"
allowed-tools:
  # Cogny Cloud (aggregated) namespace
  - mcp__cogny__klaviyo__*
  - mcp__cogny__mailchimp__*
  - mcp__cogny__rule__*
  - mcp__cogny__get_a_newsletter__*
  - mcp__cogny__create_finding
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

# Pre-Send QA

Catch the embarrassing stuff before it ships to your list. Runs a full pre-flight check on an email: merge tag fallbacks, broken links, spam triggers, CAN-SPAM / GDPR footers, mobile rendering, size limits, accessibility.

**Requires:** Cogny MCP for campaign-ID mode. Paste-HTML mode works without MCP (but without send-context checks).

## Usage

`/pre-send-qa <campaign-or-draft-id>` — QA a specific campaign (or draft, for Get a Newsletter) in your ESP
`/pre-send-qa` — then paste the email HTML/MJML/text when prompted

## Steps

### 1. Load the email

**Mode A — Campaign ID (MCP).** Detect which ESP is connected (check both namespaces: `mcp__cogny__<svc>__*` and `mcp__<svc>__*`) and use the right tool:

| ESP | Fetch tool | What the ID refers to |
|-----|------------|----------------------|
| Klaviyo | `get_campaign` | Campaign object |
| Mailchimp | `tool_get_campaign` | Campaign object |
| Rule | `tool_get_campaign` | Campaign object |
| Get a Newsletter — pre-send | `tool_get_draft` | A draft that hasn't been sent yet |
| Get a Newsletter — post-send forensics | `tool_get_sent` + `tool_get_report` | A sent item |

For every ESP extract: subject, preheader, from name, from email, reply-to, HTML body, text body, target segment/list, scheduled send time. Also fetch the associated list/audience size so Section 2.8 has recipient count.

**Get a Newsletter has no single "campaign" object.** If the user passes an ID, try `tool_get_draft` first (pre-send QA is the common use), fall back to `tool_get_sent` if that 404s. If they want to QA a *scheduled* send, use `tool_list_scheduled` to find it.

**Mode B — Paste:**
- Ask for subject line, preheader, from name/email, and body HTML. Accept multi-line paste.
- Section 2.8 (send context) is skipped in paste mode — no recipient count, no segment, no schedule.

### 2. Run the checklist

Walk through every category. For each item, mark `[PASS]`, `[WARN]`, or `[FAIL]` and include the specific offending content.

#### 2.1 Headers & routing
- [ ] **Subject line present** — not empty
- [ ] **Subject length ≤ 55 chars** (mobile truncation threshold)
- [ ] **Preheader present** — not empty, not a duplicate of subject
- [ ] **Preheader length 85–100 chars** (too short = wasted real estate; too long = truncated)
- [ ] **From name is branded** — not "noreply", not "info"
- [ ] **From email uses sending subdomain** — flag `@gmail.com`/`@outlook.com` from addresses (deliverability killer for bulk)
- [ ] **Reply-to is monitored** — warn if it's a noreply@

#### 2.2 Merge tags / personalization
Scan body + subject + preheader for:
- `{{ ... }}`, `{% ... %}`, `*|...|*`, `[[...]]`, `%%...%%`, `{...}` — depending on ESP syntax
- [ ] **All merge tags well-formed** — balanced brackets, closed blocks
- [ ] **All merge tags have fallbacks** — e.g., `{{ first_name|default:"there" }}` (Klaviyo), `*|IFNOT:FNAME|*there*|ELSE:*|FNAME|**|END:IF|*` (Mailchimp). Flag any token without a fallback as FAIL.
- [ ] **"Hi ," or "Hello ," anti-pattern** — substring search for bare punctuation after a greeting. This is the #1 embarrassing merge-tag failure.
- [ ] **Dynamic content blocks closed** — open `{% if %}` must have `{% endif %}`; same for loops
- [ ] **No raw tokens in subject line** — e.g., subject reading literally "Hi {{ first_name }}"

#### 2.3 Links
Extract all `<a href="...">` from the HTML. For each:
- [ ] **URL is absolute** — no `href="/path"` without domain; no `href="#"` unless intentional anchor
- [ ] **URL resolves** — HEAD-check each unique URL (cap at 30 requests, dedupe). Flag non-200s.
- [ ] **No `localhost` / `127.0.0.1` / `.local`** — dev leak
- [ ] **No staging/dev domains** — flag `*.staging.*`, `*.dev.*`, `stage.`, `preprod.`
- [ ] **UTM parameters present on all outbound links** — warn on links missing `utm_source`/`utm_medium`/`utm_campaign`
- [ ] **UTM consistency** — all links should share `utm_campaign`; flag divergence
- [ ] **Link count** — report total. Warn if >20 (clutter). Warn if <1 (no CTA).
- [ ] **CTA destination consistency** — multiple buttons labeled "Shop now" should generally point to the same URL

#### 2.4 Images
- [ ] **All `<img>` have `alt` text** — non-empty, descriptive
- [ ] **No pure-image email** — flag if text-to-image ratio is <40% text. Hero-image-only emails trigger spam filters.
- [ ] **Image URLs are absolute + HTTPS**
- [ ] **Image URLs aren't hotlinked from sketchy hosts** — flag if images are on `imgur`, `cloudinary demo`, etc. instead of a brand CDN

#### 2.5 Compliance
- [ ] **Unsubscribe link present** — regex for `unsubscribe`, `preferences`, `opt out`
- [ ] **Unsubscribe link is visible** — not `display:none` or font-size:1px
- [ ] **Physical postal address in footer** — CAN-SPAM requirement. Regex for a street/city pattern or flag if missing.
- [ ] **List-Unsubscribe header** — flag if ESP allows setting it but it's not configured (one-click unsubscribe is required by Gmail/Yahoo for bulk senders)
- [ ] **Preference center link** — nice-to-have; warn if only unsubscribe exists

#### 2.6 Spam triggers
Scan subject + preheader + body for classic triggers and report offenders:
- **Word-level:** free, winner, congratulations, guaranteed, risk-free, act now, click here, limited time, no obligation, viagra (lol), make money, earn extra, $$$
- **Punctuation:** more than one `!` in subject, `!!!`, `???`
- **Casing:** ALL CAPS WORDS longer than 3 chars in subject
- **Symbols:** `$$$`, `★`, excessive emoji (>3)
- **HTML:** hidden text (color matches background), tiny font, embedded JavaScript, background images on `<body>`

Output each offender with context:
```
🔴 Subject contains "!!!"
🟡 Body has 4 instances of ALL CAPS words: "LIMITED", "TODAY", "ACT NOW", "DON'T"
```

#### 2.7 Rendering & size
- [ ] **HTML size < 102 KB** — Gmail clips at 102 KB. Report actual size.
- [ ] **Single root `<table>` layout** (desktop email standard) OR uses MJML — flag flex/grid as a deliverability risk
- [ ] **Inline CSS** — style attributes vs `<style>` blocks. Many clients strip `<head>` styles.
- [ ] **Mobile viewport meta** — `<meta name="viewport" content="width=device-width">`
- [ ] **Font stack has fallbacks** — no `font-family: "Custom Font";` without a web-safe fallback
- [ ] **No `<script>`, no `<form>`, no external fonts loaded via JS** — all stripped by most clients

#### 2.8 Send context (MCP mode only)
- [ ] **Target segment is populated** — recipient count > 0
- [ ] **Audience isn't the entire list for a promotional send** — flag "All Subscribers" when there's a segmented alternative
- [ ] **Scheduled time isn't 3am recipient-local** — flag weird send hours
- [ ] **Not a duplicate send** — check last 30 days for a campaign with the same subject going to the same segment

### 3. Report

```
Pre-send QA: <campaign name | "pasted email">
Recipient count: <N>    Send ETA: <time or "not scheduled">

Overall: <READY TO SEND | FIX BEFORE SEND | CRITICAL ISSUES>

🔴 Critical (will break or embarrass)
  — <specific issue with offending text / URL / line>
  — ...

🟡 Warnings (fix if you have time)
  — ...

🟢 Passed
  — <count> checks passed

──
Recommended fix order:
  1. ...
  2. ...

Merge-tag fallback cheatsheet for <ESP>:
  [ESP-specific syntax examples]
```

### 4. Finding (optional)

If critical issues are found and the campaign is scheduled to send soon, create a finding:

```json
{
  "title": "Campaign '<name>' has critical QA issues — blocked send",
  "body": "<enumerated issues>",
  "action_type": "pre_send_fix",
  "priority": "high"
}
```

### 5. Do not auto-fix

Never modify the campaign automatically. Always present the diff and let the user approve each fix.

## Notes

- ESP-specific merge tag syntax:
  - **Klaviyo:** `{{ first_name|default:"there" }}`
  - **Mailchimp:** `*|FNAME|*` with `*|IFNOT:FNAME|*there*|ELSE:*|FNAME|**|END:IF|*`
  - **Rule / Get a Newsletter:** `[Firstname]` with platform-specific fallback syntax
- Spam-trigger lists are heuristics; modern spam filters use ML + reputation. Treat warnings as "raise eyebrow, check reputation" not "instant spam".
