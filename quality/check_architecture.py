#!/usr/bin/env python3
"""Enforce ADR-008 on explicitly registered pure domain modules.

Fail closed: missing registered modules fail. This check does NOT certify the legacy
monolithic index.html. New domain modules must be added to domain_modules.json.
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
config = json.loads((ROOT / "quality/guardrails.json").read_text())
modules = json.loads((ROOT / "quality/domain_modules.json").read_text())["modules"]
errors = []
for rel in modules:
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"MISSING: {rel}")
        continue
    src = p.read_text(encoding="utf-8")
    for pattern in config["architecture"]["adr008"]["domain_forbidden_patterns"]:
        if re.search(pattern, src):
            errors.append(f"ADR-008: {rel}: forbidden pattern {pattern}")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"PASS: ADR-008 domain scan of {len(modules)} registered modules")
if not modules:
    print("NOTICE: No domain modules registered; this is NOT a full architecture audit.")
