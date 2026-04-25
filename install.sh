#!/bin/bash
# Install Claude Code Marketing Skills
# Detects your AI tool and copies skills to the right location.
# Works both via `curl | bash` and when run from a local clone.

set -e

echo "=== Claude Code Marketing Skills Installer ==="
echo ""

# If run via curl|bash, $0 is stdin — clone the repo to a temp dir
if [ ! -f "$0" ] || [ "$(basename "$0")" = "bash" ] || [ "$0" = "/dev/stdin" ]; then
  TMPDIR=$(mktemp -d)
  echo "Downloading skills..."
  git clone --depth 1 https://github.com/cognyai/claude-code-marketing-skills.git "$TMPDIR" 2>/dev/null
  SKILLS_DIR="$TMPDIR/skills"
  CLEANUP="$TMPDIR"
else
  REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
  SKILLS_DIR="$REPO_DIR/skills"
  CLEANUP=""
fi

# Detect AI tool
INSTALLED=""

if [ -d "$HOME/.claude" ] || command -v claude &>/dev/null; then
  INSTALLED="claude-code"
fi

if [ -d ".cursor" ] || [ -d "$HOME/.cursor" ]; then
  INSTALLED="${INSTALLED:+$INSTALLED }cursor"
fi

if [ -z "$INSTALLED" ]; then
  echo "No supported AI tool detected."
  echo "Supported: Claude Code, Cursor"
  echo ""
  echo "Manual install: cp -r skills/* .claude/skills/"
  [ -n "$CLEANUP" ] && rm -rf "$CLEANUP"
  exit 1
fi

echo "Detected: $INSTALLED"
echo ""

# Install for Claude Code
if echo "$INSTALLED" | grep -q "claude-code"; then
  TARGET="$PWD/.claude/skills"
  mkdir -p "$TARGET"
  COUNT=0

  for skill_dir in "$SKILLS_DIR"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    mkdir -p "$TARGET/$skill_name"
    cp "$skill_dir"SKILL.md "$TARGET/$skill_name/SKILL.md" 2>/dev/null || true
    # Copy any reference files. Use `cp -R src/. dst/` so the directory is
    # preserved (BSD cp on macOS flattens trailing-slash sources otherwise).
    for ref in references evals; do
      src="$skill_dir$ref"
      if [ -d "$src" ]; then
        mkdir -p "$TARGET/$skill_name/$ref"
        cp -R "$src/." "$TARGET/$skill_name/$ref/"
      fi
    done
    COUNT=$((COUNT + 1))
  done

  echo "Installed $COUNT skills to .claude/skills/"
  echo ""
  echo "Try it: /seo-audit cogny.com"
fi

# Install for Cursor
if echo "$INSTALLED" | grep -q "cursor"; then
  TARGET="$PWD/.cursor/rules"
  mkdir -p "$TARGET"

  for skill_dir in "$SKILLS_DIR"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
      cp "$skill_dir/SKILL.md" "$TARGET/${skill_name}.mdc"
    fi
  done

  echo "Installed skills to .cursor/rules/"
fi

# Cleanup temp dir if we cloned
[ -n "$CLEANUP" ] && rm -rf "$CLEANUP"

echo ""
echo "Done! Skills installed for: $INSTALLED"
echo ""
echo "Free skills ready to use:"
echo "  /seo-audit            — Audit any website's SEO"
echo "  /non-commodity-content — Interview-driven SEO briefs built on your real stories"
echo "  /landing-page-review  — CRO analysis"
echo "  /competitor-analysis  — Research competitors"
echo "  /ad-copy-writer       — Generate Google/Meta/LinkedIn ad copy"
echo "  /lead-qualification   — Research and qualify B2B leads"
echo "  /website-migration-audit — Production vs staging SEO migration QA"
echo "  /welcome-series       — 5-email welcome series from a brand URL"
echo "  /deliverability-check — SPF / DKIM / DMARC audit on a domain"
echo ""
echo "Premium skills (requires cogny.com):"
echo "  /linkedin-ads-audit       — LinkedIn Ads audit"
echo "  /seo-monitor              — Search Console monitoring"
echo "  /crm-icp-analysis         — Build ICP from HubSpot CRM data"
echo "  /crm-sales-momentum       — Pipeline velocity & stall detection"
echo "  /linkedin-micro-campaigns — Create targeted LinkedIn campaigns from ICP"
echo "  /subject-line-lab         — Mine your subject-line history, generate tuned candidates"
echo "  /winback-engine           — Tiered winback for dormant subscribers"
echo "  /pre-send-qa              — Pre-flight QA before you hit send"
echo "  /email-report             — Auto-write weekly/monthly stakeholder report"
echo "  /revenue-audit            — Find email revenue leaks, ranked by \$ impact"
echo "  /cogny                    — Full autonomous marketing agent"
