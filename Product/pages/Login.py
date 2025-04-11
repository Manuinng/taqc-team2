from playwright.async_api import Page
from config.data import url, data
import asyncio

class Login:
    def __init__(self, page:Page):
        self.page = page
        self.Email = page.locator("#login > div > div > div.tf-login-form > form > div:nth-child(1) > input")
        self.Password = page.locator("#login > div > div > div.tf-login-form > form > div:nth-child(2) > input")
        self.buttonL = page.locator("#login > div > div > div.tf-login-form > form > div.bottom > div:nth-child(1) > button")

    async def LogIN(self):
        await self.Email.fill(data.email)
        await self.Password.fill(data.password)
        await self.buttonL.click()
        await self.page.keyboard.press("Escape")
        await self.page.locator("#header > div > div > div.col-xl-3.col-md-4.col-6 > a").click()
        await asyncio.sleep(5)