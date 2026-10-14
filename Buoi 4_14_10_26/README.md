# 🛡️ BÀI THỰC HÀNH SỐ 4: BẢO MẬT WEB APP VÀ API

Tài liệu hướng dẫn và mã nguồn thực hành các lỗ hổng bảo mật ứng dụng Web phổ biến (XSS, SQL Injection, CSRF, SSRF) và triển khai cơ chế xác thực an toàn với JSON Web Token (JWT) theo chuẩn OAuth 2.0.

---

## 👨‍🎓 Thông tin sinh viên
* **Họ và tên:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Học phần:** Lập trình An toàn Thông tin (LTANTT)
* **Trường:** Đại học Công nghệ TP.HCM (HUTECH)

---

## 📂 Cấu trúc thư mục Lab 4

```text
Buoi 4_14_10_26/
│
├── 📁 web-vuln-scanner/            # Phần 4.2: Công cụ dò quét lỗ hổng ứng dụng Web
│   ├── 📁 report/                  # Module tạo báo cáo tổng hợp kết quả quét
│   │   ├── __init__.py
│   │   └── report_generator.py
│   ├── 📁 scanners/                # Các module quét lỗ hổng chuyên biệt
│   │   ├── __init__.py
│   │   ├── csrf_detector.py        # Kiểm tra Anti-CSRF Token trong HTML form
│   │   ├── sql_injection_tester.py # Kiểm tra các biến thể SQL Injection qua tham số URL
│   │   ├── ssrf_tester.py          # Phát hiện nguy cơ SSRF truy cập IP/dải mạng nội bộ
│   │   └── xss_scanner.py          # Kiểm thử chèn mã độc Cross-Site Scripting (XSS)
│   ├── 📁 tests/                   # Bộ UnitTest kiểm thử tự động các scanner
│   │   ├── __init__.py
│   │   ├── test_csrf.py
│   │   ├── test_report.py
│   │   ├── test_sql_injection.py
│   │   ├── test_ssrf.py
│   │   └── test_xss.py
│   ├── 📁 ui/                      # Giao diện Web kiểm thử tương tác (Flask)
│   │   ├── 📁 templates/
│   │   │   ├── index.html          # Form nhập URL và chọn scanner
│   │   │   └── result.html         # Giao diện hiển thị báo cáo lỗ hổng trực quan
│   │   └── app.py                  # Máy chủ Flask chạy Web UI
│   ├── main.py                     # Script thực thi quét mẫu trên Terminal
│   └── requirements.txt            # Danh sách thư viện phụ thuộc
│
└── 📁 jwt-security-tools/          # Phần 4.4: Bộ công cụ bảo mật và xác thực JWT
    ├── 📁 api_gateway/             # Cổng API tích hợp middleware xác thực Bearer Token
    │   ├── __init__.py
    │   └── gateway.py              # Endpoint bảo vệ /protected (yêu cầu JWT hợp lệ)
    ├── 📁 jwt_cracker/             # Module tấn công dò khóa bí mật JWT
    │   ├── __init__.py
    │   └── cracker.py              # Brute-force khóa bí mật HMAC-SHA256 đa luồng
    ├── 📁 jwt_validator/           # Module thẩm định toàn diện tính an toàn của JWT
    │   ├── __init__.py
    │   └── validator.py            # Kiểm tra chữ ký, thời hạn sống (exp), cấu trúc token
    ├── 📁 oauth_client/            # Client tuân thủ chuẩn luồng xác thực OAuth 2.0
    │   ├── __init__.py
    │   └── client.py               # Tạo URL ủy quyền và trao đổi Authorization Code
    ├── 📁 token_manager/           # Quản lý vòng đời Access Token và Refresh Token
    │   ├── __init__.py
    │   └── manager.py              # Cấp phát token, gia hạn Access Token mới
    ├── 📁 tests/                   # Bộ kiểm thử tự động với PyTest
    │   ├── __init__.py
    │   ├── test_api_gateway.py
    │   ├── test_cracker.py
    │   ├── test_oauth_client.py
    │   ├── test_token_manager.py
    │   └── test_validator.py
    ├── main.py                     # Khởi tạo Token và kích hoạt API Gateway
    ├── pytest.ini                  # Cấu hình đường dẫn cho PyTest
    └── requirements.txt            # Thư viện phụ thuộc (PyJWT, Flask, PyTest, ...)
```

---

## 🚀 Hướng dẫn cài đặt và Chạy kiểm thử

