# Agent Context Hub

Updated: 2026-06-07 11:51 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as sanitized replay payloads for external contributors.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Freshest runtime proof in `bot.stderr` now includes:
  - `2026-06-03 21:47:11-21:47:13 +03:00` direct-fallback startup and polling start
  - `2026-06-05 00:32:10 -> 00:32:22 +03:00` last known auto-recovery from the earlier SSL series
  - `2026-06-06 23:25:02-23:25:31 +03:00` handled bot updates; no newer live proof has landed after that point in this run
- Current runtime truth: the expired June 3 `nutri_chat` rail is still displaced. The active runtime rail remains `20260606T202509Z_1084557944` with `offer = habits`, `step = habits_daily_log`, and one daily-log entry.
- Lead blocker: duplicate same-offer paid-path multiplication plus the older delivered-case review contradiction. Runtime is live enough for a controlled pilot, but the proof has not advanced since late June 6.
- Latest hard breach: `20260531T183007Z_1084557944` is still `delivered_to_client` while `internal_review.judge_verdict = fail_major_issues`.
- Current disk state: `C:` free space is `7307649024` bytes (`~6.81 GiB`) at `2026-06-07 11:51:32 +03:00`, still below the `10 GB` floor and slightly worse than the late June 6 reading.
- Latest completed benchmark anchor: `ops/reports/quality_report_20260531T083403Z.md`.
- Current benchmark interpretation doc: `docs/WELLNESS_DIALOGUE_QA_20260605.md`.
- Current QA status: routing tests and smoke still pass, but the full batch still aborts on prompt `1` because `ops/quality_probe.py` still fails all-or-nothing on model-path connection errors.
- Current repo delta:
  - tracked docs changes remain open
  - `ops/bot-status.ps1` still has a tracked local monitoring patch that resolves the latest `bot.stderr` and `bot.stdout` files before tailing
  - untracked runtime artifacts still include `bot.stderr`, `bot.stdout`, `.bot.lock`, local backup files, the QA note file, and `ops/skills/graphify-codex/`
- External sync status in this cycle:
  - Notion run note: created as page `3788a9de-1d41-817c-95d5-e0a86315f984`
  - Notion hub page `AGENT CONTEXT HUB — Antigravity / Wellness`: prepended with a fresh `Context For New Model — 2026-06-07 11:51 MSK` block
  - GitHub sanitized artifacts:
    - `antigravity_sync_20260607T085132Z.md` -> `5df38b3c676bbd8d6d2e4095868483cb6b31f60a`
    - `antigravity_context_snapshot_20260607T085132Z.md` -> `73fd849e7e04a0ea951249ccfd09e1b39fbae9ca`
    - `2026-06-07_1151_sync_blocked.md` -> `1d288c3e06a2a1abd8f2d0e50d4dc0d81df827e2`
  - Google Drive upload/share: blocked because no file discovery/create/upload/share tools are exposed

## Stage

- Controlled concierge pilot where runtime was freshly re-proven late on June 6 and remains stable enough for a controlled pilot, but commercialization control is still regressing into duplicate paid `habits` paths for the same user while the older delivered case still conflicts with failed review.

## Done This Cycle

- Re-read the latest state across `docs`, `WellnessBot`, `mini-app`, `landing`, `ops/reports`, runtime logs, persisted submissions, and governance artifacts.
- Re-validated `WellnessBot/data/runtime_state.json` and confirmed that the mounted rail is still the June 6 `habits` daily-log path rather than the expired June 3 `nutri_chat` rail.
- Re-checked `bot.stderr` and confirmed that no newer runtime evidence displaced the June 6 `23:25` handled-update proof.
- Re-measured current disk headroom and confirmed a slight slip from the late-night reading while the `10 GB` floor is still breached.
- Re-checked current working-tree truth and confirmed that the tracked `ops/bot-status.ps1` monitoring patch is still the only non-doc tracked delta.
- Wrote the June 7 Notion run note, prepended the Notion hub context block, and synced the new sanitized GitHub artifacts for external contributors.
- Refreshed the required pulse log, strategy delta, sprint board, agent-context handoff, Obsidian mirror, and outward-sync artifacts.

## Objective

- Keep one canonical paid path per Telegram user.
- Preserve the recently proven live runtime without re-opening stale outage narratives.
- Repair the delivered-case contradiction before counting higher-ticket proof as valid.
- Stop same-user same-offer paid-branch multiplication.
- Restore per-prompt QA visibility so model-path failures stop hiding the benchmark state.
- Keep the public proof story narrower than the landing currently claims.

## Product Direction

- Telegram-first only.
- Manual concierge remains the official pilot mode.
- Treat `habits` as a live commercial rail only after one canonical `habits` path exists per user.
- Treat `nutri_chat`, `week`, `basic`, `full`, `vip`, and `premium` naming as non-canonical until one approved map is normalized across code, docs, prompts, and persisted artifacts.
- Text-first is the only proven live modality; voice and audio remain removed from the active path.
- Keep the mini-app in safe placeholder-only territory until pricing, delivery, and public proof are governed.
- Do not treat landing as approved proof while its case-study metrics remain hardcoded.

## Current Truth

- `WellnessBot/data/runtime_state.json` currently uses `user_sessions` plus `chat_sessions`:
  - `submission_id = 20260606T202509Z_1084557944`
  - `offer = habits`
  - `tier = habits`
  - `step = habits_daily_log`
  - `payment_status = manual_payment_confirmed`
  - `amount_rub = 6900`
  - `daily_logs[0].created_at = 2026-06-06T20:25:31Z`
  - `daily_logs[0].text = "Р§С‚Рѕ РґРµР»Р°РµРј?"`
  - `chat_sessions` is currently empty
