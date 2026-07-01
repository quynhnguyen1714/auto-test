# ============================================================
# tests/cart/test_cart.py  ← Test cases cho chức năng Cart
# ============================================================

import pytest
from playwright.sync_api import Page, expect
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.login_helper import login_as_standard_user


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    """Mỗi test tự login và tạo ProductPage riêng"""
    login_as_standard_user(page)
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


# ----------------------------------------------------------
# TC-C01: Thêm một sản phẩm vào giỏ hàng
# ----------------------------------------------------------
def test_c01_add_product_vao_cart(product_page: ProductPage, cart_page: CartPage):
    product_name = "Sauce Labs Backpack"

    # STEP: Thêm sản phẩm từ trang danh sách
    product_page.add_to_cart(product_name)

    # VERIFY: Badge giỏ hàng phải hiển thị số "1"
    badge_count = product_page.get_cart_badge_count()
    assert badge_count == "1"

    # STEP: Vào trang giỏ hàng
    product_page.go_to_cart()

    # VERIFY: Sản phẩm phải có trong giỏ
    cart_page.expect_item_in_cart(product_name)


# ----------------------------------------------------------
# TC-C02: Thêm nhiều sản phẩm vào giỏ hàng
# ----------------------------------------------------------
def test_c02_add_nhieu_product_vao_cart(product_page: ProductPage, cart_page: CartPage):
    # STEP: Thêm 2 sản phẩm
    product_page.add_to_cart("Sauce Labs Backpack")
    product_page.add_to_cart("Sauce Labs Bike Light")

    # VERIFY: Badge phải hiện số 2
    badge_count = product_page.get_cart_badge_count()
    assert badge_count == "2"

    # STEP: Vào giỏ hàng kiểm tra
    product_page.go_to_cart()
    item_count = cart_page.get_item_count()
    assert item_count == 2


# ----------------------------------------------------------
# TC-C03: Xóa sản phẩm khỏi giỏ hàng
# ----------------------------------------------------------
def test_c03_remove_product_khoi_cart(product_page: ProductPage, cart_page: CartPage, page: Page):
    product_name = "Sauce Labs Backpack"

    # SETUP: Thêm sản phẩm trước
    product_page.add_to_cart(product_name)
    product_page.go_to_cart()

    # VERIFY: Có sản phẩm trong giỏ
    cart_page.expect_item_in_cart(product_name)

    # STEP: Xóa sản phẩm
    cart_page.remove_item(product_name)

    # VERIFY: Giỏ hàng phải rỗng
    cart_page.expect_cart_empty()

    # VERIFY: Badge giỏ hàng không còn hiển thị
    expect(page.locator(".shopping_cart_badge")).not_to_be_visible()


# ----------------------------------------------------------
# TC-C04: Xóa một sản phẩm khi giỏ có nhiều sản phẩm
# ----------------------------------------------------------
def test_c04_remove_mot_product_khi_co_nhieu_item(product_page: ProductPage, cart_page: CartPage):
    # SETUP: Thêm 2 sản phẩm
    product_page.add_to_cart("Sauce Labs Backpack")
    product_page.add_to_cart("Sauce Labs Bike Light")
    product_page.go_to_cart()

    # STEP: Xóa chỉ sản phẩm đầu tiên
    cart_page.remove_item("Sauce Labs Backpack")

    # VERIFY: Chỉ còn 1 sản phẩm
    item_count = cart_page.get_item_count()
    assert item_count == 1

    # VERIFY: Sản phẩm còn lại vẫn có trong giỏ
    cart_page.expect_item_in_cart("Sauce Labs Bike Light")
