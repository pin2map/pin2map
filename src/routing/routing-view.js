/* pin2map RoutingView – standalone, framework-free UI module.
 * Prototype scaffold; not wired into production. Lucide icons supplied by
 * an injected central icon factory, never by routing domain code.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.P2MRoutingView = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const MODES = Object.freeze(['car', 'bike', 'walk', 'transit']);
  const ICONS = Object.freeze({
    car: 'car-front', bike: 'bike', walk: 'footprints',
    transit: 'tram-front', reverse: 'arrow-left-right',
    end: 'x', close: 'check'
  });
  function createRoutingView(options) {
    if (!options || !options.document || !options.mount) {
      throw new TypeError('document and mount are required');
    }
    const doc = options.document;
    const mount = options.mount;
    const emit = typeof options.onAction === 'function' ? options.onAction : function () {};
    const icon = typeof options.createIcon === 'function' ? options.createIcon : null;
    let state = { mode: 'car', expanded: false, alternatives: [], selectedId: null, summary: '', legsNode: null };
    function el(tag, className, text) {
      const node = doc.createElement(tag);
      if (className) node.className = className;
      if (text != null) node.textContent = String(text);
      return node;
    }
    function addIcon(button, key) {
      const name = ICONS[key];
      const node = icon && icon(name, doc);
      if (node) button.appendChild(node);
      else {
        const fallback = el('span', 'p2m-routing-icon-fallback', name);
        fallback.setAttribute('aria-hidden', 'true');
        button.appendChild(fallback);
      }
    }
    function actionButton(action, label, className) {
      const b = el('button', className);
      b.type = 'button';
      b.setAttribute('aria-label', label);
      b.title = label;
      addIcon(b, action);
      const caption = el('span', 'p2m-routing-action-caption', label);
      b.appendChild(caption);
      b.addEventListener('click', function () { emit(action); });
      return b;
    }
    function render() {
      mount.replaceChildren();
      const dialog = el('section', 'p2m-routing-view');
      dialog.setAttribute('aria-label', 'Routing');
      const main = el('div', 'p2m-routing-main');
      const header = el('header', 'p2m-routing-header');
      const modeGroup = el('div', 'p2m-routing-modes');
      const visible = state.expanded ? MODES : [state.mode];
      visible.forEach(function (mode) {
        const button = el('button', 'p2m-routing-mode' + (mode === state.mode && state.expanded ? ' is-expanded' : ''));
        button.type = 'button';
        button.setAttribute('aria-label', mode);
        button.setAttribute('aria-expanded', String(mode === state.mode && state.expanded));
        addIcon(button, mode);
        button.addEventListener('click', function () {
          if (mode === state.mode) {
            state = Object.assign({}, state, { expanded: !state.expanded });
            render();
          } else {
            state = Object.assign({}, state, { mode: mode, expanded: false });
            emit('mode', mode);
            render();
          }
        });
        modeGroup.appendChild(button);
      });
      header.appendChild(modeGroup);
      header.appendChild(el('div', 'p2m-routing-summary', state.summary));
      main.appendChild(header);
      const controls = el('div', 'p2m-routing-controls');
      if (state.mode === 'transit') {
        ['departureOrArrival', 'date', 'time'].forEach(function (name) {
          const slot = el('div', 'p2m-routing-control-slot');
          slot.dataset.control = name;
          controls.appendChild(slot);
        });
      } else {
        ['all', 'fix', 'opt', 'apple'].forEach(function (name) {
          const slot = el('div', 'p2m-routing-control-slot');
          slot.dataset.control = name;
          controls.appendChild(slot);
        });
      }
      main.appendChild(controls);
      const scroll = el('div', 'p2m-routing-scroll');
      if (state.mode === 'transit') {
        const alternatives = el('div', 'p2m-routing-alternatives');
        state.alternatives.forEach(function (route, index) {
          const active = route.id === state.selectedId;
          const b = el('button', 'p2m-routing-alternative' + (active ? ' is-active' : ''));
          b.type = 'button';
          b.setAttribute('aria-pressed', String(active));
          b.appendChild(el('span', 'p2m-routing-number', index + 1));
          const details = el('span', 'p2m-routing-alternative-details');
          details.appendChild(el('span', 'p2m-routing-times', route.times || ''));
          const meta = el('span', 'p2m-routing-meta');
          meta.textContent = [route.duration, route.transfers].filter(Boolean).join(' · ');
          details.appendChild(meta);
          b.appendChild(details);
          b.addEventListener('click', function () { emit('selectAlternative', route.id); });
          alternatives.appendChild(b);
        });
        scroll.appendChild(alternatives);
      }
      const legs = el('div', 'p2m-routing-legs');
      if (state.legsNode) legs.appendChild(state.legsNode);
      scroll.appendChild(legs);
      main.appendChild(scroll);
      const actions = el('aside', 'p2m-routing-actions');
      actions.appendChild(actionButton('reverse', 'Umkehren', 'p2m-routing-action'));
      actions.appendChild(actionButton('end', 'Beenden', 'p2m-routing-action is-danger'));
      actions.appendChild(actionButton('close', 'Schließen', 'p2m-routing-action'));
      dialog.appendChild(main);
      dialog.appendChild(actions);
      mount.appendChild(dialog);
    }
    function update(next) {
      if (!next || typeof next !== 'object') throw new TypeError('state must be an object');
      if (next.mode != null && !MODES.includes(next.mode)) throw new RangeError('unsupported mode');
      state = Object.assign({}, state, next);
      render();
    }
    render();
    return { update: update, destroy: function () { mount.replaceChildren(); }, getState: function () { return Object.assign({}, state); } };
  }
  return Object.freeze({ createRoutingView: createRoutingView, MODES: MODES, ICONS: ICONS });
});
