# Canonical Case Collapse — 2026-05-30

Статус: applied
Основание: Ольга подтвердила продуктовые решения по пилоту.

## Подтвержденные продуктовые решения

1. Главный вход в пилот: `7-дневный разбор за 1 000 руб.`
2. Premium `6 900 руб.`: продолжение/апгрейд после первичного кейса, не параллельная новая ветка.
3. VIP: только вручную, не массовая продажа в пилоте.
4. Mini-app: не публичный продукт сейчас; только макет/будущий кабинет.
5. Главный клиентский результат: `PDF-досье + короткое Telegram-сообщение с первыми действиями`.

## Каноническое решение по live-relevant веткам одного пользователя

### Canonical

`20260501T162705Z_1084557944`

- offer: `week`
- payment_status: `manual_payment_confirmed`
- intake_status: `delivery_blocked_needs_revision`
- review: `needs_revision`
- lab truth: `requires_lab_resubmission = true`

Решение:

- это единственный канонический оплаченный вход в пилот;
- кейс остается заблокированным до выравнивания review truth и lab truth;
- нельзя считать его успешной доставкой;
- следующий operator action: привести анализы/досье в безопасное состояние или явно оставить блок.

### Merge / continuation

`20260505T131604Z_1084557944`

- offer: `premium`
- payment_status: `manual_payment_confirmed`
- intake_status: `review_priority_quality_and_market`
- review: `pass_with_minor_edits`, но есть market/quality rework flags

Решение:

- это не второй активный клиентский путь;
- это continuation/upgrade evidence к canonical week case;
- оператор должен решить: зачесть как апгрейд/продолжение после исправления canonical кейса или временно держать parked до закрытия week truth;
- нельзя запускать новый отдельный premium delivery, пока canonical week заблокирован.

### Parked duplicate

`20260514T213116Z_1084557944`

- offer: `premium`
- intake_status до решения: `consent_pending`
- consent_given: `false`
- медицинских данных и оплаты нет

Решение:

- parked duplicate;
- не является воронкой, продажей или прогрессом;
- не должен отображаться как активная ветка клиента;
- статус в JSON обновлен на `parked_duplicate_consent_pending`.

## Что внесено в данные

В три JSON-кейса добавлено поле `canonical_path`:

- `canonical_case_id`
- `canonical_role`
- `canonical_status`
- `decision`
- `decided_at`
- `decided_by`
- `rule`

Это audit metadata. Данные клиента не удалялись.

## Почему это устраняет топтание

До решения проект мог одновременно считать успешными/активными:

- week-вход;
- premium-ветку;
- новый premium restart.

Это ломало ощущение результата: непонятно, что продаем, что доставляем и какой кейс главный.

После решения:

- один canonical case;
- premium только continuation;
- duplicate parked;
- pilot entry остается week-first.

## Следующий шаг

Следующий proof шаг:

`live e2e walkthrough`

Проверить руками в Telegram:

1. `/start`
2. выбор 7-дневного разбора
3. анкета
4. анализы: PDF / фото / ручной ввод
5. ручная оплата
6. admin review
7. delivery gate
8. досье не уходит без review

Критерий прохождения:

- нет второго активного кейса для того же пользователя;
- путь не создает новую premium-ветку;
- клиентский текст соответствует week-first пилоту;
- результат остается human-reviewed.