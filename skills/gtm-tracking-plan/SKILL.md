---
name: gtm-tracking-plan
description: Turn a measurement plan into a Google Tag Manager spec — tags, triggers, variables, and copy-paste dataLayer snippets for every event
version: "1.1.1"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<site url>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Enhanced when connected via Cogny MCP (read-only)
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__list_integrations
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_triggers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_variables
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_data_streams
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_pixels
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_get_pixels
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_conversions
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_conversion_events
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_pixels
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__X_Ads__tool_get_web_event_tags
---

# GTM Tracking Plan

Give it a site URL and get back a complete Google Tag Manager build spec — every tag,
trigger, and variable to create, plus the exact `dataLayer.push()` snippets a
developer drops into the site. It's the implementation half of a measurement plan. No
account connection required.

Best run after `/ga4-measurement-plan` — pass the same URL and this skill builds the
GTM container to deliver that plan. Run alone, it derives a sensible plan first.

## Works with

Works with zero accounts (placeholders for every ID). When connected, the spec is filled
with real IDs and diffed against the live container:

| Job | Without accounts | Enhanced when connected |
|-----|------------------|-------------------------|
| Existing container | — | GTM `tool_list_tags`, `tool_list_triggers`, `tool_list_variables` |
| GA4 Measurement ID | `G-XXXXXXX` | GA4 `tool_list_data_streams` |
| Ad-platform tags to include | ask the user | one row per connected ad platform (Step 4b) |
| Build it | hand to a GTM builder | `/gtm-setup` (GTM writes, asks first) |

## Usage

`/gtm-tracking-plan example.com` — full GTM build spec for the site

## Steps

### 1. Establish the events to implement

If a GA4 measurement plan already exists in the conversation, use its event taxonomy.
Otherwise, `WebFetch` the site, infer the site type and funnel, and derive the event
list yourself (the same logic as `/ga4-measurement-plan`, in brief).

For each event you need: name, when it fires, its parameters, whether it's a key event.

### 1b. Diff against the live container (enhanced when connected)

If Cogny isn't connected, skip this and note what connecting adds.

If GTM is connected: `tool_list_accounts` → `tool_list_containers` (`account_id`) →
`tool_list_workspaces` → `tool_list_tags`, `tool_list_triggers`, `tool_list_variables`
(`account_id`, `container_id`, `workspace_id`). Give every row in Steps 2–4 a **Status**:
`exists` / `modify` / `new` / `remove` (duplicates, dead tags). Use the container's own
naming convention if it has one. If GA4 is connected, take the Measurement ID from
`tool_list_data_streams` (`property_id`).

### 2. Variables

List every variable to create, by type:

- **Data Layer Variables** — one per parameter pushed to the data layer
  (`ecommerce`, `value`, `currency`, `transaction_id`, `lead_source`, …)
- **Built-in variables to enable** — Click Element, Click URL, Click Text, Form ID,
  Page Path, Page URL, plus the relevant ones per trigger
- **Constant** — the GA4 Measurement ID (`G-XXXXXXX`)
- **Lookup / RegEx table** — only if routing or value mapping is genuinely needed
- **Consent state variables** — if Consent Mode is in scope

Present as a table: variable name, type, configuration, used by.

### 3. Triggers

One trigger per distinct firing condition. For each: name, type, and conditions.

- **Initialization / Consent Initialization** — for Consent Mode default state
- **Custom Event** triggers — one per dataLayer event (`event` equals `purchase`,
  `generate_lead`, …) — the recommended approach for anything pushed to the dataLayer
- **DOM-based** triggers (click, form submission, element visibility) only where the
  site cannot push a dataLayer event
- **History Change** — for SPA page views

Name them consistently: `CE - purchase`, `Click - CTA button`.

### 4. Tags

List every tag to create. For each: name, type, what fires it, and key fields.

- **Google tag** (formerly the "GA4 Configuration tag") — exactly one per Measurement
  ID, on Initialization / All Pages, with the Tag ID (`G-XXXXXXXXXX`). (Calling out "exactly one" prevents the classic double-count bug.)
- **GA4 Event tags** — one per event from Step 1, with the same Measurement ID as the Google tag, and
  parameters mapped from the Data Layer Variables
- **Google Ads Conversion tags** — for key events that feed Ads bidding, with
  conversion ID/label placeholders
