# HERMES-20260505-017: Implement Russian Text Cleanup (DRAFT)

Task ID: `HERMES-20260505-017`
Status: `draft` | Owner: `Codex + Hermes` | Priority: `P1`
Requires: `Codex/Olga approval`

## Objective
«Premium Wellness Dossier» + CTA — английский.

## Scope
**Можно менять:** `ai_drafting.py`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, payment settings, VPS, production, client data.

## Smallest Safe Patch
Замена 3 строк.

## Verification
- Syntax check: `python -m py_compile ai_drafting.py`
- Manual walkthrough: проверить визуально.

## Rollback
`git checkout -- ai_drafting.py`

## Self-Audit Checklist
- [ ] Scope не нарушен
- [ ] Secrets не затронуты
- [ ] Client data не затронуты
- [ ] Diff минимален
- [ ] Rollback задокументирован

## Approval
Требуется: Codex/Olga approval перед реализацией.
