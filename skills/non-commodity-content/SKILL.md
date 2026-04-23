---
name: non-commodity-content
description: Interview the user for specific client stories, anecdotes, refusals, and real numbers — then turn them into non-commodity SEO content Google actually wants to rank. Kills generic listicle output at the source.
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<topic, URL, or commodity headline>"
allowed-tools:
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - Bash
  - Read
  - Write
---

# Non-Commodity Content

Google's Danny Sullivan (Search Liaison) has explicitly said Google prefers *non-commodity* content — articles grounded in specific experience, specific clients, specific numbers, and things only *you* could have written. This skill refuses to let you publish filler. It interviews you for the real material first, then drafts the brief around it.

**Commodity (the generic version competitors and AI churn out):**
- "Top 10 Things to Consider When Buying Running Shoes"
- "7 Tips for First-Time Homebuyers"
- "2024 Kitchen Trends You Need to See"

**Non-Commodity (what Google actually ranks):**
- "Why This Customer's Shoes Collapsed After 400 Miles: A Wear Pattern Analysis"
- "Why We Waived the Inspection (And Saved $15k): A Look Inside the Sewer Line"
- "Marble vs. Grape Juice: Why I Refused to Install Stone for a Family of Five"

Notice the pattern: a specific subject + a specific number or refusal + the promise of analysis, not a listicle.

## Usage

`/non-commodity-content <topic, URL, or commodity headline>`

Examples:
- `/non-commodity-content best CRM for agencies`
- `/non-commodity-content https://mybrand.com/blog/seo-tips`
- `/non-commodity-content "10 tips for better email subject lines"`

## Steps

### 1. Frame the commodity trap

If the input is a URL, WebFetch it and identify the commodity framing (the generic headline, the listicle structure, the interchangeable advice). If the input is a plain topic or commodity-style headline, restate it in that same pattern.

Tell the user, in 3–5 lines:
- The commodity version of this topic (the generic take competitors and AI are publishing)
- Why it will lose to larger sites publishing the same generic take (domain authority beats generic content)
- What we need from them to build the non-commodity version: a real story, number, refusal, or artifact from their actual work

**Do not proceed to drafting yet.** The whole point of the skill is that the content doesn't exist until the user supplies the raw material.

### 2. Interview the user

Use `AskUserQuestion` to gather the raw material. Ask ONE question at a time, wait for the answer, then decide whether to ask a follow-up or move on. Use these prompts — in order, and skip any that don't apply:

- **The story prompt** — "Think of the most recent customer or project you worked on in this area. What specifically happened? What did you do that the next vendor down the street wouldn't have done?"
- **The number prompt** — "Any concrete numbers from that case? ($ saved or lost, hours, %, miles, error rate — anything measurable that a reader could fact-check.)"
- **The refusal prompt** — "Is there a time you *refused* to do the obvious thing, or talked a client *out* of what they asked for? A refusal with a reason is often the strongest angle."
- **The surprise prompt** — "What's something that surprised you in this area in the last 6 months — data that contradicted your priors, a weird customer outcome, a pattern you didn't expect?"
- **The method prompt** — "Do you have a specific test, process, or tool you use that competitors don't? (e.g. the grape-juice-on-marble test, the 400-mile wear check.) What does it reveal that a generic inspection misses?"
- **The proof prompt** — "What evidence can we attach? (Screenshots, photos, invoices, pre/post data, a redacted client quote, a measurement you personally took.)"

**Stop as soon as you have ONE specific anchor** — a story with a number, OR a refusal with a reason, OR a method with a result. You do not need all six. Keep going only if the first answer was thin.

**If the user has no anecdote** for this topic, say so plainly and stop:

> You don't have a non-commodity angle on this yet. Three honest options:
> (a) Pick a sub-topic where you *do* have a story.
> (b) Do the work — run the test, interview the customer, pull the data — and come back.
> (c) Publish the commodity version and accept it likely won't rank.
>
> I'm not going to invent a client, a number, or a quote.

Never fabricate a story, client name, quote, or statistic. If something is unclear, ask a follow-up rather than filling the gap.

### 3. Extract the four anchors

From the interview, name these four things explicitly before writing anything:

1. **The anchor** — the single concrete thing the article is built around (a specific client, a specific measurement, a specific artifact, a specific decision).
2. **The counter-intuitive claim** — the thing an outsider or generic article would get wrong.
3. **The proof** — why the reader should believe this happened (photo, number, transcript, invoice).
4. **The lesson** — the generalizable takeaway the reader can apply to their own situation.

