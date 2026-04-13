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
    admin_chat_ids: list[int]
    data_dir: Path
    submissions_dir: Path
    uploads_dir: Path
    drafts_dir: Path

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


def load_settings() -> Settings:
    data_dir = BASE_DIR / "data"
    llm_api_key = os.getenv("LLM_API_KEY", "").strip() or os.getenv("OPENAI_API_KEY", "").strip() or None
    llm_model = os.getenv("LLM_MODEL", "").strip() or os.getenv("OPENAI_MODEL", "").strip() or None
    llm_provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    bot_proxy_url = os.getenv("BOT_PROXY_URL", "").strip() or read_windows_system_proxy()

    if not llm_provider:
        llm_provider = "disabled" if not llm_api_key else "openai"

    settings = Settings(
        bot_token=os.getenv("BOT_TOKEN", "").strip(),
        bot_proxy_url=bot_proxy_url,
        llm_provider=llm_provider,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_api_mode=os.getenv("LLM_API_MODE", "responses").strip().lower(),
        llm_base_url=os.getenv("LLM_BASE_URL", "").strip() or None,
        llm_project_id=os.getenv("LLM_PROJECT_ID", "").strip() or None,
        llm_disable_server_logging=parse_bool(
            os.getenv("LLM_DISABLE_SERVER_LOGGING"),
            default=True,
        ),
        llm_use_iam_token=parse_bool(os.getenv("LLM_USE_IAM_TOKEN"), default=False),
        admin_chat_ids=parse_admin_chat_ids(os.getenv("ADMIN_CHAT_IDS")),
        data_dir=data_dir,
        submissions_dir=data_dir / "submissions",
        uploads_dir=data_dir / "uploads",
        drafts_dir=data_dir / "drafts",
    )
    settings.ensure_dirs()
    return settings
