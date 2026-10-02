import json
import unittest
from pathlib import Path


class CoverageDeclarationTests(unittest.TestCase):
    def test_a_r03_coverage_declaration_contains_all_contract_ids(self):
        path = Path(__file__).parents[1] / "fixtures" / "coverage-declaration.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["scenarios"]), 24)
        self.assertEqual(len(data["invariants"]), 18)
        self.assertEqual(
            {item["id"] for item in data["scenarios"]},
            {f"S-{i:02d}" for i in range(1, 25)},
        )
        self.assertEqual(
            {item["id"] for item in data["invariants"]},
            {f"INV-{i:02d}" for i in range(1, 19)},
        )
        self.assertTrue(
            all(item["coverage_status"] == "NOT_TESTED" for item in data["scenarios"])
        )
        self.assertTrue(
            all(item["coverage_status"] == "NOT_TESTED" for item in data["invariants"])
        )


if __name__ == "__main__":
    unittest.main()
