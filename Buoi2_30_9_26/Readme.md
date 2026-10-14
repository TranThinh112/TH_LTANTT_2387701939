# SecureCrypto & Mini CA Toolkit

## 1. Yêu cầu cài đặt

* Python 3.9+


* Cài đặt thư viện:

```bash
pip install cryptography flask argon2-cffi

```

---

## 2. SecureCrypto Toolkit

Hệ thống mã hóa và giải mã tệp tin bằng AES-GCM kết hợp dẫn xuất khóa Argon2.

### Chức năng chính

* **CLI (`securecrypto-cli`)**: Mã hóa và giải mã file qua dòng lệnh.


* Mã hóa: `securecrypto-cli --encrypt <file_path> --password <password>`

* Giải mã: `securecrypto-cli --decrypt <file_path.enc> --password <base64_key>`



* **API (Flask)**: Cung cấp 2 endpoint tại `[http://127.0.0.1:5000](http://127.0.0.1:5000)`[cite: 4, 15]:
* `POST /encrypt`: Tải file kèm `password`, trả về khóa Base64.


* `POST /decrypt`: Tải file `.enc` kèm `password` (khóa Base64), trả về file đã giải mã.




* **GUI (`securecrypto/app_gui.py`)**: Giao diện đồ họa hỗ trợ nhập mật khẩu, duyệt file để mã hóa và giải mã trực quan.



---

## 3. Mini CA (Public Key Infrastructure)

Mô phỏng hệ thống thẩm quyền chứng chỉ số (PKI/CA) bằng thuật toán RSA và chuẩn X.509.

### Chức năng chính (Chạy qua `mini-ca/gui.py` hoặc `mini-ca/demo.py`):

1. **Tạo Root & Intermediate CA**: Sinh cặp khóa RSA 2048-bit và chứng chỉ cho Root CA (tự ký) và Intermediate CA.


2. **Phát hành User Cert**: Cấp phát chứng chỉ số cho thực thể cuối (ký bởi Intermediate CA).


3. **Kiểm tra Chuỗi Cert**: Xác thực tính hợp lệ của chuỗi chữ ký số từ User lên CA cấp trên.


4. **Thu hồi User Cert**: Đưa chứng chỉ vào danh sách thu hồi CRL với lý do lộ khóa (`key_compromise`).
5. **Kiểm tra trạng thái (OCSP/CRL)**: Tra cứu danh sách CRL để xác định chứng chỉ còn hiệu lực hay đã bị thu hồi.

---

## 4. Lưu ý khi thực thi

* **Giải mã API**: Trường `file` trong Postman phải được chọn lại tệp thực tế (tránh lỗi tam giác vàng `⚠️`) và chuỗi `password` phải lấy đúng key Base64 được tạo từ lần mã hóa đó để tránh lỗi `InvalidTag` (500).


* **Git Commit**: Sử dụng cờ `--no-verify` (`git commit --no-verify -m "..."`) nếu bị chặn bởi pre-commit hook do có chuỗi mật khẩu trong tệp test.