---
name: google-ads-scripts
description: Google Ads Scripts Reference — JavaScript automation, AdsApp object model, selectors, GAQL queries, 10+ working script patterns, MCC parallel processing, Sheets integration
version: "1.0.0"
author: Cogny AI
platforms: []
user-invocable: true
argument-hint: "<script pattern or topic>"
allowed-tools:
  - WebSearch
  - Read
  - Write
  - Bash
  # Google Ads tools (when connected via Cogny MCP)
  - mcp__cogny__google_ads__tool_execute_gaql
  - mcp__cogny__google_ads__tool_get_gaql_doc
  - mcp__cogny__google_ads__tool_get_reporting_view_doc
  - mcp__cogny__google_ads__tool_list_accessible_accounts
---

# Google Ads Scripts Reference

Complete reference for Google Ads Scripts: JavaScript automation within Google Ads, AdsApp object model, selectors and iterators, GAQL queries, common script patterns with working code, Google Sheets integration, MCC parallel processing, and best practices.

Full docs: https://cogny.com/docs/google-ads-scripts

## Usage

```
/google-ads-scripts                          # Full overview
/google-ads-scripts budget pacing            # Budget pacing monitor script
/google-ads-scripts negative keywords        # Search term negative keyword miner
/google-ads-scripts quality score tracker    # Quality score logging to Sheets
/google-ads-scripts MCC parallel             # MCC parallel processing pattern
/google-ads-scripts selectors                # Selector and iterator patterns
/google-ads-scripts GAQL                     # GAQL queries in scripts
/google-ads-scripts anomaly detection        # Anomaly alerting script
```

## Instructions

You are a Google Ads Scripts expert. Use this reference to help users write, debug, and optimize Google Ads Scripts. Provide complete, working code with proper error handling and best practices.

When the user asks a question, find the relevant section below and provide precise, actionable answers with ready-to-use JavaScript code.

If the user provides a specific topic as an argument, focus on that area. Otherwise, provide an overview of capabilities and common patterns.

Key principles:
- Always include a `DRY_RUN` flag in scripts that modify the account
- Log changes before making them
- Use `try/catch` for error handling
- Prefer GAQL (`AdsApp.search()`) for complex queries
- Batch Google Sheets writes for performance
- Remind users about the 30-minute execution limit (60 min for MCC)

---

## Overview

Google Ads Scripts let you programmatically control Google Ads using JavaScript. Scripts run directly inside the Google Ads web interface — no external server, API keys, or OAuth needed.

**Key capabilities:**
- Read and modify campaigns, ad groups, ads, keywords, extensions
- Query performance data using GAQL (Google Ads Query Language)
- Integrate with Google Sheets for dashboards and logging
- Send email alerts via MailApp
- Make HTTP requests via UrlFetchApp
- Run on a schedule (hourly, daily, weekly, monthly)

**Single-account vs MCC scripts:**

| Feature | Single-Account | MCC Script |
|---------|---------------|------------|
| Scope | One account | All accounts under MCC |
| Entry point | `main()` | `main()` with `AdsManagerApp` |
| Execution limit | 30 minutes | 60 minutes |
| Parallel execution | No | Yes, `executeInParallel()` |

**Language:** JavaScript ES5 with some ES6. `let`, `const`, arrow functions, template literals work. `async`/`await`, `import`/`export`, `class` do not.

## AdsApp Object Model

The `AdsApp` object is the root of all single-account operations.

### Entity Hierarchy

```
AdsApp
  +-- campaigns()
  |     +-- adGroups()
  |     |     +-- ads()
  |     |     +-- keywords()
  |     |     +-- audiences()
  |     +-- extensions()
  +-- adGroups()        (account-level shortcut)
  +-- ads()             (account-level shortcut)
  +-- keywords()        (account-level shortcut)
  +-- negativeKeywords()
  +-- shoppingCampaigns()
  +-- videoCampaigns()
  +-- labels()
  +-- budgets()
  +-- biddingStrategies()
```

### Common Entity Methods

```javascript
// Status
entity.isEnabled()
entity.isPaused()
entity.isRemoved()
entity.enable()
entity.pause()
entity.remove()

// Naming
entity.getName()
entity.setName('New Name')

// Stats (requires date range)
entity.getStatsFor('LAST_30_DAYS')
entity.getStatsFor('20250101', '20250131')

// Stats object methods
var stats = entity.getStatsFor('LAST_30_DAYS');
stats.getImpressions()
stats.getClicks()
stats.getCtr()
stats.getAverageCpc()
stats.getCost()
stats.getConversions()
stats.getConversionRate()
```

## Selectors and Iterators

Every entity collection uses the selector-iterator pattern — the fundamental data access pattern in every script.

### Selector Methods

```javascript
var keywords = AdsApp.keywords()
  .withCondition('Status = ENABLED')
  .withCondition('CampaignStatus = ENABLED')
  .withCondition('AdGroupStatus = ENABLED')
  .withCondition('Ctr < 0.01')
  .forDateRange('LAST_30_DAYS')
  .orderBy('Impressions DESC')
  .withLimit(100)
  .get();
```

