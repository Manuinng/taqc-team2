import pytest_asyncio
from playwright.async_api import async_playwright
from pages.Product import Product
from pages.HomePage import HomePage
from config.data import url

@pytest_asyncio.fixture(scope="function")
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        home = HomePage(page)
        await home.navigate(url.BASE_URL)
        await home.popup()
        yield page
        await browser.close()

@pytest_asyncio.fixture
async def product(page):
    product = Product(page)
    return product