import pytest
import os
from utils.config import BASE_URL
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras


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
            screenshots_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            # Save screenshot with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_file = os.path.join(screenshots_dir, f"{item.name}_{timestamp}.png")
            driver.save_screenshot(screenshot_file)

            # Adding screenshot to pytest-html report
            if hasattr(report, "extra"):
                report.extra.append(extras.image(screenshot_file, mime_type="image/png"))
            else:
                report.extra = [extras.image(screenshot_file, mime_type="image/png")]

