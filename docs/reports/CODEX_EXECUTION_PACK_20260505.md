# Codex Execution Pack — 2026-05-05

## P0 Fixes: READY NOW (copy-paste → commit)

---

### FIX 1: Delivery Gate (P0, main.py:1810, 15 мин)

**Проблема:** досье уходит клиенту без проверки judge_verdict.
**Файл:** `WellnessBot/main.py`, найти строку 1810.

**Заменить:**
```python
    update_submission_status(submission, intake_status="delivered_to_client", now_iso=utc_now_iso())
    submission["delivered_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, submission)
```

**На:**
```python
    # Delivery gate: check judge verdict before delivery
    review_signals = submission.get("review_signals") or {}
    judge_verdict = str(review_signals.get("judge_verdict") or "")
    blocking = {"needs_revision", "must_rewrite", "must_rewrite_with_high_caution", "reject", "fail", "unsafe"}
    if judge_verdict in blocking:
        override_note = submission.get("manual_override_note")
        override_by = submission.get("manual_override_by")
        if not (override_note and override_by):
            await bot.answer_callback_query(callback_query.id,
                f"Блок: judge_verdict={judge_verdict}. Устраните проблемы или добавьте manual override.", show_alert=True)
            return
        logger.warning("Delivery override for %s by %s: %s", submission_id, override_by, override_note)
        submission["manual_override_applied_at"] = utc_now_iso()
    update_submission_status(submission, intake_status="delivered_to_client", now_iso=utc_now_iso())
    submission["delivered_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, submission)
```

**Проверка:** попробовать одобрить досье с `judge_verdict=needs_revision` → должно заблокировать.

---

### FIX 2: Invoice Payload Hardcode (P1, payment_flow.py:57, 5 мин)

**Проблема:** все invoice имеют префикс "premium:", даже week и vip.
**Файл:** `WellnessBot/payment_flow.py`

**Заменить строку 57:**
```python
def build_invoice_payload(submission_id: str, telegram_user_id: int) -> str:
    return f"premium:{submission_id}:{telegram_user_id}"
```

**На:**
```python
def build_invoice_payload(submission_id: str, telegram_user_id: int, offer_code: str = "premium") -> str:
    return f"{offer_code}:{submission_id}:{telegram_user_id}"
```

**Строка 91 — заменить:**
```python
"invoice_payload": build_invoice_payload(session["submission_id"], telegram_user_id),
```
**На:**
```python
"invoice_payload": build_invoice_payload(session["submission_id"], telegram_user_id, offer_code=offer["code"]),
```

**Также строка 65 — заменить:**
```python
if len(parts) != 3 or parts[0] != "premium":
```
**На:**
```python
if len(parts) != 3:
```

---

### FIX 3: Russian Text (P1, ai_drafting.py, 5 мин)

**Файл:** `WellnessBot/ai_drafting.py`

**Строка 91 — заменить:**
```python
    "premium wellness dossier",
```
**На:**
```python
    "премиальное досье",
```

**Строка 329 — заменить:**
```python
    if contains_any(normalized, ("premium wellness dossier", "premium", "досье", "в какой момент становится нужен")):
```
**На:**
```python
    if contains_any(normalized, ("премиальное досье", "премиум", "досье", "в какой момент становится нужен")):
```

**Строки 151-154 — заменить CTA_DEFAULT_TEXT:**
```python
CTA_DEFAULT_TEXT = (
    "\n\nЕсли решите идти глубже, напишите: «хочу разбор». "
    "Я запущу структурированное персональное досье в этом чате."
)
```
*(было: "Premium Wellness Dossier")*

---

## Priority Order

1. Fix 1 (delivery gate) — 15 min
2. Fix 2 (invoice) — 5 min  
3. Fix 3 (Russian text) — 5 min
4. Restore bot runtime — 2-4 hours
5. Mini-app cleanup — 30 min

Все диффы минимальны: 1-3 строки замены каждый.
