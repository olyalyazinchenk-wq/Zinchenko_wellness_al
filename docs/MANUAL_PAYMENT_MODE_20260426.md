# Manual Payment Mode

Date: 2026-04-26
Status: active pilot decision

## Decision

Because YooKassa / Telegram payment activation is unstable or may reject the flow, the bot now uses manual payment mode as the official pilot mode.

Current setting:

`PAYMENT_MODE=manual`

This means:

- the bot does not try to open a Telegram invoice even if a `PAYMENT_TOKEN` exists;
- after the client completes the questionnaire, the case is saved;
- Olga/admin receives the case, selected product, amount, symptoms and manual confirmation button;
- dossier generation is blocked until admin manually confirms payment;
- after confirmation, the bot can generate the dossier and continue the review flow.

## Why

Manual payment is safer during pilot because:

- YooKassa can reject or delay activation;
- Telegram provider token can be confusing or not live;
- payment failures create client friction;
- the product still needs controlled concierge validation before public launch.

## Product Prices In Manual Mode

- `week`: Разбор на 7 дней — 3 900 ₽
- `premium`: Персональный разбор на 30 дней — 6 900 ₽
- `vip`: VIP-сопровождение на 30 дней — 14 900 ₽

## Client-facing logic

The client sees:

- questionnaire completed;
- online payment is temporarily disabled;
- the team will contact them in Telegram to confirm payment and next step;
- dossier is not delivered until payment confirmation and expert review.

## Admin logic

Admin receives:

- submission ID;
- selected product;
- amount;
- client name;
- symptoms and goal;
- button: `✅ Подтвердить ручную оплату`.

After admin clicks the button:

- payment status becomes `manual_payment_confirmed`;
- dossier generation is allowed;
- client receives confirmation that work starts.

## How To Switch Back To Telegram/YooKassa Later

Only after YooKassa/Telegram live payment is proven:

1. set `PAYMENT_MODE=telegram`;
2. set valid live `PAYMENT_TOKEN`;
3. restart bot;
4. run a real paid Telegram walkthrough;
5. verify `payment_status=paid` and dossier generation.

Until that proof exists, public launch remains blocked and manual concierge mode remains the safe pilot path.

## Important Safety Rule

Manual payment does not remove human review.

Payment confirmation only allows dossier generation. The result still needs expert review before delivery to the client.
