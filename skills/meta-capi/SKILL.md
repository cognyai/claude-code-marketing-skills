---
name: meta-capi
description: Meta Conversions API (CAPI) Setup Reference — architecture, event types, customer information hashing, deduplication, implementation examples, AEM, and testing
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<query or topic>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Meta Ads tools (when connected via Cogny MCP)
  - mcp__cogny__meta_ads__tool_get_pixels
  - mcp__cogny__meta_ads__tool_get_insights
  - mcp__cogny__meta_ads__tool_get_campaigns
  - mcp__cogny__meta_ads__tool_get_ad_sets
  - mcp__cogny__meta_ads__tool_get_ads
  - mcp__cogny__meta_ads__tool_get_custom_audiences
  - mcp__cogny__meta_ads__tool_list_ad_accounts
---

# Meta Conversions API (CAPI) Setup Reference

Complete technical reference for Meta Conversions API: architecture, all standard event types with parameters, customer information hashing, implementation methods, event deduplication, testing, and Aggregated Event Measurement.

Full docs: https://cogny.com/docs/meta-conversions-api

## Usage

```
/meta-capi                          # Full CAPI overview
/meta-capi deduplication            # Event dedup strategy
/meta-capi purchase event           # Purchase event parameters
/meta-capi emq                      # Improve Event Match Quality
/meta-capi aem                      # Aggregated Event Measurement
/meta-capi node.js                  # Node.js implementation example
/meta-capi gtm server-side          # GTM SS container setup
```

## Instructions

You are a Meta Conversions API expert. Use this reference to help users implement CAPI correctly, debug event tracking issues, improve Event Match Quality, configure deduplication, and understand Aggregated Event Measurement.

When the user asks a question, find the relevant section below and provide precise, actionable answers with ready-to-use code examples.

If the user provides a specific topic as an argument, focus on that area. Otherwise, provide an overview of the CAPI architecture and key implementation steps.

If Cogny MCP tools are available, use them to inspect the user's actual Pixel configuration, ad account setup, and campaign data to provide contextual recommendations.

---

## Architecture: Browser Pixel vs Server-Side CAPI

```
                         User's Browser
                        +------------------------------+
                        |  Meta Pixel (fbevents.js)     |
                        |  - Fires on page interaction  |
                        |  - Sets _fbp / _fbc cookies   |
                        |  - Sends event_id for dedup   |
                        +----------+-------------------+
                                   |  HTTPS (browser -> Meta)
                                   v
                        +------------------------------+
                        |       Meta Servers            |
                        |  - Receives Pixel events      |
                        |  - Receives CAPI events       |
                        |  - Deduplicates via event_id  |
                        |  - Matches users (EMQ)        |
                        |  - Feeds ad optimization      |
                        +------------------------------+
                                   ^
                                   |  HTTPS (server -> Meta)
                        +----------+-------------------+
                        |  Your Server / GTM SS         |
                        |  - Conversions API endpoint   |
                        |  - POST /v21.0/{pixel_id}/    |
                        |    events                     |
                        |  - Hashes PII before sending  |
                        |  - Sends same event_id        |
                        +------------------------------+
```

**Why both matter:**

- **Pixel only:** Subject to ad blockers (15-30% signal loss), ITP cookie expiry (7-day cap on Safari), and network failures.
- **CAPI only:** Misses real-time browser interactions and cannot set first-party cookies.
- **Pixel + CAPI (recommended):** Redundant data paths with deduplication. Recovers 10-25% of lost conversions.

## Standard Events

### Purchase

Fired when a transaction is completed.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | **Yes** | Total transaction value |
| `currency` | string | **Yes** | ISO 4217 code (e.g., `USD`, `EUR`) |
| `content_ids` | array<string> | Recommended | Product IDs from catalog |
| `content_type` | string | Recommended | `product` or `product_group` |
| `contents` | array<object> | Recommended | Array of `{id, quantity, item_price}` |
| `content_name` | string | Optional | Product or page name |
| `content_category` | string | Optional | Product category |
| `num_items` | integer | Optional | Number of items |
| `order_id` | string | Optional | Internal order ID |

### AddToCart

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Recommended | Item value |
| `currency` | string | Recommended | ISO 4217 code |
| `content_ids` | array<string> | Recommended | Product IDs |
| `content_type` | string | Recommended | `product` or `product_group` |
| `contents` | array<object> | Recommended | `{id, quantity, item_price}` |
| `content_name` | string | Optional | Product name |
| `content_category` | string | Optional | Product category |

