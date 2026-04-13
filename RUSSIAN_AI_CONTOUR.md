# Russian AI Contour

Date: 2026-04-13

## Goal

Keep product development, operations, and strategy in this workspace while routing any optional model inference through a Russian-controlled runtime.

## Recommended Runtime Hierarchy

### Level 1

`Recommended by default`

- Telegram bot collects intake
- submissions and uploads are stored locally or in Russian infrastructure
- human review is mandatory
- no external LLM is used for sensitive cases

### Level 2

- Yandex AI Studio with OpenAI-compatible API
- request logging disabled
- model access configured inside Yandex Cloud folder

Use when:

- you want the fastest Russian-cloud rollout
- you accept a managed runtime inside Yandex Cloud

### Level 3

- self-hosted DeepSeek or another model in Yandex Cloud
- private OpenAI-compatible endpoint for internal use

Use when:

- you want tighter operational control
- you need deeper vendor independence

## Current Code Support

The bot now supports:

- `LLM_PROVIDER=disabled`
- `LLM_PROVIDER=yandex_foundation`
- `LLM_PROVIDER=yandex_ai_studio`
- `LLM_PROVIDER=openai_compatible`

And both API styles:

- `LLM_API_MODE=responses`
- `LLM_API_MODE=chat_completions`

## Suggested First Production Path

1. Keep `LLM_PROVIDER=disabled` for live intake validation.
2. Validate operational flow and human review.
3. Connect Yandex AI Studio or your own DeepSeek endpoint only after intake quality is stable.

## Security Note

The current bot token is already active in local config. Since it was shared in chat, rotate it later in `@BotFather` after the current setup phase is complete.
