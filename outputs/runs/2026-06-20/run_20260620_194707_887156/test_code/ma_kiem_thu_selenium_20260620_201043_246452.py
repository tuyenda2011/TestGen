import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------------------------------------------------
# Selectors � use stable IDs / data-testids
# ----------------------------------------------------------------------
SUBTOTAL_INPUT = (By.ID, "subtotal")
WEIGHT_INPUT = (By.ID, "weight")
DESTINATION_SELECT = (By.ID, "destination")
TIER_SELECT = (By.ID, "tier")
FRAGILE_CHECKBOX = (By.ID, "fragile")
CREDIT_INPUT = (By.ID, "credit")
CALCULATE_BUTTON = (By.ID, "calculate")
TOTAL_OUTPUT = (By.CSS_SELECTOR, "[data-testid='total']")
ERROR_OUTPUT = (By.CSS_SELECTOR, "[data-testid='error']")

# ----------------------------------------------------------------------
# Fixture � Edge browser
# ----------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver():
    """Kh?i t?o tr�nh duy?t Edge v� d�ng sau m?i test."""
    drv = webdriver.Edge()
    yield drv
    drv.quit()

# ----------------------------------------------------------------------
# Helper � open the fixture page
# ----------------------------------------------------------------------
def open_page(driver):
    url = (Path.cwd() / "source_under_test.html").resolve().as_uri()
    driver.get(url)

# ----------------------------------------------------------------------
# 1?? Ki?m tra t�nh t?ng khi m?i d? li?u h?p l?
# ----------------------------------------------------------------------
def test_total_calculation_basic(driver):
    """
    Subtotal=100, tier=standard, weight=6 (domestic ? fee 5 + 10 = 15),
    credit=0, kh�ng fragile.
    T?ng = 100 - 0 + 15 - 0 = 115.00
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("100")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("6")
    driver.find_element(*DESTINATION_SELECT).send_keys("domestic")
    driver.find_element(*TIER_SELECT).send_keys("standard")
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("0")
    driver.find_element(*CALCULATE_BUTTON).click()

    # T?ng hi?n th?
    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # 100 (subtotal) - 0 (discount) + 15 (shipping) - 0 (credit) = 115.00
    assert total_elem.text == "115.00"
    # Kh�ng c� th�ng b�o l?i
    assert driver.find_element(*ERROR_OUTPUT).text == ""

# ----------------------------------------------------------------------
# 2?? Ki?m tra gi?m gi� cho tier VIP (max $50)
# ----------------------------------------------------------------------
def test_discount_vip_capped(driver):
    """
    Subtotal=600, tier=vip ? discount = min(600*0.12, 50) = 50
    Weight=4kg (domestic, fee=5), credit=0.
    T?ng = 600 - 50 + 5 = 555.00
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("600")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("4")
    driver.find_element(*DESTINATION_SELECT).send_keys("domestic")
    driver.find_element(*TIER_SELECT).send_keys("vip")
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("0")
    driver.find_element(*CALCULATE_BUTTON).click()

    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # 600 - 50 + 5 = 555.00
    assert total_elem.text == "555.00"
    assert driver.find_element(*ERROR_OUTPUT).text == ""

# ----------------------------------------------------------------------
# 3?? Ki?m tra ph� v?n chuy?n qu?c t? (kh�ng ph? thu?c tr?ng lu?ng <5kg)
# ----------------------------------------------------------------------
def test_shipping_fee_international(driver):
    """
    Subtotal=50, tier=standard, weight=3kg, destination=international.
    Fee co b?n = 18 (kh�ng c?ng th�m v� weight =5), kh�ng fragile.
    T?ng = 50 + 18 = 68.00
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("50")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("3")
    driver.find_element(*DESTINATION_SELECT).send_keys("international")
    driver.find_element(*TIER_SELECT).send_keys("standard")
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("0")
    driver.find_element(*CALCULATE_BUTTON).click()

    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # 50 + 18 = 68.00
    assert total_elem.text == "68.00"
    assert driver.find_element(*ERROR_OUTPUT).text == ""

# ----------------------------------------------------------------------
# 4?? Ki?m tra ph� tr?ng lu?ng trong kho?ng 5-20kg (th�m $10)
# ----------------------------------------------------------------------
def test_shipping_fee_weight_between_5_and_20(driver):
    """
    Subtotal=80, tier=standard, weight=10kg (domestic).
    Fee co b?n = 5 + 10 = 15, kh�ng fragile.
    T?ng = 80 + 15 = 95.00
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("80")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("10")
    driver.find_element(*DESTINATION_SELECT).send_keys("domestic")
    driver.find_element(*TIER_SELECT).send_keys("standard")
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("0")
    driver.find_element(*CALCULATE_BUTTON).click()

    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # 80 + 15 = 95.00
    assert total_elem.text == "95.00"
    assert driver.find_element(*ERROR_OUTPUT).text == ""

