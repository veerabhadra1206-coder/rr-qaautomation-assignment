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
            # Create folder: reports/screenshots
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(file_path)

            # Attach to HTML report 
            relative_path = f"screenshots/{file_name}"

            # Adding screenshot to pytest-html report
            if hasattr(report, "extra"):
                report.extra.append(extras.image(relative_path, mime_type="image/png"))
            else:
                report.extra = [extras.image(relative_path, mime_type="image/png")]

