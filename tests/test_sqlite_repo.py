from __future__ import annotations

import contextlib
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from repo.sqlite_repo import SqliteRepository  # noqa: E402
from storage import (  # noqa: E402
    load_runtime_state,
    load_submission,
    save_runtime_state,
    save_submission,
)


class SqliteRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="nutriok_sqlite_test_"))
        self.db_path = self.tmp_dir / "nutriok.db"
        self.submissions_dir = self.tmp_dir / "submissions"
        self.submissions_dir.mkdir(parents=True, exist_ok=True)
        self.repo = SqliteRepository(self.db_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_pragmas_configured_properly(self) -> None:
        pragmas = self.repo.get_pragmas()
        self.assertEqual(pragmas["journal_mode"], "wal")
        self.assertEqual(pragmas["foreign_keys"], 1)
        self.assertEqual(pragmas["user_version"], 1)

    def test_save_and_get_case_with_intake_and_events(self) -> None:
        submission_id = "20261030T120000Z_501"
        payload = {
            "submission_id": submission_id,
            "product_code": "ok_review",
            "intake_status": "awaiting_expert_review",
            "created_at": "2026-10-30T12:00:00Z",
            "status_updated_at": "2026-10-30T12:05:00Z",
            "profile": {
                "telegram_user_id": 501,
                "name": "Анна Тест",
            },
            "intake": {
                "schema_version": 2,
                "product_code": "ok_review",
                "primary_goal": "energy_after_meals",
                "baseline_score": 4,
            },
            "payment_status": "paid_confirmed",
            "payment_amount_rub": 4900,
            "payment_mode": "manual",
            "audit_events": [
                {
                    "at": "2026-10-30T12:05:00Z",
                    "actor_id": 501,
                    "submission_id": submission_id,
                    "kind": "intake_submitted",
                    "data": {"goal": "energy_after_meals"},
                }
            ],
        }
        self.repo.save_case(submission_id, payload)
        loaded = self.repo.get_case(submission_id)
        self.assertEqual(loaded, payload)

        by_user = self.repo.list_cases(user_id=501)
        self.assertEqual(len(by_user), 1)
        self.assertEqual(by_user[0]["submission_id"], submission_id)

        by_status = self.repo.list_cases(status="awaiting_expert_review")
        self.assertEqual(len(by_status), 1)

    def test_reviews_table_is_append_only(self) -> None:
        submission_id = "20261030T121000Z_777"
        self.repo.save_case(
            submission_id,
            {
                "submission_id": submission_id,
                "profile": {"telegram_user_id": 777},
                "intake_status": "delivered_to_client",
            },
        )
        review_id = self.repo.append_review(
            submission_id,
            reviewer_id=999,
            decision="approved",
            decided_at="2026-10-30T12:15:00Z",
            artifact_sha256="deadbeef" * 8,
            notes="LGTM",
        )
        self.assertGreater(review_id, 0)
        reviews = self.repo.list_reviews(submission_id)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["decision"], "approved")

        with contextlib.closing(sqlite3.connect(str(self.db_path))) as conn:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("UPDATE reviews SET decision = 'rejected' WHERE id = ?", (review_id,))
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))

    def test_storage_facade_persists_to_sqlite_and_json_backup(self) -> None:
        submission_id = "20261030T123000Z_888"
        payload = {
            "submission_id": submission_id,
            "product_code": "ok_express",
            "intake_status": "delivered_to_client",
            "profile": {"telegram_user_id": 888},
        }
        json_path = save_submission(self.submissions_dir, submission_id, payload)
        self.assertTrue(json_path.exists())

        # Remove JSON file to verify SQLite fallback works through storage facade
        json_path.unlink()
        loaded = load_submission(self.submissions_dir, submission_id)
        self.assertEqual(loaded, payload)

    def test_sessions_roundtrip_via_storage_facade(self) -> None:
        state_path = self.tmp_dir / "runtime_state.json"
        user_sessions = {101: {"step": "diary_day_2", "product_code": "ok_review"}}
        chat_sessions = {101: [{"role": "user", "content": "Привет"}]}
        save_runtime_state(state_path, user_sessions, chat_sessions)

        # Remove JSON runtime_state to prove SQLite sessions table restores it
        state_path.unlink()
        restored = load_runtime_state(state_path)
        self.assertEqual(restored["user_sessions"]["101"]["step"], "diary_day_2")
        self.assertEqual(restored["chat_sessions"]["101"][0]["content"], "Привет")


if __name__ == "__main__":
    unittest.main()
