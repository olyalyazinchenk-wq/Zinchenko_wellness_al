# Agent Context Hub

Updated: 2026-05-03 09:20 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and the GitHub source-of-truth doc for sanitized contributor onboarding.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Official pilot prices remain `3900 / 6900 / 14900 RUB`.
- Top live defect: the `week` case `20260501T162705Z_1084557944` still shows `delivered_to_client` even though its attached review verdict is `needs_revision`, and no explicit override note is recorded.
- `WellnessBot/data/runtime_state.json` is empty, so runtime/storage mismatch is not the active blocker.
- Disk headroom is healthy: `C:` free space is approximately `22.97 GB` as of `2026-05-03 09:20 MSK`.
- Latest benchmark reference: `ops/reports/quality_report_20260501T080509Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions in `7/9` model-handled symptom prompts
- Bot runtime is currently up, but polling resilience is still unresolved:
  - recovered outage window `2026-05-02 15:09:39-15:17:57 MSK` with repeated `WinError 64`
  - recovered outage window `2026-05-02 20:26:15-20:27:14 MSK` with server disconnects and proxy refusal on `127.0.0.1:12334`
  - recovered outage window `2026-05-02 21:38:36-21:38:48 MSK` with `ServerDisconnectedError`

## Stage

- controlled concierge pilot with validated paid `week` demand and restored live-model reach, but unresolved delivery-gate integrity, same-user paid-path duplication, unsafe mini-app price/result drift, and three same-day polling recovery windows that still block runtime confidence

## Done

- `week` is now validated as a paid entry rail because `20260501T162705Z_1084557944` reached payment, delivery, and follow-up.
- Runtime-state mismatch is no longer the main issue:
  - `WellnessBot/data/runtime_state.json` is empty
  - disk headroom is healthy again
- Router overreach is no longer the main quality blocker:
  - benchmark moved from full routing capture to `9/20` model-handled replies
  - clarifying-question behavior now appears in `7/9` model-handled symptom prompts
- Governance pressure is quantified and unchanged:
  - `120` experiments
  - `4` duplicate title groups
  - largest duplicate group `x7`

## Objective

- make the next delivered result review-safe and auditable
- collapse the same-user `week` / `premium` sprawl into one canonical path
- remove unsafe hardcoded price/result content from TMA / mini-app surfaces
- prove a stable polling path for the next safe proof cycle without losing the current reach baseline
- improve model-path discipline without losing the current reach baseline

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
  - no explicit delivery override note is present
- The same user still also has three non-canonical branches:
  - `20260427T173913Z_1084557944` = stale `week` placeholder at `consent_pending`
  - `20260425T214914Z_1084557944` = evidence-only premium branch because `requires_lab_resubmission = true`
  - `20260425T212847Z_1084557944` = parked rewrite-only premium branch with `must_rewrite_with_high_caution`
- Landing still matches the Telegram-first funnel.
- Mini-app still drifts from backend truth:
  - shows off-policy `2990` pricing
  - hardcodes ferritin / vitamin D / cortisol findings
  - hardcodes supplement-dose and `LCHF` result content
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - false specificity, invented personalization, over-familiar tone, and early diagnosis-like labels are the live quality risks
- Current runtime evidence remains worse than the fallback-improvement narrative:
  - one recovered outage window lasted more than 8 minutes
  - a second recovered outage window included direct proxy refusal on `127.0.0.1:12334`
  - a third same-day recovered disconnect happened later that evening

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Same-user paid-path drift:
  - one delivered `week` case plus one stale `week` placeholder plus two unresolved `premium` branches
- Mini-app price and demo safety drift:
  - off-policy `2990` price and hardcoded medical-style result content
- Runtime polling fragility:
  - repeated same-day recovered failures, including proxy refusal on `127.0.0.1:12334`
- Model-path response discipline:
  - invented names, over-familiar tone, and early diagnosis-like labels still leak through QA

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Declare one canonical paid path for the current same-user stack and freeze / archive the rest.
3. Replace unsafe mini-app price/result demo content with a safe placeholder or reviewed backend-fed state.
4. Verify whether polling really needs `127.0.0.1:12334`, add a documented no-proxy fallback if not, and require one clean post-fix verification before calling runtime stable.
5. Tighten live-answer sanitization and benchmark assertions around invented personalization and false specificity.
6. Turn the delivered `week` follow-up into one explicit premium-upgrade hypothesis after review truth is repaired.

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
- do not treat a delivered status as trustworthy if the internal-review verdict still demands revision and no override note exists
- do not call runtime stability solved while polling still depends on a flapping proxy path without a documented fallback
- do not call runtime stability solved before one clean post-fix verification
- do not let landing, mini-app, growth work, or benchmark churn outrun delivery safety, canonical state truth, and Telegram runtime resilience

## Context For New Model

Stage:

- controlled concierge pilot with validated paid `week` demand and restored live-model reach, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, and polling resilience

Done:

- `week` is commercially validated as a paid entry rail
- runtime-state mismatch is cleared
- benchmark baseline improved to `9/20` model-path replies with `7/9` clarifying-question coverage on model-handled symptom prompts
- governance pressure is measured and unchanged instead of being mistaken for progress

Next:

1. Add a guard so unresolved internal-review verdicts cannot move to `delivered_to_client` without an explicit manual override record.
2. Decide the canonical path for the current same-user stack and retire `20260427T173913Z_1084557944` plus the non-canonical premium branches.
3. Remove `2990` pricing and unsafe hardcoded result content from `mini-app/index.html`.
4. Verify the proxy dependency on `127.0.0.1:12334`, choose the stable path, and require one clean post-fix verification before calling runtime stable.
5. Tighten `sanitize_live_reply()` and benchmark assertions for invented names, over-familiar tone, and early diagnosis-like language.
6. Convert the delivered `week` follow-up plus fresh labs into one explicit premium-upgrade brief.

Must-Not-Change:

- Telegram-first only
- manual concierge remains official pilot mode
- official pilot prices remain `3900 / 6900 / 14900 RUB`
- human review required before delivery
- one canonical paid path per Telegram user
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA / public surfaces
- no off-policy pricing on TMA / public surfaces
- no silent proxy dependency without a documented fallback
- no claim of runtime stability before one clean post-fix verification

Reference benchmark:

- `ops/reports/quality_report_20260501T080509Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260501.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `7/9` clarifying-question coverage on model-handled symptom prompts
