# Live Payment Enable Runbook

Date: 2026-04-21
Owner: Olga / Wellness Bot
Goal: enable the real paid Telegram branch for pilot launch

## Current Situation

The code is ready for a real payment branch.

But the working environment is not yet fully payment-live because `PAYMENT_TOKEN` is not configured in the active `.env` files.

Without it:

- the bot cannot complete the real invoice path,
- the flow falls back to `manual_handoff_no_provider`,
- pilot cannot be honestly called end-to-end paid.

## Source Of Truth

Payment logic:

- [payment_flow.py](C:\Users\HP\Desktop\Новая папка\WellnessBot\payment_flow.py)

Current synchronized launch price:

- `6900 ₽`

Current helper scripts:

- [set-payment-token.ps1](C:\Users\HP\Desktop\Новая папка\ops\set-payment-token.ps1)
- [payment-token-to-clipboard.ps1](C:\Users\HP\Desktop\Новая папка\ops\payment-token-to-clipboard.ps1)

## What You Need Before Enabling

You need:

- a real Telegram payment provider token,
- the correct YooKassa product configured at `6900 ₽`,
- the same price in the bot code,
- ability to restart the bot after env update.

## Practical Enable Steps

### Step 1. Confirm YooKassa card

Use the approved product card:

- name: `Premium Wellness Dossier`
- price: `6900 ₽`
- quantity: `1`
- format: `Услуга`

Reference:

- [YOOKASSA_COPY_PASTE_20260421.md](C:\Users\HP\Desktop\Новая папка\docs\YOOKASSA_COPY_PASTE_20260421.md)

### Step 2. Insert PAYMENT_TOKEN

Run:

- `powershell -ExecutionPolicy Bypass -File .\ops\set-payment-token.ps1`

What the script does:

- asks for `PAYMENT_TOKEN`,
- writes it to:
  - root `.env`
  - `WellnessBot/.env`

Important:

- do not paste a damaged or truncated token,
- if the token looks incomplete, stop and recopy it.

### Step 3. Confirm env now contains the token

Check:

- root `.env`
- `WellnessBot/.env`

You should see:

- `PAYMENT_TOKEN=...`

### Step 4. Restart bot

Run:

- `powershell -ExecutionPolicy Bypass -File .\ops\bot-start.ps1`

Then:

- `powershell -ExecutionPolicy Bypass -File .\ops\bot-status.ps1`

Confirm:

- bot process is running,
- polling is active,
- no startup exceptions appear.

### Step 5. Run one fresh live payment walkthrough

Use a fresh Telegram case.

Walkthrough:

1. `/start`
2. consent
3. complete intake
4. reach invoice stage
5. confirm invoice appears
6. confirm successful payment event
7. confirm case moves beyond `awaiting_payment`
8. confirm dossier branch continues
9. confirm admin receives handoff / review message

### Step 6. Confirm stored state

After the live payment event, verify the saved case JSON:

- `payment_status` should become `paid`
- `payment_received_at` should exist
- `payment_context` should exist

### Step 7. Confirm operator handling

After payment:

- operator must see the case,
- dossier generation must continue,
- final client delivery must still remain human-reviewed.

## What Counts As Success

Live payment branch can be considered enabled only if all of these are true:

- `PAYMENT_TOKEN` is present in both env files,
- bot restarts successfully,
- invoice is shown in Telegram,
- payment is accepted,
- submission state becomes `paid`,
- dossier flow continues,
- admin sees the case in the expected handoff path.

## Common Failure Modes

### 1. Invoice does not appear

Check:

- `PAYMENT_TOKEN` exists,
- bot was restarted after env change,
- current code price is still `6900 ₽`.

### 2. Payment is rejected

Check:

- YooKassa amount matches bot amount,
- wrong or outdated product price was not entered,
- user and payload match the case.

### 3. Invoice branch falls back to manual handoff

This usually means:

- `PAYMENT_TOKEN` is still missing or not loaded.

### 4. Bot starts but polling conflicts

Run:

- `powershell -ExecutionPolicy Bypass -File .\ops\bot-status.ps1`

If another instance exists:

- stop duplicate instance,
- restart once.

## Operator Note

Do not announce paid pilot readiness only because the token was inserted.

Payment-live status exists only after:

- token inserted,
- bot restarted,
- one real Telegram payment walkthrough succeeds.

## Final Decision Rule

After the first successful live payment walkthrough:

- update [PILOT_LAUNCH_CHECKLIST_20260421.md](C:\Users\HP\Desktop\Новая папка\docs\PILOT_LAUNCH_CHECKLIST_20260421.md)
- then re-evaluate whether the project is now `pilot-ready`.
