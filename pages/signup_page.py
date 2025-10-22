from selenium.webdriver.common.by import By
from utilities.wait_utils import WaitUtils

class SignupPage:
    def __init__(self, driver):
        self.driver = driver
        self.signup_btn = (By.ID, "signin2")
        self.username_input = (By.ID, "sign-username")
        self.password_input = (By.ID, "sign-password")
        self.signup_submit = (By.XPATH, "//button[text()='Sign up']")

    def open_signup_modal(self):
        WaitUtils.wait_for_element_clickable(self.driver, self.signup_btn).click()

    def enter_signup_details(self, username, password):
        WaitUtils.wait_for_element_visible(self.driver, self.username_input).send_keys(username)
        WaitUtils.wait_for_element_visible(self.driver, self.password_input).send_keys(password)

    def submit_signup(self):
        WaitUtils.wait_for_element_clickable(self.driver, self.signup_submit).click()
