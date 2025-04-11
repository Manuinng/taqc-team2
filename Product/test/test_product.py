import pytest
import asyncio
from config.data import data

@pytest.mark.asyncio
async def test_success_product(product):
    await product.selectProduct()
    await product.addCart(data.input_success)
    #assert await product.get_field_validation_state("")
    cart_product = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert cart_product, "El producto no se encontró en el carrito."

@pytest.mark.asyncio
async def test_fail_infinity_product(product):
    await product.selectProduct()
    await product.addCart(data.input_infinity)
    cart_product_visible = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert not cart_product_visible, "El producto no debería estar en el carrito al usar una cantidad infinita."

@pytest.mark.asyncio
async def test_fail_NaN_product(product):
    await product.selectProduct()
    await product.addCart(data.input_Nan)
    cart_product_visible = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert not cart_product_visible, "El producto no debería estar en el carrito al usar una cantidad NaN."

@pytest.mark.asyncio
async def test_fail_zero_product(product):
    await product.selectProduct()
    await product.addCart(data.input_zero)
    cart_product_visible = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert not cart_product_visible, "El producto no debería estar en el carrito al usar una cantidad Zero."

@pytest.mark.asyncio
async def test_fail_max_product(product):
    await product.selectProduct()
    await product.addCart(data.input_max)
    cart_product_visible = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert not cart_product_visible, "El producto se agrega aun con cantidades que deberian tocar el maimo de producto disponible."

@pytest.mark.asyncio
async def test_fail_neg_product(product):
    await product.selectProduct()
    await product.addCart(data.input_neg)
    cart_product_visible = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert not cart_product_visible, "El producto no debería estar en el carrito al usar una cantidad negativa."

@pytest.mark.asyncio
async def test_eliminate_compare(product):
    await product.selectProduct()
    await product.viewCompare()
    products_in_compare_count_before_removal = await product.page.locator("#remove-compare-color-beige-1").is_visible()
    assert not products_in_compare_count_before_removal , "La sección de comparación está vacía, no hay productos para comparar."

@pytest.mark.asyncio
async def test_int_value(product):
    await product.selectProduct()
    await product.addCart(data.input_int)
    cart_product_visible = await product.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
    assert not cart_product_visible, "El producto no debería estar en el carrito al usar una cantidad numeral."