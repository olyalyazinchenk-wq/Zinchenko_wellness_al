# HERMES-20260505-020: Implement Client Next Actions (DRAFT)

Task ID: `HERMES-20260505-020`
Status: `draft` | Owner: `Codex + Hermes` | Priority: `P2`
Requires: `Codex/Olga approval`

## Objective
Демо длинное, нет инсайта после анкеты.

## Scope
**Можно менять:** `texts.py`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, payment settings, VPS, production, client data.

## Smallest Safe Patch
Сокращение + 2 строки.

## Verification
- Syntax check: `python -m py_compile texts.py`
- Manual walkthrough: проверить визуально.

## Rollback
`git checkout -- texts.py`

## Self-Audit Checklist
- [ ] Scope не нарушен
- [ ] Secrets не затронуты
- [ ] Client data не затронуты
- [ ] Diff минимален
- [ ] Rollback задокументирован

## Approval
Требуется: Codex/Olga approval перед реализацией.
