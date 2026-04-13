from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import re


def build_submission_id(user_id: int) -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{user_id}"


def sanitize_filename(file_name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", file_name.strip())
    return cleaned or "upload.bin"


def case_upload_dir(uploads_dir: Path, submission_id: str) -> Path:
    target_dir = uploads_dir / submission_id
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def save_submission(submissions_dir: Path, submission_id: str, payload: dict) -> Path:
    target_path = submissions_dir / f"{submission_id}.json"
    target_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return target_path


def save_draft(drafts_dir: Path, submission_id: str, draft_text: str) -> Path:
    target_path = drafts_dir / f"{submission_id}.md"
    target_path.write_text(draft_text.strip() + "\n", encoding="utf-8")
    return target_path


def list_recent_cases(submissions_dir: Path, limit: int = 5) -> list[dict]:
    files = sorted(
        submissions_dir.glob("*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    recent_cases: list[dict] = []
    for path in files[:limit]:
        try:
            recent_cases.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return recent_cases
