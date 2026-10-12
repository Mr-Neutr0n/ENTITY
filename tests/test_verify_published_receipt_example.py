import pathlib
import subprocess
import sys
import unittest


REPO = pathlib.Path(__file__).resolve().parents[1]
TOOL = REPO / "examples" / "verify_published_receipt.py"
VALID = REPO / "examples" / "fixtures" / "independent_node_receipt_valid.json"
TAMPERED = REPO / "examples" / "fixtures" / "independent_node_receipt_tampered.json"


class VerifyPublishedReceiptExampleTests(unittest.TestCase):
    def test_valid_fixture_exits_zero(self):
        run = subprocess.run(
            [sys.executable, str(TOOL), str(VALID)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr or run.stdout)
        self.assertIn("file_sha256=", run.stdout)
        self.assertIn("PASS:", run.stdout)

    def test_tampered_fixture_exits_nonzero(self):
        run = subprocess.run(
            [sys.executable, str(TOOL), str(TAMPERED)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("receipt_sha256", run.stderr)


if __name__ == "__main__":
    unittest.main()
