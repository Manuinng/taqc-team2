from playwright.async_api import Page
import asyncio
from faker import Faker


fake = Faker()
class Registration:
    def __init__(self, page:Page):
        self.page = page
        self.Fname = page.locator("#register-form > div:nth-child(1) > input")
        self.Lname = page.locator("#register-form > div:nth-child(2) > input")
        self.Email = page.locator("#register-form > div:nth-child(3) > input")
        self.Password = page.locator("#register-form > div.tf-field.style-1.mb_30 > input")
        self.buttonR = page.locator("#register-form > div.mb_20 > button")

    async def register(self):

        #first_name = fake.first_name()
        #last_name = fake.last_name()
        #email = fake.email()
        #password = fake.password(length=12)

        await self.Fname.fill("first_name")
        await self.Lname.fill("last_name")
        await self.Email.fill("email@4")
        await self.Password.fill("pass")
        await asyncio.sleep(5)
        await self.buttonR.click()
        await asyncio.sleep(5)
        #await self.page.click("enter")

