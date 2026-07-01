# ============================================================
# pages/login_page.py  ← Page Object Model cho trang Login
#
# 💡 KHÁI NIỆM PAGE OBJECT MODEL (POM):
# Thay vì viết locator trực tiếp trong test, ta gom tất cả
# locator và action của một trang vào một CLASS riêng.
#
# LỢI ÍCH:
# - Test case chỉ gọi method, không quan tâm HTML bên trong
# - Khi HTML thay đổi, chỉ cần sửa Page Object, test giữ nguyên
# - Code dễ đọc, dễ tái sử dụng
# ============================================================

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        # 🔍 Locator dùng get_by_placeholder, get_by_role thay vì CSS selector
        # → Bền hơn vì ít bị ảnh hưởng khi class/id thay đổi
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator('[data-test="error"]')

    # ============================================================
    # ACTION METHODS - Các thao tác người dùng thực hiện
    # ============================================================

    def goto(self):
        """Mở trang login"""
        self.page.goto("/")
        # ✅ Smart wait: chờ button login xuất hiện thay vì sleep/timeout
        expect(self.login_button).to_be_visible()

    def login(self, username: str, password: str):
        """Điền form và nhấn Login"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    # ============================================================
    # ASSERTION METHODS - Kiểm tra kết quả
    # ============================================================

    def expect_login_success(self):
        """Kiểm tra login thành công → URL chuyển sang /inventory.html"""
        self.page.wait_for_url("**/inventory.html")

    def expect_error_message(self, message: str):
        """Kiểm tra thông báo lỗi hiển thị đúng nội dung"""
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(message)
