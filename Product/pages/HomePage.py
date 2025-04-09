from playwright.async_api import Page
from config.data import url
import asyncio

class HomePage:
    def __init__(self, page:Page):
        self.page = page
        self.pop = page.locator('a[data-bs-dismiss="modal"].btn-hide-popup')
        self.btnLog = page.locator("#login > div > div > div.tf-login-form > form > div.bottom > div:nth-child(1) > button")
        self.btnToRegister = page.locator("a[href='#register']")
        self.btnRegister = page.locator("a[href='/register']")
        self.btnOut = page.locator("#register > div > div > div.header > span")
        self.account = page.locator(".nav-account")
        #self.productView = page.locator("#wrapper > div > section:nth-child(6) > div.tf-grid-layout.tf-col-2.md-col-3.gap-0.home-pckaleball-page > div:nth-child(5) > div.card-product-info > a")

    async def navigate(self, url):
        await self.page.goto(url, wait_until="domcontentloaded")

    async def popup(self):
        await self.page.wait_for_selector("#newsletterPopup", state="visible", timeout=5000)
        await self.page.wait_for_timeout(1000)
        await self.pop.click()
        await self.page.wait_for_selector("#newsletterPopup", state="hidden")

    async def registerHome(self):
        await self.account.click()
        await self.page.wait_for_selector("#login")
        await self.btnToRegister.click()
        await self.btnRegister.click()
        await self.page.wait_for_selector("#register", state="visible")
        await self.page.wait_for_timeout(1000)
        await self.btnOut.click()

    async def logHome(self):
        await self.account.click()
        await self.page.wait_for_selector("#login")
        await self.btnLog.click()

    async def productHome(self):
        await self.productView.click()
        await self.page.wait_for_timeout(5000)