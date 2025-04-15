import pytest
from pages import CheckoutPage
from playwright.async_api import TimeoutError

@pytest.mark.parametrize("test_field,test_value,test_description", [
    (None, None, "valid data"),
    ("first_name", "", "empty first name"),
    ("last_name", "", "empty last name"),
    ("country", "", "empty country"),
    ("city", "", "empty city"),
    ("address", "", "empty address"),
    ("phone", "", "empty phone number"),
    ("email", "", "empty email"),
    ("card_number", "", "empty card number"),
    ("card_date", "", "empty card date"),
    ("card_cvc", "", "empty card cvc"),
    ("tos_checkbox", False, "unchecked terms and conditions"),
    ("email", "not_an_email", "invalid email (no @)"),
    ("phone", "not_a_phone_number", "invalid phone number"),
    ("card_number", "not_a_card_number", "invalid card number (not a number)"),
    ("card_number", "0000000000000001", "invalid card number (fails luhn algorithm)"),
    ("card_date", "not_a_date", "invalid card expiration date (not a date)"),
    ("card_date", "13/26", "invalid card expiration date (invalid date)"),
    ("card_date", "12/24", "invalid card expiration date (expired card)"),
    ("card_cvc", "abc", "invalid card cvc (not a number)"),
])
@pytest.mark.asyncio(loop_scope = "module")
async def test_form_input(browser, session, checkout_valid_data, test_field, test_value, test_description):
    context = await browser.new_context()
    await context.add_cookies(session)
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

    if test_field:
        assert not order_placed, f"Order was placed with {test_description}"
    else:
        assert order_placed, "Order with valid data wasn't placed after 2s"
