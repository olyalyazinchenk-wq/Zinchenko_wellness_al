# HERMES-20260505-004: Delivery Gate Patch (DRAFT)

Task ID: `HERMES-20260505-004`
Status: `draft`
Owner: `Codex`
Agent: `Codex`
Priority: `P0`
Deadline: `2026-05-06 18:00 MSK`

## Objective

Добавить в `WellnessBot/main.py` проверку `judge_verdict` перед отправкой досье клиенту. Заблокировать `delivered_to_client` при `needs_revision`, `must_rewrite`, `must_rewrite_with_high_caution`, `reject` без явного manual override.

## Context

- Файл: `WellnessBot/main.py`, функция `process_admin_approve`, строка 1810.
- Текущее поведение: `update_submission_status(submission, intake_status="delivered_to_client")` вызывается безусловно.
- Проблема: кейс `20260501T162705Z_1084557944` доставлен клиенту с `judge_verdict=needs_revision`.

## Allowed Scope

**Можно менять:** `WellnessBot/main.py` (только функция `process_admin_approve`).
**Нельзя менять:** `.env`, `WellnessBot/data/`, платёжные настройки, VPS/production-конфиги.

## Technical Spec

Добавить ПЕРЕД строкой `update_submission_status(submission, intake_status="delivered_to_client", ...)`:

```python
review_signals = submission.get("review_signals") or {}
judge_verdict = str(review_signals.get("judge_verdict") or "")
blocking_verdicts = {"needs_revision", "must_rewrite", "must_rewrite_with_high_caution", "reject", "fail", "unsafe"}

if judge_verdict in blocking_verdicts:
    manual_override_note = submission.get("manual_override_note")
    manual_override_by = submission.get("manual_override_by")
    if not (manual_override_note and manual_override_by):
        await bot.answer_callback_query(
            callback_query.id,
            f"Невозможно отправить: judge_verdict={judge_verdict}. "
            "Устраните проблемы или добавьте manual override через админ-команду.",
            show_alert=True,
        )
        return
    logger.warning(
        "Delivery override for %s by admin %s: %s",
        submission_id, manual_override_by, manual_override_note,
    )
```

## Acceptance Criteria

- Кнопка «Одобрить и отправить» блокируется при `needs_revision` без override.
- При блокировке админ видит alert с причиной.
- При наличии `manual_override_note` + `manual_override_by` доставка разрешается с логом.
- Существующие delivered-кейсы не ломаются.

## Hard Rules

- Не менять логику оплаты.
- Не менять `.env`.
- Не трогать клиентские данные.
