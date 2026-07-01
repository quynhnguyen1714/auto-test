import pytest
from playwright.sync_api import sync_playwright, Page, expect

# ================================================================
# URL màn hình Login - thay bằng URL thực tế của bạn
# ================================================================
LOGIN_URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988/users/login"

# ================================================================
# Hàm helper: lấy textbox email (sync - bỏ async/await)
# ================================================================
def get_email_textbox(page: Page):
    return page.locator("input[type='email'], input[type='text']").first

def trigger_validation(page: Page, textbox):
    # Nhấn Tab để rời khỏi field → kích hoạt validation/error message
    textbox.press("Tab")

# ================================================================
# FIXTURE: Khởi tạo browser và page dùng chung cho tất cả test
# scope="module" = chỉ mở browser 1 lần cho cả file
# ================================================================
@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        # headless=False: hiện cửa sổ browser để quan sát
        browser = p.chromium.launch(headless=False)
        pg = browser.new_page()

        # Mở trang Login 1 lần duy nhất
        pg.goto(LOGIN_URL)

        # Trả page cho các test dùng, giữ browser mở trong suốt
        yield pg

        # Sau khi tất cả test xong mới đóng browser
        browser.close()

# ================================================================
# TEST CASE 1: Xác nhận màn hình Login hiển thị đúng thành phần
# Tiền điều kiện : Đang hiển thị màn hình Login
# Hành động      : Xác nhận hiển thị màn hình
# Kết quả mong đợi: Label「メールアドレス」và Textbox hiển thị
# ================================================================
def test_1_display_email_label_and_textbox(page: Page):
    print("\n📌 TC1: Xác nhận label và textbox hiển thị")

    # Kiểm tra label「メールアドレス」có hiển thị không
    email_label = page.get_by_text("メールアドレス")
    expect(email_label).to_be_visible()
    print("  ✅ Label 'メールアドレス' hiển thị đúng")

    # Kiểm tra textbox email có hiển thị không
    email_textbox = get_email_textbox(page)
    expect(email_textbox).to_be_visible()
    print("  ✅ Textbox email hiển thị đúng")

# ================================================================
# TEST CASE 2: Xác nhận có thể nhập ký tự vào textbox
# Tiền điều kiện : Tiếp theo TC1
# Hành động      : Thực hiện nhập ký tự
# Kết quả mong đợi: Nhập được và ký tự hiển thị trong textbox
# ================================================================
def test_2_can_type_in_textbox(page: Page):
    print("\n📌 TC2: Xác nhận có thể nhập ký tự vào textbox")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("test")

    expect(email_textbox).to_have_value("test")
    print("  ✅ Nhập được ký tự và hiển thị đúng trong textbox")

# ================================================================
# TEST CASE 3: Nhập email hợp lệ chữ thường abc@gmail.com
# Tiền điều kiện : Tiếp theo TC2
# Hành động      : Nhập「メールアドレス」= abc@gmail.com
# Kết quả mong đợi: Ký tự nhập hiển thị đúng
# ================================================================
def test_3_input_valid_email_lowercase(page: Page):
    print("\n📌 TC3: Nhập email hợp lệ chữ thường 'abc@gmail.com'")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("abc@gmail.com")

    expect(email_textbox).to_have_value("abc@gmail.com")
    print("  ✅ Email 'abc@gmail.com' hiển thị đúng trong textbox")

# ================================================================
# TEST CASE 4: Nhập email chữ HOA ABC@GMAIL.COM
# Tiền điều kiện : Tiếp theo TC3
# Hành động      : Nhập「メールアドレス」= ABC@GMAIL.COM
# Kết quả mong đợi: Ký tự nhập hiển thị đúng
# ================================================================
def test_4_input_valid_email_uppercase(page: Page):
    print("\n📌 TC4: Nhập email chữ HOA 'ABC@GMAIL.COM'")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("ABC@GMAIL.COM")

    expect(email_textbox).to_have_value("ABC@GMAIL.COM")
    print("  ✅ Email 'ABC@GMAIL.COM' hiển thị đúng trong textbox")

