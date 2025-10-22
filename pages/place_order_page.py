from selenium.webdriver.common.by import By
from utilities.wait_utils import WaitUtils

class PlaceOrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.place_order_btn = (By.XPATH, "//button[text()='Place Order']")
        self.name_input = (By.ID, "name")
        self.country_input = (By.ID, "country")
        self.city_input = (By.ID, "city")
        self.card_input = (By.ID, "card")
        self.month_input = (By.ID, "month")
        self.year_input = (By.ID, "year")
        self.purchase_btn = (By.XPATH, "//button[text()='Purchase']")

    def open_place_order_modal(self):
        WaitUtils.wait_for_element_clickable(self.driver, self.place_order_btn).click()

    def fill_order_details(self, name, country, city, card, month, year):
        WaitUtils.wait_for_element_visible(self.driver, self.name_input).send_keys(name)
        WaitUtils.wait_for_element_visible(self.driver, self.country_input).send_keys(country)
        WaitUtils.wait_for_element_visible(self.driver, self.city_input).send_keys(city)
        WaitUtils.wait_for_element_visible(self.driver, self.card_input).send_keys(card)
        WaitUtils.wait_for_element_visible(self.driver, self.month_input).send_keys(month)
        WaitUtils.wait_for_element_visible(self.driver, self.year_input).send_keys(year)

    def place_order(self):
        WaitUtils.wait_for_element_clickable(self.driver, self.purchase_btn).click()
        # Accept alert if present
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception:
            pass
