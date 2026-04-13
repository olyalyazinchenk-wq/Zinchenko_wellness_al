from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ai_drafting import generate_case_draft, generate_live_reply
from config import load_settings
from storage import (
    build_submission_id,
    case_upload_dir,
    list_recent_cases,
    save_draft,
    save_submission,
    sanitize_filename,
)
from texts import (
    ABOUT_TEXT,
    CONSENT_DECLINED_TEXT,
    CONSENT_TEXT,
    FINAL_MESSAGE,
    LABS_GUIDANCE_TEXT,
    RESET_TEXT,
    START_TEXT,
    TIER_PREMIUM_DESC,
    TIER_SPORT_DESC,
    TIER_SOCIAL_DESC,
    UNKNOWN_STATE_TEXT,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("wellness_bot")

settings = load_settings()

if not settings.bot_token:
    raise RuntimeError(
        "BOT_TOKEN is not configured. Copy .env.example to .env and set BOT_TOKEN."
    )

bot_session = AiohttpSession(proxy=settings.bot_proxy_url) if settings.bot_proxy_url else None
bot = Bot(token=settings.bot_token, session=bot_session)
dp = Dispatcher()

SKIP_WORDS = {"пропустить", "скип", "skip", "нет", "не знаю"}
user_sessions: dict[int, dict[str, Any]] = {}
chat_sessions: dict[int, list[dict[str, str]]] = {}
MAX_CHAT_HISTORY = 12


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 Premium Wellness", callback_data="tier_premium")],
            [InlineKeyboardButton(text="💪 Sport PRO", callback_data="tier_sport")],
            [InlineKeyboardButton(text="🌿 Здоровье 50+", callback_data="tier_social")],
            [InlineKeyboardButton(text="ℹ️ Как это работает", callback_data="show_process")],
        ]
    )


def consent_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Согласен(на), продолжаем", callback_data="consent_yes")],
            [InlineKeyboardButton(text="Не согласен(на)", callback_data="consent_no")],
        ]
    )


def labs_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Готово, перейти дальше", callback_data="labs_done")],
            [InlineKeyboardButton(text="Пропустить анализы", callback_data="skip_labs")],
        ]
    )


TIER_NAMES = {
    "premium": "Premium Wellness",
    "sport": "Sport PRO",
    "social": "Здоровье 50+",
}


def start_session(user: types.User, tier: str = "premium") -> dict[str, Any]:
    submission_id = build_submission_id(user.id)
    session = {
        "submission_id": submission_id,
        "offer": tier,
        "tier": tier,
        "step": "consent",
        "telegram_user_id": user.id,
        "telegram_username": user.username,
        "telegram_full_name": user.full_name,
        "documents": [],
        "lab_notes": "",
    }
    user_sessions[user.id] = session
    return session


def clear_session(user_id: int) -> None:
    user_sessions.pop(user_id, None)


def get_session(user_id: int) -> dict[str, Any] | None:
    return user_sessions.get(user_id)


def reset_chat_session(user_id: int) -> None:
    chat_sessions.pop(user_id, None)


def append_chat_message(user_id: int, role: str, content: str) -> list[dict[str, str]]:
    history = chat_sessions.setdefault(user_id, [])
    history.append({"role": role, "content": content})
    if len(history) > MAX_CHAT_HISTORY:
        chat_sessions[user_id] = history[-MAX_CHAT_HISTORY:]
    return chat_sessions[user_id]


def get_chat_history(user_id: int) -> list[dict[str, str]]:
    return chat_sessions.get(user_id, [])


