from __future__ import annotations

from pathlib import Path
from typing import Any

from storage import load_submission, save_submission


def build_submission_payload(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "submission_id": session["submission_id"],
        "offer": session["offer"],
        "profile": {
            "telegram_user_id": session["telegram_user_id"],
            "telegram_username": session.get("telegram_username"),
            "telegram_full_name": session.get("telegram_full_name"),
            "full_name": session.get("full_name"),
            "age": session.get("age"),
            "city": session.get("city"),
            "anthropometrics": session.get("anthropometrics"),
            "contact": session.get("contact"),
        },
        "medical_context": {
            "symptoms": session.get("symptoms"),
            "wellbeing_energy": session.get("wellbeing_energy"),
            "complaint_pattern": session.get("complaint_pattern"),
            "goal": session.get("goals"),
            "work_lifestyle": session.get("work_lifestyle"),
            "nutrition": session.get("nutrition"),
            "food_behavior": session.get("food_behavior"),
            "digestion": session.get("digestion"),
            "sleep_stress": session.get("sleep_stress"),
            "activity": session.get("activity"),
            "female_hormones": session.get("female_hormones"),
            "hormonal_reproductive_context": session.get("female_hormones"),
            "emotional_stress": session.get("emotional_stress"),
            "background": session.get("background"),
            "risk_details": session.get("risk_details"),
            "motivation": session.get("motivation"),
            "red_flags": session.get("red_flags"),
            "lab_notes": session.get("lab_notes"),
        },
        "documents": session.get("documents", []),
        "parsed_biomarkers": session.get("parsed_biomarkers", []),
        "lab_confirmation_status": session.get("lab_confirmation_status"),
        "lab_confirmation_needed": session.get("lab_confirmation_needed", False),
        "pending_biomarker_confirmation": session.get("pending_biomarker_confirmation", []),
        "lab_quality_check": session.get("lab_quality_check"),
        "requires_lab_resubmission": session.get("requires_lab_resubmission", False),
        "vision_analysis": session.get("vision_analysis"),
        "intake_status": "submitted",
        "consent_given": session.get("consent_given", False),
    }


def build_initial_submission_payload(session: dict[str, Any], *, now_iso: str) -> dict[str, Any]:
    submission = build_submission_payload(session)
    submission["intake_status"] = "consent_pending"
    submission["status_updated_at"] = now_iso
    submission["created_at"] = now_iso
    return submission


def save_submission_state(submissions_dir: Path, submission: dict[str, Any]) -> None:
    save_submission(submissions_dir, submission["submission_id"], submission)


def persist_submission_enrichment(
    submissions_dir: Path,
    submission_id: str,
    *,
    now_iso: str,
    **fields: Any,
) -> None:
    submission = load_submission(submissions_dir, submission_id)
    if not submission:
        return

    changed = False
    for key, value in fields.items():
        if value is None:
            continue
        submission[key] = value
        changed = True

    if not changed:
        return

    submission["enrichment_updated_at"] = now_iso
    save_submission_state(submissions_dir, submission)


def update_submission_status(
    submission: dict[str, Any],
    *,
    intake_status: str,
    now_iso: str,
    payment_status: str | None = None,
) -> None:
    submission["intake_status"] = intake_status
    if payment_status is not None:
        submission["payment_status"] = payment_status
    submission["status_updated_at"] = now_iso


def build_session_from_submission(submission: dict[str, Any], user: Any) -> dict[str, Any]:
    profile = submission.get("profile", {})
    medical = submission.get("medical_context", {})
    tier = submission.get("offer") or "premium"
    return {
        "submission_id": submission["submission_id"],
        "offer": tier,
        "tier": tier,
        "step": "done",
        "telegram_user_id": user.id,
        "telegram_username": user.username,
        "telegram_full_name": user.full_name,
        "full_name": profile.get("full_name"),
        "age": profile.get("age"),
        "city": profile.get("city"),
        "anthropometrics": profile.get("anthropometrics"),
        "contact": profile.get("contact"),
        "documents": submission.get("documents", []),
        "symptoms": medical.get("symptoms"),
        "wellbeing_energy": medical.get("wellbeing_energy"),
        "complaint_pattern": medical.get("complaint_pattern"),
        "goals": medical.get("goal"),
        "work_lifestyle": medical.get("work_lifestyle"),
        "nutrition": medical.get("nutrition"),
        "food_behavior": medical.get("food_behavior"),
        "digestion": medical.get("digestion"),
        "sleep_stress": medical.get("sleep_stress"),
        "activity": medical.get("activity"),
        "female_hormones": medical.get("female_hormones"),
        "hormonal_reproductive_context": medical.get("hormonal_reproductive_context") or medical.get("female_hormones"),
        "emotional_stress": medical.get("emotional_stress"),
        "background": medical.get("background"),
        "risk_details": medical.get("risk_details"),
        "motivation": medical.get("motivation"),
        "red_flags": medical.get("red_flags"),
        "lab_notes": medical.get("lab_notes", ""),
        "parsed_biomarkers": submission.get("parsed_biomarkers", []),
        "lab_confirmation_status": submission.get("lab_confirmation_status"),
        "lab_confirmation_needed": submission.get("lab_confirmation_needed", False),
        "pending_biomarker_confirmation": submission.get("pending_biomarker_confirmation", []),
        "lab_quality_check": submission.get("lab_quality_check"),
        "requires_lab_resubmission": submission.get("requires_lab_resubmission", False),
        "consent_given": submission.get("consent_given", False),
    }
