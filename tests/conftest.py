import pytest
import pytest_asyncio
from config.config import TEST_USER
from utils.api_helper import APIHelper
from playwright.async_api import async_playwright, Browser, Cookie
from pages.automation_portal import AutomationPortal
from pages.register_form import RegisterForm
from pages.login_form import LoginForm
from pages.components import Navbar, CartSidebar, LoginPopup

def pytest_addoption(parser):
    parser.addoption("--no-headless", action="store_false", default=True, help="Run tests with GUI instead of headless")

@pytest.fixture(scope="session", autouse=True)
def cleanup_user():
    emails_to_cleanup = ["test9999@example.com", "a@a"]
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

@pytest_asyncio.fixture(scope="function")
async def browser(request):
    headless_cmd = request.config.getoption("--no-headless")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_cmd)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(scope="function")
async def browser_page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

@pytest_asyncio.fixture(scope="function")
async def portal_page(browser_page):
    return {
        "home": AutomationPortal(browser_page),
        "register": RegisterForm(browser_page),
        "login": LoginForm(browser_page),
        "navbar": Navbar(browser_page),
        "cart_sidebar": CartSidebar(browser_page),
        "login_popup": LoginPopup(browser_page),
    }

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: marks a test as asynchronous")