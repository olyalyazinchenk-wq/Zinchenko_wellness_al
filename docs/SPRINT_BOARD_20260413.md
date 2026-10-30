# Sprint Board

Date: 2026-07-18
Status: July 18 NutriOK controlled build; strategy is stable, release remains blocked by missing intake persistence, missing review artifacts, stale benchmark coverage, no fresh runtime proof, and disk below floor
Sprint owner: Chief Orchestrator
Operating mode: controlled Telegram-first NutriOK validation

## 2026-07-18 16:45 MSK Delta

What changed:

- product direction does not change again; the governing path remains `НутриОК by Olga Kovaleva` with the approved five-step ladder
- the current blocker stack is operational, not conceptual: intake persistence is still incomplete, reviewer evidence is still not an enforced persisted invariant, and the current-product benchmark is still missing
- `ops/agent-sync-status.ps1` now shows `master`, `HEAD=origin/master=a9f0734`, `Published=True`, `TrackedDirtyFiles=22`, `BotTaskState=Ready`, `BotProcessCount=0`, `Synchronized=False`
- this session re-verified 63 passing tests and successful Python compilation without starting Telegram polling
- disk pressure is worse than the earlier same-day hub snapshot: `C:` free space is now `3171799040` bytes (`~2.95 GiB`)
- latest completed benchmark still remains the May 31 report; no completed NutriOK-specific benchmark artifact exists yet

Next 12h command set:

1. Persist goal, baseline, metric, adherence, and three-day diary end to end.
2. Persist reviewer identity, decision, timestamp, and approved artifact for guarded outputs.
3. Build the 20-case NutriOK fixture pack and run the benchmark twice.
4. Capture one fresh scheduled-task runtime proof without starting a second poller.
5. Recover `C:` above `10 GiB` with operator-reviewed cleanup.
6. Split publishable source changes from secrets, logs, lockfiles, and local ops debris.
7. Draft RF retention, deletion, encryption, access, and audit controls.

Sprint success means one release-readiness packet lands, not another strategy rewrite, surface polish pass, or offer expansion.

## Loop Risk

Repeated low-impact tasks to stop:

- strategy refreshes that do not create new runtime, intake, review, or benchmark artifacts
- copy and surface cleanup before the controlled paid cycle is technically enforceable
- offer and supplement expansion before one governed current-product benchmark exists

Replacement action:

- ship one release-readiness control packet:
  1. structured intake persistence
  2. reviewer artifact persistence
  3. current-product benchmark scaffold and first two runs
## 2026-07-16 22:07 MSK Delta

What changed:

- the bot is not running; the last scheduled-task attempt exited on July 1 after Telegram network/proxy failure
- the previous duplicate-poller priority is superseded by runtime recovery through the single permitted scheduled task
- current dossier code explicitly uses `direct_delivery`; named expert approval is not enforced
- a delivered HMS draft contains critical specificity and unsupported-context defects
- 47 submissions map to only two unique Telegram users, so current payment records do not validate demand
- the product direction is one human-reviewed `HMS Clarity Map` pilot at 5,900 RUB
- current `C:` free space is about 4.67 GiB, below the 10 GiB floor
- latest completed benchmark remains the May 31 artifact

Next 12h command set:

1. Repair scheduled-task Telegram connectivity and capture single-owner runtime proof.
2. Hard-block dossier delivery unless a named approval artifact is persisted.
3. Feature-gate all paid offers except the 5,900 RUB HMS pilot.
4. Remove the automatic supplement/affiliate upsell from the HMS path.
5. Convert the unsafe delivered HMS draft into a golden negative fixture.
6. Implement the HMS fact/uncertainty/boundary output contract.
7. Add tests for diagnosis language, invented history, microbe causation, doses, courses, and affiliate leakage.
8. Answer founder qualification, revenue, capacity, channel, and affiliate-priority questions.
9. Recruit five external discovery interviews.
10. Recover `C:` above 10 GiB with operator review.

Sprint success means one result is safe and reviewable, not that another feature or offer exists.

