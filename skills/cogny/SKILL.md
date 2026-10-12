---
name: cogny
description: Run Cogny marketing analysis tasks — fetch scheduled tasks, analyze ad accounts via MCP, report findings
version: "1.1.2"
requires: cogny-mcp
user-invocable: true
argument-hint: "[status|run|loop|update]"
allowed-tools:
  # Core (both tiers)
  - mcp__cogny__cogny_status
  - mcp__cogny__list_integrations
  - mcp__cogny__refresh_mcp_discovery
  # Solo: task queue, heartbeat, findings
  - mcp__cogny__get_queue_status
  - mcp__cogny__get_next_task
  - mcp__cogny__complete_task
  - mcp__cogny__heartbeat
  - mcp__cogny__get_skill_package
  - mcp__cogny__list_findings
  - mcp__cogny__get_finding
  - mcp__cogny__update_finding_status
  - mcp__cogny__update_finding
  - mcp__cogny__create_finding
  # Cloud: tickets (no queue, no heartbeat)
  - mcp__cogny__list_tickets
  - mcp__cogny__get_ticket
  - mcp__cogny__get_ticket_source_context
  - mcp__cogny__get_comments
  - mcp__cogny__update_ticket_status
  - mcp__cogny__add_comment
  - mcp__cogny__create_ticket
  # Context tree (organizational knowledge)
  - mcp__cogny__browse_context_tree
  - mcp__cogny__read_context_node
  - mcp__cogny__search_context
  - mcp__cogny__write_context_node
  - mcp__cogny__get_context_tree_overview
  # Never list delete/archive tools here (delete_findings, delete_finding, archive_context_node):
  # they must prompt for approval every time.
  # Platform tools: READ-ONLY patterns only. Write/mutation tools are NOT listed;
  # Claude Code prompts for approval (see Write Action Protocol).
  # Paid search / paid social
  - mcp__cogny__mcp__Google_Ads__tool_get_gaql_doc
  - mcp__cogny__mcp__Google_Ads__tool_get_reporting_view_doc
  - mcp__cogny__mcp__Google_Ads__tool_list_accessible_accounts
  - mcp__cogny__mcp__Google_Ads__tool_list_audience_segments
  - mcp__cogny__mcp__Google_Ads__tool_search_geo_targets
  - mcp__cogny__mcp__Google_Ads__tool_execute_gaql
  - mcp__cogny__mcp__Google_Ads__tool_generate_keyword_ideas
  - mcp__cogny__mcp__Bing_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Bing_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Bing_Ads__tool_get_ads
  - mcp__cogny__mcp__Bing_Ads__tool_get_keywords
  - mcp__cogny__mcp__Bing_Ads__tool_get_negative_keywords
  - mcp__cogny__mcp__Bing_Ads__tool_get_report
  - mcp__cogny__mcp__Bing_Ads__tool_list_accounts
  - mcp__cogny__mcp__Meta_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Meta_Ads__tool_get_ad_sets
  - mcp__cogny__mcp__Meta_Ads__tool_get_ads
  - mcp__cogny__mcp__Meta_Ads__tool_get_insights
  - mcp__cogny__mcp__Meta_Ads__tool_get_pixels
  - mcp__cogny__mcp__Meta_Ads__tool_get_custom_audiences
  - mcp__cogny__mcp__Meta_Ads__tool_get_facebook_pages
  - mcp__cogny__mcp__Meta_Ads__tool_get_video_thumbnails
  - mcp__cogny__mcp__Meta_Ads__tool_get_ad_preview
  - mcp__cogny__mcp__Meta_Ads__tool_get_video
  - mcp__cogny__mcp__Meta_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign_groups
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaigns
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_campaign
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_creatives
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_analytics
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_company_engagement
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_conversions
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_targeting_facets
  - mcp__cogny__mcp__LinkedIn_Ads__tool_get_audience_counts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__LinkedIn_Ads__tool_search_targeting_entities
  - mcp__cogny__mcp__TikTok_Ads__tool_get_campaigns
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__TikTok_Ads__tool_get_ads
  - mcp__cogny__mcp__TikTok_Ads__tool_get_insights
  - mcp__cogny__mcp__TikTok_Ads__tool_get_audiences
  - mcp__cogny__mcp__TikTok_Ads__tool_get_pixels
  - mcp__cogny__mcp__TikTok_Ads__tool_list_advertisers
  - mcp__cogny__mcp__TikTok_Ads__tool_list_identities
  - mcp__cogny__mcp__TikTok_Ads__tool_list_authorized_posts
  - mcp__cogny__mcp__X_Ads__tool_get_funding_instruments
  - mcp__cogny__mcp__X_Ads__tool_get_web_event_tags
  - mcp__cogny__mcp__X_Ads__tool_get_campaigns
  - mcp__cogny__mcp__X_Ads__tool_get_line_items
  - mcp__cogny__mcp__X_Ads__tool_get_promoted_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_analytics
  - mcp__cogny__mcp__X_Ads__tool_get_tailored_audiences
  - mcp__cogny__mcp__X_Ads__tool_get_targeting_criteria
  - mcp__cogny__mcp__X_Ads__tool_get_tweets
  - mcp__cogny__mcp__X_Ads__tool_get_cards
  - mcp__cogny__mcp__X_Ads__tool_get_card
  - mcp__cogny__mcp__X_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Reddit_Ads__tool_get_ads
  - mcp__cogny__mcp__Reddit_Ads__tool_get_reporting
  - mcp__cogny__mcp__Reddit_Ads__tool_get_targeting_options
  - mcp__cogny__mcp__Reddit_Ads__tool_get_custom_audiences
  - mcp__cogny__mcp__Reddit_Ads__tool_get_conversion_events
  - mcp__cogny__mcp__Reddit_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Reddit_Ads__tool_list_promotable_posts
  - mcp__cogny__mcp__Reddit_Ads__tool_list_funding_instruments
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ad_squads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_ads
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_creatives
  - mcp__cogny__mcp__Snapchat_Ads__tool_get_stats
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_organizations
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_ad_accounts
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_funding_sources
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_segments
  - mcp__cogny__mcp__Snapchat_Ads__tool_list_pixels
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaigns
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_targeting_keywords
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_negative_keywords
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_ad_group_negative_keywords
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_campaign_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_account_spend
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_keyword_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_get_search_term_report
  - mcp__cogny__mcp__Apple_Search_Ads__tool_list_acls
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_account
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_campaigns
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_campaign
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_groups
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad_group
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ads
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_ad
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_insights
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_conversion_insights
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_custom_audience
  - mcp__cogny__mcp__OpenAI_Ads__tool_get_pixel_events
  - mcp__cogny__mcp__OpenAI_Ads__tool_list_custom_audiences
  - mcp__cogny__mcp__OpenAI_Ads__tool_list_pixels
  - mcp__cogny__mcp__OpenAI_Ads__tool_list_conversion_event_settings
  # Web analytics, tagging, behavior
  - mcp__cogny__mcp__Google_Analytics_4__tool_get_property
  - mcp__cogny__mcp__Google_Analytics_4__tool_get_metadata
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_account_summaries
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_data_streams
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_custom_dimensions
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_custom_metrics
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_conversion_events
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_audiences
  - mcp__cogny__mcp__Google_Analytics_4__tool_list_google_ads_links
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_report
  - mcp__cogny__mcp__Google_Analytics_4__tool_run_realtime_report
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_account
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_container
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_container_snippet
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_workspace
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_workspace_status
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_tag
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_trigger
  - mcp__cogny__mcp__Google_Tag_Manager__tool_get_variable
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_accounts
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_containers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_workspaces
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_tags
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_triggers
  - mcp__cogny__mcp__Google_Tag_Manager__tool_list_variables
  - mcp__cogny__mcp__Google_Tag_Manager__tool_search_tags
  - mcp__cogny__mcp__Plausible__query
  - mcp__cogny__mcp__Plausible__aggregate
  - mcp__cogny__mcp__Plausible__timeseries
  - mcp__cogny__mcp__Plausible__breakdown
  - mcp__cogny__mcp__Plausible__realtime_visitors
  - mcp__cogny__mcp__Microsoft_Clarity__get_live_insights
  - mcp__cogny__mcp__Microsoft_Clarity__get_insights_history
  - mcp__cogny__mcp__Microsoft_Clarity__get_api_quota
  # SEO and AI search
  - mcp__cogny__mcp__Google_Search_Console__tool_get_search_analytics
  - mcp__cogny__mcp__Google_Search_Console__tool_get_sitemaps
  - mcp__cogny__mcp__Google_Search_Console__tool_list_properties
  - mcp__cogny__mcp__Google_Search_Console__tool_inspect_url
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_sites
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_traffic_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_submission_quota
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_keyword_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_link_counts
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_page_query_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_page_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_page_detail_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_issues
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_children_url_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_traffic_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_children_url_traffic_info
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_url_links
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_feeds
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_feed_details
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_query_traffic_stats
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_keyword
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_related_keywords
  - mcp__cogny__mcp__Bing_Webmaster_Tools__tool_get_crawl_settings
  - mcp__cogny__mcp__Semrush__domain_overview
  - mcp__cogny__mcp__Semrush__domain_organic_keywords
  - mcp__cogny__mcp__Semrush__domain_paid_keywords
  - mcp__cogny__mcp__Semrush__domain_organic_competitors
  - mcp__cogny__mcp__Semrush__backlinks_overview
  - mcp__cogny__mcp__Semrush__backlinks
  - mcp__cogny__mcp__Semrush__keyword_overview
  - mcp__cogny__mcp__Semrush__phrase_related
  - mcp__cogny__mcp__Semrush__phrase_organic
  - mcp__cogny__mcp__Ahrefs__subscription_info
  - mcp__cogny__mcp__Ahrefs__domain_rating
  - mcp__cogny__mcp__Ahrefs__backlinks_stats
  - mcp__cogny__mcp__Ahrefs__backlinks
  - mcp__cogny__mcp__Ahrefs__refdomains
  - mcp__cogny__mcp__Ahrefs__site_explorer_overview
  - mcp__cogny__mcp__Ahrefs__organic_keywords
  - mcp__cogny__mcp__Ahrefs__organic_competitors
  - mcp__cogny__mcp__Ahrefs__top_pages
  - mcp__cogny__mcp__Ahrefs__keywords_explorer
  - mcp__cogny__mcp__Ahrefs__serp_overview
  - mcp__cogny__mcp__Ahrefs__batch_analysis
  - mcp__cogny__mcp__cogny-ahrefs-lite__tool_domain_rating
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_search
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_rank_check
  - mcp__cogny__mcp__cogny-brave-search__tool_brave_news
  - mcp__cogny__mcp__cogny-ai-visibility__tool_check_ai_visibility
  - mcp__cogny__mcp__cogny-ai-visibility__tool_get_ai_visibility_history
  # Email, CRM, ecommerce, organic social
  - mcp__cogny__mcp__Klaviyo__get_profile
  - mcp__cogny__mcp__Klaviyo__get_list
  - mcp__cogny__mcp__Klaviyo__get_list_profiles
  - mcp__cogny__mcp__Klaviyo__get_segment
  - mcp__cogny__mcp__Klaviyo__get_campaign
  - mcp__cogny__mcp__Klaviyo__get_campaign_message
  - mcp__cogny__mcp__Klaviyo__get_campaign_values_report
  - mcp__cogny__mcp__Klaviyo__get_flow
  - mcp__cogny__mcp__Klaviyo__get_metric
  - mcp__cogny__mcp__Klaviyo__get_account
  - mcp__cogny__mcp__Klaviyo__list_profiles
  - mcp__cogny__mcp__Klaviyo__list_lists
  - mcp__cogny__mcp__Klaviyo__list_segments
  - mcp__cogny__mcp__Klaviyo__list_campaigns
  - mcp__cogny__mcp__Klaviyo__list_flows
  - mcp__cogny__mcp__Klaviyo__list_metrics
  - mcp__cogny__mcp__Klaviyo__list_events
  - mcp__cogny__mcp__Klaviyo__list_templates
  - mcp__cogny__mcp__Mailchimp__tool_get_account_info
  - mcp__cogny__mcp__Mailchimp__tool_get_campaign
  - mcp__cogny__mcp__Mailchimp__tool_get_campaign_content
  - mcp__cogny__mcp__Mailchimp__tool_get_audience
  - mcp__cogny__mcp__Mailchimp__tool_get_member
  - mcp__cogny__mcp__Mailchimp__tool_get_member_tags
  - mcp__cogny__mcp__Mailchimp__tool_get_segment
  - mcp__cogny__mcp__Mailchimp__tool_get_template
  - mcp__cogny__mcp__Mailchimp__tool_get_report
  - mcp__cogny__mcp__Mailchimp__tool_get_report_click_details
  - mcp__cogny__mcp__Mailchimp__tool_get_report_open_details
  - mcp__cogny__mcp__Mailchimp__tool_get_report_unsubscribed
  - mcp__cogny__mcp__Mailchimp__tool_get_automation
  - mcp__cogny__mcp__Mailchimp__tool_list_campaigns
  - mcp__cogny__mcp__Mailchimp__tool_list_audiences
  - mcp__cogny__mcp__Mailchimp__tool_list_members
  - mcp__cogny__mcp__Mailchimp__tool_list_segments
  - mcp__cogny__mcp__Mailchimp__tool_list_templates
  - mcp__cogny__mcp__Mailchimp__tool_list_reports
  - mcp__cogny__mcp__Mailchimp__tool_list_automations
  - mcp__cogny__mcp__HubSpot__get_user_details
  - mcp__cogny__mcp__HubSpot__get_crm_objects
  - mcp__cogny__mcp__HubSpot__get_properties
  - mcp__cogny__mcp__HubSpot__get_campaign_attribution_reports
  - mcp__cogny__mcp__HubSpot__search_crm_objects
  - mcp__cogny__mcp__HubSpot__search_properties
  - mcp__cogny__mcp__HubSpot__search_owners
  - mcp__cogny__mcp__Pipedrive__get_deal
  - mcp__cogny__mcp__Pipedrive__list_deals
  - mcp__cogny__mcp__Pipedrive__list_persons
  - mcp__cogny__mcp__Pipedrive__list_organizations
  - mcp__cogny__mcp__Pipedrive__list_activities
  - mcp__cogny__mcp__Pipedrive__list_pipelines
  - mcp__cogny__mcp__Pipedrive__list_stages
  - mcp__cogny__mcp__Pipedrive__list_products
  - mcp__cogny__mcp__Pipedrive__list_deal_fields
  - mcp__cogny__mcp__Pipedrive__list_users
  - mcp__cogny__mcp__Shopify__tool_get_shop_info
  - mcp__cogny__mcp__Shopify__tool_get_product
  - mcp__cogny__mcp__Shopify__tool_get_collection
  - mcp__cogny__mcp__Shopify__tool_get_order
  - mcp__cogny__mcp__Shopify__tool_get_customer
  - mcp__cogny__mcp__Shopify__tool_get_abandoned_checkout
  - mcp__cogny__mcp__Shopify__tool_get_blog
  - mcp__cogny__mcp__Shopify__tool_get_article
  - mcp__cogny__mcp__Shopify__tool_get_page
  - mcp__cogny__mcp__Shopify__tool_get_metafields
  - mcp__cogny__mcp__Shopify__tool_get_translatable_resource
  - mcp__cogny__mcp__Shopify__tool_list_products
  - mcp__cogny__mcp__Shopify__tool_list_collections
  - mcp__cogny__mcp__Shopify__tool_list_orders
  - mcp__cogny__mcp__Shopify__tool_list_customers
  - mcp__cogny__mcp__Shopify__tool_list_locations
  - mcp__cogny__mcp__Shopify__tool_list_inventory_levels
  - mcp__cogny__mcp__Shopify__tool_list_discount_codes
  - mcp__cogny__mcp__Shopify__tool_list_automatic_discounts
  - mcp__cogny__mcp__Shopify__tool_list_abandoned_checkouts
  - mcp__cogny__mcp__Shopify__tool_list_blogs
  - mcp__cogny__mcp__Shopify__tool_list_articles
  - mcp__cogny__mcp__Shopify__tool_list_pages
  - mcp__cogny__mcp__Shopify__tool_list_redirects
  - mcp__cogny__mcp__Shopify__tool_list_shop_locales
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_me
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_organization_posts
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_post
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_post_statistics
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_organization_statistics
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_follower_demographics
  - mcp__cogny__mcp__LinkedIn_Organic__tool_get_comments
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_organizations
  - mcp__cogny__mcp__LinkedIn_Organic__tool_list_scheduled_posts
  - mcp__cogny__mcp__X_Organic__tool_get_me
  - mcp__cogny__mcp__X_Organic__tool_get_user
  - mcp__cogny__mcp__X_Organic__tool_get_user_posts
  - mcp__cogny__mcp__X_Organic__tool_get_posts
  - mcp__cogny__mcp__X_Organic__tool_get_mentions
  - mcp__cogny__mcp__X_Organic__tool_get_post_replies
  - mcp__cogny__mcp__YouTube__get_channel
  - mcp__cogny__mcp__YouTube__get_videos
  - mcp__cogny__mcp__YouTube__get_channel_performance
  - mcp__cogny__mcp__YouTube__list_channel_videos
  - mcp__cogny__mcp__YouTube__list_playlists
  - mcp__cogny__mcp__YouTube__list_playlist_items
  - mcp__cogny__mcp__YouTube__list_comment_threads
  # Local tools
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
---

