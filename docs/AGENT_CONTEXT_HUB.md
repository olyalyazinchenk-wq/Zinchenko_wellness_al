# Agent Context Hub

Updated: 2026-05-05 21:31 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and the GitHub source-of-truth doc for sanitized contributor onboarding.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Official pilot prices remain `3900 / 6900 / 14900 RUB`.
- Top product-truth defect: the `week` case `20260501T162705Z_1084557944` still shows `delivered_to_client` even though its attached review verdict is `needs_revision`, and no explicit override note is recorded.
- `WellnessBot/data/runtime_state.json` is empty, so runtime/storage mismatch is not the active blocker.
- Bot runtime is evidenced as running:
  - `bot.stderr.log` shows a fresh start at `2026-05-05 17:15:59 MSK`
  - polling started at `2026-05-05 17:16:00 MSK`
  - TMA server started at `http://localhost:8000`
  - proxy is configured as `http://127.0.0.1:12334`
  - latest local requests are visible at `2026-05-05 17:58-17:59 MSK`
- Disk headroom remains acceptable: `C:` free space was approximately `18.97 GB` as of `2026-05-05 09:31 MSK` (escalation threshold remains `10 GB`).
- Repo state: no new WellnessBot core code/test/landing/mini-app commits after `b6010bb`; current local changes are docs plus optional Docker dev artifacts pending commit.
- New local artifacts present for review/sync: `docs/2026-05-04_nutrition-bot-architecture.md`, `docs/2026-05-04_nutrition-bot-context-document.md`, `docs/2026-05-05_STRATEGIC_MASTER_PLAN.md`, `WellnessBot/Dockerfile`, and `WellnessBot/docker-compose.yml`.
- New Hermes planning artifacts are present locally (docs-only): `docs/hermes_os/*`, `docs/hermes_skills/*`, `docs/reports/*`, `docs/tasks/HERMES-20260505-*.md` (ensure no secrets before syncing).
- Latest benchmark reference: `ops/reports/quality_report_20260501T080509Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions in `7/9` model-handled symptom prompts

## Stage

- controlled concierge pilot with validated paid `week` demand and restored live-model reach, but unresolved delivery-gate integrity, same-user paid-path duplication, unsafe mini-app truth drift, and still-fragile polling/proxy resilience

## Done

- `week` is still validated as a paid entry rail because `20260501T162705Z_1084557944` reached payment, delivery, and follow-up.
- Runtime-state mismatch is still cleared:
  - `WellnessBot/data/runtime_state.json` is empty
  - there is no active runtime-only session drift
- Router overreach is no longer the main quality blocker:
  - benchmark moved from full routing capture to `9/20` model-handled replies
  - clarifying-question behavior appears in `7/9` model-handled symptom prompts
- Governance pressure is quantified and unchanged:
  - `120` experiments
  - `4` duplicate title groups
  - largest duplicate group `x7`

## Objective

- restore delivery truth before the next client-facing proof
- collapse the same-user `week`/`premium` sprawl into one canonical path
- remove unsafe hardcoded price/result content from TMA/mini-app surfaces
- re-establish a verifiable polling path before calling runtime healthy again

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
  - hardcodes ferritin / vitamin D findings
  - hardcodes supplement-dose and `LCHF` result content
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - false specificity, invented personalization, over-familiar tone, and early diagnosis-like labels are the live quality risks
- Current runtime evidence is worse than the previous sync narrative:
  - the latest log tail is an unresolved same-day outage window from `2026-05-03 14:20:44` through `14:30:12 MSK`
  - that window includes repeated `ClientOSError [WinError 64]`
  - the same window also includes direct proxy refusals on `127.0.0.1:12334`
  - no active local Python bot process is visible at the current sync time

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Same-user paid-path drift:
  - one delivered `week` case, one stale `week` placeholder, and two unresolved `premium` branches
- Mini-app price and demo safety drift:
  - off-policy `2990` pricing and hardcoded supplement/diet result content
- Runtime availability and resilience regression:
  - latest log ends in fetch/proxy failures and the bot is not currently evidenced as running
- Model-path response discipline:
  - invented names, over-familiar tone, and early diagnosis-like labels still leak through QA

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Restore a verifiable polling process, then prove whether the stable path is proxy-backed or no-proxy.
3. Declare one canonical paid path for the current same-user stack and freeze/archive the rest.
4. Replace unsafe mini-app price/result demo content with a safe placeholder or reviewed backend-fed state.
5. Tighten live-answer sanitization and benchmark assertions around invented personalization and false specificity.
6. Convert the delivered `week` follow-up plus fresh labs into one explicit premium-upgrade brief only after the review contradiction is resolved.

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
- do not treat an errored log tail plus an absent process as acceptable runtime health
- do not call polling resilience fixed before one clean post-fix verification passes
- do not let landing, mini-app, or growth work outrun delivery safety, runtime health, and canonical state truth

## Context For New Model

Stage:

- controlled concierge pilot with validated paid `week` demand and restored live-model reach, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, and runtime availability

Objective:

- restore delivery truth
- collapse the same-user branch sprawl to one canonical path
- remove unsafe mini-app price/result drift
- re-establish a verifiable polling path before the next proof cycle

Constraints:

- Telegram-first only
- manual concierge remains official pilot mode
- official pilot prices remain `3900 / 6900 / 14900 RUB`
- human review required before delivery
- one canonical paid path per Telegram user
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA / public surfaces
- Google Drive upload/share is unavailable in the current Codex session

Immediate next actions:

1. Add a guard so unresolved internal-review verdicts cannot move to `delivered_to_client` without an explicit manual override record.
2. Restore a running bot process, verify the proxy dependency on `127.0.0.1:12334`, and require one clean post-fix verification before calling runtime stable.
3. Decide the canonical path for the current same-user stack and retire `20260427T173913Z_1084557944` plus the non-canonical premium branches.
4. Remove `2990` pricing and unsafe hardcoded result content from `mini-app/index.html`.
5. Tighten `sanitize_live_reply()` and benchmark assertions for invented names, over-familiar tone, and early diagnosis-like language.
6. Convert the delivered `week` follow-up plus fresh labs into one explicit premium-upgrade brief after the delivery-review contradiction is resolved.

Reference benchmark:

- `ops/reports/quality_report_20260501T080509Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260501.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `7/9` clarifying-question coverage on model-handled symptom prompts
