---
name: landing-page-review
description: CRO review of a landing page with specific conversion recommendations
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<url>"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
---

# Landing Page Review

Analyze a landing page for conversion optimization — messaging, layout, trust signals, and CTA effectiveness.

## Usage

`/landing-page-review example.com/pricing` — review the given page

## Steps

### 1. Fetch and analyze the page
Use WebFetch to load the URL. Extract:
- Headline and subheadline text
- CTA buttons (text, placement, count)
- Value proposition clarity
- Above-the-fold content
- Page structure (sections, flow)

### 2. Evaluate messaging
Score each element:
- **Headline clarity** (1-10): Does it immediately communicate what you get?
- **Value prop specificity** (1-10): Numbers > vague claims
- **CTA strength** (1-10): Action-oriented, specific, visible
- **Social proof** (1-10): Testimonials, logos, stats
- **Urgency/scarcity** (1-10): Reason to act now

### 3. Check trust signals
Look for:
- Customer logos or testimonials
- Security badges / certifications
- Pricing transparency
- Contact information
- Privacy policy / terms links
- Case studies or results

### 4. Analyze form/CTA friction
If there's a form:
- Number of fields (fewer = higher conversion)
- Field labels and placeholder text
- Submit button text (specific > generic)
- Error handling
- Privacy reassurance near form

### 5. Mobile assessment
Check:
- Mobile viewport optimization
- Touch target sizes
- Content readability on small screens
- CTA visibility without scrolling

### 6. Competitive comparison
WebSearch for 2-3 competitors and briefly compare:
- How do their landing pages differ?
- What trust signals do they use?
- How is their CTA different?

### 7. Report

```
Landing Page Review: [URL]
Conversion Score: X/100

Messaging: X/30
- Headline: [score] — [specific feedback]
- Value prop: [score] — [specific feedback]
- CTA: [score] — [specific feedback]

Trust: X/30
- Social proof: [score]
- Credibility signals: [score]
- Transparency: [score]

UX: X/20
- Form friction: [score]
- Mobile: [score]
- Load speed: [score]

Differentiation: X/20
- vs [Competitor 1]: [comparison]
- vs [Competitor 2]: [comparison]

Top 5 Changes (in priority order):
1. [Specific change with expected impact]
2. ...
3. ...
4. ...
5. ...
```
