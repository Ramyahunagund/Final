# tests/conftest.py
import pytest
import time
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage

@pytest.fixture(scope="session", params=["chrome", "edge", "firefox"])
def logged_in_driver(request):
    browser_name = request.param
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=False)
    driver.get("https://www.demoblaze.com")
    login_page = LoginPage(driver)
    login_page.open_login_modal()
    login_page.enter_username("jane smith")
    login_page.enter_password("jane123")
    login_page.click_login()
    time.sleep(2)  # wait for login to complete
    yield driver
    driver.quit()
