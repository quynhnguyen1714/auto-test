# ============================================================
# conftest.py
# File đặc biệt của pytest — chứa các fixture/cấu hình dùng
# chung cho TOÀN BỘ project (giống playwright.config.ts bên TS).
#
# Project này dùng plugin pytest-playwright (cài qua requirements.txt),
# plugin này đã tự cung cấp sẵn fixture "page" cho mỗi test case
# (mỗi test 1 page riêng → các test ĐỘC LẬP với nhau).
#
# Ta chỉ cần override fixture có sẵn của plugin để set baseURL chung.
# ============================================================

import pytest

BASE_URL = "https://www.saucedemo.com"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override fixture có sẵn của pytest-playwright để set baseURL chung.
    Sau khi set, trong test chỉ cần page.goto('/') thay vì gõ full URL."""
    return {
        **browser_context_args,
        "base_url": BASE_URL,
    }


# ============================================================
# Cách dùng các cờ CLI có sẵn của pytest-playwright:
#   pytest --headed                  → mở browser thấy được
#   pytest --browser firefox         → chạy trên Firefox
#   pytest --browser webkit          → chạy trên WebKit (Safari engine)
#   pytest --slowmo 1000             → chạy chậm lại 1000ms mỗi action
#   pytest -n 4                      → chạy song song 4 worker (cần pytest-xdist)
# ============================================================