**`.withCondition(condition)`** — Filter entities. Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`, `CONTAINS`, `DOES_NOT_CONTAIN`, `STARTS_WITH`, `CONTAINS_IGNORE_CASE`, `REGEXP_MATCH`, `IN []`.

```javascript
.withCondition('Name CONTAINS "brand"')
.withCondition('Name REGEXP_MATCH "^(buy|shop|order).*"')
.withCondition('QualityScore > 5')
.withCondition('LabelNames CONTAINS_ANY ["Priority", "Monitor"]')
.withCondition('CampaignName IN ["Search - Brand", "Search - Generic"]')
```

**`.forDateRange(dateRange)`** — Required for metrics-based conditions. Predefined ranges: `TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `THIS_WEEK_SUN_TODAY`, `THIS_WEEK_MON_TODAY`, `LAST_WEEK`, `LAST_14_DAYS`, `LAST_30_DAYS`, `LAST_BUSINESS_WEEK`, `LAST_WEEK_SUN_SAT`, `THIS_MONTH`, `LAST_MONTH`, `ALL_TIME`.

```javascript
// Custom date range
.forDateRange('20250101', '20250131')
```

**`.orderBy(orderSpec)`** — Sort results (`ASC` / `DESC`).

**`.withLimit(limit)`** — Cap the number of results.

### Iterator Pattern

```javascript
var iterator = AdsApp.keywords()
  .withCondition('Status = ENABLED')
  .forDateRange('LAST_7_DAYS')
  .withCondition('Impressions > 100')
  .get();

while (iterator.hasNext()) {
  var keyword = iterator.next();
  var stats = keyword.getStatsFor('LAST_7_DAYS');
  Logger.log(keyword.getText() + ': ' + stats.getClicks() + ' clicks');
}
```

## GAQL in Scripts

Google Ads Query Language provides SQL-like access to the full Google Ads API from within scripts.

### AdsApp.search(query)

Returns an iterator of result rows as JavaScript objects.

```javascript
function main() {
  var query = "SELECT " +
    "campaign.name, " +
    "campaign.status, " +
    "metrics.impressions, " +
    "metrics.clicks, " +
    "metrics.cost_micros, " +
    "metrics.conversions " +
    "FROM campaign " +
    "WHERE campaign.status = 'ENABLED' " +
    "AND segments.date DURING LAST_30_DAYS " +
    "ORDER BY metrics.cost_micros DESC";

  var results = AdsApp.search(query);

  while (results.hasNext()) {
    var row = results.next();
    Logger.log(row.campaign.name +
      ' | Cost: $' + (row.metrics.costMicros / 1000000).toFixed(2) +
      ' | Conversions: ' + row.metrics.conversions);
  }
}
```

### AdsApp.report(query)

Returns a report object with export capabilities — best for bulk data and Sheets integration.

```javascript
var report = AdsApp.report(
  "SELECT " +
  "ad_group_criterion.keyword.text, " +
  "ad_group_criterion.quality_info.quality_score, " +
  "metrics.impressions, " +
  "metrics.clicks, " +
  "metrics.conversions " +
  "FROM keyword_view " +
  "WHERE campaign.status = 'ENABLED' " +
  "AND segments.date DURING LAST_30_DAYS"
);

// Export directly to Google Sheets
var sheet = SpreadsheetApp.openByUrl('YOUR_SHEET_URL').getActiveSheet();
report.exportToSheet(sheet);
```

### Search vs Report

| Feature | `AdsApp.search()` | `AdsApp.report()` |
|---------|-------------------|-------------------|
| Return type | Row iterator | Report object |
| Field access | `row.campaign.name` | Row iterator or `exportToSheet()` |
| Sheet export | Manual | Built-in `exportToSheet()` |
| Best for | Processing rows individually | Bulk export, dashboards |

## Common Script Patterns

### 1. Pause Low-Performing Keywords

