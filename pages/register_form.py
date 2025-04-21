from playwright.async_api import Page

class RegisterForm:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = "input[name='firstName']"
        self.last_name = "input[name='lastName']"
        self.email = "form#register-form input[name='email']"
        self.password = "input[name='password']"
        self.register_button = "button[type='submit']:has-text('Register')"

    async def __fill_input(self, selector, value):
        await self.page.locator(selector).scroll_into_view_if_needed()
        await self.page.fill(selector, value)

    async def fill_registration_form(self, first_name=None, last_name=None, email=None, password=None):
        print("Esperando que el formulario de registro esté visible...")
        await self.page.wait_for_selector("form#register-form", timeout=5000)

        fields = [
            (self.first_name, first_name),
            (self.last_name, last_name),
            (self.email, email),
            (self.password, password),
        ]

        for selector, value in fields:
            if value:
                print(f"Rellenando el campo: {selector} con el valor: {value}")
                await self.page.locator(selector).wait_for(state="visible", timeout=3000)
                await self.page.fill(selector, value)

    async def submit_registration(self):
        await self.page.locator(self.register_button).scroll_into_view_if_needed()
        await self.page.click(self.register_button)
