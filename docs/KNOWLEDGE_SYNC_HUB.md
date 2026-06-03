# Knowledge Sync Hub

## Purpose
Single control point for the Antigravity synchronization cycle.
This hub defines what must be refreshed every run, how connector availability is judged, and what local artifacts remain mandatory even when external sync is partially blocked.

## Mandatory Knowledge Bases
- Obsidian local mirror: `C:\Users\HP\Desktop\Новая папка\docs\obsidian_mirror`
- Notion workspace: connected workspace pages for run notes and model context
- GitHub repo: `olyalyazinchenk-wq/Zinchenko_wellness_al`
- Google Drive: required target only when upload/create and share tools are actually exposed in the current session

## Every-Run Standard
Every run must refresh:
- key changes since the previous run
- latest project state across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`
- latest benchmark reference from `ops/reports` when one exists
- current runtime evidence, latest paid-delivery evidence, and storage headroom
- current blockers, risks, owners, and next fix actions
- `Plan Delta`, `Strategy Delta`, `Goals Delta`, and next 12h priorities
- a concise `Context For New Model` block
- sanitized external-contributor artifacts for GitHub and the local mirror

## Run Output Contract
Each sync cycle creates or refreshes:
- one new timestamped entry in `docs/PROJECT_PULSE_LOG.md`
- one new strategy refresh section in `docs/STRATEGY_LIVE_DELTA.md`
- refreshed onboarding hubs:
  - `docs/AGENT_CONTEXT_HUB.md`
  - `docs/obsidian_mirror/AGENT_CONTEXT_HUB.md`
- one run-note mirror in `docs/obsidian_mirror/`
- one GitHub status artifact and one GitHub context snapshot for external contributors
- one connector status map with `Done`, `Changed`, `Blocked`, and `Next 12h`

## Connector Discovery Rule
At the start of every run:
- verify which connector tools are exposed in the current session
- treat plugin presence alone as insufficient; required write tools must be actually exposed by tool discovery or the connector is blocked for that capability
- treat GitHub as connector-first when the repository name is known; a missing local `git remote` is a CLI gap, not by itself a GitHub sync blocker
- treat Google Drive as available only when file discovery/create/upload/share tools are exposed
- if a connector is partially available, use the working surface and log the missing capability precisely

## Connector Startup Health Rule
After tool discovery and before claiming connector success:
- run at least one real connector call on every connector that must write in the current cycle
- if the call fails with `failed to get client`, `MCP startup failed`, or another startup-timeout error, mark the connector as blocked even if its tools were discoverable
- write the local fallback artifact anyway so the sync payload can be replayed later without redoing the analysis
- include the exact startup error and the exact access request in `PROJECT_PULSE_LOG.md` and the inbox summary

## Connector Fallback Rule
If any connector is unavailable:
- complete the full local refresh first
- mark the connector as `Blocked` with the exact reason
- write the exact access request needed for the next run
- repeat that same access request in the inbox summary

## Dirty Working Tree Truth Rule
Before concluding a sync:
- run `git status --short --branch` and inspect diffs for dirty files in `WellnessBot`, `mini-app`, `landing`, `ops`, and `docs`
- if uncommitted changes materially alter runtime behavior, product surfaces, benchmark behavior, or safety rules, log them as current project truth even if no commit exists yet
- separate `repo head` from `working tree truth` in `PROJECT_PULSE_LOG.md` and `AGENT_CONTEXT_HUB.md`
- if a dirty change conflicts with the standing pilot, safety, or pricing rules, call it out immediately as a regression with owner and next fix action

## Timestamp Integrity Rule
Before writing the new run entry:
- resolve the current local run time explicitly
- if the latest sync artifact is future-dated relative to the current run, correct that entry instead of stacking a second contradictory timestamp
- keep the pulse log, agent hub, Obsidian mirror, and outward-sync artifacts aligned to the same absolute run timestamp

## Runtime Artifact Precedence Rule
Before carrying forward any runtime narrative:
- compare `bot.stderr`, `bot.stderr.log`, and any newer runtime proof artifacts by actual file modification time
- prefer the freshest successful or failed runtime artifact over older hub summaries
- if fresh runtime evidence overturns the earlier same-day story, write the correction explicitly into `PROJECT_PULSE_LOG.md`, `AGENT_CONTEXT_HUB.md`, and the outward-sync artifacts
- do not keep a stale outage narrative active once a newer successful polling or model-call artifact exists

## Benchmark Reference Precedence Rule
Before carrying forward any benchmark or QA narrative:
- compare the newest completed `ops/reports/quality_report_*.md` artifact against the latest `docs/WELLNESS_DIALOGUE_QA_*.md` synthesis by actual timestamp
- if a newer completed quality report exists, treat that report as the latest benchmark reference even if the QA synthesis has not yet been refreshed
- if the older QA synthesis still claims there is no fresh completed artifact, log it as stale and correct the benchmark reference explicitly in `PROJECT_PULSE_LOG.md`, `AGENT_CONTEXT_HUB.md`, and outward-sync artifacts
- if benchmark-critical files changed between the stale QA synthesis and the fresh report, call out that the old QA interpretation is obsolete rather than silently carrying it forward

## Storage Floor Escalation Rule
If the current run measures `C:` below the `10 GB` floor:
- log the exact free-space value and timestamp as an active ops regression, not a background hygiene note
- move disk recovery into the current `Plan Delta`, `Goals Delta`, and `Next 12h` set before new artifact generation
- do not describe the environment as back within margin until a later run re-measures above `10 GB`

## External Sanitization Rule
Before syncing status artifacts outside the local workspace:
- redact Telegram user IDs and case identifiers that embed personal identifiers
- keep secrets, tokens, and private local paths out of shared artifacts
- allow internal local docs to retain operational identifiers only when they are required for execution

## State Validation Rule
Before carrying forward any active case or blocker:
- re-read `WellnessBot/data/runtime_state.json`
- re-check the newest `WellnessBot/data/submissions/*.json` and latest review artifacts
- prefer fresh persisted evidence over yesterday's narrative
- if the live story changed, write the correction explicitly into `PROJECT_PULSE_LOG.md`
- if `runtime_state.json` is empty, rebuild the live picture from the newest persisted submissions and review artifacts instead of inferring no active work
- if `runtime_state.json` points to a `submission_id` with no matching JSON file, treat that session as provisional only and log a persistence regression

## Active Continuity Thread Audit Rule
Before describing `nutri_chat` or any paid continuity-chat rail as safe or commercially healthy:
- inspect the latest assistant turns in `WellnessBot/data/runtime_state.json` chat memory
- if a paid continuity thread exists, sample it for invented diagnoses, medication-like advice, unsupported names or ages, and continuity promises that exceed approved scope
- if continuity behavior is the freshest product proof, treat that thread as benchmark-relevant product truth even when no new PDF or dossier artifact exists
- log any false-specificity or escalation-boundary breach immediately in `PROJECT_PULSE_LOG.md`, `AGENT_CONTEXT_HUB.md`, and outward-sync artifacts with owner and next fix action

## Single Active Paid Path Rule
Before carrying execution forward for any Telegram user:
- verify the same user is not simultaneously holding a live `week`, `premium`, `basic`, `full`, or `vip` runtime session plus unresolved older paid submissions
- if multiple paid paths coexist, log the conflict immediately in `PROJECT_PULSE_LOG.md` with owner and next fix action
- explicitly declare one active paid path and freeze, archive, or merge the others before calling the state coherent

## Paid Delivery Completion Rule
Before describing a paid path as operationally healthy:
- verify whether payment confirmation, draft generation, review generation, PDF export, and handoff all completed
- if the paid path crashes after payment confirmation but before the final deliverable exists, log it as a P0 fulfilment regression with owner and next fix action
- record the exact failing function or missing artifact when the failure is code-path specific

## Safety Gate Validation Rule
Before confirming a premium or full-depth case as active or delivery-safe:
- verify whether `lab_quality_check.requires_resubmission` is `true`
- verify whether draft or PDF generation happened despite an unsafe lab gate
- if a safety gate was bypassed, log it immediately in `PROJECT_PULSE_LOG.md` as a regression with owner and next fix action

## Delivery Review Gate Rule
Before confirming any paid case as delivered:
- verify the latest internal review verdict is no longer `needs_revision`, `must_rewrite_with_high_caution`, `fail_major_issues`, or otherwise flagged for rewrite
- if delivery still proceeds, record an explicit manual override note with who approved it and why
- if a case reaches `delivered_to_client` without a cleared review verdict or override note, log it immediately in `PROJECT_PULSE_LOG.md` as a P0 regression with owner and next fix action
- do not infer delivery safety from the existence of a generated PDF alone; artifact existence cannot override a failing review verdict
