import pytest
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils import Utils, WAIT_TIME
import allure

@pytest.mark.feature("web-testing")
def test_scenario_1_standard_user_checkout(driver):
    Utils.login(driver, "standard_user")
    Utils.add_all_items_to_cart(driver)
    Utils.go_to_cart(driver)

    # Use Utils to get cart items (already waits for them)
    cart_items = Utils.get_cart_items(driver)
    initial_count = len(cart_items)
    assert initial_count > 2, f"Expected more than 2 items in cart, got {initial_count}"

    # Remove 3rd item
    cart_items[2].find_element(By.CSS_SELECTOR, "button").click()

    # Wait for cart items to update via Utils
    cart_items = Utils.get_cart_items(driver)
    assert len(cart_items) == initial_count - 1, "Cart item count did not decrease by 1"

    # Checkout and confirm
    confirmation = Utils.checkout(driver)
    assert "THANK YOU" in confirmation.upper(), "Checkout confirmation missing"

@pytest.mark.feature("web-testing")
def test_scenario_2_problem_user_add_item(driver):
    Utils.login(driver, "problem_user")
    item_name = "Sauce Labs Backpack"

    # Use Utils helper to add item to cart (handles clicking and waiting)
    Utils.add_item_to_cart(driver, item_name)

    # Go to cart
    Utils.go_to_cart(driver)

    # Get cart items using Utils
    cart_items = Utils.get_cart_items(driver)
    names = [i.find_element(By.CLASS_NAME, "inventory_item_name").text for i in cart_items]
    assert item_name in names, f"Expected '{item_name}' in cart items: {names}"

@pytest.mark.feature("web-testing")
def test_scenario_3_sort_products(driver):
    Utils.login(driver, "standard_user")

    # Wait for sort dropdown
    sort_dropdown = WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container"))
    )
    select = Select(sort_dropdown)
    select.select_by_visible_text("Name (Z to A)")

    # Wait a bit for page to update (or optionally add smarter wait)
    WebDriverWait(driver, WAIT_TIME).until(lambda d: Utils.get_inventory_names(d))

    # Get inventory names using Utils
    names = Utils.get_inventory_names(driver)

    # Compare with descending sorted list
    assert names == sorted(names, reverse=True), "Products are not sorted from Z to A"

@pytest.mark.feature("web-testing")
def test_scenario_4_locked_out_user(driver):
    Utils.login(driver, "locked_out_user")

    # Wait for error message (no Utils method for login errors yet)
    error = WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    assert "locked" in error.text.lower(), f"Expected 'locked' in error, got: {error.text}"

