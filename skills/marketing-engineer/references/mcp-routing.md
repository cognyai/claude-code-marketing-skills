# Cogny MCP routing guide

Shared by every skill in this repo. It says which tool to call for a job, on whichever
provider the workspace has connected. Generated tool lists live in `docs/mcp-catalog.json`
(built from the Cogny MCP proxy, `cogny/services/mcp-proxy`); run
`python3 scripts/check-tool-names.py` after editing any skill.

## 0. When Cogny isn't connected

Every skill that uses Cogny starts with this check. If no `mcp__cogny__*` tools exist (no
`list_integrations`, no `cogny_status`), print this block, filled in for the skill, and then
either take the skill's local fallback (say which) or stop. Never fail on a missing tool, and
never point to the repo README (it isn't installed with the skills).

```
<Skill> needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect <the integrations this skill uses>.
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

<Without Cogny you can still: <the local fallback>, or "Nothing to run without Cogny.">
```

When Cogny *is* connected but the integration this skill needs isn't, say "connect <X> in Cogny"
instead. They're already subscribed, so don't ask them to sign up.

## 1. Tool names

The Cogny gateway (`https://app.cogny.com/mcp`) federates every connected integration as
`mcp__<Prefix>__<tool>`. `<Prefix>` is the integration's display name with every character
outside `[a-zA-Z0-9_-]` replaced by `_`:

| Client sees | Example |
|-------------|---------|
| Claude Code with `.mcp.json` key `cogny` | `mcp__cogny__mcp__Google_Ads__tool_execute_gaql` |
| claude.ai connector "Cogny" | `mcp__claude_ai_Cogny__mcp__Google_Ads__tool_execute_gaql` |
| `@cogny/cli` | `cogny tools call mcp__Google_Ads__tool_execute_gaql` |

Skills write the first form. If a client shows another, map it by swapping the leading part.

- Cogny-native servers keep their own prefixes: `cogny-brave-search`, `cogny-ai-visibility`,
  `cogny-image-gen`, `cogny-ahrefs-lite`.
- **HubSpot** is HubSpot's own MCP (`mcp.hubspot.com`). Cogny only handles OAuth, so its
  tools (`search_crm_objects`, `get_user_details`, `search_properties`, …) carry no `tool_` prefix and only
  read CRM scopes. **HubSpot Forms** is a separate proxy connection (`list_forms`, `get_form_submissions`).
- **Stripe** and **Fibbler** (`app-fibbler-co`) are vendor MCPs routed through Cogny.
- **Legacy names** like `mcp__cogny__google_ads__tool_execute_gaql` are no longer served. <!-- check-tool-names: ignore -->
- **A tool that should exist is missing?** Workspaces cache the tool list from when the
  integration was connected, so `docs/mcp-catalog.json` can list tools a workspace doesn't expose
  yet. Call `refresh_mcp_discovery` once. The server picks up the new tools, but **the client only
  sees them after it reconnects**, so they won't load in the current run. Use the skill's named
  fallback for this run, mark the source ⚠ "needs reconnect", and tell the user to reconnect the
  Cogny MCP. Never loop on refresh.

## 2. Health checks and what each plan sees

`list_integrations` `health_status` misses revoked tokens: a LinkedIn Ads token that returns 401
still reads `healthy`. Before relying on an integration, make **one cheap read** (e.g.
`tool_list_ad_accounts`, `tool_list_properties`, `list_guilds`) and treat 401, Forbidden or
"lacks scope" as 🔴 broken: say "reconnect <integration>" and don't retry the same call.
A passing account call doesn't prove the data calls work: a token can list accounts but lack the
reporting scope (TikTok `40001` on `tool_get_insights`). Treat a scope error on any data call the
same way, as 🔴 for that source. On a 5xx or timeout from a read, retry **once**; if it fails again,
mark the source ⚠ and continue.
Cogny-native servers (`cogny-brave-search`, `cogny-ai-visibility`, `cogny-ahrefs-lite`,
`cogny-image-gen`) don't appear in `list_integrations`. Treat them as available if their tools load.

**Detect the plan from the tools that exist**: Cloud if `create_ticket` / `list_tickets` exist,
Solo if `create_finding` / `list_findings` exist. Automations are on if `list_automations`
responds. `cogny_status` doesn't name the plan.

| Capability | Solo (lite) | Cloud (classic) |
|------------|-------------|-----------------|
| Connected integrations (`mcp__<Prefix>__*`) | ✅ | ✅ |
| Context tree (`read_context_node`, `write_context_node`, `search_context`, …) | ✅ | ✅ |
| Record a work item | `create_finding` | `create_ticket` |
| Work queue | `get_queue_status`, `get_next_task`, `complete_task`, `heartbeat` | `list_tickets`, `get_ticket`, `update_ticket_status` |
| BigQuery (`execute_bigquery_sql`, …), reports | ❌ | ✅ |
| Scripts (`create_script`, …) and automations (`create_automation`, …) | ❌ | ✅ when the workspace flag is on |
| Image generation (`cogny-image-gen`) | ❌ | ✅ |

### Recording findings on either plan

Use `create_ticket` if the tool exists; otherwise `create_finding`. Same content, different fields:

| Meaning | `create_ticket` (Cloud) | `create_finding` (Solo) |
|---------|------------------------|-------------------------|
| Decision to make | `title` | `title` |
| Evidence, what it touches, how to do it | `body` | `body` |
| Measurable result | `expected_outcome` (required) | `expected_outcome` |
| Monthly $ impact | `estimated_impact_usd` | `estimated_impact_usd` |
| Category | put it in `body` ("Type: budget_adjustment") | `action_type` |
| Urgency | prefix the title ("[Critical] …") | `priority` |
| Spend it activates | `estimated_cost_usd`, `cost_cadence`, `cost_type` | put it in `body` |
| Who acts | `execution_target: "manual"` | — |
| Already done, measure it | `already_done: true` + `result` | `update_finding_status` after creating |

`list_tickets` returns at most 100 results and doesn't page. Filter with `execution_target: "manual"`
and the open statuses (`new`, `assigned`, `doing`, `review`), then filter titles client-side.
Ticket status `analysis` means "shipped, impact being measured", not done.

Solo caps findings at 100. If the cap is hit, `list_findings` and merge or delete stale ones
before creating new ones.

## 3. Choosing a provider

1. Call `list_integrations` (or `cogny_status`) once. Treat any integration whose
   `health_status` is not healthy as **broken**, and name it in the output.
2. For each job a skill needs, take the connected providers in that job's category (tables below).
   - **One connected:** use it.
   - **Several connected:** run the job on each and report them **side by side**. Never
     merge different providers' numbers into one total unless the definitions match and the
     currency is the same.
   - **None connected:** use the skill's stated fallback (public web data, a local export, or
     asking the user), and say which integration would have answered it.