### InitiateCheckout

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Recommended | Cart value |
| `currency` | string | Recommended | ISO 4217 code |
| `content_ids` | array<string> | Recommended | Product IDs in cart |
| `content_type` | string | Recommended | `product` or `product_group` |
| `contents` | array<object> | Recommended | `{id, quantity, item_price}` |
| `num_items` | integer | Optional | Number of items |

### CompleteRegistration

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Optional | Registration value |
| `currency` | string | Optional | ISO 4217 code |
| `content_name` | string | Optional | Form or page name |
| `status` | string | Optional | Registration status |

### Lead

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Optional | Estimated lead value |
| `currency` | string | Optional | ISO 4217 code |
| `content_name` | string | Optional | Lead form name |
| `content_category` | string | Optional | Lead category |

### ViewContent

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Recommended | Content value |
| `currency` | string | Recommended | ISO 4217 code |
| `content_ids` | array<string> | Recommended | Content/product IDs |
| `content_type` | string | Recommended | `product` or `product_group` |
| `content_name` | string | Optional | Content name |
| `content_category` | string | Optional | Content category |

### Search

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search_string` | string | Recommended | The search query |
| `value` | float | Optional | Assigned value |
| `currency` | string | Optional | ISO 4217 code |
| `content_ids` | array<string> | Optional | Result IDs |
| `content_category` | string | Optional | Result category |

### AddPaymentInfo

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Optional | Cart value |
| `currency` | string | Optional | ISO 4217 code |
| `content_ids` | array<string> | Optional | Product IDs |
| `content_type` | string | Optional | `product` or `product_group` |
| `content_category` | string | Optional | Payment method category |

### AddToWishlist

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Optional | Item value |
| `currency` | string | Optional | ISO 4217 code |
| `content_ids` | array<string> | Optional | Product IDs |
| `content_name` | string | Optional | Product name |
| `content_category` | string | Optional | Product category |

### Contact

Fired when a user initiates contact (phone, SMS, email, chat). No required or recommended parameters beyond customer information.

### CustomizeProduct

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content_ids` | array<string> | Optional | Product IDs |
| `content_type` | string | Optional | `product` or `product_group` |
| `content_name` | string | Optional | Product name |

### Donate

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Recommended | Donation amount |
| `currency` | string | Recommended | ISO 4217 code |

### FindLocation

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content_name` | string | Optional | Location name or query |
| `content_category` | string | Optional | Location type |

### Schedule

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content_name` | string | Optional | Appointment type |
| `content_category` | string | Optional | Service category |

### StartTrial

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | Recommended | Predicted trial value |
| `currency` | string | Recommended | ISO 4217 code |
| `content_name` | string | Optional | Trial plan name |

### SubmitApplication

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content_name` | string | Optional | Application type |
| `content_category` | string | Optional | Application category |

### Subscribe

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | float | **Yes** | Subscription value |
| `currency` | string | **Yes** | ISO 4217 code |
| `content_name` | string | Optional | Plan name |

## Custom Events

Custom events cover actions not mapped to standard events. Used for audience building and custom conversions but cannot power standard optimization objectives.

**Naming rules:**

- Max 40 characters
- Lowercase letters, numbers, underscores only
- Must not start with a number
- Must not use reserved names (standard event names, `fb_`, `_fb` prefixes)
- Examples: `qualified_lead`, `demo_booked`, `pricing_page_scroll_50`

## Customer Information Parameters

Customer info parameters enable Meta to match events to user profiles. Higher match quality improves ad optimization.

### Available Parameters

| Parameter | Key | Format Before Hashing |
|-----------|-----|-----------------------|
| Email | `em` | Lowercase, trim whitespace |
| Phone | `ph` | Digits only with country code (e.g., `14155551234`) |
| First Name | `fn` | Lowercase, trim, no punctuation |
| Last Name | `ln` | Lowercase, trim, no punctuation |
| City | `ct` | Lowercase, trim, no punctuation, no spaces |
| State | `st` | 2-letter abbreviation, lowercase (e.g., `ca`) |
| Zip Code | `zp` | Trim. US: 5-digit only |
| Country | `country` | 2-letter ISO 3166-1 alpha-2, lowercase (e.g., `us`) |
| Date of Birth | `db` | `YYYYMMDD` format |
| Gender | `ge` | Single letter: `m` or `f` |
| External ID | `external_id` | Any string. Hash recommended but not required |

### Hashing Requirements

All parameters except `external_id` **must** be SHA-256 hashed before sending via CAPI. The Pixel hashes automatically; CAPI does not.

**Procedure:** Normalize (lowercase, trim) -> SHA-256 -> lowercase hex string (64 chars)

```javascript
// Node.js
const crypto = require('crypto');
function hashForMeta(value) {
  if (!value) return null;
  return crypto.createHash('sha256')
    .update(value.toString().trim().toLowerCase())
    .digest('hex');
}
```

```python
# Python
import hashlib
def hash_for_meta(value):
    if not value:
        return None
    return hashlib.sha256(str(value).strip().lower().encode('utf-8')).hexdigest()
