import pytest_asyncio
from typing import Dict, List, Any, AsyncGenerator
from playwright.async_api import async_playwright, Browser, Cookie
from config.config import TEST_USER
from pages import AutomationPortal, Navbar, LoginPopup

@pytest_asyncio.fixture(loop_scope="module", scope="module")
async def checkout_valid_data() -> Dict[str, Any]:
    return {
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
async def browser() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(loop_scope="module", scope="module")
async def session() -> List[Cookie]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        test_email = TEST_USER["email"] or "email@example.com"
        test_password = TEST_USER["password"] or "password"

        portal = AutomationPortal(page)
        navbar = Navbar(page)
        login_popup = LoginPopup(page)

        await portal.navigate()
        await portal.close_newsletter_popup()
        await navbar.navigate_to_account()
        await login_popup.fill_login_popup(test_email, test_password)
        await login_popup.submit_login_popup()
        session =  await page.context.cookies()
        await browser.close()
        return session
