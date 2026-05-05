# Implementation Gate Protocol

## 7 ворот перехода от аудита к реализации

### Gate 1: Problem Clarity
Проблема конкретна, проверяема, воспроизводима.
❌ «Улучшить UX» → ✅ «main.py:1810 — delivery без проверки judge_verdict»

### Gate 2: Risk Class
P0/P1/P2/P3 определён.
P0 = блокирует pilot/public launch немедленно.

### Gate 3: Scope
Указаны КОНКРЕТНЫЕ файлы и строки, которые можно менять.

### Gate 4: Forbidden Scope
Указано, что нельзя трогать: `.env`, data, payment, VPS.

### Gate 5: Minimal Patch
Самый маленький полезный фикс. Не «переписать модуль», а «добавить 5 строк».

### Gate 6: Verification
Есть команда или способ проверки: syntax check, smoke test, manual walkthrough.

### Gate 7: Approval
Есть явный approved task/implementation packet от Codex/Olga.

## Правило
Если хотя бы одних ворот нет → НЕ реализуй. Создай draft packet.
