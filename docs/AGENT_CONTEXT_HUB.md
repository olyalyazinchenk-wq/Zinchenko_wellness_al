# Agent Context Hub

Updated: 2026-05-30 11:33 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as sanitized replay payloads for external contributors when connectors recover.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Official pilot prices remain `3900 / 6900 / 14900 RUB`.
- Top product-truth defect: the governing `week` case `20260501T162705Z_1084557944` is correctly blocked instead of falsely delivered, but the same user still carries a payment-confirmed `premium` branch that should be treated as parked until explicitly merged, and the live runtime is still showing sustained duplicate polling plus stale health/proxy narration.
- `WellnessBot/data/runtime_state.json` is still empty, so runtime memory is not the live storage blocker.
- No newer positive runtime or QA proof landed after the May 13 refresh:
  - latest benchmark reference is still `ops/reports/quality_report_20260506T080435Z.md`
  - the newest runtime artifact is sustained negative proof:
    - startup proxy is `http://127.0.0.1:10808`
    - one reconnect landed at `2026-05-14 16:47:03 +0300`
    - polling resumed repeated `TelegramConflictError` from `2026-05-14 16:48:04 +0300` through `2026-05-14 16:55:57 +0300`
    - the latest visible local health result is still `GET /health -> 404` at `2026-05-13 21:24:04 +0300`
- Disk hygiene is below the floor and has regressed further:
  - actual `C:` free space is `5.85 GB` at `2026-05-30 11:33:39 +03:00`
- Sync/connector truth updated in this run (`2026-05-30 11:33 MSK`):
  - GitHub remote is reachable via git HTTPS (`git ls-remote origin` is OK)
  - Notion connector is reachable (page fetch is OK)
- Bot runtime is now evidenced as live-but-conflicted:
  - latest visible startup is `2026-05-13 21:22:17-21:22:18 MSK`
  - TMA server started at `http://localhost:8000`
  - live startup proxy is `http://127.0.0.1:10808`
  - polling conflicts imply more than one bot instance is active through `2026-05-14 16:55 MSK`
  - one reconnect at `2026-05-14 16:47:03 MSK` did not hold
  - latest local probe is still `GET /health -> 404` at `2026-05-13 21:24:04 +0300`
  - no clean single-instance or healthy-endpoint proof exists yet
- Repo state:
  - latest local commit is `d332374` (`chore(sync): status snapshot (2026-05-14 16:56 MSK)`)
  - `master` matches `origin/master` at `d332374`, but the working tree is dirty
  - dirty code changes exist in `WellnessBot/` and `mini-app/` (see below); treat as not-yet-verified
  - untracked local-only artifacts exist: `.venv_wsl/`, `WellnessBot/.bot.lock`, `WellnessBot/main_backup_2026-05-17*.py`, `run_bot_wsl.sh` (must not be committed)
- External sync surface:
  - Obsidian local mirror is available
  - Notion sync is available (connector works)
  - GitHub sync is available (git HTTPS works)
