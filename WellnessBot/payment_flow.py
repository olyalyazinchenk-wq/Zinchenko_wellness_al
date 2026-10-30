from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nutriok_product import (
    LEGACY_PRODUCT_ALIASES,
    PRODUCT_OFFERS as NUTRIOK_PRODUCT_OFFERS,
    normalize_product_code as normalize_nutriok_product_code,
)

PRODUCT_OFFERS = {
    code: {
        "name": offer.name,
        "price_rub": offer.pilot_price_rub,
        "regular_price_rub": offer.regular_price_rub,
        "invoice_title": offer.name,
        "invoice_description": offer.result,
    }
    for code, offer in NUTRIOK_PRODUCT_OFFERS.items()
}
PRODUCT_ALIASES = {
    **LEGACY_PRODUCT_ALIASES,
    "month": "ok_review",
    "premium_wellness_dossier": "ok_review",
}

def normalize_product_code(raw_code: str | None) -> str:
    code = str(raw_code or "ok_review").strip().lower()
    return PRODUCT_ALIASES.get(code, normalize_nutriok_product_code(code))


def get_product_offer(raw_code: str | None) -> dict[str, Any]:
    code = normalize_product_code(raw_code)
    offer = dict(PRODUCT_OFFERS[code])
    offer["code"] = code
    offer["amount_kop"] = int(offer["price_rub"]) * 100
    return offer


def is_adult_age(age: Any) -> bool:
    if isinstance(age, bool):
        return False
    if isinstance(age, (int, float)):
        return int(age) >= 18
    digits = "".join(character for character in str(age or "") if character.isdigit())
    return bool(digits) and int(digits[:3]) >= 18


PREMIUM_PRICE_RUB = PRODUCT_OFFERS["ok_result_8"]["price_rub"]
PREMIUM_PRICE_KOPECKS = PREMIUM_PRICE_RUB * 100
PAYMENT_STATUS_PAID = "paid"
PAYMENT_STATUS_MANUAL_PENDING = "manual_payment_pending"
PAYMENT_STATUS_MANUAL_CONFIRMED = "manual_payment_confirmed"
PAYMENT_STATUSES_CONFIRMED_FOR_DOSSIER = {
    PAYMENT_STATUS_PAID,
    PAYMENT_STATUS_MANUAL_CONFIRMED,
}


def build_invoice_payload(submission_id: str, telegram_user_id: int, offer_code: str = "standard") -> str:
    normalized_offer_code = normalize_product_code(offer_code)
    return f"{normalized_offer_code}:{submission_id}:{telegram_user_id}"


def parse_invoice_payload(payload: str | None) -> tuple[str | None, int | None]:
    if not payload:
        return None, None

    parts = payload.split(":")
    raw_offer_code = parts[0].strip().lower() if parts else ""
    if len(parts) != 3 or raw_offer_code not in {*PRODUCT_OFFERS, *PRODUCT_ALIASES}:
        return None, None

    submission_id = parts[1].strip() or None
    try:
        telegram_user_id = int(parts[2].strip())
    except (TypeError, ValueError):
        return submission_id, None
    return submission_id, telegram_user_id


def build_payment_context(
    session: dict[str, Any],
    *,
    now_iso: str,
) -> dict[str, Any]:
    telegram_user_id = int(session["telegram_user_id"])
    offer = get_product_offer(session.get("offer") or session.get("tier"))
    return {
        "offer_code": offer["code"],
        "offer_name": offer["name"],
        "invoice_title": offer["invoice_title"],
        "invoice_description": offer["invoice_description"],
        "amount_rub": offer["price_rub"],
        "amount_kop": offer["amount_kop"],
        "currency": "RUB",
        "invoice_payload": build_invoice_payload(
            session["submission_id"],
            telegram_user_id,
            offer_code=offer["code"],
        ),
        "invoice_sent_at": now_iso,
        "expected_telegram_user_id": telegram_user_id,
    }


def validate_payment_event(
    submission: dict[str, Any],
    *,
    telegram_user_id: int,
    invoice_payload: str | None,
    currency: str,
    total_amount: int,
) -> str | None:
    payment_context = submission.get("payment_context") or {}
    expected_payload = str(payment_context.get("invoice_payload") or "")
    expected_currency = str(payment_context.get("currency") or "RUB")
    expected_amount = int(payment_context.get("amount_kop") or 0)
    expected_user_id = int(
        payment_context.get("expected_telegram_user_id")
        or submission.get("profile", {}).get("telegram_user_id")
        or 0
    )

    if not expected_payload:
        return "В кейсе отсутствует payment context."
    if invoice_payload != expected_payload:
        return "Payload оплаты не совпадает с ожидаемым кейсом."
    if currency != expected_currency:
        return "Валюта оплаты не совпадает с ожидаемой."
    if total_amount != expected_amount:
        return "Сумма оплаты не совпадает с ожидаемой."
    if telegram_user_id != expected_user_id:
        return "Пользователь оплаты не совпадает с владельцем кейса."
    return None


def is_payment_confirmed_for_dossier(submission: dict[str, Any]) -> bool:
    return str(submission.get("payment_status") or "") in PAYMENT_STATUSES_CONFIRMED_FOR_DOSSIER


def mark_manual_payment_pending(
    submission: dict[str, Any],
    *,
    now_iso: str,
    reason: str,
) -> None:
    submission["intake_status"] = PAYMENT_STATUS_MANUAL_PENDING
    submission["payment_status"] = PAYMENT_STATUS_MANUAL_PENDING
    submission["manual_payment_pending_at"] = now_iso
    submission["manual_payment_reason"] = reason
    submission["status_updated_at"] = now_iso


def mark_manual_payment_confirmed(
    submission: dict[str, Any],
    *,
    now_iso: str,
    admin_user_id: int,
    note: str | None = None,
) -> None:
    submission["intake_status"] = PAYMENT_STATUS_MANUAL_CONFIRMED
    submission["payment_status"] = PAYMENT_STATUS_MANUAL_CONFIRMED
    submission["manual_payment_confirmed_at"] = now_iso
    submission["manual_payment_confirmed_by"] = admin_user_id
    if note:
        submission["manual_payment_note"] = note
    submission["status_updated_at"] = now_iso




