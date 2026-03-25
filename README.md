# Claude Code Marketing Skills

AI marketing skills for Claude Code, Cursor, Windsurf, and other AI coding tools.
Analyze ads, audit SEO, research competitors, qualify leads — all from your terminal.

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
| SEO Audit | `/seo-audit` | Full technical + content SEO analysis of any website |
| Landing Page Review | `/landing-page-review` | CRO review with specific conversion recommendations |
| Competitor Analysis | `/competitor-analysis` | Research competitor positioning, ads, and market gaps |
| Ad Copy Writer | `/ad-copy-writer` | Generate ad copy variations for Google/Meta/LinkedIn |
| Lead Qualification | `/lead-qualification` | Research and qualify business leads against your ICP |

## Premium Skills (requires [Cogny Agent](https://cogny.com/agent) — $9/mo per channel)

These skills connect to your actual ad accounts via Cogny's hosted MCP servers:

| Skill | Command | MCP Server | What it does |
|-------|---------|-----------|-------------|
| Google Ads Audit | `/google-ads-audit` | Google Ads | Deep account audit — keywords, QS, budgets, search terms |
| Meta Ads Audit | `/meta-ads-audit` | Meta Ads | Audience analysis, creative fatigue, budget pacing |
| SEO Monitor | `/seo-monitor` | Search Console | Track rankings, queries, indexing, core web vitals |
| Cogny Agent | `/cogny` | All | Full autonomous agent — scheduled analysis, strategy, execution |

### Setting up Premium Skills

1. Sign up at [cogny.com/agent](https://cogny.com/agent)
2. Connect your ad accounts (Google Ads, Meta Ads, Search Console)
3. Copy your API key
4. Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "cogny": {
      "type": "http",
      "url": "https://app.cogny.com/api/lite/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

5. Run any premium skill — your AI now has direct access to your ad data.

## How It Works

**Free skills** use `WebFetch` and `WebSearch` to analyze publicly available data. No accounts or API keys needed.

**Premium skills** use [Cogny's MCP servers](https://cogny.com/agent) to connect directly to Google Ads, Meta Ads, and Search Console APIs. Your AI runs locally (Claude Code, Cursor, etc.), Cogny provides the data pipeline. $9/month per channel.

```
Your Claude Code ──MCP──> Cogny MCP Proxy ──OAuth──> Google Ads / Meta / Search Console
    (local)                (hosted)                      (your accounts)
```

## Contributing

PRs welcome! See individual skill files for the format. Skills should include:
- YAML frontmatter with metadata
- Clear step-by-step instructions
- Specific queries/actions (not vague recommendations)
- Example output format

## License

MIT
