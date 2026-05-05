# HERMES-20260505-021: Implement Launch Checklist (DRAFT)

Task ID: `HERMES-20260505-021`
Status: `draft` | Owner: `Codex + Hermes` | Priority: `P2`
Requires: `Codex/Olga approval`

## Objective
Формализация критериев pilot-ready.

## Scope
**Можно менять:** `docs/reports/`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, payment settings, VPS, production, client data.

## Smallest Safe Patch
Чек-лист + AGENT_CONTEXT_HUB update.

## Verification
- Syntax check: `python -m py_compile docs/reports/`
- Manual walkthrough: проверить визуально.

## Rollback
`git checkout -- docs/reports/`

## Self-Audit Checklist
- [ ] Scope не нарушен
- [ ] Secrets не затронуты
- [ ] Client data не затронуты
- [ ] Diff минимален
- [ ] Rollback задокументирован

## Approval
Требуется: Codex/Olga approval перед реализацией.
