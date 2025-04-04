import pytest_asyncio
from playwright.async_api import async_playwright
from models.Product import Product
from models.HomePage import HomePage

URL = "https://automation-portal-bootcamp.vercel.app"
@pytest_asyncio.fixture(scope="function")
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded")
        home = HomePage(page)
        await home.popup()
        yield page
        await browser.close()

@pytest_asyncio.fixture
async def product(page):
    product = Product(page)
    return product