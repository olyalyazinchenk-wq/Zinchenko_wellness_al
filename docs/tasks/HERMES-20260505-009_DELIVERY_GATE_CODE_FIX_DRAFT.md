# HERMES-20260505-009: Delivery Gate Code Fix (DRAFT)
Task ID: `HERMES-20260505-009` | Status: `draft` | Owner: `Codex` | Priority: `P0`
Requires: `Codex/Olga approval` | Files: `WellnessBot/main.py:1810`

## Objective
Добавить guard: не доставлять досье клиенту при judge_verdict `needs_revision`/`must_rewrite`/`reject` без manual override.

## Fix (main.py, перед строкой 1810)
```python
review_signals = submission.get("review_signals") or {}
judge_verdict = str(review_signals.get("judge_verdict") or "")
if judge_verdict in {"needs_revision","must_rewrite","must_rewrite_with_high_caution","reject","fail","unsafe"}:
    if not (submission.get("manual_override_note") and submission.get("manual_override_by")):
        await bot.answer_callback_query(callback_query.id, f"Блок: judge_verdict={judge_verdict}", show_alert=True)
        return
```

## Acceptance
- [ ] judge_verdict блокирует доставку
- [ ] manual_override_note разрешает доставку с логом
- [ ] Существующие delivered-кейсы не ломаются
