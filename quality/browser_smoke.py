#!/usr/bin/env python3
"""Real Chromium smoke tests of the shipped single-file app.

Includes routing panel interaction tests, but NOT route calculation or ADR-007/008 certification.
Produces screenshots and fails on missing app content or page load errors.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent.parent
out = root / "quality-artifacts"
out.mkdir(exist_ok=True)
url = (root / "index.html").as_uri()

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    try:
        for label, width, height in [("desktop", 1280, 800), ("mobile", 390, 844)]:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2500)
            title = page.title()
            body_text = page.locator("body").inner_text(timeout=10000)
            page.screenshot(path=str(out / f"{label}.png"), full_page=True, timeout=20000)
            if not body_text.strip():
                raise AssertionError(f"{label}: empty body text")
            # Absolutely positioned applications can have a zero-height body.
            # Require an actual visible descendant with nontrivial viewport overlap.
            visible = page.evaluate("""() => {
                const vw = innerWidth, vh = innerHeight;
                let count = 0, examples = [];
                for (const el of document.body.querySelectorAll('*')) {
                    const st = getComputedStyle(el);
                    if (st.display === 'none' || st.visibility !== 'visible' || Number(st.opacity) === 0) continue;
                    const r = el.getBoundingClientRect();
                    const w = Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0));
                    const h = Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
                    if (w >= 30 && h >= 20) {
                        count++;
                        if (examples.length < 6) examples.push({tag: el.tagName, id: el.id, width: Math.round(w), height: Math.round(h)});
                    }
                }
                return {count, examples};
            }""")
            if visible["count"] < 1:
                raise AssertionError(f"{label}: no visible app elements with viewport overlap; diagnostics={visible}; js_errors={errors[:5]}")
            # Verify the existing routing controls are present and uniquely identified.
            # This is a DOM contract test, not an end-to-end routing calculation.
            required = [
                "routeInfo", "routeSummary", "routePanelHide", "routeClear",
                "routeVisiblePins", "routeOrderToggle", "routeOrderOptimal",
                "routeReverse", "routeDetailsToggle", "routeEndpoints",
                "routeEdit", "routeLegs", "routePanelToggle"
            ]
            missing = [ident for ident in required if page.locator(f'[id="{ident}"]').count() != 1]
            if missing:
                raise AssertionError(f"{label}: routing DOM contract failed (missing or duplicate ids): {missing}")
            modes = page.locator('[data-route-mode]')
            if modes.count() < 4:
                raise AssertionError(f"{label}: expected 4 routing mode controls, found {modes.count()}")
            print(f"PASS {label}: routing DOM contract; {len(required)} unique controls, {modes.count()} modes")
            # Exercise real event handlers with synthetic route endpoints.
            # No network routing is invoked: this checks UI state transitions only.
            routing = page.evaluate("""() => {
                if (typeof syncRoutePanelToggle !== 'function' ||
                    typeof setRoutePanelHidden !== 'function' ||
                    typeof routeStartItem === 'undefined' ||
                    typeof routeTargetItem === 'undefined') {
                    return {error: 'routing globals or handlers unavailable'};
                }
                const startBefore = routeStartItem, targetBefore = routeTargetItem;
                const panel = document.getElementById('routeInfo');
                const toggle = document.getElementById('routePanelToggle');
                try {
                    routeStartItem = {label:'QA start'};
                    routeTargetItem = {label:'QA destination'};
                    syncRoutePanelToggle();
                    if (toggle.disabled || !toggle.classList.contains('route-toggle-visible'))
                        throw Error('routing toggle not enabled for active route');
                    setRoutePanelHidden(false);
                    document.getElementById('routePanelHide').click();
                    if (!panel.classList.contains('route-panel-hidden') ||
                        toggle.getAttribute('aria-pressed') !== 'false')
                        throw Error('hide button did not hide routing panel');
                    toggle.click();
                    if (panel.classList.contains('route-panel-hidden') ||
                        toggle.getAttribute('aria-pressed') !== 'true')
                        throw Error('toggle did not reopen routing panel');
                    return {ok: true};
                } catch (e) {
                    return {error: String(e)};
                } finally {
                    routeStartItem = startBefore;
                    routeTargetItem = targetBefore;
                    setRoutePanelHidden(false);
                    syncRoutePanelToggle();
                }
            }""")
            if not routing.get("ok"):
                raise AssertionError(f"{label}: routing panel interaction failed: {routing}")
            print(f"PASS {label}: routing hide/reopen event handlers")
            if errors:
                raise AssertionError(f"{label}: uncaught JavaScript errors: {errors[:5]}")
            print(f"PASS {label}: browser loaded; title={title!r}; text_chars={len(body_text)}; js_errors={len(errors)}")
            page.close()
    finally:
        browser.close()
print("LIMITATION: screenshots are evidence only; no visual-diff, route calculation or architecture certification.")
