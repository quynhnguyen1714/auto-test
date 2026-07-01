# ============================================================
# tests/login/test_login.py  ← Test cases cho chức năng Login
#
# 💡 CÁCH TỔ CHỨC TEST FILE (pytest):
# - import: khai báo những gì cần dùng
# - class TestXxx: nhóm các test liên quan lại (tùy chọn)
# - def test_xxx(): mỗi hàm bắt đầu bằng test_ là một test case
# - fixture page: pytest-playwright tự cung cấp page mới cho mỗi test
#
# 💡 BEST PRACTICE được áp dụng:
# ✅ Dùng Page Object (LoginPage) → không có selector nào ở đây
# ✅ Mỗi test tự gọi login_page.goto() → không phụ thuộc test khác
# ✅ Smart wait (wait_for_url, to_be_visible) → không dùng sleep/timeout
# ============================================================

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.test_data_loader import load_users_from_json

# Đọc dữ liệu test từ file JSON một lần duy nhất khi load module
users = load_users_from_json()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture: mỗi test case nhận một LoginPage đã goto() sẵn.
    Đảm bảo mỗi test bắt đầu từ trang login sạch, KHÔNG phụ thuộc
    test khác."""
    lp = LoginPage(page)
    lp.goto()
    return lp


# ----------------------------------------------------------
# TC-L01: Login thành công với tài khoản hợp lệ
# ----------------------------------------------------------
def test_l01_login_thanh_cong_voi_valid_user(login_page: LoginPage, page: Page):
    # STEP: Nhập thông tin và đăng nhập
    login_page.login(users["validUser"]["username"], users["validUser"]["password"])

    # VERIFY: URL phải chuyển sang trang danh sách sản phẩm
    login_page.expect_login_success()
    assert "inventory" in page.url


# ----------------------------------------------------------
# TC-L02: Login thất bại với sai password
# ----------------------------------------------------------
def test_l02_login_that_bai_sai_password(login_page: LoginPage):
    # STEP: Dùng username đúng nhưng password sai
    login_page.login(users["validUser"]["username"], "wrong_password_123")

    # VERIFY: Phải có thông báo lỗi
    login_page.expect_error_message("Username and password do not match")


# ----------------------------------------------------------
# TC-L03: Login thất bại với sai username
# ----------------------------------------------------------
def test_l03_login_that_bai_sai_username(login_page: LoginPage):
    login_page.login(users["invalidUser"]["username"], users["validUser"]["password"])
    login_page.expect_error_message("Username and password do not match")


# ----------------------------------------------------------
# TC-L04: Login với username và password bỏ trống
# ----------------------------------------------------------
def test_l04_login_that_bai_de_trong_ca_hai(login_page: LoginPage):
    # STEP: Không điền gì, nhấn thẳng vào nút Login
    login_page.login("", "")
    login_page.expect_error_message("Username is required")


# ----------------------------------------------------------
# TC-L05: Login với username có giá trị, password để trống
# ----------------------------------------------------------
def test_l05_login_that_bai_de_trong_password(login_page: LoginPage):
    login_page.login(users["validUser"]["username"], "")
    login_page.expect_error_message("Password is required")
