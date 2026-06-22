import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import time

@pytest.fixture(scope="module")
def driver():
    """Kh?i t?o tr�nh duy?t Edge v� m? file HTML fixture."""
    options = EdgeOptions()
    options.add_argument("--headless")
    service = EdgeService()
    driver = webdriver.Edge(service=service, options=options)
    file_uri = (Path.cwd() / "source_under_test.html").resolve().as_uri()
    driver.get(file_uri)
    yield driver
    driver.quit()

def fill_form(driver, data):
    """Nh?p d? li?u v�o c�c tru?ng c?a form d?a tr�n dict `data`."""
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys(str(data["subtotal"]))
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys(str(data["weight"]))
    driver.find_element(By.ID, "destination").send_keys(data["destination"])
    driver.find_element(By.ID, "tier").send_keys(data["tier"])
    fragile_elem = driver.find_element(By.ID, "fragile")
    if data["fragile"]:
        if not fragile_elem.is_selected():
            fragile_elem.click()
    else:
        if fragile_elem.is_selected():
            fragile_elem.click()
    driver.find_element(By.ID, "credit").clear()
    driver.find_element(By.ID, "credit").send_keys(str(data["credit"]))

def click_calculate(driver):
    """Nh?n n�t t�nh to�n v� ch? UI c?p nh?t."""
    driver.find_element(By.ID, "calculate").click()
    # �?i ng?n d? JavaScript th?c thi
    time.sleep(0.2)

def get_output(driver, selector):
    """L?y textContent c?a ph?n t? output."""
    return driver.find_element(By.CSS_SELECTOR, selector).text

def test_standard_domestic_nonfragile_weight6_credit0(driver):
    """TC-001: Ki?m tra t?ng cho tier standard, destination domestic, kh�ng fragile, weight 6, kh�ng credit."""
    data = {
        "subtotal": 100,
        "weight": 6,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    click_calculate(driver)

    total = get_output(driver, "#total")
    error = get_output(driver, "#error")
    assert total == "115.00"
    assert error == ""

def test_vip_international_fragile_weight22_credit20(driver):
    """TC-002: Ki?m tra t?ng cho tier vip, destination international, fragile, weight 22, credit 20."""
    data = {
        "subtotal": 200,
        "weight": 22,
        "destination": "international",
        "tier": "vip",
        "fragile": True,
        "credit": 20,
    }
    fill_form(driver, data)
    click_calculate(driver)

    total = get_output(driver, "#total")
    error = get_output(driver, "#error")
    assert total == "206.50"
    assert error == ""

def test_loyal_weight5_domestic(driver):
    """TC-003: Ki?m tra tr?ng lu?ng d�ng 5kg (kh�ng c?ng ph� ph?) cho tier loyal, domestic."""
    data = {
        "subtotal": 150,
        "weight": 5,
        "destination": "domestic",
        "tier": "loyal",
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    click_calculate(driver)

    total = get_output(driver, "#total")
    error = get_output(driver, "#error")
    assert total == "144.50"
    assert error == ""

def test_standard_weight20_international(driver):
    """TC-004: Ki?m tra tr?ng lu?ng d�ng 20kg (c?ng 10, kh�ng 25) cho tier standard, international."""
    data = {
        "subtotal": 80,
        "weight": 20,
        "destination": "international",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    click_calculate(driver)

    total = get_output(driver, "#total")
    error = get_output(driver, "#error")
    assert total == "108.00"
    assert error == ""

def test_negative_subtotal_error(driver):
    """TC-005: Ki?m tra l?i khi subtotal �m � kh�ng thay d?i total v� error v?n r?ng."""
    # Luu tr?ng th�i hi?n t?i d? so s�nh
    prev_total = get_output(driver, "#total")
    prev_error = get_output(driver, "#error")

    data = {
        "subtotal": -10,
        "weight": 5,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    click_calculate(driver)

    # V� l?i du?c n�m trong JavaScript v� kh�ng c� catch, UI kh�ng thay d?i
    assert get_output(driver, "#total") == prev_total
    assert get_output(driver, "#error") == prev_error

def test_zero_weight_error(driver):
    """TC-006: Ki?m tra l?i khi weight b?ng 0 � UI kh�ng thay d?i total v� error."""
    prev_total = get_output(driver, "#total")
    prev_error = get_output(driver, "#error")

    data = {
        "subtotal": 50,
        "weight": 0,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    click_calculate(driver)

    assert get_output(driver, "#total") == prev_total
    assert get_output(driver, "#error") == prev_error

def test_unsupported_tier_error(driver):
    """TC-007: Ki?m tra l?i khi tier kh�ng h?p l? � UI kh�ng thay d?i total v� error."""
    prev_total = get_output(driver, "#total")
    prev_error = get_output(driver, "#error")

    # Thay d?i gi� tr? tier b?ng c�ch th?c thi JavaScript v� select kh�ng c� option 'gold'
    driver.execute_script("document.getElementById('tier').value = 'gold';")
    data = {
        "subtotal": 100,
        "weight": 5,
        "destination": "domestic",
        "tier": "gold",  # gi� tr? kh�ng h?p l?
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    click_calculate(driver)

    assert get_output(driver, "#total") == prev_total
    assert get_output(driver, "#error") == prev_error

def test_credit_exceeds_total(driver):
    """TC-008: Ki?m tra khi credit l?n hon subtotal+shippingFee � total hi?n th? 0.00."""
    data = {
        "subtotal": 30,
        "weight": 3,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 40,
    }
    fill_form(driver, data)
    click_calculate(driver)

    total = get_output(driver, "#total")
    error = get_output(driver, "#error")
    assert total == "0.00"
    assert error == ""

def test_default_values_produce_correct_total(driver):
    """TC-009: Ki?m tra khi kh�ng thay d?i gi� tr? m?c d?nh � t?ng d�ng 115.00."""
    # Reset l?i trang d? d?m b?o gi� tr? m?c d?nh
    driver.refresh()
    time.sleep(0.2)  # d?i trang t?i l?i
    click_calculate(driver)

    total = get_output(driver, "#total")
    error = get_output(driver, "#error")
    assert total == "115.00"
    assert error == ""