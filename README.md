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

## Free Skills (no account needed)

These skills work immediately using web search and public data:

| Skill | Command | What it does |
|-------|---------|-------------|
| SEO Audit | `/seo-audit` | Full technical + content SEO analysis (enhanced with live Search Console + Bing data when connected) |
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

## Premium Skills (requires [Cogny](https://cogny.com) — $9/mo for all managed MCPs)

These skills connect to your actual ad accounts via Cogny's MCP servers:

| Skill | Command | MCP Server | What it does |
|-------|---------|-----------|-------------|
| LinkedIn Ads Audit | `/linkedin-ads-audit` | LinkedIn Ads | Campaign structure, targeting, creative performance, spend efficiency |
| SEO Monitor | `/seo-monitor` | Search Console | Track rankings, queries, indexing, core web vitals |
| CRM ICP Analysis | `/crm-icp-analysis` | HubSpot | Build data-driven ICP from closed-won deals, contacts, and companies |
| Sales Momentum Drivers | `/crm-sales-momentum` | HubSpot | Pipeline velocity, stage conversions, stuck deals, win/loss patterns |
| LinkedIn Micro Campaigns | `/linkedin-micro-campaigns` | HubSpot + LinkedIn Ads | Create precision-targeted LinkedIn campaigns from ICP data |
| Cogny Agent | `/cogny` | All | Full autonomous agent — scheduled analysis, strategy, execution |

### Setting up Premium Skills

1. Sign up at [cogny.com](https://cogny.com)
2. Connect your accounts (Google Ads, Meta Ads, Search Console, Bing, LinkedIn, HubSpot)
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

## How It Works

**Free skills** use `WebFetch` and `WebSearch` to analyze publicly available data. No accounts or API keys needed.

**Premium skills** use [Cogny's MCP servers](https://cogny.com) to connect directly to Google Ads, Meta Ads, Search Console, Bing Webmaster Tools, LinkedIn Ads, and HubSpot. Your AI runs locally (Claude Code, Cursor, etc.), Cogny provides the data pipeline.

```
Your Claude Code ──MCP──> Cogny MCP Server ──OAuth──> Google Ads / Meta / Search Console / Bing / LinkedIn / HubSpot
    (local)                (hosted)                      (your accounts)
```
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

## License

MIT
