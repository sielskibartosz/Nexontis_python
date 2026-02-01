import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import wraps

BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"
WAIT_TIME = 5


def log_step(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        step_name = func.__name__.replace("_", " ").title()
        with allure.step(step_name):
            return func(self, *args, **kwargs)
    return wrapper


class Utils:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIME)

    @log_step
    def login(self, username):
        self.driver.get(BASE_URL)
        self.wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
        self.wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
        self.wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    @log_step
    def add_all_items_to_cart(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".inventory_item button"))
        )
        for btn in buttons:
            self.wait.until(EC.element_to_be_clickable(btn)).click()

    @log_step
    def get_cart_items(self):
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart_item"))
            )
        except:
            return []

    @log_step
    def go_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "shopping_cart_container"))
        ).click()

    @log_step
    def checkout(self, first_name="Test", last_name="User", postal_code="12345"):
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys(first_name)
        self.wait.until(EC.visibility_of_element_located((By.ID, "last-name"))).send_keys(last_name)
        self.wait.until(EC.visibility_of_element_located((By.ID, "postal-code"))).send_keys(postal_code)
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

        return self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

    @log_step
    def get_inventory_names(self):
        items = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".inventory_item_name"))
        )
        return [item.text for item in items]

    @log_step
    def add_item_to_cart(self, item_name):
        item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[text()='{item_name}']"))
        )
        item.click()

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']"))
        ).click()
