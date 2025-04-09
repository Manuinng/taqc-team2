import pytest
from config.config import TEST_USER
from pages import AutomationPortal, CheckoutPage, Navbar, LoginPopup, CartSidebar

@pytest.mark.asyncio(loop_scope = "module")
async def test_checkout(browser):
    page = await browser.new_page()
    order_saved_message = page.locator("p:has-text('Order saved successfully!')")

    portal = AutomationPortal(page)
    checkout = CheckoutPage(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)
    cart_sidebar = CartSidebar(page)

    await portal.navigate()
    await portal.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.fill_login_popup(TEST_USER["email"], TEST_USER["password"])
    await login_popup.submit_login_popup()
    await page.keyboard.press("Escape") # To remove bugged overlay in "My Account" page
    await navbar.open_cart_sidebar()
    await cart_sidebar.click_tos_checkbox()
    await cart_sidebar.go_to_checkout()
    await checkout.fill_billing_details("first", "last", "Spain", "city", "address", "phone", "email", "notes")
    await checkout.apply_discount_code("discount")
    await checkout.fill_credit_card_details("4242424242424242", "12/12", "123")
    await checkout.click_tos_checkbox()
    await checkout.place_order()

    await order_saved_message.scroll_into_view_if_needed(timeout=5000)
    order_placed = await order_saved_message.is_visible()
    assert order_placed, "F: Order with correct details wasn't placed (5s timeout)"
