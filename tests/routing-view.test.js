/* node --test tests/routing-view.test.js
 * No external packages. Tests the public view contract with a minimal DOM.
 */
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { createRoutingView, MODES, ICONS } = require('../src/routing/routing-view.js');

class Node {
  constructor(tag) {
    this.tagName = tag;
    this.children = [];
    this.attributes = {};
    this.dataset = {};
    this.listeners = {};
    this.className = '';
    this.textContent = '';
  }
  appendChild(child) {
    if (child.parentNode) child.parentNode.children = child.parentNode.children.filter(x => x !== child);
    this.children.push(child);
    child.parentNode = this;
    return child;
  }
  replaceChildren(...children) {
    this.children.forEach(x => { x.parentNode = null; });
    this.children = [];
    children.forEach(x => this.appendChild(x));
  }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  addEventListener(k, fn) { this.listeners[k] = fn; }
  click() { if (this.listeners.click) this.listeners.click(); }
}
const document = { createElement: tag => new Node(tag) };
function find(node, className) {
  const all = [];
  function visit(n) {
    if (n.className.split(/\s+/).includes(className)) all.push(n);
    n.children.forEach(visit);
  }
  visit(node);
  return all;
}
function setup() {
  const mount = new Node('main');
  const events = [];
  const view = createRoutingView({ document, mount, onAction: (...args) => events.push(args) });
  return { mount, events, view };
}
test('mode menu initially has exactly one grey button', () => {
  const { mount } = setup();
  assert.equal(find(mount, 'p2m-routing-mode').length, 1);
  assert.equal(find(mount, 'is-expanded').length, 0);
});
test('expanding exposes four modes and selecting closes menu and emits', () => {
  const { mount, events } = setup();
  find(mount, 'p2m-routing-mode')[0].click();
  assert.equal(find(mount, 'p2m-routing-mode').length, 4);
  assert.equal(find(mount, 'is-expanded').length, 1);
  find(mount, 'p2m-routing-mode')[1].click();
  assert.deepEqual(events, [['mode', 'bike']]);
  assert.equal(find(mount, 'p2m-routing-mode').length, 1);
  assert.equal(find(mount, 'is-expanded').length, 0);
});
test('transit has exactly three control slots', () => {
  const { mount, view } = setup();
  view.update({ mode: 'transit' });
  assert.deepEqual(find(mount, 'p2m-routing-control-slot').map(x => x.dataset.control),
    ['departureOrArrival', 'date', 'time']);
});
test('non-transit has multi-pin controls and Apple slot', () => {
  const { mount, view } = setup();
  for (const mode of ['car', 'bike', 'walk']) {
    view.update({ mode });
    assert.deepEqual(find(mount, 'p2m-routing-control-slot').map(x => x.dataset.control),
      ['all', 'fix', 'opt', 'apple']);
  }
});
test('transit list is dynamic and emits selected id without mutating selection', () => {
  const { mount, events, view } = setup();
  view.update({ mode: 'transit', alternatives: [
    { id: 'a', times: '10–11' }, { id: 'b', times: '12–13' }
  ], selectedId: 'a' });
  assert.equal(find(mount, 'p2m-routing-alternative').length, 2);
  assert.equal(find(mount, 'is-active').length, 1);
  find(mount, 'p2m-routing-alternative')[1].click();
  assert.deepEqual(events, [['selectAlternative', 'b']]);
  view.update({ selectedId: 'b', alternatives: [{ id: 'b' }] });
  assert.equal(find(mount, 'p2m-routing-alternative').length, 1);
  assert.equal(find(mount, 'is-active').length, 1);
});
test('action order and labels are stable', () => {
  const { mount, events } = setup();
  const buttons = find(mount, 'p2m-routing-action');
  assert.deepEqual(buttons.map(x => x.attributes['aria-label']), ['Umkehren', 'Beenden', 'Schließen']);
  buttons.forEach(x => x.click());
  assert.deepEqual(events, [['reverse'], ['end'], ['close']]);
});
test('rejects invalid mode and preserves previous state', () => {
  const { view } = setup();
  assert.throws(() => view.update({ mode: 'airplane' }), RangeError);
  assert.equal(view.getState().mode, 'car');
  assert.deepEqual(MODES, ['car', 'bike', 'walk', 'transit']);
  assert.equal(ICONS.transit, 'tram-front');
});
test('existing itinerary node is preserved across rerenders', () => {
  const { mount, view } = setup();
  const existing = new Node('article');
  view.update({ legsNode: existing });
  assert.equal(find(mount, 'p2m-routing-legs')[0].children[0], existing);
  view.update({ summary: 'Updated' });
  assert.equal(find(mount, 'p2m-routing-legs')[0].children[0], existing);
});
test('destroy clears mount', () => {
  const { mount, view } = setup();
  view.destroy();
  assert.equal(mount.children.length, 0);
});
