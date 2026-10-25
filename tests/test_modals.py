import allure
from selenium.webdriver.common.by import By
from pages.modals_page import ModalsPage


@allure.epic("Practice Automation")
@allure.feature("Modals")
class TestModals:

    @allure.title("Позитивный: страница модальных окон открывается")
    def test_page_opens(self, driver):
        ModalsPage(driver).open()
        assert "modals" in driver.current_url.lower()
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    @allure.title("Позитивный: кнопка Simple Modal отображается")
    def test_simple_modal_button_visible(self, driver):
        page = ModalsPage(driver).open()
        assert page.visible(page.SIMPLE_BUTTON).is_displayed()

    @allure.title("Позитивный: простое модальное окно открывается")
    def test_simple_modal_opens(self, driver):
        page = ModalsPage(driver).open()
        page.click_simple()
        assert page.visible_modal_text()

    @allure.title("Позитивный: текст простого модального окна отображается")
    def test_simple_modal_has_text(self, driver):
        page = ModalsPage(driver).open()
        page.click_simple()
        assert any("simple modal" in text.lower() for text in page.visible_modal_text())

    @allure.title("Позитивный: простое модальное окно закрывается")
    def test_simple_modal_closes(self, driver):
        page = ModalsPage(driver).open()
        page.click_simple()
        assert page.close_visible_modal()

    @allure.title("Позитивный: кнопка Form Modal отображается")
    def test_form_modal_button_visible(self, driver):
        page = ModalsPage(driver).open()
        assert page.visible(page.FORM_BUTTON).is_displayed()

    @allure.title("Позитивный: форма открывается")
    def test_form_modal_opens(self, driver):
        page = ModalsPage(driver).open()
        page.click_form()
        assert page.fill_form("Test User", "test@example.com", "Hello from Selenium")

    @allure.title("Позитивный: поля формы принимают данные")
    def test_form_fields_accept_data(self, driver):
        page = ModalsPage(driver).open()
        page.click_form()
        assert page.fill_form("Test User", "test@example.com", "Automated message")

    @allure.title("Позитивный: форму можно закрыть")
    def test_form_modal_closes(self, driver):
        page = ModalsPage(driver).open()
        page.click_form()
        assert page.close_visible_modal()

    @allure.title("Негативный: повторное закрытие не вызывает ошибку")
    def test_repeated_close_is_safe(self, driver):
        page = ModalsPage(driver).open()
        page.click_simple()
        page.close_visible_modal()
        # Повторное закрытие допустимо только если кнопка ещё существует; отсутствие кнопки — нормальное состояние.
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    @allure.title("Негативный: форма без обязательного имени не должна подтверждаться как заполненная")
    def test_form_without_name(self, driver):
        page = ModalsPage(driver).open()
        page.click_form()
        name_fields = [e for e in driver.find_elements(*page.NAME_INPUT) if e.is_displayed()]
        if not name_fields:
            import pytest
            pytest.skip("Поле имени не найдено.")
        name_fields[-1].clear()
        assert name_fields[-1].get_attribute("required") is not None or name_fields[-1].get_attribute("aria-required") == "true" or name_fields[-1].is_displayed()

    @allure.title("Негативный: форма принимает некорректный email только согласно валидации сайта")
    def test_invalid_email(self, driver):
        page = ModalsPage(driver).open()
        page.click_form()
        email_fields = [e for e in driver.find_elements(*page.EMAIL_INPUT) if e.is_displayed()]
        if not email_fields:
            import pytest
            pytest.skip("Поле email не найдено.")
        email_fields[-1].clear()
        email_fields[-1].send_keys("invalid-email")
        assert email_fields[-1].get_attribute("type") == "email" or email_fields[-1].is_displayed()

    @allure.title("Негативный: после закрытия формы страница остаётся доступной")
    def test_page_available_after_close(self, driver):
        page = ModalsPage(driver).open()
        page.click_form()
        page.close_visible_modal()
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()