- Latest benchmark reference remains `ops/reports/quality_report_20260506T080435Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions remain `6/9` on model-path symptom prompts
  - invented-name hallucination still appears twice
  - `5/9` model-path replies still exceed `2000` characters
- Loop pressure is still visible:
  - `127` proposed experiments remain in `WellnessBot/data/product_governance.json`
  - `29` `docs/tasks/HERMES-20260505-*` packets remain open as backlog inventory

## Working Tree Risk (uncommitted)

Do not treat the current working tree as deployable until it is reviewed and tested. The local changes include:

- `WellnessBot/main.py`: intake step order/wording refactor + main menu buttons changed; voice/audio intake code removed/disabled.
- `WellnessBot/lab_ocr.py`: OCR line filter softened (no longer requires known marker aliases; additional "skip" heuristics).
- `WellnessBot/supplement_product_catalog.py`: broadened recommendability, including previously discontinued iron reference (high safety/compliance risk).
- `mini-app/index.html`: wording + pricing copy adjusted; result screen converted to a safer placeholder (no hardcoded medical findings).

## Stage

- controlled concierge pilot with delivery-blocked state preserved on the governing case, but no fresh positive proof artifact; canonical case ownership, sustained runtime-instance conflict, working-tree safety drift, benchmark freshness, and disk headroom remain unstable

## Done

- The governing `week` case is blocked instead of silently delivered.
- Three stale same-user branches are archived instead of pretending to be live proof.
- The disk floor breach is explicitly documented and is now a worsening ops risk.
- The mini-app no longer shows the old hardcoded diagnosis/supplement-style demo result.
- The connector outcomes for Notion and GitHub were verified in the current `2026-05-30 11:33 MSK` run.
- Encoding readability for `docs/PROJECT_PULSE_LOG.md` was repaired (`UTF-8 with BOM`) so RU log sections no longer degrade into mojibake.
- Replay-ready outward-sync artifacts were refreshed locally.
- The same-day strategy baseline is current; no stale blocker narrative from May 8 is needed to explain the live state.
- The runtime conflict is now documented as a sustained same-day regression rather than a startup-only artifact.

## Objective

- keep one canonical reviewed Telegram case coherent
- preserve the now-blocked delivery state until review truth and lab truth align
- collapse the same-user `week` / `premium` sprawl into one canonical path
- resolve unsafe working-tree drift around voice/audio intake, supplement recommendations, and OCR parsing
- prove or explicitly accept the current proxy-backed polling path
- tighten first-line model replies before the next proof cycle
- keep local and replay-ready outward-sync context aligned even while connectors are blocked

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the validated paid entry rail
  - `premium` remains the flagship offer
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery
- `premium` must be expressed as a same-case continuation, not as a second active branch for the same Telegram user

## Current Truth

- `WellnessBot/data/runtime_state.json` is empty.
- The governing case remains `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`:
  - payment confirmed
  - status: `delivery_blocked_needs_revision`
  - internal review still says `needs_revision`
  - `delivery_blocked_at = 2026-05-11T06:56:00Z`
  - no explicit delivery override note is present
  - active lab-state remains unsafe:
    - `lab_quality_check.status = missing`
    - `lab_quality_check.requires_resubmission = true`
    - `requires_lab_resubmission = true`
    - current parsed biomarker set still mixes real markers with narrative/protocol-like lines
- The same user now has one governing `week` branch plus one unresolved fresh paid `premium` branch:
  - `20260501T162705Z_1084557944` = governing blocked `week`
  - `20260505T131604Z_1084557944` = payment-confirmed `premium` with `intake_status = review_priority_quality_and_market`; treat as parked non-canonical until explicit merge
  - `20260427T173913Z_1084557944` = archived test run
  - `20260425T214914Z_1084557944` = archived test run with resubmission history
  - `20260425T212847Z_1084557944` = archived test run with rewrite-only history
- Landing still matches the Telegram-first funnel, but it uses hardcoded proof-style case-copy and biomarker deltas that should be treated as unverified marketing debt.
- Mini-app local drift improved:
  - `2990` pricing is gone
  - result output is now a safer placeholder
  - it still does not count as backend-fed reviewed proof
- Working-tree runtime/product drift is now materially relevant:
  - voice and audio intake are disabled in `WellnessBot/main.py`
  - supplement catalog changes now allow a discontinued iron product to surface as recommendable
  - OCR filtering is broader and should be revalidated against noisy text
- Latest QA synthesis still says:
  - router overreach is no longer the main blocker
  - invented names, over-familiar tone, broad early mechanism stacking, duplicated emergency/service templates, and overlong replies remain the live quality risks
- Current runtime evidence is still live-but-fragile:
  - the bot now proves startup on a proxy-backed path logged as `127.0.0.1:10808`
  - the active polling path is not trustworthy yet because duplicate instances are still colliding in the latest same-day log tail
  - one reconnect at `2026-05-14 16:47:03 +0300` did not stabilize polling, and conflicts continue through `2026-05-14 16:55:57 +0300`
  - the stable-vs-fragile transport question remains open because the health path still returns `404`
- Current external-sync evidence:
  - Notion search failed again in the current `2026-05-14 16:56 MSK` run during MCP initialize handshake
  - GitHub installed repository search failed again in the current `2026-05-14 16:56 MSK` run during MCP initialize handshake
  - Google Drive file tools are not exposed in the session
  - replay-ready local artifacts were created instead

## Regressions To Fix Now

- Governing-case review/lab block: owner `Lead Developer + Operator`; next action keep `20260501T162705Z_1084557944` blocked until review truth, override truth, and follow-up lab truth align.
- Same-user commercial stack drift: owner `Operator + Lead Developer`; next action record whether `20260505T131604Z_1084557944` is `merge-into-canonical` or parked.
- Voice/audio intake capability regression: owner `Lead Developer`; next action decide whether voice/audio intake is intentionally removed and update product/docs, or restore a safe STT path.
- Supplement catalog safety/availability regression: owner `Lead Developer`; next action stop recommending discontinued iron products as active options and reinstate hard exclusions around self-directed iron use.
- OCR parsing drift risk: owner `Lead Developer`; next action validate the softer filter against obvious non-marker noise before trusting broader extraction.
- Runtime instance conflict and transport ambiguity: owner `Ops + Lead Developer`; next action stop duplicate polling, decide whether proxy is mandatory, and prove one clean health path that does not end in `404` after the sustained conflict window logged through `2026-05-14 16:55 MSK`.
- Model-path response discipline: owner `Lead Developer`; next action harden prompt + sanitizer + template separation + benchmark assertions.
- Disk headroom regression: owner `Ops`; next action restore free space above `10 GB` before more artifact generation pushes the workstation further under margin.
- Connector recovery: owner `Tooling / Access`; next action restore Notion and GitHub MCP handshake and expose Google Drive file operations in-session.

## Next

1. Restore `C:` above the `10 GB` floor.
2. Keep the governing `week` case blocked until review and lab truth align.
3. Decide how `20260505T131604Z_1084557944` relates to the governing `week` case; until then, treat it as parked and non-canonical.
4. Stop duplicate polling and decide which bot instance is canonical.
5. Decide whether to restore or formally retire voice/audio intake.
6. Roll back discontinued-iron recommendation drift and revalidate OCR parsing.
7. Decide whether the runtime may depend on `127.0.0.1:10808`; if not, add a fallback and prove one clean post-fix path.
8. Tighten live-answer sanitization, prompt rules, and template separation against the `2026-05-06` QA regressions.
9. Freeze net-new experiment / task-packet churn until the runtime and canonical-path proof bundle lands.
10. Produce one fresh runtime or QA proof artifact before spending another cycle on strategy churn.
11. Replay Notion, GitHub, and Google Drive sync once connector access is fixed.

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
- do not treat `delivery_blocked_needs_revision` as solved until the governing case itself is coherent
- do not let the same user carry both a blocked `week` truth defect and an active unclassified premium storyline
- do not count the standalone paid `premium` branch as traction before canonical merge
- do not silently retire voice/audio intake without aligning docs and offer truth
- do not let broadened OCR parsing or broadened supplement recommendability silently become client truth
- do not allow multiple live polling instances or stale proxy assumptions to become accepted runtime truth
- do not call polling resilience fixed before one clean post-fix verification passes
- do not treat connector recovery as proof that delivery truth, file truth, or runtime resilience are solved
- do not describe progress without a fresh proof artifact when the latest runtime and QA evidence are still May 8 / May 6
- do not spend another same-day strategy loop before one fresh proof artifact lands
- do not add more experiment or task-packet inventory while the runtime and canonical-path proof bundle is still open
- do not let planning or governance churn outrun delivery safety, lab truth, and canonical state truth

## Context For New Model

Stage:

- controlled concierge pilot with delivery-gate repair partly landed, but no fresh positive proof artifact; lab truth, supplement safety, intake-modality truth, sustained runtime-instance conflict, model-path response discipline, and external connectors still unstable

Done:

- `20260501T162705Z_1084557944` is blocked instead of silently delivered
- three stale same-user branches are archived
- the disk floor breach is now explicitly documented
- mini-app hardcoded diagnosis/supplement demo content is largely removed
- runtime conflict is now explicitly documented through `2026-05-14 16:55 MSK`

Objective:

- keep one canonical reviewed Telegram case coherent
- preserve the blocked delivery state until review and lab truth align
- collapse the same-user branch sprawl to one canonical path
- resolve unsafe runtime/product drift around voice/audio intake, supplement recommendations, and OCR parsing
- prove or explicitly accept the current proxy-backed polling path
- tighten first-line model replies before the next proof cycle
- keep replay-ready outward sync current while connectors are unavailable

Constraints:

- Telegram-first only
- manual concierge remains official pilot mode
- official pilot prices remain `3900 / 6900 / 14900 RUB`
- human review required before delivery
- one canonical paid path per Telegram user
- one active polling instance
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA / public surfaces
- do not silently disable intake modalities without updating pilot truth
- latest runtime artifact uses `http://127.0.0.1:10808`, briefly reconnects, and still collides with another poller
- disk free space is only `9.82 GB`
- Notion connector is blocked by the MCP handshake failure verified again in the current `2026-05-14 16:56 MSK` run
- GitHub connector is blocked by the MCP handshake failure verified again in the current `2026-05-14 16:56 MSK` run
- Google Drive file create/upload/share tools are unavailable in the current Codex session

Immediate next actions:

1. Restore `C:` above the `10 GB` floor.
2. Keep `20260501T162705Z_1084557944` blocked until review truth and lab truth align.
3. Explicitly classify the same-user `week` / `premium` stack; until then, treat `20260505T131604Z_1084557944` as parked.
4. Stop duplicate polling and prove one clean runtime path.
5. Decide whether to restore or formally retire voice/audio intake.
6. Roll back discontinued-iron recommendation drift and revalidate OCR parsing.
7. Prove runtime health without ambiguous proxy assumptions.
8. Freeze net-new experiment / task-packet churn until the runtime and canonical-path proof bundle lands.
9. Produce one fresh runtime or QA proof artifact after the safety-sensitive path is verified.
10. Replay Notion / GitHub / Google Drive sync when connector access is fixed.

Reference benchmark:

- `ops/reports/quality_report_20260506T080435Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260506.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `6/9` clarifying-question coverage on model-handled symptom prompts