### Yêu cầu tiên quyết
* Python 3.10 trở lên.
* Đã cài đặt công cụ quản lý gói `pip`.

---

### PHẦN 1: BÀI 4.2 - WEBVULNSCANNER (`web-vuln-scanner`)

Di chuyển vào thư mục:
```powershell
cd web-vuln-scanner
```

#### 1. Cài đặt thư viện:
```powershell
pip install -r requirements.txt
```

#### 2. Chạy bộ kiểm thử tự động (UnitTest):
```powershell
python -m unittest discover tests
```
* **Kết quả kỳ vọng:** `Ran 9 tests in ...s - OK` (Toàn bộ 9/9 test case đều vượt qua).

#### 3. Chạy chương trình quét mẫu Console:
```powershell
python main.py
```
* Chương trình sẽ quét một URL và HTML mẫu, in ra báo cáo phát hiện lỗ hổng `SQL Injection` và `SSRF` trực tiếp trên Terminal.

#### 4. Khởi chạy giao diện Web UI:
```powershell
python ui/app.py
```
* Mở trình duyệt truy cập: `http://127.0.0.1:5000/`
* Nhập URL cần kiểm thử, tích chọn các scanner tương ứng và nhấn **Bắt đầu kiểm thử**.
* Để kiểm thử phản chiếu XSS ổn định cục bộ, có thể nhập URL:
  ```text
  http://127.0.0.1:5000/demo-xss
  ```

---

### PHẦN 2: BÀI 4.4 - JWTSECURE (`jwt-security-tools`)

Di chuyển vào thư mục:
```powershell
cd ../jwt-security-tools
```

#### 1. Cài đặt thư viện:
```powershell
pip install -r requirements.txt
```

#### 2. Chạy kiểm thử tự động với PyTest:
```powershell
pytest
```
* **Kết quả kỳ vọng:** `7 passed` (Đạt 100% các bài test: Gateway, Cracker, OAuth, TokenManager, Validator).

#### 3. Khởi chạy API Gateway và cấp phát Token:
Mở cửa sổ Terminal thứ nhất:
```powershell
python main.py
```
* Terminal sẽ in ra cặp khóa:
  * `Access Token`: Chuỗi JWT dùng để xác thực truy cập tài nguyên (hạn 15 phút).
  * `Refresh Token`: Chuỗi JWT dùng để cấp lại Access Token mới (hạn 24 giờ).
* Máy chủ Flask tự động khởi động tại `http://127.0.0.1:5000`.

#### 4. Kiểm tra xác thực API Gateway:
Mở một cửa sổ Terminal thứ hai (song song):

* **Trường hợp gửi Token hợp lệ (Được cấp quyền - HTTP 200):**
  * *Trên PowerShell:*
    ```powershell
    $token = "<DÁN_CHUỖI_ACCESS_TOKEN_VÀO_ĐÂY>"
    Invoke-RestMethod -Uri "http://127.0.0.1:5000/protected" -Headers @{ Authorization = "Bearer $token" }
    ```
  * *Hoặc dùng cURL:*
    ```cmd
    curl.exe -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/protected
    ```
  * **Phản hồi:**
    ```json
    { "message": "Access granted", "user": "phuoc" }
    ```

* **Trường hợp gửi Token giả mạo/không hợp lệ (Bị từ chối - HTTP 401):**
  * *Trên PowerShell:*
    ```powershell
    Invoke-RestMethod -Uri "http://127.0.0.1:5000/protected" -Headers @{ Authorization = "Bearer invalid_token" }
    ```
  * **Phản hồi:** Báo lỗi `401 Unauthorized` kèm nội dung `{"message": "Access denied"}`.

---

## 🔒 Cơ chế bảo mật và Ghi chú kỹ thuật
1. **Quy tắc GitSecure:** Toàn bộ khóa bí mật mẫu (`secret`) trong mã nguồn kiểm thử được cấu hình an toàn, tránh vi phạm bộ quy tắc rà quét thông tin nhạy cảm của pre-commit hook GitSecure.
2. **Chu kỳ sống của JWT:**
   * Thuật toán ký: **HMAC-SHA256 (`HS256`)**.
   * Thuộc tính `exp` lưu theo thời gian thực (Unix timestamp UTC), giúp token tự động vô hiệu hóa sau khi hết hạn mà không cần lưu trạng thái trên cơ sở dữ liệu (Stateless).
