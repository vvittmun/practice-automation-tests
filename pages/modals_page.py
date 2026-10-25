
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class ModalsPage(BasePage):
    URL = "https://practice-automation.com/modals/"

    SIMPLE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Simple Modal')]"
    )

    FORM_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Form Modal')]"
    )

    CLOSE_BUTTONS = (
        (By.XPATH, "//button[normalize-space(.)='×']"),
        (By.XPATH, "//*[self::button or self::a][contains(@class,'close')]"),
    )

    NAME_INPUT = (
        By.CSS_SELECTOR,
        "input[name*='name' i], input[placeholder*='name' i]"
    )

    EMAIL_INPUT = (
        By.CSS_SELECTOR,
        "input[type='email'], input[name*='email' i]"
    )

    MESSAGE_INPUT = (
        By.CSS_SELECTOR,
        "textarea, input[name*='message' i]"
    )

    def __init__(self, driver):
        super().__init__(driver, self.URL)

    def click_simple(self):
        self.clickable(self.SIMPLE_BUTTON).click()

    def click_form(self):
        self.clickable(self.FORM_BUTTON).click()

    def close_visible_modal(self):
        close_locators = (
            (By.XPATH, "//button[normalize-space(.)='×']"),
            (By.XPATH, "//button[normalize-space(.)='✕']"),
            (By.XPATH, "//button[normalize-space(.)='✖']"),
            (By.XPATH, "//*[@aria-label='Close' or @aria-label='close']"),
            (By.XPATH, "//*[contains(@class, 'pum-close')]"),
            (By.XPATH, "//*[contains(@class, 'close')]"),
        )

        for locator in close_locators:
            for element in self.driver.find_elements(*locator):
                if element.is_displayed() and element.is_enabled():
                    try:
                        element.click()
                        return True
                    except Exception:
                        continue

        self.driver.find_element(
            By.TAG_NAME, "body"
        ).send_keys(Keys.ESCAPE)

        return True

    def visible_modal_text(self):
        candidates = self.driver.find_elements(
            By.XPATH,
            "//*[contains(., \"Hi, I'm a simple modal\") "
            "or contains(., 'Please enter your contact info below.')]"
        )

        return [
            element.text
            for element in candidates
            if element.is_displayed() and element.text.strip()
        ]

    def fill_form(
        self,
        name="Test User",
        email="test@example.com",
        message="Selenium test"
    ):
        wait = WebDriverWait(self.driver, 10)

        fields = [
            ("name", self.NAME_INPUT, name),
            ("email", self.EMAIL_INPUT, email),
            ("message", self.MESSAGE_INPUT, message),
        ]

        for field_name, locator, value in fields:
            try:
                elements = wait.until(
                    lambda driver: [
                        element
                        for element in driver.find_elements(*locator)
                        if element.is_displayed() and element.is_enabled()
                    ]
                )

                field = elements[-1]
                field.clear()
                field.send_keys(value)

                actual_value = field.get_attribute("value")

                if actual_value is None:
                    actual_value = field.get_attribute("textContent")

                if actual_value != value:
                    print(
                        f"Поле: {field_name}, "
                        f"ожидалось: {value!r}, "
                        f"получено: {actual_value!r}, "
                        f"тег: {field.tag_name}, "
                        f"type: {field.get_attribute('type')}, "
                        f"name: {field.get_attribute('name')}, "
                        f"placeholder: {field.get_attribute('placeholder')}"
                    )
                    return False

            except Exception as error:
                print(f"Проблема с полем {field_name}: {error}")
                return False

        return True
