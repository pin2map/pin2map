#!/usr/bin/env python3
"""Real Chromium smoke tests of the shipped single-file app.

Checks initial routing UI state and dependency readiness, but NOT active-route interaction or ADR-007/008 certification.
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
            # Deterministic OSRM fixture: no external routing dependency.
            # Preserve the real fetch -> parse -> render application path.
            osrm_calls = []
            def mock_osrm(route):
                osrm_calls.append(route.request.url)
                route.fulfill(status=200, content_type="application/json", body='{"code":"Ok","routes":[{"distance":180,"duration":45,"geometry":{"type":"LineString","coordinates":[[9.1829,48.7758],[9.1840,48.7768]]},"legs":[{"distance":180,"duration":45,"steps":[{"geometry":{"coordinates":[[9.1829,48.7758],[9.1840,48.7768]]}}]}]}]}')
            page.route("**/route/v1/driving/**", mock_osrm)
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
            # A no-route state is testable without manipulating closure-private state.
            # Do not pretend that routeStartItem is a window global: it is private
            # to the app's IIFE. Active-route interactions need a real fixture.
            readiness = page.evaluate("""() => ({
                leaflet: !!window.L,
                routeToggleDisabled: document.getElementById('routePanelToggle').disabled,
                routeTogglePressed: document.getElementById('routePanelToggle').getAttribute('aria-pressed'),
                routeInfoPresent: !!document.getElementById('routeInfo'),
                leafletError: (document.getElementById('formStatus')?.textContent || '').includes('Kartenbibliothek')
            })""")
            if not readiness["leaflet"]:
                raise AssertionError(f"{label}: Leaflet dependency not loaded; cannot claim app interaction coverage: {readiness}")
            if not readiness["routeToggleDisabled"] or readiness["routeTogglePressed"] != "false":
                raise AssertionError(f"{label}: no-route toggle state incorrect: {readiness}")
            print(f"PASS {label}: initial no-route UI state and Leaflet loaded")
            # Exercise the actual mode-selection event listener with a real
            # DOM click. No endpoints exist, so no network route is requested.
            # This is a component interaction, not a full user journey.
            mode_result = page.evaluate("""() => {
                const driving = document.querySelector('[data-route-mode="driving"]');
                const bicycle = document.querySelector('[data-route-mode="bicycle"]');
                if (!driving || !bicycle) return {error:'missing mode controls'};
                try {
                    bicycle.click();
                    if (!bicycle.classList.contains('active'))
                        throw Error('bicycle mode not activated');
                    driving.click();
                    if (!driving.classList.contains('active'))
                        throw Error('driving mode not restored');
                    return {ok:true};
                } catch (e) { return {error:String(e)}; }
            }""")
            if not mode_result.get("ok"):
                raise AssertionError(f"{label}: mode-switch interaction failed: {mode_result}")
            print(f"PASS {label}: driving/bicycle mode event handling")
            # Build a deterministic two-pin map through the real list UI.
            # Numeric coordinates bypass geocoding. No private JS state is changed.
            page.locator("#back").click(force=True)
            page.locator("#input").fill("# 📍 [Red] QA\n48.7758, 9.1829 (Stuttgart)\n48.7768, 9.1840 (Stuttgart Ost)")
            page.locator("#go").evaluate("(el) => el.click()")
            page.wait_for_selector(".leaflet-marker-icon", state="attached", timeout=20000)
            page.wait_for_function("document.querySelectorAll('.leaflet-marker-icon').length >= 2", timeout=20000)
            markers = page.locator(".leaflet-marker-icon")
            if markers.count() < 2:
                raise AssertionError(f"{label}: fixture pins not rendered")
            # Spy on Leaflet's polyline constructor before routing.
            # The app uses preferCanvas; SVG path counting is invalid.
            page.evaluate("""() => {
                window.__qaRoutePolylines = [];
                const original = L.polyline;
                L.polyline = function(latlngs, options) {
                    window.__qaRoutePolylines.push(latlngs);
                    return original.apply(this, arguments);
                };
            }""")
            markers.nth(0).click()
            page.locator(".leaflet-popup [data-route-start]").click()
            markers.nth(1).click()
            page.locator(".leaflet-popup [data-route-target]").click()
            page.wait_for_function("!document.getElementById('routePanelToggle').disabled", timeout=15000)
            # Observe each click and its DOM mutation in one browser task.
            # An in-flight asynchronous routing request can otherwise reopen
            # the panel between Playwright's separate click and assertion.
            panel_result = page.evaluate("""() => {
                const panel = document.getElementById('routeInfo');
                const toggle = document.getElementById('routePanelToggle');
                document.getElementById('routePanelHide').click();
                const hidden = panel.classList.contains('route-panel-hidden');
                const pressedHidden = toggle.getAttribute('aria-pressed');
                toggle.click();
                const reopened = !panel.classList.contains('route-panel-hidden');
                const pressedOpen = toggle.getAttribute('aria-pressed');
                return {hidden, pressedHidden, reopened, pressedOpen};
            }""")
            if panel_result != {"hidden": True, "pressedHidden": "false", "reopened": True, "pressedOpen": "true"}:
                raise AssertionError(f"{label}: routing panel click contract failed: {panel_result}")
            print(f"PASS {label}: real two-pin routing selection and hide/reopen")
            # The app's summary uses de-DE formatting; capture explicit
            # diagnostics instead of obscuring failures behind a timeout.
            page.wait_for_timeout(1500)
            route_state = page.evaluate("""() => ({
                summary: document.getElementById('routeSummary')?.textContent,
                hint: document.getElementById('routeHint')?.textContent,
                routePolylineCount: (window.__qaRoutePolylines || []).length,
                canvasCount: document.querySelectorAll('.leaflet-overlay-pane canvas').length,
                legCount: document.querySelectorAll('#routeLegs .route-leg').length
            })""")
            if not (route_state["summary"] and "0.2 km" in route_state["summary"]
                    and route_state["routePolylineCount"] > 0
                    and route_state["canvasCount"] > 0):
                raise AssertionError(f"{label}: mocked OSRM route not rendered: state={route_state}; osrm_calls={osrm_calls}; js_errors={errors[:3]}")
            if len(osrm_calls) != 1:
                raise AssertionError(f"{label}: expected one OSRM request, got {len(osrm_calls)}")
            if page.locator("#routeLegs .route-leg").count() != 1:
                raise AssertionError(f"{label}: expected one rendered route leg")
            print(f"PASS {label}: mocked OSRM route fetched, drawn and summarized")
            # Failure regression: switch the same mocked endpoint to HTTP 503,
            # then trigger a fresh route request through a real mode change.
            page.unroute("**/route/v1/driving/**", mock_osrm)
            failure_calls = []
            def fail_osrm(route):
                failure_calls.append(route.request.url)
                route.fulfill(status=503, content_type="application/json", body='{"message":"Service unavailable"}')
            page.route("**/route/v1/driving/**", fail_osrm)
            page.locator('[data-route-mode="bicycle"]').evaluate("(el) => el.click()")
            page.locator('[data-route-mode="driving"]').evaluate("(el) => el.click()")
            page.wait_for_function("""() => {
                const b = document.querySelector('[data-route-mode="driving"]');
                return b && b.classList.contains('p2m-route-failed')
                    && b.disabled && document.getElementById('routeSummary')?.textContent.includes('Routing nicht möglich');
            }""", timeout=15000)
            if not failure_calls:
                raise AssertionError(f"{label}: expected a failing OSRM request")
            print(f"PASS {label}: HTTP 503 routing failure shown and failed mode disabled")
            # Recovery through the public UI: clear the failed route, then
            # select the two pins again. A new route must succeed.
            page.locator("#routeClear").evaluate("(el) => el.click()")
            page.unroute("**/route/v1/driving/**", fail_osrm)
            recovery_calls = []
            def recover_osrm(route):
                recovery_calls.append(route.request.url)
                route.fulfill(status=200, content_type="application/json", body='{"code":"Ok","routes":[{"distance":180,"duration":45,"geometry":{"type":"LineString","coordinates":[[9.1829,48.7758],[9.1840,48.7768]]},"legs":[{"distance":180,"duration":45,"steps":[{"geometry":{"coordinates":[[9.1829,48.7758],[9.1840,48.7768]]}}]}]}]}')
            page.route("**/route/v1/driving/**", recover_osrm)
            page.locator(".leaflet-marker-icon").nth(0).click()
            page.locator(".leaflet-popup [data-route-start]").click()
            page.locator(".leaflet-marker-icon").nth(1).click()
            page.locator(".leaflet-popup [data-route-target]").click()
            page.wait_for_function("""() => {
                const b = document.querySelector('[data-route-mode="driving"]');
                const summary = document.getElementById('routeSummary');
                return b && !b.disabled && !b.classList.contains('p2m-route-failed')
                    && summary?.textContent.includes('0.2 km');
            }""", timeout=15000)
            if len(recovery_calls) != 1:
                raise AssertionError(f"{label}: expected one successful recovery request, got {len(recovery_calls)}")
            print(f"PASS {label}: route recovered after clearing failed route")
            # A successful HTTP status with invalid route payload must
            # not leave a success summary or an enabled failed mode.
            page.unroute("**/route/v1/driving/**", recover_osrm)
            invalid_calls = []
            def invalid_osrm(route):
                invalid_calls.append(route.request.url)
                route.fulfill(status=200, content_type="application/json", body='{"code":"NoRoute","routes":[]}')
            page.route("**/route/v1/driving/**", invalid_osrm)
            page.locator('[data-route-mode="bicycle"]').evaluate("(el) => el.click()")
            page.locator('[data-route-mode="driving"]').evaluate("(el) => el.click()")
            page.wait_for_function("""() => {
                const b = document.querySelector('[data-route-mode="driving"]');
                return b?.disabled && b.classList.contains('p2m-route-failed')
                    && document.getElementById('routeSummary')?.textContent.includes('Routing nicht möglich');
            }""", timeout=15000)
            if len(invalid_calls) != 1:
                raise AssertionError(f"{label}: expected one invalid OSRM response request, got {len(invalid_calls)}")
            print(f"PASS {label}: HTTP 200 NoRoute payload rejected")
            # Malformed JSON must also fail safely without uncaught errors.
            page.locator("#routeClear").evaluate("(el) => el.click()")
            page.unroute("**/route/v1/driving/**", invalid_osrm)
            malformed_calls = []
            def malformed_osrm(route):
                malformed_calls.append(route.request.url)
                route.fulfill(status=200, content_type="application/json", body='{"code":')
            page.route("**/route/v1/driving/**", malformed_osrm)
            page.locator(".leaflet-marker-icon").nth(0).click()
            page.locator(".leaflet-popup [data-route-start]").click()
            page.locator(".leaflet-marker-icon").nth(1).click()
            page.locator(".leaflet-popup [data-route-target]").click()
            page.wait_for_function("""() => {
                const b = document.querySelector('[data-route-mode="driving"]');
                return b?.disabled && b.classList.contains('p2m-route-failed')
                    && document.getElementById('routeSummary')?.textContent.includes('Routing nicht möglich');
            }""", timeout=15000)
            if len(malformed_calls) != 1:
                raise AssertionError(f"{label}: malformed JSON request count {len(malformed_calls)}")
            print(f"PASS {label}: malformed routing JSON handled without crash")
            # Deterministic stale-response race: hold the first driving fetch
            # in the browser, clear the route, then complete a fresh request.
            # Releasing the old NoRoute response must not overwrite success.
            page.locator("#routeClear").evaluate("(el) => el.click()")
            page.unroute("**/route/v1/driving/**", malformed_osrm)
            race_calls = []
            def race_osrm(route):
                race_calls.append(route.request.url)
                route.fulfill(status=200, content_type="application/json", body='{"code":"Ok","routes":[{"distance":180,"duration":45,"geometry":{"type":"LineString","coordinates":[[9.1829,48.7758],[9.1840,48.7768]]},"legs":[{"distance":180,"duration":45,"steps":[{"geometry":{"coordinates":[[9.1829,48.7758],[9.1840,48.7768]]}}]}]}]}')
            page.route("**/route/v1/driving/**", race_osrm)
            page.evaluate("""() => {
                const realFetch = window.fetch.bind(window);
                window.__qaHeld = 0;
                window.__qaReleaseOld = null;
                window.fetch = function(url, opts) {
                    if (String(url).includes('/route/v1/driving/') && window.__qaHeld++ === 0) {
                        return new Promise(resolve => {
                            window.__qaReleaseOld = () => resolve(new Response(
                                '{"code":"NoRoute","routes":[]}',
                                {status: 200, headers: {'Content-Type': 'application/json'}}
                            ));
                        });
                    }
                    return realFetch(url, opts);
                };
            }""")
            page.locator(".leaflet-marker-icon").nth(0).click()
            page.locator(".leaflet-popup [data-route-start]").click()
            page.locator(".leaflet-marker-icon").nth(1).click()
            page.locator(".leaflet-popup [data-route-target]").click()
            page.wait_for_function("typeof window.__qaReleaseOld === 'function'", timeout=15000)
            page.locator("#routeClear").evaluate("(el) => el.click()")
            page.locator(".leaflet-marker-icon").nth(0).click()
            page.locator(".leaflet-popup [data-route-start]").click()
            page.locator(".leaflet-marker-icon").nth(1).click()
            page.locator(".leaflet-popup [data-route-target]").click()
            page.wait_for_function("""() => document.getElementById('routeSummary')?.textContent.includes('0.2 km')""", timeout=15000)
            page.evaluate("window.__qaReleaseOld()")
            page.wait_for_timeout(300)
            race_state = page.evaluate("""() => ({
                summary: document.getElementById('routeSummary')?.textContent,
                failed: document.querySelector('[data-route-mode="driving"]')?.classList.contains('p2m-route-failed')
            })""")
            if "0.2 km" not in (race_state["summary"] or "") or race_state["failed"] or len(race_calls) != 1:
                raise AssertionError(f"{label}: stale response corrupted new route: {race_state}, calls={race_calls}")
            print(f"PASS {label}: stale NoRoute response ignored after successful replacement")
            if errors:
                raise AssertionError(f"{label}: uncaught JavaScript errors: {errors[:5]}")
            print(f"PASS {label}: browser loaded; title={title!r}; text_chars={len(body_text)}; js_errors={len(errors)}")
            page.close()
    finally:
        browser.close()
print("LIMITATION: screenshots are evidence only; no visual-diff, live routing service verification or architecture certification.")
