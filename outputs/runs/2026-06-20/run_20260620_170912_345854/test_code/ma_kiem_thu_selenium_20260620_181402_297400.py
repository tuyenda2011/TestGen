# Plan: TC-001 (form structure), TC-002 (calculateDiscount - positive, negative, boundary), TC-003 (shippingFee - positive, negative, boundary), TC-004 (submit and total - positive, negative, boundary)
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """T?o v� d�ng tr�nh duy?t Edge cho m?i test."""
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Edge(options=options)
    yield drv
    drv.quit()


def test_TC_001_form_structure_verification(driver):
    """Ki?m tra c?u tr�c form #quote-form c� d?y d? c�c di?u khi?n nhu y�u c?u."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Ki?m tra form t?n t?i v� hi?n th?
    form = driver.find_element(By.ID, "quote-form")
    assert form.is_displayed(), "Form #quote-form should be visible"
    
    # Ki?m tra n�t submit c� id l� calculate
    calculate_btn = driver.find_element(By.ID, "calculate")
    assert calculate_btn.get_attribute("type") == "submit", "Calculate button should be type submit"
    
    # Ki?m tra tru?ng subtotal
    subtotal = driver.find_element(By.ID, "subtotal")
    assert subtotal.get_attribute("type") == "number", "Subtotal should be number type"
    assert subtotal.get_attribute("step") == "0.01", "Subtotal step should be 0.01"
    assert float(subtotal.get_attribute("value")) == 100.0, "Subtotal default value should be 100"
    
    # Ki?m tra tru?ng weight
    weight = driver.find_element(By.ID, "weight")
    assert weight.get_attribute("type") == "number", "Weight should be number type"
    assert weight.get_attribute("step") == "0.01", "Weight step should be 0.01"
    assert float(weight.get_attribute("value")) == 6.0, "Weight default value should be 6"
    
    # Ki?m tra tru?ng destination
    destination = driver.find_element(By.ID, "destination")
    assert destination.tag_name == "select", "Destination should be select element"
    selected_option = destination.find_element(By.CSS_SELECTOR, "option:checked")
    assert selected_option.get_attribute("value") == "domestic", "Destination default should be domestic"
    
    # Ki?m tra tru?ng tier
    tier = driver.find_element(By.ID, "tier")
    assert tier.tag_name == "select", "Tier should be select element"
    selected_tier = tier.find_element(By.CSS_SELECTOR, "option:checked")
    assert selected_tier.get_attribute("value") == "standard", "Tier default should be standard"
    
    # Ki?m tra tru?ng fragile
    fragile = driver.find_element(By.ID, "fragile")
    assert fragile.get_attribute("type") == "checkbox", "Fragile should be checkbox type"
    
    # Ki?m tra tru?ng credit
    credit = driver.find_element(By.ID, "credit")
    assert credit.get_attribute("type") == "number", "Credit should be number type"
    assert credit.get_attribute("step") == "0.01", "Credit step should be 0.01"
    assert float(credit.get_attribute("value")) == 0.0, "Credit default value should be 0"


def test_TC_002_calculateDiscount_vip_tier(driver):
    """Ki?m tra t�nh chi?t kh?u cho tier vip: Math.min(subtotal * 0.12, 50)."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal = 500, tier = vip -> discount = min(500 * 0.12, 50) = 50
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("500")
    Select(driver.find_element(By.ID, "tier")).select_by_value("vip")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=500, discount=min(500*0.12,50)=50, shipping=domestic+weight6->+10=15, credit=0
    # total = 500 - 50 + 15 - 0 = 465
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "465.00", f"Expected total 465.00, got {total_element.text}"


def test_TC_002_calculateDiscount_loyal_tier(driver):
    """Ki?m tra t�nh chi?t kh?u cho tier loyal: Math.min(subtotal * 0.07, 30)."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal = 500, tier = loyal -> discount = min(500 * 0.07, 30) = 30
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("500")
    Select(driver.find_element(By.ID, "tier")).select_by_value("loyal")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=500, discount=min(500*0.07,30)=30, shipping=domestic+weight6->+10=15, credit=0
    # total = 500 - 30 + 15 - 0 = 485
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "485.00", f"Expected total 485.00, got {total_element.text}"


def test_TC_002_calculateDiscount_standard_tier(driver):
    """Ki?m tra t�nh chi?t kh?u cho tier standard: tr? v? 0."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal = 100, tier = standard -> discount = 0
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    Select(driver.find_element(By.ID, "tier")).select_by_value("standard")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0, shipping=domestic+weight6->+10=15, credit=0
    # total = 100 - 0 + 15 - 0 = 115
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "115.00", f"Expected total 115.00, got {total_element.text}"


