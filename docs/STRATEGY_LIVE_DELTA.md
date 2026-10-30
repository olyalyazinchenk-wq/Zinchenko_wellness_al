# Strategy Live Delta

Rolling log for strategy and plan corrections between major strategy documents.

# 2026-07-18 16:45 MSK

### Artifact Delta

- Re-verified the canonical startup docs, `ops/agent-sync-status.ps1`, current `git status`, benchmark references, and the current NutriOK implementation markers in the working tree.
- Fresh verification in this session: `py -3.12 -m unittest discover -s tests -v` passed with 63 tests; `py -3.12 -m compileall WellnessBot tests` passed.
- Current sync truth: `master`, `HEAD=origin/master=a9f0734`, `Published=True`, `TrackedDirtyFiles=22`, `Synchronized=False`.
- Current runtime truth: scheduled task `WellnessBot` is `Ready`, bot process count is `0`, and no second poller was started in this run.
- Current storage truth: `C:` free space is `3171799040` bytes (`~2.95 GiB`), lower than the earlier same-day snapshot and far below the `10 GiB` floor.
- Latest completed benchmark still remains `ops/reports/quality_report_20260531T083403Z.md`; latest QA synthesis still remains `docs/WELLNESS_DIALOGUE_QA_20260608.md`.

### Product Direction Delta

- Keep the current direction: `НутриОК by Olga Kovaleva` in controlled build, not another strategy pivot.
- The core unit of value stays: one chosen goal, one baseline, one metric, one three-day diary, and one measurable next-step plan.
- Telegram-first and manual-review-first remain the operating model; do not reopen public-launch or multi-surface growth narratives.
- Do not expand offers, supplement paths, or public claims until structured intake persistence, runtime proof, and current-product benchmark coverage exist.

### Monetization Delta

- The approved five-step ladder remains the map, but the active monetization path stays constrained:
  - manual payment only
  - safe `ОК-Экспресс` is the only automated paid output
  - `ОК-Разбор`, `ОК-Результат 8`, `ОК-Ритм`, and every supplement detail remain Olga-reviewed
- No ads, no live automated payment story, and no scale claims before runtime, privacy, reviewer, payment, and benchmark gates pass.

### Plan Delta

1. Persist the structured intake contract end to end: goal, baseline, metric, adherence, and three-day diary.
2. Persist reviewer identity, decision, timestamp, and approved artifact for every full-tier or supplement release.
3. Build 20 de-identified NutriOK fixtures and complete two consecutive current-product benchmark passes.
4. Restore one scheduled-task polling owner and capture a fresh proof-of-life artifact.
5. Recover `C:` above `10 GiB` before replay-heavy QA or artifact generation.
6. Split reviewed product changes from local secrets and runtime debris before any further source publication.
7. Write RF retention, deletion, encryption, access, and audit controls for the intended cloud path.

### Strategy Delta

- Sell accountable clarity and an evidence-backed next step, not a diagnosis, giant PDF, or supplement-first narrative.
- Product differentiation is now only credible if the structured intake and Olga-review trail are persisted, not just described in docs.
- Strategy work should now optimize for release-readiness proof, not another repositioning cycle.

### Inefficiency Loop Delta

- Repeated low-impact loop: rewriting strategy docs while structured intake persistence is still missing.
- Repeated low-impact loop: polishing public surfaces before fresh runtime proof, current-product benchmark proof, and disk headroom exist.
- Repeated low-impact loop: expanding offers or supplement logic before one governed NutriOK benchmark exists.

### Higher-Impact Replacement Action

- Ship one release-readiness control packet before another strategy pass:
  1. intake persistence
  2. reviewer artifact persistence
  3. 20-fixture benchmark scaffold and first two runs

### Goals Delta

- Goal 1: no paid assessment can proceed without the structured intake contract.
- Goal 2: no full-tier or supplement output can proceed without persisted reviewer evidence.
- Goal 3: two consecutive zero-critical NutriOK benchmark runs exist and are newer than May 31.
- Goal 4: one scheduled-task polling owner is proven with a fresh runtime artifact.
- Goal 5: `C:` is back above `10 GiB`.
- Goal 6: only reviewed intentional source changes are candidates for publication.

### Next 12h Command Set

