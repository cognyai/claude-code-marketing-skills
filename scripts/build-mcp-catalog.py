#!/usr/bin/env python3
"""Build docs/mcp-catalog.json from the Cogny MCP proxy source.

Usage:
  python3 scripts/build-mcp-catalog.py <path-to>/cogny --ref <deployed tag>
  python3 scripts/build-mcp-catalog.py <path-to>/cogny/services/mcp-proxy/src/servers   # working tree

Build from the deployed tag (latest `mcp-proxy-v*`, see `git tag -l 'mcp-proxy-v*' --sort=-creatordate`),
not from a feature branch, so the catalog matches what the gateway actually serves.

The Cogny gateway (app.cogny.com/mcp) exposes every connected integration as
`mcp__<prefix>__<tool>`, where <prefix> is the integration's display name with
every character outside [a-zA-Z0-9_-] replaced by "_" ("Google Ads" ->
"Google_Ads"). When the gateway is registered in .mcp.json as "cogny", Claude
Code sees `mcp__cogny__mcp__<prefix>__<tool>`.

Only server.py modules are read: standalone*.py files are a separate local
stdio server with older tool names and are never exposed by the gateway.
"""
import ast
import json
import os
import re
import sys

# proxy dir -> (display name in Cogny, category)
SERVERS = {
    "google_ads": ("Google Ads", "paid_search"),
    "bing_ads": ("Bing Ads", "paid_search"),
    "apple_search_ads": ("Apple Search Ads", "paid_search"),
    "openai_ads": ("OpenAI Ads", "paid_search"),
    "meta_ads": ("Meta Ads", "paid_social"),
    "linkedin_ads": ("LinkedIn Ads", "paid_social"),
    "tiktok_ads": ("TikTok Ads", "paid_social"),
    "x_ads": ("X Ads", "paid_social"),
    "reddit_ads": ("Reddit Ads", "paid_social"),
    "snapchat_ads": ("Snapchat Ads", "paid_social"),
    "bidtheatre": ("Bidtheatre", "programmatic"),
    "ga4": ("Google Analytics 4", "web_analytics"),
    "plausible": ("Plausible", "web_analytics"),
    "fathom": ("Fathom Analytics", "web_analytics"),
    "simple_analytics": ("Simple Analytics", "web_analytics"),
    "adobe_analytics": ("Adobe Analytics", "web_analytics"),
    "clarity": ("Microsoft Clarity", "behavior_analytics"),
    "posthog": ("PostHog", "product_analytics"),
    "mixpanel": ("Mixpanel", "product_analytics"),
    "segment": ("Segment", "cdp"),
    "appsflyer": ("AppsFlyer", "mobile_attribution"),
    "growthbook": ("GrowthBook", "experimentation"),
    "gtm": ("Google Tag Manager", "tag_management"),
    "search_console": ("Google Search Console", "seo"),
    "bing_webmaster": ("Bing Webmaster Tools", "seo"),
    "semrush": ("Semrush", "seo"),
    "ahrefs": ("Ahrefs", "seo"),
    "ahrefs_lite": ("cogny-ahrefs-lite", "seo"),
    "ai_visibility": ("cogny-ai-visibility", "ai_search"),
    "brave_search": ("cogny-brave-search", "web_search"),
    "klaviyo": ("Klaviyo", "email"),
    "mailchimp": ("Mailchimp", "email"),
    "rule": ("Rule", "email"),
    "getanewsletter": ("Get a Newsletter", "email"),
    "brevo": ("Brevo", "email"),
    "mailerlite": ("MailerLite", "email"),
    "drip": ("Drip", "email"),
    "braze": ("Braze", "email"),
    "salesforce_marketing_cloud": ("Salesforce Marketing Cloud", "email"),
    "symplify": ("Symplify", "email"),
    "pipedrive": ("Pipedrive", "crm"),
    "upsales": ("Upsales", "crm"),
    "hubspot_forms": ("HubSpot Forms", "lead_forms"),
    "linkedin_organic": ("LinkedIn Organic", "organic_social"),
    "x_organic": ("X Organic", "organic_social"),
    "youtube": ("YouTube", "organic_social"),
    "discord": ("Discord", "community"),
    "crisp": ("Crisp", "support"),
    "shopify": ("Shopify", "ecommerce"),
    "woocommerce": ("WooCommerce", "ecommerce"),
    "abicart": ("Abicart", "ecommerce"),
    "litium": ("Litium", "ecommerce"),
    "shipstation": ("ShipStation", "ecommerce"),
    "wordpress": ("WordPress", "cms"),
    "webflow": ("Webflow", "cms"),
    "ghost": ("Ghost", "cms"),
    "framer": ("Framer", "cms"),
    "wix": ("Wix", "cms"),
    "sanity": ("Sanity", "cms"),
    "contentful": ("Contentful", "cms"),
    "fortnox": ("Fortnox", "finance"),
    "supabase": ("Supabase", "database"),
    "azure_sql": ("Azure SQL", "database"),
    "image_gen": ("cogny-image-gen", "creative"),
    "magnific": ("Magnific", "creative"),
    "bloom": ("Bloom", "other"),
}

