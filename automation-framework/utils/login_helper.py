# ============================================================
# utils/login_helper.py
# Hàm dùng chung để login trước khi test.
#
# 💡 TẠI SAO CẦN FILE NÀY?
# Nhiều test cần login trước (Product, Cart...).
# Thay vì copy-paste code login vào từng test,
# ta viết một function dùng chung → tránh trùng lặp.
#
# 💡 BEST PRACTICE: Mỗi test tự chuẩn bị dữ liệu
# TC02 KHÔNG phụ thuộc vào TC01.
# TC Cart KHÔNG giả định đã login sẵn từ TC Login.
# ============================================================

from playwright.sync_api import Page
from pages.login_page import LoginPage


def login_as_standard_user(page: Page):
    """Login với tài khoản standard (tài khoản hợp lệ chuẩn)"""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    # Đợi URL chuyển sang inventory để chắc chắn đã login xong
    page.wait_for_url("**/inventory.html")
