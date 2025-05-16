import pytest
from config.config import BASE_URL
from tests.utils.api_helper import APIHelper
from playwright.async_api import TimeoutError
from pages.automation_portal import AutomationPortal as AutoPortal

@pytest.mark.asyncio(loop_scope="module")
async def test_quick_view_full_options(browser):
    """Test adding a product with full options using Quick View and verifying the cart is not empty."""
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await home.scroll_down()
    await home.scroll_down()
    await home.quick_view_product()
    await home.view_select_product_options_and_click_find_your_size({"color": "Blue", "size": "L", "quantity": 2})
    await home.interact_with_cart(["adjust_quantity"])
    cart_items = page.locator("#shoppingCart .tf-mini-cart-item")
    item_count = await cart_items.count()
    assert item_count > 0, "Cart is empty after adding a product with full options."
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_quick_add_no_options(browser):
    """Test adding a product without options using Quick Add and verifying the cart is not empty."""
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await home.scroll_down()
    await home.scroll_down()
    await home.quick_add_product()
    cart_items = page.locator("#shoppingCart .tf-mini-cart-item")
    item_count = await cart_items.count()
    assert item_count > 0, "Cart is empty after adding a product without options."
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_quick_view_partial_options(browser):
    """Test adding a product with partial options using Quick View and verifying the cart is not empty."""
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await home.scroll_down()
    await home.scroll_down()
    await home.quick_view_product()
    await home.view_select_product_options_and_click_find_your_size({"color": "White"})
    await home.interact_with_cart(["estimate_shipping"])
    cart_items = page.locator("#shoppingCart .tf-mini-cart-item")
    item_count = await cart_items.count()
    assert item_count > 0, "Cart is empty after adding a product with partial options."
    await context.close()

@pytest.mark.asyncio(loop_scope="module")
async def test_quick_view_negative_quantity(browser):
    """Test adding a product with negative quantity using Quick View and verifying the cart is not empty due to lack of validation."""
    context = await browser.new_context()
    page = await context.new_page()
    home = AutoPortal(page)

    await home.navigate()
    await home.close_newsletter_popup()
    await home.scroll_down()
    await home.scroll_down()
    await home.quick_view_product()
    await home.view_select_product_options_and_click_find_your_size({"color": "Red", "size": "M", "quantity": -1})
    await home.interact_with_cart(["adjust_quantity"])
    cart_items = page.locator("#shoppingCart .tf-mini-cart-item")
    item_count = await cart_items.count()
    assert item_count > 0, "Cart is empty after adding a product with negative quantity."
    await context.close()