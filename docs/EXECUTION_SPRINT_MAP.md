# Execution Sprint Map

Date: 2026-04-13
Owner: Chief Orchestrator

## North Star

Create a premium Telegram-first wellness service that takes a user from confusion to a paid, human-reviewed `Premium Wellness Dossier` inside one coherent flow.

## One Core Wedge

For now, the product is only this:

`Premium Wellness Dossier`

Target user:

- women 28-45
- fatigue, unclear symptoms, digestive complaints
- history of "everything looks normal" frustration

## What We Are Not Building Now

- multi-audience product branches
- autonomous medical advisor
- full platform
- heavy mini-app dependency
- advanced RAG / vector memory
- large analytics stack

## Critical Path

1. Stabilize Telegram bot runtime and core flow.
2. Tighten intake logic and persistence.
3. Standardize AI draft structure.
4. Create a minimal human review loop.
5. Define the paid offer trigger and follow-up logic.
6. Unify premium tone and visual identity.

## Parallel Tracks

These can run in parallel without blocking the critical path:

- landing and copy refinement
- premium design unification
- quality checks and prompt tuning
- permissions and compliance documentation
- payment-flow preparation

## 7-Day Sprint

### Day 1. Product lock

Goal:

- lock one product, one user, one value proposition

Done when:

- the product can be explained in one sentence
- there is one primary CTA
- there is a clear "not now" list

### Day 2. Intake hardening

Goal:

- make the intake clear, calm, and resilient

Done when:

- 3-5 internal runs complete without confusion
- red-flag handling is explicit
- data structure is consistent

### Day 3. Draft standardization

Goal:

- make AI output predictable and easy to review

Done when:

- every test case produces the same output structure
- fallback behavior is defined for LLM failures

### Day 4. Human review loop

Goal:

- establish a minimum review workflow for Olga

Done when:

- a case can move from intake to draft to reviewed result
- status handling is clear

### Day 5. Monetization point

Goal:

- define where and why the user pays

Done when:

- the paid offer is explicit
- the point of payment is clear
- the next paid step is named

### Day 6. Premium UX pass

Goal:

- remove generic tone and visual inconsistency

Done when:

- landing, bot, and mini-app no longer feel like separate brands
- copy feels calm, premium, and guided

### Day 7. Mini-beta

Goal:

- run real end-to-end scenarios and surface the last major breaks

Done when:

- 3-5 realistic cases complete end-to-end
- blockers are documented
- the MVP is presentable

## 14-Day Sprint

### Days 8-10. Repeatability

Goal:

- make results consistent across multiple cases

Done when:

- the same process works across 8-10 test runs
- runtime issues are reduced
- outputs stay coherent

### Days 11-12. Payment and offer mechanics

Goal:

- turn the product into a reliable paid service

Done when:

- there is a real or near-real payment flow
- the transition from free chat to paid dossier is understandable

### Days 13-14. Pilot control

Goal:

- validate the system in a small commercial beta

Done when:

- pilot cases are run
- friction points are documented
- the product is ready for limited launch

## Immediate Technical Priorities

- move live session state out of process memory
- introduce a clearer state machine for intake
- add retry/backoff around LLM calls
- tighten startup configuration validation
- reduce duplicated finalization paths

## Immediate Product Priorities

- compress the product into one wedge
- make Telegram feel like concierge, not questionnaire
- define one premium result artifact
- reduce diagnostic-sounding language

## Immediate Design Priorities

- unify the brand language across all surfaces
- reduce black-gold luxury cliches
- shift toward quiet luxury + editorial wellness + clinical precision
- strengthen Olga as author and curator, not abstract AI
