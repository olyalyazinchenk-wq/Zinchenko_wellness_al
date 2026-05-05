# HERMES-20260505-023: Canonical Client Path Fix (DRAFT)
Status: `draft` | Priority: `P0` | Owner: `Codex`

## Problem
Один пользователь может иметь несколько активных submission. Нет enforcement «один канонический путь».

## Scope
**Можно:** `WellnessBot/main.py`, `WellnessBot/case_service.py`.
**Нельзя:** `.env`, data, payment, VPS, client data.

## Smallest Safe Patch
1. При создании нового intake → `list_recent_cases(user_id)`.
2. Если есть delivered → переключить в follow-up mode.
3. Если есть pending → спросить: продолжить или новый.
4. Старые submission → `archived` статус.

## Verification
- /start при delivered кейсе → follow-up, не новый intake.
- /start при pending → вопрос «продолжить?».
