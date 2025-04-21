from playwright.async_api import Page
from config.config import BASE_URL

class AutomationPortal:
    def __init__(self, page: Page):
        self.page = page

    async def navigate(self):
        await self.page.goto(BASE_URL)

    async def close_newsletter_popup(self):
        await self.page.wait_for_selector("#newsletterPopup", state="visible")
        close_newsletter = "a:has-text('Not interested')"
        await self.page.wait_for_timeout(1000)
        await self.page.click(close_newsletter)
        await self.page.wait_for_selector("#newsletterPopup", state="hidden")

    async def navigate_to_wishlist(self):
        print("Navegando a la wishlist...")
        wishlist_button_selector = ".nav-wishlist .nav-icon-item"
        await self.page.wait_for_selector(wishlist_button_selector, timeout=5000)
        await self.page.wait_for_timeout(1000)
        await self.page.click(wishlist_button_selector)

    async def navigate_to_home(self):
        print("Navegando a la home...")
        await self.page.wait_for_timeout(5000)
        await self.page.click("a.logo-header[href='/']")
        await self.page.wait_for_timeout(5000)

    async def scroll_down(self):
        print("Scrolling down...")
        await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
        await self.page.wait_for_timeout(2000)

    async def quick_add_product(self):
        print("Haciendo hover en el producto y presionando 'Quick Add'...")
        product_selector = ".card-product-wrapper .product-img"
        quick_add_button_selector = ".card-product-wrapper .quick-add"

        await self.page.hover(product_selector)
        await self.page.wait_for_timeout(1000)
        await self.page.click(quick_add_button_selector)
        await self.page.wait_for_timeout(2000)

    async def quick_view_product(self):
        print("Haciendo hover en el producto y presionando 'Quick View'...")
        product_selector = ".card-product-wrapper .product-img"
        quick_view_button_selector = ".card-product-wrapper .quickview"

        await self.page.hover(product_selector)
        await self.page.wait_for_timeout(1000)
        await self.page.click(quick_view_button_selector)
        await self.page.wait_for_timeout(5000)

    async def select_product_options_and_add_to_cart(self):
        print("Selecting product options and adding to cart...")

        color_selector = "#quick_add label.hover-tooltip[data-value='White']"
        await self.page.wait_for_selector(color_selector, state="visible")
        await self.page.click(color_selector)
        await self.page.wait_for_timeout(1000)

        size_selector = "#quick_add label.style-text[data-value='M']"
        await self.page.click(size_selector)
        await self.page.wait_for_timeout(2000)

        quantity_input_selector = "#quick_add input[name='number']"
        await self.page.fill(quantity_input_selector, "3")
        await self.page.wait_for_timeout(2000)

        add_to_cart_button_selector = "#quick_add .tf-product-info-buy-button .tf-btn"
        await self.page.click(add_to_cart_button_selector)
        await self.page.wait_for_timeout(5000)
