from playwright.async_api import Page, expect, TimeoutError
from config.config import BASE_URL
from tests.utils.api_helper import APIHelper
from tests.utils.common_utils import camel_to_snake
from typing import Optional, Dict, List, Any
from uuid import UUID

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = f"{BASE_URL}/checkout"
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.country = page.locator("#country")
        self.city = page.locator("#city")
        self.address = page.locator("#address")
        self.phone = page.locator("#phone")
        self.email = page.locator("#email")
        self.notes = page.locator("#note")
        self.discount_code = page.locator("input[placeholder='Discount code']")
        self.apply_discount_button = page.locator("a.tf-btn.btn-sm.radius-3.btn-fill.btn-icon.animate-hover-btn:has-text('Apply')")
        self.card_number = page.locator("input[placeholder='Card Number (try 4242424242424242)']")
        self.expiry = page.locator("input[placeholder='MM/YY']")
        self.cvc = page.locator("input[placeholder='CVC']")
        self.tos_checkbox = page.locator("#check-agree")
        self.place_order_button = page.locator("button.tf-btn.btn-fill.btn-icon.animate-hover-btn:has-text('Place order')")
        self.cart_items = page.locator("#wrapper > section > div > div > div.tf-page-cart-footer > div > form > ul > li")
        self.cart_item_quantities = page.locator("#wrapper > section > div > div > div.tf-page-cart-footer > div > form > ul > li > figure > span.quantity")
        self.cart_item_titles = page.locator("#wrapper > section > div > div > div.tf-page-cart-footer > div > form > ul > li > div > div > p.name")
        self.cart_item_variants = page.locator("#wrapper > section > div > div > div.tf-page-cart-footer > div > form > ul > li > div > div > span.variant")
        self.order_message = page.locator("#order-message > p")

    async def __fill_input(self, locator: str, value: str):
        await locator.scroll_into_view_if_needed()
        await locator.fill(value)
        await expect(locator).to_have_value(value)

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

        for locator, value in fields:
            if value:
                await self.__fill_input(locator, value)

        if country:
            await self.country.scroll_into_view_if_needed()
            await self.country.select_option(country)
            await expect(self.country).to_have_value(country)

    async def fill_credit_card_info(
            self,
            card_number: Optional[str] = None,
            expiry: Optional[str] = None,
            cvc: Optional[str] = None,
    ):
        fields = [
            (self.card_number, card_number),
            (self.expiry, expiry),
            (self.cvc, cvc),
    ]

        for locator, value in fields:
            if value:
                await self.__fill_input(locator, value)

    async def apply_discount_code(self, code=None):
        if code:
            await self.__fill_input(self.discount_code, code)
            await self.apply_discount_button.click()

    async def click_tos_checkbox(self):
        await self.tos_checkbox.scroll_into_view_if_needed()
        await self.tos_checkbox.click()
        await expect(self.tos_checkbox).to_be_checked()

    async def fill_form(self, billing_details: Dict[str, str], credit_card_info: Dict[str, str], discount_code: str, check_tos: bool):
        await self.fill_billing_details(**billing_details)
        await self.fill_credit_card_info(**credit_card_info)
        if discount_code:
            await self.apply_discount_code(discount_code)
        if check_tos:
            await self.click_tos_checkbox()

    async def place_order(self, timeout=2000) -> UUID | bool:
        await self.place_order_button.scroll_into_view_if_needed()

        try:
            async with self.page.expect_response(f"{BASE_URL}/api/checkout", timeout=timeout) as response_info:
                await self.place_order_button.click()

            response = await response_info.value
            if response.ok:
                response_data = await response.json()
                return response_data.get("orderId", False)
        except TimeoutError:
            pass

        return False
