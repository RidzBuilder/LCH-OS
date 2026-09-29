import unittest

from remediation_engine import generate_remediation


class RemediationEngineTests(unittest.TestCase):
    def test_nonpassing_statuses_generate_open_action(self):
        for status in ("FAIL", "BLOCKED", "NOT_TESTED", "INCONCLUSIVE", "CONTRADICTED", "UNRESOLVED"):
            with self.subTest(status=status):
                result = generate_remediation({"test_id": "T-1", "status": status})
                self.assertIsNotNone(result)
                self.assertEqual(result["status"], "ACTION_REQUIRED")
                self.assertEqual(result["closure_state"], "OPEN")

    def test_pass_and_approved_na_do_not_generate_action(self):
        self.assertIsNone(generate_remediation({"test_id": "T-2", "status": "PASS"}))
        self.assertIsNone(generate_remediation({"test_id": "T-3", "status": "NOT_APPLICABLE"}))

    def test_unknown_status_routes_to_triage(self):
        result = generate_remediation({"test_id": "T-4", "status": "MYSTERY"})
        self.assertEqual(result["action_code"], "MANUAL_TRIAGE_UNKNOWN_STATUS")


if __name__ == "__main__":
    unittest.main()
