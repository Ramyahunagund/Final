from selenium.webdriver.common.by import By
from utilities.wait_utils import WaitUtils
from utilities.js_utils import JSUtils

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_link = (By.LINK_TEXT, "Samsung galaxy s6")
        self.add_to_cart_btn = (By.LINK_TEXT, "Add to cart")

    def open_product(self):
        product = WaitUtils.wait_for_element_visible(self.driver, self.product_link)
        JSUtils.scroll_into_view(self.driver, product)
        product.click()

    def add_to_cart(self):
        btn = WaitUtils.wait_for_element_clickable(self.driver, self.add_to_cart_btn)
        JSUtils.click_element(self.driver, btn)