1. Implement end-to-end persistence for goal, baseline, metric, adherence, and three-day diary.
2. Implement persisted reviewer metadata and approved-artifact linkage for every guarded release path.
3. Create the 20-case NutriOK fixture pack and run the benchmark twice.
4. Recover one clean scheduled-task polling proof without starting a second poller.
5. Perform operator-reviewed disk cleanup until `C:` is above `10 GiB`.
6. Separate publishable product files from secrets, logs, and local ops artifacts.
7. Draft RF data-lifecycle and audit controls aligned with the Telegram-first manual-review model.

### Context For New Model

- Stage: `nutriok-controlled-build-2026-07-17-r1`; controlled build / concierge pilot; public launch blocked.
- Done: verified current sync truth, reran 63 tests, reran Python compilation, reconfirmed the approved NutriOK ladder, and re-measured runtime/storage truth.
- Next: persist intake, persist reviewer evidence, build the current-product benchmark, restore fresh runtime proof, recover disk, and split the dirty tree.
- Constraints: one scheduled-task poller only, manual payment only, no diagnosis/treatment framing, Olga approval for full tiers and supplement details, stale benchmark, disk below floor, source tree still mixed.


# 2026-07-17 00:27 MSK

### Artifact Delta

- Implemented the first NutriOK vertical slice: canonical product catalog, legacy migration, prompt contract, deterministic safety/review gate, aligned Telegram menu, root site, landing, mini-app prototype, and tests.
- 63 unit tests and Python compilation pass; Telegram polling was not started.
- Current stage is nutriok-controlled-build-2026-07-17-r1; public launch remains blocked.
- Scheduled task is Ready with zero bot processes.
- Latest completed benchmark remains ops/reports/quality_report_20260531T083403Z.md and predates NutriOK.
- Disk is about 4.31 GiB free, below the 10 GiB floor.
- Notion, Google Drive, and GitHub sanitized artifacts were written and verified by readback.
- Full Git synchronization remains false because the local implementation and pre-existing tracked changes are unpublished.

### Product Direction Delta

- HMS/Osipov is no longer a standalone product; it is an optional input inside a complete nutrition assessment.
- Brand: НутриОК by Olga Kovaleva.
- Promise: Разбор, после которого понятно, что делать.
- One primary goal plus baseline 0-10 and a three-day diary define one assessment cycle.
- Ladder: ОК-Старт, ОК-Экспресс, ОК-Разбор, ОК-Результат 8, ОК-Ритм.

### Monetization Delta

- Pilot prices: 0 / 990 / 5900 / 14900 / 1990 monthly.
- Regular prices: 0 / 1490 / 7900 / 19900 / 1990 monthly.
- The previous payment is credited in full for an upgrade within 30 days.
- Scale gate: 20 unique external Express buyers, at least 8 Full upgrades, at least 4 eight-week upgrades.
- Supplements are optional and secondary; every product, dose, duration, and link requires Olga approval and disclosure.

### Plan Delta

1. Persist structured intake end to end.
2. Persist reviewer identity, approval, timestamp, and approved artifact before full-tier release.
3. Build 20 NutriOK fixtures and pass two consecutive zero-critical-defect runs.
4. Restore scheduled-task Telegram connectivity without a second poller.
5. Recover disk above 10 GiB.
6. Define RF cloud retention, deletion, encryption, access, and audit controls.
7. Conduct five external interviews and prepare the controlled pilot.
8. Publish only reviewed intentional changes from the dirty working tree.

### Strategy Delta

- Sell measurable clarity and an accountable decision process, not diagnosis, PDF volume, or supplement intensity.
- AI structures facts and hypotheses; Olga owns full-tier conclusions.
- Safe Express can be automatic; full tiers and all supplement details cannot.
- No paid advertising before runtime, privacy, reviewer, payment, and benchmark gates pass.

### Goals Delta

- Goal 1: structured goal/baseline/diary persists without data loss.
- Goal 2: no full-tier direct-delivery bypass.
- Goal 3: zero critical defects across two current NutriOK benchmark runs.
- Goal 4: one clean scheduled-task polling owner.
- Goal 5: 20 unique external Express buyers with measured upgrades.
- Goal 6: disk above 10 GiB and RF data controls documented.

### Next 12h Command Set

1. Implement structured intake persistence.
2. Implement persisted named approval invariant.
3. Create the fixture matrix and current benchmark runner.
4. Repair scheduled-task connectivity.
5. Perform operator-reviewed disk recovery.
6. Draft RF privacy and data-lifecycle controls.
7. Recruit five interviews; do not buy traffic.