## 2026-06-21 16:40 MSK Delta

What changed:

- runtime continuity is newer than the morning sprint board claimed:
  - `bot.stderr.log` now shows handled updates at `2026-06-21 08:36:49 +03:00`, `08:36:51 +03:00`, `08:36:54 +03:00`, `08:36:56 +03:00`, `08:36:58 +03:00`, and `08:37:00 +03:00`
  - `WellnessBot/data/runtime_state.json` was last written at `2026-06-21 08:37:00 +03:00`
- persisted runtime state is no longer empty, but it is not yet coherent:
  - `user_sessions` now mounts `20260621T053653Z_1084557944`
  - mounted state is `offer = osipov`, `step = osipov_context`, `payment_status = manual_payment_confirmed`, `consent_given = true`, `adult_confirmed = false`
  - `chat_sessions` is still empty
- commercialization control is worse than the morning story:
  - the new mounted case `20260621T053653Z_1084557944` is another `osipov` rail at `5900 RUB`
  - the same user already had delivered `osipov` at `20260618T192846Z_1084557944`
  - the same user also already had delivered `gut_support_18` at `20260619T215149Z_1084557944`
  - both older specialist rails still lack persisted review artifacts
- duplicate polling proof is still unresolved:
  - the current `ops/agent-sync-status.ps1` run still reports `TrackedDirtyFiles = 19`, `BotTaskState = Running`, `BotProcessCount = 2`, `Published = True`, `Synchronized = False`
- public-surface commercialization is still not governed:
  - `landing/index.html` still names `Premium Wellness Dossier` and Telegram support
  - root `index.html` still claims live payment, YooKassa, PDF, and off-map pricing truth
  - `mini-app/index.html` still presents a live `1 000 ₽` rail plus dossier/PDF/support output
- disk pressure worsened again:
  - current `C:` free space from `Get-PSDrive C` is `5226946560` bytes (`~4.87 GiB`)
- governance and QA are still stalled:
  - `WellnessBot/data/product_governance.json` still shows `151` experiments and `0` decisions
  - repeated experiment titles still cluster at `12`, `11`, `8`, `8`, and `5`
  - `docs/tasks` still holds `29` open `HERMES-20260505-*` packets
  - the full batch still dies on prompt `1`

Next 12h command set:

1. Stop the duplicate poller and capture one clean runtime artifact newer than `2026-06-21 08:37:00 +03:00`.
2. Decide whether the `user_sessions` without `chat_sessions` split is expected for `osipov` or a persistence bug, then make runtime, docs, and UX agree.
3. Enforce `direct_delivery` review evidence or an explicit named manual override before any further specialist delivery counts as proof.
4. Audit `20260621T053653Z_1084557944`, `20260618T192846Z_1084557944`, and `20260619T215149Z_1084557944` as one same-user specialist chain.
5. Declare one canonical path across the May 31 / June 18 / June 19 / June 21 same-user stack.
6. Write `canonical_path` or explicit `case_relation` for every non-canonical rail.
7. Add a hard same-user duplicate paid-branch guard.
8. Decide whether `gut_support_18` is approved product truth, feature-gated, or rollback-required.
9. Neutralize landing, root, and mini-app overclaims after the offer map is governed.
10. Recover `C:` back above `10 GiB` with operator delete-review of the known large files.
11. Treat repeated experiment ideation as blocked work until one decision or control artifact lands.
12. Patch `ops/quality_probe.py` and `WellnessBot/ai_drafting.py` only after the control packet above lands.

## Loop Risk

Repeated low-impact tasks to stop:

- rereading sync and strategy docs while the same user can still reopen specialist rails
- adding experiments to governance while `decisions = 0`
- polishing premium-dossier copy before review truth and canonical-path truth are governed

Replacement action:

- ship one case-control packet:
  1. stop duplicate polling
  2. block same-user specialist re-entry
  3. enforce persisted review evidence or named override
  4. gate `gut_support_18`
  5. then clean up public-surface overclaims


