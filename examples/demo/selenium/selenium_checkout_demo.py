import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def _demo_url() -> str:
    configured = os.environ.get("CHECKOUT_DEMO_URL")
    if configured:
        return configured
    return (Path(__file__).with_name("ui_checkout_fixture.html")).resolve().as_uri()


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_selenium_checkout_vip_domestic_total(driver) -> None:
    driver.get(_demo_url())

    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("6")
    Select(driver.find_element(By.ID, "destination")).select_by_value("domestic")
    Select(driver.find_element(By.ID, "tier")).select_by_value("vip")
    driver.find_element(By.ID, "fragile").click()
    driver.find_element(By.ID, "credit").clear()
    driver.find_element(By.ID, "credit").send_keys("10")
    driver.find_element(By.ID, "calculate").click()

    total = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "total"), "100.50")
    )
    assert total is True


def test_selenium_checkout_boundary_without_weight_surcharge(driver) -> None:
    driver.get(_demo_url())

    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys("100")
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys("5")
    Select(driver.find_element(By.ID, "destination")).select_by_value("domestic")
    Select(driver.find_element(By.ID, "tier")).select_by_value("standard")
    driver.find_element(By.ID, "calculate").click()

    assert driver.find_element(By.ID, "total").text == "105.00"