### Context For New Model

- Stage: NutriOK controlled build; bot down; public launch blocked.
- Objective: release a full nutrition assessment that turns one goal and three days of evidence into a safe measurable plan with Olga accountable for full-tier output.
- Constraints: one poller, manual payment, full-tier approval, no diagnosis/treatment/medication changes, benchmark stale, disk below floor, implementation unpublished.
- Immediate next actions: structured intake, reviewer evidence, fixtures, runtime, disk, RF controls, interviews.
# 2026-07-16 22:07 MSK

### Artifact Delta

- Re-audited canonical docs, dirty bot code, runtime logs/state, submissions/drafts, root/landing/mini-app surfaces, latest benchmark/QA, GitHub, Notion, Drive availability, and channel artifacts.
- Current runtime truth supersedes the June duplicate-poller narrative:
  - scheduled task `WellnessBot` is `Ready`
  - bot process count is `0`
  - last runner start was `2026-07-01 20:11:42 +03:00`
  - runner exited with code `1` after Telegram proxy/direct-network failure
- Current local/remote Git head remains `2968cdb`, but 20 tracked files are dirty.
- Current `C:` free space is `5018693632` bytes (`~4.67 GiB`).
- Latest completed benchmark remains `ops/reports/quality_report_20260531T083403Z.md`; QA anchor remains `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Demand evidence is invalid for market sizing: 47 submissions map to only two unique Telegram users.
- The delivered HMS output and current `direct_delivery` code prove a P0 safety/review regression.

### Product Direction Delta

- Collapse the project from a broad nutritionist bot and six-offer ladder to one human-reviewed product: `HMS Clarity Map`.
- Target people who already have an HMS report; do not drive unnecessary testing.
- AI is the intake/OCR/structuring layer. A named specialist is accountable for final delivery.
- Core V1 excludes diagnosis, treatment, automatic supplement protocols, and affiliate upsells.

### Value Proposition Delta

- Previous: a deep AI-generated wellness dossier with personalized protocols.
- New: independent protection from report overinterpretation, unnecessary interventions, and unclear next steps.
- Differentiation: marker-accounting, uncertainty labels, method limits, doctor-question pack, 14-day observation plan, and reviewer sign-off.

### Monetization Delta

- First ten unique external clients: one `5900 RUB` HMS pilot.
- After release and demand gates: `7900 RUB` core.
- `14900 RUB` 21-day support appears only after at least five core clients request implementation help.
- Affiliate revenue is excluded from the core model until trust, compliance, and separate demand are proven.

### Plan Delta

1. Runtime and safety before traffic.
2. Persisted named approval before every dossier delivery.
3. One product before a ladder.
4. Twenty de-identified fixtures before release.
5. Ten unique external buyers before revenue claims.
6. One CTA and measured funnel before advertising.
7. One canonical offer across every surface.

### Goals Delta

- Goal 1: restore single-owner scheduled-task runtime.
- Goal 2: zero review-gate bypasses.
- Goal 3: zero critical defects across two consecutive HMS fixture runs.
- Goal 4: ten external paid pilots in 30 days.
- Goal 5: at least 80% of completed clients can state the next safe action.
- Goal 6: restore disk above 10 GiB and publish health-data controls.

### Next 12h Command Set

1. Repair scheduled-task proxy/network and capture handled-update proof.
2. Hard-block delivery without persisted named approval.
3. Feature-gate to the 5,900 RUB HMS pilot; remove supplement upsell.
4. Convert the unsafe delivered draft into a golden negative fixture.
5. Write the dedicated HMS fact/uncertainty/boundary schema.
6. Recruit five external interviews and answer founder context questions.
7. Recover disk above 10 GiB with operator review.

### Context For New Model

- Stage: controlled concierge pilot; bot down; public launch blocked.
- Objective: ten external paid, reviewer-approved HMS clarity cases with zero critical defects.
- Constraints: one poller, manual payment, mandatory human approval, no HMS diagnosis/treatment, no core supplement upsell, health-data controls required, benchmark stale, disk below floor.
- Immediate next actions: runtime, review gate, one offer, fixture suite, external interviews.

# 2026-06-21 16:40 MSK
### Artifact Delta
- Re-read the current strategy-driving evidence after the stale `16:38 MSK` onboarding snapshot:
  - `docs/CURRENT_STAGE.json`
  - `docs/AGENT_CONTEXT_HUB.md`
  - `docs/KNOWLEDGE_SYNC_HUB.md`
  - `docs/PROJECT_PULSE_LOG.md`
  - `docs/AGENT_SYNC_PROTOCOL.md`
  - `docs/STRATEGY_LIVE_DELTA.md`
  - `docs/SPRINT_BOARD_20260413.md`
  - `docs/ENGINEERING_MANDATE_20260413.md`
  - current `git status --short --branch`
  - `WellnessBot/data/runtime_state.json`
  - `WellnessBot/data/submissions/20260621T053653Z_1084557944.json`
  - `WellnessBot/data/product_governance.json`
  - `WellnessBot/data/submissions/20260531T183007Z_1084557944.json`
  - `WellnessBot/data/submissions/20260618T192846Z_1084557944.json`
  - `WellnessBot/data/submissions/20260619T215149Z_1084557944.json`
  - current `bot.stderr.log`
  - current `Get-PSDrive C`
  - current `landing/index.html`, root `index.html`, and `mini-app/index.html`
- New hard facts for the strategy layer:
  - current local run time is `2026-06-21 16:40:06 +03:00`
  - the current `ops/agent-sync-status.ps1` run still reports `TrackedDirtyFiles = 19`, `BotTaskState = Running`, `BotProcessCount = 2`, `Published = True`, `Synchronized = False`
  - `bot.stderr.log` now contains newer handled updates at `2026-06-21 08:36:49 +03:00`, `08:36:51 +03:00`, `08:36:54 +03:00`, `08:36:56 +03:00`, `08:36:58 +03:00`, and `08:37:00 +03:00`
  - `WellnessBot/data/runtime_state.json` is no longer empty; it was last written at `2026-06-21 08:37:00 +03:00`
  - the mounted runtime state is now `submission_id = 20260621T053653Z_1084557944`, `offer = osipov`, `step = osipov_context`, `payment_status = manual_payment_confirmed`, `consent_given = true`, `adult_confirmed = false`
  - the matching persisted submission exists and confirms a fresh same-user specialist re-entry at `5900 RUB`
  - `chat_sessions` is still empty even though `user_sessions` is no longer empty
  - the older specialist-delivery breaches still remain unresolved:
    - `20260618T192846Z_1084557944` = delivered `osipov`, `direct_delivery = true`, `adult_confirmed = false`, no persisted review artifact
    - `20260619T215149Z_1084557944` = delivered `gut_support_18`, `direct_delivery = true`, `adult_confirmed = true`, `source_submission_id = 20260618T192846Z_1084557944`, no persisted review artifact
  - `20260531T183007Z_1084557944` still remains delivered despite `internal_review.judge_verdict = fail_major_issues`
  - current `C:` free space is `5226946560` bytes (`~4.87 GiB`)
  - public surfaces still overclaim beyond the governed pilot
  - `WellnessBot/data/product_governance.json` still holds `151` experiments and `0` decisions, and the top repeated experiment titles still cluster at `12`, `11`, `8`, `8`, and `5`

### Product Direction Delta
- Product direction stays `Telegram-first controlled concierge`, but the new June 21 correction is harsher than the morning story:
  - runtime continuity is fresher
  - commercialization control is worse
  - the same user has now re-entered `osipov` before the earlier `osipov` and `gut_support_18` specialist deliveries were review-traceable or canonically owned
- The operating direction therefore narrows again:
  - one governed entry rail
  - one canonically owned specialist path
  - no second specialist or paid branch for the same user until review evidence and case ownership are explicit

### Value Proposition Delta
- The only defensible live value proposition remains:
  - `human-reviewed nutrition navigation in Telegram with explicit safety, escalation, and manual review boundaries`
- Do not market a stronger proposition yet:
  - not `stable automated dossier pipeline`
  - not `specialist ladder that can safely loop the same user through repeat paid branches`
  - not `live payment + PDF fulfillment system`

### Monetization Delta
- Official monetization posture remains `manual concierge first`.
- The near-term monetization path must now contract further:
  - one governed `1490 RUB` entry rail under one canonical name
  - one explicitly governed specialist escalation path
  - no same-user specialist re-entry until old direct-delivery rails have review evidence and canonical ownership
- Therefore:
  - the new `20260621T053653Z_1084557944` `osipov` rail is demand evidence, not healthy proof
  - the earlier `osipov` and `gut_support_18` deliveries remain commercialization debt, not reusable proof
  - landing/root/mini-app copy still overstates what is safely live

### Plan Delta
1. Stop the duplicate poller and capture one clean runtime artifact newer than `2026-06-21 08:37:00 +03:00`.
2. Explain or repair the runtime-state split: `user_sessions` now mounts a live case while `chat_sessions` stays empty and polling ownership is still unresolved.
3. Block new same-user specialist or paid re-entry until `canonical_path` or `case_relation` is written across the existing stack.
4. Add a hard `direct_delivery` gate that requires a persisted review artifact or explicit named manual override.
5. Audit the relation between `20260621T053653Z_1084557944`, `20260618T192846Z_1084557944`, and `20260619T215149Z_1084557944`.
6. Freeze `gut_support_18` behind explicit approval or roll it back from the live path.
7. Neutralize landing/root/mini-app overclaims to the surviving Telegram-first truth.
8. Recover `C:` above the `10 GiB` floor before replay-heavy benchmark work.

### Inefficiency Loop Delta
- Repeated low-impact loop:
  - refreshing docs and sync status while the same user can still open a new specialist rail before earlier specialist rails are review-traceable or canonically owned
- Repeated low-impact loop:
  - adding experiments to a `151`-item governance file with `0` decisions and repeated titles
- Repeated low-impact loop:
  - polishing premium-dossier messaging on landing, root, and mini-app before delivery truth and same-user ownership are governed

### Higher-Impact Replacement Action
- Run one case-layer control packet before more strategy churn:
  1. stop the competing poller and capture one clean post-fix runtime artifact
  2. block same-user specialist re-entry until `canonical_path` and review evidence exist
  3. enforce persisted review evidence or explicit named override before any `direct_delivery`
  4. feature-gate `gut_support_18` until the approved ladder is explicit
  5. then neutralize public-surface overclaims and return to benchmark transport work

### Goals Delta
- Goal 1: restore one intentional polling owner with fresh proof after `2026-06-21 08:37:00 +03:00`.
- Goal 2: make runtime state coherent again, not merely non-empty.
- Goal 3: make direct-delivery specialist rails review-traceable.
- Goal 4: collapse the same-user paid stack into one governed path that can block re-entry duplication.
- Goal 5: replace low-impact experiment churn with one approved case-control packet.
- Goal 6: restore `C:` above the `10 GiB` floor.

### Next 12h Command Set
1. Stop the duplicate poller and capture one clean runtime artifact newer than `2026-06-21 08:37:00 +03:00`.
2. Determine whether the `user_sessions` without `chat_sessions` split is expected for `osipov` or a persistence bug.
3. Enforce `direct_delivery => review artifact or named manual override`.
4. Audit `20260621T053653Z_1084557944`, `20260618T192846Z_1084557944`, and `20260619T215149Z_1084557944` as one same-user specialist chain.
5. Repair `20260531T183007Z_1084557944`.
6. Write `canonical_path` or `case_relation` across the same-user stack.
7. Add a hard same-user duplicate paid-branch guard.
8. Decide whether `gut_support_18` is approved, feature-gated, or rollback-required.
9. Neutralize landing, root, and mini-app overclaims to the surviving Telegram-first truth.
10. Recover `C:` above `10 GiB`.

### Context For New Model
- Stage:
  - `controlled-concierge-pilot-2026-06-18-r1`
- Done:
  - re-verified the shared control docs, target strategy docs, runtime evidence, delivery evidence, and public surfaces in the canonical workspace
  - corrected the stale claim that `runtime_state.json` is empty
  - confirmed a fresh same-user `osipov` re-entry at `2026-06-21 08:37:00 +03:00`
  - reconfirmed missing specialist review artifacts, the legacy delivered-case contradiction, and repeated experiment churn
- Next:
  - restore single-owner polling
  - explain or repair the runtime-state split
  - block same-user specialist re-entry until canonical ownership exists
  - add the persisted review gate
  - then trim public-surface overclaims

# 2026-06-21 04:40 MSK
### Prior Snapshot
- The morning refresh still believed `runtime_state.json` was empty and that the freshest handled updates were only the June 20 `05:26 +03:00` sequence.
- The new `16:40 MSK` section above supersedes that stale runtime-state assumption.


