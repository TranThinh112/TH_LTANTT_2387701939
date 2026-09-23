import tempfile
import unittest
from pathlib import Path

from gitsecure.scanner import (
    check_license,
    run_security_checks,
    scan_hardcoded_identity,
    scan_sensitive_data,
)


class TestGitSecure(unittest.TestCase):
    def test_scan_sensitive_data_detects_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample = root / "config.py"
            secret = "abcd1234" * 3
            sample.write_text(f'API_KEY = "{secret}"\n', encoding="utf-8")
            findings = scan_sensitive_data(root, [sample])
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].check, "Sensitive Data")

    def test_scan_hardcoded_identity_detects_username(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample = root / "settings.py"
            identity = "admin" + "_user"
            key = "user" + "name"
            sample.write_text(f'{key} = "{identity}"\n', encoding="utf-8")
            findings = scan_hardcoded_identity(root, [sample])
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].check, "Hardcoded Identity")

    def test_check_license_passes_when_license_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "LICENSE").write_text("MIT", encoding="utf-8")
            self.assertEqual(check_license(root), [])

    def test_run_security_checks_can_skip_bandit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "LICENSE").write_text("MIT", encoding="utf-8")
            (root / "safe.py").write_text('print("safe")\n', encoding="utf-8")
            findings = run_security_checks(root, staged_only=False, include_bandit=False)
            self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()


