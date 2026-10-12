#!/usr/bin/env python3
"""Check every Cogny tool reference in skills/ against docs/mcp-catalog.json.

  python3 scripts/check-tool-names.py            # all skills
  python3 scripts/check-tool-names.py skills/x   # one skill

Flags:
  LEGACY   old-style names (mcp__cogny__google_ads__...) that the gateway no longer serves
  UNKNOWN  a prefix or tool that isn't in the catalog
Lines containing "check-tool-names: ignore" are skipped.
Exit code 1 when anything is flagged.
"""
import fnmatch
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
catalog = json.load(open(os.path.join(ROOT, "docs", "mcp-catalog.json")))
core = {t for group in catalog["core"].values() for t in group}
servers = {p: {t["name"] for t in s["tools"]} for p, s in catalog["servers"].items()}

REF = re.compile(r"mcp__cogny__([A-Za-z0-9_*-]+?)(?=[`'\")\s,;:]|$)", re.M)


def check(token):
    if token.startswith("mcp__"):
        rest = token[len("mcp__"):]
        prefix, sep, tool = rest.partition("__")
        if not sep:
            return "UNKNOWN", f"no tool after prefix '{prefix}'"
        if prefix not in servers:
            return "UNKNOWN", f"prefix '{prefix}' not in catalog"
        if "*" in tool:
            return (None, None) if fnmatch.filter(servers[prefix], tool) else ("UNKNOWN", f"wildcard matches nothing in {prefix}")
        return (None, None) if tool in servers[prefix] else ("UNKNOWN", f"{prefix} has no tool '{tool}'")
    if token in core or token == "*":
        return None, None
    if "__" in token:
        return "LEGACY", "old namespace; use mcp__cogny__mcp__<Prefix>__<tool>"
    return "UNKNOWN", "not a core Cogny tool"


def main():
    targets = sys.argv[1:] or [os.path.join(ROOT, "skills")]
    files = []
    for t in targets:
        if os.path.isfile(t):
            files.append(t)
        for dp, _, fs in os.walk(t):
            files += [os.path.join(dp, f) for f in fs if f.endswith(".md")]
    problems = 0
    for f in sorted(set(files)):
        for i, line in enumerate(open(f), 1):
            if "check-tool-names: ignore" in line:
                continue
            for m in REF.finditer(line):
                kind, why = check(m.group(1))
                if kind:
                    problems += 1
                    print(f"{os.path.relpath(f, ROOT)}:{i}: {kind} mcp__cogny__{m.group(1)} ({why})")
    print(f"{problems} problem(s) in {len(set(files))} file(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
