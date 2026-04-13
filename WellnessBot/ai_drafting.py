from __future__ import annotations

import json
import logging
import httpx

from openai import OpenAI

from config import Settings
from prompts import (
    DOSSIER_DRAFT_PROMPT,
    LIVE_CHAT_PROMPT,
    PREMIUM_PROMPT,
    SOCIAL_PROMPT,
    SPORT_PROMPT,
)

TIER_PROMPTS = {
    "premium": PREMIUM_PROMPT,
    "sport": SPORT_PROMPT,
    "social": SOCIAL_PROMPT,
}


def get_system_prompt_for_tier(tier: str | None) -> str:
    """Return the tier-specific system prompt, falling back to the generic dossier prompt."""
    if tier and tier in TIER_PROMPTS:
        return TIER_PROMPTS[tier] + "\n\n" + DOSSIER_DRAFT_PROMPT
    return DOSSIER_DRAFT_PROMPT

logger = logging.getLogger("wellness_bot.ai")
YANDEX_FOUNDATION_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def build_client(settings: Settings) -> OpenAI:
    client_kwargs: dict = {"api_key": settings.llm_api_key}

    if settings.llm_base_url:
        client_kwargs["base_url"] = settings.llm_base_url

    if settings.llm_project_id:
        client_kwargs["project"] = settings.llm_project_id

    if settings.llm_disable_server_logging:
        client_kwargs["default_headers"] = {"x-data-logging-enabled": "false"}

    return OpenAI(**client_kwargs)


def generate_case_draft_yandex_foundation(settings: Settings, submission: dict, tier: str | None = None) -> str | None:
    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": "2000",
        },
        "messages": [
            {"role": "system", "text": get_system_prompt_for_tier(tier).strip()},
            {"role": "user", "text": json.dumps(submission, ensure_ascii=False, indent=2)},
        ],
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None


def generate_live_reply_yandex_foundation(
    settings: Settings,
    history: list[dict[str, str]],
    user_text: str,
) -> str | None:
    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    messages: list[dict[str, str]] = [{"role": "system", "text": LIVE_CHAT_PROMPT.strip()}]
    for item in history[-10:]:
        role = item.get("role")
        text = (item.get("content") or "").strip()
        if role in {"user", "assistant"} and text:
            messages.append({"role": role, "text": text})
    messages.append({"role": "user", "text": user_text.strip()})

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": "1200",
        },
        "messages": messages,
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None


def extract_chat_completion_text(response) -> str | None:
    if not response.choices:
        return None

    message = response.choices[0].message
    content = getattr(message, "content", None)

    if isinstance(content, str):
        return content.strip() or None

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text_value = getattr(item, "text", None)
            if text_value:
                parts.append(text_value)
        merged = "\n".join(parts).strip()
        return merged or None

    return None


def generate_case_draft(settings: Settings, submission: dict, tier: str | None = None) -> str | None:
    if settings.llm_provider == "disabled":
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return None

    if settings.llm_provider == "yandex_foundation":
        return generate_case_draft_yandex_foundation(settings, submission, tier=tier)

    client = build_client(settings)
    submission_payload = json.dumps(submission, ensure_ascii=False, indent=2)

    if settings.llm_api_mode == "chat_completions":
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": get_system_prompt_for_tier(tier)},
                {"role": "user", "content": submission_payload},
            ],
            temperature=0.2,
        )
        return extract_chat_completion_text(response)

    response = client.responses.create(
        model=settings.llm_model,
        instructions=get_system_prompt_for_tier(tier),
        input=submission_payload,
    )
    return (response.output_text or "").strip() or None


def generate_live_reply(
    settings: Settings,
    history: list[dict[str, str]],
    user_text: str,
) -> str | None:
    if settings.llm_provider == "disabled":
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return None

    if settings.llm_provider == "yandex_foundation":
        return generate_live_reply_yandex_foundation(settings, history, user_text)

    client = build_client(settings)
    if settings.llm_api_mode == "chat_completions":
        messages: list[dict[str, str]] = [{"role": "system", "content": LIVE_CHAT_PROMPT}]
        for item in history[-10:]:
            role = item.get("role")
            text = (item.get("content") or "").strip()
            if role in {"user", "assistant"} and text:
                messages.append({"role": role, "content": text})
        messages.append({"role": "user", "content": user_text.strip()})

        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            temperature=0.4,
        )
        return extract_chat_completion_text(response)

    transcript = []
    for item in history[-10:]:
        role = item.get("role")
        text = (item.get("content") or "").strip()
        if role in {"user", "assistant"} and text:
            transcript.append(f"{role}: {text}")
    transcript.append(f"user: {user_text.strip()}")
    response = client.responses.create(
        model=settings.llm_model,
        instructions=LIVE_CHAT_PROMPT,
        input="\n".join(transcript),
    )
    return (response.output_text or "").strip() or None
