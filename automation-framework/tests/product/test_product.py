# ============================================================
# tests/product/test_product.py  ← Test cases cho chức năng Product
#
# 💡 LƯU Ý QUAN TRỌNG - ĐỘC LẬP GIỮA CÁC TEST:
# Module Product cần login trước mới vào được trang sản phẩm.
# CÁCH SAI: dựa vào TC Login đã chạy trước đó để có sẵn session
# CÁCH ĐÚNG: mỗi test tự login trong fixture của riêng nó
# → Dù chạy riêng lẻ hay cả suite, test vẫn pass
# ============================================================

import pytest
from playwright.sync_api import Page, expect
from pages.product_page import ProductPage
from pages.product_detail_page import ProductDetailPage
from utils.login_helper import login_as_standard_user


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    """Mỗi test tự login → không phụ thuộc test nào khác"""
    login_as_standard_user(page)
    return ProductPage(page)


# ----------------------------------------------------------
# TC-P01: Kiểm tra trang danh sách sản phẩm hiển thị đúng
# ----------------------------------------------------------
def test_p01_hien_thi_danh_sach_san_pham(product_page: ProductPage, page: Page):
    # VERIFY: Phải có đúng 6 sản phẩm trên trang
    product_page.expect_products_visible()

    # VERIFY: Tiêu đề trang phải hiển thị
    expect(page.locator(".title")).to_have_text("Products")


# ----------------------------------------------------------
# TC-P02: Xem chi tiết một sản phẩm cụ thể
# ----------------------------------------------------------
def test_p02_xem_chi_tiet_san_pham(product_page: ProductPage, page: Page):
    target_product = "Sauce Labs Backpack"

    # STEP: Click vào tên sản phẩm
    product_page.click_product(target_product)

    # VERIFY: Trang chi tiết phải load đúng sản phẩm
    detail_page = ProductDetailPage(page)
    detail_page.expect_page_loaded(target_product)

    # VERIFY: Giá phải có định dạng $XX.XX
    price = detail_page.get_price()
    assert price.startswith("$")
    assert "." in price


# ----------------------------------------------------------
# TC-P03: Kiểm tra có thể quay lại trang danh sách từ chi tiết
# ----------------------------------------------------------
def test_p03_quay_lai_danh_sach_tu_trang_chi_tiet(product_page: ProductPage, page: Page):
    product_page.click_product("Sauce Labs Bike Light")

    detail_page = ProductDetailPage(page)
    detail_page.back_button.click()

    # VERIFY: URL phải quay về /inventory.html
    page.wait_for_url("**/inventory.html")
    product_page.expect_products_visible()
