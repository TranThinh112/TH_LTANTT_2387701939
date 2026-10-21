# NetRecon - Bộ công cụ trinh sát mạng và cảnh báo lỗ hổng tự động

> **Học phần:** Lập trình An toàn Thông tin (LTANTT)  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Bài thực hành:** Buổi 3 - Mục 3.4: Công cụ trinh sát mạng NetRecon

---

## 1. Giới thiệu tổng quan

Trong chu trình kiểm thử xâm nhập (Penetration Testing) và quản trị an toàn mạng, giai đoạn **Trinh sát (Reconnaissance)** là bước đầu tiên và quan trọng nhất nhằm thu thập thông tin về bề mặt tấn công (Attack Surface).

**NetRecon** là hệ thống trinh sát mạng tự động hóa toàn diện được xây dựng bằng Python, kết hợp sức mạnh của công cụ tiêu chuẩn công nghiệp **Nmap** và kiến trúc lập trình bất đồng bộ (`asyncio`):
- **Port Scanning:** Quét nhanh các cổng mở TCP thông qua socket bất đồng bộ tốc độ cao.
- **Service Detection & Banner Grabbing:** Nhận diện loại dịch vụ (HTTP, SSH, FTP, SMTP, ...) và bóc tách chuỗi Banner để xác định phiên bản chính xác của phần mềm.
- **Network Mapping (Nmap Integration):** Tích hợp công cụ quét Nmap quét sâu thông tin hệ điều hành (OS Fingerprinting) và phân tích topo mạng.
- **Vulnerability Checker:** Tự động tra cứu cảnh báo lỗ hổng bảo mật (CVE) dựa trên phiên bản dịch vụ phát hiện.
- **Tự động gửi cảnh báo qua Email (SMTP Alert):** Gửi báo cáo kết quả quét định dạng HTML chi tiết về hộp thư quản trị viên qua giao thức SMTP (hỗ trợ Google App Password).
- **Hỗ trợ 2 giao diện:** Dòng lệnh tiện lợi (`cli.py`) và Giao diện Web trực quan (`app.py`).

---

## 2. Cấu trúc thư mục

```text
Buoi3_7_10_26/netrecon/
├── modules/
│   ├── __init__.py            # Khởi tạo package modules
│   ├── port_scanner.py        # Module quét cổng TCP bất đồng bộ bằng asyncio
│   ├── service_detector.py    # Module phân tích nhận diện dịch vụ
│   ├── banner_grabber.py      # Module thu thập chuỗi Banner dịch vụ
│   ├── network_mapper.py      # Module điều khiển Nmap và bóc tách kết quả XML/Text
│   ├── vuln_checker.py        # Module đối soát và cảnh báo lỗ hổng bảo mật (CVE)
│   ├── email_sender.py        # Module soạn và gửi email cảnh báo tự động qua SMTP
│   └── filter_utils.py        # Module kiểm soát tần suất quét (Rate Limit) và IP Whitelist/Blacklist
├── static/
│   └── style.css              # Giao diện CSS hiện đại cho Web UI
├── templates/
│   ├── layout.html            # Khung giao diện HTML cơ sở
│   ├── index.html             # Trang chủ thiết lập tham số quét (Target, Ports, Email)
│   └── result.html            # Bảng hiển thị kết quả phân tích sau khi quét
├── images/
│   ├── image5.png             # Hình 5: Kiểm tra cài đặt Nmap trên Terminal
│   ├── image6.png             # Hình 6: Thiết lập mật khẩu ứng dụng Gmail (SMTP_PASS)
│   ├── image7.png             # Hình 7: Cài đặt gói phụ thuộc requirements.txt
│   ├── image8.png             # Hình 8: Kiểm tra trợ giúp lệnh cli.py
│   ├── image9.png             # Hình 9: Thực hiện lệnh quét mẫu với cli.py
│   ├── image10.png            # Hình 10: Khởi động máy chủ Flask app.py
│   ├── image11.png            # Hình 11: Giao diện Web UI tại http://localhost:5000/
│   ├── image12.png            # Hình 11 (sau scan): Bảng kết quả quét chi tiết trên Web UI
│   └── image13.png            # Hình 12: Email báo cáo nhận được từ hệ thống
├── app.py                     # Máy chủ Flask Web UI cho công cụ NetRecon
├── cli.py                     # Điểm vào công cụ dòng lệnh (Click CLI)
├── netrecon.log               # Nhật ký ghi nhận các phiên quét mạng
├── requirements.txt           # Danh sách các thư viện Python phụ thuộc
└── README.md                  # Tài liệu hướng dẫn sử dụng (file này)
```

