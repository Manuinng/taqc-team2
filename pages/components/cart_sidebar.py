from playwright.async_api import Page, expect
from config.config import BASE_URL

class CartSidebar:
    def __init__(self, page: Page):
        self.page = page
        self.tos_checkbox = "input#CartDrawer-Form_agree"
        self.checkout_button = "a.tf-btn.btn-fill.animate-hover-btn.radius-3.w-100.justify-content-center:has-text('Check out')"
        self.close_cart = "#shoppingCart > div > div > div.header > span"
        self.remove_product = "#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div:nth-child(1) > div.tf-mini-cart-info > div.tf-mini-cart-btns > div.tf-mini-cart-remove"

    async def click_tos_checkbox(self):
        await self.page.wait_for_selector(self.tos_checkbox)
        await self.page.click(self.tos_checkbox)

    async def go_to_checkout(self):
        await self.page.wait_for_selector(self.checkout_button)
        await self.page.click(self.checkout_button)
        await self.page.wait_for_url(f"{BASE_URL}/checkout")

    async def close_cart_sidebar(self):
        await expect(self.page.locator(self.close_cart), "The cart sidebar should be open.").to_be_visible()
        await self.page.click(self.close_cart)
        await expect(self.page.locator(self.close_cart), "The cart sidebar should be closed.").not_to_be_visible()

    async def remove_product_from_cart(self):
        await expect(self.page.locator(self.remove_product), "The remove product button should be visible.").to_be_visible()
        await self.page.click(self.remove_product)
        await expect(self.page.locator(self.remove_product), "The product should be removed from the cart.").to_be_visible()