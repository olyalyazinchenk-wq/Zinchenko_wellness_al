from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import re
import tempfile
from typing import Any

from repo.sqlite_repo import SqliteRepository


def _repo_for_submissions_dir(submissions_dir: Path) -> SqliteRepository:
    return SqliteRepository(Path(submissions_dir).parent / "nutriok.db")


def _repo_for_state_path(state_path: Path) -> SqliteRepository:
    return SqliteRepository(Path(state_path).parent / "nutriok.db")


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


def atomic_write_text(target_path: Path, content: str, *, encoding: str = "utf-8") -> Path:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding=encoding,
        dir=target_path.parent,
        delete=False,
    ) as temp_file:
        temp_file.write(content)
        temp_path = Path(temp_file.name)
    temp_path.replace(target_path)
    return target_path


def save_submission(submissions_dir: Path, submission_id: str, payload: dict) -> Path:
    target_path = submissions_dir / f"{submission_id}.json"
    written_path = atomic_write_text(
        target_path,
        json.dumps(payload, ensure_ascii=False, indent=2),
    )
    try:
        repo = _repo_for_submissions_dir(submissions_dir)
        repo.save_case(submission_id, payload)
    except Exception:
        pass
    return written_path


def load_submission(submissions_dir: Path, submission_id: str) -> dict | None:
    target_path = submissions_dir / f"{submission_id}.json"
    json_payload: dict | None = None
    if target_path.exists():
        try:
            loaded = json.loads(target_path.read_text(encoding="utf-8-sig"))
            if isinstance(loaded, dict):
                json_payload = loaded
        except (json.JSONDecodeError, OSError):
            json_payload = None

    db_payload: dict | None = None
    try:
        repo = _repo_for_submissions_dir(submissions_dir)
        db_payload = repo.get_case(submission_id)
    except Exception:
        db_payload = None

    if json_payload is not None and db_payload is None:
        try:
            _repo_for_submissions_dir(submissions_dir).save_case(submission_id, json_payload)
        except Exception:
            pass
        return json_payload

    if json_payload is not None and db_payload is not None:
        if json_payload != db_payload:
            try:
                _repo_for_submissions_dir(submissions_dir).save_case(submission_id, json_payload)
            except Exception:
                pass
            return json_payload
        return db_payload

    return db_payload


def save_draft(drafts_dir: Path, submission_id: str, draft_text: str) -> Path:
    target_path = drafts_dir / f"{submission_id}.md"
    return atomic_write_text(target_path, draft_text.strip() + "\n")


def save_review_report(drafts_dir: Path, submission_id: str, review_text: str) -> Path:
    target_path = drafts_dir / f"{submission_id}.review.json"
    return atomic_write_text(target_path, review_text.strip() + "\n")


def save_growth_report(drafts_dir: Path, submission_id: str, growth_text: str) -> Path:
    target_path = drafts_dir / f"{submission_id}.growth.json"
    return atomic_write_text(target_path, growth_text.strip() + "\n")


def load_product_insights(product_insights_path: Path) -> dict[str, Any]:
    if not product_insights_path.exists():
        return {"cases": {}, "updated_at": None}

    try:
        payload = json.loads(product_insights_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"cases": {}, "updated_at": None}

    if not isinstance(payload, dict):
        return {"cases": {}, "updated_at": None}

    cases = payload.get("cases", {})
    if not isinstance(cases, dict):
        cases = {}

    return {
        "cases": cases,
        "updated_at": payload.get("updated_at"),
    }


def save_product_insights(product_insights_path: Path, payload: dict[str, Any]) -> Path:
    return atomic_write_text(
        product_insights_path,
        json.dumps(payload, ensure_ascii=False, indent=2),
    )


def load_product_governance(product_governance_path: Path) -> dict[str, Any]:
    if not product_governance_path.exists():
        return {"decisions": [], "experiments": [], "updated_at": None}

    try:
        payload = json.loads(product_governance_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"decisions": [], "experiments": [], "updated_at": None}

    if not isinstance(payload, dict):
        return {"decisions": [], "experiments": [], "updated_at": None}

    decisions = payload.get("decisions", [])
    experiments = payload.get("experiments", [])
    if not isinstance(decisions, list):
        decisions = []
    if not isinstance(experiments, list):
        experiments = []

    return {
        "decisions": decisions,
        "experiments": experiments,
        "updated_at": payload.get("updated_at"),
    }


def save_product_governance(product_governance_path: Path, payload: dict[str, Any]) -> Path:
    return atomic_write_text(
        product_governance_path,
        json.dumps(payload, ensure_ascii=False, indent=2),
    )


def list_recent_cases(submissions_dir: Path, limit: int = 5) -> list[dict]:
    files = sorted(
        submissions_dir.glob("*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    recent_cases: list[dict] = []
    for path in files[:limit]:
        try:
            case_data = json.loads(path.read_text(encoding="utf-8-sig"))
            if isinstance(case_data, dict):
                recent_cases.append(case_data)
        except json.JSONDecodeError:
            continue
    if recent_cases:
        return recent_cases
    try:
        return _repo_for_submissions_dir(submissions_dir).list_cases(limit=limit)
    except Exception:
        return []


def load_runtime_state(runtime_state_path: Path) -> dict[str, Any]:
    if runtime_state_path.exists():
        try:
            payload = json.loads(runtime_state_path.read_text(encoding="utf-8-sig"))
            if isinstance(payload, dict):
                return {
                    "user_sessions": payload.get("user_sessions", {}) or {},
                    "chat_sessions": payload.get("chat_sessions", {}) or {},
                }
        except (json.JSONDecodeError, OSError):
            pass

    try:
        return _repo_for_state_path(runtime_state_path).load_sessions()
    except Exception:
        return {"user_sessions": {}, "chat_sessions": {}}


def save_runtime_state(
    runtime_state_path: Path,
    user_sessions: dict[int, dict[str, Any]],
    chat_sessions: dict[int, list[dict[str, str]]],
) -> Path:
    serialized = {
        "user_sessions": {str(user_id): session for user_id, session in user_sessions.items()},
        "chat_sessions": {str(user_id): history for user_id, history in chat_sessions.items()},
    }
    written = atomic_write_text(
        runtime_state_path,
        json.dumps(serialized, ensure_ascii=False, indent=2),
    )
    try:
        _repo_for_state_path(runtime_state_path).save_sessions(user_sessions, chat_sessions)
    except Exception:
        pass
    return written
