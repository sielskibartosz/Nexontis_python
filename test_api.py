import pytest
import requests
import time
import allure

BASE_URL = "https://dummyjson.com/products"

@allure.feature("API Testing")
@allure.story("Get all products")
def test_get_all_products():
    response = requests.get(BASE_URL)

    # Validate request was successful
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    data = response.json()
    products = data.get("products", [])
    assert products, "No products returned"

    # Print titles of products with odd IDs
    odd_id_titles = [p["title"] for p in products if p["id"] % 2 == 1]
    print("Products with odd IDs:", odd_id_titles)

@allure.feature("API Testing")
@allure.story("Create a new product")
def test_create_product():
    new_product = {
        "title": "Test Product",
        "description": "This is a test product",
        "price": 99,
        "brand": "TestBrand"
    }

    response = requests.post(BASE_URL + "/add", json=new_product)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    data = response.json()
    # Validate response data
    for key in new_product:
        assert data.get(key) == new_product[key], f"Expected {key}='{new_product[key]}', got {data.get(key)}"
        assert data.get("id") is not None, "Expected an 'id' in the response"

@allure.feature("API Testing")
@allure.story("Update third product")
def test_update_third_product():
    product_id = 3

    # Get current product data
    response = requests.get(f"{BASE_URL}/{product_id}")
    assert response.status_code == 200
    original_data = response.json()

    # Update only price
    new_price = original_data["price"] + 10
    patch_response = requests.patch(
        f"{BASE_URL}/{product_id}",
        json={"price": new_price}
    )

    assert patch_response.status_code == 200
    updated_data = patch_response.json()

    # 1 Price updated
    assert updated_data["price"] == new_price
    # 2 Other fields unchanged
    for key in updated_data.keys():
        if key != "price":
            assert original_data[key] == updated_data[
                key], f"Expected {key}='{original_data[key]}', got {updated_data[key]}"

@allure.feature("API Testing")
@allure.story("Validate response time with delay parameter")
@pytest.mark.parametrize("delay", [0, 5000, 6000])
def test_delay_response_time(delay):
    start_time = time.time()

    response = requests.get(
        BASE_URL,
        params={"delay": delay / 1000}  # dummyjson używa sekund
    )

    elapsed_ms = (time.time() - start_time) * 1000

    # 3. Validate request was successful
    assert response.status_code == 200

    # 4. Validate response time
    assert elapsed_ms <= 1000, (
        f"Response time too long: {elapsed_ms:.0f} ms for delay={delay}"
    )
