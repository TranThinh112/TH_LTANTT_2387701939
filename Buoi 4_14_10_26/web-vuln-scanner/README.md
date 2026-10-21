# Web Vulnerability Scanner - Công cụ rà quét lỗ hổng ứng dụng Web

> **Học phần:** Lập trình An toàn Thông tin (LTANTT)  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Bài thực hành:** Buổi 4 - Mục 4.2: Công cụ dò quét lỗ hổng Web (WebVulnScanner)

---

## 1. Giới thiệu tổng quan

Các ứng dụng Web hiện đại thường xuyên đối mặt với các nguy cơ tấn công nằm trong bảng xếp hạng **OWASP Top 10**. **Web Vulnerability Scanner** là bộ công cụ kiểm thử bảo mật tự động hóa được phát triển bằng Python, hỗ trợ các chuyên viên kiểm thử (Penetration Testers) và lập trình viên phát hiện sớm các lỗ hổng nghiêm trọng:
- **Cross-Site Scripting (XSS):** Dò quét lỗ hổng Reflected XSS bằng kỹ thuật tự động tiêm tập payload đa dạng (Script tag, SVG Event Handler) vào các tham số URL.
- **Cross-Site Request Forgery (CSRF):** Phân tích mã nguồn HTML của các biểu mẫu (`<form>`) để phát hiện sự thiếu vắng của Anti-CSRF Tokens.
- **SQL Injection (SQLi):** Kiểm tra khả năng chèn câu lệnh SQL độc hại qua tham số truy vấn bằng các mẫu payload Boolean-based và Error-based.
- **Server-Side Request Forgery (SSRF):** Phát hiện nguy cơ ứng dụng bị lợi dụng để truy vấn các địa chỉ mạng nội bộ (IP Private, Loopback, Cloud Metadata).
- **Hệ thống tạo báo cáo (Report Generator):** Tổng hợp danh sách lỗ hổng, mức độ nghiêm trọng (High, Medium, Low), bằng chứng khai thác (Proof-of-Concept) và gợi ý biện pháp khắc phục.

---

## 2. Cấu trúc thư mục

```text
Buoi 4_14_10_26/web-vuln-scanner/
├── scanners/
│   ├── __init__.py            # Khởi tạo package scanners
│   ├── xss_scanner.py          # Kiểm thử chèn mã độc Cross-Site Scripting (XSS)
│   ├── csrf_detector.py        # Kiểm tra token chống giả mạo yêu cầu (Anti-CSRF)
│   ├── sql_injection_tester.py # Dò quét lỗi tiêm câu lệnh SQL (SQL Injection)
│   └── ssrf_tester.py          # Phát hiện nguy cơ truy cập mạng nội bộ trái phép (SSRF)
├── report/
│   ├── __init__.py            # Khởi tạo package report
│   └── report_generator.py    # Phân loại mức độ rủi ro và xuất báo cáo tổng hợp
├── ui/
│   ├── templates/
│   │   ├── index.html          # Form nhập URL mục tiêu và chọn module quét
│   │   └── result.html         # Bảng hiển thị kết quả kiểm thử trực quan
│   └── app.py                  # Máy chủ Flask chạy Web UI tại http://127.0.0.1:5000/
├── tests/
│   ├── __init__.py
│   ├── test_xss.py             # Unit test cho module XSS
│   ├── test_csrf.py            # Unit test cho module CSRF
│   ├── test_sql_injection.py   # Unit test cho module SQLi
│   ├── test_ssrf.py            # Unit test cho module SSRF
│   └── test_report.py          # Unit test cho module Report
├── images/
│   ├── image1.png              # Hình 1: Kết quả chạy UnitTest tự động
│   ├── image2.png              # Hình 2: Chạy kiểm tra chương trình chính CLI (main.py)
│   ├── image3.png              # Hình 3: Khởi động giao diện Web UI (ui/app.py)
│   └── image4.png              # Hình 4: Báo cáo phát hiện lỗ hổng XSS & CSRF trên Web UI
├── main.py                     # Script thực thi quét mẫu qua giao diện Console
├── requirements.txt            # Danh sách các thư viện phụ thuộc (Flask, requests, beautifulsoup4)
└── README.md                   # Tài liệu hướng dẫn sử dụng (file này)
```

---

## 3. Cài đặt môi trường

Mở PowerShell tại thư mục `web-vuln-scanner`:

```powershell
cd "Buoi 4_14_10_26\web-vuln-scanner"
pip install -r requirements.txt
```

---

## 4. Chạy kiểm thử tự động (Unit Tests)

