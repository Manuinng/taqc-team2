from playwright.async_api import Page
import asyncio

class HomePage:
    def __init__(self, page:Page):
        self.page = page
        self.pop = page.locator('a[data-bs-dismiss="modal"].btn-hide-popup')
        self.btnToRegister = page.locator("a[href='#register']")
        self.btnRegister = page.locator("a[href='/register']")
        self.btnOut = page.locator("#register > div > div > div.header > span")
        self.account = page.locator(".nav-account")

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