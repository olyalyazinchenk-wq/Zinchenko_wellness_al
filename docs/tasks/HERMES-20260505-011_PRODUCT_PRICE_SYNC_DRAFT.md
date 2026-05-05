# HERMES-20260505-011: Product Price Sync (DRAFT)
Task ID: `HERMES-20260505-011` | Status: `draft` | Owner: `Codex` | Priority: `P1`
Requires: `Codex/Olga approval` | Files: `payment_flow.py, mini-app/index.html`

## Changes
1. **payment_flow.py:57** — `build_invoice_payload`: использовать `offer['code']` вместо хардкода `"premium"`
2. **mini-app/index.html** — убрать 2990₽ и medical findings, заменить placeholder: цены 3900/6900/14900, демо без диагнозов

## Acceptance
- [ ] week-клиент получает invoice с префиксом "week:"
- [ ] Mini-app не показывает 2990₽ и medical findings
