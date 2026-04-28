from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from case_service import (  # noqa: E402
    build_session_from_submission,
    build_submission_payload,
    persist_submission_enrichment,
    save_submission_state,
    update_submission_status,
)
from payment_flow import (  # noqa: E402
    PREMIUM_PRICE_KOPECKS,
    PREMIUM_PRICE_RUB,
    build_payment_context,
    build_invoice_payload,
    parse_invoice_payload,
    validate_payment_event,
)
from storage import load_submission  # noqa: E402


def main() -> int:
    smoke_dir = BOT_DIR / "data" / "smoke_payment_case"
    submissions_dir = smoke_dir / "submissions"
    uploads_dir = smoke_dir / "uploads"
    drafts_dir = smoke_dir / "drafts"
    for directory in (smoke_dir, submissions_dir, uploads_dir, drafts_dir):
        directory.mkdir(parents=True, exist_ok=True)

    for path in submissions_dir.glob("*.json"):
        path.unlink()

    session = {
        "submission_id": "smoke_case_payment_001",
        "offer": "premium",
        "tier": "premium",
        "telegram_user_id": 1084557944,
        "telegram_username": "Olgazinchenko1186",
        "telegram_full_name": "Ольга",
        "full_name": "Ольга",
        "age": 40,
        "city": "Москва",
        "contact": "telegram_current_chat",
        "symptoms": "Выпадение волос, усталость, ломкие ногти",
        "goals": "Получить понятный нутрициологический разбор и план следующего шага",
        "background": "Принимаю селен и белок",
        "red_flags": "Нет",
        "lab_notes": "Анализы пока не приложены",
        "documents": [],
        "consent_given": True,
        "parsed_biomarkers": [],
        "vision_analysis": None,
    }

    submission = build_submission_payload(session)
    update_submission_status(
        submission,
        intake_status="awaiting_payment",
        now_iso="2026-04-21T00:25:00Z",
        payment_status="awaiting_payment",
    )
    submission["payment_context"] = build_payment_context(
        session,
        now_iso="2026-04-21T00:25:00Z",
    )
    save_submission_state(submissions_dir, submission)

    good_payment_error = validate_payment_event(
        submission,
        telegram_user_id=session["telegram_user_id"],
        invoice_payload=submission["payment_context"]["invoice_payload"],
        currency="RUB",
        total_amount=PREMIUM_PRICE_KOPECKS,
    )
    wrong_amount_error = validate_payment_event(
        submission,
        telegram_user_id=session["telegram_user_id"],
        invoice_payload=submission["payment_context"]["invoice_payload"],
        currency="RUB",
        total_amount=100,
    )
    wrong_user_error = validate_payment_event(
        submission,
        telegram_user_id=999999,
        invoice_payload=submission["payment_context"]["invoice_payload"],
        currency="RUB",
        total_amount=PREMIUM_PRICE_KOPECKS,
    )

    persist_submission_enrichment(
        submissions_dir,
        submission["submission_id"],
        now_iso="2026-04-21T00:26:00Z",
        parsed_biomarkers=[{"marker": "Ferritin", "value": "22"}],
        vision_analysis="Клиент прислал фото анализов, нужен ручной follow-up.",
    )
    enriched_submission = load_submission(submissions_dir, submission["submission_id"])
    assert enriched_submission is not None

    update_submission_status(
        enriched_submission,
        intake_status="paid",
        now_iso="2026-04-21T00:27:00Z",
        payment_status="paid",
    )
    save_submission_state(submissions_dir, enriched_submission)

    restored_session = build_session_from_submission(
        enriched_submission,
        SimpleNamespace(
            id=session["telegram_user_id"],
            username=session["telegram_username"],
            full_name=session["telegram_full_name"],
        ),
    )

    parsed_submission_id, parsed_user_id = parse_invoice_payload(
        build_invoice_payload(session["submission_id"], session["telegram_user_id"])
    )

    report_lines = [
        "# Smoke Report: Payment / Case Flow",
        "",
        "## Scope",
        "- built a fresh submission payload from session data",
        "- moved it through awaiting_payment -> enrichment -> paid state",
        "- validated payment checks for good and bad scenarios",
        "- restored a chat session from stored submission state",
        "",
        "## Payment Context",
        "```json",
        json.dumps(submission["payment_context"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Validation Results",
        f"- good_payment_error: {good_payment_error}",
        f"- wrong_amount_error: {wrong_amount_error}",
        f"- wrong_user_error: {wrong_user_error}",
        "",
        "## Enriched Submission",
        "```json",
        json.dumps(enriched_submission, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Restored Session",
        "```json",
        json.dumps(restored_session, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Invoice Roundtrip",
        f"- payload_submission_id: {parsed_submission_id}",
        f"- payload_user_id: {parsed_user_id}",
        f"- premium_price_rub: {PREMIUM_PRICE_RUB}",
        f"- premium_price_kop: {PREMIUM_PRICE_KOPECKS}",
    ]

    report_path = PROJECT_ROOT / "docs" / "SMOKE_PAYMENT_CASE_20260421.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    print("SMOKE_OK")
    print(f"report={report_path}")
    print(f"stored_submission={submissions_dir / (submission['submission_id'] + '.json')}")
    print(f"restored_session_step={restored_session.get('step')}")
    print(f"payment_validation_good={good_payment_error}")
    print(f"payment_validation_wrong_amount={wrong_amount_error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
