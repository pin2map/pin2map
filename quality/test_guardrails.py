#!/usr/bin/env python3
"""Mutation tests: deliberately violating ADR-008 must fail."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
config = json.loads((ROOT / "quality/guardrails.json").read_text())
patterns = config["architecture"]["adr008"]["domain_forbidden_patterns"]
cases = [
    "document.getElementById('routeInfo')",
    "window.document.querySelector('#routeInfo')",
    "L.polyline(points)",
    "L.marker([1,2])",
]
for case in cases:
    assert any(re.search(p, case) for p in patterns), f"Guardrail failed to detect: {case}"
assert not any(re.search(p, "function distance(a,b){return a+b;}") for p in patterns)
print("PASS: four deliberate ADR-008 violations detected; pure sample accepted")
