import pytest
import asyncio
from tests.test_data.quantity_data import data
from pages import ProductPage, AutomationPortal

@pytest.mark.asyncio(loop_scope="module")
async def test_success_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_success)
    assert product.get_information_cart, "The product was not found in the cart."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_infinity_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_infinity)
    assert not product.get_information_cart, "The product should not be in the cart when using an infinite quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_NaN_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_Nan)
    assert not product.get_information_cart, "The product should not be in the cart when using a NaN quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_zero_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_zero)
    assert not product.get_information_cart, "The product should not be in the cart when using a Zero quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_max_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_max)
    assert not product.get_information_cart, "The product is added even with quantities that should reach the maximum available product."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_negative_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_neg)
    await product.get_information_cart()
    assert not product.get_information_cart, "The product should not be in the cart when using a negative quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_eliminate_compare(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.viewCompare()
    assert not product.get_product_compare , "The comparison section is empty, there are no products to compare."

@pytest.mark.asyncio(loop_scope="module")
async def test_int_value_quantity(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_int)
    assert not product.get_information_cart, "The product should not be in the cart when using a numeral quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_empty_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_empty)
    assert not product.get_information_cart, "The product should not be in the cart when it is empty."

@pytest.mark.asyncio(loop_scope="module")
async def test_buy_with(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.buyOption()
    assert "/checkout" in product.page.url, "The page has not been redirected to checkout."

@pytest.mark.asyncio(loop_scope="module")
async def test_categories_button(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.categoryOption()
    assert "/shop-default" in product.page.url, "The page was not redirected to categories."

@pytest.mark.asyncio(loop_scope="module")
async def test_compare_product_cart(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addCart(data.input_success)
    assert product.get_compare_cart == "Light gray", "The color of the product in the cart does not match."

@pytest.mark.asyncio(loop_scope="module")
async def test_find_size(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.findOption()
    assert not product.get_find_size, "The 'Find Size' button is not working."

@pytest.mark.asyncio(loop_scope="module")
async def test_wishlist_option(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.wishlistOption()
    assert product.get_wishlist_info, "No products were found in the wishlist."

@pytest.mark.asyncio(loop_scope="module")
async def test_price_discount(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    assert product.get_actual_discount_price == product.discountPrice, "The discount is not being applied correctly."
