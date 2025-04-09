import pytest_asyncio
from playwright.async_api import async_playwright

@pytest_asyncio.fixture(loop_scope="module")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()
