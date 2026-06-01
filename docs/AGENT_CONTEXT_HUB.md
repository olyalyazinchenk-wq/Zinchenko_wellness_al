# Agent Context Hub

Updated: 2026-06-01 23:40 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as sanitized replay payloads for external contributors.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Standing pilot prices remain `1000 / 6900 / 14900 RUB`.
- Monetization truth is split across three ladders:
  - standing docs and mini-app: `1000 / 6900 / 14900 RUB`
  - bot surfaces and prompts: `500 / 6900 / 14000 RUB`
  - `payment_flow.py`: `screening/week = 700 RUB`, `basic/full/premium/vip = 14900 RUB`
  - the two fresh paid case artifacts still show `payment_context.amount_rub = 6900`
- Fresh runtime proof exists, but it is no longer the latest governing runtime truth:
  - `bot.stderr` shows the successful window from `2026-05-30 23:51:21 +0300` through `23:57:08 +0300`
  - the same file then shows repeated `ProxyConnectionError` against `127.0.0.1:10808` from `2026-05-31 20:47:40 +0300` through `20:53:15 +0300`
  - reconnect happens at `20:53:31 +0300`
  - the run then degrades into repeated `TelegramNetworkError` / `WinError 64` through `20:55:40 +0300`
  - current runtime truth is intermittent proxy-dependent polling, not stable live service
- The PDF/export blocker is locally patched but not yet re-proven:
  - current `WellnessBot/main.py` imports `create_premium_pdf` again
  - current `ops/qa_tester_agent.py` renders PDFs through the normalized dossier path
  - there is still no fresh post-fix paid replay artifact proving dossier delivery now completes
- Disk hygiene is still below the floor:
  - actual `C:` free space is `~8.1 GB` at `2026-06-01 23:40:00 +03:00`
- `WellnessBot/data/runtime_state.json` has no active intake session.
- Latest completed benchmark truth is now anchored to `ops/reports/quality_report_20260531T083403Z.md`:
  - `20` prompts
  - `0` empty replies
- `docs/WELLNESS_DIALOGUE_QA_20260530.md` is now stale:
  - it still says no fresh completed artifact exists
  - it still says benchmark-critical files have no local diff
  - both claims are now false for the current workspace state
- External sync truth in this run:
  - GitHub outward-sync is reachable via git HTTPS in this session (but the workspace has large unreviewed diffs outside `docs/*`)
  - Notion connector: pending verification in this run
  - Google Drive file discovery/create/upload/share tools are not exposed in this session

## Stage

- controlled concierge pilot with fresh benchmark evidence, but runtime is intermittent again, paid replay after the local PDF fix is still unproven, and offer/pricing truth is unstable

## Done

- The successful `2026-05-30 23:51-23:57 MSK` runtime window remains captured as proof that the bot can work on the current stack.
- A second fresh paid case still exists with persisted submission, draft, review, and Obsidian export evidence.
- The repo now contains a local PDF-path patch and a QA-tester PDF normalization patch.
- The latest completed benchmark anchor remains `ops/reports/quality_report_20260531T083403Z.md`.

## Objective

- keep one canonical reviewed Telegram case coherent
- restore one stable runtime mode
- prove a complete paid delivery path from payment through final dossier artifact
- collapse the same-user multi-branch stack into one canonical commercial path
- collapse pricing and offer mapping to one approved ladder
- keep intake, OCR, supplement, and full-tier assignment drift out of product truth until verified

## Product Direction

- Telegram-first only
- manual concierge remains the official pilot mode
- `week` remains the standing entry rail until pricing and package governance are explicitly changed
- do not treat `screening / basic / full` as approved product direction while canonical path ownership, pricing truth, and paid replay are unresolved
- text-first is the only proven intake mode; voice/audio remains removed from the active path

## Current Truth

- `WellnessBot/data/runtime_state.json` has no active user session.
- The governing blocked case remains `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`:
  - `offer = week`
  - `payment_status = manual_payment_confirmed`
  - `intake_status = delivery_blocked_needs_revision`
  - `internal_review.judge_verdict = needs_revision`
  - `requires_lab_resubmission = true`
- The same Telegram user now spans five live-relevant paid paths:
  - `20260501T162705Z_1084557944` = governing blocked `week`
  - `20260505T131604Z_1084557944` = older paid `premium` continuation branch
  - `20260514T213116Z_1084557944` = parked duplicate `premium` placeholder at `consent_pending`
  - `20260530T183208Z_1084557944` = fresh paid `premium` case with manual payment confirmed, `pass_with_major_edits`, and no `canonical_path` metadata
  - `20260530T205040Z_1084557944` = fresh paid `basic` case with manual payment confirmed, `needs_substantial_rewrite`, and no `canonical_path` metadata
