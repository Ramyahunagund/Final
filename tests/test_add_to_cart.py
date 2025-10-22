import pytest
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.product_page import ProductPage
from pages.login_page import LoginPage

@pytest.mark.order(3)
def test_add_to_cart(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    print("\n=== Starting Add to Cart Test ===")
    driver.get("https://www.demoblaze.com")
    driver.maximize_window()

    print("[Login] Using already logged-in session")

    # 🔹 FEATURE 1: List first 5 products on homepage
    print("[Feature] Loading products...")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tbodyid .hrefch")))
    items = driver.find_elements(By.CSS_SELECTOR, "#tbodyid .hrefch")
    print(f"[Feature] Total products found: {len(items)}")
    for i, item in enumerate(items[:5], start=1):
        print(f"  Product {i}: {item.text}")

    # 🔹 FEATURE 2: Open first product
    product_page = ProductPage(driver)
    print("[Step] Opening first product...")
    product_page.open_product()
    time.sleep(1)

    # 🔹 FEATURE 3: Scroll down on product page
    driver.execute_script("window.scrollBy(0, 500);")
    print("[Feature] Scrolled down 500px.")
    time.sleep(1)

    # 🔹 FEATURE 4: Add to Cart and handle Alert
    print("[Feature] Adding product to cart...")
    product_page.add_to_cart()
    try:
        alert = wait.until(EC.alert_is_present())
        print(f"[Alert] Alert text: {alert.text}")
        alert.accept()
        print("[Alert] Alert accepted successfully.")
    except:
        print("[Alert] No alert appeared.")

    # 🔹 FEATURE 5: Drag & Drop Simulation
    try:
        logo = driver.find_element(By.ID, "nava")
        actions.drag_and_drop_by_offset(logo, 20, 0).perform()
        print("[Feature] Drag action performed on logo.")
    except Exception as e:
        print("[Feature] Drag simulation skipped:", e)

    # 🔹 FEATURE 6: Right Click (context click)
    try:
        actions.context_click(logo).perform()
        print("[Feature] Right-click action performed on logo.")
    except Exception as e:
        print("[Feature] Right-click failed:", e)

    # 🔹 FEATURE 7: Window Handling
    print("[Feature] Opening new window and switching...")
    main_window = driver.current_window_handle
    driver.execute_script("window.open('https://www.demoblaze.com/about.html', '_blank');")
    time.sleep(2)
    all_windows = driver.window_handles
    for win in all_windows:
        if win != main_window:
            driver.switch_to.window(win)
            print("[Window Handling] Switched to About Us page.")
            time.sleep(1)
            driver.close()
            print("[Window Handling] Closed About Us page window.")
            break
    driver.switch_to.window(main_window)
    print("[Window Handling] Back to main window.")

    # 🔹 FEATURE 8: Go to Cart page
    cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cartur")))
    cart_link.click()
    print("[Feature] Navigated to Cart page.")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("[Feature] Scrolled to bottom of cart page.")

    print("✅ Add to Cart test executed with all advanced Selenium features.")
    print("=== Test Completed ===\n")
