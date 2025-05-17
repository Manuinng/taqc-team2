import pytest
from pages import AutomationPortal, LoginPopup, CheckoutPage, ProductPage, RegisterForm, Navbar, CartSidebar, LoginForm
from tests.test_data.quantity_data import data

@pytest.mark.asyncio(loop_scope="module")
async def test_success_purchase_product(setup_e2e, valid_billing_details, valid_credit_card_info):
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
    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()
    api_errors = await checkout_page.validate_api_order(
        order_id,
        valid_billing_details | valid_credit_card_info
    )
    assert not api_errors, "API order data mismatch (check complete message for details)\n" + '\n'.join(api_errors)

@pytest.mark.asyncio(loop_scope="module")
async def test_purchase_with_account(setup_page, valid_billing_details, valid_credit_card_info):
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
    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()
    api_errors = await checkout_page.validate_api_order(
        order_id,
        valid_billing_details | valid_credit_card_info
    )
    assert not api_errors, "API order data mismatch (check complete message for details)\n" + '\n'.join(api_errors)

@pytest.mark.asyncio(loop_scope="module")
async def test_purchase_product_without_account(setup_page, valid_billing_details, valid_credit_card_info):
    home = AutomationPortal(setup_page)
    product = ProductPage(setup_page)
    cart = CartSidebar(setup_page)
    checkout_page = CheckoutPage(setup_page)

    await home.navigate()
    await home.close_newsletter_popup()
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    await cart.go_to_checkout()
    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()
    api_errors = await checkout_page.validate_api_order(
        order_id,
        valid_billing_details | valid_credit_card_info
    )
    assert not api_errors, "API order data mismatch (check complete message for details)\n" + '\n'.join(api_errors)

@pytest.mark.asyncio(loop_scope="module")
async def test_add_two_product_remove_one(setup_page, valid_billing_details, valid_credit_card_info):
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
    await checkout_page.fill_billing_details(**valid_billing_details)
    await checkout_page.apply_discount_code("TESTDISCOUNT")
    await checkout_page.fill_credit_card_info(**valid_credit_card_info)
    await checkout_page.click_tos_checkbox()
    order_id = await checkout_page.place_order()
    api_errors = await checkout_page.validate_api_order(
        order_id,
        valid_billing_details | valid_credit_card_info
    )
    assert not api_errors, "API order data mismatch (check complete message for details)\n" + '\n'.join(api_errors)
