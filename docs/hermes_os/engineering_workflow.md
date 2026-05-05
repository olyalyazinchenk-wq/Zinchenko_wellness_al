# Engineering Workflow

## Цикл: Анализ → Архитектура → Реализация → Проверка

### 1. Analysis (Read-only)
- Понять проблему: файл, строка, риск.
- Классифицировать: P0-P3.
- Определить scope.

### 2. Architecture (Design)
- Минимальный патч: что изменить, куда, зачем.
- Проверить: не затронет ли соседние модули.
- Оценить риски изменения.

### 3. Implementation (Code)
- Только по approved implementation packet.
- Маленький diff. Одно изменение за раз.
- После: syntax check.

### 4. Verification
- Smoke test (если доступен).
- Manual walkthrough.
- Self-audit.

### Rollback
- Всегда документировать, как откатить изменение.
- `git diff` перед коммитом.

## Запрещено без отдельного approval
- Менять архитектуру.
- Трогать payment/VPS/production.
- Удалять файлы.
- Большие рефакторинги.