```

**Common mistakes:**

- Hashing before normalizing (uppercase in input)
- Double-hashing an already-hashed value
- Including whitespace in hash input
- Missing country code on phone numbers
- Using MD5 instead of SHA-256

### Event Match Quality (EMQ)

EMQ is a 1-10 score indicating how well Meta matched an event to a user profile.

| EMQ Score | Quality | Impact |
|-----------|---------|--------|
| 1-3 | Poor | Most events unmatched |
| 4-5 | Fair | Partial matching |
| 6-7 | Good | Strong matching |
| 8-10 | Excellent | Full optimization potential |

**How to improve EMQ:**

1. Send `em` (email) with every event -- single biggest impact
2. Add `ph` (phone) as second identifier
3. Include `fn` + `ln` to disambiguate common emails
4. Pass `external_id` for cross-device matching
5. Forward `fbp` and `fbc` cookies from browser to server
6. Ensure correct normalization and hashing

## Implementation Methods

### Direct API Integration

**Endpoint:** `POST https://graph.facebook.com/v21.0/{pixel_id}/events`

**Auth:** `access_token` query parameter (System User token with `ads_management` permission)

#### Node.js Example

```javascript
const crypto = require('crypto');

const PIXEL_ID = 'YOUR_PIXEL_ID';
const ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN';

function hash(value) {
  if (!value) return undefined;
  return crypto.createHash('sha256')
    .update(value.toString().trim().toLowerCase())
    .digest('hex');
}

async function sendEvent(eventName, eventData, userData, eventId = null) {
  const payload = {
    data: [{
      event_name: eventName,
      event_time: Math.floor(Date.now() / 1000),
      event_id: eventId || crypto.randomUUID(),
      event_source_url: eventData.source_url,
      action_source: 'website',
      user_data: {
        em: hash(userData.email),
        ph: hash(userData.phone),
        fn: hash(userData.firstName),
        ln: hash(userData.lastName),
        ct: hash(userData.city),
        st: hash(userData.state),
        zp: hash(userData.zipCode),
        country: hash(userData.country),
        external_id: hash(userData.externalId),
        client_ip_address: userData.ipAddress,
        client_user_agent: userData.userAgent,
        fbp: userData.fbp,   // raw cookie value, not hashed
        fbc: userData.fbc,   // raw cookie value, not hashed
      },
      custom_data: eventData.customData || {},
    }],
  };

  const url = `https://graph.facebook.com/v21.0/${PIXEL_ID}/events?access_token=${ACCESS_TOKEN}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(`CAPI error: ${JSON.stringify(err)}`);
  }
  return response.json();
}

// Example: Purchase event
await sendEvent('Purchase', {
  source_url: 'https://example.com/checkout/thank-you',
  customData: {
    value: 99.99,
    currency: 'USD',
    content_ids: ['SKU-123', 'SKU-456'],
    content_type: 'product',
    order_id: 'ORDER-789',
    num_items: 2,
  },
}, {
  email: 'john@example.com',
  phone: '14155551234',
  firstName: 'John',
  lastName: 'Doe',
  ipAddress: '203.0.113.50',
  userAgent: 'Mozilla/5.0 ...',
  fbp: 'fb.1.1612345678901.1234567890',
  fbc: 'fb.1.1612345678901.AbCdEfGhIjKl',
  externalId: 'user-12345',
}, 'evt_purchase_abc123');
```

#### Python Example

```python
import hashlib, time, uuid, requests

PIXEL_ID = 'YOUR_PIXEL_ID'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

def hash_value(value):
    if not value:
        return None
    return hashlib.sha256(str(value).strip().lower().encode('utf-8')).hexdigest()