```javascript
function main() {
  var CONFIG = {
    MIN_QUALITY_SCORE: 4,
    MIN_CTR: 0.005,
    MIN_IMPRESSIONS: 100,
    DATE_RANGE: 'LAST_30_DAYS',
    DRY_RUN: true
  };

  var query = "SELECT " +
    "ad_group_criterion.keyword.text, " +
    "ad_group_criterion.keyword.match_type, " +
    "ad_group_criterion.quality_info.quality_score, " +
    "ad_group.name, " +
    "campaign.name, " +
    "metrics.impressions, " +
    "metrics.clicks, " +
    "metrics.ctr, " +
    "metrics.cost_micros, " +
    "metrics.conversions " +
    "FROM keyword_view " +
    "WHERE campaign.status = 'ENABLED' " +
    "AND ad_group.status = 'ENABLED' " +
    "AND ad_group_criterion.status = 'ENABLED' " +
    "AND metrics.impressions > " + CONFIG.MIN_IMPRESSIONS + " " +
    "AND segments.date DURING " + CONFIG.DATE_RANGE;

  var results = AdsApp.search(query);
  var pauseCount = 0;

  while (results.hasNext()) {
    var row = results.next();
    var qs = row.adGroupCriterion.qualityInfo.qualityScore;
    var ctr = row.metrics.ctr;

    if (qs < CONFIG.MIN_QUALITY_SCORE || ctr < CONFIG.MIN_CTR) {
      Logger.log('PAUSE: "' + row.adGroupCriterion.keyword.text + '"' +
        ' | QS: ' + qs + ' | CTR: ' + (ctr * 100).toFixed(2) + '%' +
        ' | Campaign: ' + row.campaign.name);

      if (!CONFIG.DRY_RUN) {
        var keywords = AdsApp.keywords()
          .withCondition('Text = "' + row.adGroupCriterion.keyword.text + '"')
          .withCondition('AdGroupName = "' + row.adGroup.name + '"')
          .withCondition('CampaignName = "' + row.campaign.name + '"')
          .get();
        if (keywords.hasNext()) keywords.next().pause();
      }
      pauseCount++;
    }
  }

  Logger.log('Total keywords to pause: ' + pauseCount);
  if (CONFIG.DRY_RUN) Logger.log('DRY RUN — no changes applied.');
}
```

### 2. Budget Pacing Monitor

```javascript
function main() {
  var CONFIG = {
    MONTHLY_BUDGET: 10000,
    ALERT_THRESHOLD_OVER: 0.15,
    ALERT_THRESHOLD_UNDER: 0.20,
    ALERT_EMAIL: 'team@example.com',
    CAMPAIGN_LABEL: 'Budget-Monitor'
  };

  var today = new Date();
  var daysInMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();
  var dayOfMonth = today.getDate();
  var expectedSpend = (CONFIG.MONTHLY_BUDGET / daysInMonth) * dayOfMonth;

  var firstOfMonth = Utilities.formatDate(
    new Date(today.getFullYear(), today.getMonth(), 1), 'UTC', 'yyyyMMdd');
  var todayStr = Utilities.formatDate(today, 'UTC', 'yyyyMMdd');

  var campaigns = AdsApp.campaigns()
    .withCondition('Status = ENABLED')
    .withCondition('LabelNames CONTAINS_ANY ["' + CONFIG.CAMPAIGN_LABEL + '"]')
    .forDateRange(firstOfMonth, todayStr)
    .get();

  var totalSpend = 0;
  var campaignDetails = [];

  while (campaigns.hasNext()) {
    var campaign = campaigns.next();
    var stats = campaign.getStatsFor(firstOfMonth, todayStr);
    var spend = stats.getCost();
    totalSpend += spend;
    campaignDetails.push({
      name: campaign.getName(),
      spend: spend,
      conversions: stats.getConversions()
    });
  }

  var paceRatio = totalSpend / expectedSpend;
  var projectedSpend = (totalSpend / dayOfMonth) * daysInMonth;
  var status = 'ON PACE';

  if (paceRatio > (1 + CONFIG.ALERT_THRESHOLD_OVER)) status = 'OVERSPENDING';
  else if (paceRatio < (1 - CONFIG.ALERT_THRESHOLD_UNDER)) status = 'UNDERSPENDING';

  Logger.log('Day ' + dayOfMonth + '/' + daysInMonth +
    ' | Expected: $' + expectedSpend.toFixed(2) +
    ' | Actual: $' + totalSpend.toFixed(2) +
    ' | Projected: $' + projectedSpend.toFixed(2) +
    ' | Status: ' + status);

  if (status !== 'ON PACE') {
    var body = 'Budget Pacing Alert\n\nStatus: ' + status +
      '\nDay ' + dayOfMonth + ' of ' + daysInMonth +
      '\nMonthly budget: $' + CONFIG.MONTHLY_BUDGET.toFixed(2) +
      '\nExpected spend: $' + expectedSpend.toFixed(2) +
      '\nActual spend: $' + totalSpend.toFixed(2) +
      '\nProjected: $' + projectedSpend.toFixed(2);

    MailApp.sendEmail(CONFIG.ALERT_EMAIL, '[Google Ads] Budget Alert: ' + status, body);
  }
}
```

### 3. Search Terms Negative Keyword Miner

