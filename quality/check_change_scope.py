#!/usr/bin/env python3
"""Fail-closed change-scope gate. NOT a substitute for browser or ADR audit.

On a PR targeting main, changes to the shipped application are blocked until
a separately implemented browser/architecture release gate exists.
"""
import os, subprocess, sys

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

base = os.environ.get("GITHUB_BASE_REF", "main")
try:
    git("fetch", "--no-tags", "--depth=1", "origin", base)
    changed = git("diff", "--name-only", f"origin/{base}...HEAD").splitlines()
except (subprocess.CalledProcessError, OSError) as exc:
    sys.exit(f"BLOCKED: Cannot establish changed-file inventory: {exc}")

print("Changed files:", ", ".join(changed) if changed else "(none)")
production = [p for p in changed if p == "index.html" or p.endswith(".html") and not p.startswith("tests/")]
if production:
    sys.exit("BLOCKED: Application changes require real browser regression, ADR-007/008 verification and human approval. No such release gate exists yet. Changed: " + ", ".join(production))
print("PASS: no production HTML changes in this PR")
print("LIMITATION: Governance files are not independently protected by this script.")
