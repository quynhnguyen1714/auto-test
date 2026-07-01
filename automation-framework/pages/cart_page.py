# ============================================================
# pages/cart_page.py  ← Page Object cho trang giỏ hàng
# ============================================================

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping_button = page.get_by_role("button", name="Continue Shopping")

    def goto(self):
        self.page.goto("/cart.html")
        expect(self.checkout_button).to_be_visible()

    def expect_item_in_cart(self, product_name: str):
        """Kiểm tra sản phẩm có trong giỏ hàng không"""
        item = self.cart_items.filter(has_text=product_name)
        expect(item).to_be_visible()

    def expect_cart_empty(self):
        """Kiểm tra giỏ hàng rỗng"""
        expect(self.cart_items).to_have_count(0)

    def remove_item(self, product_name: str):
        """Xóa sản phẩm khỏi giỏ hàng theo tên"""
        item = self.cart_items.filter(has_text=product_name)
        item.get_by_role("button", name="Remove").click()

    def get_item_count(self) -> int:
        """Đếm số lượng item trong giỏ"""
        return self.cart_items.count()
