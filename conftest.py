import os
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver(request):
    options = Options()

    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(2)

    yield browser

    try:
        if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
            Path("screenshots").mkdir(parents=True, exist_ok=True)

            screenshot_path = Path("screenshots") / f"{request.node.name}.png"

            if browser.save_screenshot(str(screenshot_path)):
                allure.attach.file(
                    str(screenshot_path),
                    name=f"Failure - {request.node.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
