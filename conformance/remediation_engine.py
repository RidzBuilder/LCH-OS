"""Deterministic remediation recommendations for LCH-OS A-R06.6.

Recommendations are generated from a conformance result record. They are not
proof that remediation was executed or that a finding is closed.
"""
from typing import Any

REMEDIATION_BY_STATUS = {
    "FAIL": (
        "REMEDIATE_FAILED_CRITERIA",
        "Inspect failed criteria and forbidden-behavior evidence; correct the "
        "implementation or configuration, then rerun the affected test.",
    ),
    "BLOCKED": (
        "RESOLVE_PREREQUISITES",
        "Resolve the listed prerequisite, authorization, environment, or "
        "dependency blockers; preserve blocker evidence and rerun.",
    ),
    "NOT_TESTED": (
        "SCHEDULE_REQUIRED_TEST",
        "Execute the applicable test in an authorized, controlled environment "
        "and capture required evidence.",
    ),
    "INCONCLUSIVE": (
        "RESOLVE_EVIDENCE_OR_CRITERIA_GAP",
        "Resolve evidence insufficiency, material conflicts, or missing "
        "acceptance criteria before making a conformance determination.",
    ),
    "CONTRADICTED": (
        "INVESTIGATE_EVIDENCE_CONTRADICTION",
        "Preserve the conflicting artifacts, investigate integrity/provenance, "
        "and obtain independently verifiable evidence.",
    ),
    "UNRESOLVED": (
        "RECOVER_OR_LOCATE_EVIDENCE",
        "Locate the missing artifact or rerun the controlled test to produce "
        "the required evidence.",
    ),
}


def generate_remediation(result: dict[str, Any]) -> dict[str, Any] | None:
    status = result.get("status")
    if status in ("PASS", "NOT_APPLICABLE"):
        return None
    if status not in REMEDIATION_BY_STATUS:
        return {
            "remediation_id": "REM-" + str(result.get("test_id", "UNKNOWN")),
            "source_test_id": result.get("test_id"),
            "status": "BLOCKED",
            "action_code": "MANUAL_TRIAGE_UNKNOWN_STATUS",
            "recommended_action": (
                "Validate the result status against the canonical registry "
                "before proceeding."
            ),
            "closure_state": "OPEN",
        }
    code, action = REMEDIATION_BY_STATUS[status]
    return {
        "remediation_id": "REM-" + str(result.get("test_id", "UNKNOWN")),
        "source_test_id": result.get("test_id"),
        "source_status": status,
        "status": "ACTION_REQUIRED",
        "action_code": code,
        "recommended_action": action,
        "evidence_refs": list(result.get("evidence_refs", [])),
        "closure_state": "OPEN",
        "closure_requires": [
            "remediation evidence",
            "re-execution or justified disposition",
            "authorized review",
        ],
        "note": (
            "Generated recommendation only; no remediation execution or "
            "closure is implied."
        ),
    }
