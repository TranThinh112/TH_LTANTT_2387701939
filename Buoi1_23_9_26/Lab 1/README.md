# Lab 1 - Thư viện xác thực đầu vào SecureValidator

Bài này triển khai mục **1.2 THỰC HÀNH: THƯ VIỆN XÁC THỰC ĐẦU VÀO** trong file `lab-01.pdf`.

Mục tiêu: xây dựng thư viện Python `SecureValidator` để kiểm tra và làm sạch dữ liệu đầu vào, giúp giảm rủi ro từ các lỗi bảo mật phổ biến như Injection, SSRF, Path Traversal và XSS.

## Demo trực tuyến (Render)

- Đường dẫn chạy thật: https://securevalidator-e79j.onrender.com
- Giao diện gồm 5 ô nhập: `Email`, `URL`, `Filename`, `SQL Input`, `HTML Input`.
- Bấm **Xác thực ngay** để xem kết quả kiểm tra / làm sạch dữ liệu.

Cấu hình deploy trên Render:

| Field | Value |
|---|---|
| Name | `securevalidator` |
| Runtime | `Python 3` |
| Branch | `main` |
| Root Directory | `Buoi1/Lab 1` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Instance Type | `Free` |

> Lưu ý: Render gói Free sẽ tự "ngủ" sau khoảng 15 phút không có truy cập. Lần mở lại đầu tiên có thể chậm khoảng 30-60 giây, đây là hiện tượng bình thường, không phải lỗi ứng dụng.

## Cấu trúc thư mục

```text
Buoi1/
└── Lab 1/
    ├── app.py
    ├── requirements.txt
    ├── render.yaml
    ├── securevalidator/
    │   ├── __init__.py
    │   └── core.py
    ├── templates/
    │   └── index.html
    └── tests/
        └── test_validators.py
```

## Chức năng đã cài đặt

| Hàm | Mục đích | Ý nghĩa bảo mật |
|---|---|---|
| `validate_email(email)` | Kiểm tra email hợp lệ | Chặn định dạng sai, ký tự điều khiển và mẫu injection phổ biến |
| `validate_url(url)` | Kiểm tra URL hợp lệ | Chỉ cho phép HTTP/HTTPS, chặn localhost/IP private để giảm SSRF |
| `validate_filename(filename)` | Kiểm tra tên file | Chặn `../`, `%2f`, đường dẫn tuyệt đối và truy cập vượt thư mục |
| `sanitize_sql_input(input_str)` | Làm sạch chuỗi SQL input | Loại bỏ token nguy hiểm như `DROP`, `UNION`, `--`, `;` |
| `sanitize_html_input(html_str)` | Làm sạch HTML input | Loại bỏ/escape script và thuộc tính nguy hiểm để giảm XSS |

## Cài đặt

Mở terminal tại thư mục gốc repository, sau đó vào thư mục lab:

```powershell
cd "Buoi1\Lab 1"
pip install -r requirements.txt
```

Nếu muốn dùng môi trường ảo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Chạy kiểm thử

Tại thư mục `Buoi1\Lab 1`, chạy:

```powershell
python -m unittest discover tests
```

Kết quả hiện tại:

```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.012s

OK
```

Ý nghĩa:

- Mỗi dấu `.` là một test case chạy thành công.
- `OK` nghĩa là toàn bộ test đã pass.
- Bộ test gồm dữ liệu hợp lệ và dữ liệu độc hại cho email, URL, filename, SQL input và HTML input.

## Chạy giao diện web

Tại thư mục `Buoi1\Lab 1`, chạy:

```powershell
python app.py
```

Mở trình duyệt:

```text
http://127.0.0.1:5000/
```

Giao diện gồm 5 ô nhập giống mẫu bài lab: `Email`, `URL`, `Filename`, `SQL Input`, `HTML Input`. Bấm **Xác thực ngay** để xem kết quả.

## Dữ liệu mẫu để kiểm thử thủ công

| Trường | Input | Kết quả mong đợi | Ý nghĩa |
|---|---|---|---|
| Email | `student@example.edu.vn` | Hợp lệ | Email đúng định dạng |
| Email | `admin@example.com; DROP TABLE users` | Không hợp lệ | Chứa mẫu injection |
| URL | `https://example.com` | Hợp lệ | URL public dùng HTTPS |
| URL | `http://127.0.0.1/admin` | Không hợp lệ | Chặn SSRF tới localhost |
| Filename | `file.txt` | Hợp lệ | Tên file an toàn |
| Filename | `../secret.txt` | Không hợp lệ | Chặn path traversal |
| SQL Input | `' OR 1=1; DROP TABLE users --` | Chuỗi đã làm sạch | Giảm rủi ro SQL Injection |
| HTML Input | `<script>alert(1)</script><b>OK</b>` | HTML đã làm sạch | Giảm rủi ro XSS |

## Thống kê

| Hạng mục | Số lượng |
|---|---:|
| Hàm validator/sanitizer | 5 |
| File Python thư viện | 2 |
| File Flask demo | 1 |
| File giao diện HTML | 1 |
| Unit test | 8 |
| File cấu hình deploy Render | 1 |

## Ghi chú

- Đây là bài thực hành về kiểm tra và làm sạch đầu vào, không thay thế hoàn toàn các lớp bảo mật production.
- Với SQL thật, luôn dùng truy vấn tham số hóa thay vì nối chuỗi SQL.
- Với SSRF production, nên kiểm tra thêm DNS resolution, redirect và cấu hình firewall/egress rule.
- Với HTML production, nên dùng thư viện chuyên dụng như `bleach` và cấu hình whitelist phù hợp.
