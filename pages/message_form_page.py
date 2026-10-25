
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MessageFormPage(BasePage):
    URL = "https://practice-automation.com/form-fields/"

    TOOL_ITEMS = (
        (
            By.XPATH,
            "//li[normalize-space(.)='Selenium' "
            "or normalize-space(.)='Playwright' "
            "or normalize-space(.)='Cypress' "
            "or normalize-space(.)='Appium' "
            "or normalize-space(.)='Katalon Studio']"
        ),
    )

    MESSAGE = (
        By.XPATH,
        "//textarea"
    )

    def __init__(self, driver):
        super().__init__(driver, self.URL)

    def get_automation_tools_text(self):
        for locator in self.TOOL_ITEMS:
            elements = [
                e for e in self.driver.find_elements(*locator)
                if e.is_displayed()
            ]
            values = [e.text.strip() for e in elements if e.text.strip()]
            if values:
                return values
        return []

    def fill_message_from_automation_tools(self):
        items = self.get_automation_tools_text()

        if not items:
            raise AssertionError(
                "Не найдены элементы Automation tools на странице Form Fields."
            )

        message = ", ".join(items)

        fields = [
            e for e in self.driver.find_elements(*self.MESSAGE)
            if e.is_displayed()
        ]

        if not fields:
            raise AssertionError("Не найдено поле Message.")

        fields[-1].clear()
        fields[-1].send_keys(message)

        return message
