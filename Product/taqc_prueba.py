from playwright.async_api import async_playwright
from pages.HomePage import HomePage
from pages.registration import Registration
from pages.Login import Login
from pages.Product import Product
import asyncio

URL = "https://automation-portal-bootcamp.vercel.app"
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded")

        home = HomePage(page)
        await home.popup()
        #await home.registerHome()
        await home.productHome()

        product = Product(page)
        await product.viewCompare()
        await product.addCart()
        #registration = Registration(page)
        #await registration.register()

        #login = Login(page)
        #await login.LogIN()
        await browser.close()

asyncio.run(main())