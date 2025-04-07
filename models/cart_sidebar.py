from config.config import BASE_URL

class CartSidebar:
    def __init__(self, page):
        self.page = page

    async def open(self):
        await self.page.click("li.nav-cart a.nav-icon-item")

    async def click_tos_checkbox(self):
        tos_checkbox_selector = "input#CartDrawer-Form_agree"
        await self.page.wait_for_selector(tos_checkbox_selector)
        await self.page.click(tos_checkbox_selector)

    async def go_to_checkout(self):
        checkout_button_selector = "a.tf-btn.btn-fill.animate-hover-btn.radius-3.w-100.justify-content-center:has-text('Check out')"
        await self.page.wait_for_selector(checkout_button_selector)
        await self.page.click(checkout_button_selector)
        await self.page.wait_for_url(f"{BASE_URL}/checkout")
