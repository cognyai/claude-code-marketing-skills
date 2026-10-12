---
name: gtm-setup
description: GTM Event Tracking & Setup Reference — dataLayer fundamentals, trigger types, variable types, GA4 tag configuration, debug mode, and best practices
version: "1.1.1"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<topic or question>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # GTM tools (when connected via Cogny MCP)
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_triggers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_variables
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_tag
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_trigger
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_variable
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_workspace_status
  - mcp__cogny__mcp__Google_Tag_Manager__tool_search_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__mcp__Google_Tag_Manager__tool_audit_container_privacy
  # Verification when connected (read-only)
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_realtime_report
  - mcp__cogny__mcp__Microsoft_Clarity__get_live_insights
---

# GTM Event Tracking & Setup Reference

Complete reference guide to Google Tag Manager event tracking, including dataLayer fundamentals, trigger and variable types, GA4 tag configuration, debug mode, and implementation best practices.

Full docs: https://cogny.com/docs/gtm-event-tracking

## Usage

```
/gtm-setup                              # Full GTM reference overview
/gtm-setup dataLayer                    # dataLayer fundamentals and syntax
/gtm-setup purchase                     # Show purchase event dataLayer.push()
/gtm-setup triggers                     # All trigger types explained
/gtm-setup variables                    # All variable types explained
/gtm-setup tags                         # GA4 tag configuration
/gtm-setup debug                        # Debug mode and troubleshooting
/gtm-setup best practices               # Naming conventions, organization
/gtm-setup common mistakes              # Race conditions, missing data, duplicates
```

## Instructions

You are a Google Tag Manager expert. Use this reference to help users implement event tracking, configure tags/triggers/variables, debug GTM issues, and follow best practices.

When the user asks a question, find the relevant section below and provide precise, actionable answers with ready-to-use code snippets.

If the user provides a specific topic as an argument, focus on that area. Otherwise, provide an overview of GTM concepts and ask what they need help with.

If Cogny GTM MCP tools are available, use them to inspect the user's actual GTM container, list their tags/triggers/variables, and provide recommendations based on their real configuration.

## Works with

Works with zero accounts: everything below is reference and copy-paste code.

| Job | Without accounts | Enhanced when connected |
|-----|------------------|-------------------------|
| Read the real container | — | GTM `tool_list_tags`, `tool_list_triggers`, `tool_list_variables`, `tool_audit_container_privacy` |
| Build tags / triggers / variables | user clicks it in GTM | GTM write tools (asks first; see "Building in the connected container") |
| Verify the event arrives | GTM Preview + DebugView | GA4 `tool_run_realtime_report` |
| Check a Custom HTML tag didn't break pages | Console | Microsoft Clarity `get_live_insights` (Script Error Count) |

---

## dataLayer Fundamentals

### What Is the dataLayer?

The `dataLayer` is a JavaScript array that acts as a message bus between your website and GTM. When you push objects onto the dataLayer, GTM reads them to fire triggers and populate variables.

### Initialization

Declare the dataLayer before the GTM snippet to capture early pushes:

```html
<script>
  window.dataLayer = window.dataLayer || [];
</script>
<!-- GTM snippet follows -->
```

### dataLayer.push() Syntax

```javascript
// Push data AND fire a trigger (event key is required for trigger evaluation)
dataLayer.push({
  'event': 'custom_event_name',
  'key1': 'value1',
  'key2': 'value2'
});

// Push data without firing a trigger (no 'event' key)
dataLayer.push({
  'user_type': 'premium',
  'user_id': '12345'
});
```

### Object Persistence and Merging

Later pushes override earlier values for the same key. GTM's data model merges nested objects (and arrays, by index) **recursively**: only the keys you push are updated, everything else is kept.

```javascript
dataLayer.push({ 'user': { 'name': 'John', 'plan': 'free' } });
dataLayer.push({ 'user': { 'plan': 'premium' } });
// Result: user = { name: 'John', plan: 'premium' } — user.name survives
```

That recursive merge is why stale e-commerce data leaks from one event into the next, and why you push `{ ecommerce: null }` first.

### Clearing Stale Data (Critical for E-Commerce)