async def send_step_prompt(chat_id: int, step: str) -> None:
    prompts = {
        "full_name": "Шаг 1/7. Как к вам обращаться? Напишите имя и фамилию.",
        "age": "Шаг 2/7. Сколько вам полных лет?",
        "city": "Шаг 3/7. Из какого вы города и часового пояса?",
        "symptoms": "Шаг 4/7. Какие 3-5 симптомов сейчас беспокоят сильнее всего?",
        "goals": "Шаг 5/7. Какой результат вы хотите получить от разбора в ближайшие 4-8 недель?",
        "background": "Шаг 6/7. Какие диагнозы, лекарства, БАДы или важные ограничения уже есть?",
        "red_flags": (
            "Шаг 7/7. Есть ли сейчас красные флаги: острая боль в груди, потеря сознания, кровь в стуле, "
            "температура несколько дней подряд, беременность с осложнениями или другое состояние, "
            "где нужна срочная очная помощь? Ответьте коротко: `да` или `нет`, и если нужно - уточните."
        ),
        "labs": LABS_GUIDANCE_TEXT,
        "contact": "Финальный шаг. Как лучше связаться с вами после разбора: Telegram, телефон или email?",
    }

    reply_markup = labs_keyboard() if step == "labs" else None
    await bot.send_message(chat_id, prompts[step], reply_markup=reply_markup)


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_chat_ids


def build_submission_payload(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "submission_id": session["submission_id"],
        "offer": session["offer"],
        "profile": {
            "telegram_user_id": session["telegram_user_id"],
            "telegram_username": session.get("telegram_username"),
            "telegram_full_name": session.get("telegram_full_name"),
            "full_name": session.get("full_name"),
            "age": session.get("age"),
            "city": session.get("city"),
            "contact": session.get("contact"),
        },
        "medical_context": {
            "symptoms": session.get("symptoms"),
            "goal": session.get("goals"),
            "background": session.get("background"),
            "red_flags": session.get("red_flags"),
            "lab_notes": session.get("lab_notes"),
        },
        "documents": session.get("documents", []),
        "intake_status": "submitted",
        "consent_given": session.get("consent_given", False),
    }


async def notify_admins(submission: dict[str, Any], draft_text: str | None) -> None:
    if not settings.admin_chat_ids:
        return

    summary_lines = [
        "Новая intake-заявка",
        f"ID: {submission['submission_id']}",
        f"Клиент: {submission['profile'].get('full_name') or submission['profile'].get('telegram_full_name')}",
        f"Город: {submission['profile'].get('city')}",
        f"Симптомы: {submission['medical_context'].get('symptoms')}",
        f"Цель: {submission['medical_context'].get('goal')}",
        f"Документов: {len(submission.get('documents', []))}",
        f"Красные флаги: {submission['medical_context'].get('red_flags')}",
    ]

    if draft_text:
        draft_preview = draft_text.strip().replace("\n", " ")
        summary_lines.append("")
        summary_lines.append("AI draft:")
        summary_lines.append(draft_preview[:1200])

    message_text = "\n".join(summary_lines)
    for admin_chat_id in settings.admin_chat_ids:
        try:
            await bot.send_message(admin_chat_id, message_text)
        except Exception:
            logger.exception("Failed to notify admin chat %s", admin_chat_id)


async def finalize_submission(message: types.Message, session: dict[str, Any]) -> None:
    submission = build_submission_payload(session)
    submission_path = save_submission(settings.submissions_dir, session["submission_id"], submission)

    draft_text: str | None = None
    tier = submission.get("offer") or session.get("tier")
    if settings.llm_provider != "disabled" and settings.llm_api_key and settings.llm_model:
        try:
            draft_text = await asyncio.to_thread(generate_case_draft, settings, submission, tier=tier)
        except Exception:
            logger.exception("AI drafting failed for %s", session["submission_id"])

    if draft_text:
        draft_path = save_draft(settings.drafts_dir, session["submission_id"], draft_text)
        submission["draft_path"] = str(draft_path)
        save_submission(settings.submissions_dir, session["submission_id"], submission)

    logger.info("Saved submission %s to %s", session["submission_id"], submission_path)
    await notify_admins(submission, draft_text)
    clear_session(message.from_user.id)
    await message.answer(
        "Спасибо. Intake сохранен под номером "
        f"`{session['submission_id']}`.\n\n"
        "Следующий шаг: команда увидит заявку, соберет внутренний черновик и продолжит общение с вами здесь, в этом Telegram-чате.\n\n"
        "Если нужно начать заново, используйте /reset."
    )


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    clear_session(message.from_user.id)
    reset_chat_session(message.from_user.id)
    await message.answer(START_TEXT, reply_markup=start_keyboard())


