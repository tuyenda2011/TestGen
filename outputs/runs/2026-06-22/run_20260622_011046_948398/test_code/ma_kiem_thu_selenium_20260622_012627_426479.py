import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import JavascriptException

def calculate_discount(subtotal: float, tier: str) -> float:
    """Tính chiết khấu dựa trên tier giống JavaScript."""
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
    """Tính phí vận chuyển dựa trên trọng lượng, địa điểm và tính fragile."""
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
    """Khởi tạo Edge WebDriver ở chế độ headless cho toàn bộ module."""
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=options)
    html = """
<!doctype html>
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
    driver.get("data:text/html;charset=utf-8," + html)
    yield driver
    driver.quit()

def fill_form(driver, data):
    """Điền dữ liệu vào form dựa trên dict input."""
    driver.find_element(By.CSS_SELECTOR, "#subtotal").clear()
    driver.find_element(By.CSS_SELECTOR, "#subtotal").send_keys(str(data.get("subtotal", "")))
    driver.find_element(By.CSS_SELECTOR, "#weight").clear()
    driver.find_element(By.CSS_SELECTOR, "#weight").send_keys(str(data.get("weight", "")))
    Select(driver.find_element(By.CSS_SELECTOR, "#destination")).select_by_value(data.get("destination", "domestic"))
    Select(driver.find_element(By.CSS_SELECTOR, "#tier")).select_by_value(data.get("tier", "standard"))
    fragile_elem = driver.find_element(By.CSS_SELECTOR, "#fragile")
    if data.get("fragile", False):
        if not fragile_elem.is_selected():
            fragile_elem.click()
    else:
        if fragile_elem.is_selected():
            fragile_elem.click()
    driver.find_element(By.CSS_SELECTOR, "#credit").clear()
    driver.find_element(By.CSS_SELECTOR, "#credit").send_keys(str(data.get("credit", "")))

@pytest.mark.parametrize(
    "case_id,input_data,expected_total",
    [
        (
            "TC-001",
            {
                "subtotal": 100,
                "weight": 10,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
            None,  # sẽ tính trong test
        ),
        (
            "TC-002",
            {
                "subtotal": 200,
                "weight": 25,
                "destination": "international",
                "tier": "vip",
                "fragile": True,
                "credit": 20,
            },
            None,
        ),
        (
            "TC-003",
            {
                "subtotal": 50,
                "weight": 5,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
            None,
        ),
        (
            "TC-004",
            {
                "subtotal": 80,
                "weight": 20,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
            None,
        ),
        (
            "TC-006",
            {
                "subtotal": 30,
                "weight": 2,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 100,
            },
            None,
        ),
    ],
)
def test_calculate_total(driver, case_id, input_data, expected_total):
    """Kiểm tra tính tổng cho các trường hợp hợp lệ và biên."""
    fill_form(driver, input_data)
    driver.find_element(By.CSS_SELECTOR, "#calculate").click()
    total_text = driver.find_element(By.CSS_SELECTOR, "#total").text
    error_text = driver.find_element(By.CSS_SELECTOR, "#error").text

    # Tính toán kỳ vọng dựa trên logic JavaScript
    subtotal = float(input_data["subtotal"])
    weight = float(input_data["weight"])
    destination = input_data["destination"]
    tier = input_data["tier"]
    fragile = input_data["fragile"]
    credit = float(input_data["credit"])

    discount = calculate_discount(subtotal, tier)
    fee = shipping_fee(weight, destination, fragile)
    raw_total = subtotal - discount + fee - credit
    expected = round(max(raw_total, 0), 2)

    assert error_text == "", f"{case_id}: error output should be empty"
    assert float(total_text) == expected, f"{case_id}: expected {expected:.2f}, got {total_text}"

def test_missing_subtotal(driver):
    """Kiểm tra hành vi khi subtotal để trống (sẽ được chuyển thành 0)."""
    data = {
        "subtotal": "",  # để trống
        "weight": 10,
        "destination": "domestic",
        "tier": "standard",
        "fragile": False,
        "credit": 0,
    }
    fill_form(driver, data)
    driver.find_element(By.CSS_SELECTOR, "#calculate").click()
    total_text = driver.find_element(By.CSS_SELECTOR, "#total").text
    error_text = driver.find_element(By.CSS_SELECTOR, "#error").text

    subtotal = 0.0
    weight = 10.0
    discount = calculate_discount(subtotal, data["tier"])
    fee = shipping_fee(weight, data["destination"], data["fragile"])
    expected = round(max(subtotal - discount + fee - 0, 0), 2)

    assert error_text == ""
    assert float(total_text) == expected

def test_negative_weight_exception(driver):
    """Kiểm tra rằng hàm shippingFee ném lỗi khi weight <= 0."""
    # Sử dụng execute_script để gọi trực tiếp hàm JS và bắt lỗi
    with pytest.raises(JavascriptException):
        driver.execute_script("return shippingFee(0, 'domestic', false);")