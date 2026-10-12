# Claude Code Marketing Skills

AI marketing skills for Claude Code, Cursor, Windsurf, and other AI coding tools.
Audit SEO, analyze ads, research competitors, qualify leads — all from your terminal.

**Free skills need no account. Premium skills connect your real data for $9/mo.**

<p align="center">
  <img src="demo.gif" alt="Claude Code Marketing Skills demo" width="800">
</p>

Built by [Cogny](https://cogny.com) — AI marketing infrastructure.

## Quick Install

```bash
curl -sSL https://raw.githubusercontent.com/cognyai/claude-code-marketing-skills/main/install.sh | bash
```

Or manually copy the skills you want:

```bash
git clone https://github.com/cognyai/claude-code-marketing-skills.git
cp -r claude-code-marketing-skills/skills/* .claude/skills/
```

For Codex, copy them into your Codex skills directory:

```bash
git clone https://github.com/cognyai/claude-code-marketing-skills.git
cp -r claude-code-marketing-skills/skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Free Skills (no account needed)

These skills work immediately using web search and public data:

| Skill | Command | What it does |
|-------|---------|-------------|
| SEO Audit | `/seo-audit` | Full technical + content SEO analysis (enhanced with live Search Console + Bing data when connected) |
| Non-Commodity Content | `/non-commodity-content` | Interviews you for real client stories, refusals, and numbers — then drafts the non-commodity SEO brief Google actually ranks |
| Landing Page Review | `/landing-page-review` | CRO review with specific conversion recommendations |
| Competitor Analysis | `/competitor-analysis` | Research competitor positioning, ads, and market gaps |
| Ad Copy Writer | `/ad-copy-writer` | Generate ad copy variations for Google/Meta/LinkedIn |
| Lead Qualification | `/lead-qualification` | Research and qualify business leads against your ICP |
| GA4 BigQuery Schema | `/ga4-bigquery-schema` | Complete GA4 BigQuery export schema reference with query patterns |
| GA4 Event Implementation | `/ga4-events` | GA4 event model reference — recommended events, custom dimensions, validation |
| GTM Event Tracking | `/gtm-setup` | GTM dataLayer, triggers, variables, tag configuration, and debug mode |
| GAQL Reference | `/gaql-reference` | Google Ads Query Language syntax, fields, and common report queries |
| Conversion Tracking Debugger | `/conversion-debug` | Cross-platform conversion tracking troubleshooting (GTM + GA4 + Ads + Meta) |
| Meta Conversions API | `/meta-capi` | Meta CAPI setup — server-side events, dedup, event match quality |
| UTM Strategy & Builder | `/utm-builder` | UTM naming conventions, channel grouping rules, validation queries |
| Structured Data | `/structured-data` | Schema.org JSON-LD templates for rich results — all major types |
| Core Web Vitals | `/cwv-audit` | LCP, INP, CLS diagnosis and fixes with CrUX BigQuery queries |
| Google Ads Scripts | `/google-ads-scripts` | Google Ads Scripts patterns — automation, Sheets integration, MCC scripts |
| Website Migration Audit | `/website-migration-audit` | Compare production vs staging — SEO parity, content integrity, launch readiness (enhanced with Search Console data when connected) |
| Welcome Series Writer | `/welcome-series` | Generate a full 5-email welcome series from a brand URL — ready to paste into any ESP |
| Deliverability Check | `/deliverability-check` | Audit SPF / DKIM / DMARC / BIMI on your sending domain, with a prioritized fix order |
| Performance Max Launch Kit | `/pmax-launch-kit` | Build a full Performance Max campaign — asset group copy, search themes, audience signals, shot list — from a brand URL |
| GA4 Measurement Plan | `/ga4-measurement-plan` | Event taxonomy, parameters, custom dimensions, and key events — a GA4 spec built from a site URL |
| GTM Tracking Plan | `/gtm-tracking-plan` | GTM tags, triggers, variables, and copy-paste dataLayer snippets — a build spec from a site URL |
| Submit to agentlaunch | `/submit-to-agentlaunch` | List, launch, or register an AI agent on agentlaunch (a Product Hunt-style directory) and upvote agents via a public, no-auth REST API |

## Premium Skills (requires [Cogny](https://cogny.com) — $9/mo for all managed MCPs)

These skills connect to your actual ad accounts and email platforms via Cogny's MCP servers:

| Skill | Command | MCP Server | What it does |
|-------|---------|-----------|-------------|
| LinkedIn Ads Audit | `/linkedin-ads-audit` | LinkedIn Ads | Campaign structure, targeting, creative performance, spend efficiency |
| SEO Monitor | `/seo-monitor` | Search Console / Bing Webmaster | Track rankings, queries, indexing, core web vitals |
| CRM ICP Analysis | `/crm-icp-analysis` | HubSpot / Pipedrive / Upsales | Build data-driven ICP from closed-won deals, contacts, and companies |
| Sales Momentum Drivers | `/crm-sales-momentum` | HubSpot / Pipedrive / Upsales | Pipeline velocity, stage conversions, stuck deals, win/loss patterns |
| LinkedIn Micro Campaigns | `/linkedin-micro-campaigns` | HubSpot / Pipedrive / Upsales + LinkedIn Ads | Create precision-targeted LinkedIn campaigns from ICP data |
| Subject Line Lab | `/subject-line-lab` | Any connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, SFMC, …) | Mine your last 100+ sends, find the subject-line patterns that actually lift opens on *your* list, and generate 20 tuned candidates |
| Winback Engine | `/winback-engine` | Any connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, SFMC, …) | Find dormant subscribers, tier by historical value, draft personalized winback series per tier, flag suppression candidates |
| Pre-Send QA | `/pre-send-qa` | Any connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, SFMC, …) | Pre-flight QA: merge tag fallbacks, broken links, spam triggers, CAN-SPAM compliance, mobile rendering |
| Email Report | `/email-report` | Any connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, SFMC, …) | Auto-write the weekly/monthly email performance report in 3 formats — Slack, CEO email, board deck section |
| Revenue Audit | `/revenue-audit` | Any connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, SFMC, …) | "Email growth consultant in a box" — finds missing flows, dormant high-value subscribers, under-segmented blasts, ranked by estimated $ impact |
| Drop-off Rescue | `/drop-off-rescue` | Any connected ESP (Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, SFMC, …) | Find contacts stalled at funnel stages (abandoned cart, signed-up-but-no-trial, trial-but-no-convert), draft re-engagement emails, schedule sends — reruns weekly without double-sending |
| Community Pulse | `/community-pulse` | Discord (+ Crisp, YouTube) | Weekly digest — new joins, hot/dead channels, top contributors, lurker→active conversions, unanswered questions, 3–6 actions you can ship in 15 min |
| Google Ads Audit | `/google-ads-audit` | Google Ads | Account-wide audit across every campaign type — structure, budget, conversion tracking, wasted spend, ranked by estimated $ impact |
| Google Ads Monitor | `/google-ads-monitor` | Google Ads (+ Microsoft, Apple Search, OpenAI Ads) | Weekly health check — budget pacing, spend spikes, disapproved ads, conversion-tracking breaks — week-over-week |
| Performance Max Audit | `/pmax-audit` | Google Ads | Deep PMax audit — asset group strength, asset coverage, search themes, audience signals, brand exclusions |
| Search Campaign Audit | `/search-campaign-audit` | Google Ads / Microsoft Ads | Deep Search audit — quality score, match types, negative keyword gaps, search terms, ad strength |
| Shopping Campaign Audit | `/shopping-campaign-audit` | Google Ads | Deep Shopping / retail audit — feed coverage, listing-group granularity, wasted product spend |
| Demand Gen Audit | `/demand-gen-audit` | Google Ads | Deep Demand Gen audit — audience strategy, creative format diversity, fatigue, CPA vs goal |
| GA4 Audit | `/ga4-audit` | GA4 | GA4 configuration + data-quality audit — key events, custom dimensions, PII, attribution, `(not set)` traffic |
| GA4 Monitor | `/ga4-monitor` | GA4 / Plausible / Fathom / Simple Analytics / Adobe | Weekly GA4 check — sessions, conversions, revenue, channel mix, tracking-break alerts — week-over-week |
| GTM Audit | `/gtm-audit` | GTM | GTM container audit — duplicate GA4 tags, orphaned tags, trigger coverage, Consent Mode, naming hygiene |
| GTM Monitor | `/gtm-monitor` | GTM | Weekly GTM check — diffs tags / triggers / variables vs last week, flags risky changes and unpublished drafts |
| Cogny Agent | `/cogny` | All | Full autonomous agent — scheduled analysis, strategy, execution |

## Marketing Engineer Stack — beta (requires [Cogny](https://cogny.com))

One person wiring agents into a machine that runs experiments every week: researching the customer, building pages and creative, launching tests, and killing the losers. Inspired by Greg Isenberg's [Marketing Engineers playbook](https://x.com/gregisenberg/status/2108188646973313195). Every agent reads one shared **brain** in the Cogny context tree. Every campaign carries an ID from the first ad to the closed deal. Every decision lands in a review queue that takes under a minute per item. Guardrails live in the tools: ads are created paused, outreach is drafted and never sent, and scheduled agents get pause-only grants.

| Skill | Command | MCP Servers | What it does |
|-------|---------|-------------|-------------|
| Marketing Engineer | `/marketing-engineer` | All | The hub: setup, the Monday loop, one campaign end to end, scheduling agents with tool-level guardrails |
| Marketing Brain | `/marketing-brain` | Context tree + HubSpot + Stripe | Interview-built START-HERE, customer-fit, offers, voice, founder opinions, failed campaigns. Agents propose, humans promote |
| Customer Language | `/customer-language` | HubSpot | The exact words customers use for their problems, from CRM calls, meetings, notes and tickets, clustered by distinct company. Weekly |
| Campaign Ledger | `/campaign-ledger` | Google / Meta / LinkedIn / Bing / TikTok / X Ads, GA4, HubSpot, fibbler | Campaign IDs in every name and UTM, a naming audit, and one ledger joining spend → calls → deals → revenue |
| Buying Triggers | `/buying-triggers` | fibbler + HubSpot + Brave | Accounts with a fresh trigger (funding, hiring, launches, rising ad engagement). Drafts outreach only when the "event → problem → fix" sentence is sharp |
| Search Demand | `/search-demand` | Search Console + Bing + AI Visibility + Brave + Ahrefs | Pre-purchase questions from search and calls, what ChatGPT/Claude/Gemini/Perplexity recommend, and briefs for the most useful page or calculator per gap |
| Creative Engine | `/creative-engine` | Image Gen + Meta / LinkedIn / TikTok Ads | 8–12 distinct concepts from customer words, images generated with real brand assets, uploaded **paused** and named `ID_angle_format_vN` |
| Ad Kill Rules | `/ad-kill-rules` | All ad platforms | A pre-declared evidence bar, enforced daily. Dry run, approved pause, or a scheduled pause-only script |
| Closed-Lost Revival | `/closed-lost-revival` | HubSpot + fibbler + Brave | The real reason for every lost deal plus a reopen condition, watched weekly. Drafts notes that quote the original call |
| Social Engine | `/social-engine` | LinkedIn Organic + X Organic + Brave + Discord | Listening, a weekly hook batch from founder opinions, approved-only scheduling, and organic winners promoted to paid |
| Performance Memo | `/performance-memo` | fibbler + HubSpot + Stripe + Fortnox + ad platforms | The Monday memo: spend → qualified calls → deals → churn per campaign, every line ending in keep / kill / change / test |

**CRM:** HubSpot is the default (read-only). Salesforce, Pipedrive and Attio map onto the same jobs through the CRM layer in `/marketing-engineer`.

**Beta:** these skills are tested live on Cogny Cloud with Google Ads, Meta, X, GA4, GTM, Search Console, Bing, Mailchimp, Get a Newsletter, Stripe and Discord. Other integrations are built from the Cogny MCP proxy source but haven't run against real accounts yet. If something breaks, [open an issue](https://github.com/cognyai/claude-code-marketing-skills/issues).

**Start here:** `/marketing-engineer setup` → `/marketing-brain` → `/customer-language`. Add the next agent only once you trust the last one.

### Setting up Premium Skills

1. Sign up at [cogny.com](https://cogny.com)
2. Connect the accounts you use. Skills pick whichever provider in a category is connected (see [Supported integrations](#supported-integrations))
3. Add Cogny to your `.mcp.json`:

```json
{
  "mcpServers": {
    "cogny": {
      "type": "http",
      "url": "https://app.cogny.com/mcp"
    }
  }
}
```

4. Claude Code will open a browser for OAuth login on first use.
5. Run any premium skill — your AI now has direct access to your marketing data.

On **Solo**, skills record what they find with `create_finding`. On **Cloud**, they use tickets (`create_ticket`) and can also use BigQuery, scripts, automations and image generation. Every skill handles both plans.

### Supported integrations

Skills are written against jobs ("ad-level spend", "campaign report", "lost deals"), not one vendor. A skill runs on any connected provider in the category and reports each one separately when several are connected.

| Category | Providers |
|----------|-----------|
| Paid search | Google Ads, Microsoft Ads (Bing Ads), Apple Search Ads, OpenAI Ads |
| Paid social | Meta Ads, LinkedIn Ads, TikTok Ads, X Ads, Reddit Ads, Snapchat Ads, Bidtheatre |
| B2B attribution | Fibbler |
| Web & product analytics | Google Analytics 4, Plausible, Fathom Analytics, Simple Analytics, Adobe Analytics, Microsoft Clarity, PostHog, Mixpanel, Segment, AppsFlyer, GrowthBook |
| Tagging | Google Tag Manager |
| SEO & AI search | Google Search Console, Bing Webmaster Tools, Semrush, Ahrefs, AI Visibility (ChatGPT / Claude / Gemini / Perplexity), Brave Search |
| Email | Klaviyo, Mailchimp, Rule, Get a Newsletter, Brevo, MailerLite, Drip, Braze, Salesforce Marketing Cloud, Symplify |
| CRM & forms | HubSpot, Pipedrive, Upsales, HubSpot Forms |
| Organic social & community | LinkedIn Organic, X Organic, YouTube, Discord, Crisp |
| Ecommerce | Shopify, WooCommerce, Abicart, Litium, ShipStation |
| CMS | WordPress, Webflow, Ghost, Framer, Wix, Sanity, Contentful |
| Billing & finance | Stripe, Fortnox |
| Creative | Image generation (Cloud) |

The routing rules every skill follows (tool names, plan differences, choosing a provider, same-job tables) are in [`skills/marketing-engineer/references/mcp-routing.md`](skills/marketing-engineer/references/mcp-routing.md).

## How It Works

**Free skills** use `WebFetch` and `WebSearch` to analyze publicly available data. No accounts or API keys needed.

**Premium skills** use [Cogny's MCP gateway](https://cogny.com), which federates 60+ integrations through the Cogny MCP proxy. Your AI runs locally (Claude Code, Cursor, Codex, etc.), and Cogny holds the credentials and serves the data.

```
Your Claude Code ──MCP──> Cogny MCP gateway ──> Cogny MCP proxy ──OAuth/Token──> Google Ads / Meta / LinkedIn / TikTok / Reddit / …
    (local)               app.cogny.com/mcp     (hosted)                         GA4 / Search Console / Semrush / Ahrefs / …
                                                                                 Klaviyo / Mailchimp / Brevo / HubSpot / Shopify / …
                                                                                 (your accounts)
```

Every connected integration appears as `mcp__<Integration>__<tool>`, e.g. `mcp__Google_Ads__tool_execute_gaql`. With the server registered as `cogny` in `.mcp.json`, Claude Code shows that as `mcp__cogny__mcp__Google_Ads__tool_execute_gaql`, which is the form the skills use. Old names like `mcp__cogny__google_ads__…` are no longer served. <!-- check-tool-names: ignore -->
## Results

### GrowthHackers.se — +271% organic clicks in 3 weeks

Connected Search Console and Bing Webmaster Tools via Cogny MCP. 
Ran `/seo-audit` + `/seo-monitor` after a site migration.

| Metric | Before | After |
|--------|--------|-------|
| Organic clicks | baseline | **+271%** |
| Click-through rate | 0.29% | **0.66%** |
| Search impressions | baseline | **+60%** |
| AI citations (Bing Copilot) | baseline | **+154%** |
| PageSpeed score | 78 | **97** |

> "Cogny gave Claude Code eyes into our actual search data. 
> The audit caught things we'd never have found manually."
> — Yi Li, CEO at GrowthHackers

[Read the full case study →](https://cogny.com/case-studies/growthhackers-4x-organic-traffic)

---

*Got results? [Open an issue](https://github.com/cognyai/claude-code-marketing-skills/issues) 
and we'll feature you here.*


## Contributing

PRs welcome! See individual skill files for the format. Skills should include:
- YAML frontmatter with metadata
- Clear step-by-step instructions
- Specific queries/actions (not vague recommendations)
- Example output format
- Read-only tools in `allowed-tools`. Write tools (pause, create, send, schedule) prompt the user.

Tool names are checked against the real Cogny MCP surface:

```bash
# Regenerate the catalog from the Cogny monorepo (services/mcp-proxy)
python3 scripts/build-mcp-catalog.py ../cogny/services/mcp-proxy/src/servers

# Check every mcp__cogny__… reference in skills/
python3 scripts/check-tool-names.py
```

## License

MIT
