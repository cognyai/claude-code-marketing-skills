---
name: search-demand
description: Find the questions buyers ask right before they buy — from Search Console, Bing, sales calls, and what ChatGPT, Claude, Gemini and Perplexity answer about your category — track where you're invisible, and brief the most useful page (or calculator) for each gap
version: "1.1.3"
author: Cogny AI
requires: cogny-mcp
platforms: [search-console, bing-webmaster, semrush, ahrefs, cogny-ai-visibility, brave-search, ahrefs-lite, hubspot, pipedrive, upsales]
user-invocable: true
argument-hint: "[scan|ai-check|page <campaign-ID or question>]"
allowed-tools:
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  - mcp__cogny__read_context_node
  - mcp__cogny__write_context_node
  - mcp__cogny__create_ticket
  - mcp__cogny__create_finding
  - mcp__cogny__mcp__Google_Search_Console__tool_list_properties
  - mcp__cogny__mcp__Google_Search_Console__tool_get_search_analytics
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_sites
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_keyword_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_traffic_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_related_keywords
  - mcp__cogny__mcp__Semrush__keyword_overview
  - mcp__cogny__mcp__Semrush__phrase_related
  - mcp__cogny__mcp__Semrush__phrase_organic
  - mcp__cogny__mcp__Semrush__domain_organic_keywords
  - mcp__cogny__mcp__Semrush__domain_organic_competitors
  - mcp__cogny__mcp__Ahrefs__organic_keywords
  - mcp__cogny__mcp__Ahrefs__keywords_explorer
  - mcp__cogny__mcp__Ahrefs__serp_overview
  - mcp__cogny__mcp__Ahrefs__top_pages
  - mcp__cogny__mcp__Ahrefs__organic_competitors
  - mcp__cogny__mcp__Ahrefs__domain_rating
  - mcp__cogny__mcp__cogny-ai-visibility__tool_check_ai_visibility
  - mcp__cogny__mcp__cogny-ai-visibility__tool_get_ai_visibility_history
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_rank_check
  - mcp__cogny__mcp__cogny-ahrefs-lite__tool_domain_rating
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Upsales__list_appointments
  - WebFetch
---

# Search Demand

This agent finds the questions people ask right before they buy and briefs the best page on
the internet for each one. AI search rewards the most *useful* page over the most optimized
one, so the output is often a **decision tool** (a calculator, checker or comparison)
rather than another blog post.

