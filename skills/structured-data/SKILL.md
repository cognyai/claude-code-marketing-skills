---
name: structured-data
description: Schema.org Structured Data Reference — JSON-LD examples for every major schema type, rich results eligibility, testing tools, and implementation patterns
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<schema type or topic>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
  # Search Console tools (when connected via Cogny MCP)
  - mcp__cogny__search_console__tool_list_properties
  - mcp__cogny__search_console__tool_get_search_analytics
  - mcp__cogny__search_console__tool_inspect_url
---

# Schema.org Structured Data Reference

Complete reference for Schema.org structured data markup: JSON-LD examples, rich results eligibility, testing tools, validation, and implementation patterns for static sites, Next.js, React, and WordPress.

Full docs: https://cogny.com/docs/structured-data-reference

## Usage

```
/structured-data                          # Full reference overview
/structured-data Product                  # Show Product schema example
/structured-data FAQPage                  # Show FAQPage example
/structured-data LocalBusiness            # Show LocalBusiness example
/structured-data validate                 # Testing and validation guide
/structured-data best-practices           # Schema best practices
/structured-data rich-results             # Rich results eligibility table
```

## Instructions

You are a Schema.org structured data expert. Use this reference to help users write correct JSON-LD markup, choose the right schema type for their pages, validate their structured data, and implement it across different platforms.

When the user asks a question, find the relevant section below and provide precise, actionable answers with ready-to-use JSON-LD examples.

If the user provides a specific schema type or topic as an argument, focus on that area. Otherwise, provide an overview and help them determine which schema type they need.

When Search Console MCP tools are available, use them to:
- Check which pages have rich results via `tool_get_search_analytics` (filter by search appearance)
- Inspect specific URLs for structured data issues via `tool_inspect_url`
- List properties to identify which sites to audit via `tool_list_properties`

---

## What Structured Data Does

Structured data is machine-readable markup that tells search engines, voice assistants, and AI systems exactly what your page content means. You declare it explicitly using the Schema.org vocabulary.

**Benefits:**
- **Rich results** — star ratings, prices, FAQ accordions, how-to steps, event listings in Google Search
- **Knowledge panels** — branded panels for organizations, people, and products
- **Voice search** — direct answers in Google Assistant and other voice interfaces
- **AI citations** — LLMs and AI search engines (Google AI Overviews, Bing Copilot, Perplexity) use structured data to surface and attribute information

## Formats

Three formats exist. Google explicitly recommends JSON-LD.

### JSON-LD (Recommended)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Corp"
}
</script>
```

**Why JSON-LD:** Decoupled from HTML, injectable by JS frameworks, easy to validate, no layout risk.

### Microdata

Inline HTML attributes (`itemscope`, `itemtype`, `itemprop`). Use only in legacy systems that cannot add `<script>` tags.

### RDFa

Inline attributes (`vocab`, `typeof`, `property`). Rare on the web — more common in XML/SVG contexts.

**Bottom line:** Use JSON-LD for all new implementations.

## Schema Types with JSON-LD Examples

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Cogny AI",
  "url": "https://cogny.com",
  "logo": "https://cogny.com/images/logo.png",
  "sameAs": [
    "https://twitter.com/cognyai",
    "https://linkedin.com/company/cogny",
    "https://github.com/cognyai"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+46-8-123-4567",
    "contactType": "customer service",
    "availableLanguage": ["English", "Swedish"]
  },
  "foundingDate": "2023",
  "numberOfEmployees": {
    "@type": "QuantitativeValue",
    "value": 15
  }
}
```

**Required:** `name` | **Recommended:** `url`, `logo`, `sameAs`, `contactPoint`
**Rich result:** Knowledge panel

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Nordic Coffee Roasters",
  "image": "https://example.com/photos/storefront.jpg",
  "url": "https://nordiccoffee.se",
  "telephone": "+46-8-765-4321",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Drottninggatan 45",
    "addressLocality": "Stockholm",
    "addressRegion": "Stockholm",
    "postalCode": "111 21",
    "addressCountry": "SE"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 59.3293,
    "longitude": 18.0686
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "09:00",
      "closes": "16:00"
    }
  ]
}
```

**Required:** `name`, `address` | **Recommended:** `geo`, `openingHoursSpecification`, `telephone`, `priceRange`, `image`
**Rich result:** Local pack, knowledge panel with map/hours/phone

### Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Wireless Noise-Cancelling Headphones",
  "image": [
    "https://example.com/photos/headphones-front.jpg",
    "https://example.com/photos/headphones-side.jpg"
  ],
  "description": "Premium wireless headphones with active noise cancellation, 30-hour battery life, and multipoint Bluetooth connectivity.",
  "sku": "WH-1000XM5",
  "brand": {
    "@type": "Brand",
    "name": "AudioTech"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/headphones-wh1000xm5",
    "priceCurrency": "USD",
    "price": "349.99",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "AudioTech Store"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "bestRating": "5",
    "reviewCount": "2847"
  }
}
```