def test_TC_002_calculateDiscount_vip_cap(driver):
    """Ki?m tra cap t?i da discount vip: Math.min(subtotal * 0.12, 50) v?i subtotal nh?."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal = 100, tier = vip -> discount = min(100 * 0.12, 50) = 12
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    Select(driver.find_element(By.ID, "tier")).select_by_value("vip")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=min(100*0.12,50)=12, shipping=domestic+weight6->+10=15, credit=0
    # total = 100 - 12 + 15 - 0 = 103
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "103.00", f"Expected total 103.00, got {total_element.text}"


def test_TC_002_calculateDiscount_loyal_cap(driver):
    """Ki?m tra cap t?i da discount loyal: Math.min(subtotal * 0.07, 30) v?i subtotal l?n."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal = 1000, tier = loyal -> discount = min(1000 * 0.07, 30) = 30
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("1000")
    Select(driver.find_element(By.ID, "tier")).select_by_value("loyal")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=1000, discount=min(1000*0.07,30)=30, shipping=domestic+weight6->+10=15, credit=0
    # total = 1000 - 30 + 15 - 0 = 985
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "985.00", f"Expected total 985.00, got {total_element.text}"


def test_TC_002_calculateDiscount_negative_subtotal(driver):
    """Ki?m tra khi subtotal �m th� JavaScript error x?y ra v� total kh�ng du?c c?p nh?t."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal = -100
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("-100")
    driver.find_element(By.ID, "calculate").click()
    
    # Khi c� l?i JavaScript, total s? kh�ng du?c c?p nh?t (gi? nguy�n 0.00)
    # L?i du?c throw nhung kh�ng du?c catch trong source, n�n total kh�ng thay d?i
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    # Do error x?y ra, total kh�ng du?c t�nh (gi? gi� tr? m?c d?nh ho?c tru?c d�)
    # Source kh�ng catch error n�n ch�ng ta ki?m tra total kh�ng thay d?i t? gi� tr? ban d?u
    assert total_element.text == "0.00", f"Expected total unchanged at 0.00 due to error, got {total_element.text}"


def test_TC_002_calculateDiscount_unsupported_tier(driver):
    """Ki?m tra khi tier kh�ng h?p l? th� JavaScript error x?y ra v� total kh�ng du?c c?p nh?t."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Th�m option tier kh�ng h?p l? v�o DOM
    driver.execute_script(
        "var option = document.createElement('option'); option.value = 'gold'; option.textContent = 'Gold'; document.getElementById('tier').appendChild(option);"
    )
    
    # Thi?t l?p subtotal = 100, tier = gold (kh�ng h?p l?)
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    Select(driver.find_element(By.ID, "tier")).select_by_value("gold")
    driver.find_element(By.ID, "calculate").click()
    
    # Khi c� l?i JavaScript, total s? kh�ng du?c c?p nh?t
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "0.00", f"Expected total unchanged at 0.00 due to error, got {total_element.text}"


def test_TC_003_shippingFee_domestic_base(driver):
    """Ki?m tra ph� v?n chuy?n co b?n cho domestic: 5."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = 1 (weight <= 5), destination = domestic
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("1")
    Select(driver.find_element(By.ID, "destination")).select_by_value("domestic")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0 (standard), shipping=domestic=5, credit=0
    # total = 100 - 0 + 5 - 0 = 105
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "105.00", f"Expected total 105.00, got {total_element.text}"


def test_TC_003_shippingFee_international_base(driver):
    """Ki?m tra ph� v?n chuy?n co b?n cho international: 18."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = 1, destination = international
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("1")
    Select(driver.find_element(By.ID, "destination")).select_by_value("international")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0 (standard), shipping=international=18, credit=0
    # total = 100 - 0 + 18 - 0 = 118
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "118.00", f"Expected total 118.00, got {total_element.text}"


