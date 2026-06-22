import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    """T?o fixture page cho Playwright v?i Microsoft Edge"""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page()
        yield page
        browser.close()


def test_calculate_total_vip_tier_no_cap(page):
    """Ki?m tra t�nh to�n t?ng cho tier VIP khi chua d?t m?c gi?m t?i da"""
    page.goto((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    page.fill('#subtotal', '200')
    page.fill('#weight', '10')
    page.select_option('#destination', 'domestic')
    page.select_option('#tier', 'vip')
    page.uncheck('#fragile')
    page.fill('#credit', '0')
    page.click('#calculate')
    page.wait_for_selector('#total')
    total = page.text_content('#total')
    assert total == '191.00'


def test_calculate_total_vip_tier_with_cap(page):
    """Ki?m tra t�nh to�n t?ng cho tier VIP khi d?t m?c gi?m t?i da"""
    page.goto((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    page.fill('#subtotal', '600')
    page.fill('#weight', '5')
    page.select_option('#destination', 'international')
    page.select_option('#tier', 'vip')
    page.check('#fragile')
    page.fill('#credit', '20')
    page.click('#calculate')
    page.wait_for_selector('#total')
    total = page.text_content('#total')
    assert total == '555.50'


def test_calculate_total_loyal_tier_weight_over_20_fragile(page):
    """Ki?m tra t�nh to�n t?ng cho tier Loyal v?i weight > 20 v� fragile"""
    page.goto((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    page.fill('#subtotal', '150')
    page.fill('#weight', '25')
    page.select_option('#destination', 'domestic')
    page.select_option('#tier', 'loyal')
    page.check('#fragile')
    page.fill('#credit', '0')
    page.click('#calculate')
    page.wait_for_selector('#total')
    total = page.text_content('#total')
    assert total == '177.00'


def test_calculate_total_zero_subtotal(page):
    """Ki?m tra t�nh to�n t?ng khi subtotal b?ng 0"""
    page.goto((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    page.fill('#subtotal', '0')
    page.fill('#weight', '1')
    page.select_option('#destination', 'domestic')
    page.select_option('#tier', 'standard')
    page.uncheck('#fragile')
    page.fill('#credit', '0')
    page.click('#calculate')
    page.wait_for_selector('#total')
    total = page.text_content('#total')
    assert total == '5.00'


def test_calculate_total_weight_exactly_20(page):
    """Ki?m tra t�nh to�n t?ng khi weight d�ng 20kg �p d?ng ph� surcharge d�ng"""