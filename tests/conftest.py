import pytest
import pytest_asyncio
from config.config import TEST_USER
from utils.api_helper import APIHelper
from playwright.async_api import async_playwright
from pages.automation_portal import AutomationPortal
from pages.register_form import RegisterForm
from pages.login_form import LoginForm
from pages.components import Navbar, CartSidebar, LoginPopup

@pytest.fixture(scope="session", autouse=True)
def cleanup_user():
    emails_to_cleanup = ["test9999@example.com", "a@a"]
    for email in emails_to_cleanup:
        user_id = APIHelper.get_user_id(email)
        if user_id:
            print(f"Usuario existente encontrado con ID {user_id} para el correo {email}. Intentando eliminarlo...")
            if APIHelper.delete_user(user_id):
                print(f"Usuario con ID {user_id} eliminado exitosamente.")
            else:
                print(f"Error al intentar eliminar al usuario con ID {user_id}.")
        else:
            print(f"No se encontró un usuario existente para el correo {email}.")

# Fixture para inicializar el navegador
@pytest_asyncio.fixture(scope="function")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

# Fixture para proporcionar una nueva página del navegador para cada prueba
@pytest_asyncio.fixture(scope="function")
async def browser_page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

# Fixture para inicializar los objetos de página necesarios para las pruebas
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
    config.addinivalue_line("markers", "asyncio: marca una prueba como asíncrona")