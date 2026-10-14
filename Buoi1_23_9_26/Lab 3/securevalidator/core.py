"""SecureValidator: các hàm xác thực và làm sạch dữ liệu đầu vào."""

from __future__ import annotations

import html
import ipaddress
import posixpath
import re
from urllib.parse import unquote, urlparse

try:
    import bleach
except ImportError:  # pragma: no cover
    bleach = None

_EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
_INJECTION_RE = re.compile(
    r"(--|;|/\*|\*/|\b(select|insert|update|delete|drop|union|exec|script|onerror|onload)\b)",
    re.IGNORECASE,
)
_SAFE_FILENAME_RE = re.compile(r"^[A-Za-z0-9._ -]+$")
_SQL_DANGEROUS_RE = re.compile(
    r"(--|#|/\*|\*/|;|\b(drop|truncate|alter|exec|execute|union|sleep|benchmark)\b)",
    re.IGNORECASE,
)
_SCRIPT_BLOCK_RE = re.compile(r"<\s*(script|style)[^>]*>.*?<\s*/\s*\1\s*>", re.IGNORECASE | re.DOTALL)
_HTML_TAG_RE = re.compile(r"<[^>]*>")
_PRIVATE_HOSTS = {"localhost", "localhost.localdomain"}
_ALLOWED_HTML_TAGS = ["b", "strong", "i", "em", "u", "p", "br", "ul", "ol", "li", "a", "code", "pre"]
_ALLOWED_HTML_ATTRS = {"a": ["href", "title", "rel"]}


def _has_control_chars(value: str) -> bool:
    return any(ord(char) < 32 or ord(char) == 127 for char in value)


def validate_email(email: str) -> bool:
    """Kiểm tra email hợp lệ và chặn các mẫu injection phổ biến."""
    if not isinstance(email, str):
        return False
    email = email.strip()
    if not email or len(email) > 254 or _has_control_chars(email):
        return False
    if _INJECTION_RE.search(email):
        return False
    if not _EMAIL_RE.fullmatch(email):
        return False
    local, domain = email.rsplit("@", 1)
    if len(local) > 64:
        return False
    return all(0 < len(label) <= 63 and not label.startswith("-") and not label.endswith("-") for label in domain.split("."))


def _is_public_hostname(hostname: str) -> bool:
    host = hostname.strip().lower().rstrip(".")
    if not host or host in _PRIVATE_HOSTS:
        return False
    try:
        ip = ipaddress.ip_address(host)
        return not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )
    except ValueError:
        return bool(re.fullmatch(r"[a-z0-9.-]+", host)) and "." in host


def validate_url(url: str) -> bool:
    """Kiểm tra URL HTTP/HTTPS và giảm rủi ro SSRF cơ bản."""
    if not isinstance(url, str):
        return False
    url = url.strip()
    if not url or len(url) > 2048 or _has_control_chars(url):
        return False
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    if parsed.username or parsed.password:
        return False
    if not parsed.hostname or not _is_public_hostname(parsed.hostname):
        return False
    if parsed.port is not None and parsed.port not in {80, 443, 8080, 8443}:
        return False
    return True


def validate_filename(filename: str) -> bool:
    """Chặn path traversal và chỉ cho phép tên file tương đối an toàn."""
    if not isinstance(filename, str):
        return False
    name = unquote(filename).strip()
    if not name or len(name) > 255 or _has_control_chars(name):
        return False
    normalized = posixpath.normpath(name.replace("\\", "/"))
    if normalized.startswith("../") or normalized == ".." or normalized.startswith("/"):
        return False
    if "/" in normalized or "\\" in normalized:
        return False
    if normalized in {".", ".."}:
        return False
    return bool(_SAFE_FILENAME_RE.fullmatch(normalized))


def sanitize_sql_input(input_str: str) -> str:
    """Làm sạch chuỗi đầu vào trước khi hiển thị/lưu tạm; truy vấn SQL vẫn nên dùng tham số hóa."""
    if not isinstance(input_str, str):
        return ""
    cleaned = input_str.replace("\x00", "")
    cleaned = _SQL_DANGEROUS_RE.sub("", cleaned)
    cleaned = cleaned.replace("'", "''").replace('"', '""')
    return cleaned.strip()


def sanitize_html_input(html_str: str) -> str:
    """Làm sạch HTML để giảm nguy cơ XSS."""
    if not isinstance(html_str, str):
        return ""
    if bleach is not None:
        return bleach.clean(
            html_str,
            tags=_ALLOWED_HTML_TAGS,
            attributes=_ALLOWED_HTML_ATTRS,
            protocols=["http", "https", "mailto"],
            strip=True,
        )
    without_scripts = _SCRIPT_BLOCK_RE.sub("", html_str)
    without_tags = _HTML_TAG_RE.sub("", without_scripts)
    return html.escape(without_tags, quote=True)


