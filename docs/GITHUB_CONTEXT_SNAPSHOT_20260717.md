# Context For External Contributors - NutriOK

## Product

`НутриОК by Olga Kovaleva`: a full nutrition assessment whose promise is
`Разбор, после которого понятно, что делать`.

## Architecture Boundary

The current repository is an aiogram monolith under controlled rebuild. Preserve one polling owner.
Near-term work should make intake, review evidence, delivery state, safety decisions, and audit events
explicit before cloud migration. Do not add new public offers or automatic supplement delivery.

## Safety Boundary

No diagnosis, treatment, medication changes, or guaranteed outcomes. Full tiers require persisted Olga
approval. Supplement brand/dose/duration/link require separate approval and disclosure. HMS/Osipov is an
optional input, not a diagnosis or standalone product.

## Immediate Work

1. Persist the structured assessment contract end to end.
2. Persist named approval and make delivery depend on it.
3. Build and pass NutriOK fixture benchmarks twice.
4. Restore the scheduled-task runtime without a second poller.
5. Implement RF-hosted privacy, retention, deletion, and audit controls.

## Synchronization Warning

This snapshot is published for orientation only. The implementation remains in a dirty local working tree,
so GitHub does not yet contain the full NutriOK code truth.