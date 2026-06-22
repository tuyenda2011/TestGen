from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_checkout_calculates_total(driver):
    fixture_url = (Path.cwd() / "source_under_test.html").resolve().as_uri()
    driver.get(fixture_url)

    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("6")
    driver.find_element(By.ID, "tier").send_keys("VIP")
    driver.find_element(By.ID, "fragile").click()
    driver.find_element(By.ID, "calculate").click()

    total = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='total']"))
    )
    assert total.text == "$100.50"
