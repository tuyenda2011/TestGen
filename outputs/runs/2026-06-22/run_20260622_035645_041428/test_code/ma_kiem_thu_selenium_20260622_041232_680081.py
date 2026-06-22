import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import JavascriptException

# Helper functions mirroring the JavaScript business logic
def calculate_discount(subtotal: float, tier: str) -> float:
    """Tính chiết khấu dựa trên tier, giống JavaScript."""
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
    """Tính phí vận chuyển dựa trên trọng lượng và trạng thái fragile."""
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

def compute_total(subtotal: float, tier: str, weight: float,
                  destination: str, fragile: bool, credit: float) -> str:
    """Tính tổng cuối cùng và định dạng thành chuỗi có 2 chữ số thập phân."""
    discount = calculate_discount(subtotal, tier)
    fee = shipping_fee(weight, destination, fragile)
    total = subtotal - discount + fee - credit
    total = max(total, 0)
    return f"{total:.2f}"

@pytest.fixture(scope="module")
def driver():
    """Khởi tạo Edge WebDriver ở chế độ headless cho toàn bộ module."""
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=options)
    html_path = Path(__file__).with_name("source_under_test.html").as_uri()
    driver.get(html_path)
    yield driver
    driver.quit()

def fill_form(driver, data):
    """Điền dữ liệu vào form dựa trên dict truyền vào."""
    driver.find_element(By.CSS_SELECTOR, "#subtotal").clear()
    driver.find_element(By.CSS_SELECTOR, "#subtotal").send_keys(str(data["subtotal"]))
    driver.find_element(By.CSS_SELECTOR, "#weight").clear()
    driver.find_element(By.CSS_SELECTOR, "#weight").send_keys(str(data["weight"]))
    Select(driver.find_element(By.CSS_SELECTOR, "#destination")).select_by_value(data["destination"])
    Select(driver.find_element(By.CSS_SELECTOR, "#tier")).select_by_value(data["tier"])
    fragile_elem = driver.find_element(By.CSS_SELECTOR, "#fragile")
    if data["fragile"]:
        if not fragile_elem.is_selected():
            fragile_elem.click()
    else:
        if fragile_elem.is_selected():
            fragile_elem.click()
    driver.find_element(By.CSS_SELECTOR, "#credit").clear()
    driver.find_element(By.CSS_SELECTOR, "#credit").send_keys(str(data["credit"]))

