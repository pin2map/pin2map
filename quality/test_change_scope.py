#!/usr/bin/env python3
"""Executable mutation tests for fail-closed change classification."""
from check_change_scope import classify

cases = [
    (["index.html"], ["index.html"]),
    (["app.js"], ["app.js"]),
    (["assets/app.css"], ["assets/app.css"]),
    (["unknown.bin"], ["unknown.bin"]),
    (["quality/check_architecture.py"], []),
    (["tests/test_route.py"], []),
    ([".github/workflows/quality.yml"], []),
    (["quality/test.py", "index.html"], ["index.html"]),
    (["README.md"], []),
]
for changed, expected in cases:
    actual = classify(changed)
    assert actual == expected, f"{changed}: expected {expected}, got {actual}"
print(f"PASS: {len(cases)} change-scope mutation cases")
