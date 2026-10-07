# SecureChat & NetRecon

## Chức năng hệ thống

### 🔐 SecureChat
- Chat Client/Server qua kết nối **SSL/TLS**.
- Xác thực Client/Server bằng **Certificate**.
- Mã hóa tin nhắn bằng **AES-256**.
- Hỗ trợ nhiều Client kết nối và trao đổi tin nhắn.
- Quản lý kết nối và phòng chat.

### 🔎 NetRecon
- **Port Scanning**: kiểm tra port đang mở.
- **Service Detection**: phát hiện dịch vụ và phiên bản.
- **Banner Grabbing**: thu thập thông tin banner.
- **Network Mapping**: thu thập thông tin mạng.
- **Vulnerability Check**: kiểm tra một số lỗ hổng cơ bản.
- Hỗ trợ **CLI và Web Interface**.
- Hỗ trợ **Rate Limiting** và lọc Whitelist/Blacklist.
- Gửi kết quả quét qua **Email**.

## Công nghệ

- Python
- OpenSSL / SSL-TLS
- AES-256
- Socket
- Nmap
- Flask
- Git/GitHub