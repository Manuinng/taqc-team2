import pytest_asyncio
import requests
from typing import List, AsyncGenerator
from playwright.async_api import async_playwright, Browser, Cookie
from config.config import BASE_URL, TEST_USER
from pages import AutomationPortal, Navbar, LoginPopup

def pytest_addoption(parser):
    parser.addoption("--no-headless", action="store_false", default=True, help="run tests with the browser's GUI instead of headless mode")

@pytest_asyncio.fixture(loop_scope="module")
async def browser(request) -> AsyncGenerator[Browser, None]:
    headless_cmd = request.config.getoption("--no-headless")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_cmd)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(loop_scope="module", scope="module")
async def session() -> List[Cookie]:
    session = requests.Session()

    # GET CSRF Token
    response_csrf = session.get(f"{BASE_URL}/api/auth/csrf")
    if response_csrf.status_code == 200:
        csrf_token = response_csrf.json().get('csrfToken')
    else:
        raise requests.exceptions.HTTPError(f"Failed to retrieve CSRF token: {response_csrf.status_code}")

    # POST Login
    data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"],
        "redirect": "false",
        "csrfToken": csrf_token,
        "callbackUrl": f"{BASE_URL}/login",
        "json": "true"
    }
    response_login = session.post(f"{BASE_URL}/api/auth/callback/credentials", data=data)
    if response_login.status_code != 200:
        raise requests.exceptions.HTTPError(f"Login failed: {response_login.status_code}")

    # GET Session
    response_session = session.get(f"{BASE_URL}/api/auth/session")
    if response_session.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to retrieve session cookie: {response_session.status_code}")

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

@pytest_asyncio.fixture(loop_scope="module", scope="module")
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
        session =  await page.context.cookies()
        await browser.close()
        return session
