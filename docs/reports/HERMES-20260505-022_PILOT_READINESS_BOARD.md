# Pilot Readiness Board

## Must pass before pilot (P0)

| # | Критерий | Статус | Owner | Verification |
|---|----------|--------|-------|-------------|
| 1 | Delivery gate: judge_verdict блокирует доставку | ✅ Fixed (Codex 17a7174) | Codex | Smoke: needs_revision → блок |
| 2 | Бот запущен и отвечает | ✅ Running | Codex | /start → ответ за < 5 сек |
| 3 | Оплата ручная: клиент видит реквизиты | ? | Codex | Live-test Ольги |
| 4 | OCR/file fallback: 5 сценариев работают | ❌ (401 risk) | Codex | Smoke: все 5 сценариев |
| 5 | Досье генерируется (AI draft → judge → PDF) | ✅ Smoke OK | Codex | Complex dossier smoke |
| 6 | Human review перед delivery | ✅ Gate есть | Codex | Smoke: approve flow |
| 7 | Один канонический путь на клиента | ❌ | Codex | Проверить multi-path |
| 8 | Русский язык во всех клиентских текстах | ⚠️ Частично | Hermes/Codex | Поиск: нет английского |

## Should pass before pilot (P1)

| # | Критерий | Статус | Owner |
|---|----------|--------|-------|
| 9 | Manual override с audit trail | ? | Codex |
| 10 | sanitize_live_reply ≥ 10 паттернов | ❌ | Codex |
| 11 | CONSENT с timestamp | ❌ | Codex |
| 12 | Invoice payload без хардкода | ✅ Fixed (17a7174) | Codex |
| 13 | CTA без английского | ✅ Fixed (17a7174) | Codex |
| 14 | Возрастной gate в анкете | ❌ | Codex |
| 15 | Демо-пример ≤ 15 строк, виден сразу | ❌ | Hermes |

## Can wait until after first pilot (P2/P3)

| # | Критерий | Owner |
|---|----------|-------|
| 16 | Mini-app cleanup (2990₽) | Codex |
| 17 | Privacy policy на домене | Olga |
| 18 | Сайт-витрина на Beget | Codex |
| 19 | Статусы review_priority_* → читаемые | Codex |
| 20 | Админ-уведомления с judge summary | Codex |
| 21 | DOSSIER_DRAFT_PROMPT → русский | Hermes→Codex |

## Open risks

| Риск | Уровень | Владелец |
|------|---------|----------|
| OCR 401 Unauthorized — нестабильное распознавание | P0 | Codex |
| Multi-path drift — путаница состояний | P0 | Codex |
| Runtime resilience — бот может упасть | P1 | Codex |
| PD non-compliance — нет privacy policy | P1 | Olga |
| Нет домена/лендинга — низкое доверие при оплате | P1 | Olga |
