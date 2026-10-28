# THỰC HÀNH LẬP TRÌNH AN TOÀN THÔNG TIN (LTANTT)

> **Kho lưu trữ mã nguồn và báo cáo thực hành môn Lập trình An toàn Thông tin**  
> **Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
> **MSSV:** 2387701939  
> **Trường Đại học Công nghệ TP.HCM (HUTECH)**  

---

## 📌 Tổng quan mục lục các buổi thực hành

Hệ thống kho lưu trữ tổng hợp các bài thực hành chuyên sâu từ lập trình bảo mật mã nguồn, mật mã học ứng dụng, bảo mật mạng, đến an toàn ứng dụng Web, API và DevSecOps / CI-CD:

| Buổi học | Chủ đề trọng tâm | Các công cụ / Module triển khai | Tài liệu chi tiết |
|---|---|---|---|
| **Buổi 1** | **An toàn mã nguồn & Dữ liệu đầu vào** | - **Lab 1:** SecureValidator (Xác thực & làm sạch dữ liệu)<br>- **Lab 2:** GitSecure (Pre-commit Hook quét secrets)<br>- **Lab 3:** SecureLogger (Ghi log bảo mật, che PII & chống sửa) | [Buoi1_23_9_26/README.md](Buoi1_23_9_26/README.md) |
| **Buổi 2** | **Mật mã ứng dụng & PKI** | - **SecureCrypto Toolkit:** Mã hóa file AES-GCM, Argon2, RSA, Flask API & GUI<br>- **Mini CA:** Hạ tầng khóa công khai X.509, Root CA, Intermediate CA, CRL | [Buoi2_30_9_26/Readme.md](Buoi2_30_9_26/Readme.md) |
| **Buổi 3** | **Bảo mật mạng & Trinh sát hệ thống** | - **SecureChat:** Chat client-server mã hóa mTLS & AES-256<br>- **NetRecon:** Quét cổng bất đồng bộ, Nmap, Banner Grabbing & Email Alert | [Buoi3_7_10_26/README.md](Buoi3_7_10_26/README.md) |
| **Buổi 4** | **Bảo mật Web App & API** | - **WebVulnScanner:** Dò quét lỗ hổng Web DAST (XSS, CSRF, SQLi, SSRF)<br>- **JWT Security Tools:** Xác thực API Gateway với JWT Token & OAuth 2.0 | [Buoi 4_14_10_26/README.md](Buoi%204_14_10_26/README.md) |
| **Buổi 5** | **Kiểm thử bảo mật SAST & DAST** | - **SAST Tool:** Phân tích AST tĩnh, Regex rule, PEP8 Linting, xuất báo cáo chuẩn SARIF 2.1.0<br>- **DAST Tool:** Giám sát tiến trình, phát hiện rò rỉ bộ nhớ, Network & RESTful API | [Buoi5_21_10_26/README.md](Buoi5_21_10_26/README.md) |
| **Buổi 6** | **DevSecOps & CI/CD Pipeline** | - **GitLab CI/CD Pipeline:** Tự động hóa build, test, deploy với `.gitlab-ci.yml`<br>- **GitLab Pages & Docusaurus:** Triển khai tự động tài liệu tĩnh lên GitLab Pages | [Buoi6_28_10_26/README.md](Buoi6_28_10_26/README.md) |

---

## 📂 Danh mục chi tiết các công cụ (Tools)

### 1. Buổi 1: An toàn mã nguồn và Dữ liệu đầu vào
- **[Lab 1 - SecureValidator](Buoi1_23_9_26/Lab%201/README.md):** Thư viện Python độc lập xác thực email, URL (chống SSRF), tên file (chống Path Traversal), làm sạch SQL Injection và XSS. Đi kèm giao diện Web UI Flask.
- **[Lab 2 - GitSecure](Buoi1_23_9_26/Lab2/README.md):** Git Pre-Commit Hook tự động quét phát hiện secret, API keys, chuỗi định danh PII và quét lỗi tĩnh Bandit trước khi commit. Chặn commit vi phạm an toàn.
- **[Lab 3 - SecureLogger](Buoi1_23_9_26/Lab%203/README.md):** Hệ thống ghi nhật ký chuẩn cấu trúc JSON Lines, tự động che giấu PII (email, CCCD, sđt), luân phiên nén file log và phát hiện can thiệp giả mạo (Tamper Detection) bằng chữ ký mật mã SHA-256.

