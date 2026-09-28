"""Deterministic conformance result semantics for LCH-OS A-R06.3.

This module evaluates a single test's supplied execution facts. It does not execute
the system under test and cannot independently establish evidence authenticity.
"""
from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_TESTED = "NOT_TESTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class EvaluationInput:
    executed: bool
    applicable: bool
    prerequisites_met: bool
    required_criteria: tuple[bool, ...] = ()
    forbidden_behavior_observed: bool = False
    required_evidence_sufficient: bool = False
    evidence_conflict_material: bool = False
    not_applicable_basis_approved: bool = False


def evaluate_result(facts: EvaluationInput) -> Status:
    """Apply pinned A-R04 decision rules to an individual test.

    Evidence sufficiency is an input from an evidence verifier; this function does
    not itself verify evidence.
    """
    if not facts.applicable:
        return Status.NOT_APPLICABLE if facts.not_applicable_basis_approved else Status.BLOCKED
    if not facts.executed:
        return Status.NOT_TESTED
    if not facts.prerequisites_met:
        return Status.BLOCKED
    if facts.forbidden_behavior_observed:
        return Status.FAIL
    if facts.evidence_conflict_material:
        return Status.INCONCLUSIVE
    if not facts.required_evidence_sufficient:
        return Status.INCONCLUSIVE
    if not facts.required_criteria:
        return Status.INCONCLUSIVE
    if not all(facts.required_criteria):
        return Status.FAIL
    return Status.PASS