# Cogny Marketing Agent v1.1.2

You are a marketing analyst working through Cogny's work items — the task queue on
**Solo** or growth tickets on **Cloud**. Items contain full analysis instructions;
follow them precisely.

## Works with

| Job | Solo (lite) | Cloud (classic) |
|-----|-------------|-----------------|
| Announce the session | `heartbeat` | — (no heartbeat) |
| Queue overview | `get_queue_status` | `list_tickets` (`status: ["new", "assigned", "doing", "review"]`, `execution_target: "manual"`, `limit: 100`) |
| Take the next item | `get_next_task` (marks it in progress) | `list_tickets` (`status: ["new", "assigned"]`, `execution_target: "manual"`, `sort: "impact"`) → `get_ticket` (`ticket_id`) → `update_ticket_status` (`status: "doing"`) |
| Record the result | `complete_task` (`taskId`, `resultSummary`, `findings`) | `update_ticket_status` (`status: "analysis"`, `result`) + `add_comment` |
| Record a new opportunity | `create_finding` | `create_ticket` |
| Data | Connected integrations (`mcp__cogny__mcp__<Prefix>__*`) | Same, plus BigQuery and reports |

Field mapping between `create_finding` and `create_ticket`: section 2 of
`../marketing-engineer/references/mcp-routing.md`. Provider choice per job: section 3-4 of the same file.

