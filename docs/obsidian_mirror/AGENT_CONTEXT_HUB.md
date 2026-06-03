# Agent Context Hub

Updated: 2026-06-03 23:41 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as sanitized replay payloads for external contributors.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Freshest runtime proof is now the June 3 direct-fallback restart in `bot.stderr`:
  - `2026-06-03 21:47:08 +0300` bot config
  - `2026-06-03 21:47:11 +0300` proxy connectivity failure and direct fallback
  - `2026-06-03 21:47:11-21:47:13 +0300` bot start, loops start, and polling start
- Current runtime truth: direct-fallback polling works again on June 3 night; proxy `127.0.0.1:10808` is still not proven required.
- Strongest fresh product proof: active paid `nutri_chat` continuity chat in `WellnessBot/data/runtime_state.json`.
- Active runtime session now points to `20260603T121917Z_1084557944` at `300 RUB`.
- Lead blocker: same-user paid-branch multiplication plus continuity-chat overreach, not runtime liveness.
- Latest hard breach: `20260531T183007Z_1084557944` is still `delivered_to_client` while `internal_review.judge_verdict = fail_major_issues`.
- Current disk state: `C:` free space is `6.70 GB` at `2026-06-03 23:41:46 +03:00`.
- Latest completed benchmark anchor: `ops/reports/quality_report_20260531T083403Z.md`.
- Current benchmark interpretation doc: `docs/WELLNESS_DIALOGUE_QA_20260603.md`.
- June 3 QA status: routing tests and smoke passed, but the full batch still aborts on prompt `1` with `openai.APIConnectionError`.

## Stage

- controlled concierge pilot where runtime is re-proven, but June 3 widened the same-user paid stack again: the live proof-bearing rail is a paid `nutri_chat`, the same user also opened new `habits` and another `nutri_chat` branch the same day, and delivery / ladder control is now the main execution risk

## Done

- The June 3 21:47 MSK direct-fallback runtime proof is now the current ops baseline.
- The active `nutri_chat` case in `runtime_state.json` has been re-read and it now points to the new June 3 submission, not the June 2 one.
- The June 3 QA interpretation remains refreshed in `docs/WELLNESS_DIALOGUE_QA_20260603.md`.
- Local sync artifacts, Obsidian mirror artifacts, and sanitized external-sync artifacts have been refreshed for this cycle.
- Notion and GitHub write-capable surfaces were re-attempted in this run.
- Google Drive availability was re-checked and remains unavailable in-session.

## Objective

- keep one canonical reviewed Telegram case coherent
- preserve the June 3 direct-fallback runtime mode without wasting more cycles on proxy narration
- treat the active paid `nutri_chat` thread as the current proof-bearing product and bound it with a tighter live-chat contract
- repair the delivery-gate contradiction before counting new sales as traction
- stop same-user paid-branch multiplication and collapse the stack into one canonical commercial path
- collapse pricing and offer mapping to one approved ladder
- keep intake, OCR, supplement, and full-tier assignment drift out of product truth until verified
- restore per-prompt QA visibility so model-path failures stop hiding the benchmark state

## Product Direction

- Telegram-first only
- manual concierge remains the official pilot mode
- treat the current best ladder as an inference, not approved truth:
  - `nutri_chat` is the only active proof-bearing rail
  - `habits`, `standard`, and `premium` are not approved live truth until canonical-path and review controls are current
- treat `week`, `basic`, `full`, and `vip` as conflicting legacy or alias names until normalized
- do not treat any package ladder as approved until one map is normalized across code, docs, prompts, payment flow, and persisted artifacts
- text-first is the only proven intake mode; voice/audio remains removed from the active path
- do not treat continuity promises inside the low-ticket rail as approved product truth

## Current Truth

