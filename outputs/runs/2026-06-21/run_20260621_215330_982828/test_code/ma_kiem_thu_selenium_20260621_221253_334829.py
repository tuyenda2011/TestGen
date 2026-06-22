import pytest
import urllib.parse
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

HTML_CONTENT = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Checkout Quote Demo</title>
</head>
<body>
  <main>
    <h1>Checkout Quote</h1>
    <form id="quote-form">
      <label>
        Subtotal
        <input id="subtotal" name="subtotal" type="number" step="0.01" value="100">
      </label>
      <label>
        Weight
        <input id="weight" name="weight" type="number" step="0.01" value="6">
      </label>
      <label>
        Destination
        <select id="destination" name="destination">
          <option value="domestic">Domestic</option>
          <option value="international">International</option>
        </select>
      </label>
      <label>
        Tier
        <select id="tier" name="tier">
          <option value="standard">Standard</option>
          <option value="loyal">Loyal</option>
          <option value="vip">VIP</option>
        </select>
      </label>
      <label>
        Fragile
        <input id="fragile" name="fragile" type="checkbox">
      </label>
      <label>
        Store credit
        <input id="credit" name="credit" type="number" step="0.01" value="0">
      </label>
      <button id="calculate" type="submit">Calculate</button>
    </form>
    <output id="total" data-testid="total">0.00</output>
    <output id="error" data-testid="error"></output>
  </main>
  <script>
    function calculateDiscount(subtotal, tier) {
      if (subtotal < 0) throw new Error("subtotal must not be negative");
      if (tier === "vip") return Math.min(subtotal * 0.12, 50);
      if (tier === "loyal") return Math.min(subtotal * 0.07, 30);
      if (tier === "standard") return 0;
      throw new Error("unsupported customer tier");
    }

    function shippingFee(weight, destination, fragile) {
      if (weight <= 0) throw new Error("weight must be greater than zero");
      let fee = destination === "domestic" ? 5 : 18;
      if (weight > 20) fee += 25;
      else if (weight > 5) fee += 10;
      if (fragile) fee += 7.5;
      return fee;
    }

    document.getElementById("quote-form").addEventListener("submit", function (event) {
      event.preventDefault();
      const subtotal = Number(document.getElementById("subtotal").value);
      const weight = Number(document.getElementById("weight").value);
      const destination = document.getElementById("destination").value;
      const tier = document.getElementById("tier").value;
      const fragile = document.getElementById("fragile").checked;
      const credit = Number(document.getElementById("credit").value);
      const total = subtotal - calculateDiscount(subtotal, tier) + shippingFee(weight, destination, fragile) - credit;
      document.getElementById("total").textContent = Math.max(total, 0).toFixed(2);
      document.getElementById("error").textContent = "";
    });
  </script>
</body>
</html>
"""

def calculate_discount(subtotal: float, tier: str) -> float:
    """Tính giảm giá dựa trên tier, giống JavaScript."""
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    if tier == "vip":
        return min(subtotal * 0.12, 50)
    if tier == "loyal":
        return min(subtotal * 0.07, 30)
    if tier == "standard":
        return 0.0
    raise ValueError("unsupported customer tier")

def shipping_fee(weight: float, destination: str, fragile: bool) -> float:
    """Tính phí vận chuyển dựa trên trọng lượng, địa điểm và fragile."""
    if weight <= 0:
        raise ValueError("weight must be greater than zero")
    fee = 5 if destination == "domestic" else 18
    if weight > 20:
        fee += 25
    elif weight > 5:
        fee += 10
    if fragile:
        fee += 7.5
    return fee

@pytest.fixture(scope="module")
def driver():
    """Khởi tạo Edge driver ở chế độ headless cho toàn bộ module."""
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=options)
    data_url = "data:text/html;charset=utf-8," + urllib.parse.quote(HTML_CONTENT)
    driver.get(data_url)
    yield driver
    driver.quit()

def fill_form(driver, subtotal, weight, destination, tier, fragile, credit):
    """Điền dữ liệu vào form."""
    driver.find_element(By.ID, "subtotal").clear()
    driver.find_element(By.ID, "subtotal").send_keys(str(subtotal))
    driver.find_element(By.ID, "weight").clear()
    driver.find_element(By.ID, "weight").send_keys(str(weight))
    dest_elem = driver.find_element(By.ID, "destination")
    for opt in dest_elem.find_elements(By.TAG_NAME, "option"):
        if opt.get_attribute("value") == destination:
            opt.click()
            break
    tier_elem = driver.find_element(By.ID, "tier")
    for opt in tier_elem.find_elements(By.TAG_NAME, "option"):
        if opt.get_attribute("value") == tier:
            opt.click()
            break
    fragile_chk = driver.find_element(By.ID, "fragile")
    if fragile_chk.is_selected() != fragile:
        fragile_chk.click()
    driver.find_element(By.ID, "credit").clear()
    driver.find_element(By.ID, "credit").send_keys(str(credit))
    driver.find_element(By.ID, "calculate").click()

@pytest.mark.parametrize(
    "subtotal,weight,destination,tier,fragile,credit,expected_total",
    [
        # TC-001: normal weight, non‑fragile, no credit, tier discount (standard)
        (100, 4, "domestic", "standard", False, 0,
         round(max(100 - calculate_discount(100, "standard") + shipping_fee(4, "domestic", False) - 0, 0), 2)),
        # TC-002: heavy weight, fragile, with credit, tier discount (vip)
        (200, 25, "international", "vip", True, 30,
         round(max(200 - calculate_discount(200, "vip") + shipping_fee(25, "international", True) - 30, 0), 2)),
        # TC-003: weight exactly 5 (threshold), non‑fragile, tier (standard)
        (50, 5, "domestic", "standard", False, 0,
         round(max(50 - calculate_discount(50, "standard") + shipping_fee(5, "domestic", False) - 0, 0), 2)),
        # TC-004: weight exactly 20 (threshold), non‑fragile, tier (standard)
        (80, 20, "domestic", "standard", False, 0,
         round(max(80 - calculate_discount(80, "standard") + shipping_fee(20, "domestic", False) - 0, 0), 2)),
    ]
)
def test_calculate_total_positive(driver, subtotal, weight, destination, tier, fragile, credit, expected_total):
    """Kiểm tra tính tổng cho các trường hợp dương, bao gồm các ngưỡng trọng lượng."""
    fill_form(driver, subtotal, weight, destination, tier, fragile, credit)
    total_text = driver.find_element(By.ID, "total").text
    error_text = driver.find_element(By.ID, "error").text
    assert total_text == f"{expected_total:.2f}"
    assert error_text == ""

def test_error_cleared_after_success(driver):
    """Kiểm tra thông báo lỗi trước đó được xóa khi tính toán thành công."""
    # Đặt lỗi giả
    driver.execute_script("document.getElementById('error').textContent = 'Invalid input';")
    # Thực hiện tính toán hợp lệ
    fill_form(driver, 60, 3, "domestic", "standard", False, 0)
    total_text = driver.find_element(By.ID, "total").text
    error_text = driver.find_element(By.ID, "error").text
    expected = round(max(60 - calculate_discount(60, "standard") + shipping_fee(3, "domestic", False) - 0, 0), 2)
    assert total_text == f"{expected:.2f}"
    assert error_text == ""