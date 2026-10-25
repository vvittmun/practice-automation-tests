
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class AdsPage(BasePage):
    URL = "https://practice-automation.com/ads/"

    AD_TEXT = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'I am an ad.')]"
    )

    CLOSE_BUTTONS = (
        (By.XPATH, "//button[normalize-space(.)='×']"),
        (By.XPATH, "//button[normalize-space(.)='✕']"),
        (By.XPATH, "//button[normalize-space(.)='✖']"),
        (By.XPATH, "//*[@aria-label='Close' or @aria-label='close']"),
        (By.XPATH, "//*[contains(@class, 'pum-close')]"),
        (By.XPATH, "//*[contains(@class, 'close')]"),
    )

    def __init__(self, driver):
        super().__init__(driver, self.URL)

    def ad_visible(self):
        return any(
            element.is_displayed()
            for element in self.driver.find_elements(*self.AD_TEXT)
        )

    def wait_for_ad(self, timeout=12):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: any(
                    element.is_displayed()
                    for element in d.find_elements(*self.AD_TEXT)
                )
            )
            return True
        except TimeoutException:
            return False



    def close_ad(self):
        close_locator = (
            By.CSS_SELECTOR,
            "button.pum-close.popmake-close"
        )

        buttons = self.driver.find_elements(*close_locator)

        for button in buttons:
            if not button.is_displayed() or not button.is_enabled():
                continue

            try:
                button.click()

                WebDriverWait(self.driver, 5).until(
                    lambda d: not any(
                        element.is_displayed()
                        for element in d.find_elements(
                            By.CSS_SELECTOR,
                            ".pum-overlay.pum-active"
                        )
                    )
                )

                return True

            except Exception:
                continue

        self.driver.find_element(
            By.TAG_NAME, "body"
        ).send_keys(Keys.ESCAPE)

        try:
            WebDriverWait(self.driver, 3).until(
                lambda d: not any(
                    element.is_displayed()
                    for element in d.find_elements(
                        By.CSS_SELECTOR,
                        ".pum-overlay.pum-active"
                    )
                )
            )
            return True
        except TimeoutException:
            return False


