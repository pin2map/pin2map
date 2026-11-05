/* First-stage integrated routing shell.
 * Uses the existing pin2map routing DOM and original controls. No duplicate
 * event handlers for routing business logic and no change to map providers.
 * Only call mount() once after legacy routing handlers are registered.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.P2MRoutingShell = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const modeMap = { driving: 'car', bicycle: 'bike', pedestrian: 'walk', transit: 'transit' };
  function mount(doc) {
    const panel = doc.getElementById('routeInfo');
    if (!panel) throw new Error('Missing #routeInfo');
    if (panel.classList.contains('p2m-new-routing-shell')) return { mounted: true, existing: true };
    const main = panel.querySelector('.route-main');
    const summaryRow = main && main.querySelector('.route-toolbar-summary');
    const primary = main && main.querySelector('.route-toolbar-primary');
    const secondary = main && main.querySelector('.route-toolbar-secondary');
    const modes = primary && primary.querySelector('.route-mode-options');
    const close = doc.getElementById('routePanelHide');
    const reverse = doc.getElementById('routeReverse');
    const end = doc.getElementById('routeClear');
    if (![main, summaryRow, primary, secondary, modes, close, reverse, end].every(Boolean)) {
      throw new Error('Routing shell requires all original controls');
    }
    // Original mode buttons remain in the DOM with their native listeners.
    // Collapse only their presentation; never replace their event handlers.
    const modeFieldset = modes.closest('fieldset');
    if (!modeFieldset) throw new Error('Missing routing mode fieldset');
    const actions = doc.createElement('div');
    actions.className = 'p2m-shell-actions';
    const reverseWrap = doc.createElement('div');
    reverseWrap.className = 'p2m-shell-action p2m-shell-reverse';
    const endWrap = doc.createElement('div');
    endWrap.className = 'p2m-shell-action p2m-shell-end';
    const closeWrap = doc.createElement('div');
    closeWrap.className = 'p2m-shell-action p2m-shell-close';
    reverseWrap.appendChild(reverse);
    endWrap.appendChild(end);
    closeWrap.appendChild(close);
    actions.append(reverseWrap, endWrap, closeWrap);
    panel.appendChild(actions);
    summaryRow.insertBefore(modeFieldset, summaryRow.firstChild);
    // The old primary row must not be deleted: other legacy code may use it.
    // Keep it as an empty legacy anchor after moving the controls.
    const buttons = Array.from(modes.querySelectorAll('[data-route-mode]'));
    const sync = () => {
      const active = buttons.find(b => b.classList.contains('active')) || buttons[0];
      buttons.forEach(b => { b.classList.toggle('p2m-shell-mode-visible', panel.classList.contains('p2m-shell-modes-open') || b === active); });
      panel.dataset.p2mMode = modeMap[active.dataset.routeMode] || 'car';
    };
    const collapse = () => { panel.classList.remove('p2m-shell-modes-open'); sync(); };
    // Click outside the picker dismisses the overlay without changing the route.
    doc.addEventListener('pointerdown', function (event) {
      if (panel.classList.contains('p2m-shell-modes-open') && !modeFieldset.contains(event.target)) collapse();
    });
    const open = () => { panel.classList.add('p2m-shell-modes-open'); buttons.forEach(b => b.classList.add('p2m-shell-mode-visible')); };
    buttons.forEach(b => b.addEventListener('click', function () {
      if (panel.classList.contains('p2m-shell-modes-open')) {
        // Existing mode handlers handle route changes.
        collapse();
      } else if (b.classList.contains('active')) {
        open();
      }
      // Let existing handlers finish before reflecting the selected mode.
      if (typeof queueMicrotask === 'function') queueMicrotask(sync);
    }));
    panel.classList.add('p2m-new-routing-shell');
    sync();
    return { mounted: true, collapse, sync };
  }
  return { mount };
});