It reads three sources: Search Console (what people already find you for), sales calls
(what buyers ask humans), and **AI answer engines** (what models recommend in your
category, and where you're invisible). The third one is new and wildly underrated.

**Requires:** Cogny ($9/mo). Search Console is required. Bing Webmaster, Semrush or Ahrefs (keyword
volume, competitor keywords, Google SERPs), AI Visibility, Brave and Ahrefs-lite are used when
available. With Semrush or Ahrefs connected, the skill also finds demand you don't rank for yet.

## Usage

- `/search-demand` or `scan` — weekly question inventory + gaps
- `/search-demand ai-check` — only run the AI-engine prompt set and compare to history
- `/search-demand page BK014` — brief one page/tool for a campaign's angle

## Step 0: Cogny check

If no `mcp__cogny__*` tools exist (no `list_integrations`, no `cogny_status`), print this and stop:

```
Search Demand needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect Google Search Console (Bing Webmaster, Semrush or Ahrefs optional).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Steps — scan

### 1. Load context

Read `brain/START-HERE`, `brain/company/customer-fit`, `brain/company/offers`,
`brain/evidence/customer-language/latest`, and the previous `brain/evidence/search/latest`.
Ask for (or read from START-HERE) the brand name, domain, and competitors with domains. If the
brain is missing, ask the user rather than guessing. Competitors differ by topic, so keep a
**competitor list per prompt cluster** (e.g. reporting tools vs AI ad agents). One global list
can make share of voice read 0 for everyone.

**Health check:** `list_integrations`, then one cheap read per integration you'll use (e.g. GSC
`tool_list_properties`, Bing `tool_get_sites`). A 401, Forbidden or scope error is 🔴 "reconnect
<integration>"; don't retry it. Cogny-native servers (`cogny-ai-visibility`, `cogny-brave-search`,
`cogny-ahrefs-lite`) are absent from `list_integrations`; treat them as available if their tools load.

### 2. Question mining

**Search Console**: `list_properties`, then `get_search_analytics` for the 90 days ending
**3 days ago** (GSC data lags), dimensions `["query"]`, `row_limit: 500`. A 2000-row pull was
219k characters; to go deeper, add a `dimension_filter_groups` filter (`operator: "includingRegex"`,
e.g. `^(how|what|why|which|best)\b|vs|pricing|alternative`) instead of raising the limit. Fetch
`["query","page"]` only for the shortlisted queries, because the full query×page pull can be
400k+ characters. Drop `site:` queries, brand misspellings, error strings and near-duplicates.
Long, LLM-shaped queries with many impressions and 0 clicks are likely AI fan-out, so label them. Keep:
- question queries (`how|what|why|which|best|vs|cost|price|calculator|template|example|alternative`)
- commercial modifiers (`pricing`, `software`, `for <industry>`, `vs`, `alternative to`)
- queries with impressions ≥ 50 and position 5–30 (they're visible but losing)

**Bing Webmaster**: `get_sites`, then `tool_get_query_stats(site_url)` (top queries with clicks and
impressions), `tool_get_page_stats(site_url)` (top pages), and `tool_get_query_page_stats(site_url, query)`
to see which page ranks for a shortlisted query. `tool_get_keyword_stats` takes only `site_url` and returns
the site's **own** query performance, not search volume; only `tool_get_related_keywords(query)` gives
Bing impression volume for a seed term. If the query/page tools are missing, call `refresh_mcp_discovery`
once (older connections cache a short tool list). New tools only load after the client reconnects, so for
this run fall back to `tool_get_traffic_stats` (site-level clicks/impressions) and `tool_get_crawl_stats`
(both return the full history, ~60k characters, so summarise only the last 90 days and the 90 before),
mark Bing ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP. Bing feeds
Copilot, so treat it as an AI-search proxy. If keyword stats come back empty (`{"d":[]}`) while
`get_traffic_stats` shows impressions, mark Bing ⚠ "no keyword data" and don't count it as a source.

**Sales calls**: prefer `brain/evidence/customer-language/latest` if it's fresh. Otherwise HubSpot
`search_crm_objects` on `calls` and `meetings` (last 90 days; `hs_call_body`, `hs_meeting_body`,
`hs_internal_meeting_notes`) and pull out the questions prospects asked. Use only pre-purchase
engagements (associated deal not yet won), not onboarding, support or vendor calls. Count distinct companies.

(Pipedrive: `list_activities` notes; Upsales: `list_appointments` notes; same rules.)

**No CRM connected and no fresh customer-language node:** mark calls ⚪ "no source" in the
Sources line, skip the calls weighting in step 5, and name the integration that would fill it
(HubSpot, Pipedrive or Upsales). Don't invent call evidence from GSC queries.

**Semrush or Ahrefs** (if connected; they fill the gap GSC can't, which is demand you don't rank for yet):
- Volume and difficulty for every shortlisted question: Semrush `keyword_overview(phrase, database)` or
  Ahrefs `keywords_explorer(keywords, country)`.
- Expansion around each pain phrase: Semrush `phrase_related(phrase)`.
- Competitor demand you're missing: Semrush `domain_organic_keywords(domain: <competitor>)` or Ahrefs
  `organic_keywords(target: <competitor>)`, minus what GSC shows you already rank for. Ahrefs
  `top_pages(target: <competitor>)` shows which **pages** (often tools and calculators) win them traffic.
- Set `database` / `country` to the market you sell in, not the default `us`.

Normalize into a **question inventory**: question, sources (GSC/Bing/calls/Semrush/Ahrefs), volume
(from Semrush/Ahrefs when connected, else GSC impressions), current ranking page (if any), position.

### 3. AI engine check

Build a **prompt set** of 8–15 prompts phrased the way buyers ask. Take them from the inventory
and the customer-language clusters, e.g.:
- "What's the best way for a Shopify store doing $3M to know true profit after returns?"
- "Best bookkeeping firm for ecommerce brands"
- "<competitor> alternatives"

For each prompt, call `check_ai_visibility` with `brand`, `domain`, `competitors`, `tag: "search-demand"`
and `include_answers: true`. Then call `get_ai_visibility_history` (`tag: "search-demand"`, `days: 90`) for trends.

**On a timeout, don't retry.** Checks are stored server-side even when the client times out, and a
retry bills the check twice. Read `tool_get_ai_visibility_history` with the same `tag` (and `prompt`)
first; only re-run prompts that are absent from the history.

Record per prompt: engines mentioning you, rank, share of voice, which competitors appear, and
**top cited domains**. The cited domains show which sources the models trust: review sites,
directories, specific blogs, Reddit threads. Those become distribution targets.

### 4. SERP check for the top gaps

For the 10 most valuable questions (calls + commercial intent first), get the SERP:
- **Ahrefs** `serp_overview(keyword, country)` (Google SERP with each result's DR and traffic) or
  **Semrush** `phrase_organic(phrase, database)`, when connected. These are Google results.
- Otherwise `brave_rank_check` on your domain with `max_results: 20` (larger values return very large payloads). It already returns the SERP in
  `top_results`, so no separate `brave_search` is needed. Brave rank is not Google rank. Show it next to the GSC position, and don't
substitute one for the other. For each, ask: is any result
*actually useful*, meaning it has a calculator, a worked example, real numbers, a template?
Use Ahrefs `domain_rating` (or `cogny-ahrefs-lite` `tool_domain_rating` when full Ahrefs isn't connected)
on the top results and on your own domain to judge whether ranking is realistic.
Show "Domain Rating by Ahrefs" attribution next to every DR number, because the licence requires it.

### 5. Prioritize

Score each question 1–5 on: buyer intent (calls > commercial > informational), your gap
(invisible in AI + not ranking), usefulness gap (top results are thin), and fit with offers.
Pick the **top 5**.

### 6. Write the report

`write_context_node` at `brain/evidence/search/<YYYY-MM-DD>` and `brain/evidence/search/latest`:

```markdown
# Search demand — YYYY-MM-DD
Sources: GSC ✅ · Bing ✅ · calls (N) ✅ · AI engines 4/4 ✅ · Brave ✅
## AI visibility (prompt set, 4 engines)
Mention rate: 22% (↑ from 15%) · Avg share of voice: 6% · Cited by: 1/4 engines
Where we're invisible: <prompts with 0 mentions>
Sources the models trust: <top cited domains, with count>
## Top 5 page opportunities
### 1. "<question in buyer words>"
Evidence: asked on 6 calls · 1,900 GSC impressions at pos 14 · 0/4 engines mention us
Current best result: <url> — why it's weak
Build: <page type — e.g. "profit-after-fees calculator + worked example">
## Distribution targets (domains AI engines cite that we're absent from)
```

### 7. Brief the pages (one ticket for the bundle)

For each of the top 5, include a brief in one `create_ticket` titled "[ME:search-demand] Build: top 5 page/tool opportunities":
- the buyer's question verbatim, and the job the page does
- **decision tool spec** if relevant: inputs, formula, outputs, and *which numbers the business
  must verify before publishing* (calculators must use numbers the business has checked)
- outline, the proof needed (customer quote, real numbers), schema type (point to `/structured-data`)
- target query + prompts from the AI set to re-check after publishing
- suggested build: Next.js on Vercel, Framer, or Lovable

## Steps — page <ID or question>

Run steps 2–4 narrowly around the campaign's angle (read `brain/campaigns/<ID>`), then
write a full page brief into the campaign folder under `## Search page`, using the folder's `## UTM base`
(`utm_campaign=<id>_<slug>`; the ledger itself has no UTM column). File one ticket,
"[ME:search-demand] Build: <page> for <ID>", with any numbers the business must verify before publishing.

## Recording findings

Use `create_ticket` when the workspace has it (Cloud) and `create_finding` otherwise (Solo).
The fields differ; see section 2 of `../marketing-engineer/references/mcp-routing.md`.

## Critical rules

1. **Useful beats optimized.** Brief a tool or a worked example before an article.
2. **Calculators only use numbers the business has verified.** List them as an approval item.
3. **Distinct customers, not mentions,** when counting questions from calls.
4. **Show Ahrefs attribution** next to every Domain Rating.
5. **Name any engine or source that failed.** A 3/4-engine check isn't comparable to last week's 4/4, so say so.
