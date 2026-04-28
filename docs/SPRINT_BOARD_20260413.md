# Sprint Board

Date: 2026-04-27
Status: Active refresh after persisted-branch review
Sprint owner: Chief Orchestrator
Operating mode: pilot stabilization for one safe Telegram paid cycle

## P0. Single Delivery Candidate

Owner:

- Operator
- Product Strategist
- Lead Developer

Task:

- restore one clear delivery candidate for Telegram user `1084557944`

Concrete changes:

- declare `20260425T212847Z_1084557944` the only delivery candidate
- downgrade `20260425T214914Z_1084557944` to evidence-recovery status until readable labs or manual biomarkers exist
- record this branch decision in operator practice and future state updates
- stop carrying forward freshness alone as the deciding rule when the freshest branch is unsafe

Done when:

- exactly one branch is treated as delivery-capable
- the other branch is explicitly paused for evidence recovery
- the reason is written in the next run notes and handoff context

## P0. Safe Premium Closure

Owner:

- Operator
- Product Strategist
- Lead Developer

Task:

- close `20260425T212847Z_1084557944` into a safe premium proof or archive it explicitly

Concrete changes:

- use `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json` as the rewrite brief
- remove invented symptoms, unsupported condition framing, and unjustified brand references
- compress the deliverable into a time-based map:
  - what to do in the next `72h`
  - what to verify in the next `7d`
  - what to revisit during the `30d` follow-up window
- make one human review decision only: deliver or archive with reason

Done when:

- one safe premium proof exists or the branch is archived with a reason
- the closure decision is logged
- one operator friction note and one follow-up target are captured

## P0. Unsafe Lab Gate Freeze

Owner:

- Lead Developer
- Operator

Task:

- stop `20260425T214914Z_1084557944` from acting like a deliverable while labs remain unreadable

Concrete changes:

- preserve the case as evidence-only while `lab_quality_check.status=needs_resubmission`
- do not use current generated artifacts as delivery proof
- prepare one reusable Telegram request for readable PDF/photo or manual biomarker text
- confirm the team treats unreadable labs as unreadable, not "good enough"

Done when:

- the branch is either paused with a clear operator message or reopened with readable evidence
- no unsafe PDF or draft is treated as client-ready

## P0. Week Walkthrough

Owner:

- Operator
- Lead Developer

Task:

- verify that `week` works as the low-friction packaging rail inside the same Telegram-first model

Concrete changes:

- run one walkthrough for `week`
- verify selected product, amount, and manual payment context reach the admin correctly
- verify Russian-only copy and no broken handoff text in the critical path
- check that `week` is easy to explain as a lighter entry path, not a conflicting product story

Done when:

- the `week` flow completes without critical ambiguity
- admin handoff shows the correct product and amount
- the operator can explain `week` versus `premium` without improvising

## P1. Premium Walkthrough

Owner:

- Operator
- Lead Developer

Task:

- verify the flagship `premium` flow after the branch decision is made

Concrete changes:

- run one walkthrough for `premium`
- verify manual payment handoff is coherent
- verify human review remains explicit in operator and client-facing steps
- compare copy and context against the intended `72h -> 7d -> 30d` value story

Done when:

- the `premium` flow reaches admin handoff cleanly
- there is no ambiguity around the flagship promise or payment rule

## P1. Demo Result Example

Owner:

- Product Strategist
- Lead Developer

Task:

- create one demo-ready result example only after a safe premium closure exists

Concrete changes:

- extract a safe, non-identifying sample from the corrected premium branch
- show priorities, hypotheses, doctor questions, and next-step timing
- keep the demo short enough to build trust instead of recreating dossier sprawl

Done when:

- the start menu can point to one believable demo result
- the demo makes `premium` easier to buy and makes `week` easier to understand

## P1. Governance Compression

Owner:

- Quality Auditor
- Lead Developer

Task:

- stop governance memory from pretending to be product progress

Concrete changes:

- treat `115` stored experiments and repeated titles as loop signals, not momentum
- allow no new experiment burst before one fresh safe delivery outcome exists
- keep only one next experiment candidate for the post-delivery cycle:
  - tighten premium into a stronger `72h -> 7d -> 30d` structure

Done when:

- governance reflects one next learning move instead of a backlog flood
- live delivery evidence drives the next experiment

## Stop List

Blocked for now:

- new same-user premium generation before `20260425T212847Z_1084557944` is delivered or archived
- treating `20260425T214914Z_1084557944` as delivery-safe while labs remain unreadable
- active `vip` selling before one safe premium proof and operator-load evidence exist
- pricing experiments before premium credibility is proven
- more governance experiments before fresh delivery evidence
- YooKassa debate on the live pilot critical path
- new landing, mini-app, or growth-channel expansion work

## Loop Risk

Repeated low-impact tasks to stop:

- arguing over freshest branch versus safest branch without making a branch decision
- generating or revising unsafe artifacts before readable labs exist
- adding more product-governance ideas while no fresh delivery proof exists
- treating `week` or `vip` as strategy expansion instead of controlled support rails

Replacement action:

- declare one delivery candidate, freeze the unsafe branch, close one safe premium proof, run one `week` walkthrough, and keep one post-delivery structure experiment

## Next 12h Command Set

1. Declare `20260425T212847Z_1084557944` the only delivery candidate for user `1084557944`.
2. Freeze `20260425T214914Z_1084557944` as evidence-only until readable labs or manual biomarkers arrive.
3. Rewrite and close or archive `20260425T212847Z_1084557944` after one factual human review pass.
4. Run one live Telegram walkthrough for `week`.
5. Run one live Telegram walkthrough for `premium`.
6. Verify manual payment handoff shows the correct product, amount, and Russian copy.
7. Keep one governance experiment only after real delivery evidence exists: premium compression into `72h -> 7d -> 30d`.
