# TH_LTANTT_2387701939

Repository thực hành môn **Lập trình An ninh thông tin**.

## Thông tin bài nộp

- Mã repository: `TH_LTANTT_2387701939`
- Nội dung hiện có: `Buoi1`
- Trọng tâm đã triển khai: **Bài 1 - Lab 1: Thư viện xác thực đầu vào SecureValidator**

## Cấu trúc thư mục

```text
.
└── Buoi1/
    ├── Lab 1/
    │   ├── app.py
    │   ├── requirements.txt
    │   ├── render.yaml
    │   ├── README.md
    │   ├── securevalidator/
    │   │   ├── __init__.py
    │   │   └── core.py
    │   ├── templates/
    │   │   └── index.html
    │   └── tests/
    │       └── test_validators.py
    ├── Lab2/
    └── Lab 3/
```

## Buổi 1 - Lab 1

Lab 1 tương ứng mục **1.2 THỰC HÀNH: THƯ VIỆN XÁC THỰC ĐẦU VÀO**.

Mục tiêu là xây dựng thư viện Python `SecureValidator` để kiểm tra và làm sạch dữ liệu đầu vào, giúp giảm các rủi ro bảo mật phổ biến:

- Injection qua email/input.
- SSRF qua URL không an toàn.
- Path Traversal qua tên file.
- SQL Injection qua chuỗi đầu vào.
- XSS qua HTML input.

## Chức năng chính của SecureValidator

| Hàm | Chức năng |
|---|---|
| `validate_email(email)` | Kiểm tra định dạng email và chặn mẫu injection phổ biến. |
| `validate_url(url)` | Kiểm tra URL HTTP/HTTPS, chặn localhost và IP private để giảm SSRF. |
| `validate_filename(filename)` | Chặn truy cập vượt thư mục như `../secret.txt`. |
| `sanitize_sql_input(input_str)` | Làm sạch chuỗi đầu vào để giảm nguy cơ SQL Injection. |
| `sanitize_html_input(html_str)` | Làm sạch HTML để giảm nguy cơ XSS. |

## Cách chạy Lab 1

Mở terminal tại thư mục repository:

```powershell
cd "C:\Users\Admin\Documents\TH_LTANTT_2387701939\Buoi1\Lab 1"
```

Cài thư viện:

```powershell
pip install -r requirements.txt
```

Chạy kiểm thử:

```powershell
python -m unittest discover tests
```

Kết quả mong đợi:

```text
........
----------------------------------------------------------------------
Ran 8 tests in ...s

OK
```

Chạy giao diện web:

```powershell
python app.py
```

Mở trình duyệt:

```text
http://127.0.0.1:5000/
```

## Hướng dẫn kiểm thử thủ công

Trên giao diện web, nhập các dữ liệu mẫu sau rồi bấm **Xác thực ngay**:

| Trường | Dữ liệu mẫu | Kết quả mong đợi |
|---|---|---|
| Email | `student@example.edu.vn` | Hợp lệ |
| Email | `admin@example.com; DROP TABLE users` | Không hợp lệ |
| URL | `https://example.com` | Hợp lệ |
| URL | `http://127.0.0.1/admin` | Không hợp lệ |
| Filename | `file.txt` | Hợp lệ |
| Filename | `../secret.txt` | Không hợp lệ |
| SQL Input | `' OR 1=1; DROP TABLE users --` | Chuỗi đã được làm sạch |
| HTML Input | `<script>alert(1)</script><b>OK</b>` | HTML đã được làm sạch |

## Ý nghĩa kết quả

- `Hợp lệ`: dữ liệu đạt quy tắc kiểm tra an toàn cơ bản.
- `Không hợp lệ`: dữ liệu có định dạng sai hoặc chứa dấu hiệu tấn công.
- Chuỗi đã làm sạch: dữ liệu đầu vào nguy hiểm được loại bỏ hoặc vô hiệu hóa trước khi sử dụng.
- Unit test `OK`: toàn bộ test case trong `tests/test_validators.py` đã chạy thành công.

## Ghi chú

- README chi tiết của Lab 1 nằm tại `Buoi1/Lab 1/README.md`.
- Đây là bài thực hành về kiểm tra đầu vào, không thay thế hoàn toàn cơ chế bảo mật production.
- Khi làm việc với cơ sở dữ liệu thật, vẫn cần dùng parameterized query/prepared statement.