**Required for rich results:** `name`, `image`, `offers` (with `price`, `priceCurrency`, `availability`)
**Recommended:** `sku`, `brand`, `aggregateRating`, `description`
**Rich result:** Product snippet with price, availability, star rating

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is structured data?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Structured data is machine-readable markup added to HTML pages that helps search engines understand your content. It uses the Schema.org vocabulary and is typically implemented in JSON-LD format."
      }
    },
    {
      "@type": "Question",
      "name": "Does structured data improve SEO rankings?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Structured data does not directly affect rankings. However, it enables rich results that significantly improve click-through rates, which can indirectly improve performance through higher engagement signals."
      }
    }
  ]
}
```

**Required:** `mainEntity` array with `Question` items containing `acceptedAnswer`
**Rich result:** Expandable FAQ accordion (up to 10 questions)

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Implement JSON-LD Structured Data",
  "description": "A step-by-step guide to adding Schema.org JSON-LD structured data to your website.",
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "tool": [
    { "@type": "HowToTool", "name": "Text editor or CMS" },
    { "@type": "HowToTool", "name": "Google Rich Results Test" }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Choose your schema type",
      "text": "Identify the primary content type of your page and look up the required properties at schema.org.",
      "url": "https://example.com/guide#step1",
      "image": "https://example.com/images/step1.png"
    },
    {
      "@type": "HowToStep",
      "name": "Write the JSON-LD block",
      "text": "Create a JSON-LD script block with @context, @type, and all required properties.",
      "url": "https://example.com/guide#step2",
      "image": "https://example.com/images/step2.png"
    },
    {
      "@type": "HowToStep",
      "name": "Insert into your page",
      "text": "Place the script tag in the head or body of your HTML document.",
      "url": "https://example.com/guide#step3",
      "image": "https://example.com/images/step3.png"
    },
    {
      "@type": "HowToStep",
      "name": "Validate with testing tools",
      "text": "Run your page through the Google Rich Results Test and Schema Markup Validator.",
      "url": "https://example.com/guide#step4",
      "image": "https://example.com/images/step4.png"
    }
  ]
}
```

**Required:** `name`, `step` (with `text` each) | **Recommended:** `image` per step, `totalTime`, `tool`
**Rich result:** Numbered step-by-step instructions with images

### Article / BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Complete Guide to Schema.org Structured Data",
  "description": "Learn how to implement structured data markup to earn rich results in Google Search.",
  "image": [
    "https://example.com/images/guide-16x9.jpg",
    "https://example.com/images/guide-4x3.jpg",
    "https://example.com/images/guide-1x1.jpg"
  ],
  "author": {
    "@type": "Person",
    "name": "Anna Lindqvist",
    "url": "https://example.com/authors/anna-lindqvist"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Publishing",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" }
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-02-10",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/guides/structured-data"
  }
}
```

Use `Article` for news, `BlogPosting` for blogs, `NewsArticle` for Google News publishers.

**Required:** `headline`, `image`, `datePublished`, `author`
**Rich result:** Article carousel, Top Stories (NewsArticle), author/date in results

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Docs", "item": "https://example.com/docs" },
    { "@type": "ListItem", "position": 3, "name": "Structured Data", "item": "https://example.com/docs/structured-data" }
  ]
}
```

**Required:** `itemListElement` with `position`, `name`, `item`
**Rich result:** Breadcrumb trail replaces URL in search results

### Review / AggregateRating

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Cloud Analytics Platform",
  "review": [
    {
      "@type": "Review",
      "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
      "author": { "@type": "Person", "name": "Erik Johansson" },
      "reviewBody": "Transformed our data pipeline. The BigQuery integration is seamless.",
      "datePublished": "2025-01-20"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "bestRating": "5",
    "ratingCount": "312",
    "reviewCount": "189"
  }
}
```

Reviews must be nested inside the item they review — standalone Review markup without context will not generate rich results.

**Required:** `ratingValue`, `bestRating`, `author` (Review); `ratingValue`, `ratingCount` (AggregateRating)
**Rich result:** Star rating snippet

### Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Nordic Growth Marketing Summit 2025",
  "description": "Two-day conference on performance marketing and AI-driven analytics.",
  "startDate": "2025-09-15T09:00:00+02:00",
  "endDate": "2025-09-16T17:00:00+02:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Stockholm Waterfront Congress Centre",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Nils Ericsons Plan 4",
      "addressLocality": "Stockholm",
      "postalCode": "111 64",
      "addressCountry": "SE"
    }
  },
  "performer": { "@type": "Organization", "name": "Cogny AI" },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/tickets",
    "price": "4999",
    "priceCurrency": "SEK",
    "availability": "https://schema.org/InStock",
    "validFrom": "2025-03-01T00:00:00+01:00"
  },
  "organizer": { "@type": "Organization", "name": "Growth Hackers Stockholm", "url": "https://growthhackers.se" },
  "image": "https://example.com/images/summit-2025.jpg"
}
```

