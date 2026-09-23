# Lab2 - Bảo mật trước khi commit

Thư mục này triển khai mục **1.4 THỰC HÀNH: BẢO MẬT TRƯỚC KHI COMMIT** trong `lab-01.pdf`.

Mục tiêu của Lab2 là xây dựng hệ thống pre-commit hook **GitSecure** để tự động kiểm tra mã nguồn trước khi `git commit`, phát hiện rủi ro bảo mật và chặn commit nếu có vấn đề.

## Cấu trúc thư mục

```text
Lab2/
├── .githooks/
│   └── pre-commit
├── examples/
│   ├── safe_sample.py
│   └── unsafe_sample.py.example
├── gitsecure/
│   ├── __init__.py
│   └── scanner.py
├── tests/
│   └── test_gitsecure.py
├── gitsecure_cli.py
├── LICENSE
├── README.md
└── requirements.txt
```

## Chức năng đã triển khai

| Yêu cầu trong PDF | File xử lý | Trạng thái |
|---|---|---|
| Quét thông tin nhạy cảm như API key, password, token | `gitsecure/scanner.py` | Đã có |
| Phát hiện thông tin định danh hardcode | `gitsecure/scanner.py` | Đã có |
| Quét lỗ hổng cơ bản bằng Bandit | `gitsecure/scanner.py` | Đã có |
| Kiểm tra quyền truy cập file | `gitsecure/scanner.py` | Đã có |
| Kiểm tra tuân thủ giấy phép | `gitsecure/scanner.py` + `LICENSE` | Đã có |
| Chặn commit khi phát hiện rủi ro | `.githooks/pre-commit` | Đã có |
| Ghi log chi tiết findings | `gitsecure.log` | Đã có |

## Cài đặt

Mở terminal tại thư mục này:

```powershell
cd "Buoi1\Lab2"
python -m pip install -r requirements.txt
```

## Chạy kiểm thử unit test

```powershell
python -m unittest discover tests
```

Kết quả mong đợi:

```text
....
----------------------------------------------------------------------
Ran 4 tests in ...s

OK
```

Ý nghĩa:

- Scanner phát hiện được secret mẫu.
- Scanner phát hiện được username hardcode.
- Kiểm tra license pass khi có file `LICENSE`.
- Luồng quét an toàn không báo lỗi khi không có rủi ro.

## Chạy GitSecure thủ công

Quét toàn bộ thư mục Lab2:

```powershell
python gitsecure_cli.py --all
```

Bỏ qua Bandit nếu chỉ muốn kiểm tra logic scanner nhanh:

```powershell
python gitsecure_cli.py --all --no-bandit
```

Nếu không phát hiện rủi ro, kết quả sẽ tương tự:

```text
GitSecure: Không phát hiện rủi ro bảo mật.
Kết quả đã ghi vào: ...\gitsecure.log
```

Nếu phát hiện rủi ro, chương trình trả exit code `1`, in danh sách findings và ghi vào `gitsecure.log`.

## Kiểm thử tình huống phát hiện lỗi

File `examples/unsafe_sample.py.example` cố ý chứa API key/password/username mẫu để kiểm thử.

Cách thử:

```powershell
Copy-Item examples\unsafe_sample.py.example examples\unsafe_sample.py
python gitsecure_cli.py --all --no-bandit
Remove-Item examples\unsafe_sample.py
```

Kết quả mong đợi:

```text
GitSecure chặn commit vì phát hiện rủi ro bảo mật:
- [Sensitive Data] examples\unsafe_sample.py:2 Phát hiện API key có nguy cơ bị hardcode
- [Sensitive Data] examples\unsafe_sample.py:3 Phát hiện Password có nguy cơ bị hardcode
- [Hardcoded Identity] examples\unsafe_sample.py:4 Phát hiện thông tin định danh bị cài cứng
```

Ý nghĩa: hook nhận diện dữ liệu nhạy cảm/định danh hardcode và sẽ chặn commit để lập trình viên xử lý trước.

## Kích hoạt pre-commit hook

Từ gốc repository, chạy:

```powershell
git config core.hooksPath "Buoi1/Lab2/.githooks"
```

Sau đó khi chạy:

```powershell
git commit
```

Git sẽ tự gọi `.githooks/pre-commit`. Nếu có findings, commit bị chặn.

## File log

Sau mỗi lần chạy, GitSecure ghi vào:

```text
gitsecure.log
```

Log gồm thời gian UTC, trạng thái `PASS` hoặc `FAIL`, loại kiểm tra và vị trí file/dòng nếu có.

## Thống kê

| Hạng mục | Số lượng |
|---|---:|
| Module scanner | 1 |
| CLI chạy thủ công | 1 |
| Pre-commit hook | 1 |
| Unit test | 4 |
| Nhóm kiểm tra bảo mật | 5 |
| File mẫu an toàn/rủi ro | 2 |

## Ghi chú

- Không commit `gitsecure.log` nếu log chứa thông tin nhạy cảm thật.
- Regex trong lab chỉ phục vụ phát hiện cơ bản. Môi trường thật nên kết hợp thêm GitLeaks, TruffleHog hoặc detect-secrets.
- Bandit chỉ phân tích mã Python; các ngôn ngữ khác cần công cụ SAST tương ứng.

