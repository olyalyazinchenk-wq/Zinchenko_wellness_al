# Full Day Operating Cycle

## Когда использовать
При получении задачи на полноценный рабочий день (6-8 часов) с несколькими фазами аудита.

## Входные данные
- Task packet с режимом `full working day`.
- Доступ к проекту (Level 1: read + docs + reports + skills).

## Пошаговый workflow (8 фаз)

### Phase 1: Status Snapshot (30-45 мин)
- Собрать: этап, продуктовая линейка, P0-блокеры, smoke-отчёты.
- Создать: `HERMES-YYYYMMDD-NNN_01_STATUS_SNAPSHOT.md`.

### Phase 2: Client Journey Map (60-90 мин)
- Построить карту: каждый шаг → код, текст, риск, улучшение.
- Создать: `HERMES-YYYYMMDD-NNN_02_CLIENT_JOURNEY_MAP.md`.

### Phase 3: Safety & Compliance Audit (90 мин)
- Проверить: формулировки, красные флаги, human review, delivery gate, PD.
- Создать: `HERMES-YYYYMMDD-NNN_03_SAFETY_COMPLIANCE_AUDIT.md`.

### Phase 4: Product & Growth Audit (60-75 мин)
- Оценить: ценность, отличие, демо, оффер, доверие.
- Создать: `HERMES-YYYYMMDD-NNN_04_PRODUCT_GROWTH_AUDIT.md`.

### Phase 5: Price/Text Sync (60 мин)
- Сверить: документы vs код vs тексты vs UI.
- Создать: `HERMES-YYYYMMDD-NNN_05_PRODUCT_SYNC_AUDIT.md`.

### Phase 6: Backlog + Task Packets (90 мин)
- Master backlog: ID, Priority, Area, Problem, Risk, Fix, Owner, Approval.
- Минимум 8 draft task packets.
- Создать: `HERMES-YYYYMMDD-NNN_06_MASTER_BACKLOG.md`.

### Phase 7: Self-Improvement (45 мин)
- Какие навыки использовались? Что слабое? Что повторялось?
- Обновить навыки. При необходимости — создать новый.
- Создать: `HERMES-YYYYMMDD-NNN_07_SELF_IMPROVEMENT_LOG.md`.

### Phase 8: Final Command Report (45 мин)
- Вердикт, P0/P1/P2/P3, план 72ч/7д, Codex/Olga tasks, риски.
- Создать: `HERMES-YYYYMMDD-NNN_FULL_DAY_COMMAND_REPORT.md`.

## Checkpoints
Каждые 1.5-2 часа — короткий checkpoint в Telegram: что прочитал, что нашёл, главный риск, направление.

## Критерии качества
- Все 8 phase reports созданы.
- Master backlog с разметкой P0-P3.
- ≥8 draft task packets.
- Навыки улучшены по итогам дня.
- Код не тронут.

## Что запрещено
- Пропускать фазы.
- Менять код без approval.
- Создавать лишние файлы вне разрешённого scope.