# Servers not hosted by the proxy. Tool lists are what Cogny workspaces have
# discovered; re-check them after the vendor ships changes.
EXTERNAL = {
    "HubSpot": {
        "category": "crm",
        "note": "HubSpot's own remote MCP (mcp.hubspot.com); Cogny only handles OAuth. Read-only CRM scopes.",
        "tools": ["get_user_details", "search_crm_objects", "get_crm_objects", "search_properties",
                  "get_properties", "search_owners", "query_crm_data", "discover_hubspot_schema",
                  "get_campaign_attribution_reports"],
    },
    "Stripe": {
        "category": "billing",
        "note": "Stripe's own MCP. Reads go through stripe_api_search -> stripe_api_details -> stripe_api_read.",
        "tools": ["get_stripe_account_info", "search_stripe_documentation", "stripe_api_search",
                  "stripe_api_details", "stripe_api_read", "stripe_api_write", "stripe_implementation_planner",
                  "send_stripe_mcp_feedback"],
        "writes": ["stripe_api_write", "send_stripe_mcp_feedback"],
    },
    "agents-launch-lovable-app": {
        "category": "directory",
        "note": "agentlaunch directory (Product Hunt-style listing for AI agents), routed through Cogny.",
        "tools": ["list_agents", "get_agent", "submit_agent"],
        "writes": ["submit_agent"],
    },
    "app-fibbler-co": {
        "category": "attribution",
        "note": "Fibbler B2B ad attribution (LinkedIn/Google/Meta -> CRM deals). Pass crm=hubspot|salesforce|attio|pipedrive.",
        "tools": ["compare_campaign_periods", "get_account_overview", "get_audience_insights", "get_audience_titles",
                  "get_campaign_performance", "get_company_engagement", "get_correlation_evidence",
                  "get_cross_channel_performance", "get_customer_journey", "get_deal_attribution_summary",
                  "get_deal_campaign_breakdown", "get_google_ads_audience_insights",
                  "get_google_ads_campaign_analytics", "get_google_ads_insights", "get_influenced_deals",
                  "get_journey_benchmarks", "get_meta_ads_audience_insights", "get_meta_ads_campaign_analytics",
                  "get_meta_ads_insights", "get_trend_data", "get_warm_accounts"],
    },
}

# Tools on the Cogny gateway itself (no integration prefix). Tier decides which
# a workspace sees: Solo (lite) gets findings + task queue, Cloud gets tickets,
# BigQuery, scripts and reports. Automations and scripts are also feature-flagged.
CORE = {
    "all": ["cogny_status", "list_integrations", "start_integration_oauth", "set_integration_token",
            "disconnect_integration", "add_custom_mcp_server", "refresh_mcp_discovery",
            "get_context_tree_overview", "browse_context_tree", "read_context_node", "search_context",
            "write_context_node", "archive_context_node"],
    "solo": ["get_queue_status", "get_next_task", "complete_task", "heartbeat", "list_findings", "get_finding",
             "create_finding", "update_finding", "update_finding_status", "delete_finding", "delete_findings",
             "get_skill_package"],
    "cloud": ["list_tickets", "get_ticket", "get_winner_status", "update_ticket_status", "add_comment",
              "assign_ticket", "get_comments", "link_pr_to_ticket", "get_ticket_source_context", "create_ticket",
              "add_ticket_feedback", "list_datasets", "list_tables", "inspect_schema", "execute_bigquery_sql",
              "create_bigquery_table", "append_bigquery_rows", "create_bigquery_view", "show_report_section",
              "show_metrics", "show_budget", "list_reports", "get_report", "get_report_section"],
    "flagged": ["create_automation", "update_automation", "list_automations", "run_automation",
                "get_automation_run", "create_script", "update_script", "delete_script", "list_scripts",
                "get_script", "run_script", "get_script_run", "list_script_runs", "get_script_sdk_reference"],
}


