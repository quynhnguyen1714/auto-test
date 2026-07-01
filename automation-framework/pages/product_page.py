# ============================================================
# pages/product_page.py  ← Page Object cho trang danh sách sản phẩm
# ============================================================

from playwright.sync_api import Page, expect


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_list = page.locator(".inventory_item")
        self.product_titles = page.locator(".inventory_item_name")
        self.sort_dropdown = page.locator('[data-test="product_sort_container"]')

    def goto(self):
        """Đi đến trang danh sách sản phẩm (sau khi đã login)"""
        self.page.goto("/inventory.html")
        expect(self.product_list.first).to_be_visible()

    def expect_products_visible(self):
        """Kiểm tra danh sách sản phẩm có hiển thị không"""
        expect(self.product_list).to_have_count(6)  # Saucedemo luôn có 6 sản phẩm

    def click_product(self, product_name: str):
        """Click vào sản phẩm theo tên để xem chi tiết"""
        self.product_titles.filter(has_text=product_name).click()

    def add_to_cart(self, product_name: str):
        """Thêm sản phẩm vào giỏ hàng theo tên sản phẩm
        Ví dụ: add_to_cart('Sauce Labs Backpack')
        """
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        item.get_by_role("button", name="Add to cart").click()

    def get_cart_badge_count(self) -> str:
        """Lấy số lượng badge trên icon giỏ hàng (ví dụ: '2')"""
        badge = self.page.locator(".shopping_cart_badge")
        return badge.inner_text()

    def go_to_cart(self):
        """Đi đến trang giỏ hàng"""
        self.page.locator(".shopping_cart_link").click()
