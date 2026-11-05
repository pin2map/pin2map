#!/usr/bin/env python3
from pathlib import Path
import subprocess
import json
import tempfile

source = Path(__file__).resolve().parent / 'adr007_check.py'
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / 'quality').mkdir()
    (root / 'quality' / 'adr007_check.py').write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
    app = root / 'index.html'
    inventory = root / 'quality' / 'adr007_components.json'
    app.write_text('new UI only', encoding='utf-8')
    inventory.write_text(json.dumps([{'component':'routing','legacy_tokens':['oldRoutingView'],'regression_tests':['routing-test']}]), encoding='utf-8')
    cmd = ['python', str(root / 'quality' / 'adr007_check.py')]
    assert subprocess.run(cmd, capture_output=True).returncode == 0
    app.write_text('new UI and oldRoutingView', encoding='utf-8')
    assert subprocess.run(cmd, capture_output=True).returncode != 0
    app.write_text('new UI only', encoding='utf-8')
    inventory.write_text(json.dumps([{'component':'routing','legacy_tokens':[],'regression_tests':[]}]), encoding='utf-8')
    assert subprocess.run(cmd, capture_output=True).returncode != 0
print('PASS: ADR-007 positive and negative checker tests')
