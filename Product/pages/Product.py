from playwright.async_api import Page
from config.data import url
import asyncio

class Product:
    def __init__(self ,page:Page):
        self.page = page
        self.productView = page.locator("#wrapper > div > section:nth-child(6) > div.tf-grid-layout.tf-col-2.md-col-3.gap-0.home-pckaleball-page > div:nth-child(5) > div.card-product-wrapper > a")
        self.btnColor = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-variant-picker > div:nth-child(1) > form > label:nth-child(4) > span.btn-checkbox.bg-color-black")
        self.btnSize = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-variant-picker > div:nth-child(2) > form > label:nth-child(6)")
        self.moreQuantity = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-quantity > div.wg-quantity > span.btn-quantity.plus-btn")
        self.lessQuantity = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-quantity > div.wg-quantity > span.btn-quantity.minus-btn")
        self.btnAdd = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > a.tf-btn.btn-fill.justify-content-center.fw-6.fs-16.flex-grow-1.animate-hover-btn")
        self.inputQuantity = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-quantity > div.wg-quantity > input[type=text]")
        self.btnCompare = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-extra-link > a:nth-child(1)")

    async def selectColor(self):
        await self.btnColor.click()

    async def selectSize(self):
        await self.btnSize.click()

    async def selectMore(self):
        await self.moreQuantity.click()

    async def selectLess(self):
        await self.lessQuantity.click()

    async def inputSection(self, input_singular:str):
        await self.inputQuantity.fill(input_singular)

    async def addSelection(self):
        await self.btnAdd.click()

    async def compareSection(self):
        await self.btnCompare.click()

    async def selectProduct(self):
        await self.productView.click()
        await self.page.wait_for_timeout(2000)

    async def addCart(self, input_test:str):
        await self.btnColor.wait_for(state='visible')
        await self.btnColor.click()
        await self.page.wait_for_timeout(2000)
        await self.btnSize.click()
        await self.page.wait_for_timeout(2000)
        await self.inputQuantity.fill(input_test)
        await self.page.wait_for_timeout(2000)
        await self.btnAdd.click()
        await self.page.wait_for_timeout(2000)

    async def viewCompare(self):
        await self.btnCompare.click()
        await self.page.wait_for_selector("#compare_color > div > div", state="visible", timeout=5000)
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(2) > div.tf-compare-color-top > label").click()
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(4) > div.tf-compare-color-top > label").click()
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(6) > div.tf-compare-color-top > label").click()
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(8) > div.tf-compare-color-top > label").click()
        await self.page.wait_for_timeout(2000)
        await self.page.locator("#compare_color > div > div > div.header > span").click()
        await self.btnCompare.click()
        await self.page.wait_for_timeout(2000)

    #async def get_validation_values(self):

