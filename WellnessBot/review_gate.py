from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def compute_file_sha256(path: str | Path) -> str:
    file_path = Path(path)
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_matches(submission: dict[str, Any], record: dict[str, Any]) -> bool:
    if not isinstance(submission, dict) or not isinstance(record, dict):
        return False

    record_path_raw = str(record.get("artifact_path") or "").strip()
    submission_path_raw = str(submission.get("pdf_path") or "").strip()
    if record_path_raw and submission_path_raw:
        if Path(record_path_raw) != Path(submission_path_raw):
            return False

    expected_sha = str(record.get("artifact_sha256") or "").strip().lower()
    if expected_sha:
        target_path_raw = submission_path_raw or record_path_raw
        if not target_path_raw:
            return False
        target_path = Path(target_path_raw)
        if not target_path.exists() or not target_path.is_file():
            return False
        if compute_file_sha256(target_path).lower() != expected_sha:
            return False

    return True


def is_release_approved(submission: dict[str, Any] | None) -> bool:
    if not isinstance(submission, dict):
        return False

    review_records = submission.get("review_records")
    if isinstance(review_records, list) and review_records:
        last = review_records[-1]
        if not isinstance(last, dict):
            return False
        return last.get("decision") == "approved" and _artifact_matches(submission, last)

    # legacy: кейсы, одобренные админом до внедрения review_records
    if (
        submission.get("intake_status") == "delivered_to_client"
        and submission.get("approved_by_admin_id")
    ):
        return True

    legacy_release = submission.get("legacy_release")
    if isinstance(legacy_release, dict):
        expected_sha = str(legacy_release.get("artifact_sha256") or "").strip().lower()
        pdf_path_raw = str(submission.get("pdf_path") or "").strip()
        if expected_sha and pdf_path_raw:
            pdf_path = Path(pdf_path_raw)
            if pdf_path.exists() and pdf_path.is_file():
                if compute_file_sha256(pdf_path).lower() == expected_sha:
                    return True
        return False

    auto_decision = submission.get("auto_delivery_decision")
    if isinstance(auto_decision, dict):
        return bool(auto_decision.get("allow_automatic_delivery"))

    return False


def is_report_owner_or_admin(
    submission: dict[str, Any] | None,
    requester_id: int,
    *,
    is_admin_user: bool = False,
) -> bool:
    if not isinstance(submission, dict):
        return False
    owner_id = int((submission.get("profile") or {}).get("telegram_user_id") or 0)
    if owner_id == int(requester_id) and owner_id != 0:
        return True
    return bool(is_admin_user)


def list_user_approved_reports(submissions_dir: Path, user_id: int) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    if not submissions_dir.exists():
        return reports
    for path in submissions_dir.glob(f"*_{user_id}.json"):
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            owner_id = int((data.get("profile") or {}).get("telegram_user_id") or 0)
            pdf_path = data.get("pdf_path")
            if (
                owner_id == int(user_id)
                and is_release_approved(data)
                and pdf_path
                and Path(pdf_path).exists()
            ):
                reports.append(data)
        except Exception:
            continue
    reports.sort(
        key=lambda r: r.get("status_updated_at") or r.get("created_at") or "",
        reverse=True,
    )
    return reports