Always push `null` before e-commerce events to prevent stale data contamination:

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    'items': [{ 'item_id': 'SKU-001', 'item_name': 'Blue T-Shirt', 'price': 29.99 }]
  }
});
```

## Common dataLayer Events

### page_view

```javascript
dataLayer.push({
  'event': 'page_view',
  'page_location': window.location.href,
  'page_title': document.title,
  'page_referrer': document.referrer,
  'content_group': 'blog'
});
```

For SPAs (React, Next.js, Vue), fire on route change:

```javascript
useEffect(() => {
  dataLayer.push({
    'event': 'page_view',
    'page_location': window.location.href,
    'page_title': document.title
  });
}, [location.pathname]);
```

### purchase

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T-20250211-001',
    'value': 149.97,
    'tax': 12.50,
    'shipping': 5.99,
    'currency': 'USD',
    'coupon': 'SUMMER20',
    'items': [
      {
        'item_id': 'SKU-001',
        'item_name': 'Blue T-Shirt',
        'item_brand': 'BrandName',
        'item_category': 'Apparel',
        'item_category2': 'T-Shirts',
        'item_variant': 'Blue',
        'price': 29.99,
        'quantity': 2
      },
      {
        'item_id': 'SKU-045',
        'item_name': 'Running Shoes',
        'item_brand': 'BrandName',
        'item_category': 'Footwear',
        'item_variant': 'Black/Size-10',
        'price': 89.99,
        'quantity': 1
      }
    ]
  }
});
```

### add_to_cart

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'add_to_cart',
  'ecommerce': {
    'currency': 'USD',
    'value': 29.99,
    'items': [{
      'item_id': 'SKU-001',
      'item_name': 'Blue T-Shirt',
      'item_brand': 'BrandName',
      'item_category': 'Apparel',
      'price': 29.99,
      'quantity': 1
    }]
  }
});
```

### remove_from_cart

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'remove_from_cart',
  'ecommerce': {
    'currency': 'USD',
    'value': 29.99,
    'items': [{
      'item_id': 'SKU-001',
      'item_name': 'Blue T-Shirt',
      'price': 29.99,
      'quantity': 1
    }]
  }
});
```

### view_item

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    'currency': 'USD',
    'value': 29.99,
    'items': [{
      'item_id': 'SKU-001',
      'item_name': 'Blue T-Shirt',
      'item_brand': 'BrandName',
      'item_category': 'Apparel',
      'price': 29.99
    }]
  }
});
```

### view_item_list

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'view_item_list',
  'ecommerce': {
    'item_list_id': 'category_apparel',
    'item_list_name': 'Apparel',
    'items': [
      { 'item_id': 'SKU-001', 'item_name': 'Blue T-Shirt', 'index': 0, 'price': 29.99 },
      { 'item_id': 'SKU-002', 'item_name': 'Red T-Shirt', 'index': 1, 'price': 29.99 }
    ]
  }
});
```

### begin_checkout

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'begin_checkout',
  'ecommerce': {
    'currency': 'USD',
    'value': 149.97,
    'coupon': 'SUMMER20',
    'items': [
      { 'item_id': 'SKU-001', 'item_name': 'Blue T-Shirt', 'price': 29.99, 'quantity': 2 },
      { 'item_id': 'SKU-045', 'item_name': 'Running Shoes', 'price': 89.99, 'quantity': 1 }
    ]
  }
});
```

### form_submit

```javascript
dataLayer.push({
  'event': 'form_submit',
  'form_id': 'contact_form',
  'form_name': 'Contact Us',
  'form_destination': '/thank-you'
});
```

### generate_lead

```javascript
dataLayer.push({
  'event': 'generate_lead',
  'currency': 'USD',
  'value': 50.00,
  'lead_source': 'contact_form'
});
```

### sign_up / login

```javascript
dataLayer.push({ 'event': 'sign_up', 'method': 'google' });
dataLayer.push({ 'event': 'login', 'method': 'email' });
```

### search

```javascript
dataLayer.push({
  'event': 'search',
  'search_term': 'blue t-shirt',
  'search_results_count': 42
});
```

### scroll (custom)

```javascript
dataLayer.push({
  'event': 'scroll',
  'percent_scrolled': 90
});
```

### Video events

```javascript
// video_start
dataLayer.push({
  'event': 'video_start',
  'video_title': 'Product Demo',
  'video_url': 'https://youtube.com/watch?v=abc123',
  'video_provider': 'youtube',
  'video_duration': 180
});

// video_progress
dataLayer.push({
  'event': 'video_progress',
  'video_title': 'Product Demo',
  'video_percent': 50,
  'video_current_time': 90,
  'video_duration': 180
});

