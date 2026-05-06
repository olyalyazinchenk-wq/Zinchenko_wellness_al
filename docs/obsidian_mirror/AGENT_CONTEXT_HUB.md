# Agent Context Hub

Updated: 2026-05-06 09:30 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as the sanitized outward-sync fallback while external connectors are blocked.

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
  - the active path is still unproven because no clean no-proxy fallback verification exists yet
- Disk headroom remains acceptable: `C:` free space is approximately `19.37 GB` as of `2026-05-05 21:34 MSK` (escalation threshold remains `10 GB`).
- Repo state: latest local commit is `883228b` (`docs: refresh sprint board + disk hygiene (2026-05-06)`); working tree is clean after sync.
- New local artifacts present for review/sync: `docs/2026-05-04_nutrition-bot-architecture.md`, `docs/2026-05-04_nutrition-bot-context-document.md`, `docs/2026-05-05_STRATEGIC_MASTER_PLAN.md`, `WellnessBot/Dockerfile`, and `WellnessBot/docker-compose.yml`.
- New Hermes planning artifacts are present locally (docs-only): `docs/hermes_os/*`, `docs/hermes_skills/*`, `docs/reports/*`, `docs/tasks/HERMES-20260505-*.md` (ensure no secrets before syncing).
- External sync surface:
  - Obsidian local mirror is available
  - Notion connector status: OK (status page created for `2026-05-06 09:30 MSK`)
  - GitHub sync status: OK (pushed `883228b` to `master`)
  - Google Drive upload/share tools are unavailable in the current session
