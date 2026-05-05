# HERMES-20260505-019: Implement Delivery Gate (DRAFT)

Task ID: `HERMES-20260505-019`
Status: `draft` | Owner: `Codex + Hermes` | Priority: `P0`
Requires: `Codex/Olga approval`

## Objective
delivered_to_client без проверки judge_verdict.

## Scope
**Можно менять:** `main.py:1810`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, payment settings, VPS, production, client data.

## Smallest Safe Patch
15 строк guard + manual override.

## Verification
- Syntax check: `python -m py_compile main.py:1810`
- Manual walkthrough: проверить визуально.

## Rollback
`git checkout -- main.py:1810`

## Self-Audit Checklist
- [ ] Scope не нарушен
- [ ] Secrets не затронуты
- [ ] Client data не затронуты
- [ ] Diff минимален
- [ ] Rollback задокументирован

## Approval
Требуется: Codex/Olga approval перед реализацией.
