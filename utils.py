import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from functools import wraps

BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"
WAIT_TIME = 5


def log_step(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log function name as an Allure step
        step_name = func.__name__.replace("_", " ").title()
        with allure.step(step_name):
            return func(*args, **kwargs)

    return wrapper

class Utils:

    @log_step
    @staticmethod
    def login(driver, username):
        driver.get(BASE_URL)
        WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        ).send_keys(username)
        WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys(PASSWORD)
        WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        ).click()

    @log_step
    @staticmethod
    def add_all_items_to_cart(driver):
        buttons = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".inventory_item button"))
        )
        for btn in buttons:
            WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable(btn))
            btn.click()

    @log_step
    @staticmethod
    def get_cart_items(driver):
        # Wait until cart items are present (empty list if none)
        try:
            return WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart_item"))
            )
        except:
            return []

    @log_step
    @staticmethod
    def go_to_cart(driver):
        WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "shopping_cart_container"))
        ).click()

    @log_step
    @staticmethod
    def checkout(driver, first_name="Test", last_name="User", postal_code="12345"):
        wait = WebDriverWait(driver, WAIT_TIME)
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys(first_name)
        wait.until(EC.visibility_of_element_located((By.ID, "last-name"))).send_keys(last_name)
        wait.until(EC.visibility_of_element_located((By.ID, "postal-code"))).send_keys(postal_code)
        wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))).text

    @log_step
    @staticmethod
    def get_inventory_names(driver):
        items = WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".inventory_item_name"))
        )
        return [item.text for item in items]

    @log_step
    @staticmethod
    def click_item_by_name(driver, item_name):
        """Click on an item by its displayed name."""
        item = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[text()='{item_name}']"))
        )
        item.click()

    @log_step
    @staticmethod
    def add_item_to_cart(driver, item_name):
        """Add an item to the cart by item name."""
        Utils.click_item_by_name(driver, item_name)
        add_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']"))
        )
        add_button.click()