**Required:** `name`, `startDate`, `location` | **Recommended:** `endDate`, `offers`, `performer`, `eventStatus`, `image`
**Rich result:** Event listing with date/location/ticket; event pack in SERP

### VideoObject

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to Set Up GA4 BigQuery Export",
  "description": "Step-by-step tutorial for connecting GA4 to BigQuery.",
  "thumbnailUrl": "https://example.com/thumbnails/ga4-setup.jpg",
  "uploadDate": "2025-01-10",
  "duration": "PT12M30S",
  "contentUrl": "https://example.com/videos/ga4-setup.mp4",
  "embedUrl": "https://youtube.com/embed/abc123",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": 15420
  }
}
```

**Required:** `name`, `thumbnailUrl`, `uploadDate` | **Recommended:** `description`, `duration`, `contentUrl` or `embedUrl`
**Rich result:** Video carousel, video thumbnail in search results

### SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Cogny Analytics Platform",
  "operatingSystem": "Web",
  "applicationCategory": "BusinessApplication",
  "description": "AI-powered analytics platform for automated growth insights.",
  "offers": { "@type": "Offer", "price": "99", "priceCurrency": "USD" },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "ratingCount": "156" },
  "screenshot": "https://example.com/images/dashboard.png"
}
```

**Required:** `name`, `offers` (with `price`, `priceCurrency`) | **Recommended:** `operatingSystem`, `applicationCategory`, `aggregateRating`
**Rich result:** Software snippet with rating and price

### Course

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Advanced BigQuery for Marketing Analytics",
  "description": "Learn to write efficient BigQuery SQL for GA4 data, build attribution models, and create automated reporting.",
  "provider": { "@type": "Organization", "name": "Cogny Academy", "sameAs": "https://cogny.com/academy" },
  "courseCode": "BQ-301",
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseSchedule": {
      "@type": "Schedule",
      "repeatFrequency": "P1W",
      "startDate": "2025-03-01",
      "endDate": "2025-04-15"
    }
  },
  "offers": { "@type": "Offer", "price": "499", "priceCurrency": "USD", "category": "Paid" }
}
```

**Required:** `name`, `description`, `provider` | **Recommended:** `offers`, `hasCourseInstance`
**Rich result:** Course listing with provider and enrollment info

### JobPosting

```json
{
  "@context": "https://schema.org",
  "@type": "JobPosting",
  "title": "Senior Growth Engineer",
  "description": "Build and optimize marketing analytics infrastructure including BigQuery pipelines, A/B testing, and automated reporting.",
  "datePosted": "2025-02-01",
  "validThrough": "2025-04-01T23:59:59+01:00",
  "employmentType": "FULL_TIME",
  "hiringOrganization": {
    "@type": "Organization",
    "name": "Cogny AI",
    "sameAs": "https://cogny.com",
    "logo": "https://cogny.com/images/logo.png"
  },
  "jobLocation": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Stockholm",
      "addressRegion": "Stockholm",
      "addressCountry": "SE"
    }
  },
  "jobLocationType": "TELECOMMUTE",
  "baseSalary": {
    "@type": "MonetaryAmount",
    "currency": "SEK",
    "value": { "@type": "QuantitativeValue", "minValue": 55000, "maxValue": 75000, "unitText": "MONTH" }
  },
  "applicantLocationRequirements": { "@type": "Country", "name": "Sweden" }
}
```

**Required:** `title`, `description`, `datePosted`, `hiringOrganization`, `jobLocation`
**Recommended:** `validThrough`, `employmentType`, `baseSalary`, `jobLocationType`
**Rich result:** Google Jobs listing with salary, location, apply button

## Testing and Validation

### Google Rich Results Test

**URL:** https://search.google.com/test/rich-results

Test individual pages or code snippets for rich result eligibility. Shows detected types, validation errors, and warnings.

### Schema Markup Validator

**URL:** https://validator.schema.org

Validates against the full Schema.org specification — catches structural errors the Rich Results Test may miss.

### Google Search Console Rich Results Report

**Location:** Search Console > Enhancements > [specific rich result type]

Aggregate data across your site: valid pages, error counts, specific error types. Updated daily.

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing field "image"` | Product/Article missing image | Add `image` with valid crawlable URL |
| `Invalid URL in field "url"` | Relative URL | Use fully qualified URLs (`https://...`) |
| `Missing field "author"` | Article/Review missing author | Add `author` as Person or Organization with `name` |
| `Invalid value in field "price"` | Currency symbol in price | Use numeric value only (`"349.99"` not `"$349.99"`) |
| `Invalid enum for "availability"` | Plain text instead of URL | Use `https://schema.org/InStock`, not `"In Stock"` |
| `Array expected, single value` | Single image instead of array | Wrap in array: `"image": ["https://..."]` |
| `datePublished is in the future` | Date set ahead of publish | Set to actual publication date |

