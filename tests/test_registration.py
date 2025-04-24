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
            ("firstName", first_name, "The first name field is invalid."),
            ("lastName", last_name, "The last name field is invalid."),
            ("email", email, "The email field is invalid."),
            ("password", password, "The password field is invalid."),
        ]

        is_negative_test = expected_outcome.startswith("failure")
        validation_errors = []

        for field_name, value, error_message in fields_to_validate:
            selector = f"form#register-form input[name='{field_name}']"
            if value:
                is_valid = await page.evaluate(
                    """(field) => field.checkValidity()""",
                    await page.query_selector(selector)
                )
                if not is_valid:
                    validation_errors.append(f"{error_message} Value: '{value}'")
            else:
                is_required = await page.evaluate(
                    """(field) => field.required""",
                    await page.query_selector(selector)
                )
                if is_required:
                    validation_errors.append(f"The field '{field_name}' is required but empty.")

        if validation_errors:
            print("Validation errors detected:")
            for error in validation_errors:
                print(error)
            if not is_negative_test:
                pytest.fail(f"Test case '{test_name}' failed: Validation errors detected for success case.")
            else:
                print(f"Test {test_name}: Form submission blocked as expected for {expected_outcome}")
                return

        await register.submit_registration()
        await page.wait_for_timeout(2000)

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

        if is_negative_test:
            if login_successful:
                pytest.fail(f"Test case '{test_name}' failed: Unexpected successful login for {expected_outcome}.")
            else:
                print(f"Test {test_name}: Login failed as expected for {expected_outcome}")
        else:
            if login_successful:
                user_id = APIHelper.get_user_id(email)
                if user_id:
                    if APIHelper.delete_user(user_id):
                        print(f"User with ID {user_id} deleted successfully")
                    else:
                        print(f"Error deleting user with ID {user_id}")
                else:
                    print(f"Could not retrieve user ID for email {email}")
                print("Result: Success as expected")
            else:
                pytest.fail(f"Test case '{test_name}' failed: Login failed when success was expected.")

    except TimeoutError:
        print(f"Timeout reached in test case '{test_name}'. Closing the test.")
        pytest.fail(f"Test case '{test_name}' failed: Timeout reached.")

@pytest.mark.parametrize("test_data", [
    pytest.param(("Valid registration", "FirstName", "LastName", "test9999@example.com", "12345", "success")),
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
    pytest.param(("Duplicate email registration", "FirstName", "LastName", "team2@taqc.com", "12345", "failure - email already in use")),
    pytest.param(("Missing all fields", "", "", "", "", "failure - all fields required")),
    pytest.param(("Email with special characters", "FirstName", "LastName", "test!@domain.com", "12345", "failure - invalid email")),
    pytest.param(("Email without domain", "FirstName", "LastName", "test@", "12345", "failure - invalid email")),
    pytest.param(("Password with only numbers", "FirstName", "LastName", "test9999@example.com", "12345678", "failure - weak password")),
    pytest.param(("Password with only letters", "FirstName", "LastName", "test9999@example.com", "abcdefgh", "failure - weak password")),
    pytest.param(("Password with special characters only", "FirstName", "LastName", "test9999@example.com", "@#$%^&*", "failure - weak password")),
    pytest.param(("Very long email", "FirstName", "LastName", "test" + "a" * 250 + "@example.com", "12345", "failure - email too long")),
    pytest.param(("First name exceeding character limit", "A" * 100, "LastName", "test9999@example.com", "12345", "failure - first name too long")),
    pytest.param(("Last name exceeding character limit", "FirstName", "B" * 100, "test9999@example.com", "12345", "failure - last name too long")),
])
@pytest.mark.asyncio
async def test_registration_cases(portal_page, test_data):
    test_name, first_name, last_name, email, password, expected_outcome = test_data
    await run_test_case(portal_page, test_name, first_name, last_name, email, password, expected_outcome)