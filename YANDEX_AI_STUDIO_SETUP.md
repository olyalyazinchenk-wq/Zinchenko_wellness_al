# Yandex AI Studio Setup

Date: 2026-04-13

## Goal

Connect the bot to a Russian AI runtime using Yandex AI Studio's OpenAI-compatible API.

If OpenAI-compatible mode is blocked by permissions in your organization, use the simpler provider:

```env
LLM_PROVIDER=yandex_foundation
LLM_API_KEY=<service_account_api_key>
LLM_MODEL=gpt://<folder_id>/yandexgpt/latest
LLM_API_MODE=completion
LLM_BASE_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
LLM_PROJECT_ID=<folder_id>
LLM_USE_IAM_TOKEN=false
```

## What the Code Already Supports

The bot already supports this configuration:

```env
LLM_PROVIDER=yandex_ai_studio
LLM_API_MODE=responses
LLM_API_KEY=<your_api_key>
LLM_BASE_URL=https://ai.api.cloud.yandex.net/v1
LLM_PROJECT_ID=<your_folder_id>
LLM_MODEL=gpt://<your_folder_id>/<model_uri>
LLM_DISABLE_SERVER_LOGGING=true
```

## Recommended Connection Plan

### 1. Create or select a Yandex Cloud folder

You need a folder for the project infrastructure and model access.

### 2. Create a service account

Use a dedicated service account for the bot, not a personal user key.

### 3. Assign the required role

For text generation, assign:

- `ai.languageModels.user`

If you plan to use Responses API and broader AI Studio agent features, check whether you also need:

- `ai.assistants.editor`

### 4. Create an API key for the service account

When creating the key, use a scope that covers AI Studio model execution.

Recommended broad scope:

- `yc.ai.foundationModels.execute`

### 5. Choose a model in Model Gallery

Use a text model that is available for synchronous prompting through OpenAI-compatible APIs.

The model value in config must use the Yandex URI format:

```text
gpt://<folder_id>/<model_name>
```

### 6. Disable server-side request logging

For sensitive requests, keep:

```env
LLM_DISABLE_SERVER_LOGGING=true
```

The bot already sends the `x-data-logging-enabled: false` header when this flag is enabled.

## What To Put In .env

Example:

```env
LLM_PROVIDER=yandex_ai_studio
LLM_API_MODE=responses
LLM_API_KEY=yc-...
LLM_BASE_URL=https://ai.api.cloud.yandex.net/v1
LLM_PROJECT_ID=b1g...
LLM_MODEL=gpt://b1g.../yandexgpt/latest
LLM_DISABLE_SERVER_LOGGING=true
```

## Validation Flow

Once these values are in `.env`:

1. Restart the bot.
2. Send `/llmprobe` from the admin chat.
3. Confirm that the bot returns a synthetic draft.
4. Only then enable AI-drafting for real internal cases.

## Important Notes

- Use synthetic or anonymized payloads first.
- Do not test with real client medical data until your Russian storage and consent contour are finalized.
- Rotate any leaked bot token after setup is stabilized.