- Benchmark-critical runtime/product drift is materially relevant:
  - `WellnessBot/ai_drafting.py` and `WellnessBot/prompts.py` now implement a three-tier drafting/prompt structure
  - `WellnessBot/main.py` and `WellnessBot/texts.py` shift the live funnel to `screening/basic/full`
  - `WellnessBot/payment_flow.py` does not match either the standing pilot ladder or the current surface ladder
  - `WellnessBot/case_service.py` changes submission/session field mapping
  - `WellnessBot/lab_ocr.py` softens OCR filtering
  - `WellnessBot/supplement_product_catalog.py` widens recommendability again
  - `WellnessBot/prompts.py` gives the `full` tier more concrete assignment language than the standing pilot has approved
  - `mini-app/index.html` remains in safer placeholder territory at `1000 RUB`
  - `landing/index.html` still carries proof-style marketing debt and is not verified product truth

## Regressions To Fix Now

- Runtime intermittency: owner `Ops + Lead Developer`; next action decide whether proxy `127.0.0.1:10808` is required, optional with fallback, or dead config, then capture one clean runtime artifact newer than `2026-05-31 20:55 MSK`.
- Paid delivery proof gap: owner `Lead Developer`; next action replay one affected `20260530` paid case on the current code and verify end-to-end dossier generation after payment.
- Disk floor breach: owner `Ops`; next action restore `C:` above `10 GB` before more artifact-heavy work.
- Same-user commercial stack drift: owner `Operator + Lead Developer`; next action collapse the five-path stack to one canonical paid path and archive or freeze the rest.
- Offer/pricing drift: owner `Product Strategist + Lead Developer`; next action collapse the three competing ladders to one approved map across docs, UI, prompts, payment code, and case artifacts.
- Offer-alias collision: owner `Lead Developer`; next action decide whether `basic`, `premium`, and `full` can coexist without branch multiplication, then normalize bot copy, payment flow, and docs to one story.
- Benchmark interpretation drift: owner `Lead Developer`; next action refresh QA synthesis around the completed `2026-05-31` report and the benchmark-critical prompt changes.
- OCR, supplement, and full-tier safety drift: owner `Lead Developer`; next action add proof or rollback before those behaviors count as live truth.

## Next

1. Lock proxy policy for `127.0.0.1:10808` and capture one clean runtime artifact.
2. Replay one fresh paid `20260530` case and verify whether PDF delivery now completes.
3. Collapse the five same-user paid paths to one canonical story.
4. Decide one approved price ladder and normalize every surface to it.
5. Resolve the `basic` / `premium` / `full` offer map so `6900 RUB` means one thing.
6. Restore `C:` above the `10 GB` floor.
7. Refresh QA synthesis around `ops/reports/quality_report_20260531T083403Z.md`.
8. Prove or roll back `case_service.py`, OCR, supplement, and full-tier drift.

## Must-Not-Change Rules

- Telegram-first only
- manual concierge remains the official pilot mode
- standing pilot prices stay `1000 / 6900 / 14900 RUB` until explicitly superseded by reviewed product governance
- one canonical paid path per Telegram user at a time
- human review required before delivery
- no diagnosis or treatment framing
- no unsafe supplement instructions without confirmed context and review
- no active product promise of concrete supplement assignments until the full-tier safety boundary is explicitly approved and verified
- no hardcoded medical-style results on public or TMA surfaces
- do not count a paid path as healthy if payment succeeded but the final dossier artifact is not freshly re-proven on the current code
- do not let `screening / basic / full` or `700 / 14900 / 14900` become product truth without an explicit decision
- do not describe proxy `127.0.0.1:10808` as safe or required without a current proof artifact
- do not describe OCR, supplement, or full-tier widening as safe until verified
- do not describe progress without a fresh proof artifact interpreted by current QA notes

## Context For New Model

Stage:

- controlled concierge pilot with fresh completed benchmark evidence, but runtime is intermittent again, the post-fix paid replay is still unproven, the same user spans five paid-relevant paths, and disk remains below the safety floor

Objective:

- restore one stable runtime path
- restore complete paid delivery after payment
- keep one canonical reviewed Telegram case coherent
- collapse the same-user multi-path stack
- hold unverified pricing, offer mapping, intake, OCR, supplement, and full-tier assignment drift out of product truth
- refresh benchmark interpretation around the new report

Constraints:

- Telegram-first only
- manual concierge and human review remain mandatory
- standing pilot prices remain `1000 / 6900 / 14900 RUB`
- one canonical paid path per Telegram user
- text-only intake is the only currently proven live modality
- disk free space is `9.38 GB`
- latest completed benchmark is `ops/reports/quality_report_20260531T083403Z.md`
- the latest QA synthesis doc is stale and should not be treated as current benchmark interpretation
- Google Drive file discovery/create/upload/share tools are unavailable in the current Codex session

Immediate next actions:

1. Lock proxy policy for `127.0.0.1:10808` and capture one clean runtime artifact.
2. Replay one fresh paid `20260530` case on the current code.
3. Collapse the five same-user paid paths to one canonical path.
4. Decide one approved pricing/menu story and roll every surface to it.
5. Resolve the `basic` / `premium` / `full` offer map conflict.
6. Refresh QA synthesis around the new benchmark report.

Reference proof anchors:

- runtime proof: `bot.stderr`
- benchmark reference: `ops/reports/quality_report_20260531T083403Z.md`
- stale QA synthesis to replace: `docs/WELLNESS_DIALOGUE_QA_20260530.md`
