# Production Launch Runbook

Date: 2026-04-21

Scope: Telegram-first pilot launch for the Antigravity Wellness bot and Premium Wellness Dossier flow.

## Current Technical Status

- Local preflight passes.
- Telegram bot entrypoint exists: `WellnessBot/main.py`.
- Root `.env` is present locally and contains the runtime configuration.
- Payment smoke test passes.
- Admin/governance smoke test passes.
- LLM smoke test returns a live reply.
- Bot is not currently running locally, but previous logs show successful polling for `@zinchenko_wellness_ai_1_bot`.

## Recommended Launch Mode

Use a small Ubuntu VPS and keep the bot in Telegram polling mode for the first paid pilot.

Why:

- No domain or TLS setup is required.
- Telegram polling is simpler than webhook deployment.
- The current product still requires human review, so operational stability matters more than web-scale architecture.
- Runtime data is stored locally in `WellnessBot/data`, which is acceptable for a controlled pilot if backups and access control are in place.

Recommended VPS for the paid pilot:

- Primary: Hetzner CX23, Ubuntu 24.04.
- Fallback: BuyVM Slice 1024 or 2048, Luxembourg location when in stock.
- Convenience fallback: DigitalOcean Basic 1 GiB.

Recommended VPS for a mass launch with operational reserve:

- Primary: Hetzner CX43, Ubuntu 24.04, backups enabled.
- Conservative high-reserve option: Hetzner CX53 if PDF/OCR generation and admin workflows become highly concurrent.
- Avoid the smallest VPS classes for the public launch. The bot itself is light, but health-data storage, logs, PDF generation, OCR, backups, and emergency maintenance need spare memory and disk.

## Server Layout

Expected path:

```text
/opt/antigravity-wellness
```

Runtime data:

```text
/opt/antigravity-wellness/WellnessBot/data
```

Backups:

```text
/var/backups/wellness-bot
```

Systemd service:

```text
wellness-bot.service
```

## First Deploy From Local Machine

If the VPS already exists, deploy from the project root on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\infra\deploy\deploy_to_vps.ps1 -HostName <SERVER_IP>
```

If using Hetzner Cloud and `HCLOUD_TOKEN` is available, create a production-reserve server and deploy in one run:

```powershell
$env:HCLOUD_TOKEN="paste_token_here"
powershell -ExecutionPolicy Bypass -File .\infra\deploy\create_hetzner_production_server.ps1
```

Default production profile:

```text
server_type = cx43
location = hel1
image = ubuntu-24.04
backups = enabled
```

The deploy helper intentionally excludes:

- `.env`
- `.venv`
- `.git`
- `WellnessBot/data`
- local bot logs
- generated ops reports

## Server Environment

On the server:

```bash
cd /opt/antigravity-wellness
cp infra/deploy/env.production.example .env
nano .env
chown wellnessbot:wellnessbot .env
chmod 600 .env
```

Required values:

```env
BOT_TOKEN=
ADMIN_CHAT_IDS=
```

Optional but production-relevant:

```env
PAYMENT_TOKEN=
LLM_PROVIDER=
LLM_API_KEY=
LLM_MODEL=
LLM_API_MODE=
LLM_BASE_URL=
LLM_PROJECT_ID=
```

Keep this disabled unless the Mini App surface is intentionally hardened:

```env
ENABLE_TMA=false
```

## Start And Check

```bash
systemctl restart wellness-bot
systemctl status wellness-bot --no-pager
journalctl -u wellness-bot -n 100 --no-pager
```

Live logs:

```bash
journalctl -u wellness-bot -f
```

Expected result:

- The process stays active.
- Logs show aiogram polling start.
- `/health` works for the admin account.
- `/queue` works for the admin account.

## Smoke Test Before Taking Payments

Run these locally before the final deploy and again after major changes:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest tests
.\.venv\Scripts\python.exe .\ops\payment_case_smoke.py
.\.venv\Scripts\python.exe .\ops\admin_governance_smoke.py
powershell -ExecutionPolicy Bypass -File .\ops\llm-smoke.ps1
powershell -ExecutionPolicy Bypass -File .\ops\quality-check.ps1
```

Manual Telegram smoke:

1. Send `/start`.
2. Complete intake with a test case.
3. Send a test lab file or photo if OCR is part of the pilot.
4. Trigger the paid dossier path.
5. Confirm the admin account sees the case in `/queue`.
6. Confirm no final client output is sent without human review.

## Backup

Manual backup:

```bash
sudo wellness-bot-backup
```

Add daily cron:

```bash
sudo crontab -e
```

```cron
17 2 * * * /usr/local/sbin/wellness-bot-backup >/var/log/wellness-bot-backup.log 2>&1
```

Backups contain health-related client data. Treat backup files as sensitive.

## Update Deploy

From local machine:

```powershell
powershell -ExecutionPolicy Bypass -File .\infra\deploy\deploy_to_vps.ps1 -HostName <SERVER_IP>
```

Then on the server:

```bash
systemctl status wellness-bot --no-pager
journalctl -u wellness-bot -n 100 --no-pager
```

The deploy helper does not overwrite `.env` or `WellnessBot/data`.

## Rollback

Minimum safe rollback path for the pilot:

1. Stop intake by pausing public promotion.
2. Stop service:

```bash
systemctl stop wellness-bot
```

3. Restore the previous project archive or redeploy the last known good local copy.
4. Restart:

```bash
systemctl restart wellness-bot
```

5. Check:

```bash
systemctl status wellness-bot --no-pager
journalctl -u wellness-bot -n 100 --no-pager
```

## Go-Live Checklist

- VPS is created and SSH key access works.
- `ufw` allows only OpenSSH by default.
- Project is deployed to `/opt/antigravity-wellness`.
- `.env` is filled on the server and has `600` permissions.
- `wellness-bot.service` is active.
- Admin `/health` and `/queue` commands work.
- Payment token is set only after payment provider checks are complete.
- At least one full manual test case is completed.
- Backup command works and cron is configured.
- Public copy includes non-diagnostic positioning and emergency disclaimers.
- Human review remains mandatory before sending final dossier output.

## Launch Recommendation

Launch as a controlled paid pilot, not as broad production:

- 10 to 30 clients.
- Manual review for every dossier.
- Daily admin queue checks.
- Daily backup.
- Weekly review of payment failures, edge cases, and unsafe health prompts.

Move to webhook, database storage, domain, and stronger admin UI only after the first paid pilot validates the offer and operations.
