import allure
from pages.message_form_page import MessageFormPage


@allure.epic("Practice Automation")
@allure.feature("Message form")
@allure.title("Поле Message заполняется текстом элементов Automation Tools, полученных через Selenium")
def test_message_filled_from_automation_tools(driver):
    page = MessageFormPage(driver).open()
    message = page.fill_message_from_automation_tools()
    assert message
    assert ", " in message or len(message.split(",")) == 1
