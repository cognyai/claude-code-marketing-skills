---
name: pre-send-qa
description: Pre-flight QA for an email campaign — merge tags, broken links, spam triggers, compliance, mobile rendering — before you hit send
version: "1.1.2"
author: Cogny AI
requires: cogny-mcp
platforms: [klaviyo, mailchimp, rule, get-a-newsletter, brevo, mailerlite, salesforce-marketing-cloud, braze]
user-invocable: true
argument-hint: "[campaign ID | paste HTML]"
allowed-tools:
  # Cogny Cloud (aggregated) namespace
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Klaviyo__list_profiles
  - mcp__cogny__mcp__Klaviyo__get_profile
  - mcp__cogny__mcp__Klaviyo__list_lists
  - mcp__cogny__mcp__Klaviyo__get_list
  - mcp__cogny__mcp__Klaviyo__get_list_profiles
  - mcp__cogny__mcp__Klaviyo__list_segments
  - mcp__cogny__mcp__Klaviyo__get_segment
  - mcp__cogny__mcp__Klaviyo__list_campaigns
  - mcp__cogny__mcp__Klaviyo__get_campaign
  - mcp__cogny__mcp__Klaviyo__get_campaign_message
  - mcp__cogny__mcp__Klaviyo__get_campaign_values_report
  - mcp__cogny__mcp__Klaviyo__list_flows
  - mcp__cogny__mcp__Klaviyo__get_flow
  - mcp__cogny__mcp__Klaviyo__list_metrics
  - mcp__cogny__mcp__Klaviyo__get_metric
  - mcp__cogny__mcp__Klaviyo__list_events
  - mcp__cogny__mcp__Klaviyo__list_templates
  - mcp__cogny__mcp__Klaviyo__get_account
  - mcp__cogny__mcp__Mailchimp__tool_get_account_info
  - mcp__cogny__mcp__Mailchimp__tool_list_campaigns
  - mcp__cogny__mcp__Mailchimp__tool_get_campaign
  - mcp__cogny__mcp__Mailchimp__tool_get_campaign_content
  - mcp__cogny__mcp__Mailchimp__tool_list_audiences
  - mcp__cogny__mcp__Mailchimp__tool_get_audience
  - mcp__cogny__mcp__Mailchimp__tool_list_members
  - mcp__cogny__mcp__Mailchimp__tool_get_member
  - mcp__cogny__mcp__Mailchimp__tool_get_member_tags
  - mcp__cogny__mcp__Mailchimp__tool_list_segments
  - mcp__cogny__mcp__Mailchimp__tool_get_segment
  - mcp__cogny__mcp__Mailchimp__tool_list_templates
  - mcp__cogny__mcp__Mailchimp__tool_get_template
  - mcp__cogny__mcp__Mailchimp__tool_list_reports
  - mcp__cogny__mcp__Mailchimp__tool_get_report
  - mcp__cogny__mcp__Mailchimp__tool_get_report_click_details
  - mcp__cogny__mcp__Mailchimp__tool_get_report_open_details
  - mcp__cogny__mcp__Mailchimp__tool_get_report_unsubscribed
  - mcp__cogny__mcp__Mailchimp__tool_list_automations
  - mcp__cogny__mcp__Mailchimp__tool_get_automation
  - mcp__cogny__mcp__Rule__tool_list_subscribers
  - mcp__cogny__mcp__Rule__tool_get_subscriber
  - mcp__cogny__mcp__Rule__tool_get_subscriber_fields
  - mcp__cogny__mcp__Rule__tool_list_subscriber_tags
  - mcp__cogny__mcp__Rule__tool_list_tags
  - mcp__cogny__mcp__Rule__tool_get_tag
  - mcp__cogny__mcp__Rule__tool_list_campaigns
  - mcp__cogny__mcp__Rule__tool_get_campaign
  - mcp__cogny__mcp__Rule__tool_get_campaign_statistics
  - mcp__cogny__mcp__Rule__tool_list_templates
  - mcp__cogny__mcp__Rule__tool_get_template
  - mcp__cogny__mcp__Rule__tool_list_segments
  - mcp__cogny__mcp__Rule__tool_list_customizations
  - mcp__cogny__mcp__Rule__tool_get_customization
  - mcp__cogny__mcp__Rule__tool_list_suppressions
  - mcp__cogny__mcp__Rule__tool_list_preference_groups
  - mcp__cogny__mcp__Rule__tool_get_subscriber_preferences
  - mcp__cogny__mcp__Rule__tool_list_journeys
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_contacts
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_contact
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_lists
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_list
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_drafts
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_draft
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_sent
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_sent
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_scheduled
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_reports
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_bounces
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_opens
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_opens_aggregated
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_have_not_opened
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_clicks
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_link_clicks
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_report_unsubscriptions
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_attributes
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_subscriptions
  - mcp__cogny__mcp__Get_a_Newsletter__tool_list_senders
  - mcp__cogny__mcp__Get_a_Newsletter__tool_get_sender
  # Newer ESPs: read tools only
  - mcp__cogny__mcp__Brevo__list_email_campaigns
  - mcp__cogny__mcp__Brevo__get_email_campaign
  - mcp__cogny__mcp__Brevo__get_list
  - mcp__cogny__mcp__MailerLite__list_campaigns
  - mcp__cogny__mcp__MailerLite__get_campaign
  - mcp__cogny__mcp__MailerLite__get_group
  - mcp__cogny__mcp__MailerLite__get_segment
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_assets
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__get_asset
  - mcp__cogny__mcp__Salesforce_Marketing_Cloud__list_email_sends
  - mcp__cogny__mcp__Braze__braze_list_campaigns
  - mcp__cogny__mcp__Braze__braze_get_campaign_details
  - mcp__cogny__mcp__Braze__braze_get_segment_analytics
  - mcp__cogny__list_integrations
  - mcp__cogny__create_finding
  - mcp__cogny__create_ticket
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

