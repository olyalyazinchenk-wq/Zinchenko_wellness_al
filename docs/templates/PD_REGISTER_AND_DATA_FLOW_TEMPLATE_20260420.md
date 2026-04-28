# Personal Data Register and Data Flow Template

Use this as the operator's internal inventory.

Current public service identifiers:
- Telegram bot: `@zinchenko_wellness_ai_1_bot`
- Telegram channel: `@olga_nutri86`
- Expert / service face: `Ольга Зинченко`

## System Register

| System / Location | Purpose | Data Categories | Special Health Data | Operator / Processor | RF Location Confirmed | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Bot | Intake transport | Contact, messages, files | Yes | Operator + Telegram as platform | [fill] | Transport channel |
| App Server | Processing | Intake, status, logs | Yes | [fill] | [fill] | |
| Database | Source of truth | Structured client records | Yes | [fill] | [fill] | |
| Object Storage | File archive | PDFs, photos, reports | Yes | [fill] | [fill] | |
| LLM Provider | Draft generation | Case fragments / prompts | Potentially yes | [fill] | [fill] | Check contract and routing |
| Developer Workstation | Temporary technical access only | Should be minimized | Potentially yes | Processor by instruction | [fill] | No master archive |

## Data Flow

1. Client sends intake and files in Telegram.
2. Bot writes structured record into RF-hosted database.
3. Files go into private RF-hosted object storage.
4. Consent record is stored with timestamp and proof.
5. Specialist reviews case in controlled environment.
6. Generated report is stored in controlled storage.
7. Client receives final output in Telegram or another approved channel.

## Processor Inventory

| Processor | Task | Data Scope | Contract Signed | Access Level | Notes |
| --- | --- | --- | --- | --- | --- |
| Developer | Maintenance / debugging | Minimum necessary | [yes/no] | temporary | |
| Hosting provider | Infrastructure | System and stored data | [yes/no] | indirect | |
| LLM provider | Draft generation | Prompt payload | [yes/no] | scoped | |
