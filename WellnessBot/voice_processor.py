import logging
import io
import httpx
from config import Settings
from aiogram import Bot

logger = logging.getLogger("wellness_bot.voice")

SUPPORTED_SYNC_AUDIO_EXTENSIONS = {".ogg", ".oga", ".opus"}
SUPPORTED_SYNC_AUDIO_MIME_TYPES = {
    "audio/ogg",
    "audio/opus",
    "application/ogg",
}
SYNC_STT_MAX_BYTES = 1_000_000
SYNC_STT_MAX_DURATION_SECONDS = 30


def is_sync_audio_compatible(file_name: str | None = None, mime_type: str | None = None) -> bool:
    normalized_name = (file_name or "").lower()
    normalized_mime = (mime_type or "").lower()
    return any(normalized_name.endswith(ext) for ext in SUPPORTED_SYNC_AUDIO_EXTENSIONS) or normalized_mime in SUPPORTED_SYNC_AUDIO_MIME_TYPES


def is_yandex_stt_enabled(settings: Settings) -> bool:
    return settings.stt_provider == "yandex_speechkit" or settings.llm_provider == "yandex_foundation"


async def transcribe_voice_yandex(settings: Settings, ogg_data: bytes) -> str | None:
    api_key = settings.stt_api_key or (settings.llm_api_key if settings.llm_provider == "yandex_foundation" else None)
    project_id = settings.stt_project_id or settings.llm_project_id
    use_iam_token = settings.stt_use_iam_token or settings.llm_use_iam_token

    if not api_key or not project_id:
        logger.warning("Yandex STT is enabled but STT_API_KEY or STT_PROJECT_ID is missing.")
        return None

    auth_scheme = "Bearer" if use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {api_key}",
    }

    url = (
        "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
        f"?folderId={project_id}&lang=ru-RU&format=oggopus"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                content=ogg_data,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("result")
    except Exception as e:
        logger.exception("Yandex STT failed: %s", e)
        return None


async def download_telegram_file_bytes(bot: Bot, file_id: str) -> bytes | None:
    try:
        file = await bot.get_file(file_id)
        file_bytes = await bot.download_file(file.file_path)
        return file_bytes.read()
    except Exception:
        logger.exception("Failed to download voice file")
        return None


async def handle_voice_to_text(bot: Bot, file_id: str, settings: Settings) -> str | None:
    ogg_data = await download_telegram_file_bytes(bot, file_id)
    if not ogg_data:
        return None

    if is_yandex_stt_enabled(settings):
        return await transcribe_voice_yandex(settings, ogg_data)

    if settings.llm_provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.llm_api_key)
        try:
            audio_file = io.BytesIO(ogg_data)
            audio_file.name = "voice.ogg"
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
            return transcript.text
        except Exception as e:
            logger.exception("OpenAI Whisper failed: %s", e)
            return None

    return None


async def handle_audio_to_text(
    bot: Bot,
    file_id: str,
    settings: Settings,
    *,
    file_name: str | None = None,
    mime_type: str | None = None,
    duration_seconds: int | None = None,
    file_size: int | None = None,
) -> str | None:
    audio_data = await download_telegram_file_bytes(bot, file_id)
    if not audio_data:
        return None

    if is_yandex_stt_enabled(settings):
        if duration_seconds and duration_seconds > SYNC_STT_MAX_DURATION_SECONDS:
            logger.info("Skipping sync Yandex STT for long audio: %s sec", duration_seconds)
            return None
        if file_size and file_size > SYNC_STT_MAX_BYTES:
            logger.info("Skipping sync Yandex STT for large audio: %s bytes", file_size)
            return None
        if not is_sync_audio_compatible(file_name=file_name, mime_type=mime_type):
            logger.info("Audio format is not sync-compatible for Yandex STT: %s / %s", file_name, mime_type)
            return None
        return await transcribe_voice_yandex(settings, audio_data)

    if settings.llm_provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.llm_api_key)
        try:
            audio_file = io.BytesIO(audio_data)
            audio_file.name = file_name or "audio.ogg"
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
            return transcript.text
        except Exception as e:
            logger.exception("OpenAI audio transcription failed: %s", e)
            return None

    return None
