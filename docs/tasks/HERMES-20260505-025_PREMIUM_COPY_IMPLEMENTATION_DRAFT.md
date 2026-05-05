# HERMES-20260505-025: Premium Copy Implementation (DRAFT)
Status: `draft` | Priority: `P1` | Owner: `Hermes (copy) → Codex (apply)`

## Problem
Часть клиентских текстов устарела или отсутствует. Нужны готовые премиальные тексты для всего пути.

## Scope
**Можно:** `WellnessBot/texts.py`.
**Нельзя:** логику, безопасность, оплату.

## Source
Тексты: `docs/reports/HERMES-20260505-022_PREMIUM_CLIENT_COPY_PACK.md`

## Changes
Применить 13 текстовых блоков из Copy Pack в соответствующие переменные texts.py.

## Verification
- Все тексты на русском.
- Нет «Premium Wellness Dossier».
- Нет диагнозов/лечения.
- Каждый текст ведёт к следующему действию.
