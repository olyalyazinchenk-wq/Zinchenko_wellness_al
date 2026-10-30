# Engineering Mandate

Date: 2026-07-18
Issued by: Chief Orchestrator
Status: July 18 refresh; engineering must treat NutriOK controlled build as the stable direction and focus on the missing release-readiness packet: structured intake persistence, persisted reviewer evidence, current-product benchmark proof, fresh scheduled-task runtime proof, and disk recovery above the floor
## Mission

Run one coherent NutriOK Telegram cycle through:

`approved product choice -> manual payment -> structured intake -> AI draft -> Olga review -> safe delivery -> same-thread follow-up`

No new tariff, catalog branch, supplement path, or public promise counts as live truth until the current release-readiness packet exists in code and artifacts. Public launch remains blocked.

## 2026-07-18 16:45 Correction Set

Use this correction set wherever it conflicts with older June or July assumptions.

- Treat the product direction as stable:
  - the governing path remains `НутриОК by Olga Kovaleva`
  - the approved five-step ladder remains the map
  - Telegram-first and manual-review-first remain mandatory
  - do not spend engineering cycles on another positioning pivot
- Treat the current blocker stack as implementation debt, not strategy ambiguity:
  - structured intake fields are still not persisted end to end
  - reviewer identity, decision, timestamp, and approved artifact are still not an enforced persisted invariant
  - no completed NutriOK-specific benchmark artifact exists yet
- Treat current verification as real and current:
  - `py -3.12 -m unittest discover -s tests -v` passed with `63` tests in this session
  - `py -3.12 -m compileall WellnessBot tests` passed in this session
  - `ops/agent-sync-status.ps1` now reports `HEAD=origin/master=a9f0734`, `TrackedDirtyFiles=22`, `BotTaskState=Ready`, `BotProcessCount=0`, `Published=True`, `Synchronized=False`
- Treat runtime as `not currently process-verified healthy`:
  - the scheduled task is `Ready`
  - bot process count is `0`
  - no second poller was started in this run
  - engineering still needs one fresh scheduled-task proof-of-life artifact before describing runtime as live
- Treat storage as an active P0 ops blocker:
  - current `C:` free space is `3171799040` bytes (`~2.95 GiB`)
  - do not start replay-heavy QA or bulky artifact generation before headroom is restored unless the work directly closes a release blocker
- Treat the dirty tree as mixed execution truth:
  - reviewed NutriOK product changes exist alongside local secrets, logs, lockfiles, and ops debris
  - do not publish another mixed source snapshot; split intentional product files first
- Treat repeated strategy/doc refresh without new runtime, intake, review, or benchmark artifacts as an inefficiency loop, not progress

## Next Engineering Packet

1. Persist goal, baseline, metric, adherence, and three-day diary end to end.
2. Persist reviewer identity, decision, timestamp, and approved artifact for every full-tier and supplement path.
3. Build the 20-case NutriOK fixture pack and complete two consecutive benchmark runs.
4. Capture one fresh scheduled-task runtime proof without creating a second poller.
5. Recover `C:` above `10 GiB`.
6. Split publishable source changes from secrets and local runtime debris.
7. Write RF retention, deletion, encryption, access, and audit controls.
8. Only then continue with public-surface alignment and broader pilot packaging.
## 2026-06-21 16:40 Correction Set

Use this correction set wherever it conflicts with older June or May assumptions.

- Treat runtime as `active again and fresher, but still not single-owner healthy`, not empty or solved:
  - `bot.stderr.log` now ends with handled updates at `2026-06-21 08:36:49 +03:00`, `08:36:51 +03:00`, `08:36:54 +03:00`, `08:36:56 +03:00`, `08:36:58 +03:00`, and `08:37:00 +03:00`
  - the current `ops/agent-sync-status.ps1` run still reports `BotProcessCount = 2`
  - do not claim healthy polling until the extra `getUpdates` caller is removed and a newer clean artifact exists after that fix
- Treat persisted runtime state as refilled but still unresolved:
  - `WellnessBot/data/runtime_state.json` is no longer empty
  - `user_sessions["1084557944"]` now mounts `20260621T053653Z_1084557944`
  - mounted state is `offer = osipov`, `step = osipov_context`, `payment_status = manual_payment_confirmed`
  - `chat_sessions` is still empty
  - engineering must decide whether this split is intended `osipov` state or a persistence defect
