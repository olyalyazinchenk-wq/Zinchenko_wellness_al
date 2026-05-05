# HERMES-20260505-018: Implement Product Price Sync (DRAFT)

Task ID: `HERMES-20260505-018`
Status: `draft` | Owner: `Codex + Hermes` | Priority: `P1`
Requires: `Codex/Olga approval`

## Objective
invoice_payload хардкод + mini-app 2990₽.

## Scope
**Можно менять:** `payment_flow.py, mini-app/index.html`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, payment settings, VPS, production, client data.

## Smallest Safe Patch
1 параметр + удаление хардкода.

## Verification
- Syntax check: `python -m py_compile payment_flow.py`
- Manual walkthrough: проверить визуально.

## Rollback
`git checkout -- payment_flow.py, mini-app/index.html`

## Self-Audit Checklist
- [ ] Scope не нарушен
- [ ] Secrets не затронуты
- [ ] Client data не затронуты
- [ ] Diff минимален
- [ ] Rollback задокументирован

## Approval
Требуется: Codex/Olga approval перед реализацией.
