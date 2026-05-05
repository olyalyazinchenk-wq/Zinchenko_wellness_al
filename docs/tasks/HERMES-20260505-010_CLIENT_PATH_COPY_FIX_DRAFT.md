# HERMES-20260505-010: Client Path & Copy Fix (DRAFT)
Task ID: `HERMES-20260505-010` | Status: `draft` | Owner: `Codex + Hermes (review)` | Priority: `P1`
Requires: `Codex/Olga approval` | Files: `texts.py, ai_drafting.py`

## Changes
1. **«Premium Wellness Dossier» → «Персональное досье»** (ai_drafting.py:91,151,329)
2. **CTA_DEFAULT_TEXT** → полный русский (ai_drafting.py:151)
3. **Демо-пример** — сократить до 12 строк, CTA после (texts.py:32)
4. **«Кто такая Ольга»** — 3 строки в START_TEXT
5. **После анкеты** — 1-2 строки инсайта в MANUAL_HANDOFF_START_TEXT

## Acceptance
- [ ] Ни одного английского термина в клиентских текстах
- [ ] Демо ≤ 15 строк
- [ ] После анкеты клиент видит ценность
