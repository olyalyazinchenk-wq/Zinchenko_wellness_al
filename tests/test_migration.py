from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
OPS_DIR = PROJECT_ROOT / "ops"
for p in (BOT_DIR, OPS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from migrate_json_to_sqlite import (  # noqa: E402
    migrate_json_to_sqlite,
    verify_json_vs_sqlite,
)


class MigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="nutriok_migrate_test_"))
        self.submissions_dir = self.tmp_dir / "submissions"
        self.drafts_dir = self.tmp_dir / "drafts"
        self.backups_dir = self.tmp_dir / "backups"
        self.submissions_dir.mkdir(parents=True, exist_ok=True)
        self.drafts_dir.mkdir(parents=True, exist_ok=True)

        for idx in range(1, 4):
            sid = f"20261030T100{idx}00Z_{idx}"
            payload = {
                "submission_id": sid,
                "product_code": "ok_review",
                "intake_status": "awaiting_expert_review",
                "profile": {"telegram_user_id": idx, "name": f"Client {idx}"},
            }
            (self.submissions_dir / f"{sid}.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (self.drafts_dir / f"{sid}.md").write_text(f"# Draft {idx}\n", encoding="utf-8")

        runtime_state = {
            "user_sessions": {"1": {"step": "consent"}},
            "chat_sessions": {"1": [{"role": "user", "content": "Hello"}]},
        }
        (self.tmp_dir / "runtime_state.json").write_text(
            json.dumps(runtime_state, ensure_ascii=False),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_migration_creates_backup_and_verifies_parity_idempotently(self) -> None:
        summary1 = migrate_json_to_sqlite(self.tmp_dir, backups_dir=self.backups_dir)
        self.assertEqual(summary1["json_cases_found"], 3)
        self.assertEqual(summary1["imported_cases"], 3)
        self.assertEqual(summary1["db_cases_total"], 3)
        self.assertEqual(summary1["sessions_imported"], 1)
        self.assertIsNotNone(summary1["backup_path"])

        backup_path = Path(summary1["backup_path"])
        self.assertTrue(backup_path.exists())
        with zipfile.ZipFile(backup_path, "r") as zf:
            names = zf.namelist()
            self.assertIn("submissions/20261030T100100Z_1.json", names)

        # Idempotent second run
        summary2 = migrate_json_to_sqlite(self.tmp_dir, backups_dir=self.backups_dir, skip_backup=True)
        self.assertEqual(summary2["db_cases_total"], 3)

        verification = verify_json_vs_sqlite(self.tmp_dir)
        self.assertTrue(verification["ok"])
        self.assertEqual(verification["matched_count"], 3)

    def test_verify_detects_payload_mismatch(self) -> None:
        migrate_json_to_sqlite(self.tmp_dir, backups_dir=self.backups_dir, skip_backup=True)
        # Mutate JSON file without re-migrating
        sid = "20261030T100100Z_1"
        tampered = {
            "submission_id": sid,
            "product_code": "ok_express",
            "intake_status": "tampered",
            "profile": {"telegram_user_id": 1},
        }
        (self.submissions_dir / f"{sid}.json").write_text(
            json.dumps(tampered, ensure_ascii=False),
            encoding="utf-8",
        )
        verification = verify_json_vs_sqlite(self.tmp_dir)
        self.assertFalse(verification["ok"])
        self.assertIn(sid, verification["mismatches"])


if __name__ == "__main__":
    unittest.main()
