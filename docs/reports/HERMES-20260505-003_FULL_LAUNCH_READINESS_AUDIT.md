# HERMES-20260505-003: Full Launch Readiness Audit

Дата: 2026-05-05
Агент: Hermes (Level 1)
Вердикт: **NOT pilot-ready**

---

## 1. Executive Summary

**Вердикт: проект НЕ готов к controlled concierge pilot.**

Обнаружены 4 P0-блокера, каждый из которых самостоятельно останавливает запуск:
1. **Delivery-gate bypass** — досье с вердиктом `needs_revision` уходит клиенту без проверки.
2. **Same-user multi-path drift** — один пользователь имеет 4 параллельные ветки, нет канонического пути.
3. **Mini-app safety drift** — неверные цены и хардкод медицинских findings на публичной поверхности.
4. **Runtime не подтверждён** — бот не evidenced как running, proxy-зависимость хрупкая.

Код бота в части safety-промптов и клиентских текстов — сильный. Русский язык выдержан. Продуктовая линейка в коде соответствует документации. Но gate-логика (доставка клиенту) требует немедленного исправления.

---

## 2. Топ-10 проблем по приоритету

| # | ID | Приоритет | Проблема |
|---|----|-----------|----------|
| 1 | F01 | P0 | Delivery gate: `delivered_to_client` без проверки judge_verdict |
| 2 | F04 | P0 | Runtime: бот не evidenced как running |
| 3 | F03 | P0 | Mini-app: цена 2990₽ + хардкод medical findings |
| 4 | F02 | P0 | Multi-path drift: 4 ветки на одного пользователя |
| 5 | F05 | P1 | Нет manual override audit trail для исключений |
| 6 | F09 | P1 | invoice_payload хардкодит "premium:" для всех продуктов |
| 7 | F06 | P1 | DOSSIER_DRAFT_PROMPT на английском при правиле «только русский» |
| 8 | F07 | P1 | «Premium Wellness Dossier» — английский в русском интерфейсе |
| 9 | F10 | P1 | sanitize_live_reply: только 4 паттерна, модель может обойти |
| 10 | F13 | P2 | Демо-пример недостаточно заметен для конверсии |

---

## 3. P0-блокеры (подробно)

### F01 — Delivery-gate bypass
**Файл:** `WellnessBot/main.py`, строка 1810
**Проблема:** `process_admin_approve` вызывает `update_submission_status(submission, intake_status="delivered_to_client")` без единой проверки `judge_verdict`, `review_signals`, `needs_revision`.
**Риск:** Клиент получает досье, которое внутренний judge оценил как `needs_revision` / `must_rewrite_with_high_caution`. Прецедент уже есть: кейс `20260501T162705Z_1084557944`.
**Решение:** Добавить перед строкой 1810:
```python
judge_verdict = submission.get("review_signals", {}).get("judge_verdict", "")
if judge_verdict in ("needs_revision", "must_rewrite", "must_rewrite_with_high_caution", "reject"):
    if not submission.get("manual_override_note"):
        await bot.answer_callback_query(callback_query.id, "Невозможно отправить: есть неразрешённый вердикт judge. Сначала устраните проблемы или добавьте manual override.")
        return
```

### F04 — Runtime не подтверждён
**Файл:** `WellnessBot/main.py`, `bot.stderr.log`
**Проблема:** Последняя активность бота — 2026-05-03 14:30 MSK. Лог содержит WinError 64 + proxy refusal на 127.0.0.1:12334. Активный процесс Python не обнаружен.
**Риск:** Бот не работает = продукт недоступен. Proxy-зависимость на 127.0.0.1:12334 хрупкая и непрозрачная.
**Решение:** 
1. Определить, обязателен ли локальный proxy (127.0.0.1:12334).
2. Если нет — добавить режим `BOT_PROXY_URL=` (без прокси).
3. Перезапустить бота, провести smoke-тест.
4. Зафиксировать результат в AGENT_CONTEXT_HUB.

### F03 — Mini-app safety drift
**Файл:** `mini-app/index.html` (подтверждено в 24 документах проекта)
**Проблема:** Mini-app показывает цену 2990₽ (официально: 3900/6900/14900). Хардкодит: ferritin, vitamin D, cortisol, LCHF protocol, supplement doses.
**Риск:** Юридический: публичная поверхность с неверными ценами и медицински-подобными выводами. Репутационный: клиент видит расхождение с ботом.
**Решение:** Удалить хардкод. Заменить на безопасный placeholder: «Пример результата будет здесь» с ценами из официальной линейки. Либо подключить backend-fed state.