@dp.message(Command("reset"))
async def cmd_reset(message: types.Message) -> None:
    clear_session(message.from_user.id)
    reset_chat_session(message.from_user.id)
    await message.answer(RESET_TEXT, reply_markup=start_keyboard())


@dp.message(Command("chat"))
async def cmd_chat(message: types.Message) -> None:
    clear_session(message.from_user.id)
    reset_chat_session(message.from_user.id)
    await message.answer(
        "Режим живого диалога включен. Пишите вопрос обычным сообщением, я отвечу как AI-ассистент."
    )


@dp.message(Command("chat_reset"))
async def cmd_chat_reset(message: types.Message) -> None:
    reset_chat_session(message.from_user.id)
    await message.answer("Контекст живого диалога очищен.")


@dp.message(Command("queue"))
async def cmd_queue(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    recent_cases = list_recent_cases(settings.submissions_dir, limit=5)
    if not recent_cases:
        await message.answer("Очередь пока пустая.")
        return

    lines = ["Последние кейсы:"]
    for case in recent_cases:
        profile = case.get("profile", {})
        medical = case.get("medical_context", {})
        lines.append(
            f"- {case.get('submission_id')}: "
            f"{profile.get('full_name') or profile.get('telegram_full_name')} | "
            f"{medical.get('symptoms')}"
        )
    await message.answer("\n".join(lines))


@dp.message(Command("health"))
async def cmd_health(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    submission_count = len(list(settings.submissions_dir.glob("*.json")))
    draft_count = len(list(settings.drafts_dir.glob("*.md")))
    upload_case_count = len([path for path in settings.uploads_dir.glob("*") if path.is_dir()])
    lines = [
        "Bot runtime health:",
        f"- Proxy: {settings.bot_proxy_url or 'disabled'}",
        f"- LLM provider: {settings.llm_provider}",
        f"- LLM mode: {settings.llm_api_mode}",
        f"- Submissions: {submission_count}",
        f"- Drafts: {draft_count}",
        f"- Upload folders: {upload_case_count}",
    ]
    await message.answer("\n".join(lines))


@dp.message(Command("llmprobe"))
async def cmd_llmprobe(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    if settings.llm_provider == "disabled":
        await message.answer(
            "LLM сейчас отключён. Когда будет готов российский ключ, заполни `LLM_*` поля в .env и повтори /llmprobe."
        )
        return

    synthetic_submission = {
        "submission_id": "probe_case",
        "offer": "premium_wellness_dossier",
        "profile": {
            "telegram_user_id": 0,
            "telegram_username": "probe",
            "telegram_full_name": "Probe User",
            "full_name": "Пробный кейс",
            "age": 34,
            "city": "Москва",
            "contact": "telegram",
        },
        "medical_context": {
            "symptoms": "усталость, вздутие, плохой сон",
            "goal": "понять, в какую сторону дальше копать",
            "background": "без критичных диагнозов, есть высокий стресс",
            "red_flags": "нет",
            "lab_notes": "ферритин низкий по словам клиента, точных значений пока нет",
        },
        "documents": [],
        "intake_status": "submitted",
        "consent_given": True,
    }

    try:
        draft_text = await asyncio.to_thread(generate_case_draft, settings, synthetic_submission)
    except Exception as exc:
        logger.exception("LLM probe failed")
        await message.answer(f"LLM probe failed: {type(exc).__name__}: {exc}")
        return

    if not draft_text:
        await message.answer("LLM вызов завершился без текста. Проверь модель, ключ и endpoint.")
        return

    await message.answer(
        "LLM probe successful.\n\n"
        f"Provider: {settings.llm_provider}\n"
        f"Mode: {settings.llm_api_mode}\n"
        f"Model: {settings.llm_model}\n\n"
        f"{draft_text[:2500]}"
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("tier_"))
async def process_tier_selection(callback_query: types.CallbackQuery) -> None:
    tier = callback_query.data.replace("tier_", "")
    reset_chat_session(callback_query.from_user.id)
    start_session(callback_query.from_user, tier=tier)

    tier_descs = {"premium": TIER_PREMIUM_DESC, "sport": TIER_SPORT_DESC, "social": TIER_SOCIAL_DESC}
    desc = tier_descs.get(tier, "")
    await bot.send_message(callback_query.from_user.id, desc)
    await bot.send_message(callback_query.from_user.id, CONSENT_TEXT, reply_markup=consent_keyboard())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "show_process")
async def process_show_process(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, ABOUT_TEXT)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "start_live_chat")
async def process_start_live_chat(callback_query: types.CallbackQuery) -> None:
    clear_session(callback_query.from_user.id)
    reset_chat_session(callback_query.from_user.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Режим живого диалога включен. Напишите сообщение, и я отвечу.",
    )
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "consent_yes")
async def process_consent_yes(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id) or start_session(callback_query.from_user)
    session["consent_given"] = True
    session["step"] = "full_name"
    await bot.send_message(callback_query.from_user.id, "Спасибо. Согласие зафиксировано.")
    await send_step_prompt(callback_query.from_user.id, session["step"])
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "consent_no")
async def process_consent_no(callback_query: types.CallbackQuery) -> None:
    clear_session(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, CONSENT_DECLINED_TEXT, reply_markup=start_keyboard())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "skip_labs")
