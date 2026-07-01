# ============================================================
# pages/product_detail_page.py  ← Page Object cho trang chi tiết sản phẩm
# ============================================================

from playwright.sync_api import Page, expect


class ProductDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_name = page.locator(".inventory_details_name")
        self.product_description = page.locator(".inventory_details_desc")
        self.product_price = page.locator(".inventory_details_price")
        self.add_to_cart_button = page.get_by_role("button", name="Add to cart")
        self.back_button = page.get_by_role("button", name="Back to products")

    def expect_page_loaded(self, expected_product_name: str):
        """Kiểm tra trang chi tiết đã load đúng chưa"""
        expect(self.product_name).to_be_visible()
        expect(self.product_name).to_have_text(expected_product_name)
        expect(self.product_price).to_be_visible()
        expect(self.add_to_cart_button).to_be_visible()

    def get_price(self) -> str:
        """Lấy giá sản phẩm dưới dạng string (ví dụ: '$29.99')"""
        return self.product_price.inner_text()
