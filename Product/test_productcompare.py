from playwright.async_api import async_playwright
from models.HomePage import HomePage
from models.registration import Registration
from models.Login import Login
from models.Product import Product
from config.data import data
import asyncio

URL = "https://automation-portal-bootcamp.vercel.app"
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded")

        home = HomePage(page)
        await home.popup()

        product = Product(page)
        await product.selectProduct()
        await product.viewCompare()

        await browser.close()

asyncio.run(main())