3. Name the provider on every number ("Klaviyo: 41% open rate"). Definitions differ: Apple
   Mail Privacy inflates opens on some ESPs, Meta counts link clicks differently from LinkedIn, and so on.
4. Use each account's own currency. Read it from the platform; don't assume USD.

## 4. Same job, different providers

Tool names are given without the `mcp__cogny__mcp__<Prefix>__` part.

### Paid media: accounts, structure, performance, pause

| Provider (Prefix) | Accounts | Campaigns / ad sets / ads | Performance | Pause (write, ask first) |
|-------------------|----------|---------------------------|-------------|--------------------------|
| Google Ads (`Google_Ads`) | `tool_list_accessible_accounts` | `tool_execute_gaql` (`campaign`, `ad_group`, `ad_group_ad`) | `tool_execute_gaql` with `metrics.*` (CTR is a fraction; cost in micros) | `tool_update_ad_status`, `tool_update_ad_group_status`, `tool_update_campaign_status` |
| Microsoft Ads (`Bing_Ads`) | `tool_list_accounts` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads`, `tool_get_keywords` | `tool_get_report` (percents are percents) | `tool_update_ad_status`, `tool_update_campaign` |
| Apple Search Ads (`Apple_Search_Ads`) | `tool_list_acls` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_targeting_keywords` | `tool_get_campaign_report`, `tool_get_keyword_report`, `tool_get_search_term_report` | see catalog |
| ChatGPT ads (`OpenAI_Ads`) | `tool_get_ad_account` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads` | `tool_get_insights`, `tool_get_conversion_insights` | see catalog |
| Meta (`Meta_Ads`) | `tool_list_ad_accounts` | `tool_get_campaigns`, `tool_get_ad_sets`, `tool_get_ads` (use `effective_status`) | `tool_get_insights` (`level`) | `tool_update_ad_status`, `tool_update_ad_set_status`, `tool_update_campaign_status` |
| LinkedIn (`LinkedIn_Ads`) | `tool_list_ad_accounts` | `tool_get_campaign_groups`, `tool_get_campaigns`, `tool_get_creatives` | `tool_get_analytics`, `tool_get_company_engagement` | `tool_update_campaign_status`, `tool_update_creative_status` |
| TikTok (`TikTok_Ads`) | `tool_list_advertisers` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads` | `tool_get_insights` (`level: AUCTION_*`) | `tool_update_ad_status`, `tool_update_ad_group_status` |
| X (`X_Ads`) | `tool_list_ad_accounts` | `tool_get_campaigns`, `tool_get_line_items`, `tool_get_promoted_tweets`, `tool_get_cards` (UTMs live on cards) | `tool_get_analytics` (needs `entity_ids`) | `tool_update_promoted_tweet_status`, `tool_update_line_item_status` |
| Reddit (`Reddit_Ads`) | `tool_list_ad_accounts` | `tool_get_campaigns`, `tool_get_ad_groups`, `tool_get_ads` | `tool_get_reporting` | see catalog |
| Snapchat (`Snapchat_Ads`) | `tool_list_organizations` → `tool_list_ad_accounts` | `tool_get_campaigns`, `tool_get_ad_squads`, `tool_get_ads` | `tool_get_stats` | see catalog |
| Programmatic (`Bidtheatre`) | `list_advertisers` | `list_campaigns`, `get_campaign` | `get_report` | see catalog |
| B2B attribution (`app-fibbler-co`) | — | — | `get_cross_channel_performance`, `get_deal_attribution_summary`, `get_warm_accounts` | read-only |

