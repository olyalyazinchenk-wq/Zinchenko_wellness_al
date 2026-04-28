# Hosting / VPS Decision

Date: 2026-04-21
Owner: Olga / Wellness Bot
Purpose: decide whether the project needs VPS hosting now, later, or not at all.

## Executive Verdict

The project does not need VPS as the very first blocker.

The current first blocker is still:

- live `PAYMENT_TOKEN`,
- one real Telegram e2e walkthrough,
- human-reviewed pilot delivery.

But VPS or cloud VM becomes necessary when the bot must work reliably without Olga's computer being on.

## Current Runtime Reality

The bot currently runs as:

- Python process,
- Telegram polling mode,
- local JSON storage under `WellnessBot/data/`,
- local `.env` configuration,
- local logs,
- local uploads and generated drafts.

This is acceptable for:

- development,
- local smoke tests,
- guided pilot testing,
- one controlled operator-managed walkthrough.

This is not ideal for:

- real 24/7 clients,
- paid traffic,
- unattended payment flow,
- stable intake while the operator computer is off,
- clean backup and incident handling.

## Existing Infra Status

The project already contains a VM direction:

- `infra/vm/wellness-bot.service`
- `infra/vm/deploy_bot.sh`
- `infra/cloud-init/deepseek-bootstrap.yaml`
- `infra/README_DEEPSEEK_VM.md`

This means the architecture already expects a server-like environment later.

However, current deployment assets are still starter-level, not full production operations.

## Decision Matrix

### Local computer is enough if

- Olga is testing manually,
- traffic is not public,
- payment is not fully live,
- cases are few and controlled,
- interruptions are acceptable.

### VPS / cloud VM is needed if

- the bot should work every day without the laptop,
- clients may write at night or outside operator hours,
- payment branch is live,
- paid traffic is running,
- data loss would be painful,
- you want a real pilot, not a local demo.

### Managed platform can be considered if

- you want less server administration,
- there is no need to self-host a model,
- persistent storage and backups are solved separately.

For this Python Telegram polling bot, a simple VM is currently the most straightforward path.

## Recommended Launch Sequence

### Step 1. Finish payment activation locally

Do first:

- connect YooKassa / Telegram provider token,
- add `PAYMENT_TOKEN`,
- run one live Telegram e2e walkthrough.

Reason:

- if payment is not working, VPS does not solve the real blocker.

### Step 2. Run first controlled pilot locally or on a temporary VM

Acceptable options:

- local controlled run for one test case,
- or small VM if Olga wants the bot online continuously during the first pilot.

### Step 3. Move to VPS before public launch

Before sending public traffic or selling broadly, move runtime to VPS / cloud VM.

Minimum server requirements:

- Linux Ubuntu VM,
- systemd service,
- Python virtual environment,
- secure `.env`,
- persistent `WellnessBot/data`,
- backup path,
- log rotation,
- restricted SSH access,
- firewall,
- monitoring or at least restart-on-failure.

## Recommended Minimal VPS Profile

For bot-only runtime:

- 1-2 vCPU,
- 2 GB RAM minimum,
- 20-40 GB SSD,
- Ubuntu 24.04,
- daily backups if possible.

If self-hosting a model such as DeepSeek locally:

- CPU-only small VM is likely slow,
- GPU quota / cost becomes a separate decision,
- for launch it is better to use Yandex AI Studio / Foundation / compatible API rather than self-host heavy inference.

## Data And Compliance Note

The bot handles sensitive wellness and health-related data.

For production, hosting should prioritize:

- RF-hosted infrastructure where possible,
- controlled access,
- encrypted secrets,
- regular backups,
- documented deletion workflow.

Local laptop storage is not the desired long-term source of truth.

## Final Recommendation

Do not buy or configure VPS before finishing the payment live walkthrough unless Olga specifically wants the bot online while she is away from the computer.

But do plan VPS / cloud VM before real public pilot launch.

Practical decision:

- now: finish YooKassa and live e2e,
- next: prepare production VM checklist,
- before public traffic: deploy bot to VPS / cloud VM.
