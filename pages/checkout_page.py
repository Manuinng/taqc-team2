from playwright.async_api import Page, expect
from config.config import BASE_URL

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = f"{BASE_URL}/checkout"
        self.first_name = "#first-name"
        self.last_name = "#last-name"
        self.country = "#country"
        self.city = "#city"
        self.address = "#address"
        self.phone = "#phone"
        self.email = "#email"
        self.notes = "#note"
        self.discount_code = "input[placeholder='Discount code']"
        self.apply_discount_button = "a.tf-btn.btn-sm.radius-3.btn-fill.btn-icon.animate-hover-btn:has-text('Apply')"
        self.card_number = "input[placeholder='Card Number (try 4242424242424242)']"
        self.card_date = "input[placeholder='MM/YY']"
        self.card_cvc = "input[placeholder='CVC']"
        self.tos_checkbox = "#check-agree"
        self.place_order_button = "button.tf-btn.btn-fill.btn-icon.animate-hover-btn:has-text('Place order')"

    async def __fill_input(self, selector, value):
        await self.page.locator(selector).scroll_into_view_if_needed()
        await self.page.fill(selector, value)
        await expect(self.page.locator(selector)).to_have_value(value)

    async def navigate(self):
        await self.page.goto(self.url)
        await expect(self.page).to_have_url(self.url)

    async def fill_billing_details(
            self,
            first_name=None,
            last_name=None,
            country=None,
            city=None,
            address=None,
            phone=None,
            email=None,
            notes=None,
    ):
        fields = [
            (self.first_name, first_name),
            (self.last_name, last_name),
            (self.city, city),
            (self.address, address),
            (self.phone, phone),
            (self.email, email),
            (self.notes, notes),
    ]

        for selector, value in fields:
            if value:
                await self.__fill_input(selector, value)

        if country:
            await self.page.locator(self.country).scroll_into_view_if_needed()
            await self.page.select_option(self.country, country)
            await expect(self.page.locator(self.country)).to_have_value(country)

    async def apply_discount_code(self, code=None):
        if code:
            await self.__fill_input(self.discount_code, code)
            await self.page.click(self.apply_discount_button)

    async def fill_credit_card_details(
            self,
            card_number=None,
            card_date=None,
            card_cvc=None,
    ):
        if card_number:
            await self.__fill_input(self.card_number, card_number)

        if card_date or card_cvc:
            await self.page.locator(self.card_date).scroll_into_view_if_needed()
            if card_date:
                await self.page.fill(self.card_date, card_date)
            if card_cvc:
                await self.page.fill(self.card_cvc, card_cvc)

    async def click_tos_checkbox(self):
        await self.page.locator(self.tos_checkbox).scroll_into_view_if_needed()
        await self.page.click(self.tos_checkbox)
        await expect(self.page.locator(self.tos_checkbox)).to_be_checked()

    async def place_order(self):
        await self.page.locator(self.place_order_button).scroll_into_view_if_needed()
        await self.page.click(self.place_order_button)
