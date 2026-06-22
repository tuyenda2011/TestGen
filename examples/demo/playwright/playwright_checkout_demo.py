import os
from pathlib import Path

from playwright.sync_api import Page, expect


def _demo_url() -> str:
    configured = os.environ.get("CHECKOUT_DEMO_URL")
    if configured:
        return configured
    fixture_path = Path(__file__).parents[1] / "selenium" / "ui_checkout_fixture.html"
    return fixture_path.resolve().as_uri()


def test_playwright_checkout_vip_domestic_total(page: Page) -> None:
    page.goto(_demo_url())

    page.locator("#subtotal").fill("100")
    page.locator("#weight").fill("6")
    page.locator("#destination").select_option("domestic")
    page.locator("#tier").select_option("vip")
    page.locator("#fragile").check()
    page.locator("#credit").fill("10")
    page.locator("#calculate").click()

    expect(page.get_by_test_id("total")).to_have_text("100.50")


def test_playwright_checkout_heavy_international_boundary(page: Page) -> None:
    page.goto(_demo_url())

    page.locator("#subtotal").fill("100")
    page.locator("#weight").fill("20.01")
    page.locator("#destination").select_option("international")
    page.locator("#tier").select_option("standard")
    page.locator("#credit").fill("0")
    page.locator("#calculate").click()

    expect(page.get_by_test_id("total")).to_have_text("143.00")
