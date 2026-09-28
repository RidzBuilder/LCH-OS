"""Offline fixture runner for LCH-OS A-R06.4.

This runner executes declared Python-free fixture facts through the canonical
result evaluator. It does not connect to providers, platforms, cameras, or live
sessions. Run records are deterministic apart from run_id and timestamps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from result_semantics import EvaluationInput, evaluate_result


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_case(case: dict[str, Any], baseline_id: str, source_path: str) -> dict[str, Any]:
    facts = EvaluationInput(
        executed=bool(case.get("executed", False)),
        applicable=bool(case.get("applicable", True)),
        prerequisites_met=bool(case.get("prerequisites_met", False)),
        required_criteria=tuple(case.get("required_criteria", [])),
        forbidden_behavior_observed=bool(case.get("forbidden_behavior_observed", False)),
        required_evidence_sufficient=bool(case.get("required_evidence_sufficient", False)),
        evidence_conflict_material=bool(case.get("evidence_conflict_material", False)),
        not_applicable_basis_approved=bool(case.get("not_applicable_basis_approved", False)),
    )
    status = evaluate_result(facts).value
    return {
        "test_id": case["test_id"],
        "status": status,
        "baseline_id": baseline_id,
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "execution_mode": "OFFLINE_FIXTURE",
        "source_fixture": source_path,
        "evidence_refs": list(case.get("evidence_refs", [])),
        "limitations": [
            "Fixture facts are inputs, not observations of a live system.",
            "This runner does not authenticate external evidence or invoke integrations."
        ],
    }


def run_suite(fixture_path: Path, output_path: Path, baseline_id: str) -> dict[str, Any]:
    raw = fixture_path.read_bytes()
    fixture = json.loads(raw)
    if not isinstance(fixture, dict) or not isinstance(fixture.get("cases"), list):
        raise ValueError("Fixture must be an object containing a cases array.")
    seen: set[str] = set()
    results = []
    for case in fixture["cases"]:
        if not isinstance(case, dict) or not isinstance(case.get("test_id"), str):
            raise ValueError("Every case must be an object with string test_id.")
        if case["test_id"] in seen:
            raise ValueError(f"Duplicate test_id: {case['test_id']}")
        seen.add(case["test_id"])
        results.append(run_case(case, baseline_id, fixture_path.as_posix()))
    counts: dict[str, int] = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    record = {
        "run_id": str(uuid.uuid4()),
        "baseline_id": baseline_id,
        "created_at": utc_now(),
        "execution_mode": "OFFLINE_FIXTURE",
        "fixture": fixture_path.as_posix(),
        "fixture_sha256": hashlib.sha256(raw).hexdigest(),
        "result_count": len(results),
        "status_counts": counts,
        "results": results,
        "limitations": [
            "No live platform/provider execution occurred.",
            "Fixture-run status must not be represented as production conformance."
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--baseline-id", required=True)
    args = parser.parse_args()
    record = run_suite(args.fixture, args.output, args.baseline_id)
    print(json.dumps({
        "run_id": record["run_id"],
        "result_count": record["result_count"],
        "status_counts": record["status_counts"],
        "output": args.output.as_posix(),
        "execution_mode": record["execution_mode"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
