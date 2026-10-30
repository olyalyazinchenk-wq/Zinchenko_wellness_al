from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from review_gate import compute_file_sha256  # noqa: E402
from storage import save_submission  # noqa: E402


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def redact_submission_id(submission_id: str) -> str:
    parts = str(submission_id).split("_", 1)
    if len(parts) == 2:
        return f"{parts[0]}_<redacted>"
    return "<redacted>"


def create_submissions_backup(submissions_dir: Path, backups_dir: Path) -> Path:
    backups_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = backups_dir / f"{ts}.zip"
    with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if submissions_dir.exists():
            for file_path in sorted(submissions_dir.glob("*.json")):
                zf.write(file_path, arcname=f"submissions/{file_path.name}")
    return backup_path


def evaluate_legacy_candidate(
    submission: dict[str, Any],
    *,
    drafts_dir: Path,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    submission_id = str(submission.get("submission_id") or "").strip()

    internal_review = submission.get("internal_review")
    if isinstance(internal_review, dict):
        verdict = str(internal_review.get("judge_verdict") or "").strip().lower()
        if verdict.startswith("fail"):
            reasons.append(f"judge_verdict={verdict}")

    if bool(submission.get("direct_delivery")):
        review_file = drafts_dir / f"{submission_id}.review.json"
        if not review_file.exists():
            reasons.append("direct_delivery_without_review_json")

    return (len(reasons) == 0, reasons)


def backfill_legacy_releases(
    submissions_dir: Path,
    drafts_dir: Path,
    backups_dir: Path,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    delivered_with_pdf: list[str] = []
    grandfathered: list[str] = []
    already_grandfathered: list[str] = []
    excluded: list[dict[str, Any]] = []
    pending_writes: list[tuple[str, dict[str, Any]]] = []

    now_iso = utc_now_iso()

    if submissions_dir.exists():
        for path in sorted(submissions_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            if not isinstance(data, dict):
                continue

            submission_id = str(data.get("submission_id") or path.stem)
            if data.get("intake_status") != "delivered_to_client":
                continue

            pdf_path_raw = str(data.get("pdf_path") or "").strip()
            if not pdf_path_raw:
                continue
            pdf_path = Path(pdf_path_raw)
            if not pdf_path.exists() or not pdf_path.is_file():
                continue

            delivered_with_pdf.append(submission_id)
            eligible, reasons = evaluate_legacy_candidate(data, drafts_dir=drafts_dir)
            if not eligible:
                excluded.append(
                    {
                        "submission_id": submission_id,
                        "redacted_id": redact_submission_id(submission_id),
                        "offer": data.get("offer") or data.get("tier"),
                        "reasons": reasons,
                    }
                )
                continue

            sha = compute_file_sha256(pdf_path)
            existing = data.get("legacy_release")
            if (
                isinstance(existing, dict)
                and existing.get("artifact_sha256") == sha
                and existing.get("source") == "pre_review_gate"
            ):
                already_grandfathered.append(submission_id)
                continue

            data["legacy_release"] = {
                "grandfathered_at": now_iso,
                "artifact_sha256": sha,
                "source": "pre_review_gate",
            }
            grandfathered.append(submission_id)
            pending_writes.append((submission_id, data))

    backup_path: Path | None = None
    if not dry_run and pending_writes:
        backup_path = create_submissions_backup(submissions_dir, backups_dir)
        for submission_id, payload in pending_writes:
            save_submission(submissions_dir, submission_id, payload)

    return {
        "dry_run": dry_run,
        "delivered_with_pdf_count": len(delivered_with_pdf),
        "grandfathered_count": len(grandfathered),
        "already_grandfathered_count": len(already_grandfathered),
        "excluded_count": len(excluded),
        "grandfathered_redacted": [redact_submission_id(sid) for sid in grandfathered],
        "already_grandfathered_redacted": [
            redact_submission_id(sid) for sid in already_grandfathered
        ],
        "excluded": excluded,
        "backup_path": str(backup_path) if backup_path else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Backfill legacy_release metadata for safe pre-gate delivered reports."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Inspect and print eligible/excluded cases without modifying files.",
    )
    parser.add_argument(
        "--submissions-dir",
        type=Path,
        default=PROJECT_ROOT / "WellnessBot" / "data" / "submissions",
    )
    parser.add_argument(
        "--drafts-dir",
        type=Path,
        default=PROJECT_ROOT / "WellnessBot" / "data" / "drafts",
    )
    parser.add_argument(
        "--backups-dir",
        type=Path,
        default=PROJECT_ROOT / "WellnessBot" / "data" / "backups",
    )
    args = parser.parse_args()

    summary = backfill_legacy_releases(
        args.submissions_dir,
        args.drafts_dir,
        args.backups_dir,
        dry_run=args.dry_run,
    )

    mode_str = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"=== Legacy Releases Backfill ({mode_str}) ===")
    print(f"Delivered with existing PDF : {summary['delivered_with_pdf_count']}")
    print(f"Grandfathered (opened)      : {summary['grandfathered_count']}")
    print(f"Already grandfathered       : {summary['already_grandfathered_count']}")
    print(f"Excluded (for Olga review)  : {summary['excluded_count']}")
    if summary["backup_path"]:
        print(f"Backup archive              : {summary['backup_path']}")

    if summary["grandfathered_redacted"]:
        print("\nOpened cases (de-identified):")
        for item in summary["grandfathered_redacted"]:
            print(f"  + {item}")

    if summary["excluded"]:
        print("\nExcluded cases for Olga review (de-identified):")
        for item in summary["excluded"]:
            reasons_str = ", ".join(item["reasons"])
            print(f"  - {item['redacted_id']} (offer={item['offer']}): {reasons_str}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
