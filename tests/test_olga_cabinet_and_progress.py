from __future__ import annotations

from datetime import datetime, timezone
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from handlers.olga_cabinet import (  # noqa: E402
    build_admin_queue,
    build_queue_case_card,
    compute_funnel_stats,
    format_queue_summary,
    format_stats_message,
    record_weekly_checkin,
    render_progress_chart_png,
)
from storage import load_submission, save_submission  # noqa: E402


class OlgaCabinetAndProgressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="nutriok_cabinet_test_"))
        self.submissions_dir = self.tmp_dir / "submissions"
        self.submissions_dir.mkdir(parents=True, exist_ok=True)
        self.ref_now = datetime(2026, 10, 30, 18, 0, 0, tzinfo=timezone.utc)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_queue_sorts_safety_and_sla_overdue_first(self) -> None:
        save_submission(
            self.submissions_dir,
            "20261030T150000Z_101",
            {
                "submission_id": "20261030T150000Z_101",
                "product_code": "ok_review",
                "intake_status": "awaiting_expert_review",
                "created_at": "2026-10-30T15:00:00Z",
                "intake": {"primary_goal": "energy", "baseline_score": 5},
            },
        )
        save_submission(
            self.submissions_dir,
            "20261028T100000Z_102",
            {
                "submission_id": "20261028T100000Z_102",
                "product_code": "ok_result_8",
                "intake_status": "awaiting_expert_review",
                "created_at": "2026-10-28T10:00:00Z",
                "intake": {"primary_goal": "digestion", "baseline_score": 3},
            },
        )
        save_submission(
            self.submissions_dir,
            "20261030T170000Z_103",
            {
                "submission_id": "20261030T170000Z_103",
                "product_code": "ok_express",
                "intake_status": "awaiting_safety_review",
                "created_at": "2026-10-30T17:00:00Z",
                "symptoms": "Черный дегтеобразный стул два дня",
                "intake": {"primary_goal": "digestion", "baseline_score": 2},
            },
        )

        queue = build_admin_queue(self.submissions_dir, now=self.ref_now)
        self.assertEqual(len(queue), 3)
        # Safety case first, then SLA overdue (>24h), then fresh expert review
        self.assertEqual(queue[0]["submission_id"], "20261030T170000Z_103")
        self.assertEqual(queue[1]["submission_id"], "20261028T100000Z_102")
        self.assertTrue(queue[1]["sla_overdue"])
        self.assertEqual(queue[2]["submission_id"], "20261030T150000Z_101")
        self.assertFalse(queue[2]["sla_overdue"])

        summary_html = format_queue_summary(queue)
        self.assertIn("Очередь проверки Ольги Ковалевой (3)", summary_html)
        self.assertIn(">24ч", summary_html)

        card_text, kb = build_queue_case_card(queue[0])
        self.assertIn("20261030T170000Z_103", card_text)
        cb_data = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        self.assertEqual(
            cb_data,
            [
                "approve_20261030T170000Z_103",
                "changes_20261030T170000Z_103",
                "reject_20261030T170000Z_103",
            ],
        )

    def test_funnel_stats_7d_30d_and_sla_reminder(self) -> None:
        save_submission(
            self.submissions_dir,
            "20261029T100000Z_201",
            {
                "submission_id": "20261029T100000Z_201",
                "product_code": "ok_start",
                "intake_status": "completed",
                "created_at": "2026-10-29T10:00:00Z",
            },
        )
        save_submission(
            self.submissions_dir,
            "20261010T100000Z_202",
            {
                "submission_id": "20261010T100000Z_202",
                "product_code": "ok_review",
                "intake_status": "awaiting_expert_review",
                "created_at": "2026-10-10T10:00:00Z",
            },
        )

        stats = compute_funnel_stats(self.submissions_dir, now=self.ref_now)
        self.assertEqual(stats["counts_7d"]["ok_start"], 1)
        self.assertEqual(stats["counts_7d"]["ok_review"], 0)
        self.assertEqual(stats["counts_30d"]["ok_review"], 1)
        self.assertEqual(stats["overdue_count"], 1)

        msg = format_stats_message(stats)
        self.assertIn("Воронка НутриОК", msg)
        self.assertIn("SLA-напоминание (> 24 ч)", msg)

    def test_weekly_checkin_records_adherence_and_renders_png_chart(self) -> None:
        sid = "20261030T120000Z_301"
        save_submission(
            self.submissions_dir,
            sid,
            {
                "submission_id": sid,
                "product_code": "ok_result_8",
                "intake_status": "delivered_to_client",
                "baseline_score": 4,
                "intake": {"primary_goal": "energy", "baseline_score": 4},
            },
        )

        res1 = record_weekly_checkin(
            self.submissions_dir,
            sid,
            week=1,
            metric_value=6.0,
            completed_actions=5,
            planned_actions=7,
            notes="Завтрак с белком вошел в привычку",
        )
        self.assertAlmostEqual(res1["adherence_pct"], 71.4, places=1)
        self.assertEqual(res1["intake_status"], "awaiting_expert_review")

        res2 = record_weekly_checkin(
            self.submissions_dir,
            sid,
            week=2,
            metric_value=7.5,
            completed_actions=6,
            planned_actions=7,
            notes="После обеда нет сонливости",
        )
        self.assertAlmostEqual(res2["adherence_pct"], 85.7, places=1)

        updated = load_submission(self.submissions_dir, sid)
        self.assertEqual(len(updated["adherence_history"]), 2)
        self.assertIn("Черновик адаптации недели 2", updated["weekly_adaptation_draft"])

        png = render_progress_chart_png(updated["adherence_history"], baseline_score=4.0)
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertIn(b"IHDR", png)
        self.assertIn(b"IDAT", png)
        self.assertIn(b"IEND", png)
        self.assertGreater(len(png), 250)


if __name__ == "__main__":
    unittest.main()
