from playwright.async_api import Page
from config.data import url
import asyncio

class Login:
    def __init__(self, page:Page):
        self.page = page
        self.Email = page.locator("#loginEmail")
        self.Password = page.locator("#loginPassword")
        self.buttonL = page.locator("#login > div > form > div:nth-child(4) > button")

    async def LogIN(self):
        await self.Email.fill("email@1")
        await self.Password.fill("pass")
        await self.buttonL.click()
        await asyncio.sleep(5)