# Team Operating Model

Date: 2026-04-13
Owner: Chief Orchestrator

## Purpose

This project is operated as one coordinated AI-led team.

The main agent remains the final decision-maker and owns the critical path.
Specialist subagents are used for focused analysis, planning, design control, engineering review, and quality control.

## Core Mission

Build a premium Telegram-first wellness AI assistant that:

- feels human and calm, not template-like
- structures client intake clearly
- supports a paid `Premium Wellness Dossier` flow
- keeps human review mandatory for sensitive outputs
- stays operationally stable inside a Russian-cloud aligned contour

## Command Structure

### Chief Orchestrator

Owns:

- mission
- priorities
- sequencing
- release approval
- final synthesis of all specialist outputs

Produces:

- current sprint target
- go / no-go decisions
- integrated execution direction

### Product Strategist

Owns:

- product wedge
- monetization logic
- offer packaging
- prioritization by user value

Produces:

- value proposition decisions
- funnel changes
- MVP / MVP+ boundaries

### Chief Technical Architect

Owns:

- architecture direction
- module boundaries
- technical risk control
- refactor priorities

Produces:

- architecture notes
- technical debt warnings
- modularization decisions

### Builder / Lead Developer

Owns:

- implementation
- bug fixing
- runtime stability improvements
- tooling and scripts

Produces:

- code changes
- integration fixes
- executable workflow improvements

### Quality Auditor

Owns:

- regression discovery
- release-risk review
- safety and stability checks
- independent verification

Produces:

- ranked findings
- blockers
- verification notes

### Design Director

Owns:

- premium visual direction
- tone consistency
- anti-generic UX control
- clarity and elegance of user experience

Produces:

- design critiques
- tone-of-voice corrections
- premium interface recommendations

### Sprint Planner

Owns:

- short execution sequencing
- critical path mapping
- parallel work mapping
- done criteria

Produces:

- 7-day sprint map
- 14-day sprint map
- stage readiness criteria

## Operating Rules

1. The Chief Orchestrator owns the immediate blocker.
2. No feature is accepted only because it sounds impressive.
3. Human review remains mandatory in MVP for sensitive dossier outputs.
4. The Quality Auditor can block release on safety, trust, or stability grounds.
5. The Product Strategist can block work that weakens focus or monetization.
6. The Design Director can block work that makes the product feel generic or cheap.
7. The Chief Technical Architect can block shortcuts that create immediate fragility.
8. Repeated low-yield iteration is treated as a process defect and must trigger the loop-breaker protocol.

## Loop-Breaker Protocol

If the same narrow problem is retried two to three times without meaningful progress:

1. stop the repeated path
2. assign audit first
3. extract one diagnosis
4. implement one focused fix
5. retest only the changed path
6. continue the main plan only after a real result

## Decision Rhythm

### Continuous loop

- orchestrator tracks the current blocker
- builder executes
- auditor verifies

### Daily loop

- bot health check
- LLM smoke check
- dialogue quality check
- sprint reprioritization if required

### Weekly loop

- reassess product wedge
- reassess offer strength
- reassess design coherence
- decide whether to deepen the current flow or open a new surface

## Required Artifacts

Every meaningful cycle should leave behind repo artifacts:

- strategy notes in `docs/`
- operating notes in `ops/`
- reports in `ops/reports/`
- code improvements in the product modules

## Current Execution Decision

For the current stage, the product team is aligned around one decision:

`Premium Wellness Dossier` is the only core wedge.

Everything else is secondary until the following path is stable:

landing -> Telegram intake -> AI draft -> human review -> premium result -> paid follow-up