- Treat same-user specialist re-entry as the new P0 commercialization blocker:
  - `20260621T053653Z_1084557944` is a fresh `osipov` rail at `5900 RUB`
  - `20260618T192846Z_1084557944` already delivered `osipov` with `direct_delivery = true`, `adult_confirmed = false`, and no persisted review artifact
  - `20260619T215149Z_1084557944` already delivered `gut_support_18` with `direct_delivery = true`, `adult_confirmed = true`, `source_submission_id = 20260618T192846Z_1084557944`, and no persisted review artifact
  - no same-user specialist re-entry may count as healthy proof until canonical ownership and review traceability are explicit
- Treat the same-user commercialization stack as even less controlled than the morning mandate said:
  - `20260531T183007Z_1084557944` still combines `paid`, `delivered_to_client`, and `fail_major_issues`
  - `20260618T121906Z_1084557944` and `20260618T214036Z_1084557944` still duplicate the `nutri_chat` entry rail at `1490 RUB`
  - June 18 / June 19 / June 21 specialist rails still lack explicit canonical ownership
- Treat `gut_support_18` as live product-direction drift, not approved pilot truth:
  - dirty `WellnessBot/*` code adds the offer, prompt, text, payment mapping, adult gate, and post-`osipov` upsell
  - a delivered case already exists for this rail
  - engineering must gate it behind explicit approval or remove it from the live path
- Treat public-surface commercialization as still overclaimed:
  - `landing/index.html` still names `Premium Wellness Dossier` and Telegram support beyond the governed pilot
  - root `index.html` still claims a free first step, live YooKassa-style payment, PDF delivery, and off-map pricing truth
  - `mini-app/index.html` still presents a live `1 000 ₽` entry rail plus dossier/PDF/support output
- Treat disk as a critical P0 blocker again:
  - current `C:` free space is `5226946560` bytes (`~4.87 GiB`)
  - do not start replay-heavy or benchmark-heavy work before headroom is restored unless the work directly stops a safety or delivery issue
- Treat governance and loop pressure as active engineering truth:
  - `WellnessBot/data/product_governance.json` still holds `151` experiments and `0` decisions
  - repeated experiment titles still cluster at `12`, `11`, `8`, `8`, and `5`
  - `docs/tasks` still holds `29` open `HERMES-20260505-*` packets
  - repeated experiment ideation is not progress while delivery truth and canonical ownership remain unresolved

## Next Engineering Packet

1. Stop the competing poller and capture a newer clean runtime artifact after `2026-06-21 08:37:00 +03:00`.
2. Reconcile the non-empty `user_sessions` plus empty `chat_sessions` split.
3. Block new same-user specialist or paid re-entry until `canonical_path` or `case_relation` exists.
4. Enforce `direct_delivery` review evidence or a named override.
5. Repair or invalidate the June 18-21 specialist chain as proof.
6. Repair the `20260531T183007Z_1084557944` delivery-gate breach.
7. Park `gut_support_18` behind an explicit approval flag or roll it back from the live path.
8. Neutralize landing/root/mini-app claims to the surviving Telegram-first truth.
9. Recover `C:` above `10 GiB`.
10. Patch `ops/quality_probe.py` so prompt-level failures still emit partial artifacts.
11. Patch `WellnessBot/ai_drafting.py` so transport uses explicit policy.

## Lead Developer / Executor Mandate

The lead developer owns the concrete repo and runtime behaviors that make:

- same-user canonical ownership explicit
- direct-delivery review evidence mandatory
- specialist re-entry impossible before governance
- runtime state structurally coherent
- polling ownership explicit
- public surfaces aligned with the actual Telegram-first manual-review product

## Quality Auditor Stop Conditions

Stop the cycle if any of these are still true and someone is trying to treat the state as healthy:

- `delivered_to_client` appears while internal review still demands revision and no override record exists
- the same Telegram user holds more than one active or unresolved paid specialist path
- `20260621T053653Z_1084557944` is treated as healthy proof before it is canonically linked to the June 18-19 specialist chain
- `direct_delivery` is being reused as proof without a persisted review artifact or named override
- `gut_support_18` is being treated as approved pilot truth without explicit approval, adult-gating clarity, and review evidence
- mini-app or public pages still imply live payment, PDF, dossier, or support promises beyond the governed pilot
- runtime is described as healthy before one clean post-fix polling artifact exists after the duplicate-runner fix
- governance growth is being treated as progress while `decisions = 0`

## Definition Of Done

A task is not done unless:

- it improves delivery truth
- it reduces ambiguity around the canonical same-user path
- it makes runtime polling behavior explicit and reliable
- it removes a loop instead of creating another
- it survives available logs, artifacts, and operator review


