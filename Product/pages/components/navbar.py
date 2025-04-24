from playwright.async_api import Page
from config.config import url

class Navbar:
    def __init__(self, page: Page):
        self.page = page
        self.cart_button = "li.nav-cart a.nav-icon-item"
        self.account_button = "li.nav-account a.nav-icon-item"
        self.wishlist = "li.nav-wishlist a.nav-icon-item"

    async def open_cart_sidebar(self):
        await self.page.click(self.cart_button)

    async def navigate_to_account(self, logged_in: bool = False):
        await self.page.click(self.account_button)
        if logged_in:
            await self.page.wait_for_url(f"{url.BASE_URL}/my-account")

    async def open_wishlist(self):
        await self.page.click(self.wishlist)