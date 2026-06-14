from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


PRODUCT_OFFERS = {
    "nutri_chat": {
        "name": "Экспресс-аудит «Моя тарелка»",
        "price_rub": 1490,
        "invoice_title": "Экспресс-аудит «Моя тарелка»",
        "invoice_description": "Анализ дневника питания за 3 дня, оценка баланса макронутриентов и питьевого режима от Зинченко Ольги Викторовны.",
    },
    "habits": {
        "name": "Умный куратор: Сопровождение",
        "price_rub": 14900,
        "invoice_title": "Умный куратор: Сопровождение",
        "invoice_description": "Сопровождение питания: ежедневный разбор тарелок по фото/описанию, трекинг привычек от Зинченко Ольги Викторовны.",
    },
    "standard": {
        "name": "Дефицит-чек / Карта симптомов",
        "price_rub": 3900,
        "invoice_title": "Дефицит-чек / Карта симптомов",
        "invoice_description": "Анализ жалоб, симптомов дефицитов, образа жизни, сна, ЖКТ и желчеоттока от Зинченко Ольги Викторовны.",
    },
    "premium": {
        "name": "Персональный Wellness-Паспорт",
        "price_rub": 14900,
        "invoice_title": "Персональный Wellness-Паспорт",
        "invoice_description": "Глубокий разбор анкеты, питания, жалоб и расширенной панели анализов от Зинченко Ольги Викторовны.",
    },
    "vip": {
        "name": "Персональный Wellness-Паспорт",
        "price_rub": 14900,
        "invoice_title": "Персональный Wellness-Паспорт",
        "invoice_description": "Глубокий разбор анкеты, питания, жалоб и расширенной панели анализов от Зинченко Ольги Викторовны.",
    },
    "osipov": {
        "name": "Код Микробиома: ХМС по Осипову",
        "price_rub": 5900,
        "invoice_title": "Код Микробиома: ХМС по Осипову",
        "invoice_description": "Детальный разбор анализа ХМС по Осипову, связь с ЖКТ, питанием и схема поддержки от Зинченко Ольги Викторовны.",
    },
}
PRODUCT_ALIASES = {
    "screening": "nutri_chat",
    "week": "nutri_chat",
    "basic": "standard",
    "month": "standard",
    "premium_wellness_dossier": "standard",
    "full": "premium",
}

def normalize_product_code(raw_code: str | None) -> str:
    code = (raw_code or "standard").strip().lower()
    return PRODUCT_ALIASES.get(code, code if code in PRODUCT_OFFERS else "standard")


def get_product_offer(raw_code: str | None) -> dict[str, Any]:
    code = normalize_product_code(raw_code)
    offer = dict(PRODUCT_OFFERS[code])
    offer["code"] = code
    offer["amount_kop"] = int(offer["price_rub"]) * 100
    return offer


PREMIUM_PRICE_RUB = 14900
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