- Latest benchmark reference: `ops/reports/quality_report_20260501T080509Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions in `7/9` model-handled symptom prompts

## Stage

- controlled concierge pilot with validated paid `week` demand, restored live-model reach, and runtime back up again, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, polling resilience, and connector availability

## Done

- `week` is still validated as a paid entry rail because `20260501T162705Z_1084557944` reached payment, delivery, and follow-up.
- Runtime-state mismatch is still cleared:
  - `WellnessBot/data/runtime_state.json` is empty
  - there is no active runtime-only session drift
- Router overreach is no longer the main quality blocker:
  - benchmark moved from full routing capture to `9/20` model-handled replies
  - clarifying-question behavior appears in `7/9` model-handled symptom prompts
- Fresh follow-up evidence now exists on the current canonical `week` case:
  - PDF upload
  - two photo uploads
  - ferritin correction from the client
  - user request to create a new case
- Governance pressure worsened:
  - `127` experiments
  - `4` duplicate title groups
  - largest duplicate group `x8`

## Objective

- restore delivery truth
- normalize the active `week` follow-up state
- collapse the same-user `week`/`premium` sprawl into one canonical path
- remove unsafe hardcoded price/result content from TMA/mini-app surfaces
- prove the currently running polling path before calling runtime healthy again
- compress execution loops so task/report generation stops outrunning live fixes
- restore external connector sync

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
  - fresh follow-up artifacts arrived on `2026-05-05`
  - field conflict remains active:
    - `lab_quality_check.status = ok`
    - `requires_lab_resubmission = true`
- The same user still also has three non-canonical branches:
  - `20260427T173913Z_1084557944` = stale `week` placeholder at `consent_pending`
  - `20260425T214914Z_1084557944` = evidence-only premium branch because `requires_lab_resubmission = true`
  - `20260425T212847Z_1084557944` = parked rewrite-only premium branch with `must_rewrite_with_high_caution`
- Landing still matches the Telegram-first funnel.
- Mini-app still drifts from backend truth:
  - shows off-policy `2990` pricing
  - hardcodes ferritin / vitamin D findings
  - hardcodes cortisol finding
  - hardcodes vitamin D supplement wording
  - hardcodes supplement-style and `LCHF` result content
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - false specificity, invented personalization, over-familiar tone, and early diagnosis-like labels are the live quality risks
- Current runtime evidence is mixed rather than absent:
  - the latest unresolved outage window still exists in the history at `2026-05-03 14:20:44-14:30:12 MSK`
  - a clean restart occurred on `2026-05-05 17:15:59 MSK`
  - the bot is currently up again
  - the stable-vs-fragile transport question is still open because the active path uses the same local proxy
- Current external-sync evidence:
  - Notion call failed with `tool call error: failed to get client` -> `MCP startup failed: timed out awaiting tools/list after 30s`
  - GitHub call failed with `tool call error: failed to get client` -> `MCP startup failed: timed out awaiting tools/list after 30s`
  - Google Drive file create/upload/share tools were not exposed by tool discovery in this session

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Governing-case lab-state mismatch:
  - the same `week` case now shows `lab_quality_check.status = ok` while `requires_lab_resubmission = true`
- Same-user paid-path drift:
  - one delivered `week` case, one stale `week` placeholder, and two unresolved `premium` branches
- Mini-app price and demo safety drift:
  - off-policy `2990` pricing and hardcoded supplement/diet result content
- Runtime resilience regression:
  - the bot is back up, but the active path still depends on `127.0.0.1:12334` and has not yet passed a clean post-fix verification window
- External connector outage:
  - Notion and GitHub app startups time out before use
  - Google Drive upload/share remains unavailable
- Execution diffusion / draft swarm:
  - `127` experiments
  - duplicate-title pressure now at `x8`
  - `29` same-day HERMES task or draft files are accumulating around already-known P0 themes
- Model-path response discipline:
  - invented names, over-familiar tone, and early diagnosis-like labels still leak through QA

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Normalize the governing `week` case so `lab_quality_check` and `requires_lab_resubmission` match the latest follow-up truth.
3. Record whether the current delivered `week` case needs correction before more follow-up output is treated as proof.
4. Keep the fresh `2026-05-05` follow-up uploads on the same canonical case; do not spawn a second active case.
5. Prove whether the currently running polling path is proxy-backed or no-proxy.
6. Replace unsafe mini-app price/result demo content with a safe placeholder or reviewed backend-fed state.
7. Freeze net-new draft/task generation until a P0 delivery, surface, or runtime fix lands.
8. Tighten live-answer sanitization and benchmark assertions around invented personalization and false specificity.
9. Convert the delivered `week` follow-up plus fresh labs into one explicit premium-upgrade brief only after the review contradiction is resolved.
10. Restore Notion, GitHub, and Google Drive availability, then replay the pending outward-sync artifacts from `docs/external_sync/`.

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
- do not open a second case from the `2026-05-05` follow-up uploads unless an explicit replacement decision is recorded
- do not treat the clean `2026-05-05` restart as proof that polling resilience is fixed
- do not call polling resilience fixed before one clean post-fix verification passes
- do not treat connector discovery as success if the app fails to start or the first real write call times out
- do not let task/report generation outrun delivery safety, runtime health, and canonical state truth
- do not let landing, mini-app, or growth work outrun delivery safety, runtime health, and canonical state truth

## Context For New Model

Stage:

- controlled concierge pilot with validated paid `week` demand, restored live-model reach, and runtime back up again, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, polling resilience, and connector availability

Objective:

- restore delivery truth
- normalize the active `week` follow-up state
- collapse the same-user branch sprawl to one canonical path
- remove unsafe mini-app price/result drift
- prove the currently running polling path before the next proof cycle
- compress execution loops so fixes outrun planning artifacts
- restore external connector sync

Constraints:

- Telegram-first only
- manual concierge remains official pilot mode
- official pilot prices remain `3900 / 6900 / 14900 RUB`
- human review required before delivery
- one canonical paid path per Telegram user
- fresh follow-up uploads stay on the canonical case unless an explicit replacement decision is recorded
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA / public surfaces
- Notion connector currently fails with `MCP startup failed: timed out awaiting tools/list after 30s`
- GitHub connector currently fails with `MCP startup failed: timed out awaiting tools/list after 30s`
- Google Drive upload/share tools are unavailable in the current Codex session

Immediate next actions:

1. Add a guard so unresolved internal-review verdicts cannot move to `delivered_to_client` without an explicit manual override record.
2. Normalize `lab_quality_check` versus `requires_lab_resubmission` on `20260501T162705Z_1084557944` after the new ferritin correction and uploads.
3. Decide whether the current delivered `week` case must be corrected before more follow-up output is treated as valid proof.
4. Keep the fresh `2026-05-05` follow-up files on the same canonical path; retire `20260427T173913Z_1084557944` plus the non-canonical premium branches.
5. Verify the proxy dependency on `127.0.0.1:12334` from the currently running baseline and require one clean post-fix verification before calling runtime stable.
6. Remove `2990` pricing and unsafe hardcoded result content from `mini-app/index.html`.
7. Freeze net-new draft/task generation unless it directly closes a delivery, surface, or runtime gap.
8. Tighten `sanitize_live_reply()` and benchmark assertions for invented names, over-familiar tone, and early diagnosis-like language.
9. Convert the delivered `week` follow-up plus fresh labs into one explicit premium-upgrade brief after the delivery-review contradiction is resolved.
10. Restore Notion, GitHub, and Google Drive availability, then replay the pending outward-sync artifacts from `docs/external_sync/`.

Reference benchmark:

- `ops/reports/quality_report_20260501T080509Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260501.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `7/9` clarifying-question coverage on model-handled symptom prompts
