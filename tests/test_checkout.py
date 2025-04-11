import pytest
from pages import CheckoutPage
from playwright.async_api import TimeoutError

@pytest.mark.asyncio(loop_scope = "module")
async def test_checkout_valid_data(browser, session, checkout_valid_data):
    context = await browser.new_context()
    await context.add_cookies(session)
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
        checkout_valid_data["card_date"],
        checkout_valid_data["card_cvc"]
    )
    if checkout_valid_data["tos_checkbox"]: await checkout.click_tos_checkbox()
    await checkout.place_order()

    order_saved_message = "p:has-text('Order saved successfully!')"
    try:
        await page.wait_for_selector(order_saved_message, timeout=2000)
        order_placed = await page.locator(order_saved_message).is_visible()
    except TimeoutError:
        order_placed = False
    assert order_placed, "Order with correct details wasn't placed after 2s"

required_fields = [ "first_name",
                   "last_name",
                   "country",
                   "city",
                   "address",
                   "phone",
                   "email",
                   "card_number",
                   "card_date",
                   "card_cvc",
                   "tos_checkbox"
                   ]
@pytest.mark.parametrize("field_to_empty", required_fields)
@pytest.mark.asyncio(loop_scope = "module")
async def test_checkout_required_fields(browser, session, checkout_valid_data, field_to_empty):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()

    checkout = CheckoutPage(page)
    await checkout.navigate()
    checkout_data = checkout_valid_data.copy()
    checkout_data[field_to_empty] = ""
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
        checkout_data["card_date"],
        checkout_data["card_cvc"]
    )
    if checkout_data["tos_checkbox"]: await checkout.click_tos_checkbox()
    await checkout.place_order()

    order_saved_message = "p:has-text('Order saved successfully!')"
    try:
        await page.wait_for_selector(order_saved_message, timeout=2000)
        order_placed = await page.locator(order_saved_message).is_visible()
    except TimeoutError:
        order_placed = False
    assert not order_placed, f"Order was placed with required field {field_to_empty} empty"
