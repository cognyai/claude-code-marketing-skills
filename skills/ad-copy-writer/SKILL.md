---
name: ad-copy-writer
description: Generate ad copy variations for Google, Meta, and LinkedIn Ads
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<platform> <product or URL>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
---

# Ad Copy Writer

Generate high-converting ad copy for Google Ads, Meta Ads, or LinkedIn Ads.

## Usage

`/ad-copy-writer google "project management tool"` — Google Ads copy
`/ad-copy-writer meta example.com` — Meta Ads copy from website
`/ad-copy-writer linkedin "B2B SaaS"` — LinkedIn Ads copy

## Steps

### 1. Research the product
If a URL is provided, WebFetch it and extract:
- Value proposition
- Key features / benefits
- Target audience
- Pricing (if visible)
- Unique differentiators

If a description is provided, use that directly.

### 2. Research the competition
WebSearch for competitors to understand:
- What messaging angles they use
- Common claims in the space
- Price anchoring

### 3. Generate copy by platform

#### Google Ads (RSA format)
Generate 15 headlines (max 30 chars each) and 4 descriptions (max 90 chars each):

**Headlines** — mix of:
- Benefit-led: "Cut Ad Spend 40%"
- Feature-led: "AI-Powered Optimization"
- Social proof: "Trusted by 1,000+ Agencies"
- CTA: "Start Free Trial Today"
- Keyword-match: "[Primary keyword] Tool"

**Descriptions** — mix of:
- Problem/solution
- Feature list
- Social proof + CTA
- Urgency/offer

#### Meta Ads
Generate 3 variations:
- **Primary text** (125 chars visible, up to 500)
- **Headline** (40 chars)
- **Description** (30 chars)
- **CTA button** recommendation

Angles:
1. Pain point → solution
2. Social proof → aspiration
3. Direct value prop → CTA

#### LinkedIn Ads
Generate 3 variations:
- **Intro text** (150 chars for single image)
- **Headline** (70 chars)
- **Description** (100 chars)

Angles:
1. Professional credibility
2. ROI / efficiency focus
3. Industry-specific insight

### 4. Output format

Present each variation clearly labeled with character counts:

```
=== Google Ads RSA ===

Headlines (30 char max):
1. "Cut Your Ad Spend by 40%" (25)
2. "AI Marketing Automation" (24)
...

Descriptions (90 char max):
1. "Stop wasting budget on underperforming ads. Our AI optimizes your campaigns 24/7." (83)
...

=== Meta Ads ===

Variation 1 (Pain → Solution):
Primary: "..."
Headline: "..."
...
```
