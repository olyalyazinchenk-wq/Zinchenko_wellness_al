from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import sys

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
ENV_FILE = PROJECT_ROOT / ".env"
ENV_FILE_LOCAL = BASE_DIR / ".env"

load_dotenv(ENV_FILE)
load_dotenv(ENV_FILE_LOCAL)


def parse_admin_chat_ids(raw_value: str | None) -> list[int]:
    if not raw_value:
        return []

    admin_ids: list[int] = []
    for chunk in raw_value.split(","):
        candidate = chunk.strip()
        if not candidate:
            continue
        try:
            admin_ids.append(int(candidate))
        except ValueError:
            continue
    return admin_ids


@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_proxy_url: str | None
    llm_provider: str
    llm_api_key: str | None
    llm_model: str | None
    llm_api_mode: str
    llm_base_url: str | None
    llm_project_id: str | None
    llm_disable_server_logging: bool
    llm_use_iam_token: bool
    stt_provider: str
    stt_api_key: str | None
    stt_project_id: str | None
    stt_use_iam_token: bool
    admin_chat_ids: list[int]
    tg_payment_token: str | None
    payment_mode: str
    tma_enabled: bool
    data_dir: Path
    submissions_dir: Path
    uploads_dir: Path
    drafts_dir: Path
    runtime_state_path: Path
    product_insights_path: Path
    product_governance_path: Path

    def ensure_dirs(self) -> None:
        for directory in (self.data_dir, self.submissions_dir, self.uploads_dir, self.drafts_dir):
            directory.mkdir(parents=True, exist_ok=True)


def parse_bool(raw_value: str | None, default: bool = False) -> bool:
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def read_windows_system_proxy() -> str | None:
    if sys.platform != "win32":
        return None

    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        ) as key:
            proxy_enabled = winreg.QueryValueEx(key, "ProxyEnable")[0]
            proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
    except OSError:
        return None

    if not proxy_enabled or not proxy_server:
        return None

    if "://" in proxy_server:
        return proxy_server.strip()

    if "=" in proxy_server:
        first_entry = proxy_server.split(";", 1)[0]
        proxy_server = first_entry.split("=", 1)[-1]

    return f"http://{proxy_server.strip()}"


def validate_llm_settings(settings: Settings) -> None:
    if settings.llm_provider == "disabled":
        return

    if not settings.llm_api_key:
        raise RuntimeError("LLM provider is enabled, but LLM_API_KEY is missing.")

    if not settings.llm_model:
        raise RuntimeError("LLM provider is enabled, but LLM_MODEL is missing.")

    if settings.llm_provider == "yandex_foundation":
        if settings.llm_api_mode != "completion":
            raise RuntimeError("yandex_foundation requires LLM_API_MODE=completion.")
        return

    if settings.llm_provider == "yandex_ai_studio":
        if settings.llm_api_mode not in {"responses", "chat_completions"}:
            raise RuntimeError(
                "yandex_ai_studio requires LLM_API_MODE to be responses or chat_completions."
            )
        if not settings.llm_base_url:
            raise RuntimeError("yandex_ai_studio requires LLM_BASE_URL.")
        return

    if settings.llm_provider == "openai_compatible":
        if settings.llm_api_mode not in {"responses", "chat_completions"}:
            raise RuntimeError(
                "openai_compatible requires LLM_API_MODE to be responses or chat_completions."
            )
        if not settings.llm_base_url:
            raise RuntimeError("openai_compatible requires LLM_BASE_URL.")
        return

    if settings.llm_provider == "openai":
        if settings.llm_api_mode not in {"responses", "chat_completions"}:
            raise RuntimeError("openai requires LLM_API_MODE to be responses or chat_completions.")
        return

    raise RuntimeError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")


def validate_stt_settings(settings: Settings) -> None:
    if settings.stt_provider == "disabled":
        return

    if settings.stt_provider != "yandex_speechkit":
        raise RuntimeError(f"Unsupported STT_PROVIDER: {settings.stt_provider}")

    if not settings.stt_api_key:
        raise RuntimeError("STT_PROVIDER=yandex_speechkit requires STT_API_KEY.")

    if not settings.stt_project_id:
        raise RuntimeError("STT_PROVIDER=yandex_speechkit requires STT_PROJECT_ID.")


def validate_settings(settings: Settings) -> Settings:
    if not settings.bot_token:
        return settings

    if settings.payment_mode not in {"manual", "telegram"}:
        raise RuntimeError("PAYMENT_MODE must be manual or telegram.")

    validate_llm_settings(settings)
    validate_stt_settings(settings)
    return settings


def load_settings() -> Settings:
    data_dir = BASE_DIR / "data"
    llm_api_key = os.getenv("LLM_API_KEY", "").strip() or os.getenv("OPENAI_API_KEY", "").strip() or None
    llm_model = os.getenv("LLM_MODEL", "").strip() or os.getenv("OPENAI_MODEL", "").strip() or None
    llm_provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    llm_project_id = os.getenv("LLM_PROJECT_ID", "").strip() or None
    llm_use_iam_token = parse_bool(os.getenv("LLM_USE_IAM_TOKEN"), default=False)
    bot_proxy_url = os.getenv("BOT_PROXY_URL", "").strip() or read_windows_system_proxy()

    if not llm_provider:
        llm_provider = "disabled" if not llm_api_key else "openai"

    stt_provider = os.getenv("STT_PROVIDER", "").strip().lower()
    if not stt_provider:
        stt_provider = "yandex_speechkit" if llm_provider == "yandex_foundation" else "disabled"

    stt_api_key = os.getenv("STT_API_KEY", "").strip() or None
    stt_project_id = os.getenv("STT_PROJECT_ID", "").strip() or None
    if stt_provider == "yandex_speechkit":
        stt_api_key = stt_api_key or (llm_api_key if llm_provider == "yandex_foundation" else None)
        stt_project_id = stt_project_id or llm_project_id
    stt_use_iam_token = parse_bool(
        os.getenv("STT_USE_IAM_TOKEN"),
        default=llm_use_iam_token if stt_provider == "yandex_speechkit" else False,
    )

    settings = Settings(
        bot_token=os.getenv("BOT_TOKEN", "").strip(),
        bot_proxy_url=bot_proxy_url,
        llm_provider=llm_provider,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_api_mode=os.getenv("LLM_API_MODE", "responses").strip().lower(),
        llm_base_url=os.getenv("LLM_BASE_URL", "").strip() or None,
        llm_project_id=llm_project_id,
        llm_disable_server_logging=parse_bool(
            os.getenv("LLM_DISABLE_SERVER_LOGGING"),
            default=True,
        ),
        llm_use_iam_token=llm_use_iam_token,
        stt_provider=stt_provider,
        stt_api_key=stt_api_key,
        stt_project_id=stt_project_id,
        stt_use_iam_token=stt_use_iam_token,
        admin_chat_ids=parse_admin_chat_ids(os.getenv("ADMIN_CHAT_IDS")),
        tg_payment_token=os.getenv("PAYMENT_TOKEN", "").strip() or None,
        payment_mode=os.getenv("PAYMENT_MODE", "manual").strip().lower(),
        tma_enabled=parse_bool(os.getenv("ENABLE_TMA"), default=False),
        data_dir=data_dir,
        submissions_dir=data_dir / "submissions",
        uploads_dir=data_dir / "uploads",
        drafts_dir=data_dir / "drafts",
        runtime_state_path=data_dir / "runtime_state.json",
        product_insights_path=data_dir / "product_insights.json",
        product_governance_path=data_dir / "product_governance.json",
    )
    settings.ensure_dirs()
    return validate_settings(settings)
