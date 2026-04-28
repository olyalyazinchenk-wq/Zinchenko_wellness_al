# Knowledge Sync Hub

## Purpose
Single control point for regular project synchronization and strategy refresh.
This hub defines what must be updated every 12 hours and where the updates go.

## Mandatory Knowledge Bases
- Obsidian: local mirror vault at `C:\Users\HP\Desktop\Новая папка\docs\obsidian_mirror`
- Notion: workspace connected account `Ольга Ковалева`
- GitHub: connected account `olyalyazinchenk-wq`
- Google Drive: required target when the connector is exposed with upload/share permissions

## 12h Sync Standard
Every run must update:
- Key progress since previous run
- Product changes in bot/web/mini-app
- Quality metrics (latest benchmark report and critical deltas)
- Latest benchmark reference from `ops/reports` when one exists
- Current blockers and risks
- Next 12h execution priorities
- Strategy, goal, and plan adjustments
- Context for new contributors/models (stage, purpose, current direction, next actions)
- External contributor snapshot artifacts for GitHub and local mirror storage

## Run Output Contract
Each sync cycle creates:
- One new entry in [PROJECT_PULSE_LOG.md](C:\Users\HP\Desktop\Новая папка\docs\PROJECT_PULSE_LOG.md)
- One strategy refresh note section (`Plan Delta` + `Strategy Delta`)
- Connector status map (`Done`, `Pending`, `Blocked`)
- One run note mirror inside `docs/obsidian_mirror/`
- One GitHub status artifact and one GitHub context snapshot for external contributors
- Updated onboarding artifact:
  - [AGENT_CONTEXT_HUB.md](C:\Users\HP\Desktop\Новая папка\docs\AGENT_CONTEXT_HUB.md)
  - [obsidian_mirror/AGENT_CONTEXT_HUB.md](C:\Users\HP\Desktop\Новая папка\docs\obsidian_mirror\AGENT_CONTEXT_HUB.md)

## Connector Fallback Rule
If any connector is unavailable:
- Save full update in local hub files first
- Mark connector as `Blocked` with exact reason
- Add exact action request for the next run (what access is needed)
- Repeat the same access request in the inbox summary

## State Validation Rule
Before carrying forward any "active case" or "current blocker" from the previous sync:
- Re-read `WellnessBot/data/runtime_state.json`
- Re-check the newest `WellnessBot/data/submissions/*.json` and latest draft review artifacts
- Prefer the newest persisted runtime evidence over yesterday's narrative
- If the live story changed, write that correction explicitly into `PROJECT_PULSE_LOG.md`
- If `runtime_state.json` is empty, do not infer that there is no active work. Rebuild the live picture from the newest persisted submissions by `status_updated_at`, plus the newest review and growth artifacts.

## Safety Gate Validation Rule
Before confirming a premium case as active or delivery-safe:
- Verify whether `lab_quality_check.requires_resubmission` is `true`
- Verify whether draft/PDF generation happened despite an unsafe lab gate
- If a safety gate was bypassed, log it immediately in `PROJECT_PULSE_LOG.md` as a regression with owner and next fix action
