from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from aiohttp.test_utils import TestClient, TestServer

BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from html_pdf_engine import build_nutriok_report_context, render_nutriok_report_html  # noqa: E402
from studio_server import create_studio_app  # noqa: E402


class StudioAndPdfReportTests(unittest.IsolatedAsyncioTestCase):
    def test_nutriok_editorial_report_html_contains_all_e1_blocks(self) -> None:
        submission = {
            "submission_id": "20261030T220000Z_demo",
            "product_code": "ok_review",
            "primary_goal": "energy",
            "baseline_score": 4,
            "goal_metric": "Бодрость после обеда (0–10)",
            "profile": {"full_name": "Мария Иванова"},
            "intake": {
                "product_code": "ok_review",
                "primary_goal": "energy",
                "baseline_score": 4,
                "goal_metric": "Бодрость после обеда (0–10)",
                "diary": [
                    {"day_label": "День 1", "meals_text": "Капучино натощак и круассан"},
                    {"day_label": "День 2", "meals_text": "Паста в обед и сонливость в 15:00"},
                    {"day_label": "День 3", "meals_text": "Омлет с зеленью утром"},
                ],
            },
            "review_records": [
                {
                    "reviewer_id": 481955956,
                    "reviewer_name": "Ольга Ковалева",
                    "decision": "approved",
                    "decided_at": "2026-10-30T22:30:00Z",
                    "artifact_path": "demo.pdf",
                    "artifact_sha256": "a1b2c3d4e5f60123456789abcdef",
                }
            ],
        }
        html = render_nutriok_report_html({}, submission=submission)
        self.assertIn("НутриОК by Olga Kovaleva", html)
        self.assertIn("Ваша Точка А", html)
        self.assertIn("Бодрость после обеда (0–10)", html)
        self.assertIn("Капучино натощак и круассан", html)
        self.assertIn("План действий на 7 дней", html)
        self.assertIn("День 7", html)
        self.assertIn("Как измерять прогресс", html)
        self.assertIn("Проверено лично: Ольга Ковалева", html)
        self.assertIn("SHA-256 VERIFIED", html)
        self.assertIn("не является медицинской услугой", html)
        self.assertIn("@zinchenko_wellness_ai_1_bot", html)

    def test_express_tier_does_not_show_olga_personal_stamp_by_default(self) -> None:
        submission = {
            "submission_id": "20261030T220500Z_exp",
            "product_code": "ok_express",
            "primary_goal": "gut_comfort",
            "baseline_score": 5,
        }
        ctx = build_nutriok_report_context({}, submission=submission)
        self.assertIsNone(ctx["review_stamp"])

    async def test_studio_api_simulate_and_html_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            subs_dir = tmp_path / "submissions"
            drafts_dir = tmp_path / "drafts"
            subs_dir.mkdir()
            drafts_dir.mkdir()

            from config import load_settings
            import dataclasses

            real_settings = load_settings()
            patched_settings = dataclasses.replace(
                real_settings,
                submissions_dir=subs_dir,
                drafts_dir=drafts_dir,
                admin_chat_ids=(481955956,),
            )
            with patch("studio_server.load_settings", return_value=patched_settings):
                app = create_studio_app()
                async with TestClient(TestServer(app)) as client:
                    resp = await client.get("/")
                    self.assertEqual(resp.status, 200)
                    index_text = await resp.text()
                    self.assertIn("НутриОК by Olga Kovaleva", index_text)

                    sim_resp = await client.post(
                        "/api/simulate",
                        json={
                            "client_name": "Тестовый Клиент",
                            "product_code": "ok_review",
                            "primary_goal": "energy",
                            "baseline_score": 3,
                            "symptoms": "Усталость после обеда",
                            "diary_days": ["День 1: кофе", "День 2: паста", "День 3: омлет"],
                        },
                    )
                    self.assertEqual(sim_resp.status, 200)
                    sim_data = await sim_resp.json()
                    self.assertTrue(sim_data["ok"])
                    sub_id = sim_data["submission_id"]

                    html_resp = await client.get(f"/api/cases/{sub_id}/html")
                    self.assertEqual(html_resp.status, 200)
                    html_body = await html_resp.text()
                    self.assertIn("Тестовый Клиент", html_body)


if __name__ == "__main__":
    unittest.main()