---

## 3. Cài đặt và cấu hình hệ thống

### 3.1. Kiểm tra môi trường Nmap

Đảm bảo công cụ Nmap đã được cài đặt trong biến môi trường hệ thống:

```powershell
nmap --version
```

![Kiểm tra Nmap](images/image5.png)  
*Hình 5: Kiểm tra xem Nmap đã được cài đặt hay chưa trong Terminal*

### 3.2. Cấu hình xác thực SMTP Email (Google App Password)

Để hệ thống gửi email cảnh báo bảo mật tự động, tạo mật khẩu ứng dụng (App Password) trong tài khoản Google để thiết lập biến môi trường `SMTP_PASS`:

![Tạo Google App Password](images/image6.png)  
*Hình 6: Tạo app để lấy STMP_PASS trong cài đặt bảo mật tài khoản Google*

### 3.3. Cài đặt các thư viện phụ thuộc

Mở PowerShell tại thư mục `Buoi3_7_10_26\netrecon`:

```powershell
pip install -r requirements.txt
```

![Cài đặt requirements](images/image7.png)  
*Hình 7: Cài các gói cần thiết: `pip install -r requirements.txt`*

---

## 4. Kiểm thử và vận hành NetRecon

### 4.1. Sử dụng qua giao diện dòng lệnh (CLI - `cli.py`)

Kiểm tra cú pháp và danh sách tham số hỗ trợ:

```powershell
python cli.py --help
```

![Kiểm tra cli.py](images/image8.png)  
*Hình 8: Chạy kiểm tra các tùy chọn lệnh của cli.py*

Thực hiện quét nhanh mục tiêu (ví dụ: `127.0.0.1` hoặc IP chỉ định):

```powershell
python cli.py --target 127.0.0.1 --ports 22,80,443,8443
```

![Test nhanh cli.py](images/image9.png)  
*Hình 9: Test nhanh cli.py kiểm tra các cổng mở và dịch vụ phản hồi*

---

### 4.2. Sử dụng qua giao diện Web UI trực quan (`app.py`)

Khởi động máy chủ Flask:

```powershell
python app.py
```

![Khởi động app.py](images/image10.png)  
*Hình 10: Kiểm tra khởi động thành công máy chủ web Flask `app.py`*

Mở trình duyệt web truy cập địa chỉ:
```text
http://localhost:5000/
```

![Giao diện Web UI](images/image11.png)  
*Hình 11: Giao diện trang web NetRecon khi truy cập http://localhost:5000/*

Người dùng điền địa chỉ mục tiêu (Target IP/Domain), dải cổng cần kiểm tra (Ports), nhập địa chỉ Email nhận cảnh báo và nhấp chọn **Scan**.

Sau khi hệ thống hoàn tất phân tích, giao diện chuyển sang trang báo cáo kết quả:

![Bảng kết quả quét](images/image12.png)  
*Hình 11 (sau scan): Phản hồi chi tiết sau khi bấm "Scan" hiển thị danh sách cổng mở, dịch vụ, banner và đánh giá lỗ hổng*

Đồng thời, hệ thống tự động định dạng và gửi một email báo cáo bảo mật đầy đủ đến hộp thư quản trị viên:

![Email cảnh báo](images/image13.png)  
*Hình 12: Email phản hồi từ hệ thống thông báo kết quả quét mạng và các cảnh báo an ninh*

---

## 5. Kết luận

NetRecon cung cấp giải pháp trinh sát mạng toàn diện, hiệu năng cao và tự động hóa:
- **Tốc độ:** Tận dụng xử lý socket bất đồng bộ cho phép quét hàng ngàn cổng trong thời gian ngắn.
- **Độ chính xác cao:** Kết hợp Nmap engine bóc tách thông tin dịch vụ chi tiết.
- **Khả năng phản ứng sự cố nhanh:** Tự động gửi email cảnh báo thời gian thực giúp quản trị viên kịp thời khắc phục các cổng và dịch vụ nguy hiểm đang lộ lọt ra môi trường mạng.
