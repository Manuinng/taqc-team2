import asyncio
from playwright.async_api import async_playwright
from models.automation_portal import AutomationPortal
from models.cart_sidebar import CartSidebar

async def checkout():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        portal = AutomationPortal(page)
        cart_sidebar = CartSidebar(page)

        await portal.navigate()
        await portal.close_newsletter_popup()

        # await portal.open_login_popup()
        # await portal.fill_login_popup("team2@taqc.com", "team2")
        # await portal.submit_login_popup()
        # await page.keyboard.press("Escape") # To remove bugged overlay in "My Account" page

        await cart_sidebar.open()
        await cart_sidebar.click_tos_checkbox()
        await cart_sidebar.go_to_checkout()

        await asyncio.sleep(5)
        await browser.close()

asyncio.run(checkout())
