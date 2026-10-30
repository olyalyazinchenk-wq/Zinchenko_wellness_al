from __future__ import annotations

import dataclasses
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

os.environ.setdefault("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")

import main as bot_main  # noqa: E402
from review_gate import (  # noqa: E402
    compute_file_sha256,
    is_release_approved,
    list_user_approved_reports,
)
from storage import load_submission, save_submission  # noqa: E402


class ReportAccessTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.submissions_dir = Path(self.temp_dir.name) / "submissions"
        self.drafts_dir = Path(self.temp_dir.name) / "drafts"
        self.submissions_dir.mkdir(parents=True, exist_ok=True)
        self.drafts_dir.mkdir(parents=True, exist_ok=True)

        self.pdf_path = self.drafts_dir / "report_case_1.pdf"
        self.pdf_path.write_bytes(b"%PDF-1.4 sample content")

        self.owner_id = 1001
        self.stranger_id = 2002
        self.admin_id = 9009

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_submission(self, submission_id: str, payload: dict) -> dict:
        save_submission(self.submissions_dir, submission_id, payload)
        return payload

    async def test_foreign_user_is_denied_report_access(self) -> None:
        submission_id = f"20261030T000000Z_{self.owner_id}"
        self._write_submission(
            submission_id,
            {
                "submission_id": submission_id,
                "offer": "ok_review",
                "intake_status": "delivered_to_client",
                "approved_by_admin_id": self.admin_id,
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        callback = SimpleNamespace(
            id="cb_1",
            data=f"getpdf_{submission_id}",
            from_user=SimpleNamespace(id=self.stranger_id),
        )
        with (
            patch.object(
                bot_main,
                "settings",
                dataclasses.replace(bot_main.settings, submissions_dir=self.submissions_dir),
            ),
            patch.object(bot_main, "is_admin", return_value=False),
            patch.object(bot_main.bot, "answer_callback_query", new_callable=AsyncMock) as mock_answer,
            patch.object(bot_main.bot, "send_document", new_callable=AsyncMock) as mock_send_doc,
        ):
            await bot_main.process_get_report_pdf(callback)
            mock_answer.assert_awaited_once_with("cb_1", "Отчет не найден.", show_alert=True)
            mock_send_doc.assert_not_awaited()

    async def test_client_download_does_not_forge_supplement_approval(self) -> None:
        submission_id = f"20261030T000001Z_{self.owner_id}"
        self._write_submission(
            submission_id,
            {
                "submission_id": submission_id,
                "offer": "ok_express",
                "intake_status": "delivered_to_client",
                "auto_delivery_decision": {"allow_automatic_delivery": True},
                "supplement_review_required": True,
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        callback = SimpleNamespace(
            id="cb_2",
            data=f"getpdf_{submission_id}",
            from_user=SimpleNamespace(id=self.owner_id),
        )
        with (
            patch.object(
                bot_main,
                "settings",
                dataclasses.replace(bot_main.settings, submissions_dir=self.submissions_dir),
            ),
            patch.object(bot_main, "is_admin", return_value=False),
            patch.object(bot_main.bot, "answer_callback_query", new_callable=AsyncMock),
            patch.object(bot_main.bot, "send_chat_action", new_callable=AsyncMock),
            patch.object(bot_main.bot, "send_document", new_callable=AsyncMock) as mock_send_doc,
        ):
            await bot_main.process_get_report_pdf(callback)
            mock_send_doc.assert_awaited_once()

        saved = load_submission(self.submissions_dir, submission_id)
        self.assertIsNotNone(saved)
        self.assertNotIn("supplement_review_approved_by", saved)
        self.assertNotIn("supplement_review_approved_at", saved)
        self.assertNotIn("supplement_review_decision", saved)

    async def test_unapproved_submission_is_not_released(self) -> None:
        submission_id = f"20261030T000002Z_{self.owner_id}"
        self._write_submission(
            submission_id,
            {
                "submission_id": submission_id,
                "offer": "ok_review",
                "intake_status": "awaiting_expert_review",
                "auto_delivery_decision": {"allow_automatic_delivery": False},
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        callback = SimpleNamespace(
            id="cb_3",
            data=f"getpdf_{submission_id}",
            from_user=SimpleNamespace(id=self.owner_id),
        )
        with (
            patch.object(
                bot_main,
                "settings",
                dataclasses.replace(bot_main.settings, submissions_dir=self.submissions_dir),
            ),
            patch.object(bot_main, "is_admin", return_value=False),
            patch.object(bot_main.bot, "answer_callback_query", new_callable=AsyncMock) as mock_answer,
            patch.object(bot_main.bot, "send_document", new_callable=AsyncMock) as mock_send_doc,
        ):
            await bot_main.process_get_report_pdf(callback)
            mock_answer.assert_awaited_once_with(
                "cb_3",
                "Отчет еще на проверке у Ольги.",
                show_alert=True,
            )
            mock_send_doc.assert_not_awaited()

            reports = bot_main.get_user_approved_reports(self.owner_id)
            self.assertEqual(reports, [])

    def test_get_user_approved_reports_filters_owner_and_approval(self) -> None:
        sub_approved = f"20261030T000003Z_{self.owner_id}"
        sub_unapproved = f"20261030T000004Z_{self.owner_id}"
        sub_spoofed_filename = f"20261030T000005Z_{self.owner_id}"

        self._write_submission(
            sub_approved,
            {
                "submission_id": sub_approved,
                "intake_status": "delivered_to_client",
                "approved_by_admin_id": self.admin_id,
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        self._write_submission(
            sub_unapproved,
            {
                "submission_id": sub_unapproved,
                "intake_status": "awaiting_expert_review",
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        self._write_submission(
            sub_spoofed_filename,
            {
                "submission_id": sub_spoofed_filename,
                "intake_status": "delivered_to_client",
                "approved_by_admin_id": self.admin_id,
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.stranger_id},
            },
        )

        reports = list_user_approved_reports(self.submissions_dir, self.owner_id)
        self.assertEqual([r["submission_id"] for r in reports], [sub_approved])

    def test_review_records_check_artifact_sha256(self) -> None:
        sha = compute_file_sha256(self.pdf_path)
        submission = {
            "pdf_path": str(self.pdf_path),
            "review_records": [
                {
                    "decision": "approved",
                    "artifact_path": str(self.pdf_path),
                    "artifact_sha256": sha,
                }
            ],
        }
        self.assertTrue(is_release_approved(submission))

        tampered = {
            "pdf_path": str(self.pdf_path),
            "review_records": [
                {
                    "decision": "approved",
                    "artifact_path": str(self.pdf_path),
                    "artifact_sha256": "0" * 64,
                }
            ],
        }
        self.assertFalse(is_release_approved(tampered))

    async def test_admin_approval_records_admin_id_and_supplement_approval(self) -> None:
        submission_id = f"20261030T000006Z_{self.owner_id}"
        self._write_submission(
            submission_id,
            {
                "submission_id": submission_id,
                "offer": "ok_review",
                "intake_status": "awaiting_expert_review",
                "supplement_review_required": True,
                "pdf_path": str(self.pdf_path),
                "profile": {"telegram_user_id": self.owner_id},
            },
        )
        callback = SimpleNamespace(
            id="cb_admin",
            data=f"approve_{submission_id}",
            from_user=SimpleNamespace(id=self.admin_id),
        )
        with (
            patch.object(
                bot_main,
                "settings",
                dataclasses.replace(bot_main.settings, submissions_dir=self.submissions_dir),
            ),
            patch.object(bot_main, "is_admin", return_value=True),
            patch.object(bot_main, "build_delivery_block_reason", return_value=""),
            patch.object(bot_main.bot, "answer_callback_query", new_callable=AsyncMock),
            patch.object(bot_main.bot, "send_message", new_callable=AsyncMock),
            patch.object(bot_main.bot, "send_document", new_callable=AsyncMock) as mock_send_doc,
        ):
            await bot_main.process_admin_approval(callback)
            mock_send_doc.assert_awaited_once()

        saved = load_submission(self.submissions_dir, submission_id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved.get("approved_by_admin_id"), self.admin_id)
        self.assertEqual(saved.get("supplement_review_approved_by"), self.admin_id)
        self.assertEqual(saved.get("supplement_review_decision"), "approved")
        self.assertTrue(is_release_approved(saved))


if __name__ == "__main__":
    unittest.main()
