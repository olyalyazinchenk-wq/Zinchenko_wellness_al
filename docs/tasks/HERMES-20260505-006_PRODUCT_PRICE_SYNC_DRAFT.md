# HERMES-20260505-006: Product Price Sync (DRAFT)

Task ID: `HERMES-20260505-006`
Status: `draft`
Owner: `Codex`
Agent: `Codex`
Priority: `P1`
Deadline: `2026-05-07 18:00 MSK`

## Objective

Исправить две проблемы с синхронизацией цен:
1. `build_invoice_payload` хардкодит `"premium:"` для всех продуктов — исправить на динамический `offer['code']`.
2. Mini-app показывает 2990₽ — заменить на безопасный placeholder с официальными ценами.

## Context

- `WellnessBot/payment_flow.py`: строка 57.
- `mini-app/index.html`: весь файл.

## Allowed Scope

**Можно менять:** `WellnessBot/payment_flow.py`, `mini-app/index.html`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, main.py.

## Changes

### 1. payment_flow.py:57
```python
# Было:
def build_invoice_payload(submission_id: str, telegram_user_id: int) -> str:
    return f"premium:{submission_id}:{telegram_user_id}"

# Стало:
def build_invoice_payload(submission_id: str, telegram_user_id: int, offer_code: str = "premium") -> str:
    return f"{offer_code}:{submission_id}:{telegram_user_id}"
```
Обновить вызов в `build_payment_context` (строка 91): передать `offer['code']`.

### 2. mini-app/index.html
- Убрать все упоминания цены 2990₽.
- Убрать хардкод ferritin/vitamin D/cortisol/supplement doses/LCHF.
- Заменить на безопасный placeholder:
```
Цены: 3 900 ₽ / 6 900 ₽ / 14 900 ₽
Пример результата: [безопасный демо-пример из texts.py]
```

## Acceptance Criteria

- Invoice payload содержит правильный offer_code (week/premium/vip).
- Mini-app не показывает 2990₽.
- Mini-app не содержит медицинских findings.
