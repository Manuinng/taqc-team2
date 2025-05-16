from playwright.async_api import Page, expect
import re
import asyncio

class ProductPage:
    def __init__(self ,page:Page):
        self.page = page
        self.itemProductSelection = page.locator("#wrapper > div > section:nth-child(6) > div.tf-grid-layout.tf-col-2.md-col-3.gap-0.home-pckaleball-page")
        self.btnColor = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-variant-picker > div:nth-child(1) > form > label:nth-child(4) > span.btn-checkbox.bg-color-black")
        self.btnSize = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-variant-picker > div:nth-child(2) > form > label:nth-child(6)")
        self.moreQuantity = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-quantity > div.wg-quantity > span.btn-quantity.plus-btn")
        self.lessQuantity = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-quantity > div.wg-quantity > span.btn-quantity.minus-btn")
        self.btnAdd = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > a.tf-btn.btn-fill.justify-content-center.fw-6.fs-16.flex-grow-1.animate-hover-btn")
        self.inputQuantity = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-quantity > div.wg-quantity > input[type=text]")
        self.btnCompare = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-extra-link > a:nth-child(1)")
        self.btnBuy = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > div > a.btns-full")
        self.btnCategory = page.locator("#wrapper > div > div > div > div.tf-breadcrumb-prev-next > a.tf-breadcrumb-back.hover-tooltip.center")
        self.btnFind = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-variant-picker > div:nth-child(2) > div > a")
        self.btnMore = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > div > a.payment-more-option")
        self.btnComparepro = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > a.tf-product-btn-wishlist.hover-tooltip.box-icon.bg_white.compare.btn-icon-action")
        self.btnWish = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > a.tf-product-btn-wishlist.hover-tooltip.box-icon.bg_white.wishlist.btn-icon-action")
        self.btnNavwish = page.locator("li.nav-wishlist a.nav-icon-item")
        self.discount_price = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-price > div.price-on-sale")
        self.real_price = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-price > div.compare-at-price")
        self.discount = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-price > div.badges-on-sale")
        self.cartInformation = page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div")
        self.gridColoritem = page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div")

    async def selectColor(self): #Button for color selection
        await expect(self.btnColor,"The button for selection of color is not visible").to_be_visible()
        await self.btnColor.click()

    async def selectSize(self): #Button for size selection
        await expect(self.btnSize,"The button for selection of size is not visible").to_be_visible()
        await self.btnSize.click()

    async def selectMore(self): #Button for more selection of products.
        await expect(self.moreQuantity,"The button for more quantity is not visible").to_be_visible()
        await self.moreQuantity.click()

    async def selectLess(self): #Button for less selection of products.
        await expect(self.lessQuantity,"The button for less quantity is not visible").to_be_visible()
        await self.lessQuantity.click()

    async def inputSection(self, input_singular:str): #Input quantity of products
        await expect(self.inputQuantity,"The input for quantity is not visible").to_be_visible()
        await self.inputQuantity.fill(input_singular)

    async def addSelection(self): #Button for add to cart
        await expect(self.btnAdd,"The button for add product is not visible").to_be_visible()
        await self.btnAdd.click()

    async def compareSection(self): #Button for compare options
        await expect(self.btnCompare,"The button for compare color is not visible").to_be_visible()
        await self.btnCompare.click()

    async def selectProduct(self): #Selection of product
        await self.itemProductSelection.locator("div:nth-child(5) > div.card-product-wrapper > a").click()

    async def addingProduct(self, input_test:str): #Flow for selection of product options and add to cart 
        await self.btnColor.wait_for(state='visible')
        await expect(self.btnColor,"The button for selection of color is not visible").to_be_visible()
        await self.btnColor.click()
        await expect(self.btnSize,"The button for selection of size is not visible").to_be_visible()
        await self.btnSize.click()
        await expect(self.inputQuantity,"The input for quantity is not visible").to_be_visible()
        await self.inputQuantity.fill(input_test)
        await expect(self.btnAdd,"The button for add product is not visible").to_be_visible()
        await self.btnAdd.click()
        await expect(self.cartInformation,"The product is not present in the cart").to_be_visible()

    async def viewCompare(self): #Use of compare color without any color to compare
        await expect(self.btnCompare,"The button for compare color is not visible").to_be_visible()
        await self.btnCompare.click()
        await self.page.wait_for_selector("#compare_color > div > div", state="visible", timeout=5000)
        await expect(self.gridColoritem.locator("div:nth-child(2) > div.tf-compare-color-top > label"), "The remove option for the first color is no available").to_be_visible()
        await self.gridColoritem.locator("div:nth-child(2) > div.tf-compare-color-top > label").click()
        await expect(self.gridColoritem.locator("div:nth-child(4) > div.tf-compare-color-top > label"),"The remove option for the second color is no available").to_be_visible()
        await self.gridColoritem.locator("div:nth-child(4) > div.tf-compare-color-top > label").click()
        await expect(self.gridColoritem.locator("div:nth-child(6) > div.tf-compare-color-top > label"),"The remove option for the third color is no available").to_be_visible()
        await self.gridColoritem.locator("div:nth-child(6) > div.tf-compare-color-top > label").click()
        await expect(self.gridColoritem.locator("div:nth-child(8) > div.tf-compare-color-top > label"),"The remove option for the fourth color is no available").to_be_visible()
        await self.gridColoritem.locator("div:nth-child(8) > div.tf-compare-color-top > label").click()
        await expect(self.page.locator("#compare_color > div > div > div.header > span"),"The close option for the compare color is not visible").to_be_visible()
        await self.page.locator("#compare_color > div > div > div.header > span").click()
        await expect(self.btnCompare,"The button for compare color is not visible").to_be_visible()
        await self.btnCompare.click()
        await expect(self.page.locator("#compare_color > div > div"),"The compare color section is not visible").to_be_visible()

    async def buyOption(self): #Use of buy with option
        await expect(self.btnBuy,"The button for buy with option is not visible").to_be_visible()
        await self.btnBuy.click()

    async def categoryOption(self): #Use of category button
        await expect(self.btnCategory,"The button for category is not visible").to_be_visible()
        await self.btnCategory.click()

    async def findOption(self): #Button for the find size option
        await expect(self.btnFind,"The button for find size is not visible").to_be_visible()
        await self.btnFind.click()
        await expect(self.page.locator("#find_size > div > div > div.tf-rte > div.tf-table-res-df"),"The find size option is not visible").to_be_visible()

    async def morepayOptions(self): #Button for more pay option
        await expect(self.btnMore,"The button for more option to pay is not visible").to_be_visible()
        await self.btnMore.click()

    async def compareProduct(self): #Button for compare product option
        await expect(self.btnComparepro,"The button for compare product is not visible").to_be_visible()
        await self.btnComparepro.click()

    async def wishlistOption(self): #Use of whislist button for the product
        await self.btnWish.wait_for(state='visible')
        await expect(self.btnWish,"The button for add to wishlist is not visible").to_be_visible()
        await self.btnWish.click()
        await expect(self.btnNavwish,"The button for the wishlist is not visible").to_be_visible()
        await self.btnNavwish.click()
        await expect(self.page, "The page was not redirected to categories.").to_have_url(re.compile(r".*/wishlist"))

    async def get_information_cart(self): #Know if the cart have the item added
        cart_product_visible = self.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div")
        return cart_product_visible
    
    async def get_product_compare(self): #know if the compare option have iteams to compare
        products_in_compare = self.page.locator("#remove-compare-color-beige-1")
        return products_in_compare
    
    async def get_compare_cart(self): #know if the information for the color of the product is correct in the cart
        product_cart = self.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div > div.tf-mini-cart-info > div.meta-variant")
        return product_cart
    
    async def get_find_size(self): #know if the use of find size is showing
        find_size_option = self.page.locator("#find_size > div > div > div.tf-rte > div.tf-table-res-df")
        return find_size_option
    
    async def get_wishlist_info(self): #know if the product is visible in the wishlist
        wishlist_info = self.page.locator("#wrapper > section > div > div > div:nth-child(4) > div.card-product-wrapper > a")
        return wishlist_info

    async def get_actual_discount_price(self): #Verification for the discount and transformation of text to float
        real_price_call = await self.real_price.text_content()
        real_price_call = float(real_price_call.replace("$", ""))
        discount_price = await self.discount.text_content()
        discount_price = float(discount_price.replace("% OFF", ""))
        result_discount = (real_price_call*discount_price)/100
        result = str(real_price_call - result_discount)
        result_string = f"${result}"
        return result_string

    async def discountPrice(self): #return the discount price selector
        discount_price_text = self.discount_price
        return discount_price_text

    async def addingSecondProduct(self):
        await self.itemProductSelection.locator("div:nth-child(1) > div.card-product-wrapper > a").click()
        await expect(self.btnColor,"The button for selection of color is not visible").to_be_visible()
        await self.btnColor.click()
        await expect(self.btnSize,"The button for selection of size is not visible").to_be_visible()
        await self.btnSize.click()
        await expect(self.inputQuantity,"The input for quantity is not visible").to_be_visible()
        await self.inputQuantity.fill("1")
        await expect(self.btnAdd,"The button for add product is not visible").to_be_visible()
        await self.btnAdd.click()