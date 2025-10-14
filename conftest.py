import pytest
import os
from utils.config import BASE_URL
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras

# Screenshots directory
SCREENSHOTS_DIR = "reports/screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

@pytest.fixture(scope="function")
def driver(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get(BASE_URL)

    yield driver

    driver.quit()


# Hook to track test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            # checking if screenshot folder exists
            os.makedirs("screenshots", exist_ok=True)

            # Save screenshot with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.abspath(os.path.join("screenshots", f"{item.name}_{timestamp}.png"))
            driver.save_screenshot(screenshot_path)

            # Adding screenshot to pytest-html report
            if hasattr(report, "extra"):
                report.extra.append(extras.image(screenshot_path, mime_type="image/png"))
            else:
                report.extra = [extras.image(screenshot_path, mime_type="image/png")]

