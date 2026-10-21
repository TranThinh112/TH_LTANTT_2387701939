# Lab 3 - Ghi nhật ký ưu tiên bảo mật (SecureLogger)

> **Học phần:** Lập trình An toàn Thông tin (LTANTT)  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Bài thực hành:** Buổi 1 - Mục 1.6: Ghi nhật ký ưu tiên bảo mật (SecureLogger)

---

## 1. Giới thiệu tổng quan

Nhật ký hệ thống (System Logs) là thành phần then chốt trong giám sát an ninh mạng và điều tra sự cố (Digital Forensics). Tuy nhiên, việc ghi log không đúng chuẩn thường gây ra hai rủi ro lớn:
1. **Lộ lọt thông tin cá nhân và dữ liệu nhạy cảm (PII Leakage):** Mật khẩu, token, số thẻ, số định danh CCCD bị lưu trực tiếp dạng văn bản rõ.
2. **Chỉnh sửa / giả mạo nhật ký (Log Tampering):** Kẻ tấn công xóa hoặc thay đổi nội dung file log sau khi xâm nhập để che giấu dấu vết.

Hệ thống **SecureLogger** được xây dựng nhằm giải quyết triệt để hai vấn đề trên:
- Tự động phát hiện và che giấu (masking) thông tin nhạy cảm trước khi lưu xuống đĩa.
- Xuất log dạng cấu trúc chuẩn **JSON Lines**.
- Quản lý vòng đời log với cơ chế **Log Rotation** và nén tự động (`.gz`).
- Cơ chế **chống giả mạo nhật ký (Tamper Detection)** bằng chữ ký toàn vẹn mật mã SHA-256 trong file `.sig`.
- Tích hợp chặt chẽ với thư viện `SecureValidator` từ Lab 1 để ghi nhật ký quá trình kiểm tra đầu vào.

---

## 2. Cấu trúc thư mục

```text
Buoi1_23_9_26/Lab 3/
├── app.py                     # API Flask tích hợp SecureLogger và SecureValidator
├── requirements.txt           # Thư viện phụ thuộc
├── MO_TA_CHUC_NANG_LAB3.txt   # Mô tả chi tiết chức năng Lab 3
├── README.md                  # Tài liệu hướng dẫn sử dụng
├── securelogger/
│   ├── __init__.py            # Khởi tạo package securelogger
│   └── logger.py              # Triển khai lớp SecureLogger, cơ chế che PII, ký số
├── securevalidator/
│   ├── __init__.py            # Package validator tái sử dụng từ Lab 1
│   └── core.py                # Hàm kiểm tra và làm sạch dữ liệu
└── tests/
    └── test_securelogger.py   # Bộ unit test kiểm thử tự động
```

---

## 3. Các chức năng cốt lõi

| Chức năng | Thành phần | Mô tả chi tiết |
|---|---|---|
| **Đa cấp độ nhật ký** | `securelogger/logger.py` | Hỗ trợ đầy đủ 5 cấp độ chuẩn: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |
| **Định dạng cấu trúc JSON** | `JSONFormatter` | Mỗi bản ghi là một dòng JSON chứa `timestamp` (UTC ISO 8601), `level`, `logger`, `message`, `context`. |
| **Tự động che dữ liệu nhạy cảm (PII Masking)** | `PIIFilter` | Tự động nhận diện và thay thế: <br>- Email: `***@***`<br>- Số điện thoại: `***PHONE***`<br>- Số CCCD/CMND: `***ID***`<br>- Mật khẩu/Token/API Key: `***SECRET***` |
| **Quay vòng và nén file log (Log Rotation)** | `RotatingFileHandler` | Tự động phân tách file khi dung lượng vượt ngưỡng định sẵn, lưu trữ tệp cũ dưới định dạng nén `.gz` giúp tiết kiệm dung lượng. |
| **Chống giả mạo (Tamper Detection)** | `update_signature()` | Tính toán mã băm SHA-256 trên toàn bộ nội dung file log và ghi vào `secure.log.sig`. Khi kiểm tra, nếu hash không khớp hệ thống sẽ cảnh báo tệp tin đã bị can thiệp trái phép. |
| **Tích hợp xác thực đầu vào** | `app.py: log_validation()` | Ghi lại toàn bộ lịch sử các lượt kiểm tra của `SecureValidator` với dữ liệu đầu vào đã được che PII an toàn. |