// video_complete
dataLayer.push({
  'event': 'video_complete',
  'video_title': 'Product Demo',
  'video_duration': 180
});
```

## Trigger Types

### Page View Triggers

Listed in firing order:

| Sub-Type | Fires When | Use Case |
|----------|------------|----------|
| **Consent Initialization** | Before every other trigger | CMP tag, consent mode defaults |
| **Initialization** | Before everything except Consent Initialization | Google tag, tags that set up shared config |
| **Page View** | `gtm.js` (immediately) | Page-load tags that don't need the DOM |
| **DOM Ready** | `gtm.dom` (DOM parsed) | Tags that read DOM elements |
| **Window Loaded** | `gtm.load` (all resources loaded) | Tags depending on images/scripts |

Filter by Page Path, Page Hostname, or Page URL.

### Click Triggers

| Sub-Type | Fires When | Use Case |
|----------|------------|----------|
| **All Elements** | Any element clicked | Buttons, divs, images |
| **Just Links** | `<a>` element clicked | Outbound links, downloads |

Variables available: Click Element, Click Classes, Click ID, Click Target, Click URL, Click Text.

### Custom Event Trigger

Fires when a specific `event` value is pushed to the dataLayer. Set Event Name to match the `event` key value. Supports regex (e.g., `form_submit.*`).

```javascript
dataLayer.push({ 'event': 'form_submit' });
// Fires trigger where Event Name = "form_submit"
```

### Element Visibility Trigger

Fires when an element enters the viewport.

| Setting | Description |
|---------|-------------|
| Selection Method | CSS Selector or Element ID |
| When to fire | Once per page / once per element / every time |
| Minimum % visible | Default 50% |
| Minimum on-screen duration | Milliseconds |

### Timer Trigger

Fires at a set interval (milliseconds). Configure a limit to cap the number of firings.

### Scroll Depth Trigger

Fires at specified scroll thresholds (percentages or pixels). Supports vertical and horizontal.

Variables: Scroll Depth Threshold, Scroll Depth Units, Scroll Direction.

### YouTube Video Trigger

Built-in support for embedded YouTube videos. Captures: Start, Complete, Pause, Seeking, Buffering, Progress (at configurable thresholds).

Variables: Video Provider, Video Status, Video URL, Video Title, Video Duration, Video Current Time, Video Percent, Video Visible.

### Form Submission Trigger

Fires on form submit. Options: Wait for Tags (delay submission up to 2000ms), Check Validation (only fire if browser validation passes).

Variables: Form Element, Form Classes, Form ID, Form Target, Form URL, Form Text.

### History Change Trigger

Fires on URL fragment changes or `pushState`/`replaceState`. Essential for SPAs.

Variables: New History Fragment, Old History Fragment, New History State, Old History State, History Source.

### Trigger Groups

Combine multiple triggers. Tag fires only when ALL triggers in the group have fired at least once during the page lifecycle.

## Variable Types

### Data Layer Variable

Reads a value from the dataLayer by key name. Use dot notation for nested values (e.g., `ecommerce.transaction_id`). Always use Version 2.

### JavaScript Variable

Reads a global JS variable (e.g., `document.title`, `navigator.language`).

### DOM Element Variable

Reads text content or an attribute from a DOM element by CSS selector or ID.

### URL Variable

Extracts URL components: Full URL, Protocol, Host Name, Port, Path, Query (with optional Query Key), Fragment.

### Constant Variable

Stores a fixed value. Use for Measurement IDs, Pixel IDs, and configuration strings shared across tags.

### Custom JavaScript Variable

Runs an anonymous function and returns its value:

```javascript
// Get viewport width
function() {
  return window.innerWidth;
}
```

```javascript
// Classify page type from URL
function() {
  var path = window.location.pathname;
  if (path === '/') return 'homepage';
  if (path.indexOf('/product/') === 0) return 'product';
  if (path.indexOf('/category/') === 0) return 'category';
  if (path.indexOf('/blog/') === 0) return 'blog';
  if (path.indexOf('/checkout') === 0) return 'checkout';
  return 'other';
}
```

```javascript
// Read a cookie
function() {
  var match = document.cookie.match(new RegExp('(^| )user_segment=([^;]+)'));
  return match ? match[2] : undefined;
}
```

### Lookup Table Variable

Maps input values (from another variable) to output values. Example: Page Path `/` maps to `Homepage`, `/pricing` to `Pricing`.

### RegEx Table Variable

Like Lookup Table but uses regex patterns. Example: `^/product/.*` maps to `Product Page`. Supports capture groups and case sensitivity settings.

## Tag Types

### Google Tag

Sets up the GA4 measurement stream (it replaced the old "GA4 Configuration" tag; existing ones were migrated automatically). Fire on Initialization - All Pages.

| Setting | Description |
|---------|-------------|
| Tag ID | `G-XXXXXXXXXX` (use a Constant variable) |
| Configuration settings | Key/value pairs such as `send_page_view`, `debug_mode`, `user_id` (or a "Google Tag: Configuration Settings" variable) |
| Shared event settings | Parameters sent with every event (or a "Google Tag: Event Settings" variable) |

### GA4 Event Tag

Sends a custom event to GA4.

| Setting | Description |
|---------|-------------|
| Measurement ID | `G-XXXXXXXXXX` (same as the Google tag) |
| Event Name | GA4 event name (e.g., `generate_lead`) |
| Event Parameters | Key-value pairs (e.g., `transaction_id`, `value`) |

### Custom HTML Tag

Runs arbitrary HTML/JavaScript. Always wrap in try/catch:

```html
<script>
  (function() {
    try {
      thirdPartySDK.track('event', { value: {{DLV - Value}} });
    } catch (e) {
      console.warn('GTM Custom HTML error:', e);
    }
  })();
