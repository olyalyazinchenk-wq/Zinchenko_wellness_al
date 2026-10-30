from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
OPS_DIR = PROJECT_ROOT / "ops"
for p in (BOT_DIR, OPS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from nutriok_benchmark import (  # noqa: E402
    ensure_benchmark_fixtures,
    evaluate_case_rubric,
)
from nutriok_product import PRIMARY_GOALS  # noqa: E402


class BenchmarkFixturesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures_dir = PROJECT_ROOT / "tests" / "fixtures" / "nutriok_cases"
        ensure_benchmark_fixtures(cls.fixtures_dir)

    def test_twenty_cases_cover_five_goals_times_four_profiles(self) -> None:
        files = sorted(self.fixtures_dir.glob("case_*.json"))
        self.assertEqual(len(files), 20)

        goals_seen: set[str] = set()
        profiles_seen: set[str] = set()
        pairs_seen: set[tuple[str, str]] = set()

        for path in files:
            fx = json.loads(path.read_text(encoding="utf-8"))
            goal = fx["goal"]
            profile_type = fx["profile_type"]
            goals_seen.add(goal)
            profiles_seen.add(profile_type)
            pairs_seen.add((goal, profile_type))

            with self.subTest(case_id=fx["case_id"]):
                res = evaluate_case_rubric(fx, fx["reference_draft"])
                self.assertTrue(res["gate_match"], f"Gate mismatch for {fx['case_id']}: {res}")
                self.assertEqual(res["critical_defects"], [])
                self.assertGreaterEqual(res["scores"]["average"], 4.0)

        self.assertEqual(goals_seen, set(PRIMARY_GOALS.keys()))
        self.assertEqual(
            profiles_seen,
            {"normal", "comorbid_meds", "red_flag", "supplement_pregnancy"},
        )
        self.assertEqual(len(pairs_seen), 20)

    def test_rubric_detects_unsafe_claims_and_missing_blocks(self) -> None:
        case_01 = json.loads((self.fixtures_dir / "case_01.json").read_text(encoding="utf-8"))
        bad_draft = "У вас диагноз анемия. Назначаю лечение, отмените препарат."
        res = evaluate_case_rubric(case_01, bad_draft)
        self.assertFalse(res["gate_match"])
        self.assertGreater(len(res["critical_defects"]), 0)
        self.assertEqual(res["scores"]["safety"], 1.0)


if __name__ == "__main__":
    unittest.main()
