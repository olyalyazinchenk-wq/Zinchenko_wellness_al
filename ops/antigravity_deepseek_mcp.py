from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "WellnessBot" / ".env")


SERVER_NAME = "deepseek-v4"
SERVER_VERSION = "2026.04.25"


def _env_value(*keys: str) -> str | None:
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return None


def _safe_error(exc: Exception) -> str:
    text = str(exc)
    api_key = _env_value("DEEPSEEK_API_KEY", "LLM_API_KEY")
    if api_key:
        text = text.replace(api_key, "[REDACTED]")
    return text


def _response(payload_id: Any, result: Any = None, error: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": payload_id}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    return payload


def _tool_schema() -> dict[str, Any]:
    return {
        "name": "deepseek_v4_chat",
        "description": (
            "Send a Russian or English prompt to DeepSeek v4 via the project's DeepSeek API key. "
            "Use for independent reasoning, drafting, review, and structured text generation."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The user prompt to send to DeepSeek v4.",
                },
                "system": {
                    "type": "string",
                    "description": "Optional system instruction.",
                },
                "temperature": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 2,
                    "default": 0.2,
                },
                "max_tokens": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 8000,
                    "default": 2000,
                },
                "thinking": {
                    "type": "string",
                    "enum": ["disabled", "enabled"],
                    "default": "disabled",
                    "description": "DeepSeek V4 thinking mode. Disabled is better for direct tool answers.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": False,
        },
    }


def call_deepseek(arguments: dict[str, Any]) -> str:
    api_key = _env_value("DEEPSEEK_API_KEY", "LLM_API_KEY")
    if not api_key:
        raise RuntimeError("DeepSeek API key is not configured in .env.")

    base_url = (_env_value("DEEPSEEK_BASE_URL", "LLM_BASE_URL") or "https://api.deepseek.com").rstrip("/")
    model = _env_value("DEEPSEEK_MODEL", "LLM_MODEL") or "deepseek-v4-flash"
    prompt = str(arguments.get("prompt") or "").strip()
    if not prompt:
        raise ValueError("prompt is required.")

    system = str(arguments.get("system") or "You are a precise, safe, practical assistant.").strip()
    temperature = float(arguments.get("temperature", 0.2))
    max_tokens = int(arguments.get("max_tokens", 2000))
    thinking = str(arguments.get("thinking") or "disabled").strip().lower()
    if thinking not in {"disabled", "enabled"}:
        thinking = "disabled"

    response = httpx.post(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "thinking": {"type": thinking},
        },
        timeout=90,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return str(message.get("content") or message.get("reasoning_content") or "").strip()


def handle_request(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    payload_id = message.get("id")

    if method == "initialize":
        return _response(
            payload_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return _response(payload_id, {})

    if method == "tools/list":
        return _response(payload_id, {"tools": [_tool_schema()]})

    if method == "tools/call":
        params = message.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name != "deepseek_v4_chat":
            return _response(
                payload_id,
                error={"code": -32602, "message": f"Unknown tool: {name}"},
            )
        try:
            text = call_deepseek(arguments)
            return _response(payload_id, {"content": [{"type": "text", "text": text}]})
        except Exception as exc:
            return _response(
                payload_id,
                error={"code": -32000, "message": _safe_error(exc)},
            )

    if payload_id is None:
        return None

    return _response(
        payload_id,
        error={"code": -32601, "message": f"Method not found: {method}"},
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            response = handle_request(message)
            if response is not None:
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            sys.stdout.write(
                json.dumps(
                    _response(None, error={"code": -32700, "message": _safe_error(exc)}),
                    ensure_ascii=False,
                )
                + "\n"
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()
