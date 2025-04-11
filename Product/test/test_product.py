import pytest
import asyncio
from config.data import data

@pytest.mark.asyncio
async def test_success_product(product):
    await product.selectProduct()
    await product.addCart(data.input_success)
    #assert await product.get_field_validation_state("")
    assert product.get_information_cart, "El producto no se encontró en el carrito."

@pytest.mark.asyncio
async def test_fail_infinity_product(product):
    await product.selectProduct()
    await product.addCart(data.input_infinity)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad infinita."

@pytest.mark.asyncio
async def test_fail_NaN_product(product):
    await product.selectProduct()
    await product.addCart(data.input_Nan)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad NaN."

@pytest.mark.asyncio
async def test_fail_zero_product(product):
    await product.selectProduct()
    await product.addCart(data.input_zero)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad Zero."

@pytest.mark.asyncio
async def test_fail_max_product(product):
    await product.selectProduct()
    await product.addCart(data.input_max)
    assert not product.get_information_cart, "El producto se agrega aun con cantidades que deberian tocar el maximo de producto disponible."

@pytest.mark.asyncio
async def test_fail_neg_product(product):
    await product.selectProduct()
    await product.addCart(data.input_neg)
    await product.get_information_cart()
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad negativa."

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
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad numeral."

@pytest.mark.asyncio
async def test_empty_product(product):
    await product.selectProduct()
    await product.addCart(data.input_empty)
    assert not product.get_information_cart, "El producto no debería estar en el carrito al usar una cantidad numeral."