# Price Policy And YooKassa Card

Date: 2026-04-21
Owner: Olga / Wellness Bot

## 2026-04-26 Update

This document described the earlier single-flagship policy.

Current product decision is now documented in:

- `docs/PRODUCT_LINE_V2_20260426.md`

New active commercial ladder:

- Демо-пример результата: `0 ₽` at pilot stage
- Разбор на 7 дней: `3 900 ₽`
- Персональный разбор на 30 дней: `6 900 ₽`
- VIP-сопровождение на 30 дней: `14 900 ₽`

Important: the old `6900 ₽` rule remains valid only for the `premium` / 30-day product. It is no longer the only product price.

## Current Marketing Policy

Current product policy is:

- one flagship paid offer,
- premium and delicate positioning,
- trust-first funnel from free clarity to paid deep work,
- no medical diagnosis claims,
- service format: `нутрициологическая навигация`.

The project should not be presented as a marketplace of many random services.
The main paid product remains:

`Premium Wellness Dossier`

Free layer:

`Wellness Clarity in Telegram`

Paid layer:

`Premium Wellness Dossier`

This keeps the sales path simple:

1. Client gets first clarity in Telegram.
2. Client sees that a deeper structured review is needed.
3. Client moves into the paid flagship offer.

## Current Price Synced With Product Code

The price currently hardcoded in the bot is:

- `6900 ₽`

Technical source of truth:

- [payment_flow.py](C:\Users\HP\Desktop\Новая папка\WellnessBot\payment_flow.py:5)

If the price in YooKassa differs from the price in the bot code, payments may fail validation.

So right now the safe synchronized launch price is:

- `6900 ₽`

## What The Client Is Buying

Product name:

`Premium Wellness Dossier`

Short Russian client-facing explanation:

`Персональный нутрициологический разбор в Telegram с бережной навигацией по жалобам, образу жизни, питанию и анализам без постановки диагноза.`

Expanded explanation:

`Клиент получает структурированный премиальный разбор: общую картину, возможные дефицитные риски и перегружающие факторы, ориентиры по питанию и образу жизни, рекомендации по добавкам при уместности, а также список вопросов, которые стоит обсудить с врачом.`

## Ready Card For YooKassa

Use this as the base pricing card.

Service / product name:

`Premium Wellness Dossier`

Price:

`6900 ₽`

Quantity:

`1`

Payment amount:

`6900 ₽`

Category / essence:

`Услуга`

Short description for the checkout:

`Персональный нутрициологический разбор в Telegram: жалобы, питание, образ жизни, анализы, возможные дефицитные риски и следующий шаг.`

Safer version if a shorter label is needed:

`Нутрициологический разбор и персональная навигация`

## Recommended Public Offer Wording

Do say:

- `нутрициологическая навигация`
- `персональный разбор`
- `премиальный структурированный разбор`
- `анализ жалоб, питания, образа жизни и анализов`
- `возможные дефицитные риски`
- `следующий шаг`
- `что стоит обсудить с врачом`

Do not say in the payment card:

- `диагностика`
- `лечение`
- `назначение терапии`
- `лечим щитовидку`
- `лечим анемию`
- `ставим диагноз`

## Recommended Commercial Framing

The paid promise should sound like this:

`Не диагноз и не лечение, а понятный персональный нутрициологический разбор, который помогает увидеть общую картину и понять следующий шаг.`

This is currently the best-fit commercial framing for the project:

- premium,
- personal,
- safe,
- legally cleaner,
- aligned with the current content strategy.

## Suggested Internal Price Policy

At the current stage, the cleanest policy is:

- one flagship price,
- no price ladder inside the bot yet,
- no multiple confusing packages before pilot,
- first prove conversion on one clear paid offer.

So for the current soft-launch stage:

- Free: first clarity in Telegram
- Paid flagship: `Premium Wellness Dossier — 6900 ₽`

Future upsell ideas may exist later, but they should not be added to YooKassa or the bot flow until the current single-offer conversion is proven.

## Recommended Price Ladder

Recommended commercial ladder:

- soft launch / pilot: `6900 ₽`
- after first validated cases and reviews: `9900 ₽`

Current recommended active price:

- `6900 ₽`

## Important Sync Rule

Before changing the public price, update both:

1. YooKassa product price
2. [payment_flow.py](C:\Users\HP\Desktop\Новая папка\WellnessBot\payment_flow.py:5)

Otherwise Telegram payment validation may reject the payment because the expected amount is checked in code.

## What I Recommend Entering Right Now

If YooKassa asks for a price and a product card right now, enter:

Name:

`Premium Wellness Dossier`

Description:

`Персональный нутрициологический разбор в Telegram: жалобы, питание, образ жизни, анализы, возможные дефицитные риски и следующий шаг.`

Price:

`6900 ₽`

Quantity:

`1`

Format:

`Услуга`

## Important Legal Note

Fields related to taxes, VAT / НДС, legal entity data, and fiscalization must match Olga's real legal setup.
Those fields should not be guessed from product strategy alone.
