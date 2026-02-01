import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import Utils, WAIT_TIME


@allure.feature("Web testing")
@allure.story("Standard user checkout flow")
def test_standard_user_checkout(driver):
    utils = Utils(driver)

    utils.login("standard_user")
    utils.add_all_items_to_cart()
    utils.go_to_cart()

    cart_items = utils.get_cart_items()
    initial_count = len(cart_items)
    assert initial_count > 2, f"Expected more than 2 items, got {initial_count}"

    # Remove 3rd item
    cart_items[2].find_element(By.CSS_SELECTOR, "button").click()

    updated_items = utils.get_cart_items()
    assert len(updated_items) == initial_count - 1, "Cart item count did not decrease"

    confirmation = utils.checkout()
    assert "THANK YOU" in confirmation.upper()


@allure.feature("Web testing")
@allure.story("Problem user adds item to cart")
def test_problem_user_add_item(driver):
    utils = Utils(driver)
    item_name = "Sauce Labs Backpack"

    utils.login("problem_user")
    utils.add_item_to_cart(item_name)
    utils.go_to_cart()

    cart_items = utils.get_cart_items()
    names = [
        item.find_element(By.CLASS_NAME, "inventory_item_name").text
        for item in cart_items
    ]

    assert item_name in names, f"Expected '{item_name}' in cart, got {names}"


@allure.feature("Web testing")
@allure.story("Product sorting Z to A")
def test_sort_products_z_to_a(driver):
    utils = Utils(driver)
    utils.login("standard_user")

    sort_dropdown = WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container"))
    )
    Select(sort_dropdown).select_by_visible_text("Name (Z to A)")

    names = utils.get_inventory_names()
    assert names == sorted(names, reverse=True), "Products are not sorted Z to A"


@allure.feature("Web testing")
@allure.story("Locked out user cannot log in")
def test_locked_out_user(driver):
    utils = Utils(driver)

    utils.login("locked_out_user")

    error = WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )

    assert "locked" in error.text.lower(), f"Unexpected error message: {error.text}"