# ================================================================
# TEST CASE 5: Nhập email sai định dạng - thiếu domain (abc@gmail)
# Tiền điều kiện : Tiếp theo TC4
# Hành động      : Nhập「メールアドレス」= abc@gmail
# Kết quả mong đợi: Hiển thị lỗi「メールアドレスが正しくありません。」
# ================================================================
def test_5_invalid_email_missing_domain(page: Page):
    print("\n📌 TC5: Email sai định dạng 'abc@gmail' → expect lỗi")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("abc@gmail")
    trigger_validation(page, email_textbox)

    error_message = page.get_by_text("メールアドレスが正しくありません")
    expect(error_message).to_be_visible()
    print("  ✅ Hiển thị lỗi 'メールアドレスが正しくありません' đúng")

# ================================================================
# TEST CASE 6: Nhập email sai định dạng - dấu @ sai (abc!@gmail.com)
# Tiền điều kiện : Tiếp theo TC5
# Hành động      : Nhập「メールアドレス」= abc!@gmail.com
# Kết quả mong đợi: Hiển thị lỗi「メールアドレスが正しくありません。」
# ================================================================
def test_6_invalid_email_wrong_at_symbol(page: Page):
    print("\n📌 TC6: Email sai định dạng 'abc!@gmail.com' → expect lỗi")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("abc!@gmail.com")
    trigger_validation(page, email_textbox)

    error_message = page.get_by_text("メールアドレスが正しくありません")
    expect(error_message).to_be_visible()
    print("  ✅ Hiển thị lỗi 'メールアドレスが正しくありません' đúng")

# ================================================================
# TEST CASE 7: Nhập email sai định dạng - thiếu @ (test.abc)
# Tiền điều kiện : Tiếp theo TC6
# Hành động      : Nhập「メールアドレス」= test.abc
# Kết quả mong đợi: Hiển thị lỗi「メールアドレスが正しくありません。」
# ================================================================
def test_7_invalid_email_no_at_symbol(page: Page):
    print("\n📌 TC7: Email sai định dạng 'test.abc' → expect lỗi")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("test.abc")
    trigger_validation(page, email_textbox)

    error_message = page.get_by_text("メールアドレスが正しくありません")
    expect(error_message).to_be_visible()
    print("  ✅ Hiển thị lỗi 'メールアドレスが正しくありません' đúng")

# ================================================================
# TEST CASE 8: Nhập email sai định dạng - thiếu local part (@gmail.com)
# Tiền điều kiện : Tiếp theo TC7
# Hành động      : Nhập「メールアドレス」= @gmail.com
# Kết quả mong đợi: Hiển thị lỗi「メールアドレスが正しくありません。」
# ================================================================
def test_8_invalid_email_missing_local_part(page: Page):
    print("\n📌 TC8: Email sai định dạng '@gmail.com' → expect lỗi")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("@gmail.com")
    trigger_validation(page, email_textbox)

    error_message = page.get_by_text("メールアドレスが正しくありません")
    expect(error_message).to_be_visible()
    print("  ✅ Hiển thị lỗi 'メールアドレスが正しくありません' đúng")

# ================================================================
# TEST CASE 9: Nhập ký tự toàn góc (全角文字)
# Tiền điều kiện : Tiếp theo TC8
# Hành động      : Nhập ký tự toàn góc
# Kết quả mong đợi: Hiển thị lỗi「メールアドレスが正しくありません。」
# ================================================================
def test_9_input_fullwidth_characters(page: Page):
    print("\n📌 TC9: Nhập ký tự toàn góc (全角) → expect lỗi")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    email_textbox.fill("ａｂｃ＠ｇｍａｉｌ．ｃｏｍ")
    trigger_validation(page, email_textbox)

    error_message = page.get_by_text("メールアドレスが正しくありません")
    expect(error_message).to_be_visible()
    print("  ✅ Hiển thị lỗi 'メールアドレスが正しくありません' đúng")

# ================================================================
# TEST CASE 10: Xóa toàn bộ nội dung (clear all)
# Tiền điều kiện : Tiếp theo TC9
# Hành động      : Xóa toàn bộ nội dung
# Kết quả mong đợi: Hiển thị lỗi「メールアドレスを入力してください」
# ================================================================
def test_10_clear_all_content(page: Page):
    print("\n📌 TC10: Xóa toàn bộ nội dung → expect lỗi required")

    email_textbox = get_email_textbox(page)
    email_textbox.clear()
    trigger_validation(page, email_textbox)

    error_message = page.get_by_text("メールアドレスを入力してください")
    expect(error_message).to_be_visible()
    print("  ✅ Hiển thị lỗi 'メールアドレスを入力してください' đúng")