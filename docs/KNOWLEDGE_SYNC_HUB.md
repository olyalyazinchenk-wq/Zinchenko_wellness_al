# Knowledge Sync Hub

## Purpose
Single control point for the Antigravity synchronization cycle.
This hub defines what must be refreshed every run, how connector availability is judged, and what local artifacts remain mandatory even when external sync is partially blocked.

## Mandatory Knowledge Bases
- Obsidian local mirror: `C:\Users\HP\Desktop\Новая папка\docs\obsidian_mirror`
- Notion workspace: connected workspace pages for run notes and model context
- GitHub repo: `olyalyazinchenk-wq/Zinchenko_wellness_al`
- Google Drive: required target only when upload/create and share tools are exposed in the current session

## Every-Run Standard
Every run must refresh:
- key changes since the previous run
- latest project state across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`
- latest benchmark reference from `ops/reports` when one exists
- runtime-versus-storage mismatches and delivery-safety regressions
- current blockers, risks, owners, and next fix actions
- `Plan Delta`, `Strategy Delta`, `Goals Delta`, and next 12h priorities
- a concise `Context For New Model` block
- sanitized external-contributor artifacts for GitHub and the local mirror

## Run Output Contract
Each sync cycle creates or refreshes:
- one new timestamped entry in [PROJECT_PULSE_LOG.md](C:\Users\HP\Desktop\Новая папка\docs\PROJECT_PULSE_LOG.md)
- one new strategy refresh section in [STRATEGY_LIVE_DELTA.md](C:\Users\HP\Desktop\Новая папка\docs\STRATEGY_LIVE_DELTA.md)
- refreshed onboarding hubs:
  - [AGENT_CONTEXT_HUB.md](C:\Users\HP\Desktop\Новая папка\docs\AGENT_CONTEXT_HUB.md)
  - [obsidian_mirror/AGENT_CONTEXT_HUB.md](C:\Users\HP\Desktop\Новая папка\docs\obsidian_mirror\AGENT_CONTEXT_HUB.md)
- one run-note mirror in `docs/obsidian_mirror/`
- one GitHub status artifact and one GitHub context snapshot for external contributors
- one connector status map with `Done`, `Changed`, `Blocked`, and `Next 12h`

## Connector Discovery Rule
At the start of every run:
- verify which connector tools are exposed in the current session
- treat plugin presence alone as insufficient; required write tools must be actually exposed by tool discovery or the connector is blocked for that capability
- treat GitHub as connector-first when the repository name is known; a missing local `git remote` is a CLI gap, not by itself a GitHub sync blocker
- treat Google Drive as available only when file create/upload and share tools are exposed
- if a connector is partially available, use the working surface and log the missing capability precisely

## Connector Fallback Rule
If any connector is unavailable:
- complete the full local refresh first
- mark the connector as `Blocked` with the exact reason
- write the exact access request needed for the next run
- repeat that same access request in the inbox summary

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

## Single Active Paid Path Rule
Before carrying execution forward for any Telegram user:
- verify the same user is not simultaneously holding a live `week`, `premium`, or `vip` runtime session plus unresolved older paid submissions
- if multiple paid paths coexist, log the conflict immediately in `PROJECT_PULSE_LOG.md` with owner and next fix action
- explicitly declare one active paid path and freeze, archive, or merge the others before calling the state coherent

## Safety Gate Validation Rule
Before confirming a premium case as active or delivery-safe:
- verify whether `lab_quality_check.requires_resubmission` is `true`
- verify whether draft or PDF generation happened despite an unsafe lab gate
- if a safety gate was bypassed, log it immediately in `PROJECT_PULSE_LOG.md` as a regression with owner and next fix action

## Delivery Review Gate Rule
Before confirming any paid case as delivered:
- verify the latest internal review verdict is no longer `needs_revision`, `must_rewrite_with_high_caution`, or otherwise flagged for rewrite
- if delivery still proceeds, record an explicit manual override note with who approved it and why
- if a case reaches `delivered_to_client` without a cleared review verdict or override note, log it immediately in `PROJECT_PULSE_LOG.md` as a P0 regression with owner and next fix action