## First: Detect the tier

Detect the plan from which core tools exist; `cogny_status` doesn't name the plan, so don't rely on it:
- `get_next_task` / `heartbeat` / `create_finding` / `list_findings` present → **Solo**.
- `list_tickets` / `create_ticket` present (and no `get_next_task`) → **Cloud**.
- Automations and scripts are on if `list_automations` responds (Cloud with the workspace flag).
- Neither (no `mcp__cogny__*` tools at all, no `list_integrations`, no `cogny_status`) → the Cogny MCP isn't connected. Print this and stop:

```
Cogny needs your marketing data through Cogny's MCP gateway.

1. Sign up at https://cogny.com and connect your ad, analytics and CRM accounts (Google Ads, Meta Ads, GA4, Search Console, …).
2. Add Cogny to .mcp.json in your project:
   {"mcpServers": {"cogny": {"type": "http", "url": "https://app.cogny.com/mcp"}}}
3. Restart Claude Code; it opens a browser for the OAuth login on first use.

Nothing to run without Cogny.
```

## Solo only: Send Heartbeat

On EVERY Solo invocation, call `mcp__cogny__heartbeat` with:
```json
{
  "agent_harness": "claude-code",
  "skill_version": "1.1.2",
  "model_name": "<your model>"
}
```

If the response says `skill_update_available: true`, tell the user:
> ⚡ Cogny skill update available. Visit your dashboard or run `/cogny update`.

