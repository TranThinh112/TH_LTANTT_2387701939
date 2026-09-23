from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gitsecure.scanner import run_security_checks, write_log


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="GitSecure - kiểm tra bảo mật trước khi commit")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ project thay vì chỉ file staged")
    parser.add_argument("--no-bandit", action="store_true", help="Bỏ qua Bandit")
    parser.add_argument("--root", default=".", help="Thư mục gốc cần quét")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = run_security_checks(root, staged_only=not args.all, include_bandit=not args.no_bandit)
    log_path = write_log(root, findings)

    if findings:
        print("GitSecure chặn commit vì phát hiện rủi ro bảo mật:")
        for finding in findings:
            print(f"- {finding.format()}")
        print(f"Chi tiết đã ghi vào: {log_path}")
        return 1

    print("GitSecure: Không phát hiện rủi ro bảo mật.")
    print(f"Kết quả đã ghi vào: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
