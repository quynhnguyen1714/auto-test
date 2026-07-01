# 🤖 Automation Framework - SauceDemo (Python + Playwright + pytest)

Framework automation test cho [saucedemo.com](https://www.saucedemo.com) sử dụng **Python + Playwright + pytest**.

---

## 📁 Cấu trúc Framework

```
automation-framework-py/
├── pages/                          ← Page Object Model
│   ├── login_page.py                  Trang đăng nhập
│   ├── product_page.py                Trang danh sách sản phẩm
│   ├── product_detail_page.py         Trang chi tiết sản phẩm
│   └── cart_page.py                   Trang giỏ hàng
│
├── tests/                          ← Test Cases (chia theo module)
│   ├── login/
│   │   └── test_login.py              TC-L01 đến TC-L05
│   ├── product/
│   │   └── test_product.py            TC-P01 đến TC-P03
│   ├── cart/
│   │   └── test_cart.py               TC-C01 đến TC-C04
│   └── checkout/                      (mở rộng thêm sau)
│
├── test_data/                      ← Dữ liệu Test (tách riêng khỏi code)
│   ├── users.json                     Dữ liệu dạng JSON
│   └── users.csv                      Dữ liệu dạng CSV
│
├── utils/                          ← Tiện ích dùng chung
│   ├── test_data_loader.py            Đọc file JSON/CSV
│   └── login_helper.py                Hàm login tái sử dụng
│
├── conftest.py                     ← Cấu hình pytest-playwright (baseURL...)
├── pytest.ini                      ← Cấu hình pytest
├── requirements.txt
└── README.md
```

---

## 🚀 Cách chạy test

### Bước 1: Cài đặt (chỉ cần làm 1 lần)
```bash
# Tạo virtual environment (khuyến khích)
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate          # Windows

# Cài thư viện
pip3 install -r requirements.txt --break-system-packages

# Cài browser cho Playwright
playwright install
```

### Bước 2: Chạy test

| Lệnh | Mô tả |
|------|-------|
| `pytest` | Chạy toàn bộ test (chế độ headless - không thấy browser) |
| `pytest --headed` | Chạy có hiển thị browser |
| `pytest --headed --slowmo 1000` | Chạy chậm lại 1000ms mỗi action, dễ quan sát |
| `pytest tests/login/` | Chỉ chạy module Login |
| `pytest tests/product/` | Chỉ chạy module Product |
| `pytest tests/cart/` | Chỉ chạy module Cart |
| `pytest --browser firefox` | Chỉ chạy trên Firefox |
| `pytest --browser webkit` | Chỉ chạy trên WebKit (engine của Safari) |
| `pytest -k test_l01` | Chạy đúng 1 test case theo tên hàm |
| `pytest -v` | In chi tiết tên từng test khi chạy |

---

## 📊 Cách thêm Test Data

### Thêm user mới vào JSON (`test_data/users.json`):
```json
{
  "validUser": { "username": "standard_user", "password": "secret_sauce" },
  "newUser": { "username": "new_username", "password": "new_password" }
}
```

### Thêm dòng mới vào CSV (`test_data/users.csv`):
```
type,username,password,expected_result
valid,standard_user,secret_sauce,login_success
new_case,new_user,new_pass,login_fail
```

### Đọc data trong test:
```python
from utils.test_data_loader import load_users_from_json, load_users_from_csv

# Đọc JSON
users = load_users_from_json()
login_page.login(users["validUser"]["username"], users["validUser"]["password"])

# Đọc CSV
csv_users = load_users_from_csv()
for row in csv_users:
    # dùng row["username"], row["password"]
    pass
```

---

## 🏗️ Cách áp dụng Page Object Model (POM)

### ❌ CÁCH SAI (không dùng POM):
```python
# Test case viết trực tiếp selector → khó bảo trì
def test_login(page):
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
```

### ✅ CÁCH ĐÚNG (dùng POM):
```python
# Bước 1: Tạo Page Object (pages/login_page.py)
class LoginPage:
    def __init__(self, page):
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)

# Bước 2: Dùng trong test - rất gọn và dễ đọc
def test_login(page):
    login_page = LoginPage(page)
    login_page.login("standard_user", "secret_sauce")
```

**Lợi ích:** Khi selector thay đổi, chỉ sửa `login_page.py` - không cần sửa từng test.

---

## ✅ Best Practices được áp dụng

### 1. Độc lập giữa các test (No Test Dependency)
```python
# Mỗi test có fixture riêng để tự chuẩn bị dữ liệu
@pytest.fixture
def product_page(page):
    login_as_standard_user(page)  # tự login, không nhờ test khác
    return ProductPage(page)
```

### 2. Smart Wait (không dùng time.sleep)
```python
# ❌ SAI - hardcode thời gian, không ổn định
import time
time.sleep(5)

# ✅ ĐÚNG - chờ đến khi element thật sự hiển thị
expect(login_button).to_be_visible()
page.wait_for_url("**/inventory.html")
```

### 3. Locator ưu tiên semantic
```python
# Ưu tiên dùng role/placeholder (dễ đọc, bền hơn)
page.get_by_role("button", name="Login")
page.get_by_placeholder("Username")

# Dùng data-test attribute nếu có
page.locator('[data-test="error"]')
```

### 4. Dùng sync Playwright + fixture pytest
Theo đúng kiểu đã học: sync API, `@pytest.fixture` để chia sẻ và chuẩn bị state cho test.

---

## 📋 Danh sách Test Cases

| ID | Module | Mô tả | Expected |
|----|--------|-------|----------|
| TC-L01 | Login | Login với valid user | Vào trang /inventory.html |
| TC-L02 | Login | Login sai password | Hiển thị error message |
| TC-L03 | Login | Login sai username | Hiển thị error message |
| TC-L04 | Login | Login để trống cả 2 | Báo lỗi "Username is required" |
| TC-L05 | Login | Login để trống password | Báo lỗi "Password is required" |
| TC-P01 | Product | Hiển thị danh sách | Có 6 sản phẩm |
| TC-P02 | Product | Xem chi tiết sản phẩm | Đúng tên, hiển thị giá |
| TC-P03 | Product | Quay lại từ chi tiết | Về trang danh sách |
| TC-C01 | Cart | Add 1 sản phẩm | Badge = 1, có trong cart |
| TC-C02 | Cart | Add nhiều sản phẩm | Badge = 2 |
| TC-C03 | Cart | Remove sản phẩm | Giỏ rỗng, badge ẩn |
| TC-C04 | Cart | Remove 1 trong nhiều | Còn 1 sản phẩm đúng |
