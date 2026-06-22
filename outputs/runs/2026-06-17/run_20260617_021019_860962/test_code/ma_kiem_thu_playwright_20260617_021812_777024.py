import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        try:
            yield page
        finally:
            browser.close()


from pathlib import Path
from playwright.sync_api import sync_playwright, Page, expect

@pytest.fixture(scope="session")
def browser():
    """Kh?i t?o tr�nh duy?t Microsoft Edge ? ch? d? headless cho to�n b? session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser) -> Page:
    """Cung c?p m?t trang m?i, t?i file HTML c?c b? v� tr? v? d?i tu?ng Page."""
    context = browser.new_context()
    page = context.new_page()
    page.goto((Path.cwd() / "source_under_test.html").resolve().as_uri())
    yield page
    context.close()


def fill_form(page: Page, data: dict):
    """�i?n c�c tru?ng nh?p li?u tr�n form d?a tr�n dict `data`."""
    page.fill("#subtotal", str(data["subtotal"]))
    page.fill("#weight", str(data["weight"]))
    page.select_option("#destination", data["destination"])
    page.select_option("#tier", data["tier"])
    if data.get("fragile", False):
        page.check("#fragile")
    else:
        page.uncheck("#fragile")
    page.fill("#credit", str(data["credit"]))
    page.click("#calculate")


def get_total(page: Page) -> str:
    """L?y gi� tr? hi?n th? c?a total."""
    return page.locator('[data-testid="total"]').inner_text().strip()


def get_error(page: Page) -> str:
    """L?y th�ng b�o l?i n?u c�."""
    return page.locator('[data-testid="error"]').inner_text().strip()


def test_vip_domestic_shipping(page: Page):
    """TC-001: T�nh t?ng cho kh�ch VIP, giao h�ng n?i d?a, tr?ng lu?ng 10kg, kh�ng fragile, kh�ng credit."""
    fill_form(page, {
        "subtotal": 200,
        "weight": 10,
        "destination": "domestic",
        "tier": "vip",
        "fragile": False,
        "credit": 0,
    })
    # subtotal 200 - discount 24 + shipping 15 = 191.00
    expect(page.locator('[data-testid="total"]')).to_have_text("191.00")
    assert get_error(page) == ""


def test_loyal_international_heavy_fragile_credit(page: Page):
    """TC-002: T�nh t?ng cho kh�ch Loyal, giao h�ng qu?c t?, tr?ng lu?ng 22kg, fragile, credit 20."""
    fill_form(page, {
        "subtotal": 400,
        "weight": 22,
        "destination": "international",
        "tier": "loyal",
        "fragile": True,
        "credit": 20,
    })
    # subtotal 400 - discount 28 + shipping 50.5 - credit 20 = 402.50
    expect(page.locator('[data-testid="total"]')).to_have_text("402.50")
    assert get_error(page) == ""


def test_subtotal_zero_min_weight(page: Page):
    """TC-003: Subtotal = 0, tr?ng lu?ng t?i thi?u 0.01kg, tier standard, kh�ng fragile."""
    fill_form(page, {
        "subtotal": 0,
        "weight": 0.01,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    })
    # subtotal 0 + shipping 5 = 5.00
    expect(page.locator('[data-testid="total"]')).to_have_text("5.00")
    assert get_error(page) == ""


def test_weight_exactly_5kg(page: Page):
    """TC-004: Tr?ng lu?ng d�ng 5kg, ph� th�m $10 kh�ng �p d?ng (ch? �p d?ng >5kg)."""
    fill_form(page, {
        "subtotal": 100,
        "weight": 5,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    })
    # subtotal 100 + shipping 5 = 105.00
    expect(page.locator('[data-testid="total"]')).to_have_text("105.00")
    assert get_error(page) == ""


def test_weight_exactly_20kg(page: Page):
    """TC-005: Tr?ng lu?ng d�ng 20kg, ch? �p d?ng ph� $10, kh�ng $25."""
    fill_form(page, {
        "subtotal": 150,
        "weight": 20,
        "destination": "international",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    })
    # subtotal 150 + shipping (base 18 + 10) = 178.00
    expect(page.locator('[data-testid="total"]')).to_have_text("178.00")
    assert get_error(page) == ""


def test_fragile_fee(page: Page):
    """TC-006: Fragile true th�m ph� $7.5."""
    fill_form(page, {
        "subtotal": 120,
        "weight": 4,
        "destination": "domestic",
        "tier": "standard",
        "fragile": True,
        "credit": 0,
    })
    # subtotal 120 + shipping (5 + 7.5) = 132.50
    expect(page.locator('[data-testid="total"]')).to_have_text("132.50")
    assert get_error(page) == ""