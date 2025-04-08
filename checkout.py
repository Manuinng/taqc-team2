import asyncio
from playwright.async_api import async_playwright
from pages import AutomationPortal, CheckoutPage, Navbar, LoginPopup, CartSidebar

async def checkout():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        portal = AutomationPortal(page)
        checkout = CheckoutPage(page)
        navbar = Navbar(page)
        login_popup = LoginPopup(page)
        cart_sidebar = CartSidebar(page)

        await portal.navigate()
        await portal.close_newsletter_popup()
        await navbar.navigate_to_account()
        await login_popup.fill_login_popup("team2@taqc.com", "team2")
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

        await asyncio.sleep(5)
        await browser.close()

asyncio.run(checkout())