def sanitize(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def extract(server_dir: str):
    tools = []
    for dirpath, _, files in os.walk(server_dir):
        for f in sorted(files):
            if not f.endswith(".py") or f.startswith("standalone"):
                continue
            src = open(os.path.join(dirpath, f)).read()
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            # Annotations are often module or factory constants (annotations=READ).
            consts = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    consts[node.targets[0].id] = ast.get_source_segment(src, node.value) or ""
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for dec in node.decorator_list:
                    call = dec if isinstance(dec, ast.Call) else None
                    if getattr(call.func if call else dec, "attr", None) != "tool":
                        continue
                    name, read_only = node.name, None
                    for kw in call.keywords if call else []:
                        if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                            name = kw.value.value
                        if kw.arg == "annotations":
                            seg = ast.get_source_segment(src, kw.value) or ""
                            if isinstance(kw.value, ast.Name):
                                seg = consts.get(kw.value.id, seg)
                            m = re.search(r"readOnlyHint[\"']?\s*[:=]\s*(True|False)", seg)
                            read_only = (m.group(1) == "True") if m else None
                    if read_only is None:
                        read_only = bool(re.match(r"(tool_)?(get|list|search|fetch|read|query|inspect|check|analyze|aggregate|current|domain|backlinks|keyword|phrase|run_report|run_realtime)", name))
                    tools.append({"name": name, "read_only": read_only})
    seen, out = set(), []
    for t in tools:
        if t["name"] not in seen:
            seen.add(t["name"])
            out.append(t)
    return out


def main():
    root = sys.argv[1]
    ref = None
    if "--ref" in sys.argv:
        ref = sys.argv[sys.argv.index("--ref") + 1]
        import subprocess, tempfile
        tmp = tempfile.mkdtemp(prefix="mcp-catalog-")
        archive = subprocess.run(["git", "-C", root, "archive", ref, "services/mcp-proxy/src/servers"],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", tmp], input=archive, check=True)
        root = os.path.join(tmp, "services", "mcp-proxy", "src", "servers")
    catalog = {"naming": "mcp__<prefix>__<tool>; via .mcp.json key 'cogny': mcp__cogny__mcp__<prefix>__<tool>",
               "source_ref": ref or "working tree",
               "core": CORE, "servers": {}}
    for d, (display, category) in sorted(SERVERS.items()):
        path = os.path.join(root, d)
        if not os.path.isdir(path):
            print(f"warn: {d} not found", file=sys.stderr)
            continue
        catalog["servers"][sanitize(display)] = {"display_name": display, "proxy_dir": d,
                                                 "category": category, "tools": extract(path)}
    for display, meta in EXTERNAL.items():
        catalog["servers"][sanitize(display)] = {"display_name": display, "proxy_dir": None,
                                                 "category": meta["category"], "note": meta["note"],
                                                 "tools": [{"name": t, "read_only": t not in meta.get("writes", [])}
                                                           for t in meta["tools"]]}
    missing = sorted(set(os.listdir(root)) - set(SERVERS) - {"__init__.py", "__pycache__", "list_limits.py", "zenmode"} - {x for x in os.listdir(root) if x.startswith(".")})
    if missing:
        print("warn: proxy servers without a mapping: " + ", ".join(missing), file=sys.stderr)
    out = os.path.join(os.path.dirname(__file__), "..", "docs", "mcp-catalog.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(catalog, fh, indent=1, sort_keys=False)
        fh.write("\n")
    n = sum(len(s["tools"]) for s in catalog["servers"].values())
    print(f"wrote {out}: {len(catalog['servers'])} servers, {n} tools")


if __name__ == "__main__":
    main()
