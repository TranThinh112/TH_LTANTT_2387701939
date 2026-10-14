import importlib.machinery
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

HOOK_PATH = Path(__file__).resolve().parents[1] / ".githooks" / "pre-commit"


def load_hook():
    loader = importlib.machinery.SourceFileLoader("gitsecure_hook", str(HOOK_PATH))
    spec = importlib.util.spec_from_loader("gitsecure_hook", loader)
    module = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    try:
        loader.exec_module(module)
    finally:
        os.chdir(cwd)
    return module


hook = load_hook()


class TestGitSecure(unittest.TestCase):
    def test_scan_sensitive_detects_hardcoded_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write('sec' + 'ret = "' + 'A1b2C3d4' + '"\n')
            self.assertIsNotNone(hook.scan_sensitive(path))

    def test_scan_sensitive_ignores_clean_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "clean.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write("value = 1\n")
            self.assertIsNone(hook.scan_sensitive(path))

    def test_scan_identity_detects_hardcoded_credential(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "settings.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write('user' + 'name = "admin_' + 'user"\n')
            self.assertIsNotNone(hook.scan_identity(path))

    def test_check_license_passes_when_license_exists(self):
        cwd = os.getcwd()
        os.chdir(HOOK_PATH.parents[1])
        try:
            self.assertIsNone(hook.check_license())
        finally:
            os.chdir(cwd)

    def test_check_license_reports_missing_license(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                self.assertIsNotNone(hook.check_license())
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
