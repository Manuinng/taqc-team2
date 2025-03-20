from playwright.async_api import async_playwright
from models.HomePage import HomePage
from models.Registration import Registration
from models.Login import Login
import asyncio

URL = "https://automation-portal-bootcamp.vercel.app"
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded")

        home = HomePage(page)
        await home.popup()
        await home.registerHome()

        registration = Registration(page)
        await registration.register()

        login = Login(page)
        await login.LogIN()
        await browser.close()

asyncio.run(main())