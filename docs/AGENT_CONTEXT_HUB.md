# Agent Context Hub

Updated: 2026-05-03 09:19 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and the GitHub source-of-truth doc for sanitized contributor onboarding.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Official pilot prices remain `3900 / 6900 / 14900 RUB`.
- Top live defect: the `week` case `20260501T162705Z_1084557944` still shows `delivered_to_client` even though its attached review verdict is `needs_revision`.
- `WellnessBot/data/runtime_state.json` is empty, so runtime/storage mismatch is not the active blocker.
- Disk headroom is healthy: `C:` free space is approximately `22.98 GB` as of `2026-05-03 09:19 MSK`.
- Latest benchmark reference: `ops/reports/quality_report_20260501T080509Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions in `7/9` model-handled symptom prompts
- Bot runtime is currently up, but it recovered from two same-day outage windows:
  - `2026-05-02 15:09:39-15:17:57 MSK` repeated `WinError 64` polling failures
  - `2026-05-02 20:26:15-20:27:14 MSK` server disconnect and proxy refusal on `127.0.0.1:12334`

## Stage

- controlled concierge pilot with validated paid `week` demand and restored live-model reach, but unresolved delivery-gate integrity, same-user paid-path duplication, unsafe mini-app price/result drift, and unstable polling resilience

## Done

- `week` is now validated as a paid entry rail because `20260501T162705Z_1084557944` reached payment, delivery, and follow-up.
- Runtime-state mismatch is no longer the main issue:
  - `WellnessBot/data/runtime_state.json` is empty
  - disk headroom is healthy again
- Router overreach is no longer the main quality blocker:
  - benchmark moved from full routing capture to `9/20` model-handled replies
  - clarifying-question behavior now appears in `7/9` model-handled symptom prompts

## Objective

- make the next delivered result review-safe and auditable
- collapse the same-user `week`/`premium` sprawl into one canonical path
- remove unsafe hardcoded price/result content from TMA/mini-app surfaces
- stabilize bot polling enough for the next safe proof cycle without losing the current reach baseline

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the validated paid entry rail
  - `premium` remains the flagship offer
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery
- premium should now be proven from fresh post-`week` evidence, not from stale same-user April branches

## Current Truth

- `WellnessBot/data/runtime_state.json` is empty.
- The current governing case is:
  - `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`
  - offer: `week`
  - payment confirmed
  - status: `delivered_to_client`
  - follow-up already started after delivery
  - internal review on the same case still says `needs_revision`
- The same user still also has one stale `week` placeholder:
  - `20260427T173913Z_1084557944`
  - `consent_pending`
  - no active runtime session points to it now
- The same user still also has two older unresolved `premium` branches:
  - `20260425T214914Z_1084557944` remains evidence-only because `requires_lab_resubmission = true`
  - `20260425T212847Z_1084557944` remains rewrite-only with `must_rewrite_with_high_caution`
- Landing still matches the Telegram-first funnel.
- Mini-app still drifts from backend truth:
  - shows off-policy `2990` pricing
  - hardcodes supplement-dose and LCHF-style result content
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - false specificity, invented personalization, over-familiar tone, and early diagnosis-like labels are the live quality risks
- Current runtime evidence is worse than the morning snapshot:
  - one recovered outage window lasted more than 8 minutes
  - a second recovered outage window later included direct proxy refusal on `127.0.0.1:12334`

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Same-user paid-path drift:
  - one delivered `week` case, one stale `week` placeholder, and two unresolved `premium` branches
- Mini-app price and demo safety drift:
  - off-policy `2990` pricing and hardcoded supplement/diet result content
- Runtime resilience regression:
  - repeated same-day polling failures plus proxy refusal mean the bot is recoverable, but not yet stable
- Model-path response discipline:
  - invented names, over-familiar tone, and early diagnosis-like labels still leak through QA

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Declare one canonical paid path for the current same-user stack and freeze/archive the rest.
3. Replace unsafe mini-app price/result demo content with a safe placeholder or reviewed backend-fed state.
4. Remove or stabilize the fragile proxy dependency behind polling and prove one clean reconnect path.
5. Tighten live-answer sanitization and benchmark assertions around invented personalization and false specificity.

## Sync Note (2026-05-03 09:19 MSK)

- No new code changes detected since the last sync; current uncommitted edits are limited to `docs/*` governance text updates.
- Added a sustained runtime interruption escalation rule to `docs/KNOWLEDGE_SYNC_HUB.md` and corrected wording/metrics in `docs/STRATEGY_LIVE_DELTA.md`.
- Public launch remains blocked; controlled concierge pilot rules remain unchanged (manual payment + mandatory human review).

## Must-Not-Change Rules

- Telegram-first only
- manual concierge remains the official pilot mode
- official pilot prices stay `3900 / 6900 / 14900 RUB`
- one canonical paid path per Telegram user at a time
- human review required before delivery
- no diagnosis or treatment framing
- no unsafe supplement instructions without confirmed context and review
- no hardcoded medical-style or supplement-style demo results on TMA or public-facing surfaces
- no off-policy pricing on TMA or public-facing surfaces
- do not treat a delivered status as trustworthy if the internal-review verdict still demands revision
- do not treat a recovered multi-minute outage or proxy refusal loop as a solved runtime issue
- do not let landing, mini-app, or growth work outrun delivery safety and canonical state truth

## Context For New Model

Stage:

- controlled concierge pilot with validated paid `week` demand, restored live-model reach, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, and polling resilience

Objective:

- make the next delivered result review-safe
- collapse the same-user paid-path drift
- remove unsafe mini-app price/result drift
- keep polling reliable enough for the next safe proof cycle

Constraints:

- Telegram-first only
- manual concierge remains official pilot mode
- official pilot prices remain `3900 / 6900 / 14900 RUB`
- human review required before delivery
- one canonical paid path per Telegram user
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA/public surfaces
- Google Drive upload/share is unavailable in the current Codex session

Immediate next actions:

1. Add a guard so unresolved internal-review verdicts cannot move to `delivered_to_client` without an explicit manual override record.
2. Decide the canonical path for the current same-user stack and explicitly retire the stale `week` placeholder plus the non-canonical premium branches.
3. Remove `2990` pricing and unsafe hardcoded result content from `mini-app/index.html`.
4. Verify whether polling should depend on the local proxy at `127.0.0.1:12334`, and add a direct no-proxy fallback if not.
5. Tighten `sanitize_live_reply()` and benchmark assertions for invented names, over-familiar tone, and early diagnosis-like language.

Reference benchmark:

- `ops/reports/quality_report_20260501T080509Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260501.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `7/9` clarifying-question coverage on model-handled symptom prompts
