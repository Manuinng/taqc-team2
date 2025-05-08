from playwright.async_api import Page
from config.config import BASE_URL

class Navbar:
    def __init__(self, page: Page):
        self.page = page
        self.cart_button = "li.nav-cart a.nav-icon-item"
        self.account_button = "li.nav-account a.nav-icon-item"
        self.wishlist = "li.nav-wishlist a.nav-icon-item"
        self.home = "#header > div > div > div.col-xl-3.col-md-4.col-6 > a"

    async def open_cart_sidebar(self):
        await self.page.click(self.cart_button)

    async def navigate_to_account(self, logged_in: bool = False):
        await self.page.click(self.account_button)
        if logged_in:
            await self.page.wait_for_url(f"{BASE_URL}/my-account")

    async def open_wishlist(self):
        await self.page.click(self.wishlist)

    async def navigate_to_home(self):
        await self.page.click(self.home)
        await self.page.wait_for_url(f"{BASE_URL}")