```javascript
function main() {
  var CONFIG = {
    MIN_COST: 50,
    MAX_CONVERSIONS: 0,
    MIN_CLICKS: 10,
    DATE_RANGE: 'LAST_30_DAYS',
    NEGATIVE_MATCH_TYPE: 'EXACT',
    DRY_RUN: true,
    LOG_SHEET_URL: ''
  };

  var query = "SELECT " +
    "search_term_view.search_term, " +
    "campaign.name, " +
    "ad_group.name, " +
    "metrics.impressions, " +
    "metrics.clicks, " +
    "metrics.cost_micros, " +
    "metrics.conversions " +
    "FROM search_term_view " +
    "WHERE campaign.status = 'ENABLED' " +
    "AND metrics.cost_micros > " + (CONFIG.MIN_COST * 1000000) + " " +
    "AND metrics.clicks > " + CONFIG.MIN_CLICKS + " " +
    "AND metrics.conversions <= " + CONFIG.MAX_CONVERSIONS + " " +
    "AND segments.date DURING " + CONFIG.DATE_RANGE;

  var results = AdsApp.search(query);
  var negatives = [];

  while (results.hasNext()) {
    var row = results.next();
    var term = row.searchTermView.searchTerm;
    var cost = row.metrics.costMicros / 1000000;

    negatives.push({ term: term, campaign: row.campaign.name, cost: cost });

    Logger.log('NEGATIVE: "' + term + '" | Cost: $' + cost.toFixed(2) +
      ' | Clicks: ' + row.metrics.clicks + ' | Campaign: ' + row.campaign.name);

    if (!CONFIG.DRY_RUN) {
      var campaigns = AdsApp.campaigns()
        .withCondition('Name = "' + row.campaign.name + '"').get();
      if (campaigns.hasNext()) {
        var campaign = campaigns.next();
        if (CONFIG.NEGATIVE_MATCH_TYPE === 'EXACT') {
          campaign.createNegativeKeyword('[' + term + ']');
        } else if (CONFIG.NEGATIVE_MATCH_TYPE === 'PHRASE') {
          campaign.createNegativeKeyword('"' + term + '"');
        } else {
          campaign.createNegativeKeyword(term);
        }
      }
    }
  }

  Logger.log('Total negative keyword candidates: ' + negatives.length);
}
```

### 4. Broken URL Checker

```javascript
function main() {
  var CONFIG = {
    ALERT_EMAIL: 'team@example.com',
    PAUSE_BROKEN: false,
    MIN_IMPRESSIONS: 10,
    DATE_RANGE: 'LAST_7_DAYS'
  };

  var brokenUrls = [];

  var ads = AdsApp.ads()
    .withCondition('Status = ENABLED')
    .withCondition('CampaignStatus = ENABLED')
    .withCondition('AdGroupStatus = ENABLED')
    .forDateRange(CONFIG.DATE_RANGE)
    .withCondition('Impressions > ' + CONFIG.MIN_IMPRESSIONS)
    .get();

  while (ads.hasNext()) {
    var ad = ads.next();
    var url = ad.urls().getFinalUrl();
    if (url) {
      var status = checkUrl(url);
      if (status !== 200) {
        brokenUrls.push({
          campaign: ad.getCampaign().getName(),
          adGroup: ad.getAdGroup().getName(),
          url: url,
          httpStatus: status
        });
        Logger.log('BROKEN [' + status + ']: ' + url);
        if (CONFIG.PAUSE_BROKEN) ad.pause();
      }
    }
  }

  if (brokenUrls.length > 0 && CONFIG.ALERT_EMAIL) {
    var body = 'Broken URL Report\n\n';
    for (var i = 0; i < brokenUrls.length; i++) {
      body += 'HTTP ' + brokenUrls[i].httpStatus + ' | ' +
        brokenUrls[i].campaign + ' | ' + brokenUrls[i].url + '\n';
    }
    MailApp.sendEmail(CONFIG.ALERT_EMAIL,
      '[Google Ads] ' + brokenUrls.length + ' Broken URLs', body);
  }
}

function checkUrl(url) {
  try {
    var response = UrlFetchApp.fetch(url, {
      muteHttpExceptions: true,
      followRedirects: true,
      validateHttpsCertificates: false
    });
    return response.getResponseCode();
  } catch (e) {
    return 0;
  }
}
```

### 5. Bid Adjustments by Time of Day (Dayparting)

```javascript
function main() {
  var CONFIG = {
    DATE_RANGE: 'LAST_30_DAYS',
    MAX_BID_MODIFIER: 0.30,
    MIN_BID_MODIFIER: -0.50,
    MIN_CONVERSIONS: 5
  };

  var query = "SELECT " +
    "campaign.name, " +
    "segments.hour, " +
    "metrics.impressions, " +
    "metrics.clicks, " +
    "metrics.conversions, " +
    "metrics.cost_micros " +
    "FROM campaign " +
    "WHERE campaign.status = 'ENABLED' " +
    "AND segments.date DURING " + CONFIG.DATE_RANGE;

  var results = AdsApp.search(query);
  var hourlyData = {};

  while (results.hasNext()) {
    var row = results.next();
    var name = row.campaign.name;
    var hour = row.segments.hour;

    if (!hourlyData[name]) hourlyData[name] = {};
    if (!hourlyData[name][hour]) {
      hourlyData[name][hour] = { clicks: 0, conversions: 0, cost: 0 };
    }
    hourlyData[name][hour].clicks += row.metrics.clicks;
    hourlyData[name][hour].conversions += row.metrics.conversions;
    hourlyData[name][hour].cost += row.metrics.costMicros / 1000000;
  }

  for (var campaignName in hourlyData) {
    var hours = hourlyData[campaignName];
    var totalConv = 0, totalClicks = 0;
    for (var h in hours) {
      totalConv += hours[h].conversions;
      totalClicks += hours[h].clicks;
    }
    var avgCvr = totalClicks > 0 ? totalConv / totalClicks : 0;

    Logger.log('\n' + campaignName + ' | Avg CVR: ' + (avgCvr * 100).toFixed(2) + '%');

    for (var hour = 0; hour < 24; hour++) {
      var data = hours[hour] || { clicks: 0, conversions: 0 };
      var hourCvr = data.clicks > 0 ? data.conversions / data.clicks : 0;
      var modifier = 0;

      if (avgCvr > 0 && data.conversions >= CONFIG.MIN_CONVERSIONS) {
        modifier = (hourCvr / avgCvr) - 1;
        modifier = Math.max(CONFIG.MIN_BID_MODIFIER, Math.min(CONFIG.MAX_BID_MODIFIER, modifier));
      }

      Logger.log('  Hour ' + hour + ' | Conv: ' + data.conversions +
        ' | Modifier: ' + (modifier > 0 ? '+' : '') + (modifier * 100).toFixed(0) + '%');
    }
  }
}
```