- `WellnessBot/data/runtime_state.json` has an active same-user session:
  - `submission_id = 20260603T121917Z_1084557944`
  - `offer = nutri_chat`
  - `step = paid_nutri_chat`
  - runtime memory shows real post-payment continuity replies inside the same Telegram thread
  - that thread still overreaches with long mechanism-heavy interpretation and specialist-style framing
- The governing blocked case remains `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`:
  - `offer = week`
  - `payment_context.amount_rub = 3900`
  - `payment_status = manual_payment_confirmed`
  - `intake_status = delivery_blocked_needs_revision`
  - `internal_review.judge_verdict = needs_revision`
  - `requires_lab_resubmission = true`
- The same Telegram user now spans at least eleven live-relevant paid submissions:
  - `20260501T162705Z_1084557944` = governing blocked `week`, `canonical_status = active_blocked`
  - `20260505T131604Z_1084557944` = paid `premium`, `canonical_status = paid_premium_continuation_pending_operator_decision`
  - `20260514T213116Z_1084557944` = parked duplicate `premium`, `canonical_status = parked_duplicate_consent_pending`
  - `20260530T183208Z_1084557944` = paid `premium` at `6900 RUB`, `review_priority_quality_and_market`, no `canonical_path`
  - `20260530T205040Z_1084557944` = paid `basic` at `6900 RUB`, `review_priority_quality_and_market`, no `canonical_path`
  - `20260531T183007Z_1084557944` = paid `basic` at `14900 RUB`, `delivered_to_client`, `fail_major_issues`, no `canonical_path`
  - `20260601T204906Z_1084557944` = paid `basic` at `14000 RUB`, `review_priority_quality_and_market`, no `canonical_path`
  - `20260602T055745Z_1084557944` = paid `nutri_chat` at `500 RUB`, no `canonical_path`
  - `20260603T112723Z_1084557944` = paid `nutri_chat` at `500 RUB`, `manual_payment_pending`, no `canonical_path`
  - `20260603T113045Z_1084557944` = paid `habits` at `6900 RUB`, `manual_payment_confirmed`, no `canonical_path`
  - `20260603T121917Z_1084557944` = paid `nutri_chat` at `300 RUB`, active in runtime memory, no `canonical_path`
- Benchmark-critical runtime and product drift is materially relevant:
  - `WellnessBot/main.py`, `WellnessBot/payment_flow.py`, `WellnessBot/texts.py`, `WellnessBot/prompts.py`, and `WellnessBot/ai_drafting.py` now encode a different ladder than the standing docs and mini-app
  - `payment_flow.py` now maps `nutri_chat / habits / standard / premium / osipov` with live prices `300 / 6900 / 10000 / 14900 / 7000 RUB`
  - `mini-app/index.html` remains in safer placeholder territory at `1000 RUB`
  - root `index.html`, `app.js`, and `styles.css` are also in active unreviewed product-surface churn

## Regressions To Fix Now

- Same-user paid-branch multiplication: owner `Operator + Lead Developer`; next action hard-block new same-user paid branch creation while unresolved review or canonical-path conflicts exist, then collapse the eleven-submission stack to one canonical path.
- Delivery-gate breach: owner `Lead Developer + Operator`; next action audit `20260531T183007Z_1084557944`, record whether any manual override existed, and remove or remediate the `delivered_to_client` contradiction if `fail_major_issues` still stands.
- Continuity-chat safety drift: owner `Lead Developer + Quality Auditor`; next action audit the active `20260603T121917Z_1084557944` `nutri_chat` thread for over-specificity, mechanism claims, escalation boundaries, and unapproved continuity framing.
- Offer and pricing fragmentation: owner `Product Strategist + Lead Developer`; next action normalize one approved ladder across code, docs, prompts, payment flow, mini-app, and root marketing surfaces.
- Benchmark observability gap: owner `Lead Developer`; next action make `ops/quality_probe.py` emit partial per-prompt artifacts when the model path fails.
- Disk floor breach: owner `Ops`; next action restore `C:` above `10 GB` before more artifact-heavy work.
- Text-only scope drift: owner `Lead Developer`; next action keep docs and UX explicit that voice/audio is not on the active path while `WellnessBot/main.py` rejects voice messages.

