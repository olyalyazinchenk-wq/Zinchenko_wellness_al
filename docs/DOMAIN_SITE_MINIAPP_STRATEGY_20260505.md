# Domain, Site, Mini App Strategy — 2026-05-05

## Короткий вывод

Google AI Studio repo `olyalyazinchenk-wq/moy-projekt` — это не backend и не готовый сайт продаж. Это React/Vite UI-прототип `WellnessPro MVP`, который показывает будущий кабинет клиента и рабочее место эксперта: очередь заявок, review workspace, клиентское мобильное превью, safety auditor, настройки и архив досье.

Домен Beget нужен, но не как первый технический шаг для Telegram-бота. Домен нужен для:

1. Публичного сайта/лендинга Ольги.
2. HTTPS-адреса Telegram Mini App.
3. Юридических страниц: политика, согласие, оферта/условия.
4. Доверия при оплате и прохождении модераций/проверок.
5. Будущего размещения админки, если она будет выноситься из локального компьютера.

Но сам бот Telegram может работать и без домена. Сейчас главный продуктовый канал остается Telegram-first.

## Что фактически есть сейчас

### Main project: `Zinchenko_wellness_al`

Реальный backend и рабочая логика находятся в `WellnessBot`:

- Telegram bot runtime;
- анкета;
- загрузка файлов;
- ручная оплата;
- генерация AI/dossier draft;
- human review;
- safety rules;
- локальное хранение данных;
- тесты и ops-скрипты.

Это главный продуктовый репозиторий и источник правды.

### Google AI Studio repo: `moy-projekt`

Последний проверенный commit: `63fe6d1 feat: Improve layout and responsiveness`.

Стек:

- React 19;
- Vite;
- TypeScript;
- Tailwind CSS 4;
- motion;
- lucide-react;
- recharts;
- `@google/genai` присутствует как dependency, но приложение в текущем виде работает на mock data.

Ключевые файлы:

- `src/App.tsx` — переключение вкладок;
- `src/components/Sidebar.tsx` — навигация;
- `src/components/ClientAppMock.tsx` — клиентский мобильный сценарий;
- `src/components/ReviewWorkspace.tsx` — рабочее место эксперта;
- `src/components/SafetyAuditor.tsx` — визуальный аудитор безопасности;
- `src/components/CaseList.tsx` — очередь кейсов;
- `src/components/ClientsList.tsx` — список клиентов;
- `src/components/DossiersList.tsx` — архив досье;
- `src/components/Overview.tsx` — dashboard;
- `src/data.ts` — mock cases;
- `src/types.ts` — типы кейсов/профилей/досье.

## Что `moy-projekt` НЕ является

Не backend.

Не готовая production mini-app.

Не медицинский источник правды.

Не безопасный клиентский текст для прямой публикации.

Не замена `WellnessBot`.

Не место для хранения реальных клиентских анализов и персональных данных.

## Что из `moy-projekt` полезно взять

1. Визуальную идею кабинета клиента.
2. Идею экспертного review workspace.
3. Идею safety auditor как отдельной панели перед отправкой клиенту.
4. Очередь кейсов и фильтры по статусам.
5. Архив досье.
6. Мобильную структуру client journey: welcome -> survey -> labs -> payment -> processing -> ready.

## Что нельзя переносить как есть

1. Mock-клиентов и Telegram ID.
2. Медицински уверенные формулировки из `src/data.ts`.
3. Hardcoded findings вроде ferritin/vitamin D как будто это реальный результат.
4. Supplement/dose-like wording без проверки.
5. Любые цены, если они расходятся с официальной линейкой.
6. Оплату через YooKassa как готовую, пока в основном боте принят `PAYMENT_MODE=manual`.

## Роль домена Beget

Домен лучше использовать поэтапно.

### Этап 1: публичный сайт

Домен ведёт на сайт-витрину:

- кто такая Ольга;
- что такое нутрициологическая навигация;
- линейка продуктов: 3 900 / 6 900 / 14 900 ₽;
- пример результата;
- безопасность: не диагноз, не лечение;
- кнопка перехода в Telegram bot;
- юридические документы.

Это можно сделать раньше, чем полноценный mini-app.

### Этап 2: mini-app URL

Mini App должен иметь HTTPS URL. Домен дает нормальный адрес, например:

- `https://domain.ru/app` — клиентский Telegram Mini App;
- `https://domain.ru/admin` — закрытая экспертная панель;
- `https://domain.ru/legal/privacy` — политика;
- `https://domain.ru/legal/consent` — согласие;
- `https://domain.ru/legal/offer` — оферта/условия.