def send_event(event_name, event_data, user_data, event_id=None):
    url = f'https://graph.facebook.com/v21.0/{PIXEL_ID}/events'
    payload = {
        'data': [{
            'event_name': event_name,
            'event_time': int(time.time()),
            'event_id': event_id or str(uuid.uuid4()),
            'event_source_url': event_data.get('source_url'),
            'action_source': 'website',
            'user_data': {k: v for k, v in {
                'em': hash_value(user_data.get('email')),
                'ph': hash_value(user_data.get('phone')),
                'fn': hash_value(user_data.get('first_name')),
                'ln': hash_value(user_data.get('last_name')),
                'ct': hash_value(user_data.get('city')),
                'st': hash_value(user_data.get('state')),
                'zp': hash_value(user_data.get('zip_code')),
                'country': hash_value(user_data.get('country')),
                'external_id': hash_value(user_data.get('external_id')),
                'client_ip_address': user_data.get('ip_address'),
                'client_user_agent': user_data.get('user_agent'),
                'fbp': user_data.get('fbp'),
                'fbc': user_data.get('fbc'),
            }.items() if v is not None},
            'custom_data': event_data.get('custom_data', {}),
        }],
        'access_token': ACCESS_TOKEN,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

# Example: Purchase event
send_event('Purchase', {
    'source_url': 'https://example.com/checkout/thank-you',
    'custom_data': {
        'value': 99.99,
        'currency': 'USD',
        'content_ids': ['SKU-123'],
        'content_type': 'product',
    },
}, {
    'email': 'john@example.com',
    'phone': '14155551234',
    'first_name': 'John',
    'last_name': 'Doe',
    'ip_address': '203.0.113.50',
    'user_agent': 'Mozilla/5.0 ...',
    'fbp': 'fb.1.1612345678901.1234567890',
    'external_id': 'user-12345',
}, event_id='evt_purchase_abc123')
```

### GTM Server-Side Container

1. Deploy a GTM server-side container (Cloud Run, AWS, etc.)
2. Create a **Meta Conversions API tag** in your server container
3. Configure:
   - **Pixel ID** and **API Access Token**
   - **Action Source:** `website`
   - **Event Name:** Map from incoming event
   - **User Data:** Map email, phone, etc. from event data
   - **Event ID:** Must match browser Pixel's `eventID` for dedup
4. Set trigger on relevant forwarded events

**Key tag fields:**

```
Tag Type:          Meta Conversions API
Pixel ID:          {{Meta Pixel ID}}
API Access Token:  {{Meta CAPI Token}}
Event Name:        {{Event Name}}
Action Source:     website

User Data:
  Email:           {{User Email - Hashed}}
  Phone:           {{User Phone - Hashed}}
  IP Address:      {{Client IP}}  (auto-populated in SS GTM)
  User Agent:      {{Client User Agent}}  (auto-populated)
  FBP:             {{FBP Cookie}}
  FBC:             {{FBC Cookie}}

Event Parameters:
  Event ID:        {{Event ID}}  (must match browser Pixel eventID)
  Event Source URL: {{Page URL}}
  Value:           {{Event Value}}
  Currency:        {{Event Currency}}
```

### Partner Integrations

| Platform | Method | Notes |
|----------|--------|-------|
| **Shopify** | Native Meta channel app | Auto dedup; standard e-commerce events |
| **WooCommerce** | Facebook for WooCommerce plugin | Requires configuration |
| **BigCommerce** | Native Meta integration | Via app |
| **Magento** | Meta Business Extension | Server-side events |

## Event Deduplication

When running Pixel + CAPI, the same conversion can be reported twice. Meta deduplicates using `event_id` + `event_name`.

### How It Works

1. Browser Pixel fires with `eventID: "evt_abc123"` and `Purchase`
2. Server sends CAPI with `event_id: "evt_abc123"` and `Purchase`
3. Meta matches on both fields, counts one conversion
4. If one path fails (ad blocker, server error), the other still delivers

### Dedup Pattern

```javascript
// Browser: generate event_id, fire Pixel, send to server
const eventId = crypto.randomUUID();

fbq('track', 'Purchase', {
  value: 99.99,
  currency: 'USD',
}, { eventID: eventId });

navigator.sendBeacon('/api/meta-capi', JSON.stringify({
  event_name: 'Purchase',
  event_id: eventId,
  custom_data: { value: 99.99, currency: 'USD' },
}));

// Server: forward to CAPI with same event_id
```

### fbp and fbc Cookies

**`_fbp`** (Facebook Browser ID): Set by Pixel on first load. Format: `fb.1.{timestamp}.{random}`. Persists 90 days. Send raw (not hashed).

**`_fbc`** (Facebook Click ID): Set on Meta ad click. Format: `fb.1.{timestamp}.{fbclid}`. If missing, construct from URL: `fb.1.{timestamp_ms}.{fbclid}`. Send raw (not hashed).

```javascript
// Extract from cookies server-side
const fbp = req.cookies['_fbp'] || null;
const fbc = req.cookies['_fbc'] || null;

// Construct fbc from fbclid if cookie missing
function constructFbc(fbclid) {
  return fbclid ? `fb.1.${Date.now()}.${fbclid}` : null;
}
```

### Common Dedup Failures

| Problem | Fix |
|---------|-----|
| Different event_id on Pixel vs CAPI | Generate in browser, pass to server |
| event_id missing from Pixel | Add `{ eventID: id }` as 4th arg to `fbq('track')` |
| event_id missing from CAPI | Include event_id in payload |
| Different event_name casing | Use exact standard names (`Purchase`, not `purchase`) |
| CAPI sent hours later | Send within minutes, not in delayed batches (48h dedup window) |

## Testing and Validation

### Test Events Tool

1. Events Manager > Your Pixel > **Test Events** tab
2. Copy the **Test Event Code** (e.g., `TEST12345`)
3. Add `test_event_code` to your CAPI payload
4. Send events -- they appear in real time
5. **Remove test_event_code before production** (test events are not processed for ads)

```javascript
const payload = {
  data: [{ /* event data */ }],
  test_event_code: 'TEST12345',
};
```

### Event Match Quality Dashboard

Events Manager > Data Sources > Your Pixel > **Event Match Quality**:

- Per-event EMQ scores
- Parameter frequency breakdown
- Improvement recommendations
- Trend over time

### Common Error Codes

| Code | Message | Fix |
|------|---------|-----|
| `190` | Invalid OAuth access token | Regenerate system user token |
| `100` | Invalid parameter | Check required: event_name, event_time, action_source, user_data |
| `2804003` | Timestamp too old | event_time must be within 7 days |
| `2804004` | Invalid event_time | Must be Unix seconds, not milliseconds |
| `2804001` | Missing user_data | Include at least one customer info parameter |
| `368` | Temporarily blocked | Rate limiting; use exponential backoff |
| `2804002` | Invalid action_source | Use: website, app, phone_call, chat, email, in_store, other |
| `803` | Permission denied | System user needs ads_management permission |

## Aggregated Event Measurement (AEM)

Meta's protocol for measuring events from iOS 14.5+ users who opted out of tracking via ATT.

### Key Facts

- **8-event limit** per domain, ranked by priority
- **72-hour delay** for opted-out user data
- **1-day click attribution** (vs. standard 7-day click / 1-day view)
- **Statistical modeling** used to estimate opted-out conversions
- Requires **domain verification** in Business Settings

### Recommended Event Priority (E-commerce)

| Priority | Event |
|----------|-------|
| 1 (highest) | Purchase |
| 2 | Subscribe |
| 3 | StartTrial |
| 4 | InitiateCheckout |
| 5 | AddPaymentInfo |
| 6 | AddToCart |
| 7 | CompleteRegistration |
| 8 (lowest) | ViewContent |

### Recommended Event Priority (Lead Gen)

| Priority | Event |
|----------|-------|
| 1 (highest) | Purchase |
| 2 | Lead |
| 3 | SubmitApplication |
| 4 | Schedule |
| 5 | CompleteRegistration |
| 6 | Contact |
| 7 | ViewContent |
| 8 (lowest) | Search |

### Domain Verification

1. Business Settings > Brand Safety > Domains
2. Add domain, verify via DNS TXT record (recommended), HTML file, or meta tag
3. Configure 8 events in Events Manager > Aggregated Event Measurement

### Impact on Reporting

| Metric | Pre-iOS 14.5 | With AEM |
|--------|--------------|----------|
| Attribution window | 28d click, 7d view | 7d click, 1d view |
| Reporting delay | Real-time | Up to 72 hours |
| Breakdowns | Full | Limited |
| Conversion count | Exact | Modeled for opted-out |
| Optimization events | Unlimited | 8 per domain |

**Mitigations:**

- Use CAPI to maximize EMQ (partially offsets ATT opt-outs)
- Prioritize 8 most important events
- Expect 15-30% iOS conversion underreporting
- Consider broad targeting strategies

## Resources

- **Meta CAPI Docs:** https://developers.facebook.com/docs/marketing-api/conversions-api
- **CAPI Setup Guide:** https://developers.facebook.com/docs/marketing-api/conversions-api/get-started
- **EMQ Best Practices:** https://developers.facebook.com/docs/marketing-api/conversions-api/best-practices
- **Standard Events Reference:** https://developers.facebook.com/docs/meta-pixel/reference
- **Full Cogny Docs:** https://cogny.com/docs/meta-conversions-api
