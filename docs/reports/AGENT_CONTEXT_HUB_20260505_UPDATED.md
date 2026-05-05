# Agent Context Hub — UPDATED 2026-05-05

## Quick Status
- Mode: controlled concierge pilot. Public launch blocked.
- Payment: `PAYMENT_MODE=manual`. Human review mandatory.
- Prices: 3900 / 6900 / 14900 RUB.
- **Verdict: NOT pilot-ready** (4 P0 blockers open).

## P0 Blockers (stop pilot)
| # | Issue | Fix | Owner |
|---|-------|-----|-------|
| 1 | Delivery gate bypass (main.py:1810) | Add judge_verdict check | Codex |
| 2 | Runtime not evidenced as running | Restore bot, fix proxy | Codex |
| 3 | Mini-app: 2990₽ + medical findings | Remove hardcode | Codex |
| 4 | Multi-path drift (4 branches / user) | Canonical path | Codex |

## P1 — Important before first client
- Manual override audit trail missing
- "Premium Wellness Dossier" — English in UI
- invoice_payload hardcodes "premium:" for all products
- sanitize_live_reply: only 4 patterns
- DOSSIER_DRAFT_PROMPT in English
- CONSENT without timestamp

## Ready-to-apply diffs
**File:** `docs/reports/CODEX_EXECUTION_PACK_20260505.md`
3 copy-paste diffs: delivery gate (15 min), invoice (5 min), Russian text (5 min).

## Decision needed from Olga
**File:** `docs/reports/OLGA_DECISION_DRIVE_20260505.md`
3 decisions: (1) run Codex pack, (2) give Hermes Level 2, (3) send Beget DNS.

## Created artifacts today (41 files)
- `docs/reports/HERMES-20260505-004_*` — full day audit (8 phases)
- `docs/reports/HERMES-20260505-005_*` — Hermes Autonomous Engineer OS
- `docs/hermes_os/` — 12 OS files
- `docs/tasks/HERMES-20260505-009...021` — 13 draft task packets
- `docs/hermes_skills/` — 1 new skill + 4 updated

## Next
1. Codex applies Execution Pack (25 min total)
2. Hermes gets Level 2 → fixes Russian texts
3. Olga sends Beget DNS → landing preparation