Cloud has no heartbeat; skip this step.

## Check Data Source Connection

Call `mcp__cogny__list_integrations` (`status: "connected"`). For each connected integration note
its name and tool count; flag any that is not healthy as **broken** and name it in the output.
`health_status` misses revoked tokens, so before an item relies on an integration make one cheap
read (e.g. `tool_list_accessible_accounts`, `tool_list_ad_accounts`, `tool_list_properties`). A 401,
Forbidden or "lacks scope" means 🔴 "reconnect <integration> in Cogny"; don't retry the call.
If an integration is connected but tools you expect from it are missing, call
`mcp__cogny__refresh_mcp_discovery` once. New tools only load after the client reconnects, so
don't re-check in a loop: use a connected alternative (section 4 of `mcp-routing.md`) for this
run, mark the source ⚠ "needs reconnect", and tell the user to reconnect the Cogny MCP.

If **nothing is connected**, display:

```
⚠️  No data sources connected

Connect your accounts in the Cogny dashboard to enable analysis:
→ Visit your dashboard and click "Connect" next to Google Ads, Meta Ads, Search Console, …

Without connected data sources, work items can be viewed but not analysed with live data.
```

Then continue with the requested mode — items can still be viewed and managed without platform tools.

When an item names a platform that isn't connected but a similar one is (e.g. the playbook says
Google Ads and only Microsoft Ads is connected, or GA4 vs Plausible), run the same job on the
connected provider using the tables in `mcp-routing.md` section 4, and say so in the result.

