import pytest
import asyncio
from pages import AutomationPortal, LoginPopup, CheckoutPage, ProductPage, RegisterForm, Navbar, CartSidebar, LoginForm  
from tests.utils.common_utils import load_json, camel_to_snake
from tests.utils.api_helper import APIHelper
from tests.test_data.quantity_data import data
from config.config import BASE_URL


@pytest.mark.asyncio(loop_scope="module")
async def test_success_purchase_product(browser):
    page = await browser.new_page() 
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    navbar = Navbar(page)
    loginpop= LoginPopup(page)
    await navbar.navigate_to_account()
    await loginpop.open_new_customer_popup()
    register = RegisterForm(page)
    await register.fill_registration_form("FirstName", "LastName", "test9999@example.com", "12345")
    await register.submit_registration()
    login = LoginForm(page)
    await login.fill_login_form("test9999@example.com", "12345")
    await login.submit_login()
    navbar = Navbar(page)
    await navbar.navigate_to_home()
    await home.close_newsletter_popup()
    product = ProductPage(page)
    await product.selectProduct()
    await product.addCart(data.input_success)
    assert product.get_information_cart, "The product was not found in the cart."
    cart = CartSidebar(page)
    await cart.go_to_checkout()
    checkout_page = CheckoutPage(page)
    checkout_data = load_json("checkout_valid_data.json")
    await checkout_page.fill_form(checkout_data)
    order_id = await checkout_page.place_order()
    assert order_id, f"Valid order wasn't placed after 2s"

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

    assert not errors, f"Order data mismatch (check complete message for details)\n{'\n'.join(errors)}"

    user_id = APIHelper.get_user_id("test9999@example.com")
    assert user_id
    assert APIHelper.delete_user(user_id)
