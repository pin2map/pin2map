#!/usr/bin/env python3
"""Real Chromium smoke tests of the shipped single-file app.

This is NOT a routing-dialog regression test or ADR-007/008 certification.
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
            if not page.locator("body").is_visible():
                state = page.locator("body").evaluate("""el => ({
                    display: getComputedStyle(el).display,
                    visibility: getComputedStyle(el).visibility,
                    opacity: getComputedStyle(el).opacity,
                    rect: {width: el.getBoundingClientRect().width, height: el.getBoundingClientRect().height},
                    classes: el.className,
                    htmlClasses: document.documentElement.className
                })""")
                raise AssertionError(f"{label}: body not visible; computed state={state}; js_errors={errors[:5]}")
            print(f"PASS {label}: browser loaded; title={title!r}; text_chars={len(body_text)}; js_errors={len(errors)}")
            if errors:
                print(f"NOTICE {label}: JS errors observed (not yet release-blocking): {errors[:3]}")
            page.close()
    finally:
        browser.close()
print("LIMITATION: screenshots are evidence only; no visual-diff, routing behavior or architecture certification.")
