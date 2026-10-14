import unittest

from securevalidator import (
    sanitize_html_input,
    sanitize_sql_input,
    validate_email,
    validate_filename,
    validate_url,
)


class TestSecureValidator(unittest.TestCase):
    def test_validate_email_accepts_valid_email(self):
        self.assertTrue(validate_email("student@example.edu.vn"))

    def test_validate_email_rejects_injection(self):
        self.assertFalse(validate_email("admin@example.com; DROP TABLE users"))
        self.assertFalse(validate_email("attacker@example.com\nBcc: victim@example.com"))

    def test_validate_url_accepts_public_https_url(self):
        self.assertTrue(validate_url("https://example.com/path?q=1"))

    def test_validate_url_rejects_ssrf_targets(self):
        self.assertFalse(validate_url("http://127.0.0.1/admin"))
        self.assertFalse(validate_url("http://localhost:5000"))
        self.assertFalse(validate_url("file:///etc/passwd"))
        self.assertFalse(validate_url("http://169.254.169.254/latest/meta-data"))

    def test_validate_filename_accepts_simple_filename(self):
        self.assertTrue(validate_filename("bao-cao_lab-01.pdf"))

    def test_validate_filename_rejects_path_traversal(self):
        self.assertFalse(validate_filename("../secret.txt"))
        self.assertFalse(validate_filename("..%2fsecret.txt"))
        self.assertFalse(validate_filename("folder/secret.txt"))

    def test_sanitize_sql_input_removes_dangerous_tokens(self):
        cleaned = sanitize_sql_input("' OR 1=1; DROP TABLE users --")
        self.assertNotIn("DROP", cleaned.upper())
        self.assertNotIn("--", cleaned)
        self.assertNotIn(";", cleaned)

    def test_sanitize_html_input_removes_script(self):
        cleaned = sanitize_html_input('<script>alert(1)</script><b>OK</b><img src=x onerror=alert(1)>')
        self.assertNotIn("<script", cleaned.lower())
        self.assertNotIn("onerror", cleaned.lower())
        self.assertIn("OK", cleaned)


if __name__ == "__main__":
    unittest.main()
