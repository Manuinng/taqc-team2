import pytest
from utils.api_helper import APIHelper
from playwright.async_api import TimeoutError

@pytest.mark.asyncio
async def run_test_case(portal_page, test_name, first_name, last_name, email, password, expected_outcome="success"):
    home = portal_page["home"]
    register = portal_page["register"]
    login = portal_page["login"]
    navbar = portal_page["navbar"]
    login_popup = portal_page["login_popup"]
    page = home.page

    print(f"\nRunning test case: {test_name}")

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await login_popup.open_new_customer_popup()

    try:
        await page.wait_for_selector("form#register-form", timeout=3000)

        await register.fill_registration_form(first_name, last_name, email, password)

        email_selector = "form#register-form input[name='email']"
        is_email_valid = await page.evaluate(
            """(emailField) => emailField.checkValidity()""",
            await page.query_selector(email_selector)
        )
        if not is_email_valid:
            print(f"El campo de email '{email}' no es válido.")
            
            await register.submit_registration()
            
            await page.wait_for_timeout(2000)
            
            pytest.fail(f"Fallo en el caso de prueba '{test_name}': El email '{email}' no cumple con las validaciones.")

        await register.submit_registration()

        print("Attempting login after registration...")
        await login.fill_login_form(email, password)
        await login.submit_login()

        try:
            await page.wait_for_selector("a:has-text('Dashboard')", timeout=3000)
            login_successful = True
            print(f"Test {test_name}: Registration and login successful")
        except TimeoutError:
            login_successful = False
            print(f"Test {test_name}: Login failed after registration")

        if expected_outcome == "success":
            assert login_successful, f"Unexpected failure - success was expected"
            print("Result: Success as expected")
        else:
            assert not login_successful, f"Unexpected success - {expected_outcome} was expected"
            print(f"Result: Failure as expected - {expected_outcome}")

        if login_successful:
            user_id = APIHelper.get_user_id(email)
            if user_id:
                if APIHelper.delete_user(user_id):
                    print(f"User with ID {user_id} deleted successfully")
                else:
                    print(f"Error deleting user with ID {user_id}")
            else:
                print(f"Could not retrieve user ID for email {email}")

    except TimeoutError:
        print(f"Timeout alcanzado en el caso de prueba '{test_name}'. Cerrando el test.")
        pytest.fail(f"Fallo en el caso de prueba '{test_name}': Timeout alcanzado.")

@pytest.mark.parametrize("test_data", [
    pytest.param(("Invalid email", "FirstName", "LastName", "invalid_email", "12345", "failure - invalid email")),
    pytest.param(("Empty email", "FirstName", "LastName", "", "12345", "failure - email required")),
    pytest.param(("Email with spaces", "FirstName", "LastName", "test @domain.com", "12345", "failure - invalid email")),
    pytest.param(("Invalid email format", "FirstName", "LastName", "a@a", "12345", "failure - invalid email")),
])

@pytest.mark.asyncio
async def test_registration_cases(portal_page, test_data):
    test_name, first_name, last_name, email, password, expected_outcome = test_data
    await run_test_case(portal_page, test_name, first_name, last_name, email, password, expected_outcome)