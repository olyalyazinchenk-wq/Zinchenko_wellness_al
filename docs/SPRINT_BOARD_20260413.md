# Sprint Board

Date: 2026-05-01
Status: Active refresh after strategy and environment recheck
Sprint owner: Chief Orchestrator
Operating mode: controlled Telegram-first pilot stabilization

## P0. Environment Survival

Owner:

- Ops
- Lead Developer

Task:

- restore enough disk headroom for the pilot to stay alive

Concrete changes:

- treat `2.69 GB` free on `C:` at `2026-05-01 09:17 MSK` as an active execution blocker
- complete manual delete-review for the large `Downloads` candidates already listed in `docs/DISK_HYGIENE_STATUS.md`
- prioritize the two incomplete `.crdownload` files because they are the biggest immediate recovery opportunity
- block non-critical artifact growth while free space stays below `10 GB`

Done when:

- `C:` free space is back above `10 GB`
- the bot can continue operating without near-term storage failure risk

## P0. Runtime Truth Repair

Owner:

- Lead Developer
- Operator

Task:

- make runtime and persisted storage tell the same story for the live `week` session

Concrete changes:

- inspect why `20260427T173913Z_<REDACTED_ID>` exists only in `runtime_state.json`
- either persist the correct submission record or clear the orphaned runtime session
- do not progress the same user while the session remains runtime-only
- log the path decision in docs and operator practice

Done when:

- runtime and storage are coherent
- there is no runtime-only session being treated as a live paid case
- the next operator action is obvious

## P0. One Active Same-User Path

Owner:

- Operator
- Product Strategist
- Lead Developer

Task:

- reduce user `<REDACTED_ID>` to one active commercial path

Concrete changes:

- classify each branch as active, evidence-only, or archived
- keep `20260425T214914Z_<REDACTED_ID>` frozen as evidence-only because `requires_lab_resubmission=true`
- keep `20260425T212847Z_<REDACTED_ID>` as the only premium rewrite candidate if a proof closure is pursued
- block same-user `week` progression until the active-path choice is explicit

Done when:

- one user has one active path
- every other branch has an explicit non-active role
- no same-user ambiguity remains across offers

## P0. Router Scope Surgery

Owner:

- Lead Developer
- Quality Auditor

Task:

- stop deterministic reply routing from pretending to be product quality

Concrete changes:

- treat `20/20 routed` and `0/20 model reached` as an execution blocker
- narrow deterministic routing to emergency, crisis, file-upload guidance, and a small logistics FAQ surface
- remove unsupported symptom details from router templates, especially facts the user did not state
- add up to two clarifying questions on symptom-first replies when they materially change interpretation or safety
- rerun the benchmark and record routed share, duplicate clusters, unsupported-detail failures, and clarifying-question count

Done when:

- symptom prompts are no longer fully template-owned
- model-reached count is no longer zero on the benchmark
- unsupported-detail injection is gone from the routed layer

## P1. Safety and Delivery Gate Integrity

Owner:

- Lead Developer
- Quality Auditor

Task:

- stop paid confirmation, freshness, or generic templates from bypassing safety rules

Concrete changes:

- enforce that `requires_lab_resubmission=true` means no delivery and no new premium truth claims
- require rewrite-from-confirmed-facts before any premium closure attempt
- keep human review mandatory before any client-facing output
- preserve no-diagnosis, no-treatment, and urgent-care routing language

Done when:

- unreadable-lab branches cannot masquerade as ready
- the next premium candidate is fact-safe by construction
- operator copy and code follow the same safety gate

## P1. Conversion Asset Lock

Owner:

- Product Strategist
- Lead Developer

Task:

- keep the new safe example result as a trust asset without opening a UI branch

Concrete changes:

- treat `PRODUCT_EXAMPLES_TEXT` as the current approved proof-of-format asset in Telegram
- do not start dashboard integration, static-page expansion, or new demo-surface variants during this cycle
- use the example result only to support trust and handoff into the existing Telegram flow

Done when:

- the example result stays live and safe
- no parallel UI branch is created from the Google AI Studio mock

## P1. Governance Compression

Owner:

- Quality Auditor
- Lead Developer

Task:

- stop idea accumulation from pretending to be progress

Concrete changes:

- treat `115` experiments and `4` duplicate title groups as a loop signal
- allow no new experiment burst before one coherent paid closure exists
- keep only one post-closure experiment candidate:
  - stronger `week -> premium -> 30d` upgrade story

Done when:

- governance reflects one next learning move
- live evidence outranks ideation backlog growth

## Stop List

Blocked for now:

- promoting the runtime-only `week` session into the live proof path
- running concurrent `week` and `premium` progress for the same Telegram user
- treating `20260425T214914Z_<REDACTED_ID>` as delivery-safe while unreadable labs remain unresolved
- prompt or model tuning that leaves routed share unchanged
- Google AI Studio dashboard integration or any new UI branch
- new growth, landing, mini-app, or launch work
- pricing experiments
- YooKassa/provider debate on the live pilot critical path
- governance expansion before fresh paid evidence
- non-critical artifact generation while disk headroom remains below the safety floor

## Loop Risk

Repeated low-impact tasks to stop:

- status updates and sync notes that do not change runtime truth
- repeated branch debate without an active-path declaration
- prompt churn while the model still sees none of the benchmark symptom prompts
- governance additions while delivery truth is unresolved
- UI/backlog enthusiasm around the external dashboard mock while Telegram pilot blockers remain open

Replacement action:

- restore environment headroom first, fix runtime truth second, cut router overreach third, then close one safe premium proof path

## Next 12h Command Set

1. Manually delete-review the two large `.crdownload` files already flagged in `docs/DISK_HYGIENE_STATUS.md`, then recheck `C:` free space.
2. Restore `C:` above `10 GB` free before more non-critical artifact generation.
3. Repair or clear `20260427T173913Z_<REDACTED_ID>` so runtime and storage agree.
4. Freeze same-user `week` progression until one active path is declared.
5. Freeze `20260425T214914Z_<REDACTED_ID>` as evidence-only until readable labs or manual biomarkers exist.
6. Use `20260425T212847Z_<REDACTED_ID>` as the only premium rewrite candidate, or archive it explicitly.
7. Shrink `route_live_reply()` to emergency, crisis, file-upload, and narrow logistics coverage only.
8. Remove unsupported symptom details from routed templates and add clarifying-question behavior for symptom-first replies.
9. Rerun the benchmark and log routed share, duplicate clusters, unsupported-detail failures, and clarifying-question count.
10. Keep `PRODUCT_EXAMPLES_TEXT` as the approved Telegram trust asset; do not start dashboard integration work.
11. Keep `premium` at `6900 RUB`, `week` at `3900 RUB`, and manual concierge payment unchanged.
