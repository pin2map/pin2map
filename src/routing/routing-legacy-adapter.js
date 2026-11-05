/* pin2map routing integration adapter (development only).
 * Reparents existing DOM nodes rather than cloning them: their event listeners,
 * state and legacy IDs survive. No map or routing-domain calls here.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.P2MRoutingLegacyAdapter = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const IDS = Object.freeze({
    dialog: 'routeInfo', summary: 'routeSummary', modes: null,
    reverse: 'routeReverse', end: 'routeClear', close: 'routePanelHide',
    transitMode: 'transitTimeMode', transitDate: 'p2mTransitDate',
    transitTime: 'p2mTransitClock', transitControls: 'transitTimeControls',
    all: 'routeVisiblePins', fixed: 'routeOrderToggle',
    optimal: 'routeOrderOptimal', apple: 'openAppleMaps',
    legs: 'routeLegs'
  });
  function inspect(doc) {
    const missing = [];
    for (const [key, id] of Object.entries(IDS)) {
      if (id && !doc.getElementById(id)) missing.push(key + ':' + id);
    }
    const modeButtons = Array.from(doc.querySelectorAll('#routeInfo [data-route-mode]'));
    if (modeButtons.length !== 4) missing.push('modes:expected-four');
    return { ok: missing.length === 0, missing, modeButtons };
  }
  function createAdapter(doc) {
    const report = inspect(doc);
    if (!report.ok) throw new Error('Routing legacy anchors missing: ' + report.missing.join(', '));
    const get = key => doc.getElementById(IDS[key]);
    return {
      inspect: () => inspect(doc),
      get,
      modeButtons: () => Array.from(doc.querySelectorAll('#routeInfo [data-route-mode]')),
      // Use native click on original control so existing handlers remain authoritative.
      activateMode: mode => {
        const aliases = { car: 'driving', bike: 'bicycle', walk: 'pedestrian', transit: 'transit' };
        const target = aliases[mode];
        if (!target) throw new RangeError('Unsupported mode: ' + mode);
        const button = doc.querySelector('#routeInfo [data-route-mode="' + target + '"]');
        if (!button) throw new Error('Routing mode button missing: ' + target);
        button.click();
      },
      reverse: () => get('reverse').click(),
      end: () => get('end').click(),
      close: () => get('close').click(),
      // Explicitly no cloning or rewriting of legacy controls.
      moveControl: (key, target) => {
        if (!target || typeof target.appendChild !== 'function') throw new TypeError('Invalid target');
        const node = get(key);
        if (!node) throw new RangeError('Unknown control: ' + key);
        target.appendChild(node);
        return node;
      }
    };
  }
  return { IDS, inspect, createAdapter };
});