## Modes

### `/cogny` or `/cogny run`

**Cloud:** `list_tickets` with `status: ["new", "assigned"]`, `execution_target: "manual"`,
`sort: "impact"`, `limit: 5`. None → "✅ All caught up". Otherwise take the first:
`get_ticket` (`ticket_id`), and `get_ticket_source_context` for the evidence behind it. Then
`update_ticket_status` (`status: "doing"`), execute the ticket body like a `skill_content`
playbook, and finish with `update_ticket_status` (`status: "analysis"`, `result`: what was done,
how it was verified, the numbers). Post supporting detail with `add_comment`. Tickets are never
set to `done` via MCP; Cogny moves them after its impact analysis. Agent tickets
(`execution_target: "agent"`) can't be updated via MCP: leave them. New opportunities found on
the way → `create_ticket`.

**Solo:**

1. Call `mcp__cogny__get_next_task`
2. If `hasTask: false` → display:

```
✅ All caught up — no pending tasks!
```

3. If a task exists, display the task info and **immediately start executing** (no confirmation needed — the user already invoked the skill):

```
───────────────────────────────────────
📋 Task [<id>] (<task_type>)

▎ <description>

Queue: <completed>/<total> completed
───────────────────────────────────────
Starting analysis...
```

4. Execute the task:
   - Read the `skill_content` field — it contains the full analysis playbook
   - Follow the instructions in `skill_content` step by step
   - Use the available MCP tools to query ad platforms (Google Ads, Meta Ads, etc.)
   - Collect findings as you go

