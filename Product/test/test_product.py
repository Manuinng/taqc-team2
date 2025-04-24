import pytest
import asyncio
from config.config import data, url
from pages import Product, AutomationPortal

@pytest.mark.asyncio(loop_scope="module")
async def test_success_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_success)
    #assert await product.get_field_validation_state("")
    assert product.get_information_cart, "El producto no se encontró en el carrito."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_infinity_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_infinity)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad infinita."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_NaN_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_Nan)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad NaN."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_zero_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_zero)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad Zero."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_max_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_max)
    assert not product.get_information_cart, "El producto se agrega aun con cantidades que deberian tocar el maximo de producto disponible."

@pytest.mark.asyncio(loop_scope="module")
async def test_fail_neg_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_neg)
    await product.get_information_cart()
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad negativa."

@pytest.mark.asyncio(loop_scope="module")
async def test_eliminate_compare(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.viewCompare()
    assert not product.get_product_compare , "La sección de comparación está vacía, no hay productos para comparar."

@pytest.mark.asyncio(loop_scope="module")
async def test_int_value(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_int)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad numeral."

@pytest.mark.asyncio(loop_scope="module")
async def test_empty_product(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_empty)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad numeral."

@pytest.mark.asyncio(loop_scope="module")
async def test_buy_with(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.buyOption()
    assert "/checkout" in product.page.url, "La pagina no ha sido direccionado a checkout"

@pytest.mark.asyncio(loop_scope="module")
async def test_categories_button(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.categoryOption()
    assert "/shop-default" in product.page.url, "La pagina no se redirecciono a categorias"

@pytest.mark.asyncio(loop_scope="module")
async def test_compare_product_cart(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.addCart(data.input_success)
    assert product.get_compare_cart == "Light gray", "El color del producto en el carro no corresponde"

@pytest.mark.asyncio(loop_scope="module")
async def test_find_size(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.findOption()
    assert not product.get_find_size, "El boton de find size no esta funcionando"

@pytest.mark.asyncio(loop_scope="module")
async def test_find_size(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    await product.wishlistOption()
    assert product.get_wishlist_info, "No se encontraron productos en la wishlist"

@pytest.mark.asyncio(loop_scope="module")
async def test_price_discount(browser, session):
    context = await browser.new_context()
    await context.add_cookies(session)
    page = await context.new_page()
    home = AutomationPortal(page)
    await home.navigate()
    await home.close_newsletter_popup()
    product = Product(page)
    await product.selectProduct()
    assert product.get_discount_price == product.discountPrice, "El descuento no se esta realizando correctamente"