### 6. Quality Score Tracker

Log quality score history to Google Sheets (Google Ads does not retain QS history natively).

```javascript
function main() {
  var CONFIG = {
    SHEET_URL: 'YOUR_GOOGLE_SHEET_URL',
    SHEET_NAME: 'QS History',
    MIN_IMPRESSIONS: 50
  };

  var sheet = SpreadsheetApp.openByUrl(CONFIG.SHEET_URL)
    .getSheetByName(CONFIG.SHEET_NAME);

  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      'Date', 'Campaign', 'Ad Group', 'Keyword', 'Match Type',
      'Quality Score', 'Expected CTR', 'Ad Relevance', 'Landing Page Exp',
      'Impressions', 'Clicks', 'Cost', 'Conversions'
    ]);
  }

  var today = Utilities.formatDate(new Date(), 'UTC', 'yyyy-MM-dd');

  var query = "SELECT " +
    "campaign.name, ad_group.name, " +
    "ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, " +
    "ad_group_criterion.quality_info.quality_score, " +
    "ad_group_criterion.quality_info.search_predicted_ctr, " +
    "ad_group_criterion.quality_info.creative_quality_score, " +
    "ad_group_criterion.quality_info.post_click_quality_score, " +
    "metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions " +
    "FROM keyword_view " +
    "WHERE campaign.status = 'ENABLED' " +
    "AND ad_group.status = 'ENABLED' " +
    "AND ad_group_criterion.status = 'ENABLED' " +
    "AND metrics.impressions > " + CONFIG.MIN_IMPRESSIONS + " " +
    "AND segments.date DURING LAST_7_DAYS";

  var results = AdsApp.search(query);
  var rows = [];

  while (results.hasNext()) {
    var row = results.next();
    var qi = row.adGroupCriterion.qualityInfo;
    rows.push([
      today, row.campaign.name, row.adGroup.name,
      row.adGroupCriterion.keyword.text, row.adGroupCriterion.keyword.matchType,
      qi.qualityScore || '', qi.searchPredictedCtr || '',
      qi.creativeQualityScore || '', qi.postClickQualityScore || '',
      row.metrics.impressions, row.metrics.clicks,
      (row.metrics.costMicros / 1000000).toFixed(2), row.metrics.conversions
    ]);
  }

  if (rows.length > 0) {
    sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
  }
  Logger.log('Logged ' + rows.length + ' keywords');
}
```

### 7. Ad Copy Testing (RSA Performance)

```javascript
function main() {
  var CONFIG = {
    MIN_IMPRESSIONS: 500,
    DATE_RANGE: 'LAST_30_DAYS',
    WINNER_CTR_LIFT: 0.20,
    LOSER_CTR_DROP: -0.20,
    ALERT_EMAIL: 'team@example.com'
  };

  var query = "SELECT " +
    "campaign.name, ad_group.name, ad_group_ad.ad.id, " +
    "ad_group_ad.ad_strength, " +
    "metrics.impressions, metrics.clicks, metrics.ctr, " +
    "metrics.conversions, metrics.cost_micros " +
    "FROM ad_group_ad " +
    "WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' " +
    "AND ad_group_ad.status = 'ENABLED' " +
    "AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD' " +
    "AND metrics.impressions > " + CONFIG.MIN_IMPRESSIONS + " " +
    "AND segments.date DURING " + CONFIG.DATE_RANGE;

  var results = AdsApp.search(query);
  var adGroups = {};

  while (results.hasNext()) {
    var row = results.next();
    var agKey = row.campaign.name + ' > ' + row.adGroup.name;
    if (!adGroups[agKey]) adGroups[agKey] = [];
    adGroups[agKey].push({
      adId: row.adGroupAd.ad.id,
      strength: row.adGroupAd.adStrength,
      impressions: row.metrics.impressions,
      clicks: row.metrics.clicks,
      ctr: row.metrics.ctr,
      conversions: row.metrics.conversions
    });
  }

  var winners = [], losers = [];

  for (var agKey in adGroups) {
    var ads = adGroups[agKey];
    if (ads.length < 2) continue;

    var totalClicks = 0, totalImpr = 0;
    for (var i = 0; i < ads.length; i++) {
      totalClicks += ads[i].clicks;
      totalImpr += ads[i].impressions;
    }
    var avgCtr = totalImpr > 0 ? totalClicks / totalImpr : 0;

    for (var j = 0; j < ads.length; j++) {
      var ctrLift = avgCtr > 0 ? (ads[j].ctr - avgCtr) / avgCtr : 0;
      if (ctrLift >= CONFIG.WINNER_CTR_LIFT) winners.push({ adGroup: agKey, ad: ads[j], lift: ctrLift });
      else if (ctrLift <= CONFIG.LOSER_CTR_DROP) losers.push({ adGroup: agKey, ad: ads[j], lift: ctrLift });
    }
  }

  Logger.log('Winners: ' + winners.length + ' | Losers: ' + losers.length);
}
```

