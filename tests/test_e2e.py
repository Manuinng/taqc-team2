import pytest
import asyncio
from pages import AutomationPortal, LoginPopup, CheckoutPage, ProductPage, RegisterForm, Navbar, CartSidebar, LoginForm  
from tests.utils.common_utils import load_json, camel_to_snake
from tests.utils.api_helper import APIHelper
from tests.test_data.quantity_data import data
from config.config import BASE_URL


@pytest.mark.asyncio(loop_scope="module")
async def test_success_purchase_product(setup_e2e):
    home = AutomationPortal(setup_e2e)
    navbar = Navbar(setup_e2e)
    loginpopup= LoginPopup(setup_e2e)
    register = RegisterForm(setup_e2e)
    login = LoginForm(setup_e2e)
    navbar = Navbar(setup_e2e)
    product = ProductPage(setup_e2e)
    cart = CartSidebar(setup_e2e)
    checkout_page = CheckoutPage(setup_e2e)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await loginpopup.open_new_customer_popup()
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "12345")
    await register.submit_registration()
    await login.fill_login_form("test9999@example.com", "12345")
    await login.submit_login()
    await navbar.navigate_to_home()
    await home.close_newsletter_popup()
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    await cart.go_to_checkout()
    checkout_data = load_json("checkout_valid_data.json")
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()

    order_data = APIHelper.get_order(order_id)
    order_api_id = order_data.pop("id", None)
    order_data.pop("createdAt", None)
    cart_data = order_data.pop("items", [])

    errors = []
    for product in cart_data:
        product.pop("id", None)
        for key, value in product.items():
            if key == "orderId":
                reference = order_api_id
            else:
                reference = product.get(key, None)
            if value != reference:
                errors.append(f"Product {key} mismatch: reference = {reference}, saved = {value}")

    for key, value in order_data.items():
        key = camel_to_snake(key)
        reference = checkout_data.get(key, None)
        if value != reference:
            errors.append(f"Order {key} mismatch: reference = {reference}, saved = {value}")

    assert not errors, "Order data mismatch (check complete message for details)\n" + '\n'.join(errors)

@pytest.mark.asyncio(loop_scope="module")
async def test_purchase_with_account(setup_page):
    home = AutomationPortal(setup_page)
    navbar = Navbar(setup_page)
    loginpopup= LoginPopup(setup_page)
    navbar = Navbar(setup_page)
    product = ProductPage(setup_page)
    cart = CartSidebar(setup_page)
    checkout_page = CheckoutPage(setup_page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await loginpopup.fill_login_popup("team2@taqc.com", "team2")
    await loginpopup.submit_login_popup()
    await navbar.navigate_to_home()
    await home.close_newsletter_popup()
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    await cart.go_to_checkout()
    checkout_data = load_json("checkout_valid_data.json")
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()

    order_data = APIHelper.get_order(order_id)
    order_api_id = order_data.pop("id", None)
    order_data.pop("createdAt", None)
    cart_data = order_data.pop("items", [])

    errors = []
    for product in cart_data:
        product.pop("id", None)
        for key, value in product.items():
            if key == "orderId":
                reference = order_api_id
            else:
                reference = product.get(key, None)
            if value != reference:
                errors.append(f"Product {key} mismatch: reference = {reference}, saved = {value}")

    for key, value in order_data.items():
        key = camel_to_snake(key)
        reference = checkout_data.get(key, None)
        if value != reference:
            errors.append(f"Order {key} mismatch: reference = {reference}, saved = {value}")

    assert not errors, "Order data mismatch (check complete message for details)\n" + '\n'.join(errors)

@pytest.mark.asyncio(loop_scope="module")
async def test_purchase_product_without_account(setup_page):
    home = AutomationPortal(setup_page)
    product = ProductPage(setup_page)
    cart = CartSidebar(setup_page)
    checkout_page = CheckoutPage(setup_page)

    await home.navigate()
    await home.close_newsletter_popup()
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    await cart.go_to_checkout()
    checkout_data = load_json("checkout_valid_data.json")
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()

    order_data = APIHelper.get_order(order_id)
    order_api_id = order_data.pop("id", None)
    order_data.pop("createdAt", None)
    cart_data = order_data.pop("items", [])

    errors = []
    for product in cart_data:
        product.pop("id", None)
        for key, value in product.items():
            if key == "orderId":
                reference = order_api_id
            else:
                reference = product.get(key, None)
            if value != reference:
                errors.append(f"Product {key} mismatch: reference = {reference}, saved = {value}")

    for key, value in order_data.items():
        key = camel_to_snake(key)
        reference = checkout_data.get(key, None)
        if value != reference:
            errors.append(f"Order {key} mismatch: reference = {reference}, saved = {value}")

    assert not errors, "Order data mismatch (check complete message for details)\n" + '\n'.join(errors)

@pytest.mark.asyncio(loop_scope="module")
async def test_add_two_product_remove_one(setup_page):
    home = AutomationPortal(setup_page)
    navbar = Navbar(setup_page)
    loginpopup= LoginPopup(setup_page)
    navbar = Navbar(setup_page)
    product = ProductPage(setup_page)
    cart = CartSidebar(setup_page)
    checkout_page = CheckoutPage(setup_page)

    await home.navigate()
    await home.close_newsletter_popup()
    await navbar.navigate_to_account()
    await loginpopup.fill_login_popup("team2@taqc.com", "team2")
    await loginpopup.submit_login_popup()
    await navbar.navigate_to_home()
    await home.close_newsletter_popup()
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    await cart.close_cart_sidebar()
    await navbar.navigate_to_home()
    await home.close_newsletter_popup()
    await product.addingSecondProduct()
    await cart.remove_product_from_cart()
    await cart.go_to_checkout()
    checkout_data = load_json("checkout_valid_data.json")
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()

    order_data = APIHelper.get_order(order_id)
    order_api_id = order_data.pop("id", None)
    order_data.pop("createdAt", None)
    cart_data = order_data.pop("items", [])

    errors = []
    for product in cart_data:
        product.pop("id", None)
        for key, value in product.items():
            if key == "orderId":
                reference = order_api_id
            else:
                reference = product.get(key, None)
            if value != reference:
                errors.append(f"Product {key} mismatch: reference = {reference}, saved = {value}")

    for key, value in order_data.items():
        key = camel_to_snake(key)
        reference = checkout_data.get(key, None)
        if value != reference:
            errors.append(f"Order {key} mismatch: reference = {reference}, saved = {value}")

    assert not errors, "Order data mismatch (check complete message for details)\n" + '\n'.join(errors)