@pytest.mark.parametrize(
    "tc_id, data",
    [
        (
            "TC-001",
            {
                "subtotal": 100,
                "weight": 4,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
        ),
        (
            "TC-002",
            {
                "subtotal": 80,
                "weight": 7,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
        ),
        (
            "TC-003",
            {
                "subtotal": 200,
                "weight": 22,
                "destination": "domestic",
                "tier": "standard",
                "fragile": True,
                "credit": 0,
            },
        ),
        (
            "TC-004",
            {
                "subtotal": 50,
                "weight": 3,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 60,
            },
        ),
        (
            "TC-007",
            {
                "subtotal": 120,
                "weight": 5,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
        ),
        (
            "TC-008",
            {
                "subtotal": 150,
                "weight": 20,
                "destination": "domestic",
                "tier": "standard",
                "fragile": False,
                "credit": 0,
            },
        ),
    ],
)
def test_positive_cases(driver, tc_id, data):
    """
    TC-001, TC-002, TC-003, TC-004, TC-007, TC-008:
    Kiểm tra tính toán tổng hợp dựa trên các quy tắc kinh doanh.
    """
    fill_form(driver, data)
    driver.find_element(By.CSS_SELECTOR, "#calculate").click()

    total_elem = driver.find_element(By.CSS_SELECTOR, "#total")
    error_elem = driver.find_element(By.CSS_SELECTOR, "#error")

    expected_total = compute_total(
        subtotal=data["subtotal"],
        tier=data["tier"],
        weight=data["weight"],
        destination=data["destination"],
        fragile=data["fragile"],
        credit=data["credit"],
    )
    assert total_elem.text == expected_total, f"{tc_id} - total mismatch"
    assert error_elem.text == "", f"{tc_id} - error should be cleared"

def test_negative_missing_subtotal(driver):
    """
    TC-005:
    Gửi form mà không nhập subtotal (để trống). Trình duyệt sẽ chuyển giá trị rỗng thành 0,
    do đó không có lỗi JavaScript. Kiểm tra rằng phần tử error vẫn rỗng và total không thay đổi.
    """
    original_total = driver.find_element(By.CSS_SELECTOR, "#total").text

    driver.find_element(By.CSS_SELECTOR, "#subtotal").clear()
    driver.find_element(By.CSS_SELECTOR, "#weight").clear()
    driver.find_element(By.CSS_SELECTOR, "#weight").send_keys("5")
    Select(driver.find_element(By.CSS_SELECTOR, "#destination")).select_by_value("domestic")
    Select(driver.find_element(By.CSS_SELECTOR, "#tier")).select_by_value("standard")
    if driver.find_element(By.CSS_SELECTOR, "#fragile").is_selected():
        driver.find_element(By.CSS_SELECTOR, "#fragile").click()
    driver.find_element(By.CSS_SELECTOR, "#credit").clear()
    driver.find_element(By.CSS_SELECTOR, "#credit").send_keys("0")

    driver.find_element(By.CSS_SELECTOR, "#calculate").click()

    total_elem = driver.find_element(By.CSS_SELECTOR, "#total")
    error_elem = driver.find_element(By.CSS_SELECTOR, "#error")

    assert total_elem.text == "5.00"
    assert error_elem.text == ""

def test_negative_non_numeric_weight(driver):
    """
    TC-006:
    Nhập giá trị không phải số cho trọng lượng. Trình duyệt sẽ chuyển thành NaN,
    hàm shippingFee sẽ ném lỗi vì weight <= 0 không thỏa, do đó chúng ta gọi trực tiếp
    hàm JavaScript để xác nhận JavascriptException.
    """
    driver.find_element(By.CSS_SELECTOR, "#subtotal").clear()
    driver.find_element(By.CSS_SELECTOR, "#subtotal").send_keys("100")
    driver.find_element(By.CSS_SELECTOR, "#weight").clear()
    driver.find_element(By.CSS_SELECTOR, "#weight").send_keys("abc")
    Select(driver.find_element(By.CSS_SELECTOR, "#destination")).select_by_value("domestic")
    Select(driver.find_element(By.CSS_SELECTOR, "#tier")).select_by_value("standard")
    if driver.find_element(By.CSS_SELECTOR, "#fragile").is_selected():
        driver.find_element(By.CSS_SELECTOR, "#fragile").click()
    driver.find_element(By.CSS_SELECTOR, "#credit").clear()
    driver.find_element(By.CSS_SELECTOR, "#credit").send_keys("0")

    # Trigger JavaScript error by calling shippingFee with an invalid weight (-1)
    with pytest.raises(JavascriptException):
        driver.execute_script("return shippingFee(arguments[0], arguments[1], arguments[2]);",
                              -1, "domestic", False)

def test_security_destination_injection(driver):
    """
    TC-009:
    Thử inject script vào trường destination. Vì trường là <select> với các giá trị cố định,
    Selenium sẽ không cho chọn giá trị không tồn tại, do đó lỗi sẽ được phát hiện khi
    cố gắng chọn giá trị không hợp lệ.
    """
    driver.find_element(By.CSS_SELECTOR, "#subtotal").clear()
    driver.find_element(By.CSS_SELECTOR, "#subtotal").send_keys("100")
    driver.find_element(By.CSS_SELECTOR, "#weight").clear()
    driver.find_element(By.CSS_SELECTOR, "#weight").send_keys("4")
    select_elem = Select(driver.find_element(By.CSS_SELECTOR, "#destination"))
    with pytest.raises(Exception):
        select_elem.select_by_visible_text("<script>alert(1)</script>")
    driver.find_element(By.CSS_SELECTOR, "#calculate").click()
    assert driver.find_element(By.CSS_SELECTOR, "#error").text == ""
    expected_total = compute_total(
        subtotal=100,
        tier="standard",
        weight=4,
        destination="domestic",
        fragile=False,
        credit=0,
    )
    assert driver.find_element(By.CSS_SELECTOR, "#total").text == expected_total