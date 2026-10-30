from __future__ import annotations

import sys
import unittest
from pathlib import Path


BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from intake_schema import (  # noqa: E402
    GOAL_DEFAULT_METRICS,
    AdherenceEntry,
    DiaryDay,
    NutriOKIntake,
)


class IntakeSchemaTests(unittest.TestCase):
    def test_diary_day_and_adherence_entry_roundtrip(self) -> None:
        day = DiaryDay(
            day_index=2,
            meals_text="Завтрак: овсянка и яйца; обед: суп.",
            photo_file_ids=["ph_1", "ph_2"],
            water_ml=1600,
            wellbeing_0_10=7,
        )
        restored_day = DiaryDay.from_dict(day.to_dict())
        self.assertEqual(restored_day, day)

        adherence = AdherenceEntry(week=1, adherence_pct=85, metric_value=6.5, note="Лучше после обеда")
        restored_adherence = AdherenceEntry.from_dict(adherence.to_dict())
        self.assertEqual(restored_adherence, adherence)

    def test_nutriok_intake_roundtrip_preserves_all_fields(self) -> None:
        intake = NutriOKIntake(
            schema_version=1,
            product_code="ok_review",
            primary_goal="energy",
            baseline_score=4,
            goal_metric=GOAL_DEFAULT_METRICS["energy"],
            nutrition_diary=[
                DiaryDay(day_index=1, meals_text="День 1"),
                DiaryDay(day_index=2, meals_text="День 2", photo_file_ids=["f2"]),
                DiaryDay(day_index=3, meals_text="День 3"),
            ],
            symptoms="усталость в 15:00",
            medications="витамин D 2000 МЕ",
            allergies="арахис",
            lifestyle="сидячая работа, сон 6 часов",
            labs_upload_ids=["lab_pdf_1"],
            adherence=[AdherenceEntry(week=1, adherence_pct=80, metric_value=6.0)],
            adult_confirmed=True,
            pd_consent_at="2026-10-30T10:00:00Z",
        )
        payload = intake.to_dict()
        restored = NutriOKIntake.from_dict(payload)
        self.assertEqual(restored, intake)
        self.assertEqual(restored.validation_errors(), [])

    def test_goal_default_metrics_match_contract_table(self) -> None:
        self.assertEqual(GOAL_DEFAULT_METRICS["energy"], "энергия в 15:00, 0–10")
        self.assertEqual(GOAL_DEFAULT_METRICS["digestion"], "вздутие после еды, 0–10")
        self.assertIn("тяга к сладкому, 0–10", GOAL_DEFAULT_METRICS["weight_appetite"])
        self.assertIn("состояние кожи, 0–10", GOAL_DEFAULT_METRICS["skin_hair"])
        self.assertEqual(GOAL_DEFAULT_METRICS["sleep_stress"], "качество сна, 0–10")

    def test_ok_start_validation_requires_consent_adult_goal_and_baseline_without_diary(self) -> None:
        incomplete = NutriOKIntake(product_code="ok_start")
        errors = incomplete.validation_errors()
        self.assertTrue(any("18+" in err for err in errors))
        self.assertTrue(any("152-ФЗ" in err for err in errors))
        self.assertTrue(any("цель" in err.lower() for err in errors))
        self.assertTrue(any("исходную оценку" in err.lower() for err in errors))

        valid_start = NutriOKIntake(
            product_code="ok_start",
            primary_goal="digestion",
            baseline_score=5,
            adult_confirmed=True,
            pd_consent_at="2026-10-30T10:00:00Z",
        )
        self.assertEqual(valid_start.validation_errors(), [])

    def test_paid_tier_requires_metric_and_three_diary_days(self) -> None:
        missing_diary = NutriOKIntake(
            product_code="ok_express",
            primary_goal="energy",
            baseline_score=3,
            goal_metric="",
            nutrition_diary=[DiaryDay(day_index=1, meals_text="Только 1 день")],
            adult_confirmed=True,
            pd_consent_at="2026-10-30T10:00:00Z",
        )
        errors = missing_diary.validation_errors()
        self.assertTrue(any("метрику" in err.lower() for err in errors))
        self.assertTrue(any("3 дня" in err.lower() for err in errors))

        photo_only_days = NutriOKIntake(
            product_code="ok_express",
            primary_goal="energy",
            baseline_score=3,
            goal_metric="энергия в 15:00, 0–10",
            nutrition_diary=[
                DiaryDay(day_index=1, meals_text="", photo_file_ids=["p1"]),
                DiaryDay(day_index=2, meals_text="Обед и ужин"),
                DiaryDay(day_index=3, meals_text="", photo_file_ids=["p3"]),
            ],
            adult_confirmed=True,
            pd_consent_at="2026-10-30T10:00:00Z",
        )
        self.assertEqual(photo_only_days.validation_errors(), [])


if __name__ == "__main__":
    unittest.main()