async def process_skip_labs(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id)
    if not session or session.get("step") != "labs":
        await bot.answer_callback_query(callback_query.id, text="Сначала начните intake заново через /start", show_alert=True)
        return

    session["lab_notes"] = session.get("lab_notes") or "Клиент пропустил загрузку анализов на этом этапе."
    session["contact"] = "telegram_current_chat"
    session["step"] = "done"
    await finalize_submission(callback_query.message, session)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "labs_done")
async def process_labs_done(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id)
    if not session or session.get("step") != "labs":
        await bot.answer_callback_query(callback_query.id, text="Сначала начните intake заново через /start", show_alert=True)
        return

    session["contact"] = "telegram_current_chat"
    session["step"] = "done"
    await finalize_submission(callback_query.message, session)
    await bot.answer_callback_query(callback_query.id)


@dp.message(lambda message: message.document is not None)
async def handle_document_upload(message: types.Message) -> None:
    session = get_session(message.from_user.id)
    if not session or session.get("step") != "labs":
        await message.answer(UNKNOWN_STATE_TEXT)
        return

    upload_dir = case_upload_dir(settings.uploads_dir, session["submission_id"])
    original_name = message.document.file_name or "lab_document.pdf"
    file_name = sanitize_filename(original_name)
    destination = upload_dir / file_name

    await bot.download(message.document, destination=destination)
    session["documents"].append(
        {
            "kind": "document",
            "telegram_file_id": message.document.file_id,
            "file_name": original_name,
            "stored_path": str(destination),
            "mime_type": message.document.mime_type,
        }
    )
    await message.answer(
        "Файл сохранён. Если есть ещё документы, отправьте их сейчас. Когда закончите, нажмите кнопку ниже.",
        reply_markup=labs_keyboard(),
    )


