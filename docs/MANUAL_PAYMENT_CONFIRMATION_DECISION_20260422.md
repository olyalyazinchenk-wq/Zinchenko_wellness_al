# Manual Payment Confirmation Decision

Date: 2026-04-22
Owner: Olga / Wellness Bot
Purpose: make the concierge payment fallback safe while YooKassa / Telegram payments are not fully live.

## Decision

If Telegram/YooKassa online payment is not configured or fails, the bot must not treat the case as paid automatically.

Instead, the case moves into a manual payment state:

- `manual_payment_pending`

Only an admin/operator can confirm payment manually.

After confirmation, the case moves into:

- `manual_payment_confirmed`

Only after that should dossier generation continue.

## Why

The previous fallback was useful for testing, but too permissive for a paid pilot:

- intake could move into manual handoff,
- dossier generation could start immediately,
- payment confirmation was not explicit enough.

For a controlled concierge pilot, we need auditability:

- who confirmed payment,
- when payment was confirmed,
- which case moved forward,
- whether delivery was blocked before payment.

## Product Rule

Manual fallback is allowed only for controlled pilot cases.

It is not the final public paid launch mode.

## Operational Rule

The operator must confirm payment outside the bot first.

Only after that:

1. press the admin confirmation button or use the future admin command,
2. case becomes `manual_payment_confirmed`,
3. dossier generation starts,
4. human review remains mandatory before client delivery.

## Status Model

- `manual_payment_pending`
  - intake completed,
  - online provider is unavailable or invoice failed,
  - operator must send/confirm payment route manually,
  - dossier generation is blocked.

- `manual_payment_confirmed`
  - operator confirmed external payment,
  - dossier generation may start,
  - case is still not automatically delivered to client.

## Safety Rule

No paid dossier should be generated or delivered in concierge mode until payment is manually confirmed.

## Next Implementation

Implement:

- payment status helpers,
- admin confirmation button,
- queue status label,
- generation gate,
- tests for manual payment state transitions.
