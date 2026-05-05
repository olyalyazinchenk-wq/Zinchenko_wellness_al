# HERMES-20260505-007: Client Flow UX Fix (DRAFT)

Task ID: `HERMES-20260505-007`
Status: `draft`
Owner: `Codex`
Agent: `Codex`
Priority: `P2`
Deadline: `2026-05-08 18:00 MSK`

## Objective

Улучшить клиентский опыт в трёх точках:
1. Демо-пример — сделать заметнее (выше в меню или inline-кнопка).
2. После анкеты — показать немедленную ценность кейса.
3. Админ-уведомления — добавить выжимку из judge-отчёта.

## Context

- `WellnessBot/texts.py`: PRODUCT_MENU_TEXT, MANUAL_HANDOFF_START_TEXT.
- `WellnessBot/main.py`: notify_admins (строка 2276).

## Allowed Scope

**Можно менять:** `WellnessBot/texts.py`, `WellnessBot/main.py` (notify_admins).
**Нельзя менять:** `.env`, `WellnessBot/data/`, оплату, delivery gate.

## Changes

### 1. Демо-пример — повысить видимость
- В PRODUCT_MENU_TEXT добавить жирную inline-кнопку «👀 Посмотреть пример за 15 секунд».
- Или: после START_TEXT сразу показывать демо с кнопкой «Дальше к выбору формата».

### 2. Ценность после анкеты
- В MANUAL_HANDOFF_START_TEXT добавить 1-2 строки: «По вашей анкете мы уже видим: [ключевой инсайт]. Разбор поможет...»

### 3. Админ-уведомления
- В notify_admins добавить после статуса краткую выжимку: топ-3 проблемы из judge-отчёта (если есть).

## Acceptance Criteria

- Демо-пример виден на первом экране без скролла.
- После анкеты клиент понимает, что его кейс уже в работе.
- Админ видит ключевые проблемы досье в уведомлении.
