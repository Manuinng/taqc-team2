import pytest
import asyncio
from config.data import data

@pytest.mark.asyncio
async def test_success_product(product):
    await product.selectProduct()
    await product.addCart(data.input_success)
    #assert await product.get_field_validation_state("")

@pytest.mark.asyncio
async def test_fail_infinity_product(product):
    await product.selectProduct()
    await product.addCart(data.input_infinity)

@pytest.mark.asyncio
async def test_fail_NaN_product(product):
    await product.selectProduct()
    await product.addCart(data.input_Nan)

@pytest.mark.asyncio
async def test_eliminate_compare(product):
    await product.selectProduct()
    await product.viewCompare()