Use `see catalog` cells by searching `docs/mcp-catalog.json` for the provider's `update_*` tools.

### Web, product and mobile analytics

| Provider | Traffic and conversions | Notes |
|----------|-------------------------|-------|
| `Google_Analytics_4` | `tool_run_report` (dimensions/metrics), `tool_list_conversion_events` | Key events by `sessionCampaignName`, `sessionSourceMedium` |
| `Plausible` | `aggregate`, `timeseries`, `breakdown` (`visit:source`, `visit:utm_campaign`) | Goals are conversions |
| `Fathom_Analytics` | `aggregate` (`entity: pageview \| event`), `list_events` | Web analytics, **not** the Fathom call recorder |
| `Simple_Analytics` | `stats`, `pages`, `referrers`, `events` | |
| `Adobe_Analytics` | `run_report` | Report-suite based |
| `Microsoft_Clarity` | `get_insights_history`, `get_live_insights` | Rage/dead clicks, scroll depth for CRO |
| `PostHog` | `list_insights`, `get_insight`, `list_events`, `list_cohorts`, `list_session_recordings` | Product funnels, activation |
| `Mixpanel` | `list_funnels`, `get_funnel`, `get_retention`, `list_cohorts` | Retention |
| `Segment` | `get_events_volume`, `list_tracking_plans` | Tracking-plan audits |
| `AppsFlyer` | `get_partners_report`, `get_daily_report`, `get_raw_in_app_events` | Mobile installs by media source |
| `GrowthBook` | `list_experiments`, `get_experiment_results` | A/B results, so don't re-test what was already tested |

### SEO and AI search

