import pytest
import requests
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

@pytest.mark.parametrize("test_field,test_value,test_description", [
    # valid data
    (None, None, "valid data"),
    # empty fields
    ("first_name", "", "empty first name"),
    ("last_name", "", "empty last name"),
    ("country", "", "empty country"),
    ("city", "", "empty city"),
    ("address", "", "empty address"),
    ("phone", "", "empty phone number"),
    ("email", "", "empty email"),
    ("card_number", "", "empty card number"),
    ("expiry", "", "empty card date"),
    ("cvc", "", "empty card cvc"),
    ("tos_checkbox", False, "unchecked terms and conditions"),
    # email validations not covered by html input type=email attribute
    ("email", ".email@example.com", "invalid email (local part starts with special character)"),
    ("email", "invalid..email@example.com", "invalid email (local part has repeated special characters)"),
    ("email", "email@example", "invalid email (no top level domain)"),
    ("email", "email@example.c-m", "invalid email (top level domain has special character)"),
    ("email", "email@example.c", "invalid email (top level domain too short, <2 chars)"),
    # phone number length validations according to E.164
    ("phone", "not_a_phone_number", "invalid phone number (invalid chars)"),
    ("phone", "+999999", "invalid phone number (too short, <7 digits)"),
    ("phone", "+9999999999999999", "invalid phone number (too long, >15 digits)"),
    # credit card tests
    ("card_number", "not_a_card_number", "invalid card number (not a number)"),
    ("card_number", "0000000000000001", "invalid card number (fails luhn algorithm)"),
    ("expiry", "not_a_date", "invalid card expiration date (not a date)"),
    ("expiry", "13/26", "invalid card expiration date (invalid date)"),
    ("expiry", "12/24", "invalid card expiration date (expired card)"),
    ("cvc", "abc", "invalid card cvc (not a number)"),
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_input(browser, session, checkout_valid_data, cart_valid_data, test_field, test_value, test_description):
    context = await browser.new_context()
    await context.add_cookies(session)
    await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_valid_data}))")
    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    checkout_data = checkout_valid_data.copy()
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
    await checkout.apply_discount_code(checkout_data["discount_code"])
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

    if test_field:
        assert not order_placed, f"Order was placed with {test_description}"
    else:
        assert order_placed, "Order with valid data wasn't placed after 2s"

@pytest.mark.parametrize("test_case", [
    "not logged in",
    "cart is empty",
])
@pytest.mark.asyncio(loop_scope="module")
async def test_access(browser, session, cart_valid_data, test_case):
    context = await browser.new_context()

    if test_case != "not logged in":
        await context.add_cookies(session)
    if test_case != "cart is empty":
        await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_valid_data}))")

    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    await expect(page, f"should not allow the user to access checkout if {test_case}").not_to_have_url(checkout.url, timeout=2000)

@pytest.mark.asyncio(loop_scope="module")
async def test_api_order_placed(browser, session, checkout_valid_data, cart_valid_data):
    context = await browser.new_context()
    await context.add_cookies(session)
    await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_valid_data}))")
    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    await checkout.fill_billing_details(
        checkout_valid_data["first_name"],
        checkout_valid_data["last_name"],
        checkout_valid_data["country"],
        checkout_valid_data["city"],
        checkout_valid_data["address"],
        checkout_valid_data["phone"],
        checkout_valid_data["email"],
        checkout_valid_data["notes"]
    )
    await checkout.apply_discount_code(checkout_valid_data["discount_code"])
    await checkout.fill_credit_card_details(
        checkout_valid_data["card_number"],
        checkout_valid_data["expiry"],
        checkout_valid_data["cvc"]
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
    product = cart_data[0]
    product.pop("id", None)
    for key, value in product.items():
        if key == "orderId":
            reference = order_api_id
        else:
            reference = cart_valid_data[0].get(key, None)
        if value != reference:
            errors.append(f"Product {key} mismatch: reference = {reference}, saved = {value}")

    for key, value in order_data.items():
        key = camel_to_snake(key)
        reference = checkout_valid_data.get(key, None)
        if value != reference:
            errors.append(f"Order {key} mismatch: reference = {reference}, saved = {value}")

    assert not errors, f"Order data mismatch (check complete message for details)\n{'\n'.join(errors)}"
