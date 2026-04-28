# Personal Data Compliance Pack

Date: 2026-04-20
Purpose: practical package of documents and actions for Olga's Telegram wellness service.

## Pack Contents

This package is designed for a premium Telegram wellness service that handles:
- client identity data,
- complaints and lifestyle data,
- uploaded lab files,
- other health-related context.

Included documents:
- `docs/OPERATOR_PROFILE_DRAFT_20260420.md`
- `docs/PD_STORAGE_ARCHITECTURE_20260420.md`
- `docs/templates/PRIVACY_POLICY_TEMPLATE_20260420.md`
- `docs/templates/CONSENT_PERSONAL_AND_HEALTH_DATA_TEMPLATE_20260420.md`
- `docs/templates/PROCESSOR_INSTRUCTION_AGREEMENT_TEMPLATE_20260420.md`
- `docs/templates/ACCESS_RETENTION_AND_DELETION_REGULATION_TEMPLATE_20260420.md`
- `docs/templates/PD_REGISTER_AND_DATA_FLOW_TEMPLATE_20260420.md`

## Minimum Required Before Production

1. Identify the operator.
2. Publish privacy policy.
3. Configure and store explicit consent.
4. Separate production and test data.
5. Approve processor access rules for developer / contractor.
6. Move source-of-truth storage into RF-hosted infrastructure.
7. Decide retention and deletion terms.
8. Check Roskomnadzor notification obligations.

## Recommended Document Ownership

- Operator / founder: privacy policy, consent wording, processing purposes.
- Legal review: final wording and retention periods.
- Developer / architect: storage architecture, access boundaries, technical controls.
- Operations: logging, backups, deletion workflow, incident handling.

## Olga-Specific Drafting Status

Templates in this pack are already adapted to:
- `Ольга Зинченко` as the expert and service face,
- Telegram bot `@zinchenko_wellness_ai_1_bot`,
- Telegram channel `@olga_nutri86`,
- service format `нутрициологическая навигация`.

Legal requisites that are still missing are collected in:
- `docs/OPERATOR_PROFILE_DRAFT_20260420.md`

## Launch Checklist

- operator details filled in all templates,
- data categories and purposes approved,
- consent flow embedded into bot intake,
- processor list approved,
- infrastructure location confirmed in RF,
- developer access minimized,
- local uncontrolled exports disabled or documented,
- deletion workflow tested,
- policy published and linked in bot / landing / intake.
