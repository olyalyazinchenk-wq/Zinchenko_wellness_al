# HERMES-20260505-003: Full Findings Table

| ID | Priority | Area | File/Source | Problem | Risk | Recommended Fix | Needs Code | Owner |
|----|----------|------|-------------|---------|------|-----------------|------------|-------|
| F01 | P0 | Delivery Gate | WellnessBot/main.py:1810 | `process_admin_approve` ставит `delivered_to_client` без проверки `judge_verdict`. `needs_revision` / `must_rewrite` не блокируют отправку. | Клиент получает небезопасное досье с известными проблемами качества. | Добавить guard: если `judge_verdict in ('needs_revision','must_rewrite','reject')` и нет manual override — блокировать доставку. | YES | Codex |
| F02 | P0 | Client Data | WellnessBot/main.py:587, WellnessBot/data/ | Один пользователь (1084557944) имеет 4 активные ветки: доставленный week, stale week, 2 premium. Нет enforcement «один канонический путь». | Путаница состояний, риск двойной выдачи, потеря целостности кейса. | Добавить проверку: если есть активный paid path → новые заявки только как upgrade/продолжение. Старые ветки пометить archived/stale. | YES | Codex |
| F03 | P0 | Mini-app | mini-app/index.html (подтверждено в 24 документах) | Mini-app показывает цену 2990 ₽ (официально: 3900/6900/14900), хардкодит ferritin/vitamin D/cortisol/supplement/LCHF. | Клиент видит неверные цены и медицински-подобные выводы. Юридический риск. | Заменить хардкод на безопасный placeholder или reviewed backend-fed state. Цены привести к 3900/6900/14900. | YES | Codex |
| F04 | P0 | Runtime | WellnessBot/main.py, bot.stderr.log | Бот не evidenced как running. Последний лог — WinError 64 + proxy refusal 127.0.0.1:12334 (2026-05-03). | Нет работающего бота = нет продукта. Proxy-зависимость хрупкая. | Выяснить, обязателен ли proxy. Если нет — добавить no-proxy fallback. Восстановить polling. Провести post-fix verification. | YES | Codex |
| F05 | P1 | Safety | WellnessBot/main.py:1810 (то же место) | Нет явного manual override механизма: админ нажимает «Одобрить» → доставка безусловна, даже при `needs_revision`. | Отсутствие audit trail для исключений. Непонятно, кто и почему разрешил доставку проблемного досье. | Добавить explicit `manual_override_note` + `manual_override_by` при доставке вопреки judge. Логировать в submission JSON. | YES | Codex |
| F06 | P1 | Safety | WellnessBot/prompts.py:232 | `DOSSIER_DRAFT_PROMPT` написан на английском, хотя правило «только русский» повторяется внутри промпта 15+ раз. | Внутренняя непоследовательность. Модель может путаться с языком вывода. | Перевести DOSSIER_DRAFT_PROMPT и DOSSIER_JUDGE_PROMPT на русский. | YES | Hermes (draft) → Codex |
| F07 | P1 | UX/Russian | WellnessBot/ai_drafting.py:91,151,329 | «Premium Wellness Dossier» — английский термин в русском интерфейсе. | Снижает восприятие премиальности для русскоязычного клиента. | Заменить на «Премиальное досье» или «Персональное досье». | YES | Codex |
| F08 | P1 | UX/Russian | WellnessBot/ai_drafting.py:151-152 | CTA_DEFAULT_TEXT: «Я запущу Premium Wellness Dossier в этом чате.» — смесь русского и английского. | Неряшливый тон для премиум-продукта. | Полный русский: «Я запущу премиальное досье в этом чате.» | YES | Codex |
| F09 | P1 | UX | WellnessBot/payment_flow.py:57 | `build_invoice_payload` хардкодит префикс `"premium:"` для ВСЕХ продуктов, включая week и vip. | Технический долг: week-клиент получает invoice с premium-префиксом. | Использовать `offer['code']` вместо хардкода `"premium"`. | YES | Codex |
| F10 | P1 | Safety | WellnessBot/ai_drafting.py:361-384 | `sanitize_live_reply` обрабатывает только 4 жёстких паттерна. Новые unsafe-формулировки модели пройдут мимо. | Модель может выдать опасный текст в новых формулировках. | Расширить набор паттернов. Добавить обобщённые regex: «у вас X» → «это может быть похоже на X». | YES | Codex |
| F11 | P2 | UX | WellnessBot/main.py:2254-2265 | После генерации досье статусы `review_priority_*` для админа непрозрачны: админ видит «нужен реворк», но не понимает, что именно править. | Замедляет human review, повышает риск пропуска проблем. | Добавить в админ-уведомление краткую выжимку из judge-отчёта: топ-3 проблемы. | YES | Codex |
| F12 | P2 | UX | WellnessBot/texts.py:112-118 | `MANUAL_HANDOFF_START_TEXT`: клиент после анкеты получает сообщение об оплате, но не видит немедленной ценности своего кейса. | Пауза в клиентском опыте, риск отвала. | Добавить в сообщение: «Вот что мы уже видим по вашей анкете: [краткий инсайт].» | YES | Codex |
| F13 | P2 | Growth | Весь проект | Нет A/B-показа демо-примера до анкеты. Клиент должен сам найти кнопку «Пример результата». | Низкая конверсия демо → платный продукт. | Сделать демо-пример первым экраном после /start или inline-кнопкой «Посмотреть пример за 15 секунд». | YES | Codex |
| F14 | P2 | Growth | WellnessBot/texts.py:32-61 | Демо-пример качественный, но длинный (30 строк). | Клиент может не дочитать до CTA. | Сократить до 12-15 строк, сделать кнопку «Хочу такой же разбор» сразу после примера. | NO | Hermes (draft) |
| F15 | P2 | Docs | docs/PROJECT_PULSE_LOG.md | Pulse log ~1800 строк. Много повторяющихся блоков от регулярных синхронизаций. | Затрудняет быстрый вход в контекст. Зашумляет реальные изменения. | Дедуплицировать повторяющиеся блоки. Оставить только дельты. | NO | Hermes |
| F16 | P3 | Tech | WellnessBot/config.py:189 | `read_windows_system_proxy()` — бот зависит от системного прокси Windows. | Хрупкая зависимость, не работает на VPS/Linux. | Добавить `BOT_PROXY_URL` как основной источник, системный прокси — как fallback с явным логом. | YES | Codex |
| F17 | P3 | Docs | docs/AGENT_CONTEXT_HUB.md | Нет упоминания системы навыков Гермеса (`docs/hermes_skills/`). | Следующий агент не узнает о существовании навыков. | Добавить ссылку на `docs/hermes_skills/index.md` в раздел «Context For New Model». | NO | Hermes |
| F18 | P3 | Safety | WellnessBot/prompts.py:22 | `DOSSIER_DRAFT_PROMPT` начинается с английской инструкции, затем 15+ раз требует русский язык. | Модель получает противоречивый сигнал. | Убрать весь английский из промптов (кроме JSON-ключей и брендов). | NO | Hermes (draft) |

## Summary

- **P0:** 4 (F01-F04)
- **P1:** 6 (F05-F10)
- **P2:** 5 (F11-F15)
- **P3:** 3 (F16-F18)
- **Total:** 18
- **Need code change:** 13
- **Docs-only:** 5