@dp.message(lambda message: bool(message.photo))
async def handle_photo_upload(message: types.Message) -> None:
    session = get_session(message.from_user.id)
    if not session or session.get("step") != "labs":
        await message.answer(UNKNOWN_STATE_TEXT)
        return

    upload_dir = case_upload_dir(settings.uploads_dir, session["submission_id"])
    file_name = sanitize_filename(f"lab_photo_{len(session['documents']) + 1}.jpg")
    destination = upload_dir / file_name

    await bot.download(message.photo[-1], destination=destination)
    session["documents"].append(
        {
            "kind": "photo",
            "telegram_file_id": message.photo[-1].file_id,
            "file_name": file_name,
            "stored_path": str(destination),
        }
    )
    await message.answer(
        "Фото сохранено. Можно отправить ещё фото или PDF, либо нажать кнопку для продолжения.",
        reply_markup=labs_keyboard(),
    )


@dp.message()
async def handle_message(message: types.Message) -> None:
    if not message.text:
        await message.answer("Для этого шага лучше отправить текстовый ответ.")
        return

    if message.text.startswith("/"):
        return

    session = get_session(message.from_user.id)
    text = message.text.strip()

    if not session:
        if settings.llm_provider == "disabled" or not settings.llm_api_key or not settings.llm_model:
            await message.answer(UNKNOWN_STATE_TEXT, reply_markup=start_keyboard())
            return

        try:
            await bot.send_chat_action(message.chat.id, "typing")
            history = get_chat_history(message.from_user.id)
            reply = await asyncio.to_thread(generate_live_reply, settings, history, text)
        except Exception:
            logger.exception("Live chat response failed for user %s", message.from_user.id)
            await message.answer(
                "Сейчас не удалось получить ответ от AI. Попробуйте еще раз через минуту."
            )
            return

        if not reply:
            await message.answer(
                "Я не смог сформировать ответ. Попробуйте переформулировать запрос или начните intake через /start."
            )
            return

        append_chat_message(message.from_user.id, "user", text)
        append_chat_message(message.from_user.id, "assistant", reply)
        await message.answer(reply[:3800])
        return

    step = session.get("step")

    if step == "full_name":
        session["full_name"] = text
        session["step"] = "age"
        await send_step_prompt(message.chat.id, "age")
        return

    if step == "age":
        if not text.isdigit():
            await message.answer("Возраст лучше указать числом, например: 34")
            return
        session["age"] = int(text)
        session["step"] = "city"
        await send_step_prompt(message.chat.id, "city")
        return

    if step == "city":
        session["city"] = text
        session["step"] = "symptoms"
        await send_step_prompt(message.chat.id, "symptoms")
        return

    if step == "symptoms":
        session["symptoms"] = text
        session["step"] = "goals"
        await send_step_prompt(message.chat.id, "goals")
        return

    if step == "goals":
        session["goals"] = text
        session["step"] = "background"
        await send_step_prompt(message.chat.id, "background")
        return

    if step == "background":
        session["background"] = text
        session["step"] = "red_flags"
        await send_step_prompt(message.chat.id, "red_flags")
        return

    if step == "red_flags":
        session["red_flags"] = text
        if text.lower().startswith("да"):
            await message.answer(
                "Спасибо. Такой ответ помечу как красный флаг. Это не экстренный чат, поэтому при ухудшении состояния "
                "нужна очная медицинская помощь. Intake можно продолжить, чтобы команда увидела контекст."
            )
        session["step"] = "labs"
        await send_step_prompt(message.chat.id, "labs")
        return

    if step == "labs":
        if text.lower() in SKIP_WORDS:
            session["lab_notes"] = "Клиент пропустил загрузку анализов на этом этапе."
            session["contact"] = "telegram_current_chat"
            session["step"] = "done"
            await finalize_submission(message, session)
            return

        session["lab_notes"] = text
        session["contact"] = "telegram_current_chat"
        session["step"] = "done"
        await message.answer(
            "Принято. Я сохранил текстовое описание анализов. Если захотите, позже можно дослать PDF или фото прямо в диалог."
        )
        await finalize_submission(message, session)
        return

    if step == "contact":
        session["contact"] = text
        await finalize_submission(message, session)
        return

    await message.answer(UNKNOWN_STATE_TEXT, reply_markup=start_keyboard())


async def main() -> None:
    logger.info("Starting Wellness Bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
