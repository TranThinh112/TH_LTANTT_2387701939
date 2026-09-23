from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SECRET_PATTERNS = [
    ("API key", re.compile(r"(?i)\b(api[_-]?key|secret[_-]?key)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("Password", re.compile(r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
    ("Token", re.compile(r"(?i)\b(token|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*['\"][A-Za-z0-9_\-.]{20,}['\"]")),
    ("Private key", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]
LICENSE_FILES = {"LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "NOTICE"}
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".7z", ".exe", ".dll", ".example"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules"}


@dataclass(frozen=True)
class SecurityFinding:
    check: str
    message: str
    file: str | None = None
    line: int | None = None

    def format(self) -> str:
        location = ""
        if self.file:
            location = self.file
            if self.line:
                location += f":{self.line}"
            location = f" {location}"
        return f"[{self.check}]{location} {self.message}"


def iter_project_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def get_staged_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return list(iter_project_files(root))
    return [root / line.strip() for line in result.stdout.splitlines() if line.strip()]


def scan_sensitive_data(root: Path, files: Iterable[Path]) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for path in files:
        if not path.exists() or path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text[: match.start()].count("\n") + 1
                findings.append(SecurityFinding("Sensitive Data", f"Phát hiện {label} có nguy cơ bị hardcode", str(path.relative_to(root)), line))
    return findings


def scan_hardcoded_identity(root: Path, files: Iterable[Path]) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    identity_pattern = re.compile(r"(?i)\b(username|user|client_id|tenant_id)\b\s*[:=]\s*['\"][^'\"]{4,}['\"]")
    for path in files:
        if not path.exists() or path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in identity_pattern.finditer(text):
            line = text[: match.start()].count("\n") + 1
            findings.append(SecurityFinding("Hardcoded Identity", "Phát hiện thông tin định danh bị cài cứng", str(path.relative_to(root)), line))
    return findings


def run_bandit(root: Path) -> list[SecurityFinding]:
    result = subprocess.run(
        [sys.executable, "-m", "bandit", "-q", "-r", "."],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    if "No module named bandit" in result.stderr:
        return [SecurityFinding("Bandit", "Chưa cài bandit. Chạy: pip install -r requirements.txt")]
    return [SecurityFinding("Bandit", "Bandit phát hiện vấn đề bảo mật. Chạy python -m bandit -r . để xem chi tiết")]


def check_file_permissions(root: Path, files: Iterable[Path]) -> list[SecurityFinding]:
    if os.name == "nt":
        return []
    findings: list[SecurityFinding] = []
    for path in files:
        if not path.exists():
            continue
        mode = path.stat().st_mode
        if mode & stat.S_IWOTH:
            findings.append(SecurityFinding("File Permission", "File cho phép mọi người ghi", str(path.relative_to(root))))
    return findings


def check_license(root: Path) -> list[SecurityFinding]:
    if any((root / name).exists() for name in LICENSE_FILES):
        return []
    return [SecurityFinding("License", "Chưa có file LICENSE/COPYING/NOTICE để kiểm tra tuân thủ giấy phép")]


def write_log(root: Path, findings: list[SecurityFinding], log_name: str = "gitsecure.log") -> Path:
    log_path = root / log_name
    timestamp = datetime.now(timezone.utc).isoformat()
    with log_path.open("a", encoding="utf-8") as file:
        if not findings:
            file.write(f"{timestamp} PASS Không phát hiện rủi ro bảo mật\n")
        for finding in findings:
            file.write(f"{timestamp} FAIL {finding.format()}\n")
    return log_path


def run_security_checks(root: Path, staged_only: bool = True, include_bandit: bool = True) -> list[SecurityFinding]:
    files = get_staged_files(root) if staged_only else list(iter_project_files(root))
    findings: list[SecurityFinding] = []
    findings.extend(scan_sensitive_data(root, files))
    findings.extend(scan_hardcoded_identity(root, files))
    findings.extend(check_file_permissions(root, files))
    findings.extend(check_license(root))
    if include_bandit:
        findings.extend(run_bandit(root))
    return findings

