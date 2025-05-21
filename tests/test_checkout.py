import pytest
from pages import CheckoutPage
from playwright.async_api import expect, Cookie
from typing import Dict, List, Any
from tests.utils.api_helper import APIHelper

@pytest.mark.asyncio(loop_scope = "module")
async def test_cart_items_count(setup_checkout: CheckoutPage, valid_cart_data: List[Dict[str, Any]]):
    checkout_page = setup_checkout
    cart_items_count = len(valid_cart_data)
    await expect(checkout_page.cart_items).to_have_count(cart_items_count)

@pytest.mark.asyncio(loop_scope = "module")
async def test_first_product_title(setup_checkout: CheckoutPage, valid_cart_data: List[Dict[str, Any]]):
    checkout_page = setup_checkout
    product_title = valid_cart_data[0].get("title", None)
    await expect(checkout_page.cart_item_titles.first).to_have_text(product_title)

@pytest.mark.asyncio(loop_scope = "module")
async def test_first_product_quantity(setup_checkout: CheckoutPage, valid_cart_data: List[Dict[str, Any]]):
    checkout_page = setup_checkout
    product_quantity = str(valid_cart_data[0].get("quantity", None))
    await expect(checkout_page.cart_item_quantities.first).to_have_text(product_quantity)

@pytest.mark.asyncio(loop_scope = "module")
async def test_first_product_variant(setup_checkout: CheckoutPage, valid_cart_data: List[Dict[str, Any]]):
    checkout_page = setup_checkout
    product_variant = valid_cart_data[0].get("variant", None)
    await expect(checkout_page.cart_item_variants.first).to_have_text(product_variant)

@pytest.mark.asyncio(loop_scope = "module")
async def test_form_valid_data(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str]
):
    checkout_page = setup_checkout
    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    await checkout_page.place_order()

    await expect(checkout_page.order_message).to_contain_text(expected="Order saved successfully!", timeout=2000)

@pytest.mark.parametrize("empty_field", [
    "first_name",
    "last_name",
    "country",
    "city",
    "address",
    "phone",
    "email"
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_empty_billing_details_fields(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str],
    empty_field: str
):
    checkout_page = setup_checkout
    invalid_billing_details = valid_billing_details
    invalid_billing_details.pop(empty_field, None)

    await checkout_page.fill_billing_details(**invalid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    await checkout_page.place_order()

    await expect(checkout_page.order_message).not_to_be_visible(timeout=2000)

@pytest.mark.parametrize("empty_field", [
    "card_number",
    "expiry",
    "cvc"
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_empty_credit_card_fields(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str],
    empty_field: str
):
    checkout_page = setup_checkout
    invalid_credit_card_info = valid_credit_card_info
    invalid_credit_card_info.pop(empty_field, None)

    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**invalid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    await checkout_page.place_order()

    await expect(checkout_page.order_message).not_to_be_visible(timeout=2000)

@pytest.mark.asyncio(loop_scope = "module")
async def test_form_unchecked_tos(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str]
):
    checkout_page = setup_checkout

    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.place_order()

    await expect(checkout_page.order_message).not_to_be_visible(timeout=2000)

@pytest.mark.asyncio(loop_scope = "module")
async def test_form_optional_discount_code(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str]
):
    checkout_page = setup_checkout

    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    await checkout_page.place_order()

    await expect(checkout_page.order_message).to_contain_text(expected="Order saved successfully!", timeout=2000)

@pytest.mark.parametrize("test_field, test_value", [
    ("email", ".email@example.com"),
    ("email", "invalid..email@example.com"),
    ("email", "email@example"),
    ("email", "email@example.c-m"),
    ("email", "email@example.c"),
    ("phone", "not_a_phone_number"),
    ("phone", "+999999"),
    ("phone", "+9999999999999999")
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_invalid_billing_details(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str],
    test_field: str,
    test_value: str
):
    checkout_page = setup_checkout
    invalid_billing_details = valid_billing_details
    invalid_billing_details[test_field] = test_value

    await checkout_page.fill_billing_details(**invalid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    await checkout_page.place_order()

    await expect(checkout_page.order_message).not_to_contain_text(expected="Order saved successfully!", timeout=2000)

@pytest.mark.parametrize("test_field, test_value", [
    ("card_number", "not_a_card_number"),
    ("card_number", "0000000000000001"),
    ("expiry", "not_a_date"),
    ("expiry", "13/26"),
    ("expiry", "12/24"),
    ("cvc", "abc")
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_invalid_credit_card_info(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str],
    test_field: str,
    test_value: str
):
    checkout_page = setup_checkout
    invalid_credit_card_info = valid_credit_card_info
    invalid_credit_card_info[test_field] = test_value

    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**invalid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    await checkout_page.place_order()

    await expect(checkout_page.order_message).not_to_contain_text(expected="Order saved successfully!", timeout=2000)

@pytest.mark.parametrize("test_case", [
    "not logged in",
    "cart is empty",
])
@pytest.mark.asyncio(loop_scope="module")
async def test_access(
    browser,
    session: List[Cookie],
    valid_cart_data: List[Dict[str, Any]],
    test_case: str
):
    context = await browser.new_context()

    if test_case != "not logged in":
        await context.add_cookies(session)
    if test_case != "cart is empty":
        await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({valid_cart_data}))")

    page = await context.new_page()
    checkout_page = CheckoutPage(page)
    await page.goto(checkout_page.url)

    await expect(page, f"should not allow the user to access checkout if {test_case}").not_to_have_url(checkout_page.url, timeout=2000)

@pytest.mark.asyncio(loop_scope="module")
async def test_api_order_placed(
    setup_checkout: CheckoutPage,
    valid_billing_details: Dict[str, str],
    valid_credit_card_info: Dict[str, str],
    valid_cart_data: List[Dict[str, Any]]
):
    checkout_page = setup_checkout

    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()
    assert order_id, f"API response timed out (2s)"
    APIHelper.validate_order(
        order_id,
        valid_billing_details | valid_credit_card_info,
        valid_cart_data[0]
    )