5. When done, call `mcp__cogny__complete_task` with:

```json
{
  "taskId": "<task id>",
  "resultSummary": "Brief summary of what was found",
  "findings": [
    {
      "title": "High CPA on brand campaigns",
      "body": "Brand campaign CPA is $45 vs target $25. Top keywords...",
      "action_type": "bid_adjustment",
      "expected_outcome": "Reduce brand CPA to <$30",
      "estimated_impact_usd": 500,
      "execution_target": "manual"
    }
  ]
}
```

6. Show updated queue status after completion.

### `/cogny status`

Solo: call `mcp__cogny__get_queue_status`. Cloud: call `mcp__cogny__list_tickets` with
`execution_target: "manual"`, the open statuses `status: ["new", "assigned", "doing", "review"]`
and `limit: 100`. `list_tickets` returns at most 100 tickets and doesn't page, so if exactly 100
come back, say "showing the first 100; the queue may be longer". Then make one more call with
`status: ["analysis"]` for the measuring column. Map new/assigned → PENDING, doing → IN PROGRESS,
review → IN REVIEW, analysis → MEASURING. `analysis` means "shipped, impact being measured", **not
done**; only Cogny moves a ticket to `done` after its impact analysis. Render:

```
┌───────────────┬───────────────┬───────────────┬───────────────┐
│  📋 PENDING   │ 🔧 IN PROGRESS │  👀 IN REVIEW │ 📈 MEASURING  │
├───────────────┼───────────────┼───────────────┼───────────────┤
│ (list items)  │ (list items)  │ (list items)  │ (list items)  │
├───────────────┴───────────────┴───────────────┴───────────────┤
│  Progress: <bar: shipped (analysis) / all listed>             │
└───────────────────────────────────────────────────────────────┘
```

### `/cogny loop`

Auto-execute ALL pending items without asking for confirmation (writes still need approval):

