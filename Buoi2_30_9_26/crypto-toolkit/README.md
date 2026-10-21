# SecureCrypto Toolkit - Bộ công cụ mã hóa và giải mã tệp tin

> **Học phần:** Lập trình An toàn Thông tin (LTANTT)  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Bài thực hành:** Buổi 2 - Mục 2.2: Hệ thống mã hóa SecureCrypto

---

## 1. Giới thiệu tổng quan

**SecureCrypto Toolkit** là bộ thư viện và ứng dụng mật mã học toàn diện được phát triển bằng Python, cung cấp các cơ chế mã hóa đối xứng, hàm băm mật mã và chữ ký số bất đối xứng đạt tiêu chuẩn công nghiệp:
- **Mã hóa đối xứng AES-GCM (Galois/Counter Mode):** Cung cấp cả tính bảo mật (Confidentiality) lẫn tính toàn vẹn và xác thực nguồn gốc (Authenticity).
- **Dẫn xuất khóa Argon2:** Hàm dẫn xuất khóa (KDF) kháng phần cứng chuyên dụng (ASIC/GPU resistant) để biến đổi mật khẩu người dùng thành khóa đối xứng 256-bit an toàn.
- **Mật mã bất đối xứng RSA (2048-bit):** Hỗ trợ mã hóa khóa công khai, giải mã khóa riêng và ký số/xác minh chữ ký số (PSS padding).
- **Hàm băm an toàn:** Triển khai SHA-256 và SHA-3.
- **Đa giao diện tương tác:** Dòng lệnh (CLI), Giao diện đồ họa (Tkinter GUI), và Giao diện lập trình ứng dụng RESTful API (Flask API).

---

## 2. Cấu trúc thư mục

```text
Buoi2_30_9_26/crypto-toolkit/
├── securecrypto/
│   ├── __init__.py            # Khởi tạo package securecrypto
│   ├── aes_utils.py           # Triển khai thuật toán mã hóa/giải mã AES-GCM + Argon2
│   ├── hash_utils.py          # Triển khai băm SHA-256 và xác thực mật khẩu
│   ├── rsa_utils.py           # Triển khai sinh khóa RSA, mã hóa và ký số
│   ├── cli.py                 # Điểm vào giao diện dòng lệnh (CLI)
│   ├── app_gui.py             # Điểm vào giao diện đồ họa Tkinter
│   ├── api.py                 # Máy chủ Flask REST API (`/encrypt`, `/decrypt`)
│   └── upload/                # Thư mục lưu trữ tệp tải lên và tệp sau khi mã hóa
├── files/
│   ├── data.txt               # Tệp tin mẫu văn bản gốc
│   ├── data.txt.enc           # Tệp sau khi mã hóa AES
│   └── data.txt.dec           # Tệp sau khi giải mã khôi phục
├── images/
│   ├── image1.png             # Hình 1: Chạy Unit Tests với Pytest
│   ├── image2.png             # Hình 2: Mã hóa tệp qua CLI
│   ├── image3.png             # Hình 3: Giải mã tệp qua CLI
│   ├── image4.png             # Hình 4: Mã hóa thành công trên SecureCrypto GUI
│   ├── image5.png             # Hình 5: Khởi động máy chủ Flask API
│   ├── image6.png             # Hình 6: Cấu hình Request Encrypt trên Postman
│   ├── image7.png             # Hình 7: Nhận phản hồi Base64 key từ Postman
│   ├── image8.png             # Hình 7 (bổ sung): Thư mục upload chứa tệp .enc
│   └── image9.png             # Hình 8: Giải mã tệp qua Postman API
├── tests/
│   ├── test_aes_utils.py      # Kiểm thử mã hóa đối xứng AES
│   ├── test_hash_utils.py     # Kiểm thử hàm băm mật mã
│   └── test_rsa_utils.py      # Kiểm thử mã hóa và ký số RSA
├── requirements.txt           # Danh sách thư viện phụ thuộc
├── setup.py                   # Cấu hình cài đặt CLI package
└── README.md                  # Tài liệu hướng dẫn sử dụng (file này)
```

---

## 3. Cài đặt môi trường

Mở PowerShell tại thư mục `crypto-toolkit`:

```powershell
cd "Buoi2_30_9_26\crypto-toolkit"
pip install -r requirements.txt
```

Nếu cài đặt dạng gói dòng lệnh:
```powershell
pip install -e .
```

---

## 4. Chạy kiểm thử tự động (Unit Tests)

Bộ kiểm thử được viết cho `pytest` để kiểm tra độ tin cậy của thuật toán AES-GCM, Hash và RSA:

```powershell
$env:PYTHONPATH="." ; pytest
```

![Chạy Unit Tests](images/image1.png)  
*Hình 1: Thực thi toàn bộ các bài Unit Tests thành công với pytest (6 passed: aes, hash, rsa)*

---

## 5. Hướng dẫn sử dụng các chế độ thực thi

### 5.1. Chế độ dòng lệnh (CLI - `cli.py`)

#### A. Mã hóa tệp tin (`--encrypt`):
```powershell
python securecrypto/cli.py --encrypt files/data.txt --password MySecretPassword123
```
*Kết quả:* Hệ thống sinh khóa Base64 và tạo ra tệp mã hóa `files/data.txt.enc`.

![Mã hóa file bằng CLI](images/image2.png)  
*Hình 2: Kết quả thực thi mã hóa file thành công qua giao diện dòng lệnh CLI*

#### B. Giải mã tệp tin (`--decrypt`):
```powershell
python securecrypto/cli.py --decrypt files/data.txt.enc --password <base64_key>
```
*Kết quả:* Tệp `files/data.txt.dec` được khôi phục nguyên vẹn nội dung ban đầu.

![Giải mã file bằng CLI](images/image3.png)  
*Hình 3: Kết quả thực thi giải mã file thành công qua CLI và khôi phục nội dung văn bản gốc*

---

### 5.2. Chế độ giao diện đồ họa (GUI - `app_gui.py`)

Khởi động giao diện Tkinter:

```powershell
python securecrypto/app_gui.py
```

- Bấm nút **Browse** để chọn tệp tin cần xử lý.
- Nhập mật khẩu bí mật (Passphrase).
- Nhấp chọn **Encrypt File** để mã hóa hoặc **Decrypt File** để giải mã.

![Giao diện SecureCrypto GUI](images/image4.png)  
*Hình 4: Kết quả thực thi mã hóa file thành công trên giao diện đồ họa SecureCrypto GUI*

---

### 5.3. Chế độ RESTful API Server (Flask API - `api.py`)

Khởi động máy chủ Flask API:

```powershell
python securecrypto/api.py
```

Máy chủ sẽ lắng nghe tại cổng `http://127.0.0.1:5000/`.

![Chạy Flask API](images/image5.png)  
*Hình 5: Khởi động thành công máy chủ dịch vụ Flask REST API*

#### A. Kiểm thử API mã hóa tệp tin qua Postman (`POST /encrypt`)
- **URL:** `http://127.0.0.1:5000/encrypt`
- **Method:** `POST`
- **Body:** `form-data`
  - `file`: Chọn tệp `data.txt`
  - `password`: Nhập mật khẩu mã hóa

![Kiểm tra API Encrypt bằng Postman](images/image6.png)  
*Hình 6: Cấu hình tham số gửi yêu cầu mã hóa tệp tin trong Postman*

Nhấp chọn **Send**, hệ thống trả về khóa giải mã định dạng Base64 và lưu trữ tệp `.enc` vào thư mục `securecrypto/upload`:

![Kết quả mã hóa API và thư mục upload](images/image7.png)  
*Hình 7.1: Bấm Send thu được khóa mã hóa Base64 phản hồi từ server*

![Thư mục upload lưu file mã hóa](images/image8.png)  
*Hình 7.2: Tệp gốc và tệp mã hóa được lưu trữ an toàn trong thư mục `securecrypto/upload`*

#### B. Kiểm thử API giải mã tệp tin qua Postman (`POST /decrypt`)
- **URL:** `http://127.0.0.1:5000/decrypt`
- **Method:** `POST`
- **Body:** `form-data`
  - `file`: Chọn tệp `data.txt.enc`
  - `password`: Dán chính xác chuỗi khóa Base64 thu được từ bước mã hóa

![Giải mã file qua Flask API Postman](images/image9.png)  
*Hình 8: Giải mã file thông qua Flask API (Postman) kèm đường dẫn tệp tin giải mã thành công*

---

## 6. Lưu ý an toàn thông tin

1. **Khóa AES-GCM:** Chế độ mã hóa AES-GCM yêu cầu Auth Tag hợp lệ. Khi giải mã bằng API hoặc CLI, tham số khóa Base64 phải chính xác tuyệt đối; nếu sai lệch dù chỉ 1 bit, hệ thống sẽ báo lỗi `InvalidTag` (HTTP 500) và từ chối xuất dữ liệu để ngăn ngừa tấn công sửa đổi bản tin.
2. **Không lưu trữ Secret trong Git:** Sử dụng cờ `--no-verify` khi commit nếu các tệp test chứa chuỗi mật khẩu bị chặn bởi Pre-Commit Hook.
