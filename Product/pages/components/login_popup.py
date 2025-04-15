from playwright.async_api import Page
from config.data import url

class LoginPopup:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = "div.tf-field input[type='email']"
        self.password_input = "div.tf-field input[type='password']"
        self.login_button = "button:has-text('Log in')"
        self.close_button = ".icon-close.icon-close-popup"

    async def fill_login_popup(self, email: str, password: str):
        await self.page.wait_for_selector(self.email_input)
        await self.page.fill(self.email_input, email)
        await self.page.fill(self.password_input, password)

    async def submit_login_popup(self):
        await self.page.wait_for_selector(self.login_button)
        await self.page.click(self.login_button)
        await self.page.wait_for_url(f"{url.BASE_URL}/my-account")

    async def close_login_popup(self):
        await self.page.wait_for_selector(self.close_button)
        await self.page.click(self.close_button)