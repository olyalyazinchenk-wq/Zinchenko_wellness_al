# Agent Context Hub

Updated: 2026-05-08 16:40 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as the sanitized outward-sync fallback when a connector is missing.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Official pilot prices remain `3900 / 6900 / 14900 RUB`.
- Top product-truth defect: the governing `week` case `20260501T162705Z_1084557944` is still marked `delivered_to_client` even though its review verdict is `needs_revision` and no explicit override note is recorded.
- `WellnessBot/data/runtime_state.json` is still empty, so runtime-versus-storage mismatch is not the live blocker.
- Bot runtime is evidenced as running:
  - `bot.stderr.log` shows a fresh restart at `2026-05-07 23:46:49-23:46:50 MSK`
  - TMA server started at `http://localhost:8000`
  - proxy is configured as `http://127.0.0.1:12334`
  - latest local probe is visible at `2026-05-08 00:35:06 MSK`
  - the active path is still unproven because no clean no-proxy fallback verification exists yet
- Repo state:
  - latest local commit is `fe7a358` (`feat: guide manual lab entry`)
  - local `master` is ahead of `origin/master` by `2`
  - working tree currently contains docs refresh changes plus `docs/WELLNESS_DIALOGUE_QA_20260506.md`
- External sync surface:
  - Obsidian local mirror is available
  - Notion connector status: needs verification / likely blocked (auth)
  - GitHub connector status: available (remote reachable); docs sync pending push
  - Google Drive upload/create/share tools are unavailable in the current session
