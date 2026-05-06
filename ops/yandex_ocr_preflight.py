from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from config import load_settings  # noqa: E402
from lab_ocr import get_yandex_ocr_credentials  # noqa: E402

# 1x1 transparent PNG. Good enough to validate auth/request path without client data.
ONE_PIXEL_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def main() -> int:
    settings = load_settings()
    credentials = get_yandex_ocr_credentials(settings)

    result: dict[str, object] = {
        "provider": "yandex_ocr",
        "has_api_key": bool(credentials.get("api_key")),
        "has_project_id": bool(credentials.get("project_id")),
        "uses_iam_token": bool(credentials.get("use_iam_token")),
        "status": "unknown",
    }

    if not result["has_api_key"] or not result["has_project_id"]:
        result["status"] = "missing_credentials"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    auth_scheme = "Bearer" if credentials.get("use_iam_token") else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {credentials['api_key']}",
        "x-folder-id": str(credentials["project_id"]),
        "Content-Type": "application/json",
    }
    body = {
        "mimeType": "image/png",
        "languageCodes": ["ru", "en"],
        "model": "table",
        "content": ONE_PIXEL_PNG_BASE64,
    }

    try:
        response = httpx.post(
            "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText",
            headers=headers,
            json=body,
            timeout=30.0,
            trust_env=False,
        )
    except httpx.RequestError as exc:
        result["status"] = "network_error"
        result["error_type"] = exc.__class__.__name__
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 3

    result["http_status"] = response.status_code
    if response.status_code in {200, 400, 422}:
        # 400/422 can still mean auth is valid but the synthetic image is not useful for OCR.
        result["status"] = "auth_path_ok"
        result["note"] = "Authentication did not fail. Use a real lab file for functional OCR verification."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if response.status_code in {401, 403}:
        result["status"] = "auth_failed"
        result["note"] = "Check STT_API_KEY/STT_USE_IAM_TOKEN/STT_PROJECT_ID or refresh Yandex IAM token."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 4

    result["status"] = "provider_unexpected_status"
    safe_body = response.text[:500].replace(str(credentials.get("api_key") or ""), "***")
    result["body_preview"] = safe_body
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 5


if __name__ == "__main__":
    raise SystemExit(main())
