import json
import tempfile
import unittest
from pathlib import Path

from conformance.runner import run_suite


class RunnerTests(unittest.TestCase):
    def test_fixture_run_emits_results_and_remediation_actions(self):
        fixture = {
            "suite_id": "TEST-SUITE",
            "cases": [
                {
                    "test_id": "T-PASS",
                    "executed": True,
                    "applicable": True,
                    "prerequisites_met": True,
                    "required_criteria": [True],
                    "required_evidence_sufficient": True,
                },
                {
                    "test_id": "T-FAIL",
                    "executed": True,
                    "applicable": True,
                    "prerequisites_met": True,
                    "required_criteria": [False],
                    "required_evidence_sufficient": True,
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "fixture.json"
            output_path = root / "run.json"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")
            record = run_suite(fixture_path, output_path, "TEST-BASELINE")
            self.assertEqual(record["result_count"], 2)
            self.assertEqual(record["status_counts"]["PASS"], 1)
            self.assertEqual(record["status_counts"]["FAIL"], 1)
            self.assertEqual(len(record["remediation_actions"]), 1)
            self.assertEqual(
                record["remediation_actions"][0]["action_code"],
                "REMEDIATE_FAILED_CRITERIA",
            )
            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
