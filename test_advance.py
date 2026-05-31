import os
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser

BASE_URL = "https://bsv-nhungnguyen.github.io/"

# Thư mục lưu các file evidence (screenshot, video, trace)
ARTIFACTS_DIR = Path("test_artifacts")
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR     = ARTIFACTS_DIR / "videos"
TRACES_DIR     = ARTIFACTS_DIR / "traces"

# Tạo các thư mục nếu chưa tồn tại
for folder in [SCREENSHOTS_DIR, VIDEOS_DIR, TRACES_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# =============================================================================
# HOOKS: beforeAll và afterAll (dùng scope="session")
# Chạy 1 lần duy nhất cho toàn bộ file test
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def session_hooks():
    """
    Hook beforeAll + afterAll cho toàn bộ session test.
    - beforeAll: In thông báo khởi động, cho user biết artifacts lưu ở đâu
    - afterAll:  In thông báo kết thúc session
    """
    # ---- beforeAll ----
    print("\n")
    print("=" * 60)
    print("[beforeAll] Setup môi trường test")
    print(f"  Artifacts sẽ được lưu tại: {ARTIFACTS_DIR.resolve()}")
    print(f"  - Screenshots : {SCREENSHOTS_DIR.resolve()}")
    print(f"  - Videos      : {VIDEOS_DIR.resolve()}")
    print(f"  - Traces      : {TRACES_DIR.resolve()}")
    print("=" * 60)

    # yield = ranh giới giữa beforeAll và afterAll
    yield

    # ---- afterAll ----
    print("\n")
    print("=" * 60)
    print("[afterAll] Kết thúc test session – dọn dẹp môi trường")
    print("=" * 60)


# =============================================================================
# HOOKS: beforeEach và afterEach (dùng scope="function")
# Chạy trước/sau MỖI test function
# =============================================================================

@pytest.fixture(scope="function")
def page_each(browser_instance):
    """
    Hook beforeEach + afterEach cho từng test.
    - beforeEach: Mở trang web trước khi test
    - afterEach:  Đóng page sau khi test xong
    """
    # ---- beforeEach: Tạo page mới và điều hướng đến URL ----
    page = browser_instance.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    # yield page = trả page về cho test sử dụng
    yield page

    # ---- afterEach: Đóng page ----
    page.close()


@pytest.fixture(scope="session")
def browser_instance():
    """
    Khởi động browser 1 lần cho toàn session, tắt sau khi xong.
    Dùng slow_mo=300 để thao tác chậm hơn, dễ quan sát hơn.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=300)
        yield browser
        browser.close()


# =============================================================================
# NHÓM 1: FRAMES & IFRAMES (TC01 ~ TC05)
# =============================================================================

class TestFramesAndIframes:

    def test_tc01_simple_iframe_form(self, page_each):
        page = page_each

        iframe = page.frame_locator("#demo-iframe")
        iframe.locator("#iframe-name").fill("Quynh")
        iframe.locator("#iframe-submit-btn").click()

        result = iframe.locator("#frame-output")
        result.wait_for(state="visible", timeout=5000)
        assert "Hello Quynh" in result.inner_text()

    def test_tc02_nested_iframe_level_a(self, page_each):
        page = page_each

        page.get_by_role("button", name="Load Nested Frames (A → B → C)").click(force=True)
        page.locator("#iframe-A").wait_for(state="visible", timeout=5000)
        iframe_a = page.frame_locator("#iframe-A")
        iframe_a.locator("b", has_text="Iframe A").wait_for(state="visible", timeout=5000)

        assert iframe_a.locator("b", has_text="Iframe A").is_visible()
        assert iframe_a.locator("#btn-A").is_visible() 
        assert iframe_a.locator("#btn-open-B").is_visible()

    def test_tc03_nested_iframe_level_b(self, page_each):
        page = page_each

        page.get_by_role("button", name="Load Nested Frames (A → B → C)").click(force=True)
        page.locator("#iframe-A").wait_for(state="visible", timeout=5000)

        iframe_a = page.frame_locator("#iframe-A")
        iframe_a.get_by_role("button", name="Open Iframe B").click(force=True)

        iframe_a.locator("#iframe-B").wait_for(state="visible", timeout=5000)

        iframe_b = iframe_a.frame_locator("#iframe-B")
        iframe_b.locator("b", has_text="Iframe B").wait_for(state="visible", timeout=5000)

        assert iframe_b.locator("b", has_text="Iframe B").is_visible()
        assert iframe_b.get_by_role("button", name="Click button").is_visible()
        assert iframe_b.get_by_role("button", name="Open Iframe C").is_visible()

    def test_tc04_nested_iframe_level_c(self, page_each):
        page = page_each

        page.get_by_role("button", name="Load Nested Frames (A → B → C)").click(force=True)
        page.locator("#iframe-A").wait_for(state="visible", timeout=5000)

        iframe_a = page.frame_locator("#iframe-A")
        iframe_a.get_by_role("button", name="Open Iframe B").click(force=True)
        iframe_a.locator("#iframe-B").wait_for(state="visible", timeout=5000)

        iframe_b = iframe_a.frame_locator("#iframe-B")
        iframe_b.get_by_role("button", name="Open Iframe C").click(force=True)
        iframe_b.locator("#iframe-C").wait_for(state="visible", timeout=5000)

        iframe_c = iframe_b.frame_locator("#iframe-C")
        iframe_c.locator("b", has_text="Iframe C").wait_for(state="visible", timeout=5000)

        assert iframe_c.locator("b", has_text="Iframe C").is_visible()
        assert iframe_c.get_by_role("button", name="Click button").is_visible()
    
    def test_tc05_nested_iframe_click_button(self, page_each):
        page = page_each

        page.get_by_role("button", name="Load Nested Frames (A → B → C)").click(force=True)
        page.locator("#iframe-A").wait_for(state="visible", timeout=5000)

        iframe_a = page.frame_locator("#iframe-A")
        iframe_a.get_by_role("button", name="Open Iframe B").click(force=True)
        iframe_a.locator("#iframe-B").wait_for(state="visible", timeout=5000)

        iframe_b = iframe_a.frame_locator("#iframe-B")
        iframe_b.get_by_role("button", name="Open Iframe C").click(force=True)
        iframe_b.locator("#iframe-C").wait_for(state="visible", timeout=5000)

        iframe_c = iframe_b.frame_locator("#iframe-C")
        iframe_c.locator("b", has_text="Iframe C").wait_for(state="visible", timeout=5000)

        iframe_c.get_by_role("button", name="Click button").click(force=True)

        assert iframe_c.locator("text=Iframe C Clicked!").is_visible()


# =============================================================================
# NHÓM 2: WINDOWS, TABS VÀ POPUPS (TC06 ~ TC10)
# =============================================================================

class TestWindowsAndPopups:

    def test_tc06_open_new_tab(self, browser_instance):
        # Tạo context mới để quản lý nhiều tab
        context = browser_instance.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        # expect_page() = "đặt bẫy" để bắt tab mới khi nó được mở ra
        with context.expect_page() as new_page_info:
            page.get_by_role("button", name="Open New Tab (playwright.dev)").click()

        # Lấy tab mới vừa được mở
        new_page = new_page_info.value
        new_page.wait_for_load_state("networkidle")

        # Click "Get started" trên tab mới (trang playwright.dev)
        new_page.locator("text=Get started").first.click()
        new_page.wait_for_load_state("networkidle")

        # Kiểm tra tiêu đề "Installation" xuất hiện
        assert "Installation" in new_page.title() or new_page.locator("h1", has_text="Installation").is_visible()

        context.close()

    def test_tc07_popup_window(self, browser_instance):
        context = browser_instance.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        # Bắt popup window (tương tự bắt tab mới)
        with context.expect_page() as popup_info:
            page.get_by_role("button", name="Open Popup Window").click()

        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")

        # Kiểm tra tiêu đề popup
        assert "Popup Activated" in popup.title() or popup.locator("text=Popup Activated").is_visible()

        context.close()

    def test_tc08_modal_display(self, page_each):
        page = page_each

        page.get_by_role("button", name="Open In-page Modal").click()
        page.wait_for_timeout(500)

        modal = page.locator(".modal, [role='dialog'], [class*='modal']").first
        modal.wait_for(state="visible", timeout=5000)

        assert page.get_by_text("Secure Confirmation").is_visible()

    def test_tc09_modal_confirm_action(self, page_each):
        page = page_each
        test_text = "Test123"

        page.get_by_role("button", name="Open In-page Modal").click()
        page.wait_for_timeout(500)
        page.get_by_placeholder("Enter code (e.g. 1234)").fill(test_text)

        page.locator("#modal-confirm-btn").click()
        page.wait_for_timeout(500)

        result = page.locator("#modal-result")
        assert f"Verified: {test_text}" in result.inner_text()

    def test_tc10_modal_cancel_action(self, page_each):
        page = page_each
        test_text = "Test123"

        page.get_by_role("button", name="Open In-page Modal").click()
        page.wait_for_timeout(500)
        page.get_by_placeholder("Enter code (e.g. 1234)").fill(test_text)

        page.locator("#modal-cancel-btn").click()
        page.wait_for_timeout(500)

        result_area = page.locator("#modal-result")
        result_text = result_area.inner_text() if result_area.count() > 0 else ""
        assert test_text not in result_text


# =============================================================================
# NHÓM 3: DIALOGS (ALERT, CONFIRM, PROMPT) - TC11 ~ TC17
# =============================================================================

class TestDialogs:
    def test_tc11_alert_display(self, page_each):
        page = page_each
        dialog_message = []  # Lưu nội dung dialog vào list để kiểm tra sau

        # Đăng ký handler: khi dialog xuất hiện, lưu message rồi dismiss
        def handle_dialog(dialog):
            dialog_message.append(dialog.message)
            dialog.dismiss()  # Đóng dialog (tương đương Cancel hoặc OK)

        page.on("dialog", handle_dialog)

        page.get_by_role("button", name="Trigger Alert").click()
        page.wait_for_timeout(500)

        # Kiểm tra nội dung alert
        assert len(dialog_message) > 0, "Không có dialog nào xuất hiện!"
        assert "This is a browser alert!" in dialog_message[0]

    def test_tc12_alert_click_ok(self, page_each):
        page = page_each

        # Đăng ký handler: tự động accept (click OK)
        page.on("dialog", lambda dialog: dialog.accept())

        page.get_by_role("button", name="Trigger Alert").click()
        page.wait_for_timeout(500)

        # Nếu alert đã đóng thành công, page vẫn accessible
        assert page.get_by_role("button", name="Trigger Alert").is_visible()

    def test_tc13_confirm_display(self, page_each):
        page = page_each
        dialog_message = []

        def handle_dialog(dialog):
            dialog_message.append(dialog.message)
            dialog.dismiss()

        page.on("dialog", handle_dialog)

        page.get_by_role("button", name="Trigger Confirm").click()
        page.wait_for_timeout(500)

        assert "Continue?" in dialog_message[0]

    def test_tc14_confirm_click_ok(self, page_each):
        page = page_each

        # accept() = click OK trên dialog
        page.on("dialog", lambda dialog: dialog.accept())

        page.get_by_role("button", name="Trigger Confirm").click()
        page.wait_for_timeout(500)

        result = page.locator("#confirm-result")
        assert "Confirmed" in result.inner_text()

    def test_tc15_confirm_click_cancel(self, page_each):
        page = page_each

        # dismiss() = click Cancel trên dialog
        page.on("dialog", lambda dialog: dialog.dismiss())

        page.get_by_role("button", name="Trigger Confirm").click()
        page.wait_for_timeout(500)

        result = page.locator("#confirm-result")
        assert "Cancelled" in result.inner_text()

    def test_tc16_prompt_enter_text(self, page_each):
        page = page_each
        input_text = "Test123"

        page.on("dialog", lambda dialog: dialog.accept(input_text))

        page.get_by_role("button", name="Trigger Prompt").click()
        page.wait_for_timeout(500)

        result = page.locator("#prompt-result")
        assert input_text in result.inner_text()

    def test_tc17_prompt_click_cancel(self, page_each):
        page = page_each

        page.on("dialog", lambda dialog: dialog.dismiss())

        page.get_by_role("button", name="Trigger Prompt").click()
        page.wait_for_timeout(500)

        result = page.locator("#prompt-result")
        assert "Dismissed" in result.inner_text()


# =============================================================================
# NHÓM 4: SCREENSHOTS VÀ VIDEO (TC18 ~ TC23)
# =============================================================================

class TestScreenshotAndVideo:
    """
    Test chụp ảnh màn hình và quay video.

    Playwright hỗ trợ:
    - page.screenshot()           → chụp toàn trang
    - locator.screenshot()        → chụp 1 element cụ thể
    - context = browser.new_context(record_video_dir="...")  → quay video
    """

    def test_tc18_full_page_screenshot_always(self, page_each):
        page = page_each

        page.get_by_role("button", name="Normal State").click()
        page.wait_for_timeout(500)

        assert page.get_by_text("System Normal").is_visible()

        # Chụp toàn trang và lưu vào thư mục screenshots
        screenshot_path = SCREENSHOTS_DIR / "tc18_full_page.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        print(f"\n[TC18] Screenshot đã lưu tại: {screenshot_path}")

        # Kiểm tra file đã được tạo
        assert screenshot_path.exists(), "File screenshot không được tạo!"

    def test_tc19_element_screenshot_passed(self, page_each):
        """
        TC19 - Chụp element (chỉ chụp khi failed):
        Click Normal State, kiểm tra "System Normal" → test PASSED → KHÔNG chụp ảnh.
        """
        page = page_each

        page.get_by_role("button", name="Normal State").click()
        page.wait_for_timeout(500)

        # Test sẽ pass nên KHÔNG chụp ảnh
        failed = False
        try:
            assert page.get_by_text("System Normal").is_visible()
        except AssertionError:
            failed = True

        # Chỉ chụp khi failed
        if failed:
            screenshot_path = SCREENSHOTS_DIR / "tc19_element_FAILED.png"
            page.locator("#screenshot-element").screenshot(path=str(screenshot_path))
            print(f"\n[TC19] FAILED - Element screenshot lưu tại: {screenshot_path}")
        else:
            print("\n[TC19] PASSED - Không chụp ảnh (chỉ chụp khi failed)")

        # Xác nhận không có file screenshot (vì test passed)
        assert not (SCREENSHOTS_DIR / "tc19_element_FAILED.png").exists()

    def test_tc20_element_screenshot_failed(self, page_each):
        page = page_each

        # Click Failure State để làm text thay đổi
        page.get_by_role("button", name="Failure State").click()
        page.wait_for_timeout(500)

        failed = False
        try:
            # Assert "System Normal" nhưng text thực tế đã đổi → sẽ fail
            assert page.get_by_text("System Normal").is_visible(timeout=2000)
        except Exception:
            failed = True

        # Chụp element vì test đã fail
        if failed:
            screenshot_path = SCREENSHOTS_DIR / "tc20_element_FAILED.png"
            # Chụp element #screenshot-element
            element = page.locator("#screenshot-element").first
            if element.count() > 0:
                element.screenshot(path=str(screenshot_path))
            else:
                # Fallback: chụp toàn trang
                page.screenshot(path=str(screenshot_path))
            print(f"\n[TC20] FAILED - Element screenshot lưu tại: {screenshot_path}")

        assert failed, "Test này cần fail để test logic chụp ảnh khi failed"
        assert (SCREENSHOTS_DIR / "tc20_element_FAILED.png").exists()

    def test_tc21_video_always_record(self, browser_instance):
        """
        TC21 - Quay video luôn (cả passed và failed):
        Config record_video_dir, click Play Sequence, kiểm tra "Sequence complete!".
        """
        # Tạo context với cấu hình quay video
        # record_video_dir: thư mục lưu video
        context = browser_instance.new_context(
            record_video_dir=str(VIDEOS_DIR),
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        # Click Play Sequence để bắt đầu chuỗi thao tác
        page.locator("button", has_text="Play Sequence").click()

        # Chờ text "Sequence complete!" xuất hiện (tối đa 10 giây)
        page.get_by_text("Sequence complete!").wait_for(timeout=10000)

        assert page.get_by_text("Sequence complete!").is_visible()

        # QUAN TRỌNG: Phải close context để video được lưu vào file
        page.close()
        context.close()

        # Kiểm tra có file video nào trong thư mục không
        video_files = list(VIDEOS_DIR.glob("*.webm"))
        assert len(video_files) > 0, "Không có file video nào được tạo!"
        print(f"\n[TC21] Video đã lưu: {video_files[-1]}")

    def test_tc22_video_only_on_failed_but_passed(self, browser_instance):
        """
        TC22 - Quay video chỉ khi failed, nhưng test PASSED:
        Test passed nên video sẽ bị xóa sau khi hoàn thành.
        """
        video_dir_tc22 = VIDEOS_DIR / "tc22_temp"
        video_dir_tc22.mkdir(exist_ok=True)

        context = browser_instance.new_context(
            record_video_dir=str(video_dir_tc22),
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        page.get_by_role("button", name="Play Sequence").click()

        test_failed = False
        try:
            page.get_by_text("Sequence complete!").wait_for(timeout=10000)
        except Exception:
            test_failed = True

        # Lưu đường dẫn video trước khi đóng
        video_path = page.video.path() if page.video else None

        page.close()
        context.close()

        # Nếu test PASSED → xóa video (không cần giữ lại)
        if not test_failed and video_path and Path(video_path).exists():
            Path(video_path).unlink()
            print(f"\n[TC22] Test PASSED - Video đã bị xóa (không lưu khi passed)")

        assert not test_failed, "Test này cần PASS"

    def test_tc23_video_only_on_failed_and_failed(self, browser_instance):
        """
        TC23 - Quay video chỉ khi failed, và test FAILED:
        Chờ chỉ 1 giây → text chưa xuất hiện → test fail → giữ lại video.
        """
        video_dir_tc23 = VIDEOS_DIR / "tc23_failed"
        video_dir_tc23.mkdir(exist_ok=True)

        context = browser_instance.new_context(
            record_video_dir=str(video_dir_tc23),
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        page.get_by_role("button", name="Play Sequence").click()

        test_failed = False
        try:
            # Chờ chỉ 1 giây → sẽ timeout vì sequence chưa xong
            page.get_by_text("Sequence complete!").wait_for(timeout=1000)
        except Exception:
            test_failed = True

        video_path = page.video.path() if page.video else None

        page.close()
        context.close()

        # Nếu test FAILED → giữ lại video
        if test_failed:
            print(f"\n[TC23] Test FAILED - Video được giữ lại: {video_path}")

        assert test_failed, "Test này cần FAIL (timeout 1s không đủ)"
        assert video_path and Path(video_path).exists(), "Video không tồn tại!"


# =============================================================================
# NHÓM 5: TRACING (TC24 ~ TC26) - Optional
# =============================================================================

class TestTracing:
    """
    Tracing = ghi lại toàn bộ quá trình test (screenshot, network, console, DOM)
    vào 1 file .zip để phân tích chi tiết.

    Xem trace: chạy lệnh sau trong terminal:
        playwright show-trace <đường_dẫn_file_trace.zip>

    Hoặc mở online: https://trace.playwright.dev/
    """

    def test_tc24_trace_always(self, browser_instance):
        context = browser_instance.new_context()

        # Bắt đầu ghi trace
        # screenshots=True: chụp ảnh từng bước
        # snapshots=True: lưu DOM snapshot
        # sources=True: lưu source code
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        tracing_input = page.get_by_placeholder("Developer Name").first
        tracing_input.fill("Test123")

        submission_input = page.get_by_placeholder("dev@example.com").first
        submission_input.fill("Test123")

        page.get_by_role("button", name="Submit Form").click()
        page.wait_for_timeout(1000)
        assert page.get_by_text("Submitted:").is_visible()

        # Dừng trace và lưu vào file
        trace_path = TRACES_DIR / "tc24_trace_always.zip"
        context.tracing.stop(path=str(trace_path))

        page.close()
        context.close()

        print(f"\n[TC24] Trace đã lưu: {trace_path}")
        print(f"[TC24] Xem trace bằng lệnh: playwright show-trace {trace_path}")

        assert trace_path.exists()

    def test_tc25_trace_only_on_failed_and_failed(self, browser_instance):
        """
        TC25 - Trace chỉ khi failed, và test FAILED:
        KHÔNG điền text, click Submit, expect "Both fields are required" → test fail
        → lưu trace.
        """
        context = browser_instance.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        page.get_by_role("button", name="Submit Form").click()
        page.wait_for_timeout(1000)

        test_failed = False
        trace_path = TRACES_DIR / "tc25_trace_failed.zip"

        try:
            assert page.get_by_text("Both fields are required").is_visible(timeout=3000)
        except Exception:
            test_failed = True

        # Lưu trace vì test failed (hoặc kết quả không như mong đợi)
        context.tracing.stop(path=str(trace_path))
        page.close()
        context.close()

        print(f"\n[TC25] Trace đã lưu (failed case): {trace_path}")
        print(f"[TC25] Xem trace: playwright show-trace {trace_path}")

    def test_tc26_trace_only_on_failed_but_passed(self, browser_instance):
        """
        TC26 - Trace chỉ khi failed, nhưng test PASSED:
        Test passed → KHÔNG lưu trace file.
        """
        context = browser_instance.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        tracing_input = page.get_by_placeholder("Developer Name").first
        tracing_input.fill("Test123")

        submission_input = page.get_by_placeholder("dev@example.com").first
        submission_input.fill("Test123")

        page.get_by_role("button", name="Submit Form").click()
        page.wait_for_timeout(1000)

        test_failed = False
        trace_path = TRACES_DIR / "tc26_trace_passed.zip"

        try:
            assert page.locator("text=Submitted:").is_visible()
        except Exception:
            test_failed = True

        if test_failed:
            # Lưu trace vì failed
            context.tracing.stop(path=str(trace_path))
            print(f"\n[TC26] FAILED - Trace lưu tại: {trace_path}")
        else:
            # PASSED → dừng trace mà không lưu file
            context.tracing.stop()  # Không truyền path = không lưu
            print("\n[TC26] PASSED - Không lưu trace (chỉ lưu khi failed)")

        page.close()
        context.close()

        # Xác nhận không có file trace (vì test passed)
        assert not trace_path.exists(), "Trace không nên được lưu khi test passed!"


# =============================================================================
# NHÓM 6: HOOKS - beforeEach/afterEach CHO HOOKS DEMO (TC27 ~ TC30)
# =============================================================================

class TestHooksDemo:
    """
    Test section "Hooks Demo" trên trang web.
    Demo cách dùng hooks để tự động:
    - beforeEach: Login và tạo record
    - afterEach:  Xóa record sau khi test xong
    """

    # Thông tin đăng nhập (được ghi trong trang web)
    USERNAME = "Quynh"
    PASSWORD = "Test123"

    def _login(self, page: Page):
    # Scroll đến section Hooks Demo
       page.locator("#section-hooks").scroll_into_view_if_needed()
       page.wait_for_timeout(300)
       page.locator("#hk-username").fill(self.USERNAME)
       page.locator("#hk-password").fill(self.PASSWORD)
       page.locator("#hk-btn-login").click()
       page.locator("#hk-main-section").wait_for(state="visible", timeout=5000)

    def _create_record(self, page: Page, record_name: str):
      # Dùng đúng id từ DevTools thay vì đoán
       page.locator("#hk-record-name").fill(record_name)
       page.get_by_role("button", name="Create Record").click()
       page.wait_for_timeout(500)

    def _delete_all_records(self, page: Page):
        """
        Helper function: Xóa tất cả record đang hiển thị.
        Được gọi trong afterEach để dọn dẹp sau test.
        """
        # Tìm tất cả nút Delete đang hiển thị
        delete_buttons = page.get_by_role("button", name="Delete")
        count = delete_buttons.count()

        for i in range(count):
            # Luôn click button đầu tiên (sau khi xóa, list tự refresh)
            page.get_by_role("button", name="Delete").first.click()
            page.wait_for_timeout(300)

    def test_tc29_before_each_login_and_create(self, browser_instance):
        """
        TC29 - beforeEach: Tự động login và tạo record trước test.
        Test script không cần gọi hàm login thủ công.
        """
        context = browser_instance.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        # === beforeEach logic: Login tự động ===
        print("\n[beforeEach - TC29] Đang login tự động...")
        self._login(page)

        # === Test body: Tạo record ===
        record_name = "Record-TC29"
        self._create_record(page, record_name)

        # Kiểm tra record hiển thị thành công
        assert page.locator(f"text={record_name}").is_visible(), \
            f"Record '{record_name}' không hiển thị!"
        print(f"[TC29] Record '{record_name}' đã được tạo thành công!")

        context.close()

    def test_tc30_after_each_delete_record(self, browser_instance):
        """
        TC30 - afterEach: Tự động xóa record sau khi test passed.
        Sau khi test xong, hệ thống tự xóa record → màn hình sạch cho test kế tiếp.
        """
        context = browser_instance.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        # === beforeEach logic: Login ===
        self._login(page)

        # === Test body: Tạo record ===
        record_name = "Record-TC30"
        self._create_record(page, record_name)

        assert page.locator(f"text={record_name}").is_visible(), \
            f"Record '{record_name}' không hiển thị!"

        # === afterEach logic: Xóa record sau khi test passed ===
        print(f"\n[afterEach - TC30] Đang xóa record '{record_name}'...")
        self._delete_all_records(page)
        page.wait_for_timeout(500)

        # Kiểm tra record đã bị xóa
        assert not page.locator(f"text={record_name}").is_visible(), \
            f"Record '{record_name}' vẫn còn hiển thị sau khi xóa!"
        print(f"[TC30] Record '{record_name}' đã được xóa thành công!")

        context.close()


# =============================================================================
# CHẠY TRỰC TIẾP (không qua pytest)
# =============================================================================

if __name__ == "__main__":
    # Chạy bằng: python3 autotest_advance.py
    import subprocess
    subprocess.run(["python3", "-m", "pytest", __file__, "-v", "--tb=short"])