Kiểm tra toàn bộ các module dò quét và bộ tạo báo cáo với thư viện `unittest`:

```powershell
python -m unittest discover tests
```

![Chạy và kiểm tra unittest](images/image1.png)  
*Hình 1: Chạy và kiểm tra unittest - Toàn bộ 9/9 test cases đều vượt qua thành công (Ran 9 tests ... OK)*

---

## 5. Hướng dẫn sử dụng và Kết quả thực tế (Hình ảnh minh chứng)

### 5.1. Chạy chương trình quét mẫu Console (`main.py`)

Chạy script quét mẫu kiểm tra module SQL Injection và SSRF:

```powershell
python main.py
```

![Chạy kiểm tra chương trình chính](images/image2.png)  
*Hình 2: Chạy kiểm tra chương trình chính (main.py) trên Terminal in kết quả phát hiện lỗ hổng*

---

### 5.2. Chạy giao diện Web UI kiểm thử tương tác (`ui/app.py`)

Khởi động máy chủ web Flask:

```powershell
python ui/app.py
```

![Chạy kiểm tra web UI](images/image3.png)  
*Hình 3: Chạy kiểm tra khởi động web UI trên địa chỉ `http://127.0.0.1:5000/`*

Truy cập trình duyệt web tại `http://127.0.0.1:5000/`, nhập địa chỉ URL cần kiểm tra (ví dụ endpoint phản chiếu `http://127.0.0.1:5000/demo-xss`), lựa chọn các scanner tương ứng và nhấp **Bắt đầu kiểm thử**.

![Kết quả quét lỗ hổng bảo mật trên Web UI](images/image4.png)  
*Hình 4: Kết quả quét lỗ hổng bảo mật Web trên giao diện Web Vulnerability Scanner phát hiện XSS High và CSRF Medium*

---

## 6. Phân tích chi tiết các lỗ hổng phát hiện (Theo Báo cáo)

Tiến hành kiểm thử bảo mật ứng dụng web thông qua công cụ Web Vulnerability Scanner tại giao diện Web UI (`http://127.0.0.1:5000/`). Công cụ thực hiện rà quét đồng thời các module kiểm thử XSS và CSRF đối với endpoint mục tiêu. Kết quả hệ thống đã phát hiện thành công hai nhóm lỗ hổng:

### 6.1. Lỗ hổng Cross-Site Scripting (XSS) - Mức độ: HIGH
- **Cơ chế phát hiện:** Module `XSSScanner` tự động tiêm (inject) các payload XSS chuẩn hóa vào tham số truy vấn `q`. Máy chủ mục tiêu phản chiếu (reflect) trực tiếp nội dung payload về client trong HTTP response mà không qua cơ chế encode/sanitize dữ liệu đầu vào.
- **Các payload khai thác thành công:**
  - **Payload 1:** `<script>alert(1)</script>` — Khai thác thực thi thẻ `<script>` trực tiếp trong DOM.
  - **Payload 2:** `"><svg/onload=alert(1)>` — Kỹ thuật đóng thẻ HTML hiện tại và kích hoạt mã độc qua event handler `onload` của thẻ `<svg>`.
- **Giải pháp khắc phục:** Áp dụng cơ chế Context-aware HTML Entity Encoding (mã hóa các ký tự `<`, `>`, `"`, `'`, `&`) trước khi chèn vào trang HTML; thiết lập chính sách Content Security Policy (CSP) chặt chẽ.

### 6.2. Lỗ hổng Cross-Site Request Forgery (CSRF) - Mức độ: MEDIUM
- **Cơ chế phát hiện:** Module `CSRFDetector` phân tích cấu trúc HTML của form nhưng không tìm thấy bất kỳ anti-CSRF token hợp lệ nào (chẳng hạn như `csrf_token`, `_csrf`, hoặc `csrfmiddlewaretoken`).
- **Kết luận:** Form thao tác có nguy cơ bị tấn công giả mạo yêu cầu từ phía người dùng hợp lệ nếu không có cơ chế xác thực phiên bổ sung.
- **Giải pháp khắc phục:** Sử dụng đồng bộ Anti-CSRF Token dạng Synchronizer Token Pattern hoặc SameSite Cookie attribute (`SameSite=Strict` hoặc `SameSite=Lax`).

---

## 7. Kết luận

Công cụ **Web Vulnerability Scanner** đã mô phỏng chính xác phương thức hoạt động của các hệ thống DAST (Dynamic Application Security Testing), giúp tự động hóa quá trình phát hiện các lỗ hổng bảo mật Web phổ biến và nguy hiểm nhất hiện nay.
