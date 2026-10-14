"""SecureLogger: ghi log bảo mật dạng JSON, che PII và kiểm tra toàn vẹn."""

from __future__ import annotations

import gzip
import hashlib
import json
import logging
import re
import shutil
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)(?:\d[ .-]?){8,10}\d(?!\d)")
_ID_RE = re.compile(r"\b\d{12}\b")
_CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_TOKEN_RE = re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "context"):
            payload["context"] = getattr(record, "context")
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)


class SecureLogger:
    def __init__(self, log_file: str = "secure.log", max_bytes: int = 1_000_000, backup_count: int = 3):
        self.log_path = Path(log_file)
        self.signature_path = self.log_path.with_suffix(self.log_path.suffix + ".sig")
        self.logger = logging.getLogger(f"securelogger.{self.log_path}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.logger.handlers.clear()

        handler = RotatingFileHandler(self.log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        handler.setFormatter(JsonFormatter())
        handler.rotator = self._compress_rotated_log
        handler.namer = lambda name: f"{name}.gz"
        self.logger.addHandler(handler)
        self.update_signature()

    @staticmethod
    def mask_pii(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: SecureLogger.mask_pii(item) for key, item in value.items()}
        if isinstance(value, list):
            return [SecureLogger.mask_pii(item) for item in value]
        if not isinstance(value, str):
            return value
        masked = _EMAIL_RE.sub("***@***", value)
        masked = _CARD_RE.sub("***CARD***", masked)
        masked = _ID_RE.sub("***ID***", masked)
        masked = _PHONE_RE.sub("***PHONE***", masked)
        masked = _TOKEN_RE.sub(lambda m: f"{m.group(1)}=***SECRET***", masked)
        return masked.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")

    def log(self, level: str, message: str, **context: Any) -> None:
        safe_message = self.mask_pii(message)
        safe_context = self.mask_pii(context)
        level_value = getattr(logging, level.upper(), logging.INFO)
        self.logger.log(level_value, safe_message, extra={"context": safe_context})
        self.update_signature()

    def debug(self, message: str, **context: Any) -> None:
        self.log("DEBUG", message, **context)

    def info(self, message: str, **context: Any) -> None:
        self.log("INFO", message, **context)

    def warning(self, message: str, **context: Any) -> None:
        self.log("WARNING", message, **context)

    def error(self, message: str, **context: Any) -> None:
        self.log("ERROR", message, **context)

    def critical(self, message: str, **context: Any) -> None:
        self.log("CRITICAL", message, **context)

    def log_validation(self, validator: str, raw_input: Any, result: Any) -> None:
        self.info("validation_executed", validator=validator, input=raw_input, result=result)

    def calculate_digest(self) -> str:
        digest = hashlib.sha256()
        if self.log_path.exists():
            with self.log_path.open("rb") as file:
                for chunk in iter(lambda: file.read(8192), b""):
                    digest.update(chunk)
        return digest.hexdigest()

    def update_signature(self) -> str:
        signature = self.calculate_digest()
        self.signature_path.write_text(signature, encoding="utf-8")
        return signature

    def verify_integrity(self) -> bool:
        if not self.signature_path.exists():
            return False
        return self.signature_path.read_text(encoding="utf-8").strip() == self.calculate_digest()

    def close(self) -> None:
        for handler in list(self.logger.handlers):
            handler.close()
            self.logger.removeHandler(handler)

    @staticmethod
    def _compress_rotated_log(source: str, dest: str) -> None:
        with open(source, "rb") as src, gzip.open(dest, "wb") as dst:
            shutil.copyfileobj(src, dst)
        Path(source).unlink(missing_ok=True)

