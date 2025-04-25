import pytest
from pytest_csv_params.decorator import csv_params
import requests
import json
from pages import CheckoutPage
from playwright.async_api import expect, TimeoutError
from config.config import BASE_URL

def camel_to_snake(camel_case_str):
    snake_case_str = []
    for char in camel_case_str:
        if char.isupper() and snake_case_str:
            snake_case_str.append('_')
            snake_case_str.append(char.lower())
        else:
            snake_case_str.append(char)
    return ''.join(snake_case_str)

def load_json(file_name):
    file_path = f"./tests/test_data/{file_name}"
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

@csv_params(data_file="./tests/test_data/checkout_params.csv")
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_input(browser, session, test_field, test_value, test_description):
    context = await browser.new_context()
    await context.add_cookies(session)
    cart_data = load_json("cart_valid_data.json")
    await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_data}))")
    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    checkout_data = load_json("checkout_valid_data.json")
    if test_field: checkout_data[test_field] = test_value
    await checkout.fill_billing_details(
        checkout_data["first_name"],
        checkout_data["last_name"],
        checkout_data["country"],
        checkout_data["city"],
        checkout_data["address"],
        checkout_data["phone"],
        checkout_data["email"],
        checkout_data["notes"]
    )
    if test_field != "discount_code": await checkout.apply_discount_code(checkout_data["discount_code"])
    await checkout.fill_credit_card_details(
        checkout_data["card_number"],
        checkout_data["expiry"],
        checkout_data["cvc"]
    )
    if checkout_data["tos_checkbox"]: await checkout.click_tos_checkbox()

    order_placed = False
    try:
        async with page.expect_response(f"{BASE_URL}/api/checkout", timeout=2000) as response_info:
            await checkout.place_order()
        response = await response_info.value

        if response.ok:
            response_data = await response.json()
            order_placed = response_data.get("success", False)
    except TimeoutError:
        pass

    if test_field and test_field != "discount_code":
        assert not order_placed, f"Invalid order was placed with {test_description}"
    else:
        assert order_placed, f"Valid order with {test_description} wasn't placed after 2s"

@pytest.mark.parametrize("test_case", [
    "not logged in",
    "cart is empty",
])
@pytest.mark.asyncio(loop_scope="module")
async def test_access(browser, session, test_case):
    context = await browser.new_context()

    if test_case != "not logged in":
        await context.add_cookies(session)
    if test_case != "cart is empty":
        cart_data = load_json("cart_valid_data.json")
        await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_data}))")

    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    await expect(page, f"should not allow the user to access checkout if {test_case}").not_to_have_url(checkout.url, timeout=2000)

@pytest.mark.asyncio(loop_scope="module")
async def test_api_order_placed(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    cart_data = load_json("cart_valid_data.json")
    await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_data}))")
    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    checkout_data = load_json("checkout_valid_data.json")
    await checkout.fill_billing_details(
        checkout_data["first_name"],
        checkout_data["last_name"],
        checkout_data["country"],
        checkout_data["city"],
        checkout_data["address"],
        checkout_data["phone"],
        checkout_data["email"],
        checkout_data["notes"]
    )
    await checkout.apply_discount_code(checkout_data["discount_code"])
    await checkout.fill_credit_card_details(
        checkout_data["card_number"],
        checkout_data["expiry"],
        checkout_data["cvc"]
    )
    await checkout.click_tos_checkbox()

    try:
        async with page.expect_response(f"{BASE_URL}/api/checkout", timeout=2000) as response_info:
            await checkout.place_order()
        response = await response_info.value

        assert response.ok, "Failed to place order"
        response_data = await response.json()
        assert "orderId" in response_data, "Response does not contain orderId"
        order_id = response_data.get("orderId")
    except TimeoutError:
        raise TimeoutError("Order was not placed after 2s")

    api_order = requests.get(f"{BASE_URL}/api/orders/{order_id}")
    assert api_order.ok, f"Failed to retrieve order {order_id} from API - {api_order.status_code}"

    order_data = api_order.json()
    order_api_id = order_data.pop("id", None)
    order_data.pop("createdAt", None)
    cart_data = order_data.pop("items", [])

    errors = []
    for product in cart_data:
        product.pop("id", None)
        for key, value in product.items():
            if key == "orderId":
                reference = order_api_id
            else:
                reference = product.get(key, None)
            if value != reference:
                errors.append(f"Product {key} mismatch: reference = {reference}, saved = {value}")

    for key, value in order_data.items():
        key = camel_to_snake(key)
        reference = checkout_data.get(key, None)
        if value != reference:
            errors.append(f"Order {key} mismatch: reference = {reference}, saved = {value}")

    assert not errors, f"Order data mismatch (check complete message for details)\n{'\n'.join(errors)}"
