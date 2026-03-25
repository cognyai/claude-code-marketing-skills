#!/bin/bash
# Install Claude Code Marketing Skills
# Detects your AI tool and copies skills to the right location.

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

echo "=== Claude Code Marketing Skills Installer ==="
echo ""

# Detect AI tool
INSTALLED=""

if [ -d "$HOME/.claude" ] || command -v claude &>/dev/null; then
  INSTALLED="claude-code"
fi

if [ -d ".cursor" ] || [ -d "$HOME/.cursor" ]; then
  INSTALLED="${INSTALLED:+$INSTALLED }cursor"
fi

if [ -d ".windsurf" ] || [ -d "$HOME/.windsurf" ]; then
  INSTALLED="${INSTALLED:+$INSTALLED }windsurf"
fi

if [ -f ".aider.conf.yml" ] || command -v aider &>/dev/null; then
  INSTALLED="${INSTALLED:+$INSTALLED }aider"
fi

if [ -z "$INSTALLED" ]; then
  echo "No supported AI tool detected."
  echo "Supported: Claude Code, Cursor, Windsurf, Aider"
  echo ""
  echo "Manual install: cp -r skills/* .claude/skills/"
  exit 1
fi

echo "Detected: $INSTALLED"
echo ""

# Install for Claude Code
if echo "$INSTALLED" | grep -q "claude-code"; then
  TARGET="$PWD/.claude/skills"
  mkdir -p "$TARGET"

  for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$TARGET/$skill_name"
    cp "$skill_dir"SKILL.md "$TARGET/$skill_name/SKILL.md" 2>/dev/null || true
    # Copy any reference files
    for ref in "$skill_dir"references/ "$skill_dir"evals/; do
      [ -d "$ref" ] && cp -r "$ref" "$TARGET/$skill_name/" 2>/dev/null || true
    done
  done

  echo "Installed $(ls -d "$SKILLS_DIR"/*/ | wc -l | tr -d ' ') skills to .claude/skills/"
  echo ""
  echo "Try it: /seo-audit cogny.com"
fi

# Install for Cursor
if echo "$INSTALLED" | grep -q "cursor"; then
  TARGET="$PWD/.cursor/rules"
  mkdir -p "$TARGET"

  for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    # Convert SKILL.md to .mdc format for Cursor
    if [ -f "$skill_dir/SKILL.md" ]; then
      cp "$skill_dir/SKILL.md" "$TARGET/${skill_name}.mdc"
    fi
  done

  echo "Installed skills to .cursor/rules/"
fi

# Install for Windsurf
if echo "$INSTALLED" | grep -q "windsurf"; then
  TARGET="$PWD/.windsurfrules"
  echo "" >> "$TARGET"
  echo "# === Marketing Skills ===" >> "$TARGET"

  for skill_dir in "$SKILLS_DIR"/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
      echo "" >> "$TARGET"
      cat "$skill_dir/SKILL.md" >> "$TARGET"
    fi
  done

  echo "Appended skills to .windsurfrules"
fi

# Install for Aider
if echo "$INSTALLED" | grep -q "aider"; then
  TARGET="$PWD/CONVENTIONS.md"
  echo "" >> "$TARGET"
  echo "# === Marketing Skills ===" >> "$TARGET"

  for skill_dir in "$SKILLS_DIR"/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
      echo "" >> "$TARGET"
      cat "$skill_dir/SKILL.md" >> "$TARGET"
    fi
  done

  echo "Appended skills to CONVENTIONS.md"
fi

echo ""
echo "Done! Skills installed for: $INSTALLED"
echo ""
echo "Free skills ready to use:"
echo "  /seo-audit         — Audit any website's SEO"
echo "  /landing-page-review — CRO analysis"
echo "  /competitor-analysis — Research competitors"
echo ""
echo "Premium skills (requires cogny.com/agent):"
echo "  /google-ads-audit  — Deep Google Ads analysis"
echo "  /meta-ads-audit    — Meta Ads audit"
echo "  /seo-monitor       — Search Console monitoring"
echo "  /cogny             — Full autonomous marketing agent"
