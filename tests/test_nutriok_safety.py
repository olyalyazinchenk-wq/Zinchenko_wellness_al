from __future__ import annotations

import sys
import unittest
from pathlib import Path


BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from nutriok_safety import (  # noqa: E402
    RED_FLAG_CLIENT_MESSAGE,
    evaluate_delivery_gate,
    find_high_risk_medications,
    find_red_flags,
    find_unsafe_claims,
    has_pregnancy_supplement_conflict,
    is_underage,
)


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

    def test_expanded_red_flag_regex_word_forms_and_yo_normalization(self) -> None:
        cases = [
            ("Вчера заметила кровь в кале", "blood_in_stool_or_vomit"),
            ("Была рвота с кровью утром", "blood_in_stool_or_vomit"),
            ("Появился чёрный дегтеобразный стул", "black_tarry_stool"),
            ("Резкое похудение на 8 кг за месяц", "rapid_weight_loss"),
            ("Иногда теряю сознание в душном помещении", "syncope"),
            ("Сжимающая боль за грудиной", "chest_pain"),
            ("Сильная одышка в покое вечером", "dyspnea_at_rest"),
            ("Мысли, что не хочу жить", "suicidal_ideation"),
            ("Пью слабительные для похудения и вызываю рвоту", "eating_disorder"),
        ]
        for text, expected_flag in cases:
            with self.subTest(text=text):
                flags = find_red_flags({"symptoms": text})
                self.assertIn(expected_flag, flags)

    def test_high_risk_medications_route_to_awaiting_safety_review(self) -> None:
        med_cases = [
            ("Принимаю варфарин постоянно", "варфарин"),
            ("На инсулине (лантус)", "инсулине"),
            ("Прохожу курс химиотерапии", "химиотерапии"),
            ("Пью сертралин (антидепрессант)", "сертралин"),
        ]
        for med_text, expected_match in med_cases:
            with self.subTest(med_text=med_text):
                sub = {"medications": med_text, "red_flags": "нет"}
                self.assertIn(expected_match, find_high_risk_medications(sub))
                decision = evaluate_delivery_gate("ok_express", "Мягкий режим сна и воды.", sub)
                self.assertFalse(decision.allow_automatic_delivery)
                self.assertEqual(decision.status, "awaiting_safety_review")
                self.assertTrue(
                    any(r.startswith("high_risk_medications:") for r in decision.reasons)
                )

    def test_pregnancy_or_lactation_with_supplements_routes_to_review(self) -> None:
        sub = {
            "symptoms": "Кормлю грудью (на ГВ), хочу подобрать витамин D и магний",
            "medications": "бады для кормящих",
            "red_flags": "нет",
        }
        self.assertTrue(has_pregnancy_supplement_conflict(sub))
        decision = evaluate_delivery_gate("ok_express", "Безопасный рацион питания.", sub)
        self.assertFalse(decision.allow_automatic_delivery)
        self.assertEqual(decision.status, "awaiting_expert_review")
        self.assertIn("pregnancy_or_lactation_supplement_review", decision.reasons)

    def test_underage_is_blocked(self) -> None:
        sub = {"profile": {"age": 16}, "symptoms": "усталость"}
        self.assertTrue(is_underage(sub))
        decision = evaluate_delivery_gate("ok_express", "Безопасный черновик.", sub)
        self.assertFalse(decision.allow_automatic_delivery)
        self.assertEqual(decision.status, "awaiting_safety_review")
        self.assertTrue(any("underage_lt_18" in r for r in decision.reasons))
        self.assertIn("врачу", RED_FLAG_CLIENT_MESSAGE)


if __name__ == "__main__":
    unittest.main()
