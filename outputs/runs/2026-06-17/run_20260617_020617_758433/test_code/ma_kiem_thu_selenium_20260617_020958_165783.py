import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import JavascriptException

@pytest.fixture(scope="module")
def driver():
    """Kh?i t?o tr�nh duy?t Edge cho to�n b? module test."""
    options = EdgeOptions()
    options.add_argument("--headless")
    service = EdgeService()
    driver = webdriver.Edge(service=service, options=options)
    yield driver
    driver.quit()

def load_page(driver):
    """M? file HTML fixture trong tr�nh duy?t."""
    uri = (Path.cwd() / "source_under_test.html").resolve().as_uri()
    driver.get(uri)

def fill_form(driver, subtotal, weight, destination, tier, fragile, credit):
    """Nh?p d? li?u v�o c�c tru?ng c?a form."""
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys(str(subtotal))

    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys(str(weight))

    dest_select = driver.find_element(By.ID, "destination")
    for option in dest_select.find_elements(By.TAG_NAME, "option"):
        if option.get_attribute("value") == destination:
            option.click()
            break

    tier_select = driver.find_element(By.ID, "tier")
    for option in tier_select.find_elements(By.TAG_NAME, "option"):
        if option.get_attribute("value") == tier:
            option.click()
            break

    fragile_checkbox = driver.find_element(By.ID, "fragile")
    if fragile != fragile_checkbox.is_selected():
        fragile_checkbox.click()

    driver.find_element(By.ID, "credit").clear()
    driver.find_element(By.ID, "credit").send_keys(str(credit))

def submit_form(driver):
    """Nh?n n�t t�nh to�n d? submit form."""
    driver.find_element(By.ID, "calculate").click()

def get_total_text(driver):
    """L?y n?i dung hi?n th? c?a ph?n t? total."""
    return driver.find_element(By.ID, "total").text

def get_error_text(driver):
    """L?y n?i dung hi?n th? c?a ph?n t? error."""
    return driver.find_element(By.ID, "error").text

def test_standard_domestic_no_fragile_no_credit(driver):
    """TC-001: Ki?m tra t?ng cho tier standard, giao h�ng n?i d?a, kh�ng fragile, kh�ng credit."""
    load_page(driver)
    fill_form(driver, subtotal=100, weight=3, destination="domestic",
              tier="standard", fragile=False, credit=0)
    submit_form(driver)
    assert get_error_text(driver) == ""
    assert get_total_text(driver) == "105.00"

def test_vip_international_heavy_fragile_with_credit(driver):
    """TC-002: Ki?m tra t?ng cho tier VIP, giao h�ng qu?c t?, tr?ng lu?ng >20, fragile, c� credit."""
    load_page(driver)
    fill_form(driver, subtotal=600, weight=22, destination="international",
              tier="vip", fragile=True, credit=20)
    submit_form(driver)
    assert get_error_text(driver) == ""
    # T?ng = 600 - 50 (discount) + 50.5 (shipping) - 20 = 580.5 ? 580.50
    assert get_total_text(driver) == "580.50"

def test_loyal_zero_subtotal_minimal_shipping(driver):
    """TC-003: Ki?m tra t?ng khi subtotal = 0, tier loyal, tr?ng lu?ng r?t nh?, kh�ng fragile."""
    load_page(driver)
    fill_form(driver, subtotal=0, weight=0.1, destination="domestic",
              tier="loyal", fragile=False, credit=0)
    submit_form(driver)
    assert get_error_text(driver) == ""
    # Discount = 0, shipping = 5, total = 5.00
    assert get_total_text(driver) == "5.00"

def test_negative_subtotal_raises_error(driver):
    """TC-004: Ki?m tra r?ng h�m calculateDiscount n�m l?i khi subtotal �m."""
    load_page(driver)
    with pytest.raises(JavascriptException) as excinfo:
        driver.execute_script("return calculateDiscount(-10, 'standard');")
    assert "subtotal must not be negative" in str(excinfo.value)

def test_invalid_tier_raises_error(driver):
    """TC-005: Ki?m tra r?ng h�m calculateDiscount n�m l?i khi tier kh�ng h?p l?."""
    load_page(driver)
    with pytest.raises(JavascriptException) as excinfo:
        driver.execute_script("return calculateDiscount(50, 'gold');")
    assert "unsupported customer tier" in str(excinfo.value)

def test_zero_weight_raises_error(driver):
    """TC-006: Ki?m tra r?ng h�m shippingFee n�m l?i khi weight kh�ng duong."""
    load_page(driver)
    with pytest.raises(JavascriptException) as excinfo:
        driver.execute_script("return shippingFee(0, 'domestic', false);")
    assert "weight must be greater than zero" in str(excinfo.value)