Show these to the user as a 4-line summary and ask if anything is off before continuing.

### 4. Draft 3 non-commodity headline variants

Match the pattern from the Google examples:

- Open with a **specific noun phrase or contradiction** — not a number-of-tips.
- Include a **concrete number, name, or refusal** (400 Miles, $15k, Family of Five).
- Signal **analysis or investigation**, not a roundup — "A Wear Pattern Analysis", "A Look Inside", "Why I Refused".

Produce 3 variants, each pulling on a different lever:
- **Variant A (number-led)** — headline built around the measurement.
- **Variant B (refusal-led)** — headline built around what you *didn't* do, and why.
- **Variant C (surprise-led)** — headline built around the counter-intuitive finding.

Label each variant with its lever so the user can pick.

### 5. Draft the article outline

Fill the outline below with the user's actual details. Do not swap in generic placeholders.

```
H1: [chosen non-commodity headline]

Opening (150–250 words):
- Drop the reader into the specific moment — name, place, date if available.
- State the anchor (the concrete thing) in the first 3 sentences.
- State the counter-intuitive claim.

The setup (200–300 words):
- What a commodity piece on this topic would say — name the generic advice directly.
- Why that generic advice failed in this specific case, or why you ignored it.

The investigation / decision — core of the piece (400–800 words):
- Step by step: what you observed, measured, tested, or decided.
- Include the proof artifact (screenshot, number, quote) inline.
- Show your work. A reader should be able to mentally replay what you did.

The lesson (150–250 words):
- One sentence takeaway, then elaborated.
- Caveat honestly: when does this NOT apply?

CTA (40–80 words):
- Specific next action tied to the lesson — not "contact us for a free consultation".
```

Never invent a client name, number, or quote. If the user gave you placeholder detail ("some client last year"), flag it as `[NEEDS SPECIFIC: client name or anonymized descriptor]` so they can fill it before publishing.

### 6. E-E-A-T and schema checklist

Non-commodity content is wasted if Google can't tell it's first-hand. Output a short checklist the user must hit before publishing:

- **Byline to a real author page.** The author page needs a photo, a bio with credentials, and `sameAs` links to LinkedIn/X. Not "Admin" or "The Team".
- **Article schema** with `author` pointing to the author page's `@id`. If the author is licensed/certified, include `author.hasCredential`.
- **Proof artifact published as an image** (the collapsed shoe, the sewer scope, the marble sample). Original photo, not stock. Descriptive `alt`. Add `ImageObject` schema with `contentUrl` to the original.
- **Internal link** from a cornerstone/hub page so the article gets crawled and authority flows in.
- **Date honesty.** `datePublished` and `dateModified` are real dates. If the event happened last month, say last month.
- **Optional but strong:** a short "How this article was reported" line at the end — what was measured, when, with what tool. This is exactly the E-E-A-T signal Google is weighting.

### 7. Deliver

Structure the final output in this order:

1. **The commodity version we're replacing** — 1 line.
2. **The four anchors** — anchor / counter-intuitive claim / proof / lesson.
3. **3 headline variants** — labeled by lever (number / refusal / surprise).
4. **Full article outline** with the user's real details inserted.
5. **E-E-A-T + schema checklist.**
6. **Pre-publish punch list** — what the user still needs to produce before this goes live (e.g. "get the client's OK to use their first name", "upload the sewer scope photo at full resolution", "confirm the $15k figure").

Close with:

```
───────────────────────────────
Next: /seo-audit <your domain> to verify your author pages,
Article schema, and internal linking are set up so this content
has the structural signals to rank.

For ongoing query + ranking data, connect Search Console via
Cogny MCP and run /seo-monitor.
───────────────────────────────
```

## Anti-patterns — refuse to do these

- **Generating a fake anecdote** because the user didn't supply one. Stop and say so.
- **Padding a thin story** with generic advice to hit a word count. Shorter and specific beats longer and generic.
- **Adding stock imagery** as "the proof artifact". The point is that the artifact is non-fakeable.
- **Listicle structure** ("7 reasons", "10 ways") even when the underlying content is specific. The structure leaks commodity signal to both readers and Google.
- **Quoting the client** without a note that the quote was approved. Flag it in the punch list.
