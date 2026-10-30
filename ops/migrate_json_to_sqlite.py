from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from repo.sqlite_repo import SqliteRepository  # noqa: E402
from storage import load_runtime_state  # noqa: E402


def create_data_backup(data_dir: Path, backups_dir: Path) -> Path:
    backups_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = backups_dir / f"{ts}_sqlite_migration.zip"
    with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if not data_dir.exists():
            return backup_path
        for file_path in sorted(data_dir.rglob("*")):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(data_dir)
            if rel.parts and rel.parts[0] == "backups":
                continue
            if file_path.name.startswith("nutriok.db"):
                continue
            zf.write(file_path, arcname=str(rel).replace("\\", "/"))
    return backup_path


def migrate_json_to_sqlite(
    data_dir: Path,
    *,
    db_path: Path | None = None,
    backups_dir: Path | None = None,
    skip_backup: bool = False,
) -> dict[str, Any]:
    resolved_data = Path(data_dir)
    submissions_dir = resolved_data / "submissions"
    drafts_dir = resolved_data / "drafts"
    runtime_state_path = resolved_data / "runtime_state.json"
    resolved_db = Path(db_path) if db_path is not None else (resolved_data / "nutriok.db")
    resolved_backups = Path(backups_dir) if backups_dir is not None else (resolved_data / "backups")

    backup_archive: Path | None = None
    if not skip_backup:
        backup_archive = create_data_backup(resolved_data, resolved_backups)

    repo = SqliteRepository(resolved_db)

    json_files = sorted(submissions_dir.glob("*.json")) if submissions_dir.exists() else []
    imported_cases = 0
    skipped_files = 0
    draft_events_indexed = 0

    for path in json_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError):
            skipped_files += 1
            continue
        if not isinstance(payload, dict):
            skipped_files += 1
            continue

        submission_id = str(payload.get("submission_id") or path.stem)
        payload.setdefault("submission_id", submission_id)
        repo.save_case(submission_id, payload)
        imported_cases += 1

        if drafts_dir.exists():
            draft_meta: dict[str, str] = {}
            for suffix in (".md", ".review.json", ".growth.json"):
                candidate = drafts_dir / f"{submission_id}{suffix}"
                if candidate.exists() and candidate.is_file():
                    draft_meta[suffix.lstrip(".")] = candidate.name
            if draft_meta:
                repo.append_event(
                    actor_id=0,
                    submission_id=submission_id,
                    kind="draft_metadata_migrated",
                    data=draft_meta,
                    at=str(payload.get("created_at") or "2026-01-01T00:00:00Z"),
                )
                draft_events_indexed += 1

    runtime_state = load_runtime_state(runtime_state_path)
    user_sessions = runtime_state.get("user_sessions", {}) or {}
    chat_sessions = runtime_state.get("chat_sessions", {}) or {}
    repo.save_sessions(user_sessions, chat_sessions)

    return {
        "db_path": str(resolved_db),
        "backup_path": str(backup_archive) if backup_archive else None,
        "json_cases_found": len(json_files),
        "imported_cases": imported_cases,
        "skipped_files": skipped_files,
        "db_cases_total": repo.count_cases(),
        "draft_events_indexed": draft_events_indexed,
        "sessions_imported": len(set(user_sessions.keys()) | set(chat_sessions.keys())),
    }


def verify_json_vs_sqlite(
    data_dir: Path,
    *,
    db_path: Path | None = None,
) -> dict[str, Any]:
    resolved_data = Path(data_dir)
    submissions_dir = resolved_data / "submissions"
    resolved_db = Path(db_path) if db_path is not None else (resolved_data / "nutriok.db")
    repo = SqliteRepository(resolved_db)

    json_files = sorted(submissions_dir.glob("*.json")) if submissions_dir.exists() else []
    matched = 0
    mismatches: list[str] = []
    missing_in_db: list[str] = []

    for path in json_files:
        try:
            json_payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(json_payload, dict):
            continue

        submission_id = str(json_payload.get("submission_id") or path.stem)
        json_payload.setdefault("submission_id", submission_id)
        db_payload = repo.get_case(submission_id)
        if db_payload is None:
            missing_in_db.append(submission_id)
            continue
        if db_payload != json_payload:
            mismatches.append(submission_id)
            continue
        matched += 1

    return {
        "ok": len(missing_in_db) == 0 and len(mismatches) == 0,
        "json_count": len(json_files),
        "db_count": repo.count_cases(),
        "matched_count": matched,
        "missing_in_db": missing_in_db,
        "mismatches": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate WellnessBot JSON data into SQLite and verify parity.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PROJECT_ROOT / "WellnessBot" / "data",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run migration (idempotent) and verify 1-to-1 parity between JSON submissions and SQLite.",
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="Skip zip backup creation before migration.",
    )
    args = parser.parse_args()

    migration_summary = migrate_json_to_sqlite(
        args.data_dir,
        db_path=args.db_path,
        skip_backup=args.skip_backup,
    )
    print("=== SQLite Migration Summary ===")
    print(f"Database path      : {migration_summary['db_path']}")
    if migration_summary["backup_path"]:
        print(f"Backup archive     : {migration_summary['backup_path']}")
    print(f"JSON cases found   : {migration_summary['json_cases_found']}")
    print(f"Cases imported     : {migration_summary['imported_cases']}")
    print(f"Total cases in DB  : {migration_summary['db_cases_total']}")
    print(f"Sessions imported  : {migration_summary['sessions_imported']}")

    if args.verify:
        verification = verify_json_vs_sqlite(args.data_dir, db_path=args.db_path)
        print("\n=== JSON <-> SQLite Verification ===")
        print(f"Matched cases      : {verification['matched_count']}/{verification['json_count']}")
        print(f"Missing in DB      : {len(verification['missing_in_db'])}")
        print(f"Payload mismatches : {len(verification['mismatches'])}")
        print(f"Verification OK    : {verification['ok']}")
        if not verification["ok"]:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
