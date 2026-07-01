# ============================================================
# utils/test_data_loader.py
# Hàm tiện ích để đọc dữ liệu test từ file JSON hoặc CSV.
# Tách dữ liệu ra khỏi code giúp dễ bảo trì và thay đổi.
# ============================================================

import json
import csv
import os

# Tìm thư mục gốc của project (1 cấp trên thư mục utils/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_DIR = os.path.join(BASE_DIR, "test_data")


# ============================================================
# Đọc dữ liệu từ file JSON
# Cách dùng: users = load_users_from_json()
#            users["validUser"]["username"]
# ============================================================
def load_users_from_json() -> dict:
    file_path = os.path.join(TEST_DATA_DIR, "users.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Đọc dữ liệu từ file CSV
# Trả về list các dict, mỗi dict là một dòng trong CSV
# Cách dùng: rows = load_users_from_csv()
#            for row in rows: row["username"], row["password"]
# ============================================================
def load_users_from_csv() -> list[dict]:
    file_path = os.path.join(TEST_DATA_DIR, "users.csv")
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
