import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.product_page import ProductPage
from pages.place_order_page import PlaceOrderPage

import os
import csv

# ---------------------------
# Function to read order data
# ---------------------------
def read_order_data_from_csv():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "..", "testdata", "order_data.csv")

    print(f"[Data] Reading order data from CSV: {file_path}")

    data_list = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append((
                row["name"],
                row["country"],
                row["city"],
                row["card"],
                row["month"],
                row["year"]
            ))
    print(f"[Data] Loaded {len(data_list)} order(s) from CSV.")
    return data_list


# ---------------------------
# Helper function to read cart table
# ---------------------------
def read_cart_table(driver):
    print("\n[Cart] Reading Cart Table Contents...")
    table_body = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tbodyid"))
    )

    timeout = time.time() + 10
    rows = []
    while time.time() < timeout:
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        if len(rows) > 0:
            break
        time.sleep(0.5)

    if len(rows) == 0:
        raise AssertionError("[Cart] Cart table is empty!")

    table_data = []
    for i, row in enumerate(rows, start=1):
        cols = row.find_elements(By.TAG_NAME, "td")
        item = [col.text for col in cols]
        table_data.append(item)
        print(f"[Cart] Row {i}: {item}")
    return table_data

# ---------------------------
# Test
# ---------------------------
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "name,country,city,card,month,year",
    read_order_data_from_csv()
)
def test_place_order(logged_in_driver, name, country, city, card, month, year):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)

    print(f"\n=== Starting Place Order Test for {name} ===")
    driver.get("https://www.demoblaze.com")
    driver.maximize_window()

    print("[Login] Using already logged-in session")

    # Step 1: Open a product
    print("[Step 1] Opening a product...")
    product_page = ProductPage(driver)
    product_page.open_product()
    time.sleep(1)

    # Step 2: Add product to cart
    print("[Step 2] Adding product to cart...")
    product_page.add_to_cart()

    # Step 3: Handle alert
    try:
        alert = wait.until(EC.alert_is_present())
        print(f"[Alert] Alert appeared with text: {alert.text}")
        alert.accept()
        print("[Alert] Alert accepted successfully.")
    except:
        print("[Alert] No alert appeared.")

    # Step 4: Go to Cart
    print("[Step 4] Navigating to Cart page...")
    cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cartur")))
    cart_link.click()

    # Step 4a: Read and verify cart table
    cart_items = read_cart_table(driver)
    assert len(cart_items) > 0, "[Cart] Cart is empty!"

    # Step 5: Click “Place Order”
    print("[Step 5] Clicking 'Place Order' button...")
    place_order_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']")))
    place_order_btn.click()

    # Step 6: Fill order details
    print(f"[Step 6] Filling order details for {name}...")
    place_order_page = PlaceOrderPage(driver)
    place_order_page.fill_order_details(name, country, city, card, month, year)
    time.sleep(1)

    # Step 7: Click “Purchase”
    print("[Step 7] Clicking 'Purchase' button...")
    purchase_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Purchase']")))
    purchase_btn.click()

    # Step 8: Capture confirmation
    confirmation_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(),'Thank you')]"))
    ).text
    print(f"[Step 8] Order Confirmation received: {confirmation_text}")

    print(f"✅ Place Order test completed successfully for {name}")
    print("=== Test Finished ===\n")