### 2. Buổi 2: Mật mã ứng dụng và Hạ tầng khóa công khai
- **[SecureCrypto Toolkit](Buoi2_30_9_26/crypto-toolkit/README.md):** Giải pháp mã hóa tệp tin với AES-256-GCM và Argon2id KDF. Hỗ trợ 3 giao diện: CLI (`cli.py`), Tkinter Desktop GUI (`app_gui.py`), và Flask RESTful API (`api.py`) kiểm thử qua Postman.
- **[Mini CA (Public Key Infrastructure)](Buoi2_30_9_26/mini-ca/README.md):** Hệ thống nhà thẩm quyền chứng chỉ số chuẩn X.509 v3 với kiến trúc 2 cấp (Root CA, Intermediate CA), cấp phát chứng chỉ End-Entity, xác thực chuỗi tin cậy và thu hồi chứng chỉ vào danh sách CRL (`key_compromise`).

### 3. Buổi 3: Bảo mật mạng máy tính
- **[SecureChat](Buoi3_7_10_26/secure-chat/README.md):** Ứng dụng trao đổi tin nhắn mạng Client/Server bảo vệ bởi cơ chế xác thực chứng chỉ song phương Mutual TLS (mTLS) và mã hóa nội dung tin nhắn bổ sung với AES-256.
- **[NetRecon](Buoi3_7_10_26/netrecon/README.md):** Bộ công cụ trinh sát mạng tự động kết hợp Nmap engine, quét cổng bất đồng bộ `asyncio`, nhận diện banner dịch vụ, đối soát cơ sở dữ liệu lỗ hổng bảo mật (CVE) và tự động gửi email cảnh báo qua giao thức SMTP.

### 4. Buổi 4: Bảo mật ứng dụng Web và API
- **[Web Vulnerability Scanner](Buoi%204_14_10_26/web-vuln-scanner/README.md):** Bộ quét lỗ hổng động (DAST) kiểm thử tự động XSS (Reflected XSS với các payload SVG/Script), CSRF (kiểm tra Anti-CSRF Token trong form HTML), SQL Injection và SSRF qua giao diện Web UI.
- **[JWT Security Tools](Buoi%204_14_10_26/jwt-security-tools/README.md):** Nền tảng xác thực API Gateway bảo vệ tài nguyên nhạy cảm bằng Bearer Token JWT HMAC-SHA256 (`HS256`), phân tách Access Token / Refresh Token và kiểm thử ủy quyền OAuth 2.0.

### 5. Buổi 5: Kiểm thử bảo mật mã nguồn (SAST) & Động (DAST)
- **[SAST Tool](Buoi5_21_10_26/sast-tool/README.md):** Công cụ phân tích cú pháp tĩnh Abstract Syntax Tree (AST), Regex matching phát hiện Hardcoded Secret, SQLi, Command Injection, kiểm tra chất lượng mã PEP8 và xuất kết quả chuẩn quốc tế SARIF 2.1.0 tương thích GitHub Security.
- **[DAST Tool](Buoi5_21_10_26/dast-tool/README.md):** Công cụ giám sát hành vi động và sandbox tiến trình, phát hiện rò rỉ tài nguyên bộ nhớ/CPU, bắt gói tin socket/network và cung cấp RESTful API tự động hóa kiểm thử.

### 6. Buổi 6: DevSecOps và Tự động hóa CI/CD với GitLab
- **[GitLab CI/CD Pipeline & Pages](Buoi6_28_10_26/README.md):** 
  - Xây dựng quy trình tích hợp và phân phối liên tục (CI/CD) nhiều giai đoạn (`build`, `test`, `deploy`) qua tệp `.gitlab-ci.yml`.
  - Đóng gói và phát hành ứng dụng web tĩnh Docusaurus tự động qua GitLab Runner lên **GitLab Pages**.
  - Demo trực tiếp: [https://truongthinh-2387701939-fa3ba8.gitlab.io/](https://truongthinh-2387701939-fa3ba8.gitlab.io/)

---

## 🛠️ Yêu cầu môi trường chung

- **Hệ điều hành:** Windows 10/11, Linux hoặc macOS
- **Ngôn ngữ:** Python 3.10+, Node.js 18+
- **Công cụ phụ trợ:**
  - `git`: Quản lý phiên bản mã nguồn
  - `openssl`: Tạo khóa và chứng chỉ X.509
  - `nmap`: Rà quét dịch vụ mạng
  - `GitLab CI/CD`: GitLab Shared Runner & Pages
- **Thư viện chính:** `cryptography`, `flask`, `argon2-cffi`, `requests`, `pytest`, `pyjwt`, `click`, `beautifulsoup4`, `flake8`, `sarif-om`, `@docusaurus/core`.