def test_TC_003_shippingFee_weight_5_to_20(driver):
    """Ki?m tra ph� v?n chuy?n khi weight > 5 v� weight <= 20: c?ng th�m 10."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = 10 (5 < weight <= 20), destination = domestic
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("10")
    Select(driver.find_element(By.ID, "destination")).select_by_value("domestic")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0 (standard), shipping=domestic=5 + weight>5&<=20=+10=15, credit=0
    # total = 100 - 0 + 15 - 0 = 115
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "115.00", f"Expected total 115.00, got {total_element.text}"


def test_TC_003_shippingFee_weight_over_20(driver):
    """Ki?m tra ph� v?n chuy?n khi weight > 20: c?ng th�m 25."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = 25 (weight > 20), destination = domestic
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("25")
    Select(driver.find_element(By.ID, "destination")).select_by_value("domestic")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0 (standard), shipping=domestic=5 + weight>20=+25=30, credit=0
    # total = 100 - 0 + 30 - 0 = 130
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "130.00", f"Expected total 130.00, got {total_element.text}"


def test_TC_003_shippingFee_fragile_addition(driver):
    """Ki?m tra ph� v?n chuy?n khi fragile = true: c?ng th�m 7.5."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = 1, destination = domestic, fragile = checked
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("1")
    Select(driver.find_element(By.ID, "destination")).select_by_value("domestic")
    driver.find_element(By.ID, "fragile").click()
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0 (standard), shipping=domestic=5 + fragile=+7.5=12.5, credit=0
    # total = 100 - 0 + 12.5 - 0 = 112.5
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "112.50", f"Expected total 112.50, got {total_element.text}"


def test_TC_003_shippingFee_weight_zero_error(driver):
    """Ki?m tra khi weight = 0 th� JavaScript error x?y ra v� total kh�ng du?c c?p nh?t."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = 0
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("0")
    driver.find_element(By.ID, "calculate").click()
    
    # Khi c� l?i JavaScript, total s? kh�ng du?c c?p nh?t
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "0.00", f"Expected total unchanged at 0.00 due to error, got {total_element.text}"


def test_TC_003_shippingFee_weight_negative_error(driver):
    """Ki?m tra khi weight �m th� JavaScript error x?y ra v� total kh�ng du?c c?p nh?t."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p weight = -5
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("-5")
    driver.find_element(By.ID, "calculate").click()
    
    # Khi c� l?i JavaScript, total s? kh�ng du?c c?p nh?t
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "0.00", f"Expected total unchanged at 0.00 due to error, got {total_element.text}"


def test_TC_004_submit_prevents_default(driver):
    """Ki?m tra submit form g?i event.preventDefault() ngan trang reload."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Luu URL hi?n t?i
    initial_url = driver.current_url
    
    # Th?c hi?n submit
    driver.find_element(By.ID, "calculate").click()
    
    # URL kh�ng thay d?i n?u preventDefault du?c g?i
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert driver.current_url == initial_url, "URL should not change after submit (preventDefault called)"


def test_TC_004_total_calculation_with_credit(driver):
    """Ki?m tra t�nh to�n t?ng ti?n khi c� credit."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal=100, weight=1, credit=20
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("1")
    driver.find_element(By.ID, "credit").clear()
    driver.find_element(By.ID, "credit").send_keys("20")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=100, discount=0 (standard), shipping=domestic=5, credit=20
    # total = 100 - 0 + 5 - 20 = 85
    total_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "total"))
    )
    assert total_element.text == "85.00", f"Expected total 85.00, got {total_element.text}"


def test_TC_004_total_non_negative(driver):
    """Ki?m tra t?ng ti?n lu�n kh�ng �m: Math.max(total, 0)."""
    driver.get((Path.cwd() / 'source_under_test.html').resolve().as_uri())
    
    # Thi?t l?p subtotal=10, weight=1, credit=100 (credit l?n hon subtotal)
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("10")
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("1")
    driver.find_element(By.ID, "credit").clear()
    driver.find_element(By.ID, "credit").send_keys("100")
    driver.find_element(By.ID, "calculate").click()
    
    # T�nh to�n: subtotal=10, discount=0, shipping=5, credit=100
    # total = 10 - 0 + 5 - 100 = -85,