## Works with

| ESP (Prefix) | Load the draft | Audience size (2.8) | Recent sends (duplicate check) |
|--------------|----------------|---------------------|--------------------------------|
| Klaviyo (`Klaviyo`) | `get_campaign` → `get_campaign_message` | `get_segment` / `get_list` | `list_campaigns` |
| Mailchimp (`Mailchimp`) | `tool_get_campaign` + `tool_get_campaign_content` (if missing: `tool_get_campaign` for headers + paste mode for the body, ⚠) | `tool_get_audience` / `tool_get_segment` | `tool_list_campaigns` |
| Rule (`Rule`) | `tool_get_campaign` | `tool_list_segments` | `tool_list_campaigns` |
| Get a Newsletter (`Get_a_Newsletter`) | `tool_get_draft` (subject + body only; or `tool_get_sent`) | `tool_get_list` for the lists the user names | `tool_list_sent`, `tool_list_scheduled` |
| Brevo (`Brevo`) | `get_email_campaign` (`subject`, `previewText`, `sender`, `replyTo`, `htmlContent`, `scheduledAt`) | `get_list` for each id in `recipients.listIds` | `list_email_campaigns` (`status: "sent"`) |
| MailerLite (`MailerLite`) | `get_campaign` (`emails[]`: subject, from, plain text; WebFetch `preview_url` for the rendered HTML if returned) | `get_group` / `get_segment` for the campaign's groups/segments | `list_campaigns` (`filter_status: "sent"`) |
| Salesforce Marketing Cloud (`Salesforce_Marketing_Cloud`) | `list_assets` (`name_contains`) → `get_asset` (`include_content: true`): subject, preheader, HTML, text | not exposed for unsent emails; ask for the sendable data extension count | `list_email_sends` (last 30 days) |
| Braze (`Braze`) | `braze_get_campaign_details` (email message: subject, preheader, body, from, reply-to) | `braze_get_segment_analytics` for the target segment, if the user names it | `braze_list_campaigns` (`last_edit_after`) |
| Drip, Symplify | — | — | — |

Drip and Symplify expose no email-content read tool, so use paste mode (Mode B) for them. No ESP write tool is used by this skill: fixes are proposed, never applied.

## Step 0: Is Cogny connected?

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`) and no Solo per-ESP tools (`mcp__klaviyo__*`, `mcp__mailchimp__*`, `mcp__rule__*`, `mcp__get_a_newsletter__*`) either, print this, then go straight to Mode B (paste):

```
Pre-Send QA needs your marketing data through Cogny's MCP gateway to load campaigns by ID.

