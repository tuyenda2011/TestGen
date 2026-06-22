from pathlib import Path

from playwright.sync_api import expect


def test_checkout_calculates_total(page):
    fixture_url = (Path.cwd() / "source_under_test.html").resolve().as_uri()
    page.goto(fixture_url)

    page.locator("#subtotal").fill("100")
    page.locator("#weight").fill("6")
    page.locator("#tier").select_option("vip")
    page.locator("#fragile").check()
    page.locator("#calculate").click()

    expect(page.get_by_test_id("total")).to_have_text("$100.50")
