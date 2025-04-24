from playwright.async_api import async_playwright
from Product.pages.automation_portal import AutomationPortal
from pages.Registration import Registration
from pages.Login import Login
from pages.Product import Product
from config.config import data
import asyncio

URL = "https://automation-portal-bootcamp.vercel.app"
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded")

        home = AutomationPortal(page)
        await home.newclose_newsletter_popup()

        product = Product(page)
        await product.selectProduct()
        await product.addCart(data.input_infinity)

        await browser.close()

asyncio.run(main())