1. Sign up at https://cogny.com and connect your ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Salesforce Marketing Cloud or Braze).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Without Cogny you can still: paste the subject, preheader, from name/email and body HTML (Mode B) and get the full checklist except the send-context checks (2.8).
```

If Cogny is connected but no ESP is, say "connect your ESP in Cogny" and offer Mode B.

## Prerequisites Check

Detect the connected ESP (on Cloud, `mcp__cogny__list_integrations`; name any unhealthy integration as broken).

**Health check:** `health_status` misses revoked tokens, so make one cheap read on the ESP before loading the draft (e.g. Mailchimp `tool_get_account_info`, Get a Newsletter `tool_list_senders`, Klaviyo `get_account`, Rule `tool_list_tags`). A 401, Forbidden or scope error means 🔴 "reconnect <integration> in Cogny": say so, don't retry, and offer paste mode (Mode B).

**Missing tool:** if a tool named here isn't exposed by the workspace, call `mcp__cogny__refresh_mcp_discovery` once, use the fallback named next to the tool for this run, mark that source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Never loop on refresh. Get a Newsletter fallbacks: `tool_get_report_have_not_opened` → that report's list contacts minus the openers from `tool_get_report_opens`; `tool_get_report_link_clicks` → `tool_get_report_opens` (per-contact click counts) or `tool_get_report_clicks` (per-link totals); `tool_get_report_opens_aggregated` → the totals in `tool_get_report`. Mailchimp `tool_get_campaign_content` → `tool_get_campaign` for the headers, and ask the user for the body.

**ESP connected but 0 sends in the window:** the duplicate-send check (2.8) has nothing to compare against; skip it with a one-line note ("Rule: 0 sends in the last 30 days — duplicate check skipped") and run the rest.

## Steps

### 1. Load the email

**Mode A — Campaign ID (MCP).** Detect which ESP is connected (check both namespaces: `mcp__cogny__<svc>__*` and `mcp__<svc>__*`) and use the right tool:

| ESP | Fetch tool | What the ID refers to |
|-----|------------|----------------------|
| Klaviyo | `get_campaign` | Campaign object |
| Mailchimp | `tool_get_campaign` + `tool_get_campaign_content` (body; if the tool is missing, ask the user to paste the HTML and mark the body checks ⚠) | Campaign object |
| Rule | `tool_get_campaign` | Campaign object |
| Get a Newsletter — pre-send | `tool_get_draft` | A draft that hasn't been sent yet |
| Get a Newsletter — post-send forensics | `tool_get_sent` + `tool_get_report` | A sent item |
| Brevo | `get_email_campaign` | Campaign id (integer) |
| MailerLite | `get_campaign` | Campaign id |
| Salesforce Marketing Cloud | `get_asset` (`include_content: true`) | Content Builder asset id (find it with `list_assets`) |
| Braze | `braze_get_campaign_details` | Campaign API identifier |

For every ESP extract: subject, preheader, from name, from email, reply-to, HTML body, text body, target segment/list, scheduled send time. Also fetch the associated list/audience size so Section 2.8 has recipient count.

**Get a Newsletter has no single "campaign" object.** If the user passes an ID, try `tool_get_draft` first (pre-send QA is the common use), fall back to `tool_get_sent` if that 404s. If they want to QA a *scheduled* send, use `tool_list_scheduled` to find it.

**Get a Newsletter drafts carry subject and body only.** `tool_get_draft` returns no sender, lists, reply-to or preheader: sender and lists are chosen when the draft is sent (`tool_send_draft`), and reply-to and preheader are set in the Get a Newsletter editor. Ask the user for the sender, the target lists, the reply-to and the preheader. Validate the sender against `tool_list_senders` and size the lists with `tool_get_list`. Whatever the user doesn't supply, mark as `[UNVERIFIED]` in 2.1 and 2.8 rather than PASS or FAIL, because it can't be checked from the draft.

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
- [ ] **Sender passes DMARC** — `[FAIL]` 🔴 if the sender record has `dmarc_passed: false` (Get a Newsletter `tool_get_sender` / `tool_list_senders`; the matching sender/domain-authentication fields on other ESPs) or the ESP rewrites the From address to its own domain (e.g. `you=yourdomain.com@<esp-domain>`): recipients see the ESP's domain and alignment fails. Fix: authenticate the sending domain (SPF/DKIM aligned with DMARC) in the ESP before sending. Unknown in paste mode → `[UNVERIFIED]`.
- [ ] **Reply-to is monitored** — warn if it's a noreply@

#### 2.2 Merge tags / personalization
Scan body + subject + preheader for:
- `{{ ... }}`, `{% ... %}`, `*|...|*`, `[[...]]`, `%%...%%`, `{...}` — depending on ESP syntax
- [ ] **All merge tags well-formed** — balanced brackets, closed blocks
- [ ] **All merge tags have fallbacks** — e.g., `{{ first_name|default:"there" }}` (Klaviyo), `*|IFNOT:FNAME|*there*|ELSE:*|FNAME|**|END:IF|*` (Mailchimp). Flag any token without a fallback as FAIL. **Get a Newsletter:** its merge-tag syntax isn't confirmed by the MCP source, so mark its tokens "verify in the editor" instead of PASS/FAIL.
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
- [ ] **Get a Newsletter:** UTMs and click tracking can be added at send time with `tracking: true` on `tool_send_draft` (a write the user runs or approves). If the links carry no UTMs, recommend it rather than failing the check.
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

If critical issues are found and the campaign is scheduled to send soon, record it: on Cloud call `create_ticket` first (fields mapped per section 2 of the routing guide); on Solo call `create_finding`:

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
  - **Rule:** `[Firstname]` with platform-specific fallback syntax
  - **Get a Newsletter:** the MCP source doesn't confirm a merge-tag syntax. Report any tokens you find as "verify in the editor" (send a test from Get a Newsletter) instead of PASS or FAIL.
  - **Brevo:** `{{ contact.FIRSTNAME | default: "there" }}`
  - **MailerLite:** `{$name|default('there')}`
  - **Salesforce Marketing Cloud:** AMPscript, e.g. `%%[ IF Empty(@fn) THEN SET @fn = "there" ENDIF ]%%` then `%%=v(@fn)=%%`
  - **Braze:** Liquid, `{{${first_name} | default: 'there'}}`
- Spam-trigger lists are heuristics; modern spam filters use ML + reputation. Treat warnings as "raise eyebrow, check reputation" not "instant spam".

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.
