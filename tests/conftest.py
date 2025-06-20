import pytest
import pytest_asyncio
import requests
from typing import List, Tuple, Dict, Any, AsyncGenerator
from playwright.async_api import async_playwright, Browser, Page, Cookie
from config.config import TEST_USER
from tests.utils.api_helper import APIHelper
from tests.utils.common_utils import load_json
from pages import AutomationPortal, Navbar, LoginPopup, CheckoutPage


def pytest_addoption(parser):
    parser.addoption(
        "--no-headless",
        action="store_false",
        default=True,
        help="Run tests with GUI instead of headless"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: marks a test as asynchronous")


@pytest_asyncio.fixture(loop_scope="module")
async def browser(request) -> AsyncGenerator[Browser, None]:
    headless_cmd = request.config.getoption("--no-headless")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_cmd)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(loop_scope="module")
async def setup_checkout(browser, session: List[Cookie]) -> CheckoutPage:
    context = await browser.new_context()

    await context.add_cookies(session)
    valid_cart_data = load_json("valid_cart_data.json")
    await context.add_init_script(f"localStorage.setItem('cartList', JSON.stringify({valid_cart_data}))")

    page = await context.new_page()
    checkout_page = CheckoutPage(page)
    await checkout_page.navigate()

    return checkout_page

@pytest_asyncio.fixture(loop_scope="module")
async def setup_session(browser, session: List[Cookie]) -> Tuple[Page]:
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    return page

@pytest_asyncio.fixture(loop_scope="module")
async def setup_e2e(browser) -> AsyncGenerator[Page, None]:
    page = await browser.new_page()
    yield page
    user_id = APIHelper.get_user_id("temp_team2@example.com")
    if user_id:
        APIHelper.delete_user(user_id)

@pytest_asyncio.fixture(loop_scope="module")
async def setup_page(browser) -> AsyncGenerator[Page, None]:
    page = await browser.new_page()
    return page

@pytest_asyncio.fixture(loop_scope="module")
async def session() -> List[Cookie]:
    session = requests.Session()

    csrf_token = APIHelper.get_csrf_token(session)
    APIHelper.login(session, TEST_USER["email"], TEST_USER["password"], csrf_token)
    APIHelper.get_auth_session(session)

    context_cookies = []
    for cookie in session.cookies:
        context_cookies.append(Cookie(
            name=cookie.name,
            value=cookie.value,
            domain=cookie.domain,
            path=cookie.path,
            expires=cookie.expires or -1,
            httpOnly=cookie.has_nonstandard_attr('HttpOnly'),
            secure=cookie.secure,
            sameSite=cookie._rest.get('SameSite', None)
        ))

    return context_cookies


@pytest_asyncio.fixture(loop_scope="module")
async def session_ui() -> List[Cookie]:
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

        session = await page.context.cookies()
        await browser.close()
        return session
