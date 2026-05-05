# HERMES-20260505-005: Russian Text and Copy Cleanup (DRAFT)

Task ID: `HERMES-20260505-005`
Status: `draft`
Owner: `Codex + Hermes (review)`
Agent: `Codex`
Priority: `P1`
Deadline: `2026-05-07 18:00 MSK`

## Objective

Убрать английские вкрапления из клиентского интерфейса бота: заменить «Premium Wellness Dossier» на русский эквивалент, исправить CTA-тексты, перевести DOSSIER_DRAFT_PROMPT на русский.

## Context

- `WellnessBot/ai_drafting.py`: строки 91, 143-154, 329.
- `WellnessBot/prompts.py`: строки 231-402 (DOSSIER_DRAFT_PROMPT).

## Allowed Scope

**Можно менять:** `WellnessBot/ai_drafting.py`, `WellnessBot/prompts.py`.
**Нельзя менять:** `.env`, `WellnessBot/data/`, логику, main.py.

## Changes

### 1. ai_drafting.py — замена «Premium Wellness Dossier»
- Строка 91: `"premium wellness dossier"` → `"премиальное досье"`
- Строка 151-154: `CTA_DEFAULT_TEXT` → полный русский текст
- Строка 329: маркер `"premium wellness dossier"` → `"премиальное досье"`

### 2. prompts.py — перевод DOSSIER_DRAFT_PROMPT
- Перевести тело промпта (строки 231-402) на русский язык.
- Сохранить JSON-ключи как есть (на английском).
- Сохранить бренды (Сибирское здоровье, Vitamax, HelloDoc) как есть.

## Acceptance Criteria

- Ни одного «Premium Wellness Dossier» в клиентских текстах.
- DOSSIER_DRAFT_PROMPT на русском, JSON-ключи на английском.
- Все CTA-тексты на русском.
