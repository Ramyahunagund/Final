import os
from datetime import datetime

class ScreenshotUtils:

    @staticmethod
    def take_screenshot(driver, name="screenshot"):
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
        driver.save_screenshot(path)
        return path
