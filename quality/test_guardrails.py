#!/usr/bin/env python3
"""Mutation tests: ADR-008 domain modules must reject browser and adapter APIs."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
config = json.loads((ROOT / "quality/guardrails.json").read_text())
patterns = config["architecture"]["adr008"]["domain_forbidden_patterns"]
cases = [
    "document.getElementById('routeInfo')",
    "window.document.querySelector('#routeInfo')",
    "L.polyline(points)",
    "L.marker([1,2])",
    "L.latLng(48,9)",
    "fetch('https://router.project-osrm.org')",
    "const x = window.location.href",
    "const x = globalThis.location",
    "localStorage.getItem('project')",
    "sessionStorage.setItem('x', 'y')",
    "new FileReader()",
    "new XMLHttpRequest()",
    "new WebSocket('ws://example.test')",
    "navigator.geolocation.getCurrentPosition(cb)",
    "new MutationObserver(cb)",
    "new ResizeObserver(cb)",
    "requestAnimationFrame(render)",
    "alert('error')",
    "location.reload()",
]
for case in cases:
    assert any(re.search(p, case) for p in patterns), f"Guardrail failed to detect: {case}"
pure_cases = [
    "function distance(a,b){return a+b;}",
    "function routeDuration(seconds){return Math.round(seconds / 60);}",
    "const result = points.map(p => ({lat:p.lat,lng:p.lng}));",
]
for case in pure_cases:
    assert not any(re.search(p, case) for p in patterns), f"False positive: {case}"
print(f"PASS: {len(cases)} deliberate ADR-008 violations detected; {len(pure_cases)} pure samples accepted")
