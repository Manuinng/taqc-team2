from playwright.async_api import Page
from config.config import BASE_URL

class AutomationPortal:
    def __init__(self, page: Page):
        self.page = page

        # Selectors
        self.newsletter_popup = "#newsletterPopup"
        self.close_newsletter = "a:has-text('Not interested')"
        self.wishlist_button = ".nav-wishlist .nav-icon-item"
        self.home_logo = "a.logo-header[href='/']"
        self.product_image = ".card-product-wrapper .product-img"
        self.quick_add_button = ".card-product-wrapper .quick-add"
        self.quick_view_button = ".card-product-wrapper .quickview"
        self.add_to_cart_quick_add = "#quick_add .tf-product-info-buy-button .tf-btn"
        self.quantity_input_quick_add = "#quick_add input[name='number']"
        self.quantity_input_quick_view = "#quick_view .tf-product-info-quantity input[name='number']"
        self.find_your_size_button = ".find-size.btn-choose-size"
        self.add_to_wishlist_quick_view = "#quick_view .tf-product-btn-wishlist.hover-tooltip"
        self.add_to_cart_quick_view = "#quick_view .tf-product-info-buy-button .tf-btn"
        self.plus_button_cart = "#shoppingCart .btn-quantity.plus-btn"
        self.minus_button_cart = "#shoppingCart .btn-quantity.minus-btn"
        self.add_note_button = "#shoppingCart .tf-mini-cart-tool-btn.btn-add-note"
        self.note_input = "#Cart-note"
        self.close_note_button = ".tf-mini-cart-tool-primary.tf-mini-cart-tool-close:has-text('Close')"
        self.estimate_shipping_button = "#shoppingCart .tf-mini-cart-tool-btn.btn-estimate-shipping"
        self.cancel_estimate_button = ".tf-mini-cart-tool-primary.tf-mini-cart-tool-close:has-text('Cancel') >> nth=1"

    def get_color_selector(self, color, context="quick_add"):
        if context == "quick_add":
            return f"#quick_add label.hover-tooltip[data-value='{color}']"
        elif context == "quick_view":
            return f"label.hover-tooltip[data-value='{color}']"

    def get_size_selector(self, size, context="quick_add"):
        if context == "quick_add":
            return f"#quick_add label.style-text[data-value='{size}']"
        elif context == "quick_view":
            return f"label.style-text[data-value='{size}']"

    async def navigate(self):
        await self.page.goto(BASE_URL)

    async def close_newsletter_popup(self):
        await self.page.wait_for_selector(self.newsletter_popup, state="visible")
        await self.page.wait_for_timeout(1000)
        await self.page.click(self.close_newsletter)
        await self.page.wait_for_selector(self.newsletter_popup, state="hidden")

    async def navigate_to_wishlist(self):
        print("Navigating to wishlist...")
        await self.page.wait_for_selector(self.wishlist_button, timeout=5000)
        await self.page.wait_for_timeout(1000)
        await self.page.click(self.wishlist_button)

    async def navigate_to_home(self):
        print("Navigating to home...")
        await self.page.wait_for_timeout(5000)
        await self.page.click(self.home_logo)
        await self.page.wait_for_timeout(5000)

    async def scroll_down(self):
        print("Scrolling down...")
        await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
        await self.page.wait_for_timeout(2000)

    async def quick_add_product(self):
        print("Hovering over the product and pressing 'Quick Add'...")
        await self.page.hover(self.product_image)
        await self.page.wait_for_timeout(1000)
        await self.page.click(self.quick_add_button)
        await self.page.wait_for_timeout(2000)

    async def quick_view_product(self):
        print("Hovering over the product and pressing 'Quick View'...")
        await self.page.hover(self.product_image)
        await self.page.wait_for_timeout(1000)
        await self.page.click(self.quick_view_button)
        await self.page.wait_for_timeout(2000)

    async def add_select_product_options_and_quick_add_to_cart(self, options=None):
        print("Selecting product options and adding to cart via Quick Add...")
        if options:
            if "color" in options:
                color_selector = self.get_color_selector(options['color'], context="quick_add")
                await self.page.wait_for_selector(color_selector, state="visible")
                await self.page.click(color_selector)
                await self.page.wait_for_timeout(1000)
            if "size" in options:
                size_selector = self.get_size_selector(options['size'], context="quick_add")
                await self.page.click(size_selector)
                await self.page.wait_for_timeout(2000)
            if "quantity" in options:
                await self.page.fill(self.quantity_input_quick_add, str(options['quantity']))
                await self.page.wait_for_timeout(2000)
        await self.page.click(self.add_to_cart_quick_add)
        await self.page.wait_for_timeout(5000)

    async def view_select_product_options_and_click_find_your_size(self, options=None):
        print("Selecting product options and pressing 'Find Your Size'...")
        if options:
            if "color" in options:
                color_selector = self.get_color_selector(options['color'], context="quick_view")
                await self.page.wait_for_selector(color_selector, state="visible")
                await self.page.click(color_selector)
                await self.page.wait_for_timeout(1000)
            if "size" in options:
                size_selector = self.get_size_selector(options['size'], context="quick_view")
                await self.page.click(size_selector)
                await self.page.wait_for_timeout(2000)
            if "quantity" in options:
                await self.page.fill(self.quantity_input_quick_view, str(options['quantity']))
                await self.page.wait_for_timeout(1000)
        await self.page.click(self.find_your_size_button)
        await self.page.wait_for_timeout(1000)
        await self.page.click("body", position={"x": 0, "y": 0})
        await self.page.wait_for_timeout(1000)
        await self.page.click(self.add_to_wishlist_quick_view)
        await self.page.wait_for_timeout(2000)
        await self.page.click(self.add_to_cart_quick_view)
        await self.page.wait_for_timeout(3000)

    async def interact_with_cart(self, actions=None):
        print("Interacting with the cart...")
        if not actions:
            return
        for action in actions:
            if action == "adjust_quantity":
                plus_buttons = self.page.locator(self.plus_button_cart)
                minus_buttons = self.page.locator(self.minus_button_cart)
                if await plus_buttons.count() > 0:
                    print("Increasing quantity...")
                    await plus_buttons.nth(0).click()
                    await self.page.wait_for_timeout(1000)
                if await minus_buttons.count() > 0:
                    print("Decreasing quantity...")
                    await minus_buttons.nth(0).click()
                    await self.page.wait_for_timeout(1000)
            elif action == "add_note":
                print("Adding a note...")
                await self.page.locator(self.add_note_button).click()
                await self.page.wait_for_timeout(2000)
                await self.page.fill(self.note_input, "Esto es una prueba.")
                await self.page.locator(self.close_note_button).click()
                await self.page.wait_for_timeout(2000)
            elif action == "estimate_shipping":
                print("Estimating shipping...")
                await self.page.locator(self.estimate_shipping_button).click()
                await self.page.wait_for_timeout(2000)
                await self.page.locator(self.cancel_estimate_button).click()
                await self.page.wait_for_timeout(2000)