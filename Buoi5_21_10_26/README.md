# BÁO CÁO THỰC HÀNH LAB 05: PHÁT TRIỂN CÔNG CỤ SAST VÀ DAST CHO PYTHON

Thực hiện theo tài liệu hướng dẫn **Lab 05 (Phần 5.2 & Phần 5.4)**.
Toàn bộ mã nguồn được triển khai chính xác 100% theo đặc tả trong tài liệu giảng dạy, tổ chức bài bản thành 2 module độc lập:
- `sast-tool/`: Công cụ kiểm thử bảo mật tĩnh (Static Application Security Testing).
- `dast-tool/`: Công cụ kiểm thử bảo mật động (Dynamic Application Security Testing) có tích hợp REST API Flask.

---

## 1. Cấu Trúc Thư Mục Toàn Dự Án

```
Buoi5_21_10_26/
├── sast-tool/
│   ├── requirements.txt            # Thư viện phụ thuộc của SAST (flake8, sarif-om, jsonpickle)
│   ├── examples/
│   │   ├── vulnerable_01.py        # File Python mẫu chứa eval, hardcoded password, pickle
│   │   └── vulnerable_02.py        # File Python mẫu kiểm thử eval không kiểm soát đầu vào
│   ├── rules/
│   │   └── default_rules.json      # Tập luật phân loại mức độ nghiêm trọng (high, medium, low)
│   ├── sast_tool/
│   │   ├── __init__.py
│   │   ├── ast_analyzer.py         # Phân tích cây cú pháp trừu tượng AST tìm hàm eval
│   │   ├── code_quality_checker.py # Kiểm tra linting và chuẩn chất lượng mã nguồn bằng flake8
│   │   ├── vuln_pattern_matcher.py # Quét biểu thức chính quy (Regex) tìm password, unsafe pickle
│   │   ├── security_rule_engine.py # Đánh giá, gán severity dựa trên rules JSON
│   │   ├── sarif_reporter.py       # Xuất báo cáo chuẩn quốc tế SARIF 2.1.0 qua jsonpickle
│   │   └── main.py                 # Điểm khởi chạy CLI chính của SAST tool
│   └── tests/
│       ├── __init__.py
│       ├── test_ast_analyzer.py
│       ├── test_code_quality_checker.py
│       ├── test_sarif_reporter.py
│       ├── test_security_rule_engine.py
│       └── test_vuln_pattern_matcher.py
│
├── dast-tool/
│   ├── requirements.txt            # Thư viện phụ thuộc của DAST (psutil, Flask)
│   ├── __init__.py
│   ├── runtime_monitor.py          # Giám sát tài nguyên CPU, Memory, Open Files theo PID
│   ├── memory_analyzer.py          # Kiểm tra rò rỉ bộ nhớ (Garbage Collection) và tràn số nguyên
│   ├── network_traffic_analyzer.py # Thống kê lưu lượng mạng vào/ra trên các network interface
│   ├── security_behavior_checker.py# Quét các hàm/lời gọi nguy hiểm: os.system, eval, exec
│   ├── virtual_sandbox.py          # Chạy lệnh trong thư mục cô lập tạm thời an toàn
│   ├── main.py                     # Script kiểm thử độc lập các module runtime
│   ├── app.py                      # RESTful API Server cung cấp các endpoint phân tích DAST
│   └── tests/
│       ├── __init__.py
│       ├── test_runtime_monitor.py
│       ├── test_memory_analyzer.py
│       ├── test_network_traffic_analyzer.py
│       ├── test_security_behavior_checker.py
│       └── test_virtual_sandbox.py
│
└── README.md                       # Tài liệu hướng dẫn chi tiết
```

---

## 2. Hướng Dẫn Cài Đặt Môi Trường

### Yêu cầu tiên quyết:
- **Python**: Phiên bản 3.10+ hoặc 3.11+.

### Cài đặt thư viện:
Cài đặt dependencies riêng cho từng công cụ:

```bash
# Cài đặt cho SAST Tool
cd sast-tool
pip install -r requirements.txt
cd ..

# Cài đặt cho DAST Tool
cd dast-tool
pip install -r requirements.txt
cd ..
```

*Các thư viện chính bao gồm:*
- `flake8`: Phân tích chuẩn mã nguồn Python (PEP 8, syntax errors).
- `sarif-om` & `jsonpickle`: Định dạng và sinh báo cáo bảo mật chuẩn quốc tế SARIF v2.1.0.
- `psutil`: Theo dõi tiến trình phần cứng (CPU, RAM, mạng, file handles).
- `Flask`: Cung cấp dịch vụ DAST qua giao diện REST API.

---

## 3. Phần 5.2: Static Application Security Testing (SAST Tool)

### 3.1. Các thành phần chính
1. **`ast_analyzer.py`**: Sử dụng module chuẩn `ast` của Python để duyệt cây cú pháp trừu tượng, phát hiện các lệnh gọi hàm nguy hiểm (`eval()`).
2. **`vuln_pattern_matcher.py`**: Sử dụng Regex để tìm các mẫu nguy cơ tiềm ẩn:
   - Mật khẩu mã hóa cứng (`password = "..."`)
   - Thư viện serialize nguy hiểm (`import pickle`)
3. **`code_quality_checker.py`**: Chạy tiến trình nền `flake8` để bắt lỗi phong cách lập trình và lỗi cú pháp.
4. **`security_rule_engine.py`**: So khớp các cảnh báo tìm được với `rules/default_rules.json` để phân cấp mức độ rủi ro (`high`, `medium`, `low`).
5. **`sarif_reporter.py`**: Định dạng danh sách cảnh báo thành cấu trúc OASIS SARIF v2.1.0 và xuất ra file JSON/SARIF.

