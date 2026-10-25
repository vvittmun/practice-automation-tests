from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CalendarPage(BasePage):
    URL = "https://practice-automation.com/calendars/"

    # Эти локаторы намеренно допускают несколько распространённых реализаций календаря.
    DATE_INPUTS = (
        (By.CSS_SELECTOR, 'input[type="date"]'),
        (By.CSS_SELECTOR, 'input[type="datetime-local"]'),
        (By.CSS_SELECTOR, 'input[placeholder*="date" i]'),
        (By.CSS_SELECTOR, 'input[name*="date" i]'),
        (By.CSS_SELECTOR, 'input[id*="date" i]'),
    )
    CALENDAR_WIDGETS = (
        (By.CSS_SELECTOR, '[class*="calendar" i]'),
        (By.CSS_SELECTOR, '[id*="calendar" i]'),
        (By.CSS_SELECTOR, 'input[type="date"]'),
        (By.CSS_SELECTOR, 'input[type="datetime-local"]'),
    )

    def __init__(self, driver):
        super().__init__(driver, self.URL)

    def date_inputs(self):
        found = []
        for locator in self.DATE_INPUTS:
            for element in self.driver.find_elements(*locator):
                if element.is_displayed() and element not in found:
                    found.append(element)
        return found


    def calendar_elements(self):
        # На странице может быть поле даты без отдельного
        # элемента с классом calendar.
        found = self.date_inputs()

        if found:
            return found

        # Запасной вариант — поле, расположенное после подписи даты.
        locator = (
            By.XPATH,
            "//*[contains(normalize-space(.), "
            "'Select or enter a date')]/following::input[1]"
        )

        return [
            element
            for element in self.driver.find_elements(*locator)
            if element.is_displayed()
        ]

