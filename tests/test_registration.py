import pytest
from config.config import BASE_URL
from tests.utils.api_helper import APIHelper
from playwright.async_api import TimeoutError, expect
from pages.automation_portal import AutomationPortal as AutoPortal
from pages.register_form import RegisterForm
from pages.login_form import LoginForm
from pages import Navbar, LoginPopup

@pytest.fixture(autouse=True)
def cleanup_registration_user():
    from tests.utils.api_helper import APIHelper
    emails = ["test9999@example.com", "a@a", "test!@domain.com"]
    for email in emails:
        user_id = APIHelper.get_user_id(email)
        if user_id:
            APIHelper.delete_user(user_id)

@pytest.mark.asyncio(loop_scope="module")
async def test_valid_registration(browser):
    email = "test9999@example.com"
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)
    login = LoginForm(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", email, "12345")
    await register.submit_registration()
    await login.fill_login_form(email, "12345")
    await login.submit_login()
    await register.validate_registration_failed(f"{BASE_URL}/my-account")

    user_id = APIHelper.get_user_id(email)
    assert user_id
    assert APIHelper.delete_user(user_id)
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_invalid_email(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "invalid_email", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_empty_fields(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("", "", "", "")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_short_password(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test@domain.com", "123")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_empty_email(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_email_with_spaces(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test @domain.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_empty_first_name(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("", "LastName", "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_long_password(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "123456789012345678901234567890123456789012345678901234567890")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_duplicate_email(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "team2@taqc.com", "12345")
    await register.submit_registration()
    assert await page.is_visible("p.text-danger:has-text('User already exists.')")
    await context.close()
    
@pytest.mark.asyncio(loop_scope="module")
async def test_registration_invalid_password(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()
    
@pytest.mark.asyncio(loop_scope="module")
async def test_registration_empty_last_name(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "", "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_invalid_email_format(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "a@a", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_special_characters_in_name(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("First@Name", "Last#Name", "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_whitespace_only_first_name(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("   ", "LastName", "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_whitespace_only_last_name(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "   ", "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_whitespace_only_password(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "   ")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_email_with_special_characters(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test!@domain.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_email_without_domain(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test@", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_password_only_numbers(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "12345678")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_password_only_letters(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "abcdefgh")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_password_special_characters_only(browser):
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "@#$%^&*")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_very_long_email(browser):
    long_email = "test" + "xw" * 250 + "@example.com"
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", long_email, "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_long_first_name(browser):
    long_first_name = "ii" * 100
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form(long_first_name, "LastName", "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_registration_long_last_name(browser):
    long_last_name = "ww" * 100
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)
    register = RegisterForm(page)
    navbar = Navbar(page)
    login_popup = LoginPopup(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", long_last_name, "test9999@example.com", "12345")
    await register.submit_registration()
    await register.validate_registration_failed(f"{BASE_URL}/register")
    await context.close()