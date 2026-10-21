# BÁO CÁO THỰC HÀNH BUỔI 1: AN TOÀN MÃ NGUỒN VÀ DỮ LIỆU ĐẦU VÀO

> **Học phần:** Lập trình An toàn Thông tin (LTANTT)  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Ngày thực hiện:** 23/09/2026  

---

## 📑 Mục lục bài thực hành Buổi 1

1. [Lab 1: Thư viện xác thực đầu vào (SecureValidator)](#1-lab-1-thư-viện-xác-thực-đầu-vào-securevalidator)
2. [Lab 2: Bảo mật trước khi commit (GitSecure Pre-Commit Hook)](#2-lab-2-bảo-mật-trước-khi-commit-gitsecure)
3. [Lab 3: Ghi nhật ký ưu tiên bảo mật (SecureLogger)](#3-lab-3-ghi-nhật-ký-ưu-tiên-bảo-mật-securelogger)

---

## Cấu trúc thư mục Buổi 1

```text
Buoi1_23_9_26/
├── images/                        # Thư mục ảnh tổng hợp Buổi 1
│   ├── lab1_image1.png
│   ├── lab2_image1.png
│   ├── lab2_image2.png
│   ├── lab2_image3.png
│   └── lab2_image4.png
├── Lab 1/                         # Thư viện xác thực đầu vào
│   ├── app.py
│   ├── requirements.txt
│   ├── render.yaml
│   ├── MOTA_CHUCNANG_LAB1.txt
│   ├── HinhAnh.docx
│   ├── README.md
│   ├── images/image1.png
│   ├── securevalidator/
│   │   ├── __init__.py
│   │   └── core.py
│   ├── templates/index.html
│   └── tests/test_validators.py
├── Lab2/                          # Pre-commit Hook GitSecure
│   ├── .githooks/pre-commit
│   ├── examples/
│   ├── images/
│   │   ├── image1.png
│   │   ├── image2.png
│   │   ├── image3.png
│   │   └── image4.png
│   ├── tests/test_gitsecure.py
│   ├── HinhAnh.docx
│   ├── LICENSE
│   ├── MO_TA_LAB2.txt
│   ├── README.md
│   └── requirements.txt
├── Lab 3/                         # Ghi nhật ký bảo mật
│   ├── app.py
│   ├── MO_TA_CHUC_NANG_LAB3.txt
│   ├── README.md
│   ├── requirements.txt
│   ├── securelogger/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── securevalidator/
│   └── tests/test_securelogger.py
└── README.md                      # Tài liệu tổng quan Buổi 1 (file này)
```

---

## 1. Lab 1: Thư viện xác thực đầu vào (SecureValidator)

### 1.1. Mục tiêu
Xây dựng thư viện `SecureValidator` hỗ trợ kiểm tra và làm sạch dữ liệu đầu vào tại tầng ứng dụng nhằm chống lại các kỹ thuật tấn công phổ biến: SQL Injection, XSS, SSRF, Path Traversal.

### 1.2. Các chức năng chính
- `validate_email(email)`: Kiểm tra cấu trúc RFC 5322, ngăn chặn injection.
- `validate_url(url)`: Chỉ cho phép HTTP/HTTPS, chặn dải IP Private và Loopback chống SSRF.
- `validate_filename(filename)`: Chặn dấu `../` và ký tự điều khiển chống Path Traversal.
- `sanitize_sql_input(input_str)`: Làm sạch ký tự đặc biệt `'`, `;`, `--`, từ khóa nguy hiểm `DROP`, `UNION`.
- `sanitize_html_input(html_str)`: Loại bỏ các thẻ `<script>`, `<iframe>` và các event handler độc hại.

### 1.3. Kết quả chạy kiểm thử và Web UI
- Kiểm thử đơn vị: `python -m unittest discover tests` (8/8 tests passed).
- Demo trực tuyến: [https://securevalidator-e79j.onrender.com](https://securevalidator-e79j.onrender.com)
- Chạy cục bộ: `python app.py` tại `http://127.0.0.1:5000/`.

![Kết quả kiểm tra dữ liệu trên Web UI SecureValidator](Lab%201/images/image1.png)  
*Hình 1.1: Giao diện kiểm thử trực quan của SecureValidator trên trình duyệt web*

---

## 2. Lab 2: Bảo mật trước khi commit (GitSecure)

### 2.1. Mục tiêu
Thiết lập cơ chế kiểm tra tự động trước khi commit mã nguồn (Pre-Commit Hook) để ngăn chặn việc đưa secrets, khóa bí mật, thông tin định danh (PII) hoặc mã nguồn chứa lỗ hổng vào Git repository.

### 2.2. Kiểm thử và kết quả thực thi theo tài liệu Word

- **Kiểm thử tự động:** `python -m unittest discover tests` (5/5 tests passed).
- **Kích hoạt Hook:** `git config core.hooksPath "Buoi1_23_9_26/Lab2/.githooks"`.

#### Minh chứng kết quả thực thi:

| Hình ảnh | Mô tả chi tiết theo báo cáo |
|---|---|
| ![Kiểm tra scanner](Lab2/images/image1.png)<br>*Hình 2.1* | **Xác nhận scanner hoạt động:** Scanner phân tích các thay đổi diff mà không gặp lỗi hệ thống. |
| ![Đối chiếu mã nguồn](Lab2/images/image2.png)<br>*Hình 2.2* | **Đối chiếu code cấu hình:** Xác nhận sự hiện diện của `LOG_FILE`, bảng mẫu `SENSITIVE_PATTERNS`, hàm ghi nhật ký `log()` và hàm xử lý `scan_sensitive()`. |
| ![Chặn commit nguy hiểm](Lab2/images/image3.png)<br>*Hình 2.3* | **Chặn commit khi phát hiện rủi ro:** GitSecure phát hiện chuỗi secret cài cứng trong file staged và lập tức chặn lệnh commit (Exit Code 1). |
| ![Commit an toàn thành công](Lab2/images/image4.png)<br>*Hình 2.4* | **Commit thành công khi mã nguồn sạch:** Không phát hiện bất kỳ rủi ro bảo mật nào, GitSecure cho phép commit thành công (Exit Code 0). |

---

## 3. Lab 3: Ghi nhật ký ưu tiên bảo mật (SecureLogger)

### 3.1. Mục tiêu
Xây dựng giải pháp logging an toàn cho hệ thống phần mềm:
- Định dạng JSON chuẩn hóa hỗ trợ tích hợp với hệ thống SIEM.
- Tự động che thông tin định danh cá nhân (PII: Email, SĐT, CCCD, Token, Password).
- Cơ chế Log Rotation tự động chia tách và nén log dạng `.gz`.
- Cơ chế kiểm tra tính toàn vẹn (Tamper Detection) bằng chữ ký mật mã SHA-256 (`secure.log.sig`).

### 3.2. Kiểm thử và chạy API
- **Chạy Unit Test:** `python -m unittest discover tests` (3/3 tests passed).
- **Chạy Flask API:** `python app.py` tại `http://127.0.0.1:5000/`.
- **Kiểm tra tính toàn vẹn:** `GET /logs/integrity` trả về `{"integrity_ok": true}` chứng minh log chưa bị giả mạo.

---

## 4. Tổng kết Buổi 1

Các bài thực hành Buổi 1 đã trang bị đầy đủ bộ giải pháp phòng ngự 3 lớp theo định hướng DevSecOps:
1. **Lớp biên ứng dụng (Edge/Input):** `SecureValidator` làm sạch dữ liệu trước khi xử lý.
2. **Lớp phát triển phần mềm (Source/VCS):** `GitSecure` ngăn chặn rò rỉ secret và mã nguy hiểm vào kho lưu trữ.
3. **Lớp vận hành và giám sát (Runtime/Audit):** `SecureLogger` ghi log an toàn, chống lộ dữ liệu PII và bảo vệ tính toàn vẹn của nhật ký điều tra.