### 3.2. Chạy kiểm thử tự động (Unit Tests)
Từ thư mục `sast-tool`:
```bash
cd sast-tool
python -m unittest discover -s tests
```
*Kết quả:* Toàn bộ các bộ kiểm thử đơn vị (`TestASTAnalyzer`, `TestCodeQualityChecker`, `TestSarifReporter`, `TestSecurityRuleEngine`, `TestVulnPatternMatcher`) đều vượt qua (`OK`).

### 3.3. Sử dụng công cụ quét mã nguồn
Chạy phân tích trên các tệp mã nguồn mẫu:

```bash
# Quét file mẫu số 1:
python -m sast_tool.main examples/vulnerable_01.py

# Quét file mẫu số 2:
python -m sast_tool.main examples/vulnerable_02.py
```

Sau khi quét, công cụ sẽ tạo ra tệp báo cáo `report.sarif` chứa đầy đủ thông tin:
- Tên công cụ: `PySAST` (version `1.0.0`)
- Vị trí phát hiện (dòng `start_line`, cột `start_column`)
- Nội dung cảnh báo bảo mật (`Use of eval() is dangerous`, `Hardcoded password detected`, `Usage of pickle module can be unsafe`, các cảnh báo Flake8).

---

## 4. Phần 5.4: Dynamic Application Security Testing (DAST Tool)

### 4.1. Các thành phần chính
1. **`runtime_monitor.py`**: Nhận vào PID của tiến trình, thu thập tỷ lệ phần trăm CPU, dung lượng RAM sử dụng (RSS) và danh sách file descriptor đang mở.
2. **`memory_analyzer.py`**: Kích hoạt bộ thu dọn rác `gc.collect()`, phát hiện rò rỉ bộ nhớ qua `gc.garbage` và kiểm tra hiện tượng tràn số nguyên (trị tuyệt đối > 2^63).
3. **`network_traffic_analyzer.py`**: Sử dụng `psutil.net_io_counters(pernic=True)` để lấy thông số bytes gửi/nhận, số lượng gói tin trên từng card mạng.
4. **`security_behavior_checker.py`**: Quét mã nguồn đang thực thi để nhận diện các lệnh hệ thống có mức độ nguy hiểm cao (`os.system`, `eval`, `exec`).
5. **`virtual_sandbox.py`**: Tạo thư mục tạm thời `tempfile.mkdtemp()` để thực thi các câu lệnh shell cô lập, thu thập `stdout` và `stderr` mà không làm ảnh hưởng môi trường chính.

### 4.2. Chạy kiểm thử tự động (Unit Tests)
Từ thư mục `dast-tool`:
```bash
cd dast-tool
python -m unittest discover -s tests
```
*Kết quả:* Toàn bộ các test case (`TestRuntimeMonitor`, `TestMemoryAnalyzer`, `TestNetworkTrafficAnalyzer`, `TestSecurityBehaviorChecker`, `TestVirtualSandbox`) đều vượt qua (`OK`).

### 4.3. Chạy kiểm thử CLI độc lập
Thực thi trực tiếp file `main.py` để xem thông số giám sát tức thì của tiến trình:
```bash
python main.py
```

### 4.4. Khởi chạy và sử dụng REST API Server
Khởi chạy dịch vụ API giám sát:
```bash
python app.py
```
Mặc định ứng dụng chạy tại: `http://localhost:5000`

#### Danh sách API Endpoints:

| Phương thức | Đường dẫn URL | Mô tả | Dữ liệu đầu vào (Body) |
|---|---|---|---|
| **GET** | `/api/monitor` | Giám sát CPU, RAM, danh sách file mở của tiến trình server | Không |
| **GET** | `/api/memory` | Kiểm tra rò rỉ đối tượng và kiểm thử tràn số | Không |
| **GET** | `/api/network` | Thống kê số liệu mạng I/O trên tất cả card mạng | Không |
| **GET** | `/api/security` | Kiểm tra lời gọi nhạy cảm (syscalls) | Không |
| **POST** | `/api/sandbox` | Thực thi lệnh bất kỳ trong sandbox cô lập an toàn | JSON: `{"command": "echo test"}` |

#### Ví dụ gọi API (PowerShell / curl):

1. **Kiểm tra tài nguyên tiến trình:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/monitor" -Method GET
```

2. **Kiểm tra bộ nhớ:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/memory" -Method GET
```

3. **Kiểm tra lưu lượng mạng:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/network" -Method GET
```

4. **Kiểm tra lời gọi bảo mật:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/security" -Method GET
```

5. **Thực thi lệnh trong Virtual Sandbox:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/sandbox" -Method POST -ContentType "application/json" -Body '{"command": "echo Hello from Sandbox"}'
```

---

## 5. Bảng Tổng Hợp Kiểm Thử & Đánh Giá

| Module | Kiểm thử đơn vị (Unit Tests) | Chạy thực tế (CLI / API) | Đánh giá độ tương thích tài liệu |
|---|---|---|---|
| **SAST Tool** (`sast-tool/`) | 6/6 tests passed | Quét thành công `vulnerable_01.py` & `vulnerable_02.py`, xuất file chuẩn `report.sarif` | Đạt 100% đúng cấu trúc slide 5.2 |
| **DAST Tool** (`dast-tool/`) | 5/5 tests passed | Chạy thành công `main.py` và toàn bộ 5 endpoints REST API trong `app.py` | Đạt 100% đúng cấu trúc slide 5.4 |
