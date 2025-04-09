import pytest_asyncio
from config.config import TEST_USER
from playwright.async_api import async_playwright

@pytest_asyncio.fixture(loop_scope="module")
async def checkout_valid_data():
    yield {
        "first_name": "first",
        "last_name": "last",
        "country": "Spain",
        "city": "city",
        "address": "address",
        "phone": "987654321",
        "email": TEST_USER["email"] or "email@example.com",
        "notes": "notes",
        "discount_code": "discount",
        "card_number": "4242424242424242",
        "card_date": "12/12",
        "card_cvc": "123",
        "tos_checkbox": True
    }

@pytest_asyncio.fixture(loop_scope="module")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()
