#!/usr/bin/env python3
"""Non-release baseline smoke test; intentionally not a full architecture gate."""
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
html = root / "index.html"
if not html.exists():
    sys.exit("FAIL: index.html missing")
src = html.read_text(encoding="utf-8")
if "<html" not in src.lower() or "<script" not in src.lower():
    sys.exit("FAIL: index.html lacks HTML/script structure")
print("PASS: baseline HTML structure present")
print("NOT CERTIFIED: ADR-007, legacy code separation, browser behavior, regressions")
