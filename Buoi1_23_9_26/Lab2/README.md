# Lab2 - Bảo mật trước khi commit (GitSecure)

Thư mục này triển khai mục **1.4 THỰC HÀNH: BẢO MẬT TRƯỚC KHI COMMIT** trong `lab-01.pdf`.

Mục tiêu: xây dựng pre-commit hook **GitSecure** để tự động kiểm tra mã nguồn trước khi `git commit`, phát hiện rủi ro bảo mật và **chặn commit** nếu có vấn đề.

Cách tổ chức giống giáo trình: toàn bộ logic nằm trong **một file duy nhất** `.githooks/pre-commit`, không tách module.

## Cấu trúc thư mục

```text
Lab2/
├── .githooks/
│   └── pre-commit
├── examples/
│   ├── safe_sample.py
│   └── unsafe_sample.py.example
├── tests/
│   └── test_gitsecure.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Đối chiếu yêu cầu 1.4.1

| Yêu cầu trong PDF | Hàm trong `.githooks/pre-commit` |
|---|---|
| Quét API key, password, token hardcode | `scan_sensitive()` + `SENSITIVE_PATTERNS` |
| Phát hiện thông tin định danh cài cứng | `scan_identity()` + `IDENTITY_PATTERNS` |
| Quét lỗ hổng bằng Bandit | `scan_bandit()` |
| Kiểm tra quyền truy cập file | `check_permissions()` |
| Kiểm tra tuân thủ giấy phép | `check_license()` |
| Chặn commit khi có rủi ro | `main()` trả về mã `1` |
| Ghi log findings | `log()` → `gitsecure.log` |

## Cài đặt

```powershell
cd "C:\Users\Admin\Documents\TH_LTANTT_2387701939\Buoi1\Lab2"
python -m pip install -r requirements.txt
```

## Chạy kiểm thử unit test

```powershell
python -m unittest discover tests
```

Kết quả:

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.041s

OK
```

Ý nghĩa: hook import được, hàm quét secret hoạt động, hàm quét định danh hoạt động, kiểm tra license đúng cả hai chiều (có file và thiếu file).

## Chạy hook thủ công

```powershell
python .githooks\pre-commit
```

Khi dữ liệu sạch:

```text
GitSecure: Không phát hiện rủi ro bảo mật.
Kết quả đã ghi vào: ...\Lab2\gitsecure.log
```

Mã thoát là `0`, nghĩa là commit được phép đi tiếp.

## Kiểm thử trường hợp bị chặn

Tạo file chứa dữ liệu rủi ro từ file mẫu:

```powershell
copy examples\unsafe_sample.py.example examples\unsafe_sample.py
python .githooks\pre-commit
del examples\unsafe_sample.py
```

Kết quả:

```text
GitSecure chặn commit vì phát hiện rủi ro bảo mật:
- Sensitive info found in .\examples\unsafe_sample.py: pattern ...
- Hardcoded identity found in .\examples\unsafe_sample.py: pattern ...
- Bandit found security issues. Run: python -m bandit -r .
Chi tiết đã ghi vào: ...\Lab2\gitsecure.log
```

Mã thoát là `1`, nghĩa là commit **bị chặn**.

## Kích hoạt hook cho Git

Chạy từ gốc repository:

```powershell
cd "C:\Users\Admin\Documents\TH_LTANTT_2387701939"
git config core.hooksPath "Buoi1/Lab2/.githooks"
```

Kiểm tra lại:

```powershell
git config core.hooksPath
```

Từ đó mỗi lần `git commit`, GitSecure chạy tự động.

## File log

Mọi lần chạy đều ghi vào `gitsecure.log`, gồm thời gian, trạng thái `PASS`/`FAIL` và chi tiết từng phát hiện.

## Thống kê

| Hạng mục | Số lượng |
|---|---:|
| File thực thi hook | 1 |
| Nhóm kiểm tra bảo mật | 5 |
| Unit test | 5 |
| Danh sách file bỏ qua | 2 |
| File mẫu | 2 |

## Ghi chú và giới hạn

- Hook bỏ qua file `.example`, file log, thư mục `.git`, `__pycache__`, `.venv`, `venv`.
- Trên Windows, `check_permissions()` dùng `icacls` để phát hiện quyền ghi cho `Everyone`. Trên Linux/macOS dùng `stat` để phát hiện bit world-writable và group-writable.
- Regex nhận diện secret là mẫu cơ bản, phục vụ mục đích học tập. Môi trường thật nên dùng thêm GitLeaks, TruffleHog hoặc detect-secrets.
- Bandit chỉ phân tích mã Python.
- Không commit file `gitsecure.log` vì log có thể chứa thông tin nhạy cảm.
