"""Structural SHA-256 evidence integrity checks for A-R06.5.

A matching digest establishes byte integrity relative to a supplied expected
digest; it does not establish authorship, time, or truth of external events.
"""
from pathlib import Path
from typing import Any
import hashlib


def verify_file(path: Path, expected_sha256: str | None = None) -> dict[str, Any]:
    if not path.is_file():
        return {"status": "UNRESOLVED", "reason": "ARTIFACT_NOT_FOUND", "path": str(path)}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected_sha256 is None:
        status, reason = "PARTIALLY_VERIFIED", "DIGEST_COMPUTED_NO_TRUSTED_EXPECTED_DIGEST"
    elif digest.lower() == expected_sha256.lower():
        status, reason = "PARTIALLY_VERIFIED", "DIGEST_MATCH_ONLY_PROVENANCE_NOT_AUTHENTICATED"
    else:
        status, reason = "CONTRADICTED", "SHA256_MISMATCH"
    return {"status": status, "reason": reason, "path": str(path), "sha256": digest,
            "expected_sha256": expected_sha256, "verification_scope": "BYTE_INTEGRITY_ONLY"}
