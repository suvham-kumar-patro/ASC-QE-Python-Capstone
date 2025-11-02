import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ----- Custom WebDriverWait -----
POLL_FREQUENCY = 0.5
IGNORED_EXCEPTIONS = (NoSuchElementException,)


class WebDriverWaitCustom:
    def __init__(self, driver, timeout, poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        self._driver = driver
        self._timeout = float(timeout)
        self._poll = poll_frequency or POLL_FREQUENCY
        self._ignored_exceptions = tuple(ignored_exceptions) if ignored_exceptions else IGNORED_EXCEPTIONS

    def until(self, method, message=""):
        end_time = time.monotonic() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions:
                pass
            if time.monotonic() > end_time:
                break
            time.sleep(self._poll)
        raise TimeoutException(message)


# ----- Test Setup -----
BASE_URL = "https://www.tatacliq.com/"


@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    print("🚀 Browser opened")
    yield driver
    driver.quit()
    print("🛑 Browser closed")


# ----- Helper to handle popup -----
def handle_popup(driver):
    time.sleep(5)
    try:
        popup_button = WebDriverWaitCustom(driver, 5).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="moe-dontallow_button"]'),
            "Popup button not found"
        )
        popup_button.click()
        print("✅ Popup closed by clicking 'Don't Allow'")
    except TimeoutException:
        print("ℹ️ No popup appeared, continuing...")


# ---------------- TEST 1: Open Homepage ----------------
@pytest.mark.ui
def test_open_homepage(driver):
    print("🏠 Opening homepage")
    driver.get(BASE_URL)
    handle_popup(driver)


# ---------------- TEST 2: Search ----------------
@pytest.mark.ui
def test_search(driver):
    print("🔍 Searching for 'Watch'")
    search_box = WebDriverWaitCustom(driver, 10).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='search-text-input']"),
        "Search box not found"
    )
    search_box.send_keys("Watch")

    # Click first suggestion
    first_suggestion = WebDriverWaitCustom(driver, 5).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="inside-search-wrapper"]/div[1]/div/div/span[1]'),
        "Search suggestion not found"
    )
    first_suggestion.click()


# ---------------- TEST 3: Apply Filter ----------------
@pytest.mark.ui
def test_apply_filter(driver):
    print("🔧 Applying Women filter")
    women_filter = WebDriverWaitCustom(driver, 10).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="l2FilterDiv-1"]/div[2]'),
        "Women filter not found"
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", women_filter)
    driver.execute_script("arguments[0].click();", women_filter)
    time.sleep(3)  # Wait for filtered results


# ---------------- TEST 4: Open First Product ----------------

# ---------------- TEST 4: Open First Product ----------------
# ---------------- TEST 4: Open First Product ----------------
@pytest.mark.ui
def test_open_first_product(driver):
    print("🛒 Opening first product")

    # Find the first product
    first_product = WebDriverWaitCustom(driver, 10).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="ProductModule-MP000000026545715"]/a/div'),
        "First product not found"
    )
    product_name = first_product.text

    # Scroll to and click the product
    driver.execute_script("arguments[0].scrollIntoView(true);", first_product)
    driver.execute_script("arguments[0].click();", first_product)

    # Wait for new tab to open
    WebDriverWaitCustom(driver, 10).until(
        lambda d: len(d.window_handles) > 1,
        "Product page tab did not open"
    )

    # Switch to new tab
    new_tab = driver.window_handles[1]
    driver.switch_to.window(new_tab)

    # Just wait a few seconds to ensure page loads
    time.sleep(10)

    # Close the product tab and switch back
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print(f"🔙 Closed product tab of '{product_name}' and returned to main page")
