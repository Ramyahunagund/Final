class JSUtils:

    @staticmethod
    def scroll_into_view(driver, element):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

    @staticmethod
    def click_element(driver, element):
        driver.execute_script("arguments[0].click();", element)
