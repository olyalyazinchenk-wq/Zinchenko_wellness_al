from __future__ import annotations

import sys
import unittest
from pathlib import Path


BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from nutriok_safety import evaluate_delivery_gate, find_unsafe_claims  # noqa: E402


class NutriOKSafetyTests(unittest.TestCase):
    def test_safe_express_can_be_delivered_automatically(self) -> None:
        decision = evaluate_delivery_gate(
            "ok_express",
            "Наблюдение: завтрак часто пропущен. Попробуйте добавить регулярный прием пищи.",
            {"symptoms": "усталость", "red_flags": "нет"},
        )
        self.assertTrue(decision.allow_automatic_delivery)

    def test_full_tiers_always_wait_for_olga(self) -> None:
        decision = evaluate_delivery_gate("ok_review", "Безопасный черновик.", {"red_flags": "нет"})
        self.assertFalse(decision.allow_automatic_delivery)
        self.assertEqual(decision.status, "awaiting_expert_review")
        self.assertIn("tier_requires_olga_approval", decision.reasons)

    def test_medical_claim_blocks_express(self) -> None:
        self.assertIn("diagnosis", find_unsafe_claims("У вас анемия, назначаю лечение."))
        decision = evaluate_delivery_gate(
            "ok_express",
            "У вас анемия, назначаю лечение.",
            {"red_flags": "нет"},
        )
        self.assertFalse(decision.allow_automatic_delivery)
        self.assertEqual(decision.status, "awaiting_safety_review")

    def test_red_flag_blocks_express(self) -> None:
        decision = evaluate_delivery_gate(
            "ok_express",
            "Черновик рекомендаций.",
            {"symptoms": "боль в груди и тяжело дышать", "red_flags": "да"},
        )
        self.assertFalse(decision.allow_automatic_delivery)
        self.assertTrue(any(reason.startswith("red_flags:") for reason in decision.reasons))

    def test_supplement_brand_blocks_automatic_delivery(self) -> None:
        decision = evaluate_delivery_gate(
            "ok_express",
            "Можно рассмотреть Vitamax по промокоду.",
            {"red_flags": "нет"},
        )
        self.assertFalse(decision.allow_automatic_delivery)
        self.assertIn("supplement_offer_requires_olga_approval", decision.reasons)