| Job | Tools |
|-----|-------|
| Queries, pages, CTR (Google) | `Google_Search_Console`: `tool_get_search_analytics`, `tool_inspect_url`, `tool_get_sitemaps` |
| Queries, pages, crawl (Bing, which feeds Copilot) | `Bing_Webmaster_Tools`: `tool_get_query_stats`, `tool_get_page_stats`, `tool_get_keyword_stats`, `tool_get_crawl_issues`, `tool_get_url_info` |
| Keyword research | `Semrush`: `keyword_overview`, `phrase_related`, `phrase_organic` · `Ahrefs`: `keywords_explorer`, `serp_overview` · `Google_Ads`: `tool_generate_keyword_ideas` |
| Competitors' rankings | `Semrush`: `domain_organic_keywords`, `domain_organic_competitors` · `Ahrefs`: `organic_keywords`, `organic_competitors`, `top_pages` |
| Backlinks / authority | `Ahrefs`: `backlinks`, `refdomains`, `domain_rating` · `Semrush`: `backlinks_overview` · `cogny-ahrefs-lite`: `tool_domain_rating` (show "Domain Rating by Ahrefs") |
| AI answer engines | `cogny-ai-visibility`: `tool_check_ai_visibility`, `tool_get_ai_visibility_history` |
| Live SERP / news | `cogny-brave-search`: `tool_brave_search`, `tool_brave_rank_check`, `tool_brave_news` |

### Email and lifecycle

| Provider | Campaigns / sends | Performance | Audience | Automations |
|----------|-------------------|-------------|----------|-------------|
| `Klaviyo` | `list_campaigns`, `get_campaign_message` | `get_campaign_values_report` | `list_segments`, `list_profiles` | `list_flows`, `get_flow` |
| `Mailchimp` | `tool_list_campaigns`, `tool_get_campaign_content` | `tool_get_report`, `tool_get_report_click_details` | `tool_list_audiences`, `tool_list_members`, `tool_list_segments` | `tool_list_automations` |
| `Rule` | `tool_list_campaigns`, `tool_get_campaign` | `tool_get_campaign_statistics` | `tool_list_subscribers`, `tool_list_segments`, `tool_list_suppressions` | `tool_list_journeys` |
| `Get_a_Newsletter` | `tool_list_sent`, `tool_get_sent`, `tool_list_drafts` | `tool_get_report`, `tool_get_report_link_clicks` | `tool_list_contacts`, `tool_list_lists` | — |
| `Brevo` | `list_email_campaigns`, `get_email_campaign` | `get_smtp_report` | `list_contacts`, `list_contact_lists` | — |
| `MailerLite` | `list_campaigns`, `get_campaign` | `get_campaign_activity` | `list_subscribers`, `list_groups`, `list_segments` | — |
| `Drip` | `list_campaigns`, `get_campaign` | not exposed (no per-email open/click rates) | `list_subscribers`, `list_tags` | `list_workflows` |
| `Salesforce_Marketing_Cloud` | `list_email_sends`, `list_assets` | `get_journey_email_performance`, `get_triggered_send_summary` | `list_data_extensions` | `list_journeys` |
| `Symplify` | `get_campaign_overview` | `get_campaign_report`, `get_campaign_link_performance` | `get_contact` | `list_journeys` |
| `Braze` | see catalog | see catalog | see catalog | see catalog |

### CRM, sales and support

| Job | HubSpot (`HubSpot`) | Pipedrive (`Pipedrive`) | Upsales (`Upsales`) |
|-----|---------------------|-------------------------|---------------------|
| Deals | `search_crm_objects` (`deals`) | `list_deals`, `get_deal`, `list_stages` | `list_opportunities`, `list_orders` |
| People / companies | `search_crm_objects` (`contacts`, `companies`) | `list_persons`, `list_organizations` | `list_contacts`, `list_accounts` |
| Calls, meetings, notes | `search_crm_objects` (`calls`, `meetings`, `notes`) | `list_activities` | `list_activities`, `list_appointments` |
| Field definitions | `search_properties`, `discover_hubspot_schema` | `list_deal_fields` | `get_metadata` |
| Lead forms | `HubSpot_Forms`: `get_form_submissions` | — | `list_leads` |

Support and community conversations: `Crisp` (`list_conversations`, `get_conversation_messages`),
`Discord` (`get_channel_messages`). Salesforce CRM, Attio and others connect through
`add_custom_mcp_server`; map them onto the same jobs.

### Organic social and video

| Provider | Own posts and stats | Listening | Publish (write, approval only) |
|----------|---------------------|-----------|--------------------------------|
| `LinkedIn_Organic` | `tool_get_organization_posts`, `tool_get_post_statistics`, `tool_get_organization_statistics` | `tool_get_comments` | `tool_schedule_post`, `tool_create_post` |
| `X_Organic` | `tool_get_user_posts`, `tool_get_posts` | `tool_search_recent_posts`, `tool_get_mentions` | `tool_create_post`, `tool_create_thread` |
| `YouTube` | `list_channel_videos`, `get_videos`, `get_channel_performance` | `list_comment_threads`, `search_videos` | — |