- The freshest runtime proof is still the handled-update sequence at `2026-06-06 23:25:02-23:25:31 +03:00`; no newer proof landed in this June 7 morning cycle.
- The same user still holds unresolved recent paid state across multiple rails:
  - `20260603T112723Z_1084557944` = `nutri_chat`, `500 RUB`, still `manual_payment_pending`
  - `20260603T113045Z_1084557944` = `habits`, `6900 RUB`, `manual_payment_confirmed`
  - `20260606T202509Z_1084557944` = `habits`, `6900 RUB`, `manual_payment_confirmed`, and now mounted as active runtime state
- `WellnessBot/data/submissions/20260531T183007Z_1084557944.json` still combines:
  - `offer = basic`
  - `amount_rub = 14900`
  - `intake_status = delivered_to_client`
  - `internal_review.judge_verdict = fail_major_issues`
- Governance debt remains unchanged:
  - `WellnessBot/data/product_governance.json` still contains `151` experiments and `0` decisions
  - top duplicate title counts remain `12`, `11`, `8`, `8`, and `5`
- Current benchmark truth:
  - latest completed benchmark anchor is still `ops/reports/quality_report_20260531T083403Z.md`
  - current interpretation doc is `docs/WELLNESS_DIALOGUE_QA_20260605.md`
  - the batch run still aborts on prompt `1`
- Current surface truth:
  - `mini-app/index.html` still renders a safe placeholder result and should stay placeholder-only
  - `landing/index.html` still contains hardcoded proof and case-study framing that should not be treated as live proof

## Regressions To Fix Now

- Duplicate same-offer paid-path multiplication: owner `Operator + Lead Developer`; next action declare one canonical `habits` path between the June 3 and June 6 paid branches, then freeze, merge, refund, or archive the duplicate.
- Delivery-gate breach: owner `Lead Developer + Operator`; next action audit `20260531T183007Z_1084557944`, record whether any manual override existed, and remove or remediate the `delivered_to_client` contradiction if `fail_major_issues` still stands.
- Disk floor breach: owner `Ops`; next action restore `C:` above `10 GB` before more artifact-heavy work.
- Benchmark observability gap: owner `Lead Developer`; next action make `ops/quality_probe.py` emit partial per-prompt artifacts when the model path fails.
- Landing proof overclaim: owner `Product Strategist + Lead Developer`; next action remove or neutralize the hardcoded case-study metrics before using landing as live proof.
- Stagnant runtime proof cadence: owner `Ops`; next action keep monitoring for a post-June-6 proof artifact, but do not let runtime narration displace the higher-priority commercialization and QA control fixes.
- Governance indecision debt: owner `Chief Orchestrator`; next action turn the duplicate-path and delivery-gate fixes into explicit decisions before adding more experiments.

## Next

1. Restore `C:` above the `10 GB` floor.
2. Decide whether `20260603T113045Z_1084557944` or `20260606T202509Z_1084557944` is the canonical `habits` case.
3. Add a hard guard so a second paid branch for the same offer and user cannot be created while another paid path is still active or unresolved.
4. Audit `20260531T183007Z_1084557944` and repair the delivery-gate contradiction.
5. Patch `ops/quality_probe.py` so prompt-level model failures still emit partial artifacts.
6. Re-run the batch benchmark only after step `5`.
7. Neutralize landing-page case metrics before using landing as live proof.

## Must-Not-Change Rules

- Telegram-first only.
- Manual concierge remains the official pilot mode.
- No price ladder becomes product truth until one approved map is written across code, docs, and artifacts.
- One canonical paid path per Telegram user at a time.
- No second paid branch for the same offer and same user while an older paid path is still active or unresolved.
- Human review is required before delivery.
- No diagnosis or treatment framing.
- No unsafe supplement instructions without confirmed context and review.
- No hardcoded medical-style results on public or TMA surfaces.
- Do not count a paid path as healthy if payment succeeded but the final reviewed artifact is contradicted by failing review state.
- Do not treat governance backlog growth as execution progress.
- Do not describe progress without a fresh proof artifact interpreted by the current QA notes.

## Context For New Model

Stage:

- Controlled concierge pilot where runtime was freshly re-proven on June 6 and remains stable enough for a controlled pilot, but commercialization control is still regressing into duplicate paid `habits` paths for the same user while the older delivered case still conflicts with failed review.

Objective:

- Keep one canonical paid path per user.
- Repair the delivered-case contradiction.
- Restore benchmark observability.
- Remove landing proof overclaims while keeping the bot stable.

Constraints:

- Telegram-first only.
- `PAYMENT_MODE=manual`.
- Human review remains mandatory.
- One canonical commercial path per Telegram user.
- Text-only intake is the only proven live modality.
- Disk free space is `7307649024` bytes (`~6.81 GiB`), still below the `10 GB` floor.
- Latest completed benchmark is `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA synthesis doc is `docs/WELLNESS_DIALOGUE_QA_20260605.md`.
- The batch benchmark still fails on prompt `1`.
- Google Drive file discovery/create/upload/share tools are unavailable in the current Codex session.

Immediate next actions:

1. Restore disk above `10 GB`.
2. Canonicalize the duplicate paid `habits` stack.
3. Add a duplicate paid-path guard.
4. Repair the delivered-case review contradiction.
5. Patch partial-artifact QA capture.
6. Neutralize landing-page proof claims.

Reference proof anchors:

- runtime proof: `bot.stderr`
- benchmark reference: `ops/reports/quality_report_20260531T083403Z.md`
- current QA interpretation: `docs/WELLNESS_DIALOGUE_QA_20260605.md`
