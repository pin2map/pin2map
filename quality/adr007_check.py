#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = root / 'quality' / 'adr007_components.json'
items = json.loads(manifest.read_text(encoding='utf-8'))
source = (root / 'index.html').read_text(encoding='utf-8')
assert isinstance(items, list)
for item in items:
    assert item.get('component') and item.get('legacy_tokens') and item.get('regression_tests'), 'Incomplete replacement inventory'
    for token in item['legacy_tokens']:
        assert token not in source, 'Legacy component token remains: ' + token
print('ADR-007 inventory entries inspected:', len(items))
if not items:
    print('NOT CERTIFIED: no replacement inventories registered')