</script>
```

### Custom Image Tag

Fires a pixel request (1x1 image). Configure Image URL with tracking parameters. Enable cache busting.

## Built-In Variables

### Click Variables

Click Element, Click Classes, Click ID, Click Target, Click URL, Click Text

### Form Variables

Form Element, Form Classes, Form ID, Form Target, Form URL, Form Text

### Page Variables

Page URL, Page Hostname, Page Path, Referrer

### Scroll Variables

Scroll Depth Threshold, Scroll Depth Units, Scroll Direction

### Video Variables

Video Provider, Video Status, Video URL, Video Title, Video Duration, Video Current Time, Video Percent, Video Visible

### Utility Variables

Event, Environment Name, Container ID, Container Version, HTML ID, Random Number, Debug Mode

## Debug Mode

### GTM Preview/Debug

Click "Preview" in GTM workspace. Tag Assistant opens and shows:
- Tags Fired / Tags Not Fired per event
- dataLayer state at each event
- Variables and resolved values

### Console Inspection

```javascript
// View entire dataLayer
console.table(dataLayer);

// Filter for specific events
dataLayer.filter(function(item) { return item.event === 'purchase'; });

// Watch pushes in real time
(function() {
  var orig = dataLayer.push;
  dataLayer.push = function() {
    console.log('dataLayer.push:', arguments[0]);
    return orig.apply(dataLayer, arguments);
  };
})();
```

### GA4 DebugView

Add `debug_mode: true` to your Google tag's configuration settings, then view events at GA4 Admin > DebugView.

### Network Tab

Filter by `collect` in DevTools Network tab to see GA4 hits. Verify payload parameters.

### Verify from the data (enhanced when connected)

If Cogny isn't connected, skip this and note what connecting adds.

- **GA4:** right after publishing, `tool_run_realtime_report` (`property_id`,
  `metrics: [eventCount]`, `dimensions: [eventName]`). The new event should appear within
  minutes of a test conversion. Missing: back to Preview.
- **Clarity:** a day after publishing a Custom HTML tag, `get_live_insights`
  (`num_of_days: 1`, `metrics: [Script Error Count]`, `dimensions: [URL]`). A jump on the
  pages the tag fires on means the tag throws.

### Building in the connected container (writes, asks first)

If Cogny isn't connected, skip this and note what connecting adds.

Every call below changes the container. Show the exact name, type and parameters, and
wait for a yes before each batch. Never publish without a separate yes.

1. `tool_create_workspace` (`account_id`, `container_id`, `name`): work in a feature
   workspace, not Default.
2. `tool_create_variable` (`…`, `workspace_id`, `name`, `variable_type`, `parameters`).
3. `tool_create_trigger` (`…`, `workspace_id`, `name`, `trigger_type`, `parameters`).
4. `tool_create_tag` (`…`, `workspace_id`, `name`, `tag_type`, `parameters`,
   `firing_trigger_ids`).
5. Ask the user to test in GTM Preview, then `tool_create_version` (`…`, `workspace_id`,
   `name`, `notes`).
6. `tool_publish_version` (`account_id`, `container_id`, `version_id`) only on an explicit
   "publish".

## Best Practices

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tags | `[Platform] - [Action] - [Detail]` | `GA4 - Event - Purchase` |
| Triggers | `[Type] - [Condition]` | `CE - form_submit` |
| Variables | `[Type prefix] - [Name]` | `DLV - Transaction ID` |
| Custom Events | snake_case | `generate_lead` |
| Folders | By platform or function | `GA4`, `Meta`, `Consent` |

### Folder Organization

```
GA4/
  Google Tag - G-XXXX - All Pages
  GA4 - Event - Purchase
  GA4 - Event - Add to Cart
