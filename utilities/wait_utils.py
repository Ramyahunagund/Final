from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WaitUtils:

    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=15):
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=15):
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