### 8. Budget Allocation by ROAS

```javascript
function main() {
  var CONFIG = {
    TOTAL_DAILY_BUDGET: 500,
    MIN_BUDGET: 20,
    MAX_BUDGET: 200,
    DATE_RANGE: 'LAST_14_DAYS',
    CAMPAIGN_LABEL: 'Auto-Budget',
    MIN_CONVERSIONS: 3,
    DRY_RUN: true
  };

  var campaigns = AdsApp.campaigns()
    .withCondition('Status = ENABLED')
    .withCondition('LabelNames CONTAINS_ANY ["' + CONFIG.CAMPAIGN_LABEL + '"]')
    .forDateRange(CONFIG.DATE_RANGE)
    .get();

  var campaignData = [];
  while (campaigns.hasNext()) {
    var campaign = campaigns.next();
    var stats = campaign.getStatsFor(CONFIG.DATE_RANGE);
    var cost = stats.getCost();
    var convValue = stats.getConversionValue();

    campaignData.push({
      campaign: campaign,
      name: campaign.getName(),
      cost: cost,
      roas: cost > 0 ? convValue / cost : 0,
      conversions: stats.getConversions(),
      currentBudget: campaign.getBudget().getAmount()
    });
  }

  campaignData.sort(function(a, b) { return b.roas - a.roas; });

  var totalRoas = 0;
  for (var i = 0; i < campaignData.length; i++) {
    if (campaignData[i].conversions >= CONFIG.MIN_CONVERSIONS) totalRoas += campaignData[i].roas;
  }

  for (var j = 0; j < campaignData.length; j++) {
    var c = campaignData[j];
    var newBudget = (c.conversions >= CONFIG.MIN_CONVERSIONS && totalRoas > 0)
      ? (c.roas / totalRoas) * CONFIG.TOTAL_DAILY_BUDGET
      : CONFIG.MIN_BUDGET;

    newBudget = Math.max(CONFIG.MIN_BUDGET, Math.min(CONFIG.MAX_BUDGET, Math.round(newBudget * 100) / 100));

    Logger.log(c.name + ' | ROAS: ' + c.roas.toFixed(2) +
      ' | Current: $' + c.currentBudget.toFixed(2) + ' | New: $' + newBudget.toFixed(2));

    if (!CONFIG.DRY_RUN) c.campaign.getBudget().setAmount(newBudget);
  }

  if (CONFIG.DRY_RUN) Logger.log('DRY RUN — no budgets changed.');
}
```

### 9. Anomaly Detection

