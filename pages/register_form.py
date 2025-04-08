from playwright.async_api import Page

class RegisterForm:
    def __init__(self, page: Page):
        self.page = page

    async def fill_registration_form(self, first_name: str, last_name: str, email: str, password: str):
        print("Llenando el formulario de registro...")
        await self.page.fill("input[name='firstName']", first_name)
        await self.page.fill("input[name='lastName']", last_name)
        await self.page.fill("input[name='email']", email)
        await self.page.fill("input[name='password']", password)
        await self.page.wait_for_timeout(3000)

    async def submit_registration(self):
        print("Enviando el formulario de registro...")
        register_button_selector = "button[type='submit']"
        await self.page.wait_for_selector(register_button_selector, timeout=5000)
        await self.page.wait_for_timeout(2000)
        await self.page.click(register_button_selector)
