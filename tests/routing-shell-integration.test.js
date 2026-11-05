/* Regression guard for the opt-in full HTML integration.
 * Run with: node --test tests/routing-shell-integration.test.js
 */
'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const html = readFileSync(join(__dirname, '..', 'index.html'), 'utf8');
test('full application remains a complete HTML document', () => {
  assert.match(html, /^<!doctype html>/i);
  assert.match(html, /<\/body><\/html>\s*$/i);
});
test('legacy routing controls are retained once', () => {
  for (const id of ['routeInfo','routeSummary','routePanelHide','routeClear',
    'routeReverse','routeVisiblePins','routeOrderToggle','routeOrderOptimal',
    'openAppleMaps','transitTimeMode','p2mTransitDate','p2mTransitClock','routeLegs']) {
    assert.equal((html.match(new RegExp('id="' + id + '"', 'g')) || []).length, 1, id);
  }
});
test('experimental routing shell requires an explicit URL opt-in', () => {
  assert.match(html, /new URLSearchParams\(location\.search\)\.has\('routingShell'\)/);
  assert.match(html, /if\(!new URLSearchParams\(location\.search\)\.has\('routingShell'\)\)return/);
  assert.match(html, /P2MRoutingShell\.mount\(document\)/);
});
test('embedded shell is unique', () => {
  for (const id of ['p2m-dev-routing-shell-style','p2m-dev-routing-shell-code','p2m-dev-routing-shell-bootstrap'])
    assert.equal((html.match(new RegExp('id="' + id + '"', 'g')) || []).length, 1, id);
});