- Latest benchmark reference: `ops/reports/quality_report_20260506T080435Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions now appear in `6/9` model-handled symptom prompts
  - invented-name hallucination appears twice in the latest batch

## Кратко (RU)

- Режим: controlled concierge pilot; публичный запуск заблокирован.
- Оплата: `PAYMENT_MODE=manual`; human review обязателен перед выдачей.
- P0: delivery gate (нельзя `delivered_to_client` при `needs_revision` без override).
- Риск: один пользователь имеет параллельные платные ветки (`week`/`premium`) — нужен один канонический paid-path.

## Stage

- controlled concierge pilot with runtime back up again, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, model-path response discipline, and Google Drive capability

## Done

- `week` is still validated as a paid entry rail because `20260501T162705Z_1084557944` reached payment, delivery, and follow-up.
- A fresh paid `premium` case now also exists for the same user:
  - `20260505T131604Z_1084557944`
  - `manual_payment_confirmed`
  - `intake_status = review_priority_quality_and_market`
  - `judge_verdict = pass_with_minor_edits`
- Runtime-state mismatch remains cleared:
  - `WellnessBot/data/runtime_state.json` is empty
  - there is no active runtime-only session drift
- Notion outward sync is restored for this run:
  - workspace search succeeded
  - a new run note was created under the Antigravity context hub
- GitHub outward sync is restored for this run:
  - repository lookup succeeded
  - fresh sanitized outward-sync artifacts were written to the GitHub repo
- Manual-lab fallback is now a landed product affordance:
  - commit `176ac82` strengthens malformed manual-text rewrite handling
  - commit `fe7a358` adds a manual-entry button and structured typed-biomarker examples
  - this still needs end-to-end proof on a reviewed live case

## Objective

- restore delivery truth
- keep the active `week` case coherent and resubmission-safe
- collapse the same-user `week`/`premium` sprawl into one canonical path
- remove unsafe hardcoded price/result content from TMA/mini-app surfaces
- prove or explicitly accept the current proxy-backed polling path
- tighten first-line model replies before the next proof cycle
- keep outward sync live where the connector surface is actually available

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the validated paid entry rail
  - `premium` remains the flagship offer
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery
- premium should be proven as a same-case upgrade from fresh post-`week` evidence, not as a second active branch for the same user

## Current Truth

- `WellnessBot/data/runtime_state.json` is empty.
- The governing case is still `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`:
  - offer: `week`
  - payment confirmed
  - status: `delivered_to_client`
  - internal review still says `needs_revision`
  - no explicit delivery override note is present
  - latest follow-up arrived at `2026-05-07T20:46:50Z`
  - active lab-state remains unsafe:
    - `lab_quality_check.status = missing`
    - `lab_quality_check.requires_resubmission = true`
    - `requires_lab_resubmission = true`
- The same user now has five commercial branches in play:
  - `20260501T162705Z_1084557944` = governing delivered `week`
  - `20260505T131604Z_1084557944` = fresh paid `premium` with `pass_with_minor_edits`
  - `20260427T173913Z_1084557944` = stale `week` placeholder at `consent_pending`
  - `20260425T214914Z_1084557944` = evidence-only premium branch because labs still require resubmission
  - `20260425T212847Z_1084557944` = parked rewrite-only premium branch with `must_rewrite_with_high_caution`
- Landing still matches the Telegram-first funnel.
- Mini-app still drifts from backend truth:
  - shows off-policy `2990` pricing
  - hardcodes ferritin / vitamin D / cortisol result content
  - hardcodes supplement-style and `LCHF` result content
  - still presents a hardcoded `Premium Wellness-Досье` result surface
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - invented names, over-familiar tone, broad early mechanism stacking, duplicated emergency/service templates, and overlong replies are the live quality risks
- Current runtime evidence is live but still transport-sensitive:
  - latest restart baseline is `2026-05-07 23:46:49-23:46:50 MSK`
  - the bot is currently polling
  - the stable-vs-fragile transport question is still open because the active path uses the same local proxy
- Current external-sync evidence:
  - Notion and GitHub connector writes both succeeded in this run
  - local `git push` is still proxy-sensitive and should not be mistaken for connector-backed sync health
  - Google Drive file create/upload/share tools are not exposed in this session

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Same-user commercial stack drift:
  - one delivered `week`, one fresh paid `premium`, one stale `week`, and two older `premium` branches all belong to the same Telegram user
- Governing-case lab-state incoherence:
  - the governing `week` case is still in resubmission-needed state after new follow-up evidence
- Mini-app price and demo safety drift:
  - off-policy `2990` pricing and hardcoded supplement/diet result content
- Runtime transport dependency:
  - the bot is up, but the active path still depends on `127.0.0.1:12334` and has not yet passed a clean post-fix verification window
- Google Drive outward-sync gap:
  - upload/create/share tools are still unavailable in the current Codex session
- Model-path response discipline:
  - invented names, over-familiar tone, duplicated emergency templates, and over-broad first answers still leak through the latest QA pass

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Keep the governing `week` case in one coherent resubmission-needed follow-up state until the new files and ferritin correction are validated.
3. Decide whether `20260505T131604Z_1084557944` becomes the canonical paid path, merges into the governing `week` story, or is explicitly parked; then retire the other non-canonical branches.
4. Replace unsafe mini-app price/result demo content with a safe placeholder or reviewed backend-fed state.
5. Decide whether the runtime may depend on `127.0.0.1:12334`; if not, add a fallback and prove one clean post-fix path.
6. Tighten live-answer sanitization, prompt rules, and template separation against the `2026-05-06` QA regressions.
7. Keep Notion and GitHub synced; keep Google Drive blocked until upload/create/share tools actually exist.

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
- do not let the same user carry both an unresolved delivered `week` truth defect and a separate active premium proof story without an explicit merge or ownership decision
- do not call polling resilience fixed before one clean post-fix verification passes
- do not treat OCR auth recovery or manual-lab UX landing as proof that file/lab reliability is solved
- do not treat connector discovery as success if the required write surface is missing
- do not let planning or governance churn outrun delivery safety, runtime health, and canonical state truth

## Context For New Model

Stage:

- controlled concierge pilot with live runtime up again, but delivery-gate integrity, same-user case ownership, mini-app truth, model-path response discipline, and Google Drive capability are still unstable

Objective:

- restore delivery truth
- keep the active `week` case coherent and resubmission-safe
- collapse the same-user branch sprawl to one canonical path
- remove unsafe mini-app price/result drift
- prove or explicitly accept the current proxy-backed polling path
- tighten first-line model replies before the next proof cycle
- keep outward sync live where the connector surface is actually available

Constraints:

- Telegram-first only
- manual concierge remains official pilot mode
- official pilot prices remain `3900 / 6900 / 14900 RUB`
- human review required before delivery
- one canonical paid path per Telegram user
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA / public surfaces
- runtime still uses `http://127.0.0.1:12334`
- a fresh paid `premium` case for the same user now exists and must be explicitly merged, parked, or declared canonical
- Notion connector writes succeeded in this run
- GitHub connector writes succeeded in this run
- Google Drive upload/create/share tools are unavailable in the current Codex session

Immediate next actions:

1. Add or verify the hard delivery guard and manual override audit trail.
2. Reconcile `lab_quality_check` and follow-up evidence on `20260501T162705Z_1084557944` before treating the case as a success story.
3. Explicitly decide how `20260505T131604Z_1084557944` relates to the governing `week` case, then retire or park the non-canonical branches.
4. Remove `2990` pricing and unsafe hardcoded result content from `mini-app/index.html`.
5. Harden `sanitize_live_reply()`, prompt rules, and service/emergency templates against invented names, over-familiar tone, duplicate emergency replies, and overlong symptom answers.
6. Keep Notion and GitHub synced; request Google Drive upload/create/share access.

Reference benchmark:

- `ops/reports/quality_report_20260506T080435Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260506.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `6/9` clarifying-question coverage on model-handled symptom prompts