Meta/
  Meta - Pixel - Base Code
  Meta - Event - Purchase
Consent/
  HTML - Consent Banner Init
  HTML - Consent Mode Update
```

### Workspace Management

- Use feature workspaces for each project (e.g., `Q1-2025-GA4-ecommerce`)
- Always Preview before creating a version
- Delete or merge unused workspaces

### Version Control

- Create a version before and after significant changes
- Write descriptive version names: "v42 - Added GA4 e-commerce checkout funnel"
- Roll back if issues arise post-publish

### Tag Sequencing

Use Tag Sequencing to ensure setup tags fire before dependent tags. Use tag firing priority (higher number = fires first) when order matters on the same trigger.

### Consent Mode v2

Consent is set with the `gtag('consent', ...)` command, not a dataLayer event. A `dataLayer.push({event: 'consent_default', consent: {...}})` does nothing for consent mode. Put the default above the GTM snippet (or use a CMP template / consent-mode template on the **Consent Initialization** trigger, which calls `setDefaultConsentState` / `updateConsentState`).

```javascript
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

// Default (before user choice)
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'analytics_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied'
});

// After user grants consent (from the banner's callback)
gtag('consent', 'update', {
  'ad_storage': 'granted',
  'analytics_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted'
});
```

## Common Mistakes

### 1. Race Conditions

Tags fire before dataLayer contains required data. Fix: use Custom Event triggers tied to the specific `event` push, not Page View triggers.

### 2. Incorrect Trigger Firing

Tags fire on all pages instead of specific ones. Fix: always add trigger filters (e.g., Page Path equals `/thank-you`).

### 3. Missing ecommerce Null Reset

Stale data from previous pushes contaminates events. Fix: always `dataLayer.push({ ecommerce: null })` before ecommerce events.

### 4. Duplicate Tags

Same event sent multiple times. Causes: multiple triggers, conditions too broad, wrong firing option. Fix: use "Once per Page" or review trigger conditions.

### 5. Custom HTML Breaking Pages

JS errors in Custom HTML block other tags. Fix: wrap all Custom HTML in try/catch.

### 6. Data Layer Variable Returns Undefined

Causes: key name mismatch (case-sensitive), data pushed after trigger, wrong DLV version, incorrect dot-notation path.

### 7. SPA Page Views Not Tracked

Route changes not captured. Fix: use History Change trigger or push custom `page_view` events on route change:

```javascript
// Next.js App Router
'use client';
import { usePathname } from 'next/navigation';
import { useEffect } from 'react';

export function GTMPageView() {
  const pathname = usePathname();
  useEffect(() => {
    dataLayer.push({
      'event': 'page_view',
      'page_location': window.location.href,
      'page_title': document.title
    });
  }, [pathname]);
  return null;
}
```

### 8. Cross-Domain Tracking Issues

Users counted as new sessions across domains. Fix: configure cross-domain linker in the Google tag settings or GA4 Admin > Data Streams > Configure your domains.

### 9. Preview Traffic Inflating Analytics

Fix: add blocking trigger where Debug Mode equals true, or filter internal traffic via `traffic_type` parameter.

## Resources

- **GTM Developer Guide:** https://developers.google.com/tag-platform/tag-manager
- **GA4 Event Reference:** https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- **GTM Community Gallery:** https://tagmanager.google.com/gallery
- **Consent Mode:** https://developers.google.com/tag-platform/security/guides/consent
- **Full Cogny Docs:** https://cogny.com/docs/gtm-event-tracking
