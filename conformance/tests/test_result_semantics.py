import unittest

from conformance.result_semantics import EvaluationInput, Status, evaluate_result


class ResultSemanticsTests(unittest.TestCase):
    def test_pass_requires_criteria_and_evidence(self):
        facts = EvaluationInput(True, True, True, (True, True), False, True)
        self.assertEqual(evaluate_result(facts), Status.PASS)

    def test_forbidden_behavior_is_fail(self):
        facts = EvaluationInput(True, True, True, (True,), True, True)
        self.assertEqual(evaluate_result(facts), Status.FAIL)

    def test_missing_prerequisite_is_blocked(self):
        facts = EvaluationInput(True, True, False, (), False, False)
        self.assertEqual(evaluate_result(facts), Status.BLOCKED)

    def test_unexecuted_is_not_tested(self):
        facts = EvaluationInput(False, True, True)
        self.assertEqual(evaluate_result(facts), Status.NOT_TESTED)

    def test_not_applicable_requires_approved_basis(self):
        approved = EvaluationInput(False, False, False, not_applicable_basis_approved=True)
        unapproved = EvaluationInput(False, False, False, not_applicable_basis_approved=False)
        self.assertEqual(evaluate_result(approved), Status.NOT_APPLICABLE)
        self.assertEqual(evaluate_result(unapproved), Status.BLOCKED)

    def test_insufficient_evidence_is_inconclusive(self):
        facts = EvaluationInput(True, True, True, (True,), False, False)
        self.assertEqual(evaluate_result(facts), Status.INCONCLUSIVE)

    def test_conflicting_evidence_is_inconclusive(self):
        facts = EvaluationInput(True, True, True, (True,), False, True, True)
        self.assertEqual(evaluate_result(facts), Status.INCONCLUSIVE)

    def test_empty_criteria_cannot_pass(self):
        facts = EvaluationInput(True, True, True, (), False, True)
        self.assertEqual(evaluate_result(facts), Status.INCONCLUSIVE)


if __name__ == "__main__":
    unittest.main()
