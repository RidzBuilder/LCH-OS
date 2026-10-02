import hashlib
import tempfile
import unittest
from pathlib import Path

from conformance.evidence_verifier import verify_file


class EvidenceVerifierTests(unittest.TestCase):
    def test_matching_digest_is_only_partially_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.txt"
            path.write_text("evidence", encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            result = verify_file(path, digest)
            self.assertEqual(result["status"], "PARTIALLY_VERIFIED")
            self.assertEqual(result["verification_scope"], "BYTE_INTEGRITY_ONLY")

    def test_mismatched_digest_is_contradicted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.txt"
            path.write_text("evidence", encoding="utf-8")
            result = verify_file(path, "0" * 64)
            self.assertEqual(result["status"], "CONTRADICTED")
            self.assertEqual(result["reason"], "SHA256_MISMATCH")

    def test_missing_artifact_is_unresolved(self):
        result = verify_file(Path("/definitely/missing/artifact"))
        self.assertEqual(result["status"], "UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