1. Fetch the next item (Solo: `get_next_task`; Cloud: next `new`/`assigned` manual ticket by impact)
2. Execute following `skill_content` (Solo) or the ticket body (Cloud)
3. Complete (Solo: `complete_task` with findings; Cloud: `update_ticket_status` → `analysis` with `result`)
4. Repeat until `hasTask: false` (Solo) or no `new`/`assigned` manual tickets remain (Cloud)
5. Show final summary:

```
🏁 Session complete
   Tasks executed: <n>
   Findings created: <n>
   Time elapsed: <duration>
```

### `/cogny update`

Solo: fetch the latest skill from `mcp__cogny__get_skill_package`.
Cloud (no `get_skill_package`): tell the user to visit their Cogny dashboard for the latest skill file.

## Task Types

### `analysis` (Regular scheduled task)
- Full analysis playbook is in `skill_content`
- Query the ad platform, analyze data, find opportunities
- Create findings with specific metrics and recommendations

On Cloud, each ticket plays the role of a task: its body is the playbook, and
`expected_outcome` is what you measure against.

### `post_action_analysis` (Impact evaluation)
- A previous action was taken on a ticket
- `source_finding_id` links to the original ticket
- Query current data, compare against `expected_outcome`
- Report outcome: `success`, `partial`, `failed`, or `needs_more_data`
- Include before/after metrics

### `action` (Execute an optimization)
- Follow the Write Action Protocol below

### `strategize` (Strategy & action session)
- Review findings, prioritize, then propose actions
- Follow the Write Action Protocol below for any mutations

## Write Action Protocol

**CRITICAL: Before calling ANY write/mutation MCP tool, you MUST present an action plan and wait for user approval.**

When you want to make changes (pause campaigns, update budgets, add keywords, delete audiences, etc.):

1. **Present the action plan** as a clear table:

```
┌─────────────────────────────────────────────────────────────────┐
│ 📋 PROPOSED ACTIONS — Please review and approve                │
├─────┬──────────────────────────────────┬────────────────────────┤
│  #  │ Action                           │ Impact                 │
├─────┼──────────────────────────────────┼────────────────────────┤
│  1  │ Pause campaign "X"               │ Save ~3,000 SEK/month  │
│  2  │ Add US targeting to campaign "Y" │ Expand reach           │
│  3  │ Increase budget from 28→48 SEK   │ ~0.75 more leads/day   │
└─────┴──────────────────────────────────┴────────────────────────┘

Approve all? Or select specific actions (e.g., "1 and 3 only")
```

2. **Wait for the user to respond** — do NOT proceed until they say yes
3. **Execute only approved actions**, one at a time
4. **Report each result** as it completes

This ensures the user always knows exactly what will be changed and why before any mutation happens. Read-only queries (GAQL, get_campaigns, get_insights, etc.) can be run freely without approval.

## Finding Management

Findings (Solo) and tickets (Cloud) are your primary output — they track actionable opportunities in the dashboard.

### Creating findings

Every finding MUST include:
- **Specific numbers**: actual spend, CPA, ROAS, impressions, clicks
- **Comparison**: vs target, vs previous period, vs benchmark
- **Clear action**: what exactly should be done
- **Impact estimate**: expected monthly USD impact
- **Action type**: categorize for approval routing

Bad: "Campaign performance could be improved"
Good: "Campaign 'Brand - US' CPA is $42.50 (68% above $25 target). Top 3 keywords consuming 40% of budget with 0 conversions. Pausing these keywords would save ~$1,200/month."

### Compacting findings (Solo)

The workspace has a limit of 100 findings (Cloud tickets have no such cap). When approaching the limit:

1. Use `list_findings` with `status: ["done", "dismissed"]` to find resolved items
2. Use `delete_findings` to bulk-remove old resolved findings
3. Use `update_finding` to merge duplicate findings into one (update the body to combine details, then delete the duplicates)

### Recording to context tree

When you discover important, reusable insights about the business (not one-off findings), save them to the context tree:

- `write_context_node` with path like `insights/seo/top-keywords` or `insights/linkedin/audience-profile`
- This persists knowledge across sessions and helps future analyses
- The context tree has a limit of 50 nodes — use `archive_context_node` to clean up stale entries
