# Playwright Python Official Documentation (Comprehensive)

## 1. Core Concepts
Playwright supports both synchronous and asynchronous APIs.

**Sync API Example:**
```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://playwright.dev")
    expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")
    browser.close()
```

**Async API Example:**
```python
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        await expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")
        await browser.close()

asyncio.run(main())
```

## 2. Locators
Locators are the central piece of Playwright's auto-waiting and retry-ability.
- `page.get_by_role("button", name="Submit")`
- `page.get_by_text("Welcome")`
- `page.get_by_label("Password")`
- `page.get_by_placeholder("Search")`
- `page.get_by_test_id("submit-btn")`
- `page.locator("css=.submit")` or `page.locator("xpath=//button")`

### Actions
- `locator.fill("text")`
- `locator.click()`
- `locator.check()`
- `locator.select_option("value")`

## 3. Web-First Assertions
Playwright uses `expect` to automatically wait for conditions.
```python
expect(page.get_by_text("Success")).to_be_visible()
expect(page.locator(".status")).to_contain_text("OK")
expect(page.get_by_label("Subscribe")).to_be_checked()
expect(page.locator("button")).to_be_enabled()
expect(page).to_have_url("https://example.com/dashboard")
```
Negation:
```python
expect(page.locator(".loading")).not_to_be_visible()
```

## 4. Pytest Plugin (`pytest-playwright`)
Playwright provides built-in pytest fixtures: `page`, `context`, `browser`.
```python
import re
from playwright.sync_api import Page, expect

def test_homepage(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile(r"Playwright"))
```

## 5. Network Interception & Mocking
Playwright allows you to intercept network requests and mock responses using `page.route()`. This is critical for testing UI without hitting real backend APIs.

```python
from playwright.sync_api import Page

def test_mock_api(page: Page):
    # Intercept the API call and fulfill it with mock JSON
    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"users": [{"id": 1, "name": "Mock User"}]}'
        )

    # Route all matching requests to the handler
    page.route("**/api/users", handle_route)

    page.goto("https://example.com/users")
    
    # Assert that the mocked data is rendered on the screen
    expect(page.get_by_text("Mock User")).to_be_visible()
```
To block requests (e.g., images to speed up tests):
```python
page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
```

## 6. Handling Dialogs (Alerts, Confirms)
By default, Playwright automatically dismisses dialogs. To accept them, you must add an event listener.
```python
def test_dialog(page: Page):
    # Accept the next dialog automatically
    page.once("dialog", lambda dialog: dialog.accept("Optional text input"))
    page.get_by_role("button", name="Trigger Alert").click()
```

## 7. Handling Popups and New Windows
When a click opens a new tab, you must wait for it.
```python
with page.expect_popup() as popup_info:
    page.get_by_text("Open new tab").click()
popup = popup_info.value

popup.wait_for_load_state()
expect(popup).to_have_title("New Tab")
```

## 8. Waiting and Load States
Playwright auto-waits for elements to be actionable. However, sometimes you need manual waits.
- `page.wait_for_load_state("networkidle")`: Waits until there are no network connections for at least 500 ms.
- `page.wait_for_timeout(5000)`: Hard sleep (use sparingly).
- `page.wait_for_selector(".dynamic-element")`: Wait for a specific element.

## 9. Handling iFrames
To interact with elements inside an iframe, use `page.frame_locator()`.
```python
frame = page.frame_locator("iframe[name='payment']")
frame.get_by_label("Card Number").fill("1234")
```
