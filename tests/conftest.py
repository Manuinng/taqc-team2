import pytest
import pytest_asyncio
import requests
from typing import List, AsyncGenerator
from playwright.async_api import async_playwright, Browser, Cookie

from config.config import BASE_URL, TEST_USER
from tests.utils.api_helper import APIHelper
from pages import AutomationPortal, Navbar, LoginPopup
from pages.automation_portal import AutomationPortal as AutoPortal
from pages.register_form import RegisterForm
from pages.login_form import LoginForm
from pages.components import CartSidebar


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


@pytest.fixture(scope="session", autouse=True)
def cleanup_user():
    emails_to_cleanup = ["test9999@example.com", "a@a", "test!@domain.com"]
    for email in emails_to_cleanup:
        user_id = APIHelper.get_user_id(email)
        if user_id:
            print(f"Existing user found with ID {user_id} for email {email}. Trying to delete...")
            if APIHelper.delete_user(user_id):
                print(f"User with ID {user_id} successfully deleted.")
            else:
                print(f"Error trying to delete user with ID {user_id}.")
        else:
            print(f"No existing user found for the email {email}.")


@pytest_asyncio.fixture(loop_scope="module")
async def browser(request, session) -> AsyncGenerator[Browser, None]:
    headless_cmd = request.config.getoption("--no-headless")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_cmd)
        context = await browser.new_context()
        await context.add_cookies(session)
        page = await context.new_page()
        yield page
        await browser.close()


@pytest_asyncio.fixture(scope="function")
async def browser_page(browser):
    page = await browser.new_page()
    yield page
    await page.close()


@pytest_asyncio.fixture(scope="function")
async def portal_page(browser_page):
    return {
        "home": AutoPortal(browser_page),
        "register": RegisterForm(browser_page),
        "login": LoginForm(browser_page),
        "navbar": Navbar(browser_page),
        "cart_sidebar": CartSidebar(browser_page),
        "login_popup": LoginPopup(browser_page),
    }


@pytest_asyncio.fixture(loop_scope="module")
async def session() -> List[Cookie]:
    session = requests.Session()

    response_csrf = session.get(f"{BASE_URL}/api/auth/csrf")
    if response_csrf.status_code == 200:
        csrf_token = response_csrf.json().get('csrfToken')
    else:
        raise requests.exceptions.HTTPError(f"Failed to retrieve CSRF token: {response_csrf.status_code}")

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