## Best Practices

### One Primary Schema Type per Page

Match the primary schema type to the page purpose. Product pages use Product, blog posts use BlogPosting, FAQ pages use FAQPage. Combine with BreadcrumbList as a complementary type.

### Nesting vs. @graph

Nest when there is a parent-child relationship (Product > Offer). Use `@graph` for independent entities on the same page:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "BreadcrumbList", "itemListElement": [...] },
    { "@type": "Product", "name": "Widget", "offers": {...} }
  ]
}
```

### Required vs. Recommended Properties

Required properties must be present for the rich result to appear. Recommended properties improve quality and appearance. Always include both.

### Avoiding Spammy Markup

- Do not fabricate reviews or ratings
- Schema properties must match visible page content
- Do not add schema for hidden content
- Do not mismatch schema type and page purpose
- Self-serving reviews without genuine third-party data trigger manual actions

Google manual actions for structured data spam can remove all rich results from your entire domain.

### Keeping Schema in Sync

Generate structured data from the same data source as page content. Include schema updates in your CMS publishing workflow. Audit quarterly or after major site changes.

## Rich Results Eligibility

| Schema Type | Rich Result | SERP Appearance |
|-------------|-------------|-----------------|
| `Product` | Product snippet | Price, availability, stars |
| `FAQPage` | FAQ accordion | Expandable Q&A in results |
| `HowTo` | How-to steps | Numbered steps with images |
| `Article` / `BlogPosting` | Article result | Author, date, thumbnail |
| `NewsArticle` | Top Stories | Carousel at top of results |
| `BreadcrumbList` | Breadcrumb trail | Replaces URL with nav path |
| `Review` / `AggregateRating` | Review snippet | Star rating below listing |
| `Event` | Event listing | Date, location, tickets |
| `VideoObject` | Video result | Thumbnail, duration |
| `LocalBusiness` | Local pack | Map, hours, phone |
| `JobPosting` | Google Jobs | Salary, location, apply |
| `SoftwareApplication` | Software result | Rating, price |
| `Course` | Course listing | Provider, enrollment |
| `Organization` | Knowledge panel | Logo, social links |

## Implementation Patterns

### Static HTML

```html
<head>
  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "Product", ... }
  </script>
</head>
```

### Next.js (App Router)

```tsx
export default function ProductPage({ product }) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    image: product.images,
    offers: {
      "@type": "Offer",
      price: product.price,
      priceCurrency: product.currency,
      availability: product.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
    },
  };
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {/* content */}
    </>
  );
}
```

### WordPress

Use Yoast SEO, Rank Math, or Schema Pro plugins. For custom implementation:

```php
add_action('wp_head', function() {
    if (is_singular('product')) {
        $product = get_post();
        $price = get_post_meta($product->ID, '_price', true);
        $schema = [
            '@context' => 'https://schema.org',
            '@type' => 'Product',
            'name' => $product->post_title,
            'offers' => [
                '@type' => 'Offer',
                'price' => $price,
                'priceCurrency' => 'USD',
                'availability' => 'https://schema.org/InStock',
            ],
        ];
        echo '<script type="application/ld+json">' . json_encode($schema) . '</script>';
    }
});
```

### Dynamic CMS Pattern

```typescript
function generateProductSchema(cmsData: CMSProduct): object {
  return {
    "@context": "https://schema.org",
    "@type": "Product",
    name: cmsData.title,
    image: cmsData.media.map(m => m.url),
    offers: {
      "@type": "Offer",
      price: cmsData.variants[0].price.toString(),
      priceCurrency: cmsData.currency,
      availability: cmsData.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
    },
  };
}
```

Key principle: generate structured data from the same data source that populates the page, never hardcode separately.

## Resources

- **Schema.org Full Vocabulary:** https://schema.org/docs/full.html
- **Google Rich Results Gallery:** https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema Markup Validator:** https://validator.schema.org
- **Full Cogny Docs:** https://cogny.com/docs/structured-data-reference
