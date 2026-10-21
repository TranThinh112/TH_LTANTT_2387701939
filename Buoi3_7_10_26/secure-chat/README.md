# SecureChat - Hệ thống phòng chat bảo mật đa người dùng (SSL/TLS & AES-256)

> **Học phần:** Lập trình An toàn Thông tin (LTANTT)  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Bài thực hành:** Buổi 3 - Mục 3.2: Hệ thống SecureChat bảo mật mạng

---

## 1. Giới thiệu tổng quan

Trong các hệ thống truyền thông mạng truyền thống qua socket (TCP/IP), dữ liệu được truyền đi dưới dạng văn bản rõ (cleartext), tạo điều kiện cho các cuộc tấn công nghe lén (Sniffing), bắt gói tin (Man-in-the-Middle - MitM) và giả mạo danh tính (Impersonation).

**SecureChat** được thiết kế để giải quyết triệt để các nguy cơ trên bằng cách xây dựng một kiến trúc bảo mật đa lớp (Defense-in-Depth):
1. **Mã hóa kênh truyền bảo mật (Transport Layer Security - SSL/TLS):** Toàn bộ lưu lượng mạng giữa Client và Server được bọc trong kênh TLS với cổng bảo mật mặc định `8443`.
2. **Xác thực song phương (Mutual TLS - mTLS):** Cả Server và Client đều phải xuất trình chứng chỉ số X.509 hợp lệ được cấp bởi cùng một Root CA tin cậy. Nếu chứng chỉ không hợp lệ, kết nối sẽ bị hủy bỏ ngay tại bước bắt tay (TLS Handshake).
3. **Mã hóa nội dung tin nhắn (Application-Level Encryption - AES-256):** Tin nhắn trao đổi được mã hóa đối xứng AES-256 trước khi gửi qua socket, đảm bảo bí mật tuyệt đối kể cả trong trường hợp kênh TLS bị giám sát proxy.
4. **Quản lý đa phòng chat (Multi-room Support):** Phân chia người dùng vào các phòng chat riêng biệt thông qua `RoomManager` và `ConnectionManager`.

---

## 2. Cấu trúc thư mục

```text
Buoi3_7_10_26/secure-chat/
├── certs/                     # Thư mục lưu trữ chứng chỉ OpenSSL (tạo từ make-certs.bat)
│   ├── ca/                    # Khóa riêng và chứng chỉ Root CA (ca.key, ca.crt)
│   ├── server/                # Khóa và chứng chỉ máy chủ (server.key, server.crt)
│   └── client/                # Khóa và chứng chỉ máy trạm (client.key, client.crt)
├── images/
│   ├── image1.png             # Hình 1: Kiểm tra tệp cấu hình openssl.cnf
│   ├── image2.png             # Hình 2: Sinh bộ chứng chỉ bằng make-certs.bat
│   ├── image3.png             # Hình 3: Cấu trúc thư mục certs sau khi sinh
│   └── image4.png             # Hình 4: Phiên chat mã hóa thực tế giữa Client và Server
├── openssl.cnf                # Tệp cấu hình tham số OpenSSL
├── make-certs.bat             # Kịch bản Batch tự động tạo toàn bộ chứng chỉ X.509
├── connection_manager.py      # Quản lý socket kết nối và trạng thái trực tuyến
├── room_manager.py            # Quản lý định tuyến tin nhắn theo từng phòng chat
├── message_encryption.py      # Module mã hóa đối xứng AES-256 cho tin nhắn
├── server.py                  # Máy chủ đa luồng SecureChat lắng nghe tại 127.0.0.1:8443
├── client.py                  # Máy trạm SecureChat kết nối mTLS
└── README.md                  # Tài liệu hướng dẫn sử dụng (file này)
```

---

## 3. Khởi tạo hạ tầng chứng chỉ số (OpenSSL PKI)

### 3.1. Kiểm tra cấu hình OpenSSL (`openssl.cnf`)

Tệp `openssl.cnf` định nghĩa các thông số kỹ thuật cho CA, phần mở rộng X.509 v3, và Subject Alternative Name (SAN).

![Kiểm tra cấu hình Openssl](images/image1.png)  
*Hình 1: Kiểm tra cấu hình Openssl trong tệp `openssl.cnf`*

### 3.2. Chạy kịch bản tự động sinh chứng chỉ (`make-certs.bat`)

Chạy script batch để khởi tạo toàn bộ chứng chỉ và khóa RSA:

```cmd
make-certs.bat
```

![Tạo chứng chỉ OpenSSL](images/image2.png)  
*Hình 2: Tạo thành công chứng chỉ CA, Server và Client bằng OpenSSL*

### 3.3. Kiểm tra các tệp tin chứng chỉ đã tạo

Sau khi script hoàn thành, hệ thống tạo ra cấu trúc cây chứng chỉ hoàn chỉnh trong thư mục `certs/`:

![Thư mục certs](images/image3.png)  
*Hình 3: Các thư mục và chứng chỉ đã được tạo đầy đủ trong `certs/ca`, `certs/server`, `certs/client`*

---

## 4. Hướng dẫn vận hành hệ thống SecureChat

### 4.1. Khởi động máy chủ SecureChat Server

Mở Terminal thứ nhất và chạy:

```powershell
python server.py
```

*Máy chủ sẽ nạp `server.crt`, `server.key` và chứng chỉ `ca.crt`, thiết lập SSL Context yêu cầu xác thực Client (`CERT_REQUIRED`) và bắt đầu lắng nghe tại `127.0.0.1:8443`.*

### 4.2. Khởi động Client tham gia phòng chat

Mở Terminal thứ hai (và thứ ba để mô phỏng 2 người chat):

```powershell
python client.py
```

Client kết nối mTLS tới server, xác thực chứng chỉ máy chủ và gửi chứng chỉ client để máy chủ xác thực. Sau khi bắt tay TLS thành công, người dùng nhập tên hiển thị và bắt đầu gửi tin nhắn được mã hóa qua lại.

![Chạy SecureChat thực tế](images/image4.png)  
*Hình 4: Chạy thành công SecureChat, các client kết nối đến server và trao đổi tin nhắn được mã hóa an toàn*

---

## 5. Kết luận

Hệ thống SecureChat chứng minh tính hiệu quả của mô hình bảo mật Socket nâng cao:
- **Ngăn chặn triệt để nghe lén (Eavesdropping):** Kênh TLS mã hóa toàn bộ dữ liệu ở tầng mạng.
- **Xác thực định danh 2 chiều (Mutual Authentication):** Chỉ các client có chứng chỉ hợp lệ do CA ký mới được phép kết nối vào máy chủ nội bộ.
- **Toàn vẹn và an mật đa tầng:** Mã hóa kép (TLS + AES-256) bảo vệ tin nhắn ngay cả khi vượt qua các lớp proxy kiểm định.