### F02 — Multi-path drift
**Файл:** `WellnessBot/data/submissions/`
**Проблема:** Пользователь 1084557944 имеет 4 submission:
- `20260501T162705Z_1084557944` — week, delivered (с needs_revision)
- `20260427T173913Z_1084557944` — week, consent_pending (stale)
- `20260425T214914Z_1084557944` — premium, requires_lab_resubmission
- `20260425T212847Z_1084557944` — premium, must_rewrite_with_high_caution
**Риск:** Нет единой правды о клиенте. Оператор путается. Досье могут противоречить друг другу.
**Решение:** 
1. Выбрать 1 канонический путь (текущий delivered week).
2. Остальные пометить archived/stale/evidence_only.
3. Добавить проверку в код: если есть активный paid path → новые заявки только как upgrade.

---

## 4. P1 — важные исправления

| ID | Файл | Проблема | Fix |
|----|------|----------|-----|
| F05 | main.py:1810 | Нет manual override audit trail | Добавить `manual_override_note` + `manual_override_by` |
| F09 | payment_flow.py:57 | `build_invoice_payload` хардкодит "premium:" | Использовать `offer['code']` вместо хардкода |
| F06 | prompts.py:232 | DOSSIER_DRAFT_PROMPT на английском | Перевести на русский |
| F07 | ai_drafting.py:91,329 | «Premium Wellness Dossier» | Заменить на «Премиальное досье» |
| F08 | ai_drafting.py:151 | CTA_DEFAULT_TEXT — английский | Полный русский текст |
| F10 | ai_drafting.py:361 | sanitize_live_reply: 4 паттерна | Расширить паттерны |

---

## 5. P2/P3 — улучшения

**P2 (5):** непрозрачные статусы для админа (F11), пауза после анкеты (F12), слабая видимость демо (F13), длинный демо-пример (F14), зашумлённый pulse log (F15).

**P3 (3):** зависимость от Windows proxy (F16), нет ссылки на hermes_skills в AGENT_CONTEXT_HUB (F17), английский в промптах (F18).

---

## 6. Карта клиентского пути (аудит)

```
/start
  → START_TEXT (✅ хороший, русский, премиальный)
  → PRODUCT_MENU_TEXT (✅ понятная линейка, цены верны)
  → Выбор: Демо | 7 дней | 30 дней | VIP
      ├─ Демо: PRODUCT_EXAMPLES_TEXT (✅ safety framing, ⚠️ длинный)
      ├─ 7 дней: TIER_WEEK_DESC → CONSENT → анкета
      ├─ 30 дней: TIER_PREMIUM_DESC → CONSENT → анкета
      └─ VIP: TIER_VIP_DESC → CONSENT → анкета
  → Анкета (сбор жалоб/питания/сна/стресса/ЖКТ/фона)
  → LABS_GUIDANCE_TEXT (✅ HelloDoc, обработка плохих файлов)
  → MANUAL_HANDOFF_START_TEXT (⚠️ нет ценности кейса — P2 F12)
  → Оплата вручную → админ подтверждает
  → build_dossier_after_payment (✅ payment gate есть)
      → AI draft → judge → growth → PDF
      → Статус: review_priority_* / awaiting_human_review (✅ логика есть)
  → Админ: просмотр → «Одобрить и отправить»
      → process_admin_approve: line 1810
      → ❌ P0: НЕТ ПРОВЕРКИ judge_verdict!
      → delivered_to_client БЕЗУСЛОВНО
  → Клиент получает PDF + 30 дней follow-up
```

---

## 7. Safety-аудит (ключевые находки)

**Сильные стороны:**
- `ETHICS_BLOCK` в prompts.py — исчерпывающий, 14 правил.
- `DOSSIER_JUDGE_PROMPT` — жёсткий внутренний критик.
- `sanitize_live_reply` — есть базовая защита от опасных формулировок.
- `PRODUCT_EXAMPLES_TEXT` — правильный safety framing.
- `CONSENT_TEXT` — присутствует.

**Проблемы:**
- **P0 F01:** Delivery gate отсутствует (см. выше).
- **P1 F10:** sanitize_live_reply покрывает 4 паттерна — узко.
- **P1 F06:** Промпты на английском при правиле «только русский».

---

## 8. UX-аудит (ключевые находки)

**Сильные стороны:**
- Русский язык выдержан в клиентских текстах.
- Премиальный тон: START_TEXT, TIER_PREMIUM_DESC.
- Есть human fallback: OPERATOR_HELP_TEXT.

**Проблемы:**
- **P1 F07/F08:** «Premium Wellness Dossier» — английский термин.
- **P2 F12:** Пауза после анкеты без немедленной ценности.
- **P2 F13:** Демо-пример недостаточно заметен.
- **P2 F11:** Статусы review_priority_* непрозрачны для админа.

---

## 9. Payment/delivery gate аудит

