import pytest
import asyncio
from playwright.async_api import expect
from tests.test_data.quantity_data import data
from pages import ProductPage, AutomationPortal
from config.config import BASE_URL

@pytest.mark.asyncio(loop_scope="module")
async def test_success_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    product_information = await product.get_information_cart()
    await expect(product_information,"The product isn't in the cart.").to_be_visible()

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_infinity_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_infinity)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product should not be in the cart when using an infinite quantity.").not_to_be_visible()
    #assert not product.get_information_cart, "The product should not be in the cart when using an infinite quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_NaN_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_Nan)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product should not be in the cart when using a NaN quantity.").not_to_be_visible()
    #assert not product.get_information_cart, "The product should not be in the cart when using a NaN quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_zero_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_zero)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product should not be in the cart when using a Zero quantity.").not_to_be_visible()
    #assert not product.get_information_cart, "The product should not be in the cart when using a Zero quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_max_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_max)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product is added even with quantities that should reach the maximum available product.").not_to_be_visible()
    #assert not product.get_information_cart, "The product is added even with quantities that should reach the maximum available product."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_negative_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_neg)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product should not be in the cart when using a negative quantity.").not_to_be_visible()
    #assert not product.get_information_cart, "The product should not be in the cart when using a negative quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_eliminate_compare(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.viewCompare()
    get_product_compare = await product.get_product_compare()
    await expect(get_product_compare, "The comparison section is empty, there are no products to compare.").not_to_be_visible()
    #assert not product.get_product_compare , "The comparison section is empty, there are no products to compare."

@pytest.mark.asyncio(loop_scope="module")
async def test_int_value_quantity(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_int)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product should not be in the cart when using a numeral quantity.").not_to_be_visible()
    #assert not product.get_information_cart, "The product should not be in the cart when using a numeral quantity."

@pytest.mark.asyncio(loop_scope="module")
async def test_empty_product(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_empty)
    product_information = await product.get_information_cart()
    await expect(product_information, "The product should not be in the cart when it is empty.").not_to_be_visible()
    #assert not product.get_information_cart, "The product should not be in the cart when it is empty."

@pytest.mark.asyncio(loop_scope="module")
async def test_buy_with(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.buyOption()
    await expect(product.page, "The page has not been redirected to checkout.").to_have_url(f"{BASE_URL}/checkout")
    #assert "/checkout" in product.page.url, "The page has not been redirected to checkout."

@pytest.mark.asyncio(loop_scope="module")
async def test_categories_button(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.categoryOption()
    await expect(product.page, "The page was not redirected to categories.").to_have_url(f"{BASE_URL}/shop-default")
    #assert "/shop-default" in product.page.url, "The page was not redirected to categories."

@pytest.mark.asyncio(loop_scope="module")
async def test_compare_product_cart(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.addingProduct(data.input_success)
    get_compare_cart = await product.get_compare_cart()
    await expect(get_compare_cart, "The color of the product in the cart does not match.").not_to_have_text("Light gray")
    #assert product.get_compare_cart == "Light gray", "The color of the product in the cart does not match."

@pytest.mark.asyncio(loop_scope="module")
async def test_find_size(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.findOption()
    get_find_size = await product.get_find_size()
    await expect(get_find_size, "The 'Find Size' button is not working.").to_be_visible()
    #assert product.get_find_size, "The 'Find Size' button is not working."

@pytest.mark.asyncio(loop_scope="module")
async def test_wishlist_option(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    await product.wishlistOption()
    get_wishlist_info = await product.get_wishlist_info()
    await expect(get_wishlist_info, "The product was not added to the wishlist.").to_be_visible()
    #assert product.get_wishlist_info, "No products were found in the wishlist."

@pytest.mark.asyncio(loop_scope="module")
async def test_price_discount(setup_product):
    home = AutomationPortal(setup_product)
    await home.navigate()
    await home.close_newsletter_popup()
    product = ProductPage(setup_product)
    await product.selectProduct()
    get_actual_discount_price = await product.get_actual_discount_price()
    discount_price = await product.discountPrice()
    await expect(discount_price, "The discount price is not being applied correctly.").to_have_text(get_actual_discount_price)
    #assert product.get_actual_discount_price == product.discountPrice, "The discount is not being applied correctly."
