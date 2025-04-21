import pytest
from config.config import BASE_URL
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

        fields_to_validate = [
            ("firstName", first_name, "El campo de nombre no es válido."),
            ("lastName", last_name, "El campo de apellido no es válido."),
            ("email", email, "El campo de email no es válido."),
            ("password", password, "El campo de contraseña no es válido."),
        ]

        for field_name, value, error_message in fields_to_validate:
            if value:
                selector = f"form#register-form input[name='{field_name}']"
                is_valid = await page.evaluate(
                    """(field) => field.checkValidity()""",
                    await page.query_selector(selector)
                )
                if not is_valid:
                    print(f"{error_message} Valor: '{value}'")
                    await register.submit_registration()
                    await page.wait_for_timeout(2000)
                    pytest.fail(f"Fallo en el caso de prueba '{test_name}': {error_message}")
            else:
                selector = f"form#register-form input[name='{field_name}']"
                is_required = await page.evaluate(
                    """(field) => field.required""",
                    await page.query_selector(selector)
                )
                if is_required:
                    print(f"El campo '{field_name}' es obligatorio pero está vacío.")
                    await register.submit_registration()
                    await page.wait_for_timeout(2000)
                    pytest.fail(f"Fallo en el caso de prueba '{test_name}': El campo '{field_name}' es obligatorio pero está vacío.")
        
        await register.submit_registration()

        print("Attempting login after registration...")
        await login.fill_login_form(email, password)
        await login.submit_login()

        try:
            await page.wait_for_url(BASE_URL + "/my-account", timeout=5000)
            login_successful = True
            print(f"Test {test_name}: Registration and login successful")
        except TimeoutError:
            login_successful = False
            print(f"Test {test_name}: Login failed after registration")
            
        if login_successful:
            user_id = APIHelper.get_user_id(email)
            if user_id:
                if APIHelper.delete_user(user_id):
                    print(f"User with ID {user_id} deleted successfully")
                else:
                    print(f"Error deleting user with ID {user_id}")
            else:
                print(f"Could not retrieve user ID for email {email}")

        if expected_outcome == "success":
            assert login_successful, f"Unexpected failure - success was expected"
            print("Result: Success as expected")
        else:
            assert not login_successful, f"Unexpected success - {expected_outcome} was expected"
            print(f"Result: Failure as expected - {expected_outcome}")

    except TimeoutError:
        print(f"Timeout alcanzado en el caso de prueba '{test_name}'. Cerrando el test.")
        pytest.fail(f"Fallo en el caso de prueba '{test_name}': Timeout alcanzado.")

@pytest.mark.parametrize("test_data", [
            pytest.param(("Invalid email", "FirstName", "LastName", "invalid_email", "12345", "failure - invalid email")),
            pytest.param(("Empty email", "FirstName", "LastName", "", "12345", "failure - email required")),
            pytest.param(("Email with spaces", "FirstName", "LastName", "test @domain.com", "12345", "failure - invalid email")),
            pytest.param(("Invalid email format", "FirstName", "LastName", "a@a", "12345", "failure - invalid email")),
            pytest.param(("Empty first name", "", "LastName", "test9999@example.com", "12345", "failure - first name required")),
            pytest.param(("Empty last name", "FirstName", "", "test9999@example.com", "12345", "failure - last name required")),
            pytest.param(("Empty password", "FirstName", "LastName", "test9999@example.com", "", "failure - password required")),
            pytest.param(("Short password", "FirstName", "LastName", "test9999@example.com", "123", "failure - password too short")),
            pytest.param(("Long password", "FirstName", "LastName", "test9999@example.com", "123456789012345678901234567890", "failure - password too long")),
            pytest.param(("Special characters in name", "First@Name", "Last#Name", "test9999@example.com", "12345", "failure - invalid name")),
            pytest.param(("Whitespace-only first name", "   ", "LastName", "test9999@example.com", "12345", "failure - first name required")),
            pytest.param(("Whitespace-only last name", "FirstName", "   ", "test9999@example.com", "12345", "failure - last name required")),
            pytest.param(("Whitespace-only password", "FirstName", "LastName", "test9999@example.com", "   ", "failure - password required")),
        
])

@pytest.mark.asyncio
async def test_registration_cases(portal_page, test_data):
    test_name, first_name, last_name, email, password, expected_outcome = test_data
    await run_test_case(portal_page, test_name, first_name, last_name, email, password, expected_outcome)
