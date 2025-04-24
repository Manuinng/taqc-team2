from playwright.async_api import Page
import asyncio

class ProductPage:
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
        self.btnBuy = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > div > a.btns-full")
        self.btnCate = page.locator("#wrapper > div > div > div > div.tf-breadcrumb-prev-next > a.tf-breadcrumb-back.hover-tooltip.center")
        self.btnFind = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-variant-picker > div:nth-child(2) > div > a")
        self.btnMore = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > div > a.payment-more-option")
        self.btnComparepro = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > a.tf-product-btn-wishlist.hover-tooltip.box-icon.bg_white.compare.btn-icon-action")
        self.btnWish = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-buy-button > form > a.tf-product-btn-wishlist.hover-tooltip.box-icon.bg_white.wishlist.btn-icon-action")
        self.btnNavwish = page.locator("li.nav-wishlist a.nav-icon-item")
        self.discount_price = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-price > div.price-on-sale")
        self.real_price = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-price > div.compare-at-price")
        self.discount = page.locator("#wrapper > section:nth-child(3) > div.tf-main-product.section-image-zoom > div > div > div:nth-child(2) > div > div.tf-product-info-list.other-image-zoom > div.tf-product-info-price > div.badges-on-sale")

    async def selectColor(self): #Button for color selection
        await self.btnColor.click()

    async def selectSize(self): #Button for size selection
        await self.btnSize.click()

    async def selectMore(self): #Button for more selection of products.
        await self.moreQuantity.click()

    async def selectLess(self): #Button for less selection of products.
        await self.lessQuantity.click()

    async def inputSection(self, input_singular:str): #Input quantity of products
        await self.inputQuantity.fill(input_singular)

    async def addSelection(self): #Button for add to cart
        await self.btnAdd.click()

    async def compareSection(self): #Button for compare options
        await self.btnCompare.click()

    async def selectProduct(self): #Selection of product
        await self.productView.click()
        await self.page.wait_for_timeout(1000)

    async def addCart(self, input_test:str): #Flow for selection of product options and add to cart 
        await self.btnColor.wait_for(state='visible')
        await self.btnColor.click()
        await self.btnSize.click()
        await self.inputQuantity.fill(input_test)
        await self.btnAdd.click()
        await self.page.wait_for_timeout(1000)

    async def viewCompare(self): #Use of compare color without any color to compare
        await self.btnCompare.click()
        await self.page.wait_for_selector("#compare_color > div > div", state="visible", timeout=5000)
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(2) > div.tf-compare-color-top > label").click()
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(4) > div.tf-compare-color-top > label").click()
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(6) > div.tf-compare-color-top > label").click()
        await self.page.locator("#compare_color > div > div > div.tf-compare-color-wrapp > div > div:nth-child(8) > div.tf-compare-color-top > label").click()
        await self.page.wait_for_timeout(1000)
        await self.page.locator("#compare_color > div > div > div.header > span").click()
        await self.btnCompare.click()
        await self.page.wait_for_timeout(1000)

    async def buyOption(self): #Use of buy with option
        await self.btnBuy.click()
        await self.page.wait_for_timeout(1000)

    async def categoryOption(self): #Use of category button
        await self.btnCate.click()
        await self.page.wait_for_timeout(1000)

    async def findOption(self): #Button for the find size option
        await self.btnFind.click()
        await self.page.wait_for_timeout(1000)

    async def morepayOptions(self): #Button for more pay option
        await self.btnMore.click()
        await self.page.wait_for_timeout(1000)

    async def compareProduct(self): #Button for compare product option
        await self.btnComparepro.click()
        await self.page.wait_for_timeout(1000)

    async def wishlistOption(self): #Use of whislist button for the product
        await self.btnWish.wait_for(state='visible')
        await self.btnWish.click()
        await self.btnNavwish.wait_for(state='visible')
        await self.btnNavwish.click()
        await self.page.wait_for_timeout(2000)

    async def get_information_cart(self): #Know if the cart have the item added
        cart_product_visible = await self.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div").is_visible()
        return cart_product_visible
    
    async def get_product_compare(self): #know if the compare option have iteams to compare
        products_in_compare = await self.page.locator("#remove-compare-color-beige-1").is_visible()
        return products_in_compare
    
    async def get_compare_cart(self): #know if the information for the color of the product is correct in the cart
        product_cart = await self.page.locator("#shoppingCart > div > div > div.wrap > div.tf-mini-cart-wrap > div.tf-mini-cart-main > div > div.tf-mini-cart-items > div > div.tf-mini-cart-info > div.meta-variant").is_visible()
        return product_cart
    
    async def get_find_size(self): #know if the use of find size is showing
        find_size_option = await self.page.locator("#find_size > div > div > div.tf-rte > div.tf-table-res-df").is_visible()
        return find_size_option
    
    async def get_wishlist_info(self): #know if the product is visible in the wishlist
        wishlist_info = await self.page.locator("#wrapper > section > div > div > div:nth-child(4) > div.card-product-wrapper > a").is_visible()
        return wishlist_info

    async def get_discount_price(self): #Verification for the discount and transformation of text to float
        real_price_call = await self.real_price.text_content()
        real_price_call = float(real_price_call.replace("$", ""))
        discount_price = await self.discount.text_content()
        discount_price = float(discount_price.replace("% OFF", ""))
        result_discount = (real_price_call*discount_price)/100
        result = real_price_call - result_discount
        return result

    async def discountPrice(self): #Transformation of the discount price to float
        discount_price_text = await self.discount_price.text_content()
        discount_price_text = float(discount_price_text.replace("$", ""))
        return discount_price_text
