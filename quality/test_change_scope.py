#!/usr/bin/env python3
"""Self-test of the production-change classification used by the PR gate."""
from pathlib import Path
src = Path(__file__).with_name("check_change_scope.py").read_text()
assert 'p == "index.html"' in src
assert 'p.endswith(".html")' in src
assert 'sys.exit("BLOCKED:' in src
print("PASS: change-scope gate present (structural smoke only)")