### Этап 3: production backend

Когда бот переезжает на VPS, домен может указывать на сервер:

- сайт;
- mini-app;
- webhook/API;
- админка;
- безопасное файловое хранилище.

## Рекомендуемая архитектура

### Сейчас, для пилота

- Telegram bot остается главным продуктом.
- Оплата ручная.
- Human review обязателен.
- Домен используется для сайта и юридических страниц.
- Mini-app не должен принимать реальные персональные данные, пока не решена безопасная backend-архитектура.

### Ближайшая production-схема

```
Домен Beget
  -> landing / legal pages
  -> /app Telegram Mini App frontend
  -> /admin expert dashboard frontend

VPS
  -> WellnessBot backend
  -> API for app/admin
  -> file storage rules
  -> logs / backups

Telegram Bot
  -> entry point
  -> messages, files, payment handoff
  -> opens Mini App when needed
```

## Что делать с сайтом

Сайт нужен раньше mini-app.

Причина: сайт решает коммерческую и доверительную задачу, а mini-app решает интерфейсную задачу.

Сайт должен отвечать клиенту:

- что это;
- кому подходит;
- сколько стоит;
- почему безопасно;
- как выглядит результат;
- как начать;
- куда переходить в Telegram.

Минимальный сайт можно сделать как статический landing без базы данных.

## Что делать с mini-app

Mini-app нужен, но не как первая публикация `moy-projekt` на домен.

Правильная роль mini-app:

1. Клиентский кабинет:
   - анкета;
   - загрузка файлов;
   - статус разбора;
   - готовое досье;
   - follow-up в течение периода продукта.

2. Экспертная админка:
   - очередь заявок;
   - просмотр анкеты и файлов;
   - AI draft;
   - safety auditor;
   - approve/send;
   - история клиента.

На первом шаге лучше делать не весь `moy-projekt`, а вырезать из него безопасный client preview и expert review dashboard как две отдельные роли.

## Важное решение

Не переносить `moy-projekt` в основной продукт целиком.

Правильнее:

1. Взять дизайн и компоненты как reference.
2. Переписать mock data на безопасные placeholder-данные.
3. Убрать hardcoded medical findings.
4. Подключить к backend только после delivery-gate и runtime stability.
5. Разделить клиентский mini-app и админку.

## Что нужно от Ольги по домену

Нужно прислать только безопасную информацию:

- доменное имя;
- где куплено: Beget;
- скрин/текст текущих DNS-записей, без паролей;
- есть ли хостинг на Beget или куплен только домен;
- хочет ли Ольга, чтобы основной адрес открывал сайт или сразу Telegram mini-app.

Не нужно присылать:

- пароль Beget;
- паспортные данные;
- платежные данные;
- токены;
- API keys.

Если понадобится доступ, лучше использовать временный доступ/делегирование, а не отправку пароля в чат.

## Пошаговый план

### Шаг 1. Зафиксировать домен

Получить от Ольги доменное имя и понять, куплен только домен или домен + хостинг.

### Шаг 2. Сделать безопасную карту сайта

Страницы:

- `/` — лендинг;
- `/app` — будущий Telegram Mini App;
- `/legal/privacy`;
- `/legal/consent`;
- `/legal/offer`;
- `/contacts`.

### Шаг 3. Очистить mini-app truth drift

В текущем `mini-app` и Google AI Studio прототипе убрать:

- неправильные цены;
- hardcoded diagnosis-like findings;
- supplement/dose-like demo results;
- mock Telegram IDs;
- “Оплатить через YooKassa” как будто это уже работает.

### Шаг 4. Сделать landing first

Разместить на домене простой безопасный сайт с CTA в Telegram bot.

### Шаг 5. Сделать safe demo mini-app

На `/app` разместить безопасное demo-превью без реальных данных:

- как выглядит анкета;
- как выглядит статус разбора;
- пример результата без диагноза/лечения;
- кнопка “перейти в Telegram”.

### Шаг 6. Потом подключать backend

Только после:

- стабильного bot runtime;
- delivery-gate fix;
- canonical paid path;
- safe data storage decision;
- защиты admin-доступа.

## Итоговое решение

Домен нужен.

Но сначала домен использовать для сайта и юридической базы, а не сразу для полноценной mini-app с реальными данными.

`moy-projekt` использовать как дизайн и UX-прототип для будущего кабинета, но не как production-приложение.

Основной продукт остается `WellnessBot`.

Следующий лучший шаг: получить доменное имя и DNS-информацию Beget, затем подготовить безопасный landing + `/app` placeholder, после чего подключать Telegram Mini App через BotFather.
