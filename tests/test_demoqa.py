import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from drivers.driver_factory import DriverFactory

# -----------------------------
# Helper: remove floating ads
# -----------------------------
def remove_ads(driver):
    driver.execute_script("""
    var adFrames = document.querySelectorAll('iframe[src*="safeframe"]');
    adFrames.forEach(f => f.style.display='none');
    """)

# ======================================================================
# TEST 5: RADIO BUTTON
# ======================================================================
@pytest.mark.order(5)
def test_radio_buttons():
    print("\n=== TEST: Radio Button on Chrome ===")
    driver = DriverFactory.get_driver(browser_name="chrome", headless=False)
    driver.get("https://demoqa.com/radio-button")
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)
    time.sleep(1)

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

        yes_radio = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='yesRadio']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_radio)
        driver.execute_script("arguments[0].click();", yes_radio)
        time.sleep(1)
        result = driver.find_element(By.CLASS_NAME, "text-success").text
        assert "Yes" in result
        print(f"✅ Selected: {result}")

        impressive_radio = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='impressiveRadio']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", impressive_radio)
        driver.execute_script("arguments[0].click();", impressive_radio)
        time.sleep(1)
        result = driver.find_element(By.CLASS_NAME, "text-success").text
        assert "Impressive" in result
        print(f"✅ Selected: {result}")

        no_radio = driver.find_element(By.ID, "noRadio")
        assert not no_radio.is_enabled(), "'No' should be disabled"
        print("✅ 'No' radio is disabled")

    finally:
        driver.quit()

# ======================================================================
# TEST 6: CHECKBOX
# ======================================================================
@pytest.mark.order(6)
def test_checkboxes():
    print("\n=== TEST: Checkbox on Chrome ===")
    driver = DriverFactory.get_driver(browser_name="chrome", headless=False)
    driver.get("https://demoqa.com/checkbox")
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)
    time.sleep(1)

    try:
        expand = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Expand all']")))
        driver.execute_script("arguments[0].click();", expand)
        time.sleep(1)

        desktop = driver.find_element(By.XPATH, "//label[@for='tree-node-desktop']/span[@class='rct-checkbox']")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", desktop)
        driver.execute_script("arguments[0].click();", desktop)
        time.sleep(1)
        result = driver.find_element(By.ID, "result").text
        assert "desktop" in result.lower()
        print(f"✅ Selected: {result}")

        documents = driver.find_element(By.XPATH, "//label[@for='tree-node-documents']/span[@class='rct-checkbox']")
        driver.execute_script("arguments[0].click();", documents)
        time.sleep(1)
        result = driver.find_element(By.ID, "result").text
        print(f"✅ Updated: {result}")

        driver.execute_script("arguments[0].click();", desktop)  # uncheck
        time.sleep(1)
        collapse = driver.find_element(By.CSS_SELECTOR, "button[title='Collapse all']")
        driver.execute_script("arguments[0].click();", collapse)
        print("✅ Checkbox Test Completed")

    finally:
        driver.quit()

# ======================================================================
# TEST 7: DROPDOWN
# ======================================================================
@pytest.mark.order(7)
def test_dropdowns():
    print("\n=== TEST: Dropdown on Chrome ===")
    driver = DriverFactory.get_driver(browser_name="chrome", headless=False)
    driver.get("https://demoqa.com/select-menu")
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)
    time.sleep(1)

    try:
        old_select = wait.until(EC.visibility_of_element_located((By.ID, "oldSelectMenu")))
        select_obj = Select(old_select)
        select_obj.select_by_visible_text("Purple")
        time.sleep(1)
        print(f"✅ Selected: {select_obj.first_selected_option.text}")

        multi_select = driver.find_element(By.ID, "cars")
        multi_select_obj = Select(multi_select)
        if multi_select_obj.is_multiple:
            multi_select_obj.select_by_visible_text("Volvo")
            multi_select_obj.select_by_visible_text("Audi")
            time.sleep(1)
            selected = [o.text for o in multi_select_obj.all_selected_options]
            print(f"✅ Multi-selected: {selected}")
            multi_select_obj.deselect_all()
            print("✅ Deselected all")

    finally:
        driver.quit()

# ======================================================================
# TEST 8: FILE UPLOAD (Fixed)
# ======================================================================
@pytest.mark.order(8)
def test_file_upload():
    print("\n=== TEST: File Upload on Chrome ===")
    driver = DriverFactory.get_driver(browser_name="chrome", headless=False)
    driver.get("https://demoqa.com/upload-download")
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    remove_ads(driver)
    time.sleep(1)

    try:
        # ✅ Dynamically create a temporary text file
        test_folder = os.path.join(os.getcwd(), "testdata")
        os.makedirs(test_folder, exist_ok=True)
        test_file = os.path.join(test_folder, "some.txt")

        if not os.path.exists(test_file):
            with open(test_file, "w") as f:
                f.write("This is a demo test file for upload verification.")
            print(f"Created test file at: {test_file}")
        else:
            print(f"Using existing file: {test_file}")

        # Upload file
        upload_input = wait.until(EC.presence_of_element_located((By.ID, "uploadFile")))
        upload_input.send_keys(test_file)
        time.sleep(2)

        uploaded_path = driver.find_element(By.ID, "uploadedFilePath").text
        assert "some.txt" in uploaded_path
        print(f"✅ File uploaded successfully: {uploaded_path}")

    finally:
        driver.quit()

# ======================================================================
# TEST 9: DRAG & DROP
# ======================================================================
@pytest.mark.order(9)
def test_drag_drop_demo():
    print("\n=== TEST: Drag and Drop on Chrome ===")
    driver = DriverFactory.get_driver(browser_name="chrome", headless=False)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://demoqa.com/droppable")
        driver.maximize_window()
        remove_ads(driver)
        time.sleep(1)

        actions = ActionChains(driver)
        source = wait.until(EC.visibility_of_element_located((By.ID, "draggable")))
        target = wait.until(EC.visibility_of_element_located((By.ID, "droppable")))
        actions.drag_and_drop(source, target).perform()
        time.sleep(2)

        target_text = target.text
        print(f"✅ Target text after drop: {target_text}")

    finally:
        driver.quit()