## Next

1. Patch `ops/quality_probe.py` so prompt-level connection failures still emit partial artifacts.
2. Re-run the batch benchmark only after step `1` lands.
3. Tighten the live-chat contract in prompt and sanitizer rules.
4. Audit the active `20260603T121917Z_1084557944` `nutri_chat` thread against that contract.
5. Add a hard guard so unresolved same-user paid/review state blocks creation of another paid branch.
6. Audit `20260531T183007Z_1084557944` and repair the delivery-gate contradiction.
7. Classify the `20260530` to `20260603` branches into one canonical story.
8. Normalize one approved ladder only after steps `1-7` land.
9. Keep text-only intake explicit while voice remains disabled.
10. Restore `C:` above the `10 GB` floor.

## Must-Not-Change Rules

- Telegram-first only
- manual concierge remains the official pilot mode
- no price ladder becomes product truth until one approved map is written across code, docs, and artifacts
- one canonical paid path per Telegram user at a time
- no new same-user paid branch while unresolved review or delivery contradictions remain
- no premium-style escalation selling while the active approved ladder decision is still open
- human review required before delivery
- no diagnosis or treatment framing
- no unsafe supplement instructions without confirmed context and review
- no active product promise of voice/audio intake while `WellnessBot/main.py` rejects voice messages
- no hardcoded medical-style results on public or TMA surfaces
- do not count a paid path as healthy if payment succeeded but the final reviewed artifact is contradicted by failing review state
- do not describe proxy `127.0.0.1:10808` as required when the freshest proof is direct fallback
- do not describe OCR, supplement, or full-tier widening as safe until verified
- do not describe progress without a fresh proof artifact interpreted by current QA notes

## Context For New Model

Stage:

- controlled concierge pilot where runtime is re-proven on June 3 night, but the main blocker is now commercial and safety control: the same user opened new paid `habits` and `nutri_chat` branches on June 3 while an older `14900 RUB` case still carries `delivered_to_client` plus `fail_major_issues`

Objective:

- preserve the June 3 direct-fallback runtime
- treat `nutri_chat` as the current proof-bearing product and bound it directly
- repair the delivery-gate contradiction before counting new sales as proof
- stop same-user branch multiplication
- normalize one approved offer ladder
- restore benchmark observability around the live model path

Constraints:

- Telegram-first only
- `PAYMENT_MODE=manual`
- human review remains mandatory
- one canonical commercial path per Telegram user
- no new same-user paid branch while unresolved review or delivery contradictions remain
- text-only intake is the only proven live modality
- disk free space is `6.70 GB`
- latest completed benchmark is `ops/reports/quality_report_20260531T083403Z.md`
- current QA synthesis doc is `docs/WELLNESS_DIALOGUE_QA_20260603.md`
- the fresh batch benchmark still fails on prompt `1`
- Google Drive file discovery/create/upload/share tools are unavailable in the current Codex session

Immediate next actions:

1. Patch `ops/quality_probe.py` so model-path failures still emit partial artifacts.
2. Tighten the live-chat contract.
3. Hard-block new same-user paid branch creation while conflicts exist.
4. Audit the active `20260603T121917Z_1084557944` `nutri_chat` thread for safety and escalation boundaries.
5. Audit and repair `20260531T183007Z_1084557944`.
6. Classify the `20260530` to `20260603` branches into one canonical path.
7. Normalize one approved ladder only after the control fixes land.
8. Restore disk above `10 GB`.

Reference proof anchors:

- runtime proof: `bot.stderr`
- benchmark reference: `ops/reports/quality_report_20260531T083403Z.md`
- current QA interpretation: `docs/WELLNESS_DIALOGUE_QA_20260603.md`
