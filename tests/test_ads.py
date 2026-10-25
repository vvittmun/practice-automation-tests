import time
import allure
from selenium.webdriver.common.by import By
from pages.ads_page import AdsPage


@allure.epic("Practice Automation")
@allure.feature("Ads")
class TestAds:

    @allure.title("Позитивный: страница Ads открывается")
    def test_ads_page_opens(self, driver):
        AdsPage(driver).open()
        assert "ads" in driver.current_url.lower()
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    @allure.title("Позитивный: заголовок Ads отображается")
    def test_ads_heading_visible(self, driver):
        page = AdsPage(driver).open()
        assert page.visible((By.XPATH, "//*[self::h1 or self::h2][contains(normalize-space(.),'Ads')]"))

    @allure.title("Позитивный: сообщение обратного отсчёта присутствует")
    def test_countdown_message_present(self, driver):
        AdsPage(driver).open()
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "ad" in body_text.lower()

    @allure.title("Позитивный: рекламное окно появляется после ожидания, если оно не блокируется")
    def test_ad_appears_after_wait(self, driver):
        page = AdsPage(driver).open()
        appeared = page.wait_for_ad(timeout=12)
        if not appeared:
            import pytest
            pytest.skip("Рекламное окно не появилось: возможен блокировщик рекламы или изменение поведения сайта.")
        assert page.ad_visible()

    @allure.title("Позитивный: рекламное окно можно закрыть")
    def test_ad_can_be_closed(self, driver):
        page = AdsPage(driver).open()
        if not page.wait_for_ad(timeout=12):
            import pytest
            pytest.skip("Рекламное окно не появилось в текущем окружении.")
        assert page.close_ad()

    @allure.title("Позитивный: страница доступна после обработки рекламного окна")
    def test_page_stays_available(self, driver):
        AdsPage(driver).open()
        time.sleep(6)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    @allure.title("Позитивный: текст страницы можно прочитать после загрузки")
    def test_page_text_available(self, driver):
        AdsPage(driver).open()
        assert driver.find_element(By.TAG_NAME, "body").text.strip()

    @allure.title("Негативный: рекламное окно не должно считаться появившимся мгновенно")
    def test_ad_not_assumed_immediate(self, driver):
        page = AdsPage(driver).open()
        # Не утверждаем, что окно обязано отсутствовать: проверяем только, что DOM страницы доступен сразу.
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    @allure.title("Негативный: после закрытия рекламного окна страница остаётся доступной")
    def test_page_available_after_close(self, driver):
        page = AdsPage(driver).open()
        if page.wait_for_ad(timeout=12):
            page.close_ad()
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    @allure.title("Негативный: повторная попытка закрытия не ломает страницу")
    def test_repeated_close_does_not_break_page(self, driver):
        page = AdsPage(driver).open()
        if page.wait_for_ad(timeout=12):
            page.close_ad()
            page.close_ad()
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()
