from playwright.async_api import Page, expect, TimeoutError
from config.config import BASE_URL
from typing import Optional, Dict, Any
from uuid import UUID

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
        self.expiry = "input[placeholder='MM/YY']"
        self.cvc = "input[placeholder='CVC']"
        self.tos_checkbox = "#check-agree"
        self.place_order_button = "button.tf-btn.btn-fill.btn-icon.animate-hover-btn:has-text('Place order')"

    async def __fill_input(self, selector: str, value: str):
        await self.page.locator(selector).scroll_into_view_if_needed()
        await self.page.fill(selector, value)
        await expect(self.page.locator(selector)).to_have_value(value)

    async def navigate(self):
        await self.page.goto(self.url)
        await expect(self.page).to_have_url(self.url)

    async def fill_billing_details(
            self,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            country: Optional[str] = None,
            city: Optional[str] = None,
            address: Optional[str] = None,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            notes: Optional[str] = None,
            card_number: Optional[str] = None,
            expiry: Optional[str] = None,
            cvc: Optional[str] = None,
    ):
        fields = [
            (self.first_name, first_name),
            (self.last_name, last_name),
            (self.city, city),
            (self.address, address),
            (self.phone, phone),
            (self.email, email),
            (self.notes, notes),
            (self.card_number, card_number),
            (self.expiry, expiry),
            (self.cvc, cvc),
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

    async def click_tos_checkbox(self):
        await self.page.locator(self.tos_checkbox).scroll_into_view_if_needed()
        await self.page.click(self.tos_checkbox)
        await expect(self.page.locator(self.tos_checkbox)).to_be_checked()

    async def fill_form(self, checkout_data: Dict[str, Any]):
        discount_code = checkout_data.pop("discount_code", None)
        check_tos = checkout_data.pop("tos_checkbox", False)
        await self.fill_billing_details(**checkout_data)
        if discount_code:
            await self.apply_discount_code(discount_code)
        if check_tos:
            await self.click_tos_checkbox()

    async def place_order(self, timeout=2000) -> UUID | bool:
        await self.page.locator(self.place_order_button).scroll_into_view_if_needed()

        try:
            async with self.page.expect_response(f"{BASE_URL}/api/checkout", timeout=timeout) as response_info:
                await self.page.click(self.place_order_button)

            response = await response_info.value
            if response.ok:
                response_data = await response.json()
                return response_data.get("orderId", False)
        except TimeoutError:
            pass

        return False
