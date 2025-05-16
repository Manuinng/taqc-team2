from playwright.async_api import Page
from config.config import BASE_URL

class LoginPopup:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = "div.tf-field input[type='email']"
        self.password_input = "div.tf-field input[type='password']"
        self.login_button = "button:has-text('Log in')"
        self.close_button = ".icon-close.icon-close-popup"
        self.new_customer_button_selector = "button.btn-link:has-text('New customer? Create your account')"
        self.register_button_selector = "a:has-text('Register')"

    async def fill_login_popup(self, email: str, password: str):
        await self.page.wait_for_selector(self.email_input)
        await self.page.fill(self.email_input, email)
        await self.page.fill(self.password_input, password)

    async def submit_login_popup(self):
        await self.page.wait_for_selector(self.login_button)
        await self.page.click(self.login_button)
        await self.page.wait_for_url(f"{BASE_URL}/my-account")
        await self.page.keyboard.press("Escape")

    async def close_login_popup(self):
        await self.page.wait_for_selector(self.close_button)
        await self.page.click(self.close_button)
        
    async def open_new_customer_popup(self):
        await self.page.wait_for_selector(self.new_customer_button_selector, timeout=5000)
        await self.page.wait_for_timeout(1000)
        await self.page.click(self.new_customer_button_selector)