```javascript
function main() {
  var CONFIG = {
    LOOKBACK_DAYS: 14,
    SPIKE_THRESHOLD: 2.0,
    DROP_THRESHOLD: 0.5,
    ALERT_EMAIL: 'team@example.com',
    METRICS: ['impressions', 'clicks', 'cost_micros', 'conversions']
  };

  var today = new Date();
  var yesterday = new Date(today.getTime() - 86400000);
  var lookbackStart = new Date(today.getTime() - (CONFIG.LOOKBACK_DAYS + 1) * 86400000);

  var yesterdayStr = Utilities.formatDate(yesterday, 'UTC', 'yyyyMMdd');
  var lookbackStr = Utilities.formatDate(lookbackStart, 'UTC', 'yyyyMMdd');

  var query = "SELECT campaign.name, " +
    "metrics.impressions, metrics.clicks, metrics.cost_micros, " +
    "metrics.conversions, segments.date " +
    "FROM campaign WHERE campaign.status = 'ENABLED' " +
    "AND segments.date BETWEEN '" +
      lookbackStr.substring(0, 4) + '-' + lookbackStr.substring(4, 6) + '-' + lookbackStr.substring(6, 8) +
    "' AND '" +
      yesterdayStr.substring(0, 4) + '-' + yesterdayStr.substring(4, 6) + '-' + yesterdayStr.substring(6, 8) + "'";

  var results = AdsApp.search(query);
  var campaignDays = {};

  while (results.hasNext()) {
    var row = results.next();
    var name = row.campaign.name;
    var date = row.segments.date;
    if (!campaignDays[name]) campaignDays[name] = {};
    campaignDays[name][date] = {
      impressions: row.metrics.impressions,
      clicks: row.metrics.clicks,
      cost_micros: row.metrics.costMicros,
      conversions: row.metrics.conversions
    };
  }

  var alerts = [];
  var yesterdayDate = Utilities.formatDate(yesterday, 'UTC', 'yyyy-MM-dd');

  for (var campaignName in campaignDays) {
    var days = campaignDays[campaignName];
    var yesterdayData = days[yesterdayDate];
    if (!yesterdayData) continue;

    for (var m = 0; m < CONFIG.METRICS.length; m++) {
      var metric = CONFIG.METRICS[m];
      var sum = 0, count = 0;
      for (var d in days) {
        if (d !== yesterdayDate) { sum += days[d][metric] || 0; count++; }
      }
      if (count === 0) continue;
      var avg = sum / count;
      var current = yesterdayData[metric] || 0;

      if (avg > 0) {
        var ratio = current / avg;
        if (ratio >= CONFIG.SPIKE_THRESHOLD || ratio <= CONFIG.DROP_THRESHOLD) {
          alerts.push({
            campaign: campaignName, metric: metric,
            type: ratio >= CONFIG.SPIKE_THRESHOLD ? 'SPIKE' : 'DROP',
            current: current, average: avg, ratio: ratio
          });
        }
      }
    }
  }

  if (alerts.length > 0) {
    var body = 'Anomaly Report — ' + yesterdayDate + '\n\n';
    for (var a = 0; a < alerts.length; a++) {
      body += alerts[a].type + ': ' + alerts[a].campaign +
        ' | ' + alerts[a].metric + ' | ' + alerts[a].ratio.toFixed(2) + 'x avg\n';
    }
    MailApp.sendEmail(CONFIG.ALERT_EMAIL, '[Google Ads] ' + alerts.length + ' Anomalies', body);
  }
}
```

### 10. Landing Page Performance

```javascript
function main() {
  var CONFIG = {
    DATE_RANGE: 'LAST_30_DAYS',
    MIN_CLICKS: 50,
    SHEET_URL: 'YOUR_GOOGLE_SHEET_URL',
    SHEET_NAME: 'Landing Pages'
  };

  var query = "SELECT " +
    "landing_page_view.unexpanded_final_url, " +
    "metrics.clicks, metrics.impressions, " +
    "metrics.cost_micros, metrics.conversions, " +
    "metrics.conversions_value " +
    "FROM landing_page_view " +
    "WHERE segments.date DURING " + CONFIG.DATE_RANGE + " " +
    "AND metrics.clicks > " + CONFIG.MIN_CLICKS + " " +
    "ORDER BY metrics.clicks DESC";

  var results = AdsApp.search(query);
  var pages = [];

  while (results.hasNext()) {
    var row = results.next();
    var cost = row.metrics.costMicros / 1000000;
    var cvr = row.metrics.clicks > 0 ? row.metrics.conversions / row.metrics.clicks : 0;
    var roas = cost > 0 ? row.metrics.conversionsValue / cost : 0;

    pages.push([
      row.landingPageView.unexpandedFinalUrl,
      row.metrics.clicks, row.metrics.impressions,
      cost.toFixed(2), row.metrics.conversions,
      row.metrics.conversionsValue.toFixed(2),
      (cvr * 100).toFixed(2) + '%', roas.toFixed(2)
    ]);
  }

  if (CONFIG.SHEET_URL && pages.length > 0) {
    var sheet = SpreadsheetApp.openByUrl(CONFIG.SHEET_URL)
      .getSheetByName(CONFIG.SHEET_NAME);
    sheet.clear();
    sheet.appendRow(['URL', 'Clicks', 'Impressions', 'Cost', 'Conversions',
      'Conv Value', 'CVR', 'ROAS']);
    sheet.getRange(2, 1, pages.length, pages[0].length).setValues(pages);
    Logger.log('Exported ' + pages.length + ' landing pages');
  }
}
```

## Google Sheets Integration

### Opening a Spreadsheet

```javascript
var ss = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/d/SHEET_ID/edit');
var ss = SpreadsheetApp.openById('SHEET_ID');
var sheet = ss.getSheetByName('Data');
```

### Reading Data

```javascript
var values = sheet.getRange('A1:D10').getValues();  // 2D array
var allData = sheet.getDataRange().getValues();
var value = sheet.getRange('B2').getValue();         // Single cell
```

### Writing Data

```javascript
sheet.getRange('A1').setValue('Campaign Name');
sheet.appendRow(['2025-02-11', 'Brand', 150, 12]);

// Batch write (much faster than appendRow in a loop)
var data = [['Campaign', 'Clicks'], ['Brand', 150], ['Generic', 300]];
sheet.getRange(1, 1, data.length, data[0].length).setValues(data);
```

## Email and Notifications

