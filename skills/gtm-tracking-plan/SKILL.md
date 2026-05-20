---
name: gtm-tracking-plan
description: Turn a measurement plan into a Google Tag Manager spec — tags, triggers, variables, and copy-paste dataLayer snippets for every event
version: "1.0.0"
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
---

# GTM Tracking Plan

Give it a site URL and get back a complete Google Tag Manager build spec — every tag,
trigger, and variable to create, plus the exact `dataLayer.push()` snippets a
developer drops into the site. It's the implementation half of a measurement plan. No
account connection required.

Best run after `/ga4-measurement-plan` — pass the same URL and this skill builds the
GTM container to deliver that plan. Run alone, it derives a sensible plan first.

## Usage

`/gtm-tracking-plan example.com` — full GTM build spec for the site

## Steps

### 1. Establish the events to implement

If a GA4 measurement plan already exists in the conversation, use its event taxonomy.
Otherwise, `WebFetch` the site, infer the site type and funnel, and derive the event
list yourself (the same logic as `/ga4-measurement-plan`, in brief).

For each event you need: name, when it fires, its parameters, whether it's a key event.

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

- **GA4 Configuration tag** — exactly one, on Initialization / All Pages, with the
  Measurement ID. (Calling out "exactly one" prevents the classic double-count bug.)
- **GA4 Event tags** — one per event from Step 1, referencing the config tag, with
  parameters mapped from the Data Layer Variables
- **Google Ads Conversion tags** — for key events that feed Ads bidding, with
  conversion ID/label placeholders
- **Consent** — Consent Mode default + update tags if in scope

Use a clear convention: `GA4 - Event - purchase`, `Ads - Conversion - Lead`.

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
3. Create the GA4 config tag, then event tags, then Ads conversion tags
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

1. **Exactly one GA4 configuration tag.** State it explicitly — duplicate config tags
   are the most common GTM bug.
2. **Prefer Custom Event triggers over DOM triggers.** A dataLayer push is reliable;
   scraping the DOM is brittle. Use DOM triggers only when the site can't push.
3. **Every dataLayer snippet must be copy-paste ready** with clearly marked
   placeholders and a stated firing location.
4. **Respect Consent Mode** — analytics and Ads tags must not fire before consent in
   regulated regions.
5. This produces a *build spec*. To audit a live container, use `/gtm-audit`
   (requires Cogny MCP).
