# Post-Fix Verification Board

## Что уже исправлено Codex (commit 17a7174)

| # | Fix | Файл | Статус |
|---|-----|------|--------|
| 1 | Delivery gate: judge_verdict блокирует доставку | main.py:1810 | ✅ fixed |
| 2 | Invoice payload: динамический offer_code | payment_flow.py:57,91 | ✅ fixed |
| 3 | Русский CTA: «Premium Wellness Dossier» → русский | ai_drafting.py:151 | ✅ fixed |

## Как проверить (без реального клиента)

### Delivery gate
- [ ] Создать тестовый submission с `review_signals.judge_verdict = "needs_revision"`
- [ ] Админ нажимает «Одобрить и отправить» → БЛОКИРОВКА
- [ ] Alert: «Блок: judge_verdict=needs_revision»
- [ ] Добавить `manual_override_note` + `manual_override_by` → ОК, доставка

### Invoice payload
- [ ] Создать week-кейс → invoice_payload начинается с "week:"
- [ ] Создать premium-кейс → invoice_payload начинается с "premium:"
- [ ] Создать vip-кейс → invoice_payload начинается с "vip:"

### Русский CTA
- [ ] Поиск по `ai_drafting.py`: нет "Premium Wellness Dossier"
- [ ] Поиск по коду: нет английских CTA-фраз

## Существующие smoke-тесты

| Тест | Файл | Статус |
|------|------|--------|
| Payment/case flow | SMOKE_PAYMENT_CASE_20260421.md | ✅ SMOKE_OK |
| Admin/governance/digest | SMOKE_ADMIN_GOVERNANCE_20260421.md | ✅ SMOKE_OK |
| Complex dossier | упоминается в STRATEGY_V2 | ✅ прошёл ранее |

## Нужны ещё smoke-тесты

| Тест | Зачем | Owner |
|------|-------|-------|
| Delivery gate smoke | Подтвердить блокировку при needs_revision | Codex |
| OCR fallback smoke | Подтвердить все 5 сценариев из playbook | Codex + Olga |
| Full client walkthrough | /start → демо → 7д → анкета → оплата → досье → доставка | Olga |

## Что проверить в live-тесте Ольги

1. `/start` → демо-пример показывается
2. Выбор «7 дней» → анкета без зависаний
3. Загрузка PDF с анализами → biomarkers найдены
4. Загрузка плохого фото → fallback-сообщение
5. Ручная оплата → реквизиты видны
6. Админ подтверждает → досье генерируется
7. Judge verdict → доставка блокируется при needs_revision
8. Досье → клиент получает PDF + сообщение
9. 30 дней follow-up → принимаются новые сообщения