```javascript
// Simple email
MailApp.sendEmail('team@example.com', 'Subject', 'Body text');

// HTML email
MailApp.sendEmail({
  to: 'team@example.com',
  subject: '[Google Ads] Weekly Report',
  htmlBody: '<h1>Report</h1><p>Details here.</p>'
});
```

## Scheduling

Set up in **Tools & Settings > Bulk Actions > Scripts**. Available frequencies: Hourly, Daily, Weekly, Monthly.

**Recommended schedules:**
- Budget pacing: Daily or hourly
- Negative keyword mining: Weekly
- Quality score tracking: Daily
- Anomaly detection: Daily (morning)
- Broken URL checks: Weekly
- Dashboards: Daily

## Error Handling

```javascript
function main() {
  try {
    processKeywords();
  } catch (e) {
    Logger.log('ERROR: ' + e.message + '\nStack: ' + e.stack);
    MailApp.sendEmail('team@example.com',
      '[Google Ads Script] Error', 'Error: ' + e.message);
  }
}
```

**Execution time limits:** 30 minutes (single account), 60 minutes (MCC). Handle gracefully:

```javascript
var startTime = new Date().getTime();
var MAX_RUNTIME = 25 * 60 * 1000;  // 25 min buffer

while (iterator.hasNext()) {
  if (new Date().getTime() - startTime > MAX_RUNTIME) {
    Logger.log('Approaching time limit. Stopping.');
    break;
  }
  // Process...
}
```

## MCC Scripts

### Basic MCC Script

```javascript
function main() {
  var accounts = AdsManagerApp.accounts()
    .withCondition('Impressions > 0')
    .forDateRange('LAST_7_DAYS')
    .withLimit(50)
    .get();

  while (accounts.hasNext()) {
    var account = accounts.next();
    AdsManagerApp.select(account);
    Logger.log('Processing: ' + account.getName());
    // Now AdsApp refers to this account
  }
}
```

### Parallel Processing with executeInParallel()

```javascript
function main() {
  var accounts = AdsManagerApp.accounts()
    .withCondition('Impressions > 0')
    .forDateRange('LAST_7_DAYS')
    .get();

  accounts.executeInParallel('processAccount', 'aggregateResults');
}

function processAccount() {
  var account = AdsApp.currentAccount();
  var result = { name: account.getName(), id: account.getCustomerId(), campaigns: [] };

  var campaigns = AdsApp.campaigns()
    .withCondition('Status = ENABLED')
    .forDateRange('LAST_7_DAYS').get();

  while (campaigns.hasNext()) {
    var c = campaigns.next();
    var s = c.getStatsFor('LAST_7_DAYS');
    result.campaigns.push({
      name: c.getName(), clicks: s.getClicks(),
      cost: s.getCost(), conversions: s.getConversions()
    });
  }

  return JSON.stringify(result);  // Must return string
}

function aggregateResults(results) {
  for (var i = 0; i < results.length; i++) {
    if (results[i].getStatus() === 'OK') {
      var data = JSON.parse(results[i].getReturnValue());
      Logger.log(data.name + ': ' + data.campaigns.length + ' campaigns');
    } else {
      Logger.log('Error: ' + results[i].getError());
    }
  }
}
```

**executeInParallel() rules:**
- Per-account function must return a string (`JSON.stringify()`)
- Callback receives array of `ExecutionResult` objects (`.getStatus()`, `.getReturnValue()`, `.getError()`, `.getCustomerId()`)
- Max 50 accounts per call
- Each account execution has 30-minute limit

## Best Practices

1. **Preview mode first** — always click Preview before Run
2. **Log before modifying** — `Logger.log('Pausing: ' + keyword.getText())` before `keyword.pause()`
3. **DRY_RUN flag** — every modifying script should have `DRY_RUN: true` in config
4. **Incremental rollout** — start with one campaign, expand after validation
5. **Error notifications** — send emails on failure, do not rely on checking logs
6. **Use labels** — target scripts via labels instead of hardcoded campaign names
7. **Batch Sheets writes** — use `setValues()` with 2D arrays, not `appendRow()` in loops
8. **Document scripts** — add a comment block with purpose, schedule, author, config explanation

## Limitations

| Limitation | Details |
|-----------|---------|
| Execution time | 30 min (single), 60 min (MCC) |
| No async/await | Synchronous execution only |
| Limited ES6 | No `import`/`export`, no `class` |
| No Display/Video APIs | Limited support via scripts |
| No Performance Max | Read-only (limited reporting) |
| URL fetch | 50 MB response limit, 60s timeout |
| MailApp | 100 recipients/day |
| No npm/modules | Cannot import external libraries |
| executeInParallel() | Max 50 accounts per call |

## Resources

- **Google Ads Scripts Docs:** https://developers.google.com/google-ads/scripts/docs/overview
- **AdsApp Reference:** https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp
- **GAQL Reference:** https://developers.google.com/google-ads/api/docs/query/overview
- **Script Examples:** https://developers.google.com/google-ads/scripts/docs/solutions
- **Full Cogny Docs:** https://cogny.com/docs/google-ads-scripts