### Ecommerce, CMS and finance

| Job | Providers |
|-----|-----------|
| Orders, revenue, refunds | `Shopify` (`tool_list_orders`), `WooCommerce` (`list_orders`, `get_sales_report`, `list_order_refunds`), `Abicart` (`get_sales_summary`), `Litium` (`get_sales_summary`), `Wix` (`search_orders`) |
| Products / catalog | `Shopify` (`tool_list_products`), `WooCommerce` (`list_products`), `Abicart` (`list_articles`), `Litium` (`search_products`) |
| Abandoned checkouts | `Shopify` (`tool_list_abandoned_checkouts`) |
| Pages and posts | `WordPress`, `Webflow`, `Ghost`, `Framer`, `Wix`, `Sanity` (`tool_query_groq`), `Contentful` |
| Subscriptions, churn | `Stripe` (`stripe_api_read`: `GetSubscriptions`, `GetRefunds`) |
| Invoices, bookkeeping | `Fortnox` (`list_invoices`, `list_customers`) |
| Shipping | `ShipStation` |

## 5. Source-specific rules learned from live runs

- **Discord:** a channel is private when its `permission_overwrites` (or its parent category's)
  contain an entry with `id == guild_id` that denies `VIEW_CHANNEL` (bit 1024). Never quote private
  channels in reports, ads or posts; use them only as anonymised themes. Exclude `author.bot` and
  staff ids. A `Forbidden` on one channel means the bot lacks access: list it as "not readable" and
  continue. `get_channel_messages` has no date filter (it pages by snowflake `before`/`after`) and
  returns the full author object per message, so use `limit: 50`.
- **X:** `tool_upload_media` takes a `file_path` on the proxy host, not a URL. A generated image
  can't be uploaded from Cloud, so reuse an existing `media_key` or upload it in X Ads. X Organic has
  no promoted flag; drop promoted posts by matching `X_Ads` `tool_get_promoted_tweets` tweet ids.
  `exclude_replies` still returns self-thread replies, so also drop posts whose `in_reply_to_user_id`
  is the account's own id. Private metrics exist only for posts from the last 30 days, and
  `url_link_clicks` is null on posts without a link.
- **X Ads:** `tool_get_analytics` accepts at most 20 `entity_ids` per call, so batch them. Line items
  have no `effective_status`, so judge activity from the campaign's `effective_status` plus the line
  item's `entity_status`.
- **AI visibility:** a client timeout doesn't mean the check failed, because checks are stored
  server-side. Read `tool_get_ai_visibility_history` (same tag) before retrying, or you pay twice.
- **Search Console:** data lags about 3 days, so end windows 3 days ago. `tool_get_sitemaps`
  doesn't fill the indexed count; sample `tool_inspect_url` instead. Query pulls over ~500 rows get large.
- **Bing Webmaster:** `tool_get_keyword_stats` returns the site's own query data, not search
  volume, and can come back `{"d":[]}`. `tool_get_link_counts` can be empty while `tool_get_crawl_stats`
  shows InLinks, so use that as the fallback.
- **Brave:** `tool_brave_rank_check` with `max_results` above 20 returns very large payloads. A
  roundup or listicle that mentions a company is not an event about that company.
- **Stripe:** workspaces often use a restricted key (`rk_live`), which fails `get_stripe_account_info`
  ("Accounts Read") but reads subscriptions fine. Probe with `stripe_api_read` `GetSubscriptions {limit: 1}`.
  For SaaS, Stripe is the revenue source. Use `GetSubscriptions`, `GetInvoices` and
  `GetRefunds` where store or CRM revenue is used elsewhere.
- **Pages:** WebFetch summarises page bodies and can't see `<head>` tags. Use `curl -sL` via Bash
  for titles, metas, canonicals and JSON-LD.

## 6. Writes

Every write tool needs the user's explicit yes in the current session, unless an automation was
granted it with `constraints`. Create ads paused, save emails as drafts, schedule posts only after
approval, and never raise a budget the user didn't state.
