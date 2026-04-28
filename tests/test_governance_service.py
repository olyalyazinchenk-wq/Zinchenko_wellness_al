from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

import governance_service as gs  # noqa: E402


class GovernanceServiceTests(unittest.TestCase):
    def test_governance_ids_are_unique(self) -> None:
        experiment_ids = {gs.build_governance_experiment_id() for _ in range(50)}
        decision_ids = {gs.build_governance_decision_id() for _ in range(50)}

        self.assertEqual(len(experiment_ids), 50)
        self.assertEqual(len(decision_ids), 50)
        self.assertTrue(all(item.startswith("EXP-") for item in experiment_ids))
        self.assertTrue(all(item.startswith("DEC-") for item in decision_ids))

    def test_empty_state_messages_are_stable(self) -> None:
        self.assertIn(
            "Накопленные product insights пока пусты.",
            gs.format_product_insights_summary({"cases": {}, "updated_at": None}),
        )
        self.assertIn(
            "Governance Summary:",
            gs.format_governance_summary({"decisions": [], "experiments": [], "updated_at": None}),
        )

    def test_sync_and_digest_work_in_isolated_storage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            submissions_dir = tmp / "submissions"
            uploads_dir = tmp / "uploads"
            drafts_dir = tmp / "drafts"
            for directory in (submissions_dir, uploads_dir, drafts_dir):
                directory.mkdir(parents=True, exist_ok=True)

            original_settings = gs.settings
            gs.settings = replace(
                gs.settings,
                data_dir=tmp,
                submissions_dir=submissions_dir,
                uploads_dir=uploads_dir,
                drafts_dir=drafts_dir,
                runtime_state_path=tmp / "runtime_state.json",
                product_insights_path=tmp / "product_insights.json",
                product_governance_path=tmp / "product_governance.json",
            )

            try:
                submission = {
                    "submission_id": "test_case_001",
                    "internal_review": {
                        "judge_verdict": "needs_rework",
                        "market_verdict": "stronger_positioning_needed",
                        "review_flags": ["quality_rework", "market_rework"],
                    },
                    "profile": {"full_name": "Тестовый клиент"},
                    "intake_status": "awaiting_human_review",
                }
                judge_report = json.dumps(
                    {
                        "market_value_risks": [
                            "Премиальная ценность описана слишком расплывчато",
                        ]
                    },
                    ensure_ascii=False,
                )
                growth_report = json.dumps(
                    {
                        "demand_risks": [
                            "Клиенту неочевидно, какой конкретный результат он получает на выходе",
                        ],
                        "value_gaps": [
                            "Не хватает структуры следующего шага после анкеты",
                        ],
                        "positioning_upgrades": [
                            "Подчеркнуть деликатную нутрициологическую навигацию без медицинских обещаний",
                        ],
                        "conversion_ideas": [
                            "Показать пример итогового разбора и формат персонального сопровождения",
                        ],
                        "retention_ideas": [
                            "Добавить follow-up касание после выдачи разбора",
                        ],
                        "next_experiments": [
                            "Протестировать более конкретный оффер с акцентом на персональный план действий",
                        ],
                    },
                    ensure_ascii=False,
                )

                payload = gs.update_product_insights_memory(submission, judge_report, growth_report)
                gs.sync_governance_experiments_from_insights(payload)
                governance = json.loads(gs.settings.product_governance_path.read_text(encoding="utf-8"))

                experiment_ids = [item["id"] for item in governance["experiments"]]
                self.assertEqual(len(experiment_ids), len(set(experiment_ids)))
                self.assertGreaterEqual(len(experiment_ids), 3)

                decision = gs.record_product_decision(
                    "Проверить новый оффер и структуру выдачи",
                    source="unit_test",
                    title="Проверить новый оффер",
                )
                gs.update_decision_execution(
                    decision["id"],
                    owner="Olga",
                    deadline="2026-04-28",
                    kpi="5 кейсов",
                )

                digest_text = gs.build_admin_digest_text(payload)
                self.assertIn("Автодайджест продукта", digest_text)
                self.assertIn("Suggested Decisions", digest_text)
                self.assertIn("Execution Gaps", digest_text)
            finally:
                gs.settings = original_settings


if __name__ == "__main__":
    unittest.main()
