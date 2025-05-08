import pytest
from pytest_csv_params.decorator import csv_params
from pages import CheckoutPage
from playwright.async_api import expect
from tests.utils.api_helper import APIHelper
from tests.utils.common_utils import camel_to_snake

@csv_params(data_file="./tests/test_data/checkout_params.csv")
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_input(setup_checkout, test_field, test_value, test_description):
    checkout_page, checkout_data = setup_checkout
    if test_field: checkout_data[test_field] = test_value

    discount_code = checkout_data.pop("discount_code", None)
    check_tos = checkout_data.pop("tos_checkbox", False)
    await checkout_page.fill_billing_details(**checkout_data)
    if discount_code: await checkout_page.apply_discount_code(discount_code)
    if check_tos: await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()

    if test_field and test_field != "discount_code":
        assert not order_id, f"Invalid order was placed with {test_description}"
    else:
        assert order_id, f"Valid order with {test_description} wasn't placed after 2s"

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
    checkout_page = CheckoutPage(page)
    await checkout_page.navigate()
    await expect(page, f"should not allow the user to access checkout if {test_case}").not_to_have_url(checkout_page.url, timeout=2000)

@pytest.mark.asyncio(loop_scope="module")
async def test_api_order_placed(setup_checkout):
    checkout_page, checkout_data = setup_checkout

    discount_code = checkout_data.pop("discount_code", None)
    check_tos = checkout_data.pop("tos_checkbox", False)
    await checkout_page.fill_billing_details(**checkout_data)
    if discount_code: await checkout_page.apply_discount_code(discount_code)
    if check_tos: await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()
    assert order_id, f"Valid order wasn't placed after 2s"

    order_data = APIHelper.get_order(order_id)
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
