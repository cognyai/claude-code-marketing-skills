---
name: ga4-measurement-plan
description: Build a GA4 measurement plan from a site URL — event taxonomy, parameters, custom dimensions, and key events to mark as conversions
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<site url> [business goal]"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
---

# GA4 Measurement Plan

Give it a site URL and get back a complete GA4 measurement plan — which events to
track, what parameters each carries, which custom dimensions to register, and which
events to mark as key events. The deliverable is a spec a developer or GTM builder
can implement directly. No account connection required.

It pairs with `/gtm-tracking-plan`, which turns this plan into the actual GTM tags,
triggers, and variables.

## Usage

`/ga4-measurement-plan example.com` — measurement plan for the site
`/ga4-measurement-plan example.com "drive demo bookings"` — bias the plan toward a goal

## Steps

### 1. Understand the site

`WebFetch` the URL and a representative spread of pages (home, product/category,
pricing, signup/checkout, contact). Determine:

- Site type — ecommerce, lead gen, SaaS, content/media, marketplace
- The **primary conversion** and any secondary conversions (newsletter, demo, account
  creation)
- The funnel steps a visitor passes through to convert
- Notable interactions worth measuring (search, filters, video, downloads, configs)

If a business goal was passed as an argument, make the plan serve it first.

### 2. Start from what GA4 already gives you

Note which events come **free** and need no implementation:
- Automatically collected: `first_visit`, `session_start`, `page_view`,
  `user_engagement`
- Enhanced Measurement (if enabled): `scroll`, `click` (outbound), `view_search_results`,
  `video_*`, `file_download`, `form_start`, `form_submit`

Flag any of these the team should rely on rather than rebuild.

### 3. Recommended events for the site type

Map the site to GA4's recommended events — using the recommended names matters
because GA4 builds reporting around them:

- **Ecommerce**: `view_item_list`, `view_item`, `select_item`, `add_to_cart`,
  `view_cart`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase`,
  `refund`
- **Lead gen / SaaS**: `generate_lead`, `sign_up`, `login`, `search`,
  plus custom events for the funnel
- **Content / media**: `search`, `select_content`, `share`, `join_group`

For each: when it fires and its parameters (e.g. `purchase` → `transaction_id`,
`value`, `currency`, `items[]`).

### 4. Custom events for everything else

For interactions GA4 has no recommended event for, design custom events following the
rules: `snake_case`, ≤40 characters, descriptive, no reserved prefixes
(`google_`, `firebase_`, `ga_`), lowercase. Examples: `demo_requested`,
`pricing_plan_selected`, `quote_calculated`.

Keep the taxonomy tight — a parameter on a shared event usually beats a brand-new
event (`cta_click` with a `cta_location` parameter, not ten separate click events).

### 5. The event taxonomy table

Produce the core deliverable — one row per event:

| Event name | Type | Fires when | Parameters | Key event? |
|------------|------|-----------|------------|------------|
| `purchase` | recommended | order confirmation page loads | `transaction_id`, `value`, `currency`, `items[]` | ✅ |
| `generate_lead` | recommended | contact form submitted | `form_id`, `lead_source`, `value` | ✅ |
| `demo_requested` | custom | demo form submitted | `plan_interest` | ✅ |
| ... | | | | |

### 6. Custom dimensions & metrics to register

Event parameters are invisible in standard GA4 reports until registered as custom
dimensions. List every non-standard parameter from Step 5 that needs registering:

| Parameter | Scope | Register as | Why |
|-----------|-------|-------------|-----|
| `lead_source` | event | custom dimension | segment leads by origin |
| `plan_interest` | event | custom dimension | see which plan drives demos |

Warn against high-cardinality parameters (IDs, timestamps) as dimensions, and note the
50 event-scoped / 25 user-scoped limits.

### 7. Key events (conversions)

Recommend which events to mark as **key events**. Be selective — 3–8 is healthy. Mark
real business outcomes, never `page_view` or `scroll`. Note which key events should
also be imported into Google Ads for bidding.

### 8. Output

Deliver as one document:

```
GA4 Measurement Plan — [site]

Site type: ...  |  Primary conversion: ...

1. Already covered (automatic + Enhanced Measurement): ...
2. Event taxonomy table (recommended + custom)
3. Custom dimensions & metrics to register
4. Key events to mark as conversions (and which to send to Google Ads)
5. dataLayer payload examples for the 3-5 most important events
6. Implementation notes & sequencing
```

End with the handoff line: *"Run `/gtm-tracking-plan [url]` to turn this into GTM
tags, triggers, and variables."*

## Critical rules

1. **Use GA4's recommended event names** wherever one exists — reporting depends on
   them.
2. **A registered parameter beats a new event.** Keep the taxonomy small.
3. **Custom events must follow the naming rules** — `snake_case`, ≤40 chars, no
   reserved prefixes.
4. **Never recommend collecting PII** (email, phone, name) in events or parameters —
   it violates Google policy.
5. This produces a *plan*. To audit a live GA4 property, use `/ga4-audit` (requires
   Cogny MCP).