- **Consent** — Consent Mode default + update tags if in scope

Use a clear convention: `GA4 - Event - purchase`, `Ads - Conversion - Lead`.

### 4b. Ad-platform tags (enhanced when connected)

If Cogny isn't connected, skip this and note what connecting adds.

Call `list_integrations` once. For each healthy ad platform, add its base tag and the
conversion events the key events map to, with the real ID:

| Platform | Read the ID with | Tag in GTM |
|----------|------------------|------------|
| Google Ads | `tool_execute_gaql`: `SELECT conversion_action.name, conversion_action.status, conversion_action.tag_snippets FROM conversion_action` | Conversion Tracking (ID + label) + Conversion Linker |
| Meta | `tool_list_ad_accounts` → `tool_get_pixels` (`ad_account_id`) | Meta Pixel (template) + CAPI via `/meta-capi` |
| TikTok | `tool_list_advertisers` → `tool_get_pixels` (`advertiser_id`) | TikTok Pixel template |
| LinkedIn | `tool_list_ad_accounts` → `tool_get_conversions` (`ad_account_id`) | Insight Tag + conversion IDs |
| Reddit | `tool_list_ad_accounts` → `tool_get_conversion_events` (`ad_account_id`) | Reddit Pixel template |
| Snapchat | `tool_list_ad_accounts` → `tool_list_pixels` (`ad_account_id`) | Snap Pixel template |
| X | `tool_list_ad_accounts` → `tool_get_web_event_tags` (`account_id`) | X base pixel + event tags |

Platforms not connected: list them as optional rows with placeholders. Microsoft Ads (UET)
has no tag-reading tool; ask for the UET tag ID. All ad tags fire on the same Custom Event
triggers as GA4 and pass the same `transaction_id` / event ID for dedup.

### 5. dataLayer snippets

This is the developer handoff. For every event that needs site code, give a
copy-paste `dataLayer.push()` snippet with realistic placeholders:

```html
<!-- Fire on the order confirmation page, after the dataLayer is initialized -->
<script>
  window.dataLayer = window.dataLayer || [];
  dataLayer.push({ ecommerce: null });   // clear the previous ecommerce object
  dataLayer.push({
    event: "purchase",
    ecommerce: {
      transaction_id: "{{ORDER_ID}}",
      value: {{ORDER_TOTAL}},
      currency: "{{CURRENCY}}",
      items: [
        { item_id: "{{SKU}}", item_name: "{{NAME}}", price: {{PRICE}}, quantity: {{QTY}} }
      ]
    }
  });
</script>
```

Include the snippet for each key event and the most important non-key events. Note
the firing location (which page / which DOM event) for each.

### 6. Implementation order & QA

Give the build sequence:
1. Enable built-in variables and create user-defined variables
2. Create triggers
3. Create the Google tag, then GA4 event tags, then Ads conversion tags
4. Add the dataLayer snippets to the site
5. QA in **GTM Preview** + **GA4 DebugView** — verify each event fires once, with
   parameters populated, and not before consent
6. Publish a named version

Call out the common failure modes: dataLayer pushed *after* the GTM snippet, stale
`ecommerce` object not cleared, tags firing pre-consent, event-name typos.

### 7. Output

Deliver as one document:

```
GTM Tracking Plan — [site]

Container overview: X tags · X triggers · X variables

1. Variables table
2. Triggers table
3. Tags table
4. dataLayer snippets (per event, with firing location)
5. Build order
6. QA checklist
```

## Critical rules

1. **Exactly one Google tag per Measurement ID.** State it explicitly — duplicate Google tags
   are the most common GTM bug.
2. **Prefer Custom Event triggers over DOM triggers.** A dataLayer push is reliable;
   scraping the DOM is brittle. Use DOM triggers only when the site can't push.
3. **Every dataLayer snippet must be copy-paste ready** with clearly marked
   placeholders and a stated firing location.
4. **Respect Consent Mode** — analytics and Ads tags must not fire before consent in
   regulated regions.
5. **Real IDs only from the platform.** Never guess a pixel or conversion ID; leave a
   placeholder if the platform isn't connected.
6. This produces a *build spec*. To audit a live container, use `/gtm-audit`
   (requires Cogny MCP).