---

## 4. Hướng dẫn cài đặt và chạy thử nghiệm

### 4.1. Cài đặt thư viện

Mở PowerShell tại thư mục `Buoi1_23_9_26\Lab 3`:

```powershell
cd "Buoi1_23_9_26\Lab 3"
pip install -r requirements.txt
```

### 4.2. Chạy bộ kiểm thử tự động (Unit Tests)

```powershell
python -m unittest discover tests
```

**Kết quả kiểm thử:**

```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.035s

OK
```

*Ý nghĩa:* Toàn bộ các kiểm tra về định dạng JSON, cơ chế che dữ liệu định danh PII và thuật toán phát hiện giả mạo nhật ký (Tamper Detection) đều vượt qua thành công.

---

### 4.3. Khởi động dịch vụ API Flask

```powershell
python app.py
```

Dịch vụ chạy tại địa chỉ: `http://127.0.0.1:5000/`

Các Endpoint chính được cung cấp:

| Method | Endpoint | Mục đích |
|---|---|---|
| `GET` | `/` | Hiển thị thông tin dịch vụ và hướng dẫn sử dụng API |
| `POST` | `/validate` | Tiếp nhận dữ liệu, thực hiện kiểm tra bằng `SecureValidator` và ghi log |
| `POST` | `/log` | Gửi bản ghi log tùy chỉnh để kiểm tra tính năng che giấu PII |
| `GET` | `/logs/integrity` | Kiểm tra tính toàn vẹn của tệp log thông qua so khớp chữ ký SHA-256 |

---

## 5. Hướng dẫn kiểm thử tương tác qua PowerShell

### 5.1. Kiểm tra tính năng che thông tin PII

Gửi một bản tin chứa Email và số CCCD nhạy cảm:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/log" `
  -ContentType "application/json" `
  -Body '{"level":"INFO","message":"User admin@hutech.edu.vn requested action","context":{"cccd":"079201001234","phone":"0901234567"}}'
```

**Kết quả API trả về:**
```json
{
  "logged": true,
  "level": "INFO"
}
```

Kiểm tra nội dung tệp `secure.log` sinh ra:
```json
{"context": {"cccd": "***ID***", "phone": "***PHONE***"}, "level": "INFO", "logger": "securelogger", "message": "User ***@*** requested action", "timestamp": "2026-09-23T08:15:30.123456Z"}
```
*(Ghi nhận: Toàn bộ thông tin email, số CCCD và số điện thoại đã được ẩn danh an toàn trước khi lưu trữ).*

### 5.2. Kiểm tra tính toàn vẹn của tệp nhật ký (Integrity Check)

Gửi yêu cầu kiểm tra tính nguyên vẹn:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:5000/logs/integrity"
```

**Kết quả khi log chưa bị can thiệp:**
```json
{
  "integrity_ok": true,
  "message": "Log file integrity verified successfully."
}
```

Nếu một kẻ tấn công mở tệp `secure.log` và sửa đổi dù chỉ 1 ký tự, endpoint sẽ trả về:
```json
{
  "integrity_ok": false,
  "message": "Tampering detected! Hash mismatch between log file and signature."
}
```

---

## 6. Kết luận

Hệ thống **SecureLogger** đáp ứng trọn vẹn các tiêu chuẩn an ninh thông tin hiện đại về quản trị nhật ký:
- Tuân thủ các quy định bảo vệ dữ liệu cá nhân (GDPR / Nghị định 13/2023/NĐ-CP).
- Đảm bảo tính sẵn sàng, tính bảo mật và tính toàn vẹn không thể chối bỏ của dữ liệu điều tra số.
