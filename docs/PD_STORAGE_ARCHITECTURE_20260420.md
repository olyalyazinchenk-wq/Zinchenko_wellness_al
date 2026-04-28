# Safe Personal Data Storage Architecture

Date: 2026-04-20
Scope: Olga wellness Telegram product
Purpose: define a safer target architecture for client data, lab files, consent records, and developer access.

## Executive Summary

Current project state stores client data locally in JSON files and uploaded documents on disk.
For a production launch handling complaints, lab files, and health-related context, the target state should be:

- operator-controlled storage in the Russian Federation,
- structured database for client and consent records,
- separate protected file storage for uploads and generated reports,
- strict separation between operator access and developer access,
- auditability for consent, access, export, and deletion.

## Legal Framing

This project processes:
- ordinary personal data,
- special category personal data related to health,
- files and narratives that may contain sensitive health information.

Because of that, the architecture should assume:
- explicit consent collection,
- Russian data localization,
- published privacy policy,
- operator notification to Roskomnadzor where required,
- formal processor arrangement for any developer or third-party service with access.

## Roles

### Operator

Recommended operator:
- Olga directly as sole proprietor / legal entity, or
- the legal entity that sells and delivers the wellness service.

The operator defines:
- purposes of processing,
- categories of data,
- retention periods,
- access rules,
- external processors.

### Processor By Instruction

Recommended processor by instruction:
- developer / technical contractor,
- hosting provider,
- cloud storage provider,
- email / messaging / LLM contractors if they receive access or processing scope.

The developer should not be the operator by default.

## Target Architecture

### Layer 1. Telegram Intake Layer

Purpose:
- receive client messages, files, voice, and form answers.

Rules:
- Telegram is the transport channel, not the source-of-truth archive.
- Do not rely on manual chat history as the official storage layer.
- Pull structured intake into controlled storage immediately.

### Layer 2. Application Layer

Purpose:
- bot runtime,
- intake orchestration,
- consent capture,
- case status transitions,
- generation of internal draft and final report.

Rules:
- app server must run in RF-hosted environment,
- secrets stored separately from repo,
- access via named accounts only,
- admin actions logged.

### Layer 3. Structured Database

Recommended engine:
- PostgreSQL in Russian hosting.

Purpose:
- store clients,
- consents,
- cases,
- statuses,
- file metadata,
- access logs,
- deletion logs.

Recommended core tables:
- `clients`
- `client_contacts`
- `consents`
- `cases`
- `case_sections`
- `uploads`
- `documents_generated`
- `access_log`
- `export_log`
- `deletion_log`
- `processors_registry`

### Layer 4. File Storage

Recommended:
- S3-compatible or object storage hosted in the Russian Federation,
- encrypted at rest,
- private buckets only.

Store here:
- uploaded lab PDFs,
- uploaded photos,
- generated dossier PDFs,
- signed consent files if stored as documents.

Do not treat local desktop folders as the primary archive.

### Layer 5. Backup and Recovery

Requirements:
- encrypted backup,
- backup stored in RF-compatible environment,
- documented restore test,
- role-limited restore access,
- deletion policy consistent with retention matrix.

## Data Classification

### Class A: Client Identity Data

Examples:
- full name,
- phone,
- Telegram handle,
- email,
- city,
- date of birth / age if collected.

### Class B: Case and Intake Data

Examples:
- complaints,
- lifestyle answers,
- nutrition answers,
- supplement history,
- chronic condition notes.

### Class C: Special Category Health Data

Examples:
- lab values,
- uploaded analyses,
- symptoms,
- health-related hypotheses,
- reports based on health context.

### Class D: System and Security Data

Examples:
- operator account,
- admin access events,
- export logs,
- deletion confirmations,
- IP / device logs when applicable.

## Minimum Access Model

### Olga / Authorized Specialist

May access:
- client card,
- case data,
- uploads,
- generated reports,
- consents where needed.

### Developer

Default production access:
- no standing access to real client content,
- only controlled temporary access by written instruction,
- only to the minimum scope needed,
- all access logged.

### Support / Operations

May access:
- incident metadata,
- queue status,
- technical logs.

Should not have default access to full health content.

## Current Project Gap Map

Current codebase behavior:
- stores submissions in local JSON,
- stores uploaded files on local disk,
- stores drafts on local disk,
- stores runtime state on local disk,
- exports drafts to Obsidian Vault.

Production risk:
- local desktop as primary storage,
- uncontrolled duplication,
- weak access separation,
- difficult retention/deletion management,
- Obsidian export creates extra uncontrolled copy of special-category data.

## Recommended Migration Path

### Phase 1. Immediate Hygiene

- disable optional uncontrolled exports of client health data,
- stop treating local folders as the production archive,
- add explicit consent records,
- add access logging,
- define operator / processor roles.

### Phase 2. Controlled Persistence

- move structured data to PostgreSQL in RF,
- move uploads to private object storage in RF,
- keep only temporary working cache locally,
- separate test and production data.

### Phase 3. Compliance Operations

- publish privacy policy,
- collect explicit consent for personal data and health-related data,
- notify Roskomnadzor if applicable,
- document retention and deletion process,
- formalize developer processing by instruction.

## Recommended Retention Approach

Initial working recommendation:
- active client case: for service period plus defined archive term,
- signed consent: no shorter than the period needed to prove legality of processing,
- technical logs: limited operational retention,
- deleted case: remove live access immediately, retain deletion log only.

Final numbers should be approved by operator and legal counsel.

## Non-Negotiable Production Rules

- source-of-truth database and file storage in Russia,
- explicit health-data consent,
- published privacy policy,
- role-based access,
- audit log,
- deletion workflow,
- processor agreement for developer access,
- no uncontrolled exports to local knowledge tools by default.
