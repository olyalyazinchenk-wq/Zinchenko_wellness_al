from __future__ import annotations

import dataclasses
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

import main as bot_main  # noqa: E402
from review_gate import (  # noqa: E402
    ReviewRecord,
    compute_file_sha256,
    is_release_approved,
    record_review,
    release_or_raise,
)
from storage import load_submission, save_submission  # noqa: E402


class ReviewGateTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.submissions_dir = base / "submissions"
        self.drafts_dir = base / "drafts"
        self.submissions_dir.mkdir(parents=True, exist_ok=True)
        self.drafts_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_path = self.drafts_dir / "report_review.pdf"
        self.pdf_path.write_bytes(b"%PDF-1.4 NutriOK test artifact\n")
        self.admin_id = 481955956
        self.owner_id = 100500

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_record_review_rejects_non_admin(self) -> None:
        submission = {"submission_id": "sub_1", "pdf_path": str(self.pdf_path)}
        with self.assertRaises(PermissionError):
            record_review(
                submission,
                reviewer_id=999999,
                reviewer_name="Attacker",
                decision="approved",
                artifact_path=self.pdf_path,
                admin_ids={self.admin_id},
            )

    def test_record_review_appends_record_and_verifies_sha256(self) -> None:
        submission = {"submission_id": "sub_2", "pdf_path": str(self.pdf_path)}
        rec = record_review(
            submission,
            reviewer_id=self.admin_id,
            reviewer_name="Ольга Ковалева",
            decision="approved",
            artifact_path=self.pdf_path,
            notes="Проверено лично",
            admin_ids={self.admin_id},
        )
        self.assertIsInstance(rec, ReviewRecord)
        self.assertEqual(rec.artifact_sha256, compute_file_sha256(self.pdf_path))
        self.assertTrue(is_release_approved(submission))
        self.assertEqual(release_or_raise(submission), self.pdf_path)

        # Tampering with PDF after approval must block release_or_raise
        self.pdf_path.write_bytes(b"%PDF-1.4 modified after approval\n")
        self.assertFalse(is_release_approved(submission))
        with self.assertRaises(PermissionError):
            release_or_raise(submission)

    def test_changes_requested_and_rejected_block_release(self) -> None:
        submission = {"submission_id": "sub_3", "pdf_path": str(self.pdf_path)}
        record_review(
            submission,
            reviewer_id=self.admin_id,
            reviewer_name="Ольга Ковалева",
            decision="approved",
            artifact_path=self.pdf_path,
            admin_ids={self.admin_id},
        )
        self.assertEqual(release_or_raise(submission), self.pdf_path)

        record_review(
            submission,
            reviewer_id=self.admin_id,
            reviewer_name="Ольга Ковалева",
            decision="changes_requested",
            artifact_path=self.pdf_path,
            notes="Уточнить время приёма магния",
            admin_ids={self.admin_id},
        )
        self.assertFalse(is_release_approved(submission))
        with self.assertRaises(PermissionError):
            release_or_raise(submission)

        record_review(
            submission,
            reviewer_id=self.admin_id,
            reviewer_name="Ольга Ковалева",
            decision="rejected",
            artifact_path=self.pdf_path,
            notes="Красный флаг",
            admin_ids={self.admin_id},
        )
        self.assertFalse(is_release_approved(submission))
        with self.assertRaises(PermissionError):
            release_or_raise(submission)

    def test_release_or_raise_allows_auto_delivery_only_for_ok_express(self) -> None:
        express_sub = {
            "submission_id": "sub_exp",
            "offer": "ok_express",
            "pdf_path": str(self.pdf_path),
            "auto_delivery_decision": {"allow_automatic_delivery": True},
        }
        self.assertEqual(release_or_raise(express_sub), self.pdf_path)

        review_sub = {
            "submission_id": "sub_rev",
            "offer": "ok_review",
            "pdf_path": str(self.pdf_path),
            "auto_delivery_decision": {"allow_automatic_delivery": True},
        }
        with self.assertRaises(PermissionError):
            release_or_raise(review_sub)

        # B6: fail-closed when product/offer/tier codes are missing
        no_code_sub = {
            "submission_id": "sub_no_code",
            "pdf_path": str(self.pdf_path),
            "auto_delivery_decision": {"allow_automatic_delivery": True},
        }
        self.assertFalse(is_release_approved(no_code_sub))
        with self.assertRaises(PermissionError):
            release_or_raise(no_code_sub)

    def test_legacy_approved_by_admin_id_verifies_approved_artifact_sha256(self) -> None:
        original_sha = compute_file_sha256(self.pdf_path)
        legacy_sub = {
            "submission_id": "sub_legacy_admin",
            "intake_status": "delivered_to_client",
            "approved_by_admin_id": self.admin_id,
            "approved_artifact_sha256": original_sha,
            "pdf_path": str(self.pdf_path),
        }
        self.assertTrue(is_release_approved(legacy_sub))
        self.assertEqual(release_or_raise(legacy_sub), self.pdf_path)

        # Tampering with PDF after approved_by_admin_id must block release
        self.pdf_path.write_bytes(b"%PDF-1.4 tampered after legacy admin approval\n")
        self.assertFalse(is_release_approved(legacy_sub))
        with self.assertRaises(PermissionError):
            release_or_raise(legacy_sub)

    async def test_admin_callbacks_changes_with_comment_and_reject(self) -> None:
        submission_id = f"20261030T120000Z_{self.owner_id}"
        save_submission(
            self.submissions_dir,
            submission_id,
            {
                "submission_id": submission_id,
                "offer": "ok_review",
                "intake_status": "awaiting_human_review",
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        patched_settings = dataclasses.replace(
            bot_main.settings,
            submissions_dir=self.submissions_dir,
            admin_chat_ids=(self.admin_id,),
        )
        cb_changes = SimpleNamespace(
            id="cb_chg",
            data=f"changes_{submission_id}",
            from_user=SimpleNamespace(id=self.admin_id, full_name="Ольга Ковалева"),
        )
        comment_msg = SimpleNamespace(
            text="Убрать упоминание железа до сдачи ферритина",
            from_user=SimpleNamespace(id=self.admin_id, full_name="Ольга Ковалева"),
            answer=AsyncMock(),
        )
        cb_reject = SimpleNamespace(
            id="cb_rej",
            data=f"reject_{submission_id}",
            from_user=SimpleNamespace(id=self.admin_id, full_name="Ольга Ковалева"),
        )
        with (
            patch.object(bot_main, "settings", patched_settings),
            patch.object(bot_main, "is_admin", return_value=True),
            patch.object(bot_main.bot, "answer_callback_query", new_callable=AsyncMock),
            patch.object(bot_main.bot, "send_message", new_callable=AsyncMock),
        ):
            await bot_main.process_admin_draft(cb_changes)
            await bot_main.handle_message(comment_msg)
            saved_after_changes = load_submission(self.submissions_dir, submission_id)
            self.assertEqual(saved_after_changes["intake_status"], "draft_requires_edits")
            self.assertEqual(
                saved_after_changes["review_records"][-1]["notes"],
                "Убрать упоминание железа до сдачи ферритина",
            )
            self.assertFalse(is_release_approved(saved_after_changes))

            await bot_main.process_admin_reject(cb_reject)
            saved_after_reject = load_submission(self.submissions_dir, submission_id)
            self.assertEqual(saved_after_reject["intake_status"], "rejected_by_admin")
            self.assertEqual(saved_after_reject["review_records"][-1]["decision"], "rejected")
            self.assertFalse(is_release_approved(saved_after_reject))


if __name__ == "__main__":
    unittest.main()
