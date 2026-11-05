#!/usr/bin/env python3
"""Fail-closed scope gate for pull requests targeting main.

Until full architecture and interaction release gates exist, all changes to
production application assets are blocked. QA-only PRs are allowed through
this scope gate, but require human review of governance changes.
"""
import os
import pathlib
import subprocess
import sys

ALLOWED_QA_PREFIXES = ("quality/", "tests/", ".github/workflows/")
ALLOWED_QA_FILES = ("README.md", ".gitignore")

def classify(paths):
    """Return blocked production paths; fail closed on unknown files."""
    return [p for p in paths if not (
        p.startswith(ALLOWED_QA_PREFIXES) or p in ALLOWED_QA_FILES
    )]

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def main():
    base = os.environ.get("GITHUB_BASE_REF", "main")
    if base != "main":
        sys.exit(f"BLOCKED: unexpected target branch: {base}")
    try:
        git("fetch", "--no-tags", "--depth=1", "origin", base)
        paths = git("diff", "--name-only", f"origin/{base}", "HEAD").splitlines()
    except (subprocess.CalledProcessError, OSError) as exc:
        sys.exit(f"BLOCKED: Cannot determine changed-file inventory: {exc}")
    print("Changed paths:", paths)
    blocked = classify(paths)
    if blocked:
        sys.exit("BLOCKED: application changes lack certified architecture/browser/regression release gates: " + ", ".join(blocked))
    if any(p.startswith(ALLOWED_QA_PREFIXES) for p in paths):
        print("NOTICE: QA governance changes require independent owner review; not enforced by this script.")
    print("PASS: no production files changed; NOT a production release certification.")

if __name__ == "__main__":
    main()
