from __future__ import annotations

import sys
import unittest
from pathlib import Path


BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from nutriok_product import (  # noqa: E402
    BRAND_NAME,
    PARTNER_DISCLOSURE,
    get_product_offer,
    normalize_product_code,
    requires_human_review,
    upgrade_amount_due,
    validate_assessment_payload,
)


class NutriOKProductTests(unittest.TestCase):
    def test_brand_and_pilot_prices_are_canonical(self) -> None:
        self.assertEqual(BRAND_NAME, "НутриОК by Olga Kovaleva")
        self.assertEqual(get_product_offer("ok_express").pilot_price_rub, 990)
        self.assertEqual(get_product_offer("ok_review").pilot_price_rub, 5900)
        self.assertEqual(get_product_offer("ok_result_8").pilot_price_rub, 14900)
        self.assertIn("вознаграждение", PARTNER_DISCLOSURE)

    def test_legacy_codes_map_without_orphaning_cases(self) -> None:
        self.assertEqual(normalize_product_code("osipov"), "ok_review")
        self.assertEqual(normalize_product_code("premium"), "ok_result_8")
        self.assertEqual(normalize_product_code("nutri_chat"), "ok_express")

    def test_review_policy(self) -> None:
        self.assertFalse(requires_human_review("ok_express"))
        self.assertTrue(requires_human_review("ok_review"))
        self.assertTrue(requires_human_review("ok_result_8"))

    def test_upgrade_credit_is_full_within_30_days(self) -> None:
        self.assertEqual(upgrade_amount_due("ok_express", "ok_review", within_days=30), 4910)
        self.assertEqual(upgrade_amount_due("ok_review", "ok_result_8", within_days=30), 9000)
        self.assertEqual(upgrade_amount_due("ok_review", "ok_result_8", within_days=31), 14900)

    def test_paid_assessment_requires_goal_baseline_and_three_day_diary(self) -> None:
        invalid = validate_assessment_payload({"primary_goal": "energy", "baseline_score": 5}, "ok_express")
        self.assertIn("дневник питания за 3 дня", " ".join(invalid))

        valid = validate_assessment_payload(
            {
                "primary_goal": "energy",
                "baseline_score": 5,
                "nutrition_diary": ["день 1", "день 2", "день 3"],
            },
            "ok_express",
        )
        self.assertEqual(valid, [])
