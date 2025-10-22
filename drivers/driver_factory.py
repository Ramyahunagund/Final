from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class DriverFactory:

    EDGE_PATH = r"C:\WebDrivers\Edge\msedgedriver.exe"
    FIREFOX_PATH = r"C:\WebDrivers\Firefox\geckodriver.exe"

    @staticmethod
    def get_driver(browser_name="chrome", headless=False):
        browser_name = browser_name.lower()
        driver = None

        if browser_name == "chrome":
            options = ChromeOptions()
            options.headless = headless
            driver = webdriver.Chrome(options=options)  # Uses system ChromeDriver automatically

        elif browser_name == "edge":
            options = EdgeOptions()
            options.headless = headless
            service = EdgeService(DriverFactory.EDGE_PATH)
            driver = webdriver.Edge(service=service, options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.headless = headless
            service = FirefoxService(DriverFactory.FIREFOX_PATH)
            driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Browser '{browser_name}' is not supported. Choose Chrome, Edge, or Firefox.")

        driver.maximize_window()
        return driver