# ----------------------------------------------------------------------
# 5?? Ki?m tra ph� tr?ng lu?ng >20kg (th�m $25) v� ph� fragile (+7.5)
# ----------------------------------------------------------------------
def test_shipping_fee_heavy_and_fragile(driver):
    """
    Subtotal=200, tier=loyal, weight=25kg, destination=domestic, fragile=true.
    Discount = min(200*0.07,30)=14.
    Fee co b?n = 5 + 25 (tr?ng lu?ng) + 7.5 (fragile) = 37.5
    T?ng = 200 - 14 + 37.5 = 223.5 ? hi?n th? 223.50
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("200")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("25")
    driver.find_element(*DESTINATION_SELECT).send_keys("domestic")
    driver.find_element(*TIER_SELECT).send_keys("loyal")
    driver.find_element(*FRAGILE_CHECKBOX).click()          # d�nh d?u fragile
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("0")
    driver.find_element(*CALCULATE_BUTTON).click()

    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # 200 - 14 + 37.5 = 223.5 ? 223.50
    assert total_elem.text == "223.50"
    assert driver.find_element(*ERROR_OUTPUT).text == ""

# ----------------------------------------------------------------------
# 6?? Ki?m tra credit �m (gi?m t?ng)
# ----------------------------------------------------------------------
def test_negative_credit(driver):
    """
    Subtotal=100, tier=standard, weight=4kg (fee=5), credit=-5.
    T?ng = 100 - 0 + 5 - (-5) = 110.00
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("100")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("4")
    driver.find_element(*DESTINATION_SELECT).send_keys("domestic")
    driver.find_element(*TIER_SELECT).send_keys("standard")
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("-5")
    driver.find_element(*CALCULATE_BUTTON).click()

    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # 100 + 5 + 5 = 110.00
    assert total_elem.text == "110.00"
    assert driver.find_element(*ERROR_OUTPUT).text == ""

# ----------------------------------------------------------------------
# 7?? Ki?m tra tru?ng h?p subtotal �m � script n�m l?i v� total gi? gi� tr? m?c d?nh
# ----------------------------------------------------------------------
def test_subtotal_negative_keeps_default_total(driver):
    """
    Subtotal �m s? g�y l?i trong calculateDiscount, do d� h�m t�nh kh�ng thay d?i
    total (gi� tr? m?c d?nh 0.00) v� error kh�ng du?c c?p nh?t.
    """
    open_page(driver)

    driver.find_element(*SUBTOTAL_INPUT).clear()
    driver.find_element(*SUBTOTAL_INPUT).send_keys("-10")
    driver.find_element(*WEIGHT_INPUT).clear()
    driver.find_element(*WEIGHT_INPUT).send_keys("5")
    driver.find_element(*DESTINATION_SELECT).send_keys("domestic")
    driver.find_element(*TIER_SELECT).send_keys("standard")
    driver.find_element(*CREDIT_INPUT).clear()
    driver.find_element(*CREDIT_INPUT).send_keys("0")
    driver.find_element(*CALCULATE_BUTTON).click()

    total_elem = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(TOTAL_OUTPUT)
    )
    # V� l?i du?c n�m, total v?n gi? gi� tr? m?c d?nh 0.00
    assert total_elem.text == "0.00"
    # Kh�ng c� th�ng b�o l?i du?c ghi v�o element #error
    assert driver.find_element(*ERROR_OUTPUT).text == ""