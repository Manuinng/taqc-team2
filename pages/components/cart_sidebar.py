from playwright.async_api import Page
from config.config import BASE_URL

class CartSidebar:
    def __init__(self, page: Page):
        self.page = page
        self.tos_checkbox = "input#CartDrawer-Form_agree"
        self.checkout_button = "a.tf-btn.btn-fill.animate-hover-btn.radius-3.w-100.justify-content-center:has-text('Check out')"

    async def click_tos_checkbox(self):
        await self.page.wait_for_selector(self.tos_checkbox)
        await self.page.click(self.tos_checkbox)

    async def go_to_checkout(self):
        await self.page.wait_for_selector(self.checkout_button)
        await self.page.click(self.checkout_button)
        await self.page.wait_for_url(f"{BASE_URL}/checkout")
