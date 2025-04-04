import asyncio
from playwright.async_api import async_playwright
from models.automation_portal import AutomationPortal
from models.register_form import RegisterForm
from models.login_form import LoginForm
import random
import string

async def register():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()

        portal = AutomationPortal(page)
        register_form = RegisterForm(page)
        login_form = LoginForm(page)

        await portal.navigate()
        await portal.close_newsletter_popup()
        await portal.open_login_popup()
        await portal.open_new_customer_popup()
        await portal.navigate_to_register()

        def generate_random_email():
            return "a@" + ''.join(random.choices(string.ascii_lowercase, k=1)) + ".cl"

        email_generated = generate_random_email()

        await register_form.fill_registration_form(
            first_name="Prueba",
            last_name="Prueba",
            email=email_generated,
            password="12345"
        )
        await register_form.submit_registration()
        await login_form.fill_login_form(email=email_generated, password="12345")
        await login_form.submit_login()
        await portal.navigate_to_home()
        await portal.close_newsletter_popup()
    
        await browser.close()

if __name__ == "__main__":
    asyncio.run(register())
