import pytest

@pytest.mark.asyncio
async def test_success_product(product):
    await product.addCart()
    #assert await product.wait_for("#shoppingCart > div > div > div.header",state="visible")