# HERMES-20260505-012: Safety Prompt Hardening (DRAFT)
Task ID: `HERMES-20260505-012` | Status: `draft` | Owner: `Codex + Hermes` | Priority: `P1`
Requires: `Codex/Olga approval` | Files: `prompts.py, ai_drafting.py`

## Changes
1. **DOSSIER_DRAFT_PROMPT** — перевести на русский (prompts.py:231-402)
2. **sanitize_live_reply** — расширить паттерны:
   - «у вас X» → «это может быть похоже на X»
   - «вам нужно Y» → «можно обсудить Y»
   - «принимайте Z» → «не начинайте самостоятельный приём Z»
3. **DOSSIER_JUDGE_PROMPT** — перевести на русский (prompts.py:405-476)

## Acceptance
- [ ] Все промпты на русском (кроме JSON-ключей)
- [ ] sanitize_live_reply покрывает ≥10 паттернов
