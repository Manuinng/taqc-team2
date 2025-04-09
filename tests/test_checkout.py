import pytest
from config.config import TEST_USER
from pages import AutomationPortal, CheckoutPage, Navbar, LoginPopup, CartSidebar
from playwright.async_api import TimeoutError

@pytest.mark.asyncio(loop_scope = "module")
async def test_checkout_valid_data(browser, checkout_valid_data):
    page = await browser.new_page()
    test_email = TEST_USER["email"] or "email@example.com"
    test_password = TEST_USER["password"] or "password"

    portal = AutomationPortal(page)
    checkout = CheckoutPage(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)
    cart_sidebar = CartSidebar(page)

    await portal.navigate()
    await portal.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.fill_login_popup(test_email, test_password)
    await login_popup.submit_login_popup()
    await page.keyboard.press("Escape") # To remove bugged overlay in "My Account" page
    await navbar.open_cart_sidebar()
    await cart_sidebar.click_tos_checkbox()
    await cart_sidebar.go_to_checkout()
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
    assert order_placed, "F: Order with correct details wasn't placed after 2s"


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
async def test_checkout_empty_required_fields(browser, checkout_valid_data, field_to_empty):
    page = await browser.new_page()
    test_email = TEST_USER["email"] or "email@example.com"
    test_password = TEST_USER["password"] or "password"

    portal = AutomationPortal(page)
    checkout = CheckoutPage(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)
    cart_sidebar = CartSidebar(page)

    checkout_data = checkout_valid_data.copy()
    checkout_data[field_to_empty] = ""

    await portal.navigate()
    await portal.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.fill_login_popup(test_email, test_password)
    await login_popup.submit_login_popup()
    await page.keyboard.press("Escape") # To remove bugged overlay in "My Account" page
    await navbar.open_cart_sidebar()
    await cart_sidebar.click_tos_checkbox()
    await cart_sidebar.go_to_checkout()
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
    assert not order_placed, f"F: Order was placed with required field {field_to_empty} empty"
