# Antigravity Wellness Platform

This workspace currently contains three practical layers:

- a static product prototype in the project root
- a working Telegram-first intake and dossier bot in `WellnessBot/`
- a growing product-ops and governance layer in `docs/` and `ops/`

## Product Direction

The first real product wedge is:

`Wellness Clarity in Telegram`

The flagship paid artifact is:

`Premium Wellness Dossier`

Principle:

- Telegram-first intake
- first useful clarity before deep case work
- AI-assisted internal case drafting
- mandatory human review before any final client output
- product governance, experiment tracking, and admin operating rhythm

## Project Structure

- `index.html`, `styles.css`, `app.js` - static landing/demo prototype
- `PROJECT_AUDIT.md` - current-state audit
- `PRODUCT_OPERATING_SYSTEM.md` - product and execution strategy
- `PERMISSIONS_REGISTER.md` - permissions and access register
- `RUSSIAN_AI_CONTOUR.md` - Russian-contour runtime strategy
- `YANDEX_AI_STUDIO_SETUP.md` - practical Yandex AI Studio setup steps
- `WellnessBot/main.py` - Telegram intake flow
- `WellnessBot/config.py` - environment configuration
- `WellnessBot/ai_drafting.py` - optional OpenAI draft generation
- `WellnessBot/storage.py` - local JSON and upload storage
- `WellnessBot/texts.py` - user-facing copy
- `WellnessBot/prompts.py` - internal dossier drafting prompt
- `docs/PROJECT_PULSE_LOG.md` - execution and remediation changelog
- `docs/ORCHESTRATION_REMEDIATION_BLUEPRINT_20260420.md` - current architecture and next-stage plan

## Bot Environment

Copy `.env.example` to `.env` and fill in the values.

Required:

- `BOT_TOKEN`

Optional:

- `ADMIN_CHAT_IDS`
- `BOT_PROXY_URL`
- `PAYMENT_TOKEN`
- `LLM_PROVIDER`
- `LLM_API_KEY`
- `LLM_MODEL`
- `LLM_API_MODE`
- `LLM_BASE_URL`
- `LLM_PROJECT_ID`
- `LLM_DISABLE_SERVER_LOGGING`
- `LLM_USE_IAM_TOKEN`
- `ENABLE_TMA`

## Recommended LLM Modes

### 1. No external AI

Best for the strictest data posture.

```env
LLM_PROVIDER=disabled
```

### 2. Yandex AI Studio in Russian contour

Useful when you want OpenAI-compatible APIs in Yandex Cloud.

```env
LLM_PROVIDER=yandex_ai_studio
LLM_API_MODE=responses
LLM_API_KEY=your_yandex_api_key
LLM_BASE_URL=https://ai.api.cloud.yandex.net/v1
LLM_PROJECT_ID=your_folder_id
LLM_MODEL=gpt://your_folder_id/your_model_uri
LLM_DISABLE_SERVER_LOGGING=true
```

Yandex documents OpenAI compatibility for Responses API and the option to disable request logging with
`x-data-logging-enabled: false`.

### 3. Yandex Foundation Models API

Useful when you want the simplest Russian-cloud integration with a service-account API key and the
`ai.languageModels.user` role.

```env
LLM_PROVIDER=yandex_foundation
LLM_API_KEY=your_service_account_api_key
LLM_MODEL=gpt://your_folder_id/yandexgpt/latest
LLM_API_MODE=completion
LLM_BASE_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
LLM_PROJECT_ID=your_folder_id
LLM_USE_IAM_TOKEN=false
```

### 4. Your own OpenAI-compatible endpoint

Useful for a self-hosted DeepSeek runtime in Yandex Cloud, such as vLLM or Ollama behind a private endpoint.

```env
LLM_PROVIDER=openai_compatible
LLM_API_MODE=chat_completions
LLM_API_KEY=your_internal_or_gateway_key
LLM_BASE_URL=https://your-internal-endpoint.example/v1
LLM_MODEL=deepseek-r1:8b
LLM_DISABLE_SERVER_LOGGING=true
```

## Local Run

If your shell still resolves `python` to the Windows Store alias, use the installed interpreter directly:

```powershell
C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv
.venv\Scripts\python.exe -m pip install -r WellnessBot\requirements.txt
.venv\Scripts\python.exe WellnessBot\main.py
```

## Current Runtime Status

- Telegram intake is live in polling mode
- Premium dossier flow includes payment, admin review, and governance commands
- TMA is disabled by default until security hardening is fully completed
- OCR / Vision enrichment exists, but still remains a product-hardening area rather than a fully trusted production promise

## Notes

- Uploads, submissions, and AI drafts are stored locally under `WellnessBot/data/`
- `.env` and runtime data should not be committed
- The current bot is designed for polling-first validation and controlled pilot delivery
- The bot can now work with `responses` or `chat_completions` style OpenAI-compatible providers
- The bot also supports direct Yandex Foundation Models API calls
- On Windows, the bot auto-detects the system proxy when `BOT_PROXY_URL` is not set
- Sensitive health data is still stored locally, so this workspace should be treated as a controlled development/staging environment, not a broad production deployment

## Runtime Commands

User commands:

- `/start`
- `/reset`
- `/chat`
- `/chat_reset`
- `/tma` (only when `ENABLE_TMA=true`)

Admin commands:

- `/queue`
- `/health`
- `/insights`
- `/governance`
- `/experiments`
- `/decisions`
- `/gaps`
- `/learnings`
- `/decide`
- `/expstatus`
- `/review`
- `/weekly`
- `/brief`
- `/suggestdecisions`
- `/applydecision`
- `/decisionplan`
- `/digestnow`
- `/llmprobe`

## Ops Control Center

Project now includes an execution toolkit under `ops/`:

- `ops/preflight.ps1` - runtime preflight checks
- `ops/bot-start.ps1` - stable bot start
- `ops/bot-stop.ps1` - stop bot process
- `ops/bot-restart.ps1` - restart + status
- `ops/bot-status.ps1` - process/log status
- `ops/llm-smoke.ps1` - one-shot LLM response check
- `ops/quality-check.ps1` - batch quality report to `ops/reports/`

## Production Pilot Deploy

The VPS deployment package lives in `infra/deploy/`.

Start with:

- `docs/PRODUCTION_LAUNCH_RUNBOOK_20260421.md`
- `infra/deploy/deploy_to_vps.ps1`
- `infra/deploy/install_ubuntu.sh`
- `infra/deploy/wellness-bot.service`
- `infra/deploy/backup_data.sh`

Recommended first launch mode: controlled paid pilot on an Ubuntu VPS, Telegram polling, mandatory human review, local encrypted-access discipline, and daily backups.

Strategy board and controls:

- `docs/NCB.md`
- `ops/permissions-checklist.md`
- `docs/AGENT_CONTEXT_HUB.md`
- `docs/PROJECT_PULSE_LOG.md`
- `docs/ORCHESTRATION_REMEDIATION_BLUEPRINT_20260420.md`
