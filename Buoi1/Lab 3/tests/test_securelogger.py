import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from securelogger import SecureLogger
from securevalidator import validate_email


class TestSecureLogger(unittest.TestCase):
    def setUp(self):
        self.log_path = Path(f"test_secure_{self._testMethodName}.log")
        self.sig_path = Path(f"test_secure_{self._testMethodName}.log.sig")
        self.logger = None
        self.log_path.unlink(missing_ok=True)
        self.sig_path.unlink(missing_ok=True)

    def tearDown(self):
        if self.logger is not None:
            self.logger.close()
        self.log_path.unlink(missing_ok=True)
        self.sig_path.unlink(missing_ok=True)

    def test_masks_pii_in_json_log(self):
        self.logger = SecureLogger(str(self.log_path))
        self.logger.info("user email nguyen@example.com phone 0912345678", cccd="012345678901")
        content = self.log_path.read_text(encoding="utf-8")
        payload = json.loads(content)
        self.assertEqual(payload["level"], "INFO")
        self.assertIn("***@***", content)
        self.assertIn("***PHONE***", content)
        self.assertIn("***ID***", content)
        self.assertNotIn("nguyen@example.com", content)

    def test_detects_tampering(self):
        self.logger = SecureLogger(str(self.log_path))
        self.logger.warning("normal event")
        self.assertTrue(self.logger.verify_integrity())
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write("tampered")
        self.assertFalse(self.logger.verify_integrity())

    def test_logs_validator_result(self):
        self.logger = SecureLogger(str(self.log_path))
        result = validate_email("student@example.edu.vn")
        self.logger.log_validation("email", "student@example.edu.vn", result)
        content = self.log_path.read_text(encoding="utf-8")
        self.assertIn("validation_executed", content)
        self.assertIn("***@***", content)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
