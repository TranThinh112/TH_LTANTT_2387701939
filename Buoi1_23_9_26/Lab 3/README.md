# Lab 3 - Ghi nhật ký ưu tiên bảo mật SecureLogger

Bài này triển khai mục **1.6 THỰC HÀNH: GHI NHẬT KÝ ƯU TIÊN BẢO MẬT** trong `lab-01.pdf`.

Mục tiêu: xây dựng hệ thống `SecureLogger` có khả năng ghi log an toàn, che thông tin định danh cá nhân, quản lý luân phiên log, phát hiện chỉnh sửa trái phép và tích hợp với `SecureValidator` từ Lab 1.

## Cấu trúc thư mục

```text
Buoi1/
└── Lab 3/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── securelogger/
    │   ├── __init__.py
    │   └── logger.py
    ├── securevalidator/
    │   ├── __init__.py
    │   └── core.py
    └── tests/
        └── test_securelogger.py
```

## Chức năng đã cài đặt

| Chức năng | File | Ý nghĩa |
|---|---|---|
| Ghi log đa cấp độ | `securelogger/logger.py` | Hỗ trợ `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| Ghi log JSON | `securelogger/logger.py` | Mỗi dòng log là một JSON object dễ phân tích |
| Che PII | `securelogger/logger.py` | Che email, số điện thoại, số định danh, số thẻ, token/secret/password |
| Log rotation và nén | `securelogger/logger.py` | Dùng `RotatingFileHandler`, file cũ được nén `.gz` |
| Tamper detection | `securelogger/logger.py` | Tạo SHA-256 signature trong `secure.log.sig` |
| Tích hợp validator | `app.py` | Mỗi lần validation được ghi vào log qua `log_validation()` |

## Cài đặt

Mở terminal tại thư mục Lab 3:

```powershell
cd "C:\Users\Admin\Documents\ChatGPT\TruongThinh-1939\Buoi1\Lab 3"
pip install -r requirements.txt
```

## Chạy kiểm thử

```powershell
python -m unittest discover tests
```

Kết quả mong đợi:

```text
...
----------------------------------------------------------------------
Ran 3 tests in ...s

OK
```

Ý nghĩa:

- Kiểm tra logger có ghi JSON hợp lệ.
- Kiểm tra PII được che trước khi ghi log.
- Kiểm tra phát hiện log bị chỉnh sửa trái phép.
- Kiểm tra logger ghi lại kết quả validation từ `SecureValidator`.

## Chạy ứng dụng API

```powershell
python app.py
```

Mở trình duyệt hoặc Postman tại:

```text
http://127.0.0.1:5000/
```

Endpoint chính:

| Method | URL | Ý nghĩa |
|---|---|---|
| `GET` | `/` | Xem mô tả API |
| `POST` | `/validate` | Kiểm tra dữ liệu bằng `SecureValidator` và ghi log |
| `POST` | `/log` | Ghi một log tùy chọn để test che PII |
| `GET` | `/logs/integrity` | Kiểm tra log có bị sửa trái phép không |

## Test bằng PowerShell

### 1. Ghi log có PII

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/log" -ContentType "application/json" -Body '{"level":"INFO","message":"User nguyen@example.com phone 0912345678","context":{"cccd":"012345678901"}}'
```

Kết quả mong đợi:

```json
{"logged": true, "level": "INFO"}
```

Ý nghĩa: log được ghi thành công, nhưng email/số điện thoại/CCCD trong `secure.log` sẽ bị che.

### 2. Validation và ghi log

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/validate" -ContentType "application/json" -Body '{"validator":"email","value":"student@example.edu.vn"}'
```

Kết quả mong đợi:

```json
{"validator":"email","input":"student@example.edu.vn","result":true}
```

Ý nghĩa: email hợp lệ và lần kiểm tra được ghi vào log với input đã được che PII.

### 3. Kiểm tra toàn vẹn log

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:5000/logs/integrity"
```

Kết quả mong đợi:

```json
{"integrity_ok": true}
```

Ý nghĩa: nội dung `secure.log` khớp chữ ký SHA-256 trong `secure.log.sig`.

## File log sinh ra

Sau khi chạy API, thư mục Lab 3 sẽ có:

```text
secure.log
secure.log.sig
```

Ví dụ một dòng log:

```json
{"context":{"cccd":"***ID***"},"level":"INFO","logger":"securelogger.secure.log","message":"User ***@*** phone ***PHONE***","timestamp":"..."}
```

Ý nghĩa:

- `timestamp`: thời điểm ghi log theo UTC.
- `level`: cấp độ log.
- `message`: thông điệp đã được che PII.
- `context`: dữ liệu bổ sung đã được che PII.
- `secure.log.sig`: hash dùng để phát hiện thay đổi trái phép.

## Thống kê

| Hạng mục | Số lượng |
|---|---:|
| Module `securelogger` | 1 |
| Module `securevalidator` tích hợp lại | 1 |
| Endpoint Flask | 4 |
| Unit test | 3 |
| Cấp độ log hỗ trợ | 5 |
| Loại PII được che | 5 |

## Ghi chú bảo mật

- Không nên commit `secure.log` hoặc `secure.log.sig` lên Git.
- Hash trong `.sig` giúp phát hiện sửa log, nhưng môi trường thật nên lưu chữ ký ở nơi có phân quyền chặt hơn.
- Che PII giúp giảm rủi ro rò rỉ dữ liệu nhạy cảm khi phân tích hoặc chia sẻ log.
