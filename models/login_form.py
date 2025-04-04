from playwright.async_api import Page

class LoginForm:
    def __init__(self, page: Page):
        self.page = page
        
    async def fill_login_form(self, email: str, password: str):
        print("Llenando el formulario de login...")
        await self.page.wait_for_timeout(2000)
        await self.page.fill("input#loginEmail", email)
        await self.page.fill("input#loginPassword", password)
        await self.page.wait_for_timeout(1000)
        
    async def submit_login(self):
        print("Presionando el botón Log in...")
        login_button_selector = "button:has-text('Log in')"
        await self.page.wait_for_selector(login_button_selector, timeout=5000)
        await self.page.wait_for_timeout(2000)
        await self.page.click(login_button_selector)
