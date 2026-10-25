import pytest
import allure
from pages.calendar_page import CalendarPage


@allure.epic("Practice Automation")
@allure.feature("Calendar")
class TestCalendar:

    @allure.title("Позитивный: страница календаря открывается")
    def test_calendar_page_opens(self, driver):
        page = CalendarPage(driver).open()
        assert "calendars" in driver.current_url.lower()
        assert driver.title.strip()

    @allure.title("Позитивный: на странице присутствует календарный элемент или поле даты")
    def test_calendar_control_is_present(self, driver):
        page = CalendarPage(driver).open()
        assert page.calendar_elements(), "Не найден календарный элемент. Уточните локатор после осмотра страницы."

    @allure.title("Позитивный: поле даты доступно для чтения")
    def test_date_field_can_be_read(self, driver):
        page = CalendarPage(driver).open()
        inputs = page.date_inputs()
        if not inputs:
            pytest.skip("На странице не обнаружено стандартного поля даты; проверьте фактическую реализацию календаря.")
        assert inputs[0].is_displayed()

    @allure.title("Позитивный: поле даты принимает корректную дату, если оно редактируемое")
    def test_valid_date_input(self, driver):
        page = CalendarPage(driver).open()
        inputs = page.date_inputs()
        if not inputs:
            pytest.skip("Редактируемое поле даты не найдено.")
        field = inputs[0]
        if field.get_attribute("readonly") is not None or field.get_attribute("disabled") is not None:
            pytest.skip("Поле даты не редактируется напрямую.")
        field.clear()
        field.send_keys("2026-10-24")
        assert field.get_attribute("value") in ("2026-10-24", "2026-10-24T00:00")

    @allure.title("Позитивный: повторный ввод даты не ломает страницу")
    def test_date_can_be_changed(self, driver):
        page = CalendarPage(driver).open()
        inputs = page.date_inputs()
        if not inputs:
            pytest.skip("Редактируемое поле даты не найдено.")
        field = inputs[0]
        if field.get_attribute("readonly") is not None or field.get_attribute("disabled") is not None:
            pytest.skip("Поле даты не редактируется напрямую.")
        field.clear()
        field.send_keys("2026-10-24")
        field.clear()
        field.send_keys("2026-10-25")
        assert field.get_attribute("value").startswith("2026-10-25")

    @allure.title("Позитивный: календарная страница остаётся доступной после взаимодействия")
    def test_page_remains_loaded(self, driver):
        CalendarPage(driver).open()
        assert driver.find_element("tag name", "body").is_displayed()

    @allure.title("Позитивный: календарные элементы не скрыты")
    def test_visible_calendar_elements(self, driver):
        page = CalendarPage(driver).open()
        elements = page.calendar_elements()
        assert elements
        assert any(e.is_displayed() for e in elements)

    @allure.title("Негативный: некорректный формат даты не вызывает падения страницы")
    def test_invalid_date_format(self, driver):
        page = CalendarPage(driver).open()
        inputs = page.date_inputs()
        if not inputs:
            pytest.skip("Нет стандартного поля даты для негативной проверки.")
        field = inputs[0]
        if field.get_attribute("type") == "date" or field.get_attribute("readonly") is not None:
            pytest.skip("Браузерное поле date не позволяет надёжно проверить произвольный текст.")
        field.clear()
        field.send_keys("not-a-date")
        assert driver.find_element("tag name", "body").is_displayed()

    @allure.title("Негативный: невозможная дата не приводит к ошибке приложения")
    def test_impossible_date(self, driver):
        page = CalendarPage(driver).open()
        inputs = page.date_inputs()
        if not inputs:
            pytest.skip("Нет стандартного поля даты для негативной проверки.")
        field = inputs[0]
        if field.get_attribute("type") == "date" or field.get_attribute("readonly") is not None:
            pytest.skip("Нативный date input ограничивает ввод браузером.")
        field.clear()
        field.send_keys("2026-02-31")
        assert driver.find_element("tag name", "body").is_displayed()

    @allure.title("Негативный: пустое значение поля даты не ломает страницу")
    def test_empty_date(self, driver):
        page = CalendarPage(driver).open()
        inputs = page.date_inputs()
        if not inputs:
            pytest.skip("Нет стандартного поля даты для негативной проверки.")
        field = inputs[0]
        if field.get_attribute("readonly") is not None:
            pytest.skip("Поле даты нельзя редактировать напрямую.")
        field.clear()
        assert driver.find_element("tag name", "body").is_displayed()