| Gate | Статус | Детали |
|------|--------|--------|
| Досье без оплаты | ✅ Защищён | `is_payment_confirmed_for_dossier` на входе |
| Досье без human review | ❌ P0 | `process_admin_approve` не проверяет judge_verdict |
| needs_revision → клиенту | ❌ P0 | Доставка безусловна |
| Manual override | ❌ P1 | Нет audit trail |
| Multi-path drift | ❌ P0 | 4 ветки на пользователя |
| Проверка суммы | ✅ | `validate_payment_event` проверяет сумму |
| Проверка пользователя | ✅ | `validate_payment_event` проверяет user_id |
| Invoice payload | ⚠️ P1 | Хардкод "premium:" для всех продуктов |

---

## 10. Сверка цен/продуктовой линейки

| Продукт | Документы | payment_flow.py | texts.py | Статус |
|---------|-----------|-----------------|----------|--------|
| Демо | 0 ₽ | — | 0 ₽ | ✅ |
| 7 дней | 3 900 ₽ | 3 900 ₽ | 3 900 ₽ | ✅ |
| 30 дней | 6 900 ₽ | 6 900 ₽ | 6 900 ₽ | ✅ |
| VIP | 14 900 ₽ | 14 900 ₽ | 14 900 ₽ | ✅ |
| Mini-app | — | — | — | ❌ 2 990 ₽ |

**Вывод:** Код бота синхронизирован с документацией по ценам. Mini-app — отдельная проблема (F03).

---

## 11. Growth-аудит

**Что работает:**
- Продуктовая линейка понятна: демо → 7д → 30д → VIP.
- Ценовая лестница логична.
- Есть демо-пример с конкретными гипотезами и планом.
- Есть CTA-стратегия в лайв-чате (select_premium_cta).
- Тон премиальный, не шаблонный.

**Что требует улучшения:**
- **P2 F13:** Демо-пример недостаточно заметен. Клиент должен actively искать кнопку «Пример результата».
- **P2 F14:** Демо длинное (30 строк). Риск потери внимания.
- **P1 F07:** «Premium Wellness Dossier» — английский, снижает восприятие премиальности.
- Проблема из product insights: «Нет четкой разницы между AI-черновиком и персональным разбором специалиста» — цитируется в 5 документах, не решена.
- Конверсия демо → платный продукт не измеряется.

---

## 12. Рекомендованный план на 72 часа

### День 1 (срочно): P0-блокеры
1. **F01:** Добавить delivery gate в `process_admin_approve` (main.py:1810).
2. **F04:** Восстановить runtime бота, убрать proxy-зависимость или подтвердить её необходимость.
3. **F02:** Выбрать канонический путь для пользователя 1084557944, остальные archived.

### День 2: P1-исправления
4. **F05:** Добавить manual override audit trail.
5. **F09:** Исправить invoice_payload (убрать хардкод "premium:").
6. **F07/F08:** Заменить «Premium Wellness Dossier» → «Премиальное досье».

### День 3: P1 + mini-app
7. **F03:** Очистить mini-app: убрать 2990₽ и хардкод medical findings.
8. **F10:** Расширить sanitize_live_reply паттерны.
9. **F06:** Перевести DOSSIER_DRAFT_PROMPT на русский.

---

## 13. Рекомендованный план на 7 дней

| День | Задачи |
|------|--------|
| 1 | F01 (delivery gate) + F04 (runtime) + F02 (multi-path) |
| 2 | F05 (manual override) + F09 (invoice payload) + F07/F08 (русский) |
| 3 | F03 (mini-app) + F10 (sanitize) + F06 (промпты) |
| 4 | Smoke-тест полного цикла: /start → демо → 7д → анкета → оплата → judge → human review → доставка |
| 5 | F11 (админ-уведомления) + F12 (ценность после анкеты) |
| 6 | F13/F14 (демо-пример) + F16 (proxy fallback) |
| 7 | Итоговая проверка pilot-readiness. Запуск 1-го controlled pilot клиента. |

---

## 14. Подготовленные draft task packets

| # | Task ID | Назначение | Статус |
|---|---------|------------|--------|
| 1 | HERMES-20260505-004 | Delivery gate patch | draft |
| 2 | HERMES-20260505-005 | Russian text and copy cleanup | draft |
| 3 | HERMES-20260505-006 | Product price sync (invoice + mini-app) | draft |
| 4 | HERMES-20260505-007 | Client flow UX fix | draft |
| 5 | HERMES-20260505-008 | Launch checklist finalization | draft |

---

## 15. Что Hermes улучшил в своих навыках

1. **Обновлён `project-context-loader.md`:** добавлен пункт «проверить AGENT_CONTEXT_HUB на свежие блокеры» — выяснилось, что это самый информативный документ для быстрого входа.

2. **Обновлён `task-packet-executor.md`:** добавлено правило «если задача требует правки кода — создать draft task packet для Codex, а не править самому».

3. **Обновлён `launch-readiness-checker.md`:** конкретизированы критерии pilot-ready на основе реальных находок этого аудита.

4. **Новый pitfall в навыки:** «Не верь статусу delivered_to_client — всегда проверяй judge_verdict» — добавлен в `wellness-safety-auditor.md`.
