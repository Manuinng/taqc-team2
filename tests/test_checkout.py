import pytest
from pytest_csv_params.decorator import csv_params
from pages import CheckoutPage
from playwright.async_api import expect, Cookie
from tests.utils.api_helper import APIHelper
from tests.utils.common_utils import camel_to_snake
from typing import Tuple, Dict, List, Any

@pytest.mark.asyncio(loop_scope = "module")
async def test_form_valid_data(setup_checkout: Tuple[CheckoutPage, Dict[str, Any]]):
    checkout_page, checkout_data = setup_checkout
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert order_id, f"Order was not placed with valid data"

@pytest.mark.parametrize("empty_field", [
    "first_name",
    "last_name",
    "country",
    "city",
    "address",
    "phone",
    "email",
    "card_number",
    "expiry",
    "cvc",
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_empty_fields(setup_checkout: Tuple[CheckoutPage, Dict[str, Any]], empty_field:str):
    checkout_page, checkout_data = setup_checkout
    checkout_data.pop(empty_field, None)
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert not order_id, f"Order {order_id} was placed with empty {empty_field}"

@pytest.mark.asyncio(loop_scope = "module")
async def test_form_unchecked_tos(setup_checkout: Tuple[CheckoutPage, Dict[str, Any]]):
    checkout_page, checkout_data = setup_checkout
    checkout_data.pop("tos_checkbox", None)
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert not order_id, f"Order {order_id} was placed with unchecked ToS"

@pytest.mark.asyncio(loop_scope = "module")
async def test_form_optional_discount_code(setup_checkout: Tuple[CheckoutPage, Dict[str, Any]]):
    checkout_page, checkout_data = setup_checkout
    checkout_data.pop("discount_code", None)
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert order_id, f"Order was not placed with empty discount code"

@csv_params(data_file="./tests/test_data/checkout_invalid_data_params.csv")
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_invalid_data(setup_checkout: Tuple[CheckoutPage, Dict[str, Any]], test_field: str, test_value: str):
    checkout_page, checkout_data = setup_checkout
    checkout_data[test_field] = test_value
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert not order_id, f"Order {order_id} was placed with {test_value} in {test_field} field"

@pytest.mark.parametrize("test_case", [
    "not logged in",
    "cart is empty",
])
@pytest.mark.asyncio(loop_scope="module")
async def test_access(browser, session: List[Cookie], cart_valid_data: Dict[str, Any], test_case: str):
    context = await browser.new_context()

    if test_case != "not logged in":
        await context.add_cookies(session)
    if test_case != "cart is empty":
        await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({cart_valid_data}))")

    page = await context.new_page()
    checkout_page = CheckoutPage(page)
    await checkout_page.navigate()
    await expect(page, f"should not allow the user to access checkout if {test_case}").not_to_have_url(checkout_page.url, timeout=2000)

@pytest.mark.asyncio(loop_scope="module")
async def test_api_order_placed(setup_checkout: Tuple[CheckoutPage, Dict[str, Any]]):
    checkout_page, checkout_data = setup_checkout
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert order_id, f"Valid order wasn't placed after 2s"

    order_data = APIHelper.get_order(order_id)
    assert "id" in order_data, "API response is missing 'id' field"
    order_api_id = order_data.pop("id")
    order_data.pop("createdAt", None)
    assert "items" in order_data, "API response is missing 'items' field"
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

    assert not errors, "Order data mismatch (check complete message for details)\n" + '\n'.join(errors)
