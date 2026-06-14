from __future__ import annotations

import asyncio
import logging
import json
import os
import re
import secrets
import socket
from pathlib import Path
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from urllib.parse import urlsplit
from typing import Any

from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    PreCheckoutQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

from ai_drafting import (
    generate_case_draft,
    generate_case_growth_report,
    generate_case_judge_report,
    generate_live_reply,
    generate_screening_reply,
)
from case_service import (
    build_initial_submission_payload,
    build_session_from_submission,
    build_submission_payload,
    persist_submission_enrichment,
    save_submission_state,
    update_submission_status,
)
from config import load_settings
from html_pdf_engine import create_premium_pdf
from lab_ocr import (
    build_biomarker_confirmation_message,
    build_lab_resubmission_message,
    parse_biomarkers,
    recognize_text,
)
from payment_flow import (
    PAYMENT_STATUS_MANUAL_PENDING,
    PREMIUM_PRICE_KOPECKS,
    PREMIUM_PRICE_RUB,
    build_payment_context,
    is_payment_confirmed_for_dossier,
    mark_manual_payment_confirmed,
    mark_manual_payment_pending,
    parse_invoice_payload,
    validate_payment_event,
)
from governance_service import (
    GOVERNANCE_EXPERIMENT_STATUSES,
    aggregate_product_insight_counts,
    apply_suggested_decision,
    build_admin_digest_text,
    build_growth_governance_context,
    format_action_priority_brief,
    format_decisions_dashboard,
    format_execution_gaps,
    format_experiment_outcome_memory,
    format_experiments_dashboard,
    format_governance_summary,
    format_product_insights_summary,
    format_review_dashboard,
    format_suggested_decisions,
    format_windowed_product_summary,
    get_decision_execution_gaps,
    governance_title_similarity,
    is_weekly_digest_due,
    mark_weekly_digest_sent,
    parse_decision_plan_command,
    record_product_decision,
    sync_governance_experiments_from_insights,
    update_decision_execution,
    update_experiment_status,
    update_product_insights_memory,
)
from storage import (
    build_submission_id,
    case_upload_dir,
    load_product_governance,
    load_product_insights,
    list_recent_cases,
    load_runtime_state,
    save_draft,
    save_growth_report,
    save_product_governance,
    save_product_insights,
    save_review_report,
    save_runtime_state,
    save_submission,
    sanitize_filename,
    load_submission,
)

from texts import (
    ABOUT_TEXT,
    CONSENT_DECLINED_TEXT,
    CONSENT_TEXT,
    FINAL_MESSAGE,
    LABS_GUIDANCE_TEXT,
    MANUAL_HANDOFF_REVIEW_TEXT,
    MANUAL_HANDOFF_START_TEXT,
    MANUAL_HANDOFF_INSTANT_START_TEXT,
    OPERATOR_HELP_TEXT,
    PRODUCT_EXAMPLES_TEXT,
    PRODUCT_MENU_TEXT,
    RESET_TEXT,
    START_TEXT,
    TIER_DESCRIPTIONS,
    TIER_BASIC_DESC,
    UNKNOWN_STATE_TEXT,
    RED_FLAGS_INFO_TEXT,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("wellness_bot")


def _format_proxy_for_logs(proxy_url: str) -> str:
    """Return a safe proxy string for logs (no credentials)."""
    try:
        proxy_to_parse = proxy_url if "://" in proxy_url else f"http://{proxy_url}"
        parts = urlsplit(proxy_to_parse)
        if not parts.hostname:
            return "<invalid>"
        scheme_prefix = f"{parts.scheme}://" if "://" in proxy_url and parts.scheme else ""
        port_part = f":{parts.port}" if parts.port else ""
        return f"{scheme_prefix}{parts.hostname}{port_part}"
    except Exception:
        return "<invalid>"


def _extract_proxy_host_port(proxy_url: str) -> tuple[str, int] | None:
    try:
        proxy_to_parse = proxy_url if "://" in proxy_url else f"http://{proxy_url}"
        parts = urlsplit(proxy_to_parse)
        if not parts.hostname:
            return None
        if parts.port:
            port = int(parts.port)
        else:
            scheme = (parts.scheme or "").lower()
            if scheme in {"https"}:
                port = 443
            elif scheme in {"socks5", "socks5h", "socks4", "socks4a"}:
                port = 1080
            else:
                port = 80
        return parts.hostname, port
    except Exception:
        return None


def _test_proxy_connectivity(proxy_url: str, timeout: float = 3.0) -> bool:
    """Quick TCP check if the proxy host:port is reachable."""
    target = _extract_proxy_host_port(proxy_url)
    if not target:
        return False
    try:
        sock = socket.create_connection(target, timeout=timeout)
        sock.close()
        return True
    except (OSError, socket.error):
        return False


def _create_bot_session(proxy_url: str | None) -> AiohttpSession | None:
    """Create an AiohttpSession with optional proxy and connectivity check."""
    if not proxy_url:
        return None
    if not _test_proxy_connectivity(proxy_url):
        logger.warning(
            "Proxy connectivity check failed — falling back to direct connection.",
        )
        return None
    logger.info("Using proxy: %s", _format_proxy_for_logs(proxy_url))
    return AiohttpSession(proxy=proxy_url)


settings = load_settings()

if not settings.bot_token:
    raise RuntimeError(
        "BOT_TOKEN is not configured. Copy .env.example to .env and set BOT_TOKEN."
    )

logger.info(
    "Bot config: proxy=%s, llm_provider=%s, llm_model=%s",
    _format_proxy_for_logs(settings.bot_proxy_url) if settings.bot_proxy_url else "disabled",
    settings.llm_provider,
    settings.llm_model,
)

bot_session = _create_bot_session(settings.bot_proxy_url)
bot = Bot(token=settings.bot_token, session=bot_session)
dp = Dispatcher()

SKIP_WORDS = {"пропустить", "скип", "skip", "нет", "не знаю"}
PREMIUM_TRIGGER_MARKERS = (
    "хочу разбор",
    "хочу досье",
    "хочу dossier",
    "хочу premium",
    "готова идти дальше",
    "готов идти дальше",
    "запусти разбор",
    "начнем разбор",
    "начнём разбор",
    "хочу начать разбор",
)
user_sessions: dict[int, dict[str, Any]] = {}
chat_sessions: dict[int, list[dict[str, str]]] = {}
MAX_CHAT_HISTORY = 12
TELEGRAM_CAPTION_SAFE_LIMIT = 900
TELEGRAM_MESSAGE_SAFE_LIMIT = 3500
ACTIVE_TMA_PORT = int(os.getenv("TMA_PORT", "8000"))
MOSCOW_TZ = timezone(timedelta(hours=3))
PRODUCT_INSIGHT_SECTION_LABELS = [
    ("market_value_risks", "Риски ценности"),
    ("demand_risks", "Риски спроса"),
    ("value_gaps", "Провалы ценности"),
    ("positioning_upgrades", "Усиление позиционирования"),
    ("conversion_ideas", "Идеи конверсии"),
    ("retention_ideas", "Идеи удержания"),
    ("referral_ideas", "Идеи рекомендаций"),
    ("next_experiments", "Следующие эксперименты"),
]


def utc_now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def persist_runtime_state() -> None:
    save_runtime_state(settings.runtime_state_path, user_sessions, chat_sessions)


def restore_runtime_state() -> None:
    payload = load_runtime_state(settings.runtime_state_path)
    restored_user_sessions = payload.get("user_sessions", {})
    restored_chat_sessions = payload.get("chat_sessions", {})

    user_sessions.clear()
    for user_id, session in restored_user_sessions.items():
        try:
            user_sessions[int(user_id)] = session
        except (TypeError, ValueError):
            continue

    chat_sessions.clear()
    for user_id, history in restored_chat_sessions.items():
        try:
            chat_sessions[int(user_id)] = history
        except (TypeError, ValueError):
            continue


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍽️ Экспресс-аудит «Моя тарелка» — 1 490 ₽", callback_data="tier_nutri_chat")],
            [InlineKeyboardButton(text="🥗 Умный куратор (Сопровождение) — 14 900 ₽", callback_data="tier_habits")],
            [InlineKeyboardButton(text="📋 Дефицит-чек / Карта симптомов — 3 900 ₽", callback_data="tier_standard")],
            [InlineKeyboardButton(text="👑 Wellness-Паспорт с анализами — 14 900 ₽", callback_data="tier_premium")],
            [InlineKeyboardButton(text="🧬 Разбор ХМС по Осипову — 5 900 ₽", callback_data="tier_osipov")],
            [InlineKeyboardButton(text="🧪 Сдать анализы", callback_data="show_labs_link"),
             InlineKeyboardButton(text="💼 Мои тарифы", callback_data="choose_product")],
        ]
    )


def product_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍽️ Экспресс-аудит «Моя тарелка» — 1 490 ₽", callback_data="tier_nutri_chat")],
            [InlineKeyboardButton(text="🥗 Умный куратор (Сопровождение) — 14 900 ₽", callback_data="tier_habits")],
            [InlineKeyboardButton(text="📋 Дефицит-чек / Карта симптомов — 3 900 ₽", callback_data="tier_standard")],
            [InlineKeyboardButton(text="👑 Wellness-Паспорт с анализами — 14 900 ₽", callback_data="tier_premium")],
            [InlineKeyboardButton(text="🧬 Разбор ХМС по Осипову — 5 900 ₽", callback_data="tier_osipov")],
            [InlineKeyboardButton(text="Посмотреть пример результата", callback_data="show_examples")],
        ]
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Диагностика симптомов (Бесплатно)")],
            [KeyboardButton(text="🛍️ Выбрать программу"), KeyboardButton(text="📊 Мои отчеты")],
            [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="🩸 Сдать анализы")],
            [KeyboardButton(text="💬 Задать вопрос эксперту"), KeyboardButton(text="🚨 Красные флаги")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
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
            [InlineKeyboardButton(text="Ввести показатели вручную", callback_data="manual_labs_help")],
            [InlineKeyboardButton(text="Готово, перейти дальше", callback_data="labs_done")],
            [InlineKeyboardButton(text="Пропустить анализы", callback_data="skip_labs")],
        ]
    )


TIER_NAMES = {
    "nutri_chat": "Экспресс-аудит «Моя тарелка»",
    "habits": "Умный куратор: Сопровождение",
    "standard": "Дефицит-чек / Карта симптомов",
    "premium": "Персональный Wellness-Паспорт",
    "osipov": "Код Микробиома: ХМС по Осипову",
    "screening": "Экспресс-аудит «Моя тарелка»",
    "basic": "Дефицит-чек / Карта симптомов",
    "full": "Персональный Wellness-Паспорт",
}

INTAKE_STEP_ORDER = [
    "full_name",           # 1. Имя, возраст, город
    "anthropometrics",     # 2. Рост и вес
    "symptoms",            # 3. Главные жалобы
    "goals",               # 4. Цель разбора
    "nutrition_routine",   # 5. Режим питания
    "nutrition",           # 6. Рацион за день
    "food_behavior",       # 7. Пищевое поведение
    "digestion",           # 8. ЖКТ, стул, желчеотток
    "water_alcohol",       # 9. Вода, кофе, алкоголь
    "sleep_stress",        # 10. Сон, стресс, энергия
    "work_lifestyle",      # 11. Работа, активность, нагрузки
    "background",          # 12. Диагнозы, препараты, БАДы
    "female_hormones",     # 13. Гормональный/репродуктивный фон
    "lab_notes",           # 14. Анализы и обследования
    "red_flags",           # 15. Красные флаги
]
OPTIONAL_INTAKE_STEPS = {
    "anthropometrics",
    "female_hormones",
    "lab_notes",
}
NAV_BACK_WORDS = {
    "назад",
    "шаг назад",
    "вернуться назад",
    "предыдущий",
    "предыдущий вопрос",
    "к предыдущему",
}
NAV_NEXT_WORDS = {
    "вперед",
    "вперёд",
    "шаг вперед",
    "шаг вперёд",
    "дальше",
    "готово",
    "готово дальше",
    "можно дальше",
    "идем дальше",
    "идём дальше",
    "продолжить",
    "продолжай",
    "следующий",
    "следующий вопрос",
    "перейти дальше",
}
NAV_REPEAT_WORDS = {
    "повтори",
    "повторить",
    "повтори вопрос",
    "повторить вопрос",
    "текущий вопрос",
    "где мы",
}


def start_session(user: types.User, tier: str = "basic") -> dict[str, Any]:
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
    save_submission_state(
        settings.submissions_dir,
        build_initial_submission_payload(session, now_iso=utc_now_iso()),
    )
    persist_runtime_state()
    return session


def clear_session(user_id: int) -> None:
    user_sessions.pop(user_id, None)
    persist_runtime_state()


def get_session(user_id: int) -> dict[str, Any] | None:
    return user_sessions.get(user_id)


def touch_session() -> None:
    persist_runtime_state()


def normalize_nav_text(text: str) -> str:
    return " ".join(str(text).lower().replace("ё", "е").strip().split())


def intake_next_step(step: str) -> str | None:
    if step not in INTAKE_STEP_ORDER:
        return None
    index = INTAKE_STEP_ORDER.index(step)
    if index >= len(INTAKE_STEP_ORDER) - 1:
        return None
    return INTAKE_STEP_ORDER[index + 1]


def intake_previous_step(step: str) -> str | None:
    if step not in INTAKE_STEP_ORDER:
        return None
    index = INTAKE_STEP_ORDER.index(step)
    if index <= 0:
        return None
    return INTAKE_STEP_ORDER[index - 1]


def step_has_answer(session: dict[str, Any], step: str) -> bool:
    if step == "lab_notes":
        return bool(
            session.get("lab_notes")
            or session.get("documents")
            or session.get("parsed_biomarkers")
            or session.get("pending_biomarker_confirmation")
        )
    value = session.get(step)
    return value is not None and str(value).strip() != ""


async def handle_intake_navigation(message: types.Message, session: dict[str, Any], text: str) -> bool:
    step = str(session.get("step") or "")
    if step not in INTAKE_STEP_ORDER:
        return False

    normalized = normalize_nav_text(text)

    if normalized in NAV_REPEAT_WORDS:
        await message.answer("Повторяю текущий шаг.")
        await send_step_prompt(message.chat.id, step)
        return True

    if normalized in NAV_BACK_WORDS:
        previous_step = intake_previous_step(step)
        if not previous_step:
            await message.answer(
                "Вы уже на первом шаге. Ответьте на текущий вопрос или напишите /reset, чтобы начать заново."
            )
            await send_step_prompt(message.chat.id, step)
            return True
        session["step"] = previous_step
        touch_session()
        await message.answer("Возвращаю на предыдущий шаг. Новый ответ заменит прежний.")
        await send_step_prompt(message.chat.id, previous_step)
        return True

    if normalized in SKIP_WORDS and step not in {"lab_notes", "red_flags"}:
        session[step] = "Клиент пропустил шаг."
        next_step = intake_next_step(step)
        if not next_step:
            session["step"] = "lab_notes"
            next_step = "lab_notes"
        else:
            session["step"] = next_step
        touch_session()
        await message.answer("Пропускаю этот шаг и иду дальше.")
        await send_step_prompt(message.chat.id, next_step)
        return True

    if normalized in NAV_NEXT_WORDS:
        next_step = intake_next_step(step)
        if not next_step:
            await message.answer(
                "Это последний шаг анкеты. Если анализов нет, напишите `пропустить`; если есть — пришлите файл или показатели текстом."
            )
            await send_step_prompt(message.chat.id, step)
            return True
        if not step_has_answer(session, step):
            if step in OPTIONAL_INTAKE_STEPS:
                session[step] = "Клиент пропустил шаг."
            else:
                await message.answer(
                    "Поняла, что вы хотите дальше. Но по этому шагу еще нет ответа. "
                    "Напишите ответ коротко или `пропустить`, если вопрос неактуален."
                )
                await send_step_prompt(message.chat.id, step)
                return True
        session["step"] = next_step
        touch_session()
        await message.answer("Перехожу к следующему шагу.")
        await send_step_prompt(message.chat.id, next_step)
        return True

    return False


def reset_chat_session(user_id: int) -> None:
    chat_sessions.pop(user_id, None)
    persist_runtime_state()


def append_chat_message(user_id: int, role: str, content: str) -> list[dict[str, str]]:
    history = chat_sessions.setdefault(user_id, [])
    history.append({"role": role, "content": content})
    if len(history) > MAX_CHAT_HISTORY:
        chat_sessions[user_id] = history[-MAX_CHAT_HISTORY:]
    persist_runtime_state()
    return chat_sessions[user_id]


def get_chat_history(user_id: int) -> list[dict[str, str]]:
    return chat_sessions.get(user_id, [])


def wants_premium_intake(text: str) -> bool:
    normalized = " ".join(text.lower().replace("ё", "е").split())
    return any(marker in normalized for marker in PREMIUM_TRIGGER_MARKERS)


def split_telegram_text(text: str, limit: int = TELEGRAM_MESSAGE_SAFE_LIMIT) -> list[str]:
    chunks: list[str] = []
    remaining = text.strip()
    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break
        split_at = remaining.rfind("\n", 0, limit)
        if split_at < max(1, limit // 2):
            split_at = limit
        chunks.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    return chunks or [""]


def build_admin_pdf_caption(submission: dict[str, Any]) -> str:
    profile = submission.get("profile", {})
    caption = (
        "PDF готов для экспертной проверки.\n"
        f"ID: {submission.get('submission_id')}\n"
        f"Клиент: {profile.get('full_name') or profile.get('telegram_full_name')}"
    )
    return caption[:TELEGRAM_CAPTION_SAFE_LIMIT]


def parse_utc_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def find_pending_manual_payment_submission(user_id: int) -> dict[str, Any] | None:
    """Find a case with manual_payment_pending status for the user."""
    for case in list_recent_cases(settings.submissions_dir, limit=50):
        profile = case.get("profile", {})
        case_user_id = case.get("telegram_user_id") or profile.get("telegram_user_id")
        if case_user_id and int(case_user_id) == int(user_id):
            if case.get("intake_status") == "manual_payment_pending":
                return case
    return None


async def check_and_prompt_pending_payment(message: types.Message) -> bool:
    """Check if the user has a pending manual payment, and prompt them to confirm if they send a message."""
    if not message.from_user:
        return False
    pending_sub = find_pending_manual_payment_submission(message.from_user.id)
    if pending_sub:
        submission_id = pending_sub["submission_id"]
        # If client hasn't clicked "Подтвердить оплату" yet:
        if not pending_sub.get("client_reported_payment"):
            client_pay_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="✅ Подтвердить оплату (я оплатил/а)",
                            callback_data=f"clientconfirmpay_{submission_id}",
                        )
                    ]
                ]
            )
            await message.answer(
                "Вы начали оформление программы, но мы пока не получили вашу отметку об оплате.\n\n"
                "Если вы уже провели платеж, пожалуйста, <b>нажмите на кнопку «Подтвердить оплату (я оплатил/а)» ниже</b>, "
                "чтобы кураторы сразу получили уведомление и открыли вам доступ к программе.\n\n"
                "Если у вас возникли трудности с оплатой или вопросы, просто напишите здесь в чат.",
                reply_markup=client_pay_markup,
                parse_mode="HTML"
            )
            return True
        else:
            await message.answer(
                "✅ Отметка об оплате получена! Наша команда уже проверяет платёж. "
                "Как только кураторы подтвердят оплату, мы сразу же начнем работу и бот пришлет уведомление. Пожалуйста, ожидайте."
            )
            return True
    return False


def find_active_followup_case(user_id: int) -> dict[str, Any] | None:
    """Return the latest delivered case inside the 30-day support window."""
    now = datetime.now(timezone.utc)
    for case in list_recent_cases(settings.submissions_dir, limit=30):
        profile = case.get("profile", {})
        if int(profile.get("telegram_user_id") or 0) != int(user_id):
            continue
        if case.get("intake_status") != "delivered_to_client":
            continue
        delivered_at = parse_utc_iso(case.get("delivered_at") or case.get("status_updated_at"))
        if delivered_at and now - delivered_at <= timedelta(days=30):
            return case
    return None


def append_case_followup(case: dict[str, Any], payload: dict[str, Any]) -> None:
    followups = case.get("followups")
    if not isinstance(followups, list):
        followups = []
    followups.append({**payload, "created_at": utc_now_iso()})
    case["followups"] = followups[-100:]
    case["last_followup_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, case)


def build_followup_context(case: dict[str, Any], user_text: str) -> str:
    profile = case.get("profile", {})
    medical = case.get("medical_context", {})
    return json.dumps(
        {
            "mode": "30_day_followup_after_dossier",
            "client": {
                "name": profile.get("full_name") or profile.get("telegram_full_name"),
                "age": profile.get("age"),
                "city": profile.get("city"),
            },
            "case": {
                "submission_id": case.get("submission_id"),
                "symptoms": medical.get("symptoms"),
                "goals": medical.get("goals"),
                "nutrition_routine": medical.get("nutrition_routine"),
                "nutrition": medical.get("nutrition"),
                "food_behavior": medical.get("food_behavior"),
                "digestion": medical.get("digestion"),
                "water_alcohol": medical.get("water_alcohol"),
                "sleep_stress": medical.get("sleep_stress"),
                "work_lifestyle": medical.get("work_lifestyle"),
                "background": medical.get("background"),
                "female_hormones": medical.get("female_hormones"),
                "lab_notes": medical.get("lab_notes"),
                "red_flags": medical.get("red_flags"),
                "requires_lab_resubmission": case.get("requires_lab_resubmission"),
                "lab_quality_check": case.get("lab_quality_check"),
                "lab_confirmation_status": case.get("lab_confirmation_status"),
                "lab_confirmation_needed": case.get("lab_confirmation_needed"),
            },
            "client_message": user_text,
            "rules": [
                "Ответить по-русски, мягко и конкретно.",
                "Не ставить диагноз и не назначать лечение.",
                "Если фото/анализы/выписки/описание сомнительные — попросить уточнение.",
                "Дать 1-3 безопасных следующих шага и указать, когда нужен врач.",
                "Учитывать, что клиент может присылать дополнительные анализы, УЗИ, выписки и вопросы в течение 30 дней после досье.",
                "Если вопрос связан с готовым досье, объяснить как скорректировать план в рамках 30-дневного сопровождения.",
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


async def send_step_prompt(chat_id: int, step: str) -> None:
    prompts = {
        "full_name": (
            "Шаг 1 из 15\n\n"
            "Как к вам обращаться?\n\n"
            "Напишите имя, возраст и город.\n"
            "Пример: Ольга, 32 года, Санкт-Петербург"
        ),
        "anthropometrics": (
            "Шаг 2 из 15\n\n"
            "Укажите рост, текущий вес и желаемый вес.\n"
            "Пример: рост 172, вес 70, хочу 60"
        ),
        "symptoms": (
            "Шаг 3 из 15\n\n"
            "Какие главные жалобы сейчас?\n\n"
            "Выберите кнопку или напишите свои жалобы через запятую.\n"
            "Пример: усталость, вздутие, ломкость волос, тяга к сладкому"
        ),
        "goals": (
            "Шаг 4 из 15\n\n"
            "Какого результата хотите достичь?\n\n"
            "Выберите кнопку или напишите свою цель.\n"
            "Пример: вернуть бодрость к обеду, убрать изжогу, восстановить качество волос"
        ),
        "nutrition_routine": (
            "Шаг 5 из 15\n\n"
            "Какой у вас режим питания?\n\n"
            "Напишите: сколько раз в день едите, примерное время, есть ли перекусы или пропуски.\n"
            "Пример: завтрак 8:00, обед 13:00, ужин 19:00, перекус сладким в 15:00."
        ),
        "nutrition": (
            "Шаг 6 из 15\n\n"
            "Опишите обычный день питания.\n\n"
            "Укажите завтрак, обед, ужин, перекусы и напитки.\n"
            "Пример: завтрак — яйца и овощи; обед — суп и рыба; ужин — салат с курицей."
        ),
        "food_behavior": (
            "Шаг 7 из 15\n\n"
            "Есть ли тяга к сладкому, мучному, переедание или заедание стресса?\n\n"
            "Выберите кнопку или напишите подробнее."
        ),
        "digestion": (
            "Шаг 8 из 15\n\n"
            "Есть ли жалобы по ЖКТ и желчеоттоку?\n\n"
            "Выберите кнопку или напишите свой вариант.\n"
            "Можно указать: вздутие, изжога, тяжесть после жирного, горечь во рту, стул."
        ),
        "water_alcohol": (
            "Шаг 9 из 15\n\n"
            "Сколько воды, кофе, чая и алкоголя в обычный день?\n"
            "Пример: 1,5 л воды, 2 чашки кофе до обеда, алкоголь раз в неделю."
        ),
        "sleep_stress": (
            "Шаг 10 из 15\n\n"
            "Какой у вас сон и уровень стресса?\n\n"
            "Выберите кнопку или напишите: во сколько ложитесь, во сколько встаёте, как спите, какой стресс."
        ),
        "work_lifestyle": (
            "Шаг 11 из 15\n\n"
            "Какая у вас активность и нагрузка на работе?\n"
            "Пример: сидячая работа, около 5000 шагов, спорта нет."
        ),
        "background": (
            "Шаг 12 из 15\n\n"
            "Есть ли диагнозы от врача, операции, лекарства или БАДы?\n\n"
            "Важно указать дозировки, если знаете.\n"
            "Пример: гипотиреоз, L-тироксин 50 мкг, витамин D 2000 МЕ."
        ),
        "female_hormones": (
            "Шаг 13 из 15\n\n"
            "Гормональный и репродуктивный фон.\n\n"
            "Для женщин: цикл, ПМС, либидо.\n"
            "Для мужчин: либидо, простата, самочувствие.\n"
            "Выберите кнопку или напишите свой вариант."
        ),
        "lab_notes": (
            "Шаг 14 из 15\n\n"
            "Есть ли анализы за последние 6 месяцев?\n\n"
            "Можно прикрепить PDF, фото бланка или написать показатели вручную.\n"
            "Пример: ферритин 15, ТТГ 3.4"
        ),
        "red_flags": (
            "Шаг 15 из 15\n\n"
            "Есть ли сейчас острые симптомы?\n\n"
            "Например: сильная боль, кровь, высокая температура, резкое похудение, обмороки, боль в груди.\n"
            "Выберите кнопку или напишите подробнее."
        ),
    }

    reply_markup = None

    # Premium interactive keyboards based on step
    if step == "symptoms":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Усталость, низкий ресурс, ЖКТ"), KeyboardButton(text="Анемия, ломкость волос")],
                [KeyboardButton(text="Вздутие, изжога после еды"), KeyboardButton(text="Отёки, вес, тяга к сладкому")],
                [KeyboardButton(text="Напишу свой вариант"), KeyboardButton(text="Пропустить этот шаг")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "goals":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Восстановить энергию и бодрость"), KeyboardButton(text="Наладить пищеварение и ЖКТ")],
                [KeyboardButton(text="Укрепить волосы и ногти"), KeyboardButton(text="Снизить вес")],
                [KeyboardButton(text="Подобрать питание и добавки"), KeyboardButton(text="Напишу свою цель")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "food_behavior":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Тянет на сладкое"), KeyboardButton(text="Переедаю вечером")],
                [KeyboardButton(text="Заедаю стресс"), KeyboardButton(text="Нет выраженных проблем")],
                [KeyboardButton(text="Напишу подробнее"), KeyboardButton(text="Пропустить")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "digestion":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Вздутие, изжога после жирного"), KeyboardButton(text="Регулярные запоры / тяжесть")],
                [KeyboardButton(text="Горечь во рту / желчеотток"), KeyboardButton(text="Удалён желчный пузырь")],
                [KeyboardButton(text="Всё в норме, жалоб нет"), KeyboardButton(text="Пропустить")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "sleep_stress":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Сон нормальный, стресс умеренный"), KeyboardButton(text="Плохо засыпаю")],
                [KeyboardButton(text="Просыпаюсь ночью"), KeyboardButton(text="Стресс высокий")],
                [KeyboardButton(text="Напишу подробнее"), KeyboardButton(text="Пропустить")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "female_hormones":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Снижено либидо, цикл регулярный"), KeyboardButton(text="Выраженный ПМС, раздражительность")],
                [KeyboardButton(text="Я мужчина, напишу свой вариант"), KeyboardButton(text="Всё в норме, жалоб нет")],
                [KeyboardButton(text="Пропустить")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "lab_notes":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Нет анализов (хочу сдать)"), KeyboardButton(text="Пропустить анализы")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    elif step == "red_flags":
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Нет (острых симптомов нет)")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    else:
        # Restore normal keyboard for typed-only fields to avoid keyboard sticky states
        reply_markup = ReplyKeyboardRemove()

    await bot.send_message(chat_id, prompts[step], reply_markup=reply_markup)


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_chat_ids


def strip_json_code_fences(raw_text: str) -> str:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def load_report_dict(report_text: str | None) -> dict[str, Any]:
    if not report_text:
        return {}
    try:
        payload = json.loads(strip_json_code_fences(report_text))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, dict):
        return [f"{key}: {val}" for key, val in value.items() if str(val).strip()]
    text = str(value).strip()
    if not text:
        return []
    lines = [line.strip(" -•\t") for line in text.replace("\r", "\n").split("\n")]
    return [line for line in lines if line]


import re

EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff]"
    r"|[\u2600-\u27bf]"
    r"|[\u2300-\u23ff]"
    r"|[\u2b50-\u2b55]"
)

def clean_text_basic(val: Any) -> Any:
    if val is None:
        return ""
    if isinstance(val, list):
        return [clean_text_basic(item) for item in val if item]
    if isinstance(val, dict):
        return {key: clean_text_basic(value) for key, value in val.items()}
    
    text = str(val)
    text = EMOJI_REGEX.sub("", text)
    text = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "").replace("`", "")
    text = re.sub(r"^#+\s*", "", text)
    return text.strip()

def clean_list_item(val: Any) -> Any:
    if val is None:
        return ""
    if isinstance(val, list):
        return [clean_list_item(item) for item in val if item]
    if isinstance(val, dict):
        return {key: clean_list_item(value) for key, value in val.items()}
    
    text = str(val)
    text = EMOJI_REGEX.sub("", text)
    text = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "").replace("`", "")
    text = re.sub(r"^#+\s*", "", text)
    text = text.strip()
    # Remove leading bullets, dashes, list numbers (e.g. "1. ", "• ", "- ")
    text = re.sub(r"^(?:[•\-\u2013\u2014\*]|\d+[\.\)]+)\s*", "", text)
    return text.strip()

def clean_pdf_data_symbols(data: dict[str, Any]) -> dict[str, Any]:
    """Clean all emojis, markdown symbols, and duplicate bullets from PDF data fields before rendering."""
    cleaned = {}
    for key, val in data.items():
        if key in {
            "working_hypotheses",
            "support_priorities",
            "diet_strategy",
            "lifestyle",
            "additional_control"
        }:
            cleaned[key] = clean_list_item(val)
        elif key == "schemes":
            clean_schemes = []
            if isinstance(val, list):
                for s in val:
                    if isinstance(s, dict):
                        clean_schemes.append({
                            "time": clean_text_basic(s.get("time", "")),
                            "name": clean_list_item(s.get("name", "")),
                            "comment": clean_text_basic(s.get("comment", ""))
                        })
            cleaned[key] = clean_schemes
        elif key == "executive_summary":
            ex = {}
            if isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    if sub_key in {"headline", "paragraph"}:
                        ex[sub_key] = clean_text_basic(sub_val)
                    else:
                        ex[sub_key] = clean_list_item(sub_val)
            cleaned[key] = ex
        elif key == "three_step_protocol":
            clean_prot = []
            if isinstance(val, list):
                for p in val:
                    if isinstance(p, dict):
                        clean_prot.append({
                            "title": clean_text_basic(p.get("title", "")),
                            "body": clean_text_basic(p.get("body", ""))
                        })
            cleaned[key] = clean_prot
        elif key == "plan_3_days":
            clean_plan = []
            if isinstance(val, list):
                for d in val:
                    if isinstance(d, dict):
                        clean_plan.append({
                            "day": clean_text_basic(d.get("day", "")),
                            "focus": clean_text_basic(d.get("focus", "")),
                            "actions": clean_list_item(d.get("actions", []))
                        })
            cleaned[key] = clean_plan
        elif key == "doctor_questions":
            clean_doc = []
            if isinstance(val, list):
                for d in val:
                    if isinstance(d, dict):
                        clean_doc.append({
                            "specialist": clean_text_basic(d.get("specialist", "")),
                            "questions": clean_list_item(d.get("questions", []))
                        })
            cleaned[key] = clean_doc
        elif key in {"client_profile", "main_request", "final_conclusion", "analysis_confidence", "mini_example"}:
            cleaned[key] = clean_text_basic(val)
        else:
            if isinstance(val, (str, list, dict)):
                cleaned[key] = clean_text_basic(val)
            else:
                cleaned[key] = val
    return cleaned


def get_product_filename_prefix(offer_code: str | None) -> str:
    mapping = {
        "nutri_chat": "Express_Audit_Moya_Tarelka",
        "screening": "Express_Audit_Moya_Tarelka",
        "habits": "Umny_Kurator_Soprovozhdenie",
        "standard": "Deficit_Chek_Karta_Simptomov",
        "basic": "Deficit_Chek_Karta_Simptomov",
        "premium": "Personalny_Wellness_Pasport",
        "full": "Personalny_Wellness_Pasport",
        "osipov": "Kod_Mikrobioma_HMS_Osipov",
    }
    return mapping.get(offer_code, "Wellness_Dossier")


def normalize_dossier_pdf_data(raw_data: dict[str, Any], submission: dict[str, Any] | None = None) -> dict[str, Any]:
    """Map the LLM dossier schema into the HTML PDF template schema."""
    profile = raw_data.get("profile") if isinstance(raw_data.get("profile"), dict) else {}
    strategy = raw_data.get("strategy") if isinstance(raw_data.get("strategy"), dict) else {}

    client_profile_parts = [
        str(profile.get("full_name") or "").strip(),
        f"Возраст: {profile.get('age')}" if profile.get("age") else "",
        f"Город: {profile.get('city')}" if profile.get("city") else "",
        f"Цель: {profile.get('goal')}" if profile.get("goal") else "",
    ]
    client_profile = "\n".join(part for part in client_profile_parts if part)

    diet_strategy = []
    diet_strategy.extend(ensure_list(raw_data.get("diet_strategy")))
    diet_strategy.extend(ensure_list(raw_data.get("diet_habits")))
    diet_strategy.extend(ensure_list(strategy.get("nutrition")))

    lifestyle = []
    lifestyle.extend(ensure_list(raw_data.get("lifestyle")))
    lifestyle.extend(ensure_list(raw_data.get("activity")))
    lifestyle.extend(ensure_list(strategy.get("habits")))

    additional_control = []
    additional_control.extend(ensure_list(raw_data.get("additional_control")))
    additional_control.extend(ensure_list(raw_data.get("warning_signs")))
    additional_control.extend(ensure_list(raw_data.get("gi_status")))
    additional_control.extend(ensure_list(strategy.get("control")))

    offer_code = None
    if submission:
        offer_code = submission.get("offer") or submission.get("tier")
    if not offer_code:
        offer_code = raw_data.get("offer") or raw_data.get("tier")
    
    product_name = TIER_NAMES.get(offer_code, "Wellness-Паспорт")
    
    title_mapping = {
        "nutri_chat": "ЭКСПРЕСС-АУДИТ<br>«МОЯ ТАРЕЛКА»",
        "screening": "ЭКСПРЕСС-АУДИТ<br>«МОЯ ТАРЕЛКА»",
        "habits": "УМНЫЙ КУРАТОР:<br>СОПРОВОЖДЕНИЕ",
        "standard": "ДЕФИЦИТ-ЧЕК /<br>КАРТА СИМПТОМОВ",
        "basic": "ДЕФИЦИТ-ЧЕК /<br>КАРТА СИМПТОМОВ",
        "premium": "ПЕРСОНАЛЬНЫЙ<br>WELLNESS-ПАСПОРТ",
        "full": "ПЕРСОНАЛЬНЫЙ<br>WELLNESS-ПАСПОРТ",
        "osipov": "КОД МИКРОБИОМА:<br>ХМС ПО ОСИПОВУ",
    }
    product_title = title_mapping.get(offer_code, "ПЕРСОНАЛЬНОЕ<br>WELLNESS ДОСЬЕ")

    res = {
        **raw_data,
        "client_profile": raw_data.get("client_profile") or client_profile or "Клиент",
        "main_request": raw_data.get("main_request") or raw_data.get("request") or "",
        "working_hypotheses": ensure_list(raw_data.get("working_hypotheses")) or ensure_list(raw_data.get("hypotheses")),
        "support_priorities": ensure_list(raw_data.get("support_priorities")) or ensure_list(raw_data.get("priorities")) or ensure_list(raw_data.get("findings")),
        "diet_strategy": diet_strategy,
        "lifestyle": lifestyle,
        "additional_control": additional_control,
        "final_conclusion": raw_data.get("final_conclusion") or raw_data.get("expert_conclusion") or "",
        "schemes": raw_data.get("schemes") if isinstance(raw_data.get("schemes"), list) else [],
        "product_name": product_name,
        "product_title": product_title,
    }
    return clean_pdf_data_symbols(res)


def build_premium_value_packaging(pdf_data: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    """Create the premium first-page layer: quick win, 14-day route, and guided follow-up."""
    medical = submission.get("medical_context") or {}
    symptoms = str(medical.get("symptoms") or "").strip()
    sleep_stress = str(medical.get("sleep_stress") or "").strip()
    digestion = str(medical.get("digestion") or "").strip()
    nutrition = str(medical.get("nutrition") or "").strip()
    lab_notes = str(medical.get("lab_notes") or "").lower()
    background = " ".join(
        str(medical.get(key) or "")
        for key in (
            "symptoms",
            "wellbeing_energy",
            "complaint_pattern",
            "work_lifestyle",
            "nutrition",
            "food_behavior",
            "digestion",
            "sleep_stress",
            "activity",
            "female_hormones",
            "emotional_stress",
            "background",
            "risk_details",
            "motivation",
            "red_flags",
            "lab_notes",
        )
    ).lower()
    requires_lab_resubmission = bool(submission.get("requires_lab_resubmission"))
    has_lab_uncertainty_note = any(marker in lab_notes for marker in ("нечет", "нечёт", "подтвержд", "сомн"))
    biomarkers = submission.get("parsed_biomarkers") if isinstance(submission.get("parsed_biomarkers"), list) else []
    lab_confirmation_status = str(submission.get("lab_confirmation_status") or "")
    lab_confirmation_pending = lab_confirmation_status in {"pending_client_confirmation", "client_correction_needed"}
    has_labs = bool(biomarkers) and not requires_lab_resubmission and not lab_confirmation_pending

    def biomarker_map() -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for item in biomarkers:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or item.get("nutrition_marker_key") or "").lower()
            key = str(item.get("nutrition_marker_key") or "").lower()
            joined = f"{name} {key}"
            if "феррит" in joined or "ferritin" in joined:
                result["ferritin"] = item
            elif "витамин d" in joined or "vitamin_d" in joined or "25" in joined:
                result["vitamin_d"] = item
            elif "ттг" in joined or "tsh" in joined:
                result["tsh"] = item
        return result

    def format_marker(item: dict[str, Any] | None) -> str | None:
        if not item:
            return None
        name = str(item.get("name") or "").strip()
        value = str(item.get("value") or "").strip()
        unit = str(item.get("unit") or "").strip()
        optimal = str(item.get("nutrition_optimal_range") or "").strip()
        base = f"{name} {value} {unit}".strip()
        if optimal:
            base += f" при нутрициологическом ориентире {optimal}"
        return base

    markers = biomarker_map()
    ferritin_line = format_marker(markers.get("ferritin"))
    vitamin_d_line = format_marker(markers.get("vitamin_d"))
    tsh_line = format_marker(markers.get("tsh"))
    factual_lines = [line for line in (ferritin_line, vitamin_d_line, tsh_line) if line]
    has_heavy_cycle_signal = any(
        marker in background
        for marker in ("обиль", "кровотеч", "сгуст", "эндометри", "болезненн")
    )

    key_findings = [
        (
            "Ключевой инсайт: при обильном цикле/эндометриозе и низком ферритине нельзя просто «поднять железо» добавками; "
            "сначала важно понять источник кровопотери и щитовидный фон."
            if has_heavy_cycle_signal and ferritin_line
            else "Синтез: усталость, зябкость, выпадение волос, сердцебиение и обильный цикл требуют сначала проверить связку "
            "железо/щитовидный фон/кровопотеря/восстановление, а не начинать добавки вслепую."
        )
        if symptoms
        else "Синтез: сначала собираем симптомы, питание, сон, анализы и фон в одну понятную карту, затем выбираем 1-2 приоритета.",
        ("Предварительно считанные показатели: " + "; ".join(factual_lines[:3]) + ". Их нужно сверить с качественным PDF/фото.")
        if factual_lines and not requires_lab_resubmission and has_lab_uncertainty_note
        else ("Факты анализов: " + "; ".join(factual_lines[:3]) + ".")
        if factual_lines and not requires_lab_resubmission
        else "Факты анализов: по нечёткому фото выводы не строим - нужен PDF/чёткое фото или ручной ввод показателей.",
        f"Первый маршрут: гинеколог по кровопотере и циклу, затем эндокринолог по ТТГ/L-тироксину; параллельно 3 дня стабилизировать сон/кофе/завтрак ({sleep_stress})."
        if sleep_stress and has_heavy_cycle_signal and ferritin_line
        else f"Первый управляемый рычаг: 3 дня стабилизировать сон/кофе/завтрак и параллельно подготовить врачебные вопросы по ферритину, ТТГ и циклу ({sleep_stress})."
        if sleep_stress
        else "Первый управляемый рычаг: 3 дня стабилизировать питание/сон и параллельно подготовить врачебные вопросы по анализам.",
    ]
    top_actions = [
        "Сегодня: не добавлять новые препараты/сильные добавки; записать лекарства, добавки, дозировки, сон, кофе, питание и главные жалобы.",
        "Ближайшие 3 дня: выполнить персональный мини-план ниже и отметить реакцию по шкале 0-10: энергия, ЖКТ, сон, сердцебиение/цикл/кожа.",
        "До 14 дней: подтвердить анализы, выбрать 1-2 профильных врача и прийти с готовыми вопросами из этого досье.",
    ]
    stop_signals = [
        "Не начинать самостоятельно железо, йод, селен, гормонально-активные комплексы и интенсивные схемы добавок.",
        "Не интерпретировать нечёткие фото анализов как факт.",
        "Срочно к врачу/в неотложную помощь: обморок, боль в груди, одышка, пульс в покое выше 100 с плохим самочувствием, сильное кровотечение или резкое ухудшение.",
    ]

    three_step_protocol = [
        {
            "title": "1. Сон и стресс: быстрый рычаг",
            "body": "Первые 3 дня не лечим всё сразу: стабилизируем сон, кофе, вечерний экран и реакцию нервной системы. Это база, без которой питание и добавки дают меньше эффекта.",
        },
        {
            "title": "2. Врачи и анализы: точность вместо догадок",
            "body": "Отделяем факты от гипотез, подтверждаем спорные показатели и готовим конкретные вопросы врачу. Цель - снизить риск ошибки, а не собрать бесконечный список обследований.",
        },
        {
            "title": "3. Питание, добавки и нагрузка: только по данным",
            "body": "Питание и мягкую активность можно начать сразу. Добавки - только если они уместны по анализам, совместимы с фоном и не выглядят как лечение вместо врача.",
        },
    ]

    if "1:00" in sleep_stress or "01" in sleep_stress or "5:00" in sleep_stress or "5-6" in sleep_stress:
        sleep_action = "Отбой: сегодня не пытаться лечь идеально рано; сдвинуть сон на 15-20 минут раньше и выключить яркий экран за 40-60 минут до сна."
    else:
        sleep_action = "Отбой: выбрать реалистичное время сна и сдвигать его на 15-20 минут раньше каждые 2-3 дня."

    breakfast_action = (
        "Завтрак: вместо кофе и сладкого - яйца/рыба/птица/творог по переносимости + тёплая крупа или овощи; кофе только после еды."
        if "завтрак" in nutrition.lower() or "кофе" in nutrition.lower() or "слад" in nutrition.lower()
        else "Завтрак: белок + мягкая клетчатка + тёплый напиток; кофе не натощак."
    )
    digestion_action = (
        f"ЖКТ: из-за жалобы «{digestion}» 3 дня отмечать, после каких продуктов усиливается симптом; резкие исключающие диеты не начинать."
        if digestion
        else "ЖКТ: 3 дня отмечать вздутие, стул, тяжесть, реакцию на кофе, молочные продукты, выпечку и поздний ужин."
    )

    plan_3_days = [
        {
            "day": "День 1",
            "focus": "Стабилизировать день без резких протоколов",
            "actions": [
                sleep_action,
                breakfast_action,
                "Практика 3 минуты: медленный вдох на 4 счёта, выдох на 6; задача - снизить вечернее возбуждение, а не идеально медитировать.",
            ],
        },
        {
            "day": "День 2",
            "focus": "Собрать факты для точного разбора",
            "actions": [
                "Загрузить анализы в PDF/чётком фото; если показатель, единицы или дата не видны - ввести ключевые цифры текстом.",
                digestion_action,
                "Составить список: лекарства, добавки, дозировки, время приёма, как давно принимаются и кто назначил.",
            ],
        },
        {
            "day": "День 3",
            "focus": "Подготовить врачебный маршрут",
            "actions": [
                "Выбрать 1-2 первоочередных специалиста по текущему фону, а не идти ко всем сразу.",
                "Подготовить вопросы из раздела ниже и последние анализы/УЗИ.",
                "Отправить в бот один главный вопрос по разбору - он пойдёт в сопровождение на 30 дней.",
            ],
        },
    ]

    gynecology_question = {
            "specialist": "Гинеколог",
            "questions": [
                (
                    f"Может ли обильный цикл быть фактором потерь железа при {ferritin_line} и текущей усталости?"
                    if ferritin_line
                    else "Может ли обильный цикл быть фактором потерь железа и усталости?"
                ),
                "Как вести дневник кровопотери 1-2 цикла: количество прокладок/тампонов, сгустки, ночные протекания, боль, слабость?",
                "Нужно ли исключить миомы, полипы, усиление эндометриоза или другие причины кровопотери?",
            ],
        }
    endocrinology_question = {
            "specialist": "Эндокринолог",
            "questions": [
                (
                    f"Как оценить щитовидный фон с учётом {tsh_line}, усталости, зябкости, выпадения волос и текущего L-тироксина?"
                    if tsh_line
                    else "Как оценить текущий щитовидный фон по ТТГ, свободному Т4/Т3 и симптомам?"
                ),
                "Нужны ли свободный Т4/Т3, антитела к ТПО/ТГ и контроль УЗИ щитовидной железы?",
                "С каким интервалом от L-тироксина держать кофе, еду, железо, кальций и магний, чтобы не мешать терапии?",
            ],
        }
    doctor_questions = [
        gynecology_question,
        endocrinology_question,
        {
            "specialist": "Гастроэнтеролог / терапевт",
            "questions": [
                f"Как безопасно разбирать ЖКТ-жалобы: {digestion}?" if digestion else "Как безопасно разбирать вздутие, стул, переносимость продуктов и боль/дискомфорт?",
                "Нужно ли проверять переносимость продуктов, воспалительные маркеры, желчный/поджелудочный маршрут или СИБР по показаниям?",
                "Какие симптомы требуют очного обращения быстрее планового визита?",
            ],
        },
    ]

    if "сердц" in background or "тахик" in background or "пульс" in background:
        doctor_questions.append(
            {
                "specialist": "Кардиолог / терапевт",
                "questions": [
                    "Нужны ли ЭКГ, Холтер или контроль давления при сердцебиении?",
                    "Какая нагрузка безопасна до уточнения причин симптома?",
                    "При каких значениях пульса/давления и симптомах обращаться срочно, а не ждать планового приёма?",
                ],
            }
        )

    circadian_checklist = [
        "Утром: свет в первые 30-60 минут после пробуждения и вода.",
        "Днём: кофе только после еды и не во второй половине дня, если есть тревожность/сон 4-6 часов.",
        "Вечером: за 40-60 минут до сна приглушить свет, убрать яркий экран, не разбирать тяжёлые вопросы.",
        "Нагрузка: 10-15 минут спокойной ходьбы или мягкой разминки, без форсирования.",
        "Отслеживание: сон, энергия, ЖКТ, кожа/цикл, реакция на питание и нагрузку.",
    ]

    followup_offer = [
        "После загрузки качественных анализов - бесплатный 15-минутный уточняющий разбор маршрута.",
        "В течение 30 дней после готового досье можно присылать сюда анализы, УЗИ, выписки за последние 6 месяцев, фото, вопросы и реакции на план.",
        "Если врач подтвердит необходимость коррекции железа, витамина D, щитовидной терапии или других добавок, бот поможет разложить назначение по времени приёма, совместимости и наблюдению реакции.",
        "Если витамин D считан с нечёткого фото, сначала сверяем значение по PDF/тексту; только потом обсуждаем нутрицевтический вариант.",
        "Фото жалоб можно отправлять с подписью: где находится, как давно, есть ли боль/зуд/рост/температура. Бот не ставит диагноз по фото, но поможет понять срочность и к какому врачу идти.",
        "После новых данных план корректируется как сопровождение, а не как разовая выдача.",
        "Нутрицевтические схемы подбираются индивидуально: по анкете, анализам, переносимости, фону и совместимости; это не лекарственное назначение.",
    ]

    pdf_data["executive_summary"] = {
        "headline": "Карта ближайших 14 дней",
        "key_findings": key_findings[:3],
        "top_actions": top_actions,
        "stop_signals": stop_signals,
    }
    pdf_data["three_step_protocol"] = three_step_protocol
    pdf_data["plan_3_days"] = plan_3_days
    pdf_data["doctor_questions"] = doctor_questions[:4]
    pdf_data["circadian_checklist"] = circadian_checklist
    pdf_data["followup_offer"] = followup_offer
    pdf_data["mini_example"] = (
        "Пример отличия от бесплатных советов: не просто «пейте воду и спите», а конкретно: "
        "сегодня кофе только после белкового завтрака, сон сдвинуть на 15-20 минут раньше, "
        "вечером отметить ЖКТ/энергию/сердцебиение и подготовить список добавок с дозировками."
    )
    pdf_data["analysis_confidence"] = (
        "Предварительно, без опоры на анализы" if not has_labs else "С учётом подтверждённых данных, но без медицинского диагноза"
    )
    return pdf_data

def apply_safe_action_floor(pdf_data: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    """Add a concrete safe plan when the AI draft is too generic for a premium dossier."""
    medical = submission.get("medical_context") or {}
    lab_confirmation_status = str(submission.get("lab_confirmation_status") or "")
    lab_confirmation_pending = lab_confirmation_status in {"pending_client_confirmation", "client_correction_needed"}
    has_labs = bool(submission.get("parsed_biomarkers")) and not submission.get("requires_lab_resubmission") and not lab_confirmation_pending
    background = " ".join(
        str(medical.get(key) or "")
        for key in (
            "symptoms",
            "wellbeing_energy",
            "complaint_pattern",
            "work_lifestyle",
            "nutrition",
            "food_behavior",
            "digestion",
            "sleep_stress",
            "activity",
            "female_hormones",
            "emotional_stress",
            "background",
            "risk_details",
            "motivation",
            "red_flags",
            "lab_notes",
        )
    ).lower()
    complex_background = any(
        marker in background
        for marker in (
            "гипотире",
            "щитов",
            "эндометри",
            "беремен",
            "гв",
            "корм",
            "онко",
            "лекар",
            "препарат",
        )
    )

    def has_marker(*markers: str) -> bool:
        return any(marker in background for marker in markers)

    def merge_unique(front: list[str], existing: Any) -> list[str]:
        merged: list[str] = []
        seen: set[str] = set()
        for item in front + ensure_list(existing):
            text = str(item).strip()
            if not text:
                continue
            key = " ".join(text.lower().split())
            if key in seen:
                continue
            seen.add(key)
            merged.append(text)
        return merged

    def is_supplement_or_medication_hint(item: Any) -> bool:
        text = str(item).lower()
        markers = (
            "магни",
            "омега",
            "витамин",
            "д3",
            "d3",
            "b12",
            "фолат",
            "желез",
            "феррум",
            "йод",
            "селен",
            "препарат",
            "транексам",
            "гормон",
            "дозиров",
            "капсул",
            "таблет",
            "глицинат",
            "бисглицинат",
            "цитрат",
            "сибирское здоровье",
            "vitamax",
            "витамакс",
        )
        return any(marker in text for marker in markers)

    def sanitize_high_risk_text(value: str) -> str:
        text = str(value)
        replacements = {
            "Дефицит железа": "Возможный железодефицитный риск",
            "дефицит железа": "возможный железодефицитный риск",
            "дефицита железа": "железодефицитного риска",
            "Дефицит витамина D": "Недостаточный статус витамина D по нутрициологическому ориентиру",
            "дефицит витамина D": "недостаточный статус витамина D по нутрициологическому ориентиру",
            "Субклинический гипотиреоз": "Вопрос компенсации щитовидного фона",
            "субклинический гипотиреоз": "вопрос компенсации щитовидного фона",
            "Субклинический гипотиреоз или неполная компенсация": "Вопрос неполной компенсации щитовидного фона",
            "субклинический гипотиреоз или неоптимальная доза L-тироксина": "вопрос компенсации щитовидного фона и текущей тактики L-тироксина",
            "субклинической гипофункции щитовидной железы": "вопроса щитовидного фона",
            "неадекватную дозу тироксина": "вопрос текущей тактики тироксина",
            "неоптимальная доза L-тироксина": "вопрос текущей тактики L-тироксина",
            "коррекции дозы L-тироксина": "оценке текущей тактики L-тироксина",
            "необходимость повышения при ТТГ > 3.0": "что означает ТТГ в вашей ситуации",
            "возможна гормональная терапия или хирургическая коррекция для снижения кровопотери": "нужна очная врачебная оценка причин кровопотери и тактики наблюдения",
            "возможность приёма препаратов для снижения кровопотери (транексам, гормональная терапия)": "врачебную тактику при обильных кровотечениях",
            "транексам, гормональная терапия": "врачебная тактика",
            "показана очная консультация": "нужна очная консультация",
            "показана": "нужна врачебная оценка",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def sanitize_high_risk_list(items: Any, *, allow_lab_list: bool = True) -> list[str]:
        sanitized: list[str] = []
        for item in ensure_list(items):
            text = sanitize_high_risk_text(str(item).strip())
            lowered = text.lower()
            if not text:
                continue
            if any(marker in lowered for marker in ("2000 ме", "200-300", "мг вечером", "можно ли начать приём")):
                continue
            if "рассмотреть" in lowered and is_supplement_or_medication_hint(text):
                continue
            if "поддерж" in lowered and is_supplement_or_medication_hint(text):
                continue
            if is_supplement_or_medication_hint(text) and not any(
                safe_context in lowered
                for safe_context in (
                    "анализ",
                    "не начинать",
                    "не добавлять",
                    "что точно не стоит",
                    "список лекарств и добавок",
                    "ограничения по самостоятельным добавкам",
                )
            ):
                continue
            if any(marker in lowered for marker in ("транексам", "гормональная терапия", "хирургическая коррекция")):
                continue
            if "доз" in lowered and "l-тирокс" in lowered:
                text = "Эндокринолог: обсудить текущую тактику L-тироксина, динамику ТТГ/св. Т4/св. Т3 и ограничения по самостоятельным добавкам."
            if not allow_lab_list and is_supplement_or_medication_hint(text):
                continue
            sanitized.append(text)
        return merge_unique([], sanitized)

    specialist_candidates = []
    baseline_safety_lines = [
        "Если есть выраженное ухудшение, сильная боль, кровь, обмороки, нарастающая одышка или необычные кровотечения — не ждать планового разбора, а обращаться за очной медицинской помощью.",
        "На очный приём подготовить: список лекарств и добавок, дозировки, последние анализы/УЗИ, 7-дневный дневник симптомов, питания, сна, стула и реакции на нагрузку.",
    ]
    if has_marker("щитов", "гипотире", "ттг", "тиреоид"):
        specialist_candidates.append(
            "Эндокринолог: обсудить щитовидный фон, динамику ТТГ/св. Т4/св. Т3, антитела, текущую терапию и что точно не стоит добавлять самостоятельно."
        )
    if has_marker("эндометри", "цикл", "пмс", "кровотеч", "гинек", "беремен", "корм", "гв"):
        specialist_candidates.append(
            "Гинеколог: обсудить цикл, боли, кровопотери, эндометриоз/беременность/ГВ, допустимую нагрузку и ограничения по добавкам."
        )
    if has_marker("жкт", "стул", "вздут", "изжог", "тошнот", "живот", "диар", "запор"):
        specialist_candidates.append(
            "Гастроэнтеролог: обсудить стойкие жалобы ЖКТ, стул, боль, переносимость продуктов и необходимость очных обследований."
        )
    if has_marker("феррит", "гемоглоб", "анеми", "желез", "кровотеч"):
        specialist_candidates.append(
            "Терапевт или гематолог: обсудить анемический/железодефицитный паттерн, причины возможных потерь и безопасную тактику без самостоятельного железа."
        )
    if has_marker("сердц", "давлен", "тахик", "пульс", "одыш", "груд"):
        specialist_candidates.append(
            "Кардиолог или терапевт: обсудить сердцебиение, давление, одышку, боль в груди и допустимый уровень физической нагрузки."
        )
    if has_marker("голов", "онемен", "обмор", "головокруж", "невролог"):
        specialist_candidates.append(
            "Невролог: обсудить сильные головные боли, онемение, обмороки, выраженное головокружение или другие неврологические симптомы."
        )
    specialist_lines = baseline_safety_lines + specialist_candidates[:4]

    diet_floor = [
        "На ближайшие 3-7 дней не делать резких ограничительных диет: задача — стабилизировать питание и реакцию организма, а не лечить диагноз питанием.",
        "В каждом основном приёме пищи держать белковую опору: яйца, рыба, птица, творог/йогурт без сахара или бобовые — по переносимости и без насилия над ЖКТ.",
        "Добавить 1-2 порции овощей или зелени в день и наблюдать реакцию ЖКТ: вздутие, стул, тяжесть, тягу к сладкому.",
        "Кофе не пить натощак; если есть тревожность, слабость или ранние пробуждения — перенести кофе после еды и не позже первой половины дня.",
        "При эндометриозе и щитовидном фоне не уходить в экстремальные протоколы, голодания, жёсткий отказ от групп продуктов или самостоятельный йод/селен без врача и анализов.",
    ]
    habits_floor = [
        "7 дней сдвигать сон мягко: ложиться на 15-20 минут раньше каждые 2-3 дня, а не пытаться резко лечь идеально.",
        "За 60 минут до сна убрать яркий экран и тяжёлые обсуждения; оставить спокойный ритуал: душ, приглушённый свет, дыхание, чтение.",
        "Утром в первые 30-60 минут добавить свет и воду; это мягко поддерживает циркадный ритм без медицинских назначений.",
        "При сидячей работе начать с 10-15 минут спокойной ходьбы после еды или вечером; интенсивные тренировки не форсировать, если есть усталость и недосып.",
    ]
    control_floor = [
        "Протокол точности: разделять подтверждённые факты, осторожные гипотезы и неподтверждённые данные; не строить выводы на нечётком фото, сомнительных единицах измерения или неполном бланке.",
        "Если показатель, единицы, дата анализа или принадлежность бланка читаются неясно — этот показатель считается неподтверждённым до повторной отправки PDF/фото или ручного ввода.",
        "До очного уточнения не начинать самостоятельно лекарственные препараты, железо, йод, селен, гормонально-активные комплексы и интенсивные схемы добавок.",
        "При обильных менструациях вести 1-2 цикла дневник кровопотери: сколько прокладок/тампонов, есть ли сгустки, ночные протекания, слабость, головокружение и боль.",
        "Приоритет анализов для обсуждения, а не самоназначение: ОАК с формулой, ферритин с железным профилем, ТТГ + свободный Т4/Т3, витамин D, B12/фолат. Остальное добавлять только по решению врача.",
        "Если анализы уже есть, повторно не сдавать всё подряд: сначала сверить даты, единицы измерения, качество бланков и выбрать недостающие показатели.",
        "Через 2-4 недели оценить динамику: энергия, сон, ЖКТ, тяга к сладкому, переносимость питания, реакция на нагрузку и тревожные симптомы.",
        "Через 1 месяц решить вместе со специалистом, какие показатели действительно нужно пересдать, а какие пока наблюдать.",
        "Через 3 месяца провести контрольную точку: сравнить самочувствие, питание, нагрузку, сон и лабораторную динамику; не менять схему хаотично каждую неделю.",
    ]
    control_floor = specialist_lines + control_floor

    if complex_background or not has_labs:
        control_floor.append(
            "В этом кейсе первоочередной маршрут — 2-3 ключевых специалиста и подтверждение данных; расширять список врачей стоит только при симптомах из соответствующей зоны."
        )

    # Premium dossiers should read like a route, not like a generated article.
    # Keep these client-facing sections concise and deterministic; AI draft remains a source, not the final editor.
    pdf_data["diet_strategy"] = diet_floor
    pdf_data["lifestyle"] = habits_floor
    pdf_data["additional_control"] = control_floor[:10]

    schemes = pdf_data.get("schemes") if isinstance(pdf_data.get("schemes"), list) else []
    phased_plan = [
        {
            "time": "Сейчас / 24-72 часа",
            "name": "Безопасная стабилизация и стоп-лист",
            "comment": (
                "Не добавлять новые препараты и сильные добавки самостоятельно. Зафиксировать жалобы, лекарства, "
                "добавки, сон, питание и тревожные симптомы; при красных флагах — очная медицинская помощь."
            ),
        },
        {
            "time": "7 дней",
            "name": "Дневник реакции и базовая опора",
            "comment": (
                "Вести короткий дневник: питание, вода/кофе, стул, энергия, сон, нагрузка, боль/дискомфорт. "
                "Это даст врачу и нутрициологу факты, а не общие ощущения."
            ),
        },
        {
            "time": "2-4 недели",
            "name": "Уточнение анализов и маршрута специалистов",
            "comment": (
                "Собрать качественные PDF/фото анализов, не гадать по нечётким значениям, обсудить с профильным "
                "специалистом недостающие показатели и ограничения по добавкам."
            ),
        },
        {
            "time": "1 месяц",
            "name": "Первая контрольная точка",
            "comment": (
                "Оценить, что изменилось по энергии, сну, ЖКТ, циклу/нагрузке и питанию. Если жалобы сохраняются "
                "или усиливаются, не расширять добавки, а возвращаться к врачу с дневником и анализами."
            ),
        },
        {
            "time": "3 месяца",
            "name": "Контроль динамики",
            "comment": (
                "Сравнить самочувствие и лабораторную динамику, обновить нутрициологический план и оставить только "
                "те поддерживающие шаги, которые имеют понятную цель и не конфликтуют с медицинским фоном."
            ),
        },
    ]

    if not has_labs or complex_background:
        pdf_data["schemes"] = phased_plan
    else:
        pdf_data["schemes"] = phased_plan[:3] + [
            item for item in schemes
            if not is_supplement_or_medication_hint(item)
        ][:3]

    if complex_background or not has_labs:
        for field in (
            "findings",
            "hypotheses",
            "priorities",
            "working_hypotheses",
            "support_priorities",
            "diet_strategy",
            "lifestyle",
            "additional_control",
            "warning_signs",
        ):
            pdf_data[field] = sanitize_high_risk_list(pdf_data.get(field))
        strategy_payload = pdf_data.get("strategy")
        if isinstance(strategy_payload, dict):
            pdf_data["strategy"] = {
                key: "\n".join(sanitize_high_risk_list(value))
                for key, value in strategy_payload.items()
            }
            pdf_data["strategy"]["nutrition"] = "\n".join(diet_floor)
            pdf_data["strategy"]["habits"] = "\n".join(habits_floor)
            pdf_data["strategy"]["control"] = "\n".join(control_floor[:8])
        pdf_data["working_hypotheses"] = sanitize_high_risk_list(pdf_data.get("working_hypotheses"))[:4]
        pdf_data["support_priorities"] = sanitize_high_risk_list(pdf_data.get("support_priorities"))[:4]
        pdf_data["diet_strategy"] = diet_floor
        pdf_data["lifestyle"] = habits_floor
        pdf_data["additional_control"] = control_floor[:10]
        for field in (
            "main_request",
            "anamnesis",
            "diet_habits",
            "gi_status",
            "activity",
            "final_conclusion",
        ):
            if field in pdf_data:
                pdf_data[field] = sanitize_high_risk_text(str(pdf_data.get(field) or ""))

    conclusion = str(pdf_data.get("final_conclusion") or "").strip()
    accuracy_note = (
        " Точность здесь важнее скорости: этот документ является нутрициологической навигацией и черновиком для экспертной проверки, "
        "а не медицинским заключением. Все сомнительные значения анализов нужно подтвердить по качественному PDF/фото или ручному вводу; "
        "медицинские решения и терапию следует обсуждать с врачом."
    )
    if "Точность здесь важнее скорости" not in conclusion:
        pdf_data["final_conclusion"] = (conclusion + accuracy_note).strip()

    return build_premium_value_packaging(pdf_data, submission)


def value_contains_any(value: str | None, markers: tuple[str, ...]) -> bool:
    if not value:
        return False
    normalized = " ".join(str(value).lower().split())
    return any(marker in normalized for marker in markers)


def is_lab_confirmation_yes(text: str) -> bool:
    normalized = " ".join(str(text).lower().replace("ё", "е").split())
    return normalized in {
        "да",
        "да верно",
        "да, верно",
        "верно",
        "все верно",
        "все правильно",
        "правильно",
        "цифры верны",
        "подтверждаю",
    }


def mark_lab_confirmation(session: dict[str, Any], *, status: str, note: str | None = None) -> None:
    session["lab_confirmation_status"] = status
    session["lab_confirmation_needed"] = status == "pending_client_confirmation"
    if note:
        current = str(session.get("lab_notes") or "").strip()
        session["lab_notes"] = f"{current}\n{note}".strip() if current else note


def has_blocking_quality_items(items: list[Any]) -> bool:
    positive_markers = (
        "нет необосн",
        "нет риск",
        "является правильным",
        "оправдан",
        "правильный подход",
    )
    blocking_markers = (
        "опас",
        "риск",
        "необходимо",
        "недостат",
        "отсутств",
        "не хватает",
        "без уч",
        "может быть риск",
    )
    for item in items:
        normalized = " ".join(str(item).lower().split())
        if not normalized:
            continue
        if any(marker in normalized for marker in positive_markers):
            continue
        if any(marker in normalized for marker in blocking_markers):
            return True
    return False


def compute_internal_review_signals(
    judge_report_text: str | None,
    growth_report_text: str | None,
) -> dict[str, Any]:
    judge = load_report_dict(judge_report_text)
    growth = load_report_dict(growth_report_text)

    critical_issues = judge.get("critical_issues") or []
    supplement_risks = judge.get("supplement_risks") or []
    escalation_checks = judge.get("doctor_escalation_checks") or []
    market_value_risks = judge.get("market_value_risks") or []
    demand_risks = growth.get("demand_risks") or []
    value_gaps = growth.get("value_gaps") or []

    judge_verdict = str(judge.get("verdict") or "")
    market_verdict = str(growth.get("market_verdict") or "")
    quality_verdict_is_blocking = value_contains_any(
        judge_verdict,
        ("fail", "unsafe", "critical", "rework", "block"),
    )

    needs_quality_rework = (
        quality_verdict_is_blocking
        or has_blocking_quality_items(supplement_risks)
        or (quality_verdict_is_blocking and (bool(critical_issues) or bool(escalation_checks)))
    )
    needs_market_rework = (
        len(demand_risks) >= 2
        or len(value_gaps) >= 2
        or len(market_value_risks) >= 2
        or value_contains_any(
            market_verdict,
            ("needs", "weak", "rework", "low", "unclear", "stronger"),
        )
    )

    review_flags: list[str] = []
    if needs_quality_rework:
        review_flags.append("quality_rework")
    if needs_market_rework:
        review_flags.append("market_rework")

    return {
        "judge_verdict": judge_verdict or None,
        "market_verdict": market_verdict or None,
        "needs_quality_rework": needs_quality_rework,
        "needs_market_rework": needs_market_rework,
        "review_flags": review_flags,
    }


def apply_internal_review_signals(
    submission: dict[str, Any],
    judge_report_text: str | None,
    growth_report_text: str | None,
) -> dict[str, Any]:
    signals = compute_internal_review_signals(judge_report_text, growth_report_text)
    submission["internal_review"] = signals
    return signals


DELIVERY_BLOCKING_JUDGE_VERDICTS = {
    "needs_revision",
    "must_rewrite",
    "must_rewrite_with_high_caution",
    "reject",
    "fail",
    "unsafe",
    "blocked",
}


def build_delivery_block_reason(submission: dict[str, Any]) -> dict[str, Any] | None:
    internal_review = submission.get("internal_review") or {}
    judge_verdict = str(internal_review.get("judge_verdict") or "").strip().lower()
    review_flags = {
        str(flag).strip().lower()
        for flag in (internal_review.get("review_flags") or [])
        if str(flag).strip()
    }
    needs_quality_rework = bool(internal_review.get("needs_quality_rework"))

    if not (
        judge_verdict in DELIVERY_BLOCKING_JUDGE_VERDICTS
        or needs_quality_rework
        or "quality_rework" in review_flags
    ):
        return None

    return {
        "judge_verdict": judge_verdict or None,
        "review_flags": sorted(review_flags),
        "needs_quality_rework": needs_quality_rework,
    }


def build_judge_preview_lines(report_text: str | None) -> list[str]:
    if not report_text:
        return []

    try:
        report = json.loads(strip_json_code_fences(report_text))
    except Exception:
        preview = report_text.strip().replace("\n", " ")
        return ["", "Judge review:", preview[:1000]]

    lines = ["", "Judge review:"]
    verdict = report.get("verdict")
    if verdict:
        lines.append(f"Verdict: {verdict}")

    sections = [
        ("Critical issues", "critical_issues"),
        ("Logic gaps", "logic_gaps"),
        ("Unnecessary / weak", "unnecessary_or_weak_items"),
        ("Supplement risks", "supplement_risks"),
        ("Doctor escalation checks", "doctor_escalation_checks"),
        ("Market value risks", "market_value_risks"),
        ("Commercial growth opportunities", "commercial_growth_opportunities"),
        ("Rewrite priorities", "rewrite_priorities"),
    ]
    for label, key in sections:
        items = report.get(key) or []
        if not items:
            continue
        lines.append(f"{label}:")
        for item in items[:3]:
            lines.append(f"- {item}")

    admin_note = report.get("admin_note")
    if admin_note:
        lines.append(f"Заметка для администратора: {admin_note}")

    return lines


def build_growth_preview_lines(report_text: str | None) -> list[str]:
    if not report_text:
        return []

    try:
        report = json.loads(strip_json_code_fences(report_text))
    except Exception:
        preview = report_text.strip().replace("\n", " ")
        return ["", "Growth architect:", preview[:1000]]

    lines = ["", "Growth architect:"]
    market_verdict = report.get("market_verdict")
    if market_verdict:
        lines.append(f"Market verdict: {market_verdict}")

    sections = [
        ("Demand risks", "demand_risks"),
        ("Value gaps", "value_gaps"),
        ("Positioning upgrades", "positioning_upgrades"),
        ("Conversion ideas", "conversion_ideas"),
        ("Retention ideas", "retention_ideas"),
        ("Referral ideas", "referral_ideas"),
        ("Next experiments", "next_experiments"),
    ]
    for label, key in sections:
        items = report.get(key) or []
        if not items:
            continue
        lines.append(f"{label}:")
        for item in items[:3]:
            lines.append(f"- {item}")

    admin_note = report.get("admin_note")
    if admin_note:
        lines.append(f"Заметка для администратора: {admin_note}")

    return lines


async def notify_admins(
    submission: dict[str, Any],
    draft_text: str | None,
    judge_report_text: str | None = None,
    growth_report_text: str | None = None,
) -> None:
    if not settings.admin_chat_ids:
        return

    summary_lines = [
        "Новая заявка",
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
        summary_lines.append("Черновик нейросети:")
        summary_lines.append(draft_preview[:1200])

    internal_review = submission.get("internal_review") or {}
    review_flags = internal_review.get("review_flags") or []
    if review_flags:
        summary_lines.append("")
        summary_lines.append(f"Внутренние флаги проверки: {', '.join(review_flags)}")

    summary_lines.extend(build_judge_preview_lines(judge_report_text))
    summary_lines.extend(build_growth_preview_lines(growth_report_text))

    message_text = "\n".join(summary_lines)
    
    markup = None
    if draft_text and "pdf_path" in submission:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Одобрить и отправить клиенту", callback_data=f"approve_{submission['submission_id']}")],
                [InlineKeyboardButton(text="🔄 Перегенерировать PDF", callback_data=f"regen_{submission['submission_id']}")],
                [InlineKeyboardButton(text="✏️ Это черновик (требует правок)", callback_data=f"draft_only_{submission['submission_id']}")]
            ]
        )

    for admin_chat_id in settings.admin_chat_ids:
        try:
            if "pdf_path" in submission and Path(submission["pdf_path"]).exists():
                from aiogram.types import FSInputFile
                pdf_doc = FSInputFile(submission["pdf_path"])
                await bot.send_document(
                    admin_chat_id, 
                    document=pdf_doc, 
                    caption=build_admin_pdf_caption(submission),
                    reply_markup=markup
                )
                for chunk in split_telegram_text(message_text):
                    await bot.send_message(admin_chat_id, chunk)
            else:
                chunks = split_telegram_text(message_text)
                for idx, chunk in enumerate(chunks):
                    await bot.send_message(
                        admin_chat_id,
                        chunk,
                        reply_markup=markup if idx == len(chunks) - 1 else None,
                    )
        except Exception:
            logger.exception("Failed to notify admin chat %s", admin_chat_id)


async def notify_admins_payment_handoff(submission: dict[str, Any]) -> None:
    if not settings.admin_chat_ids:
        return

    payment_context = submission.get("payment_context", {})
    summary_lines = [
        "💳 Анкета завершена: ожидаем оплату",
        f"ID: {submission['submission_id']}",
        f"Продукт: {payment_context.get('offer_name') or TIER_NAMES.get(submission.get('offer'), 'Персональный разбор')}",
        f"Клиент: {submission['profile'].get('full_name') or submission['profile'].get('telegram_full_name')}",
        f"Сумма: {payment_context.get('amount_rub', PREMIUM_PRICE_RUB)} ₽",
        f"Симптомы: {submission['medical_context'].get('symptoms')}",
        "Дальше: после успешной оплаты генерация досье запустится автоматически.",
    ]
    message_text = "\n".join(summary_lines)

    for admin_chat_id in settings.admin_chat_ids:
        try:
            await bot.send_message(admin_chat_id, message_text)
        except Exception:
            logger.exception("Failed to notify admin payment handoff to chat %s", admin_chat_id)


async def notify_admins_manual_handoff(submission: dict[str, Any]) -> None:
    if not settings.admin_chat_ids:
        return

    payment_context = submission.get("payment_context", {})
    summary_lines = [
        "🟡 Анкета завершена: ожидается ручное подтверждение оплаты",
        f"ID: {submission['submission_id']}",
        f"Продукт: {payment_context.get('offer_name') or TIER_NAMES.get(submission.get('offer'), 'Персональный разбор')}",
        f"Клиент: {submission['profile'].get('full_name') or submission['profile'].get('telegram_full_name')}",
        f"Сумма: {payment_context.get('amount_rub', PREMIUM_PRICE_RUB)} ₽",
        f"Симптомы: {submission['medical_context'].get('symptoms')}",
        f"Цель: {submission['medical_context'].get('goal')}",
        "Дальше: сначала подтвердите оплату вручную. Генерация досье не стартует до подтверждения.",
    ]
    message_text = "\n".join(summary_lines)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить ручную оплату",
                    callback_data=f"manualpay_{submission['submission_id']}",
                )
            ]
        ]
    )

    for admin_chat_id in settings.admin_chat_ids:
        try:
            await bot.send_message(admin_chat_id, message_text, reply_markup=markup)
        except Exception:
            logger.exception("Failed to notify admin manual handoff to chat %s", admin_chat_id)


@dp.callback_query(lambda c: c.data and c.data.startswith("manualpay_"))
async def process_manual_payment_confirm(callback_query: types.CallbackQuery) -> None:
    if not is_admin(callback_query.from_user.id):
        return

    submission_id = callback_query.data.replace("manualpay_", "", 1)
    submission = load_submission(settings.submissions_dir, submission_id)
    if not submission:
        await bot.answer_callback_query(callback_query.id, "Кейс не найден.")
        return

    if is_payment_confirmed_for_dossier(submission):
        await bot.answer_callback_query(callback_query.id, "Оплата уже подтверждена.")
        return

    mark_manual_payment_confirmed(
        submission,
        now_iso=utc_now_iso(),
        admin_user_id=callback_query.from_user.id,
        note="Confirmed from admin Telegram callback.",
    )
    save_submission_state(settings.submissions_dir, submission)

    client_id = submission.get("profile", {}).get("telegram_user_id")
    admin_chat_id = callback_query.message.chat.id if callback_query.message else callback_query.from_user.id
    session = build_session_from_submission(
        submission,
        SimpleNamespace(
            id=client_id,
            username=submission.get("profile", {}).get("telegram_username"),
            full_name=submission.get("profile", {}).get("telegram_full_name"),
        ),
    )
    if client_id:
        user_sessions[client_id] = session
        touch_session()

    tier = str(submission.get("offer") or session.get("tier") or session.get("offer") or "standard").strip().lower()
    if is_instant_paid_product(tier):
        if client_id:
            try:
                await activate_paid_product(client_id, session)
            except Exception:
                logger.exception("Failed to activate instant product after manual payment for %s", submission_id)
        await bot.send_message(admin_chat_id, f"✅ Ручная оплата подтверждена для {submission_id}. Быстрый тариф активирован.")
        await bot.answer_callback_query(callback_query.id, "Ручная оплата подтверждена.")
        return

    if client_id:
        try:
            await bot.send_message(
                client_id,
                "Оплата подтверждена. Начинаю сборку персонального разбора. После генерации результат будет отправлен прямо сюда, без ожидания внутренней проверки.",
            )
        except Exception:
            logger.exception("Failed to notify client about manual payment confirmation for %s", submission_id)

    await bot.send_message(
        admin_chat_id,
        f"✅ Ручная оплата подтверждена для {submission_id}. Запускаю сборку разбора.",
    )
    await bot.answer_callback_query(callback_query.id, "Ручная оплата подтверждена.")

    await build_dossier_after_payment(
        callback_query.message,
        session,
        progress_chat_id=admin_chat_id,
        client_chat_id=client_id,
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("clientconfirmpay_"))
async def process_client_payment_confirm(callback_query: types.CallbackQuery) -> None:
    submission_id = callback_query.data.replace("clientconfirmpay_", "", 1)
    submission = load_submission(settings.submissions_dir, submission_id)
    if not submission:
        await bot.answer_callback_query(callback_query.id, "Заявка не найдена.")
        return

    # If already confirmed by admin
    if submission.get("intake_status") == "manual_payment_confirmed":
        await bot.answer_callback_query(callback_query.id, "Ваша оплата уже подтверждена кураторами!")
        return

    # Check if client has already reported payment
    if submission.get("client_reported_payment"):
        await bot.answer_callback_query(callback_query.id, "Вы уже подтвердили оплату. Команда проверяет её.")
        return

    # Mark as reported by client
    submission["client_reported_payment"] = True
    submission["client_reported_payment_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, submission)

    # Update the message text to confirm
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None # Remove the button
        )
    except Exception:
        pass

    await bot.send_message(
        callback_query.message.chat.id,
        "✅ Отметка об оплате получена! Наша команда уже проверяет платёж. "
        "Как только оплата будет подтверждена, мы сразу начнем работу."
    )

    # Also, notify admins about this client action!
    payment_context = submission.get("payment_context", {})
    offer_name = payment_context.get("offer_name") or TIER_NAMES.get(submission.get("offer") or submission.get("tier"), "Разбор")
    client_name = submission.get("profile", {}).get("full_name") or submission.get("profile", {}).get("telegram_full_name") or "Клиент"
    
    admin_alert_text = (
        f"⚡️ <b>Клиент подтвердил ручную оплату!</b>\n\n"
        f"ID: <code>{submission_id}</code>\n"
        f"👤 Клиент: {client_name}\n"
        f"🛍️ Продукт: {offer_name}\n"
        f"💰 Сумма: {payment_context.get('amount_rub')} ₽\n\n"
        f"Пожалуйста, проверьте поступление средств и подтвердите в системе."
    )
    
    admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить ручную оплату",
                    callback_data=f"manualpay_{submission_id}",
                )
            ]
        ]
    )

    for admin_chat_id in settings.admin_chat_ids:
        try:
            await bot.send_message(admin_chat_id, admin_alert_text, reply_markup=admin_markup, parse_mode="HTML")
        except Exception:
            logger.exception("Failed to send client payment alert to admin %s", admin_chat_id)

    await bot.answer_callback_query(callback_query.id, "Оплата подтверждена!")


@dp.callback_query(lambda c: c.data and c.data.startswith("approve_"))
async def process_admin_approval(callback_query: types.CallbackQuery) -> None:
    if not is_admin(callback_query.from_user.id):
        return
        
    submission_id = callback_query.data.replace("approve_", "")
    submission = load_submission(settings.submissions_dir, submission_id)
    
    if not submission:
        await bot.answer_callback_query(callback_query.id, "Кейс не найден.")
        return
        
    client_id = submission["profile"].get("telegram_user_id")
    pdf_path = submission.get("pdf_path")
    
    if not client_id or not pdf_path or not Path(pdf_path).exists():
        await bot.answer_callback_query(callback_query.id, "Не могу отправить: нет ID клиента или PDF-файла.")
        return

    delivery_block_reason = build_delivery_block_reason(submission)
    if delivery_block_reason:
        override_note = str(submission.get("manual_override_note") or "").strip()
        override_by = str(submission.get("manual_override_by") or "").strip()
        if not (override_note and override_by):
            now_iso = utc_now_iso()
            update_submission_status(
                submission,
                intake_status="delivery_blocked_needs_revision",
                now_iso=now_iso,
            )
            submission["delivery_blocked_at"] = now_iso
            submission["delivery_blocked_reason"] = delivery_block_reason
            save_submission_state(settings.submissions_dir, submission)
            await bot.answer_callback_query(
                callback_query.id,
                "Доставка заблокирована: внутренний критик требует доработки.",
                show_alert=True,
            )
            await bot.send_message(
                callback_query.from_user.id,
                (
                    f"⚠️ Досье {submission_id} не отправлено клиенту.\n"
                    "Причина: внутренний критик отметил риск качества/безопасности. "
                    "Сначала доработайте досье или оформите отдельный manual override."
                ),
            )
            return
        submission["manual_override_applied_at"] = utc_now_iso()
        logger.warning(
            "Delivery override for %s by %s: %s",
            submission_id,
            override_by,
            override_note,
        )

    from aiogram.types import FSInputFile
    pdf_doc = FSInputFile(pdf_path)
    
    await bot.send_document(
        client_id,
        document=pdf_doc,
        caption=(
            "Ваше досье готово. Начните с первой страницы: там карта ближайших 14 дней, "
            "план на 3 дня и стоп-сигналы.\n\n"
            "Если вам потребуется сдать назначенные анализы, вы можете сделать это со скидкой через наш кабинет в <b>HelloDoc</b>:\n"
            "🔗 <a href='https://hellodoc.app/s/27u6a/'>Сдать анализы со скидкой через HelloDoc</a>\n"
            "Резервная ссылка: <a href='https://hellodoc.app/s/gdgjq/'>HelloDoc Резерв</a>\n\n"
            "В течение 30 дней можно присылать сюда новые анализы, УЗИ, выписки за последние 6 месяцев, фото жалоб и вопросы по плану. "
            "Я помогу аккуратно скорректировать маршрут без диагнозов и самоназначений."
        ),
        parse_mode="HTML"
    )
    update_submission_status(submission, intake_status="delivered_to_client", now_iso=utc_now_iso())
    submission["delivered_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, submission)
    
    await bot.send_message(callback_query.from_user.id, f"✅ Досье {submission_id} успешно доставлено клиенту.")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(lambda c: c.data and c.data.startswith("regen_"))
async def process_admin_regen(callback_query: types.CallbackQuery) -> None:
    if not is_admin(callback_query.from_user.id):
        return
        
    submission_id = callback_query.data.replace("regen_", "")
    submission = load_submission(settings.submissions_dir, submission_id)
    
    if not submission or "draft_path" not in submission:
        await bot.answer_callback_query(callback_query.id, "Черновики не найдены.")
        return

    await bot.send_message(callback_query.from_user.id, f"🔄 Перегенерация PDF для {submission_id}...")
    
    try:
        from pathlib import Path
        draft_path = Path(submission["draft_path"])
        draft_text = draft_path.read_text(encoding="utf-8")
        
        import re
        clean_json_str = draft_text.strip()
        clean_json_str = re.sub(r"^```(?:json)?\s*", "", clean_json_str, flags=re.IGNORECASE)
        clean_json_str = re.sub(r"\s*```$", "", clean_json_str)
        
        pdf_data = apply_safe_action_floor(
            normalize_dossier_pdf_data(json.loads(clean_json_str.strip()), submission=submission),
            submission,
        )
        offer_code = submission.get("offer") or submission.get("tier")
        prefix = get_product_filename_prefix(offer_code)
        pdf_filename = f"{prefix}_{submission_id}.pdf"
        pdf_path = settings.drafts_dir / pdf_filename
        
        await asyncio.to_thread(create_premium_pdf, pdf_data, str(pdf_path))
        submission["pdf_path"] = str(pdf_path)
        update_submission_status(submission, intake_status="awaiting_human_review", now_iso=utc_now_iso())
        submission["regenerated_at"] = utc_now_iso()
        save_submission_state(settings.submissions_dir, submission)
        
        from aiogram.types import FSInputFile
        pdf_doc = FSInputFile(str(pdf_path))
        await bot.send_document(
            callback_query.from_user.id, 
            document=pdf_doc, 
            caption=f"✅ Обновлённый PDF готов для {submission_id}. Можно одобрять.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Одобрить и отправить", callback_data=f"approve_{submission_id}")]
                ]
            )
        )
    except Exception as e:
        logger.exception("Manual regeneration failed")
        await bot.send_message(callback_query.from_user.id, f"❌ Ошибка: {str(e)}")
    
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(lambda c: c.data and c.data.startswith("draft_only_"))
async def process_admin_draft(callback_query: types.CallbackQuery) -> None:
    if not is_admin(callback_query.from_user.id):
        return
    submission_id = callback_query.data.replace("draft_only_", "")
    submission = load_submission(settings.submissions_dir, submission_id)
    if submission:
        update_submission_status(submission, intake_status="draft_requires_edits", now_iso=utc_now_iso())
        save_submission_state(settings.submissions_dir, submission)
    await bot.send_message(
        callback_query.from_user.id, 
        "Окей, файл останется черновиком. Вы можете внести правки в JSON файл на сервере и перегенерировать документ."
    )
    await bot.answer_callback_query(callback_query.id)


async def send_loading_status(chat_id: int) -> asyncio.Task:
    async def _updater():
        statuses = [
            "⏳ <i>Анализирую клиническую картину...</i>",
            "⏳ <i>Выявляю корреляции и скрытые паттерны...</i>",
            "⏳ <i>Структурирую гипотезы и маркеры внимания...</i>",
            "⏳ <i>Верстаю премиальное досье...</i>",
            "⏳ <i>Финальная валидация данных...</i>"
        ]
        status_msg = None
        try:
            status_msg = await bot.send_message(chat_id, statuses[0], parse_mode="HTML")
            for idx in range(1, len(statuses)):
                await asyncio.sleep(4)
                await bot.edit_message_text(statuses[idx], chat_id=chat_id, message_id=status_msg.message_id, parse_mode="HTML")
            while True:
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
        finally:
            if status_msg:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
                except Exception:
                    pass
    return asyncio.create_task(_updater())



INSTANT_PAID_PRODUCT_STEPS = {
    "nutri_chat": "paid_nutri_chat",
    "habits": "habits_daily_log",
    "osipov": "osipov_context",
}


def is_instant_paid_product(tier: str | None) -> bool:
    return str(tier or "").strip().lower() in INSTANT_PAID_PRODUCT_STEPS


async def activate_paid_product(chat_id: int, session: dict[str, Any]) -> None:
    tier = str(session.get("tier") or session.get("offer") or "standard").strip().lower()

    if tier == "nutri_chat":
        session["step"] = "paid_nutri_chat"
        session["nutri_chat_started_at"] = utc_now_iso()
        session["nutri_chat_expires_at"] = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
        touch_session()
        await bot.send_message(
            chat_id,
            "✅ Оплата подтверждена. Нутри-чат открыт на 2 дня.\n\n"
            "Напишите вопрос по питанию, привычкам, ЖКТ, желчеоттоку, энергии, сну или самочувствию. "
            "Я отвечу в формате: кратко пойму вопрос, при необходимости уточню детали, дам возможную нутрициологическую гипотезу и 1-3 практических шага.",
        )
        return

    if tier == "habits":
        session["step"] = "habits_daily_log"
        touch_session()
        await bot.send_message(
            chat_id,
            "✅ Оплата подтверждена. Тариф «Привычки и тарелка» открыт на 21 день.\n\n"
            "Пожалуйста, присылайте каждый ваш прием пищи, начиная с самого пробуждения и стакана теплой воды — это очень важно! "
            "Отправляйте фото на завтрак, обед, ужин и перекусы, обязательно добавляя описание текстом под каждым фото.\n\n"
            "В конце дня также можете прислать текстом данные по сну, уровню стресса, энергии, тяге к сладкому, состоянию ЖКТ/стула и отёкам. "
            "Я буду формировать короткий отчет за день, а кураторы предоставят подробную обратную связь.",
        )
        return

    if tier == "osipov":
        session["step"] = "osipov_context"
        touch_session()
        await bot.send_message(chat_id, "✅ Оплата подтверждена.")
        await bot.send_message(chat_id, osipov_context_prompt())
        return
async def finalize_submission(message: types.Message, session: dict[str, Any]) -> None:
    submission = build_submission_payload(session)
    submission["payment_context"] = build_payment_context(session, now_iso=utc_now_iso())
    use_telegram_invoice = settings.payment_mode == "telegram" and bool(settings.tg_payment_token)

    tier = str(session.get("tier") or session.get("offer") or "standard").strip().lower()
    is_instant = is_instant_paid_product(tier)

    if use_telegram_invoice:
        update_submission_status(
            submission,
            intake_status="awaiting_payment",
            now_iso=utc_now_iso(),
            payment_status="awaiting_payment",
        )
        save_submission_state(settings.submissions_dir, submission)
        await notify_admins_payment_handoff(submission)

        payment_context = submission["payment_context"]
        prices = [
            LabeledPrice(
                label=payment_context.get("offer_name") or "Нутрициологический разбор",
                amount=int(payment_context.get("amount_kop") or PREMIUM_PRICE_KOPECKS),
            )
        ]
        try:
            await bot.send_invoice(
                message.chat.id,
                title=payment_context.get("invoice_title") or "Нутрициологический разбор",
                description=payment_context.get("invoice_description") or "Персональная нутрициологическая навигация в Telegram.",
                provider_token=settings.tg_payment_token,
                currency="RUB",
                prices=prices,
                payload=submission["payment_context"]["invoice_payload"],
            )
        except Exception as exc:
            logger.exception("Failed to send invoice for %s", session["submission_id"])
            update_submission_status(
                submission,
                intake_status="payment_invoice_failed",
                now_iso=utc_now_iso(),
                payment_status="invoice_failed",
            )
            submission["payment_error"] = str(exc)[:500]
            save_submission_state(settings.submissions_dir, submission)
            await notify_admins(submission, draft_text=None)
            if is_instant:
                await message.answer(
                    "Заявка создана, но сейчас не удалось открыть оплату автоматически. "
                    "Команда получила ваш запрос и свяжется с вами здесь, в Telegram."
                )
            else:
                await message.answer(
                    "Анкета сохранена, но сейчас не удалось открыть оплату автоматически. "
                    "Команда получила ваш кейс и свяжется с вами здесь, в Telegram."
                )
            return
        if is_instant:
            await message.answer(
                "Заявка успешно создана. Для начала программы оплатите её, "
                "нажав на кнопку выше. После оплаты доступ будет открыт автоматически."
            )
        else:
            await message.answer(
                "Анкета успешно собрана. Для старта выбранного разбора оплатите его, "
                "нажав на кнопку выше. После оплаты нейросеть сразу приступит к работе."
            )
        return

    mark_manual_payment_pending(
        submission,
        now_iso=utc_now_iso(),
        reason=(
            "manual_payment_mode"
            if settings.payment_mode == "manual"
            else "payment_provider_not_configured"
        ),
    )
    submission["manual_handoff_started_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, submission)
    await notify_admins_manual_handoff(submission)
    
    client_pay_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить оплату (я оплатил/а)",
                    callback_data=f"clientconfirmpay_{submission['submission_id']}",
                )
            ]
        ]
    )

    if is_instant:
        await message.answer(MANUAL_HANDOFF_INSTANT_START_TEXT, reply_markup=client_pay_markup)
    else:
        await message.answer(MANUAL_HANDOFF_START_TEXT, reply_markup=client_pay_markup)


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    submission_id, payload_user_id = parse_invoice_payload(pre_checkout_query.invoice_payload)
    if not submission_id or payload_user_id is None:
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Не удалось проверить счет. Попробуйте запустить оплату заново.",
        )
        return

    submission = load_submission(settings.submissions_dir, submission_id)
    if submission is None:
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Кейс для оплаты не найден. Напишите администратору.",
        )
        return

    error = validate_payment_event(
        submission,
        telegram_user_id=pre_checkout_query.from_user.id,
        invoice_payload=pre_checkout_query.invoice_payload,
        currency=pre_checkout_query.currency,
        total_amount=pre_checkout_query.total_amount,
    )
    if error:
        logger.warning("Pre-checkout validation failed for %s: %s", submission_id, error)
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Проверка оплаты не пройдена. Попробуйте заново или напишите администратору.",
        )
        return

    current_payment_status = str(submission.get("payment_status") or "")
    if current_payment_status == "paid":
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Этот кейс уже оплачен. Если есть вопрос, напишите администратору.",
        )
        return

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message) -> None:
    payment = message.successful_payment
    submission_id, payload_user_id = parse_invoice_payload(payment.invoice_payload if payment else None)
    session = get_session(message.from_user.id)

    if not submission_id:
        await message.answer("Оплата получена, но ID кейса не найден. Напишите администратору.")
        return

    submission = load_submission(settings.submissions_dir, submission_id)
    if submission is None:
        await message.answer("Оплата получена, но кейс не найден. Напишите администратору.")
        return

    if not payment:
        await message.answer("Оплата получена, но событие оплаты пустое. Напишите администратору.")
        return

    error = validate_payment_event(
        submission,
        telegram_user_id=message.from_user.id,
        invoice_payload=payment.invoice_payload,
        currency=payment.currency,
        total_amount=payment.total_amount,
    )
    if error:
        logger.warning("Payment validation failed for %s: %s", submission_id, error)
        submission["payment_error"] = error
        submission["payment_validation_failed_at"] = utc_now_iso()
        save_submission_state(settings.submissions_dir, submission)
        await message.answer(
            "Оплата получена, но автоматическая проверка кейса не пройдена. "
            "Команда уже увидит это и свяжется с вами здесь, в Telegram."
        )
        return

    current_payment_status = str(submission.get("payment_status") or "")
    if current_payment_status == "paid":
        await message.answer("Этот кейс уже отмечен как оплаченный. Продолжаем работу по нему.")
        return
    if current_payment_status not in {"awaiting_payment", "invoice_failed", "payment_received"}:
        submission["payment_warning"] = (
            f"Unexpected payment status transition from {current_payment_status or 'empty'}"
        )

    update_submission_status(
        submission,
        intake_status="payment_received",
        now_iso=utc_now_iso(),
        payment_status="paid",
    )
    submission["payment_received_at"] = utc_now_iso()
    if payment:
        submission["payment_event"] = {
            "currency": payment.currency,
            "total_amount": payment.total_amount,
            "telegram_payment_charge_id": payment.telegram_payment_charge_id,
            "provider_payment_charge_id": payment.provider_payment_charge_id,
            "payload_user_id": payload_user_id,
        }
    save_submission_state(settings.submissions_dir, submission)

    if not session:
        session = build_session_from_submission(submission, message.from_user)
        user_sessions[message.from_user.id] = session
        touch_session()

    tier = str(submission.get("offer") or session.get("tier") or session.get("offer") or "standard").strip().lower()
    if is_instant_paid_product(tier):
        session["tier"] = tier
        session["offer"] = tier
        await activate_paid_product(message.chat.id, session)
        return

    await message.answer("✅ Оплата успешно получена. Запускаю сборку персонального разбора.")
    await build_dossier_after_payment(message, session)


async def build_dossier_after_payment(
    message: types.Message | None,
    session: dict[str, Any],
    *,
    progress_chat_id: int | None = None,
    client_chat_id: int | None = None,
) -> None:
    submission = load_submission(settings.submissions_dir, session["submission_id"]) or build_submission_payload(session)
    submission_path = settings.submissions_dir / f"{session['submission_id']}.json"
    progress_chat_id = progress_chat_id or (message.chat.id if message else session.get("telegram_user_id"))
    client_chat_id = client_chat_id or session.get("telegram_user_id")

    if not is_payment_confirmed_for_dossier(submission):
        logger.warning(
            "Blocked dossier generation without confirmed payment for %s",
            session["submission_id"],
        )
        if progress_chat_id:
            await bot.send_message(
                progress_chat_id,
                "Генерация досье пока не может стартовать автоматически: оплата ещё не подтверждена в кейсе. "
                "Если вы уже оплатили, команда проверит это вручную и продолжит работу.",
            )
        return

    update_submission_status(submission, intake_status="dossier_generation_in_progress", now_iso=utc_now_iso())
    submission["generation_started_at"] = utc_now_iso()
    save_submission_state(settings.submissions_dir, submission)
    
    start_msg = await bot.send_message(progress_chat_id, "Мы приступаем к сборке вашего кейса. Это займёт некоторое время...")

    draft_text: str | None = None
    judge_report_text: str | None = None
    growth_report_text: str | None = None
    review_signals: dict[str, Any] = {
        "judge_verdict": None,
        "market_verdict": None,
        "needs_quality_rework": False,
        "needs_market_rework": False,
        "review_flags": [],
    }
    tier = submission.get("offer") or session.get("tier")
    
    loading_task = await send_loading_status(progress_chat_id)
    
    try:
        if settings.llm_provider != "disabled" and settings.llm_api_key and settings.llm_model:
            try:
                draft_text = await asyncio.wait_for(
                    asyncio.to_thread(generate_case_draft, settings, submission, tier=tier),
                    timeout=120,
                )
            except Exception:
                logger.exception("AI drafting failed for %s", session["submission_id"])
    
        if draft_text:
            try:
                draft_payload = normalize_dossier_pdf_data(json.loads(strip_json_code_fences(draft_text)), submission=submission)
                draft_payload = apply_safe_action_floor(draft_payload, submission)
                draft_text = json.dumps(draft_payload, ensure_ascii=False, indent=2)
            except Exception:
                logger.exception("Failed to apply safe action floor before review for %s", session["submission_id"])

            draft_path = save_draft(settings.drafts_dir, session["submission_id"], draft_text)
            submission["draft_path"] = str(draft_path)

            # Direct-to-client mode: no internal judge/growth review blocks delivery.
            judge_report_text = None
            growth_report_text = None
            review_signals = {
                "judge_verdict": "direct_delivery",
                "market_verdict": "direct_delivery",
                "needs_quality_rework": False,
                "needs_market_rework": False,
                "review_flags": [],
            }
            # [OBSIDIAN SYNC] Automatically export the draft to the expert's Second Brain
            await asyncio.to_thread(export_to_obsidian, session, draft_text)
            
            # Generation of Premium PDF from strictly structured JSON
            try:
                import re
                clean_json_str = strip_json_code_fences(draft_text)
                
                pdf_data = apply_safe_action_floor(
                    normalize_dossier_pdf_data(json.loads(clean_json_str), submission=submission),
                    submission,
                )
                
                # Normalize list-like fields for the template
                list_fields = [
                    "working_hypotheses", "support_priorities", "diet_strategy", 
                    "lifestyle", "additional_control"
                ]
                for field in list_fields:
                    val = pdf_data.get(field, [])
                    if isinstance(val, str):
                        pdf_data[field] = [line.strip() for line in val.split('\n') if line.strip()]
                    elif not isinstance(val, list):
                        pdf_data[field] = [str(val)]
                
                offer_code = submission.get("offer") or submission.get("tier")
                prefix = get_product_filename_prefix(offer_code)
                pdf_filename = f"{prefix}_{session['submission_id']}.pdf"
                pdf_path = settings.drafts_dir / pdf_filename
                
                # Run playwright pdf generation in thread pool
                await asyncio.to_thread(create_premium_pdf, pdf_data, str(pdf_path))
                submission["pdf_path"] = str(pdf_path)
            except Exception as e:
                logger.exception("Failed to render Premium PDF. Check JSON formatting.")
            
        if submission.get("pdf_path") or draft_text:
            update_submission_status(submission, intake_status="ready_for_direct_delivery", now_iso=utc_now_iso())
        else:
            update_submission_status(submission, intake_status="generation_failed_no_result", now_iso=utc_now_iso())
        submission["generation_finished_at"] = utc_now_iso()
        save_submission_state(settings.submissions_dir, submission)
    finally:
        loading_task.cancel()
        try:
            await bot.delete_message(chat_id=progress_chat_id, message_id=start_msg.message_id)
        except:
            pass

    logger.info("Saved submission %s to %s", session["submission_id"], submission_path)

    delivered = False
    if client_chat_id and submission.get("pdf_path") and Path(str(submission["pdf_path"])).exists():
        from aiogram.types import FSInputFile
        pdf_doc = FSInputFile(str(submission["pdf_path"]))
        await bot.send_document(
            client_chat_id,
            document=pdf_doc,
            caption=(
                "Ваш персональный нутрициологический разбор готов.\n\n"
                "Это не диагноз и не замена врачу. Используйте документ как навигацию: что видно по питанию, привычкам, анализам/жалобам, "
                "какие вопросы обсудить со специалистом и какие шаги можно начать безопасно."
            ),
        )
        delivered = True
    elif client_chat_id and draft_text:
        await bot.send_message(
            client_chat_id,
            "Ваш персональный нутрициологический разбор готов. PDF сейчас не собрался, поэтому отправляю результат текстом."
        )
        for chunk in split_telegram_text(draft_text):
            await bot.send_message(client_chat_id, chunk)
        delivered = True

    if delivered:
        update_submission_status(submission, intake_status="delivered_to_client", now_iso=utc_now_iso())
        submission["delivered_at"] = utc_now_iso()
        submission["direct_delivery"] = True
        save_submission_state(settings.submissions_dir, submission)
        clear_session(int(session["telegram_user_id"]))
        return

    if client_chat_id:
        await bot.send_message(
            client_chat_id,
            "Не удалось автоматически собрать результат. Данные сохранены, команда увидит ошибку и вернётся к вам здесь."
        )
    await notify_admins(submission, draft_text, judge_report_text, growth_report_text)

@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    clear_session(message.from_user.id)
    reset_chat_session(message.from_user.id)
    await message.answer(START_TEXT, reply_markup=main_menu_keyboard(), parse_mode="HTML")


@dp.message(Command("reset"))
async def cmd_reset(message: types.Message) -> None:
    clear_session(message.from_user.id)
    reset_chat_session(message.from_user.id)
    await message.answer(START_TEXT, reply_markup=main_menu_keyboard(), parse_mode="HTML")


@dp.message(Command("queue"))
async def cmd_queue(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    recent_cases = list_recent_cases(settings.submissions_dir, limit=5)
    if not recent_cases:
        await message.answer("Очередь пока пустая.")
        return

    lines = ["📋 Очередь кейсов:"]
    for case in recent_cases:
        profile = case.get("profile", {})
        medical = case.get("medical_context", {})
        intake_status = case.get("intake_status")

        if intake_status == "awaiting_payment":
            status = "💳 Ожидает оплаты"
        elif intake_status == "payment_received":
            status = "✅ Оплата получена"
        elif intake_status == "dossier_generation_in_progress":
            status = "⚙️ Генерация досье"
        elif intake_status in {"awaiting_human_review", "draft_ready_human_review"}:
            status = "📄 Готов PDF (ждём аппрува)" if case.get("pdf_path") else "✍️ Только драфт"
        elif intake_status == "review_priority_quality_rework":
            status = "🛠️ Нужна доработка качества"
        elif intake_status == "review_priority_market_rework":
            status = "📈 Нужна доработка ценности/рынка"
        elif intake_status == "review_priority_quality_and_market":
            status = "🚧 Нужна доработка качества и оффера"
        elif intake_status == "draft_requires_edits":
            status = "✏️ Требуются правки"
        elif intake_status == "awaiting_manual_review_no_draft":
            status = "🧩 Нужен ручной разбор"
        elif intake_status == PAYMENT_STATUS_MANUAL_PENDING:
            status = "🟡 Ждём ручного подтверждения оплаты"
        elif intake_status == "manual_payment_confirmed":
            status = "✅ Ручная оплата подтверждена"
        elif intake_status == "manual_handoff_no_provider":
            status = "🟡 Ручной handoff legacy"
        elif intake_status == "payment_skipped_no_provider":
            status = "🟡 Без оплаты (legacy)"
        elif intake_status == "payment_invoice_failed":
            status = "🚨 Ошибка оплаты (нужен ручной контакт)"
        elif intake_status == "delivered_to_client":
            status = "✅ Доставлено клиенту"
        elif case.get("pdf_path"):
            status = "📄 Готов PDF (ждём аппрува)"
        elif case.get("draft_path"):
            status = "✍️ Только драфт"
        else:
            status = "⏳ В обработке"
             
        lines.append(
            f"1. <code>{case.get('submission_id')}</code>\n"
            f"  👤 {profile.get('full_name') or profile.get('telegram_full_name')}\n"
            f"  🚩 {status}\n"
        )
    await message.answer("\n".join(lines), parse_mode="HTML")


@dp.message(Command("health"))
async def cmd_health(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    submission_count = len(list(settings.submissions_dir.glob("*.json")))
    draft_count = len(list(settings.drafts_dir.glob("*.md")))
    upload_case_count = len([path for path in settings.uploads_dir.glob("*") if path.is_dir()])
    product_insights = load_product_insights(settings.product_insights_path)
    product_insight_case_count = len(product_insights.get("cases") or {})
    product_governance = load_product_governance(settings.product_governance_path)
    experiment_count = len(product_governance.get("experiments") or [])
    decision_count = len(product_governance.get("decisions") or [])
    lines = [
        "Bot runtime health:",
        f"- Proxy: {_format_proxy_for_logs(settings.bot_proxy_url) if settings.bot_proxy_url else 'disabled'}",
        f"- LLM provider: {settings.llm_provider}",
        f"- LLM mode: {settings.llm_api_mode}",
        f"- Submissions: {submission_count}",
        f"- Drafts: {draft_count}",
        f"- Upload folders: {upload_case_count}",
        f"- Product insights cases: {product_insight_case_count}",
        f"- Governance experiments: {experiment_count}",
        f"- Governance decisions: {decision_count}",
    ]
    await message.answer("\n".join(lines))


@dp.message(Command("insights"))
async def cmd_insights(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    payload = load_product_insights(settings.product_insights_path)
    await message.answer(format_product_insights_summary(payload))


@dp.message(Command("governance"))
async def cmd_governance(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_governance_summary(governance))


@dp.message(Command("experiments"))
async def cmd_experiments(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_experiments_dashboard(governance))


@dp.message(Command("decisions"))
async def cmd_decisions(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_decisions_dashboard(governance))


@dp.message(Command("gaps"))
async def cmd_gaps(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_execution_gaps(governance, limit=10))


@dp.message(Command("learnings"))
async def cmd_learnings(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_experiment_outcome_memory(governance))


@dp.message(Command("decide"))
async def cmd_decide(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    raw_text = (message.text or "").strip()
    parts = raw_text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.answer("Использование: /decide <решение или зафиксированный вывод>")
        return

    decision = record_product_decision(parts[1].strip())
    await message.answer(
        f"Решение зафиксировано: {decision['id']}\n"
        f"{decision['title']}\n\n"
        "Следующий шаг: /decisionplan <DEC-id> <owner> | <deadline> | <KPI>"
    )


@dp.message(Command("expstatus"))
async def cmd_expstatus(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    raw_text = (message.text or "").strip()
    parts = raw_text.split(maxsplit=3)
    if len(parts) < 3:
        await message.answer(
            "Использование: /expstatus <EXP-id> <proposed|active|validated|rejected> [заметка]"
        )
        return

    experiment_id = parts[1].strip()
    new_status = parts[2].strip().lower()
    note = parts[3].strip() if len(parts) > 3 else ""

    if new_status not in GOVERNANCE_EXPERIMENT_STATUSES:
        await message.answer("Допустимые статусы: proposed, active, validated, rejected")
        return

    experiment = update_experiment_status(experiment_id, new_status, note=note)
    if not experiment:
        await message.answer("Эксперимент не найден.")
        return

    await message.answer(
        f"Эксперимент обновлен: {experiment['id']}\nСтатус: {experiment['status']}\n{experiment['title']}"
    )


@dp.message(Command("review"))
async def cmd_review(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    recent_cases = list_recent_cases(settings.submissions_dir, limit=20)
    priority_cases = [
        case
        for case in recent_cases
        if case.get("internal_review", {}).get("review_flags")
        or case.get("intake_status")
        in {
            "review_priority_quality_rework",
            "review_priority_market_rework",
            "review_priority_quality_and_market",
        }
    ]
    source_cases = priority_cases or recent_cases
    await message.answer(format_review_dashboard(source_cases))


@dp.message(Command("weekly"))
async def cmd_weekly(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    payload = load_product_insights(settings.product_insights_path)
    weekly_text = format_windowed_product_summary(payload, days=7)
    monthly_text = format_windowed_product_summary(payload, days=30)
    await message.answer(f"{weekly_text}\n\n{monthly_text}")


@dp.message(Command("brief"))
async def cmd_brief(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    payload = load_product_insights(settings.product_insights_path)
    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_action_priority_brief(payload, governance, days=7))


@dp.message(Command("suggestdecisions"))
async def cmd_suggest_decisions(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    payload = load_product_insights(settings.product_insights_path)
    governance = load_product_governance(settings.product_governance_path)
    await message.answer(format_suggested_decisions(payload, governance, days=7))


@dp.message(Command("applydecision"))
async def cmd_apply_decision(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    raw_text = (message.text or "").strip()
    parts = raw_text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.answer("Использование: /applydecision <номер из /suggestdecisions>")
        return

    suggestion_number = int(parts[1].strip())
    payload = load_product_insights(settings.product_insights_path)
    governance = load_product_governance(settings.product_governance_path)
    decision, error = apply_suggested_decision(payload, governance, suggestion_number, days=7)
    if error:
        await message.answer(error)
        return

    await message.answer(
        f"Решение применено: {decision['id']}\n"
        f"{decision['title']}\n\n"
        "Следующий шаг: задай owner, deadline и KPI через /decisionplan <DEC-id> <owner> | <deadline> | <KPI>"
    )


@dp.message(Command("decisionplan"))
async def cmd_decision_plan(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    raw_text = (message.text or "").strip()
    decision_id, owner, deadline, kpi = parse_decision_plan_command(raw_text)
    if not decision_id:
        await message.answer(
            "Использование: /decisionplan <DEC-id> <owner> | <deadline> | <KPI>"
        )
        return
    if owner is None or deadline is None or kpi is None:
        await message.answer(
            "Заполни все 3 поля через вертикальную черту: /decisionplan <DEC-id> <owner> | <deadline> | <KPI>"
        )
        return

    decision = update_decision_execution(
        decision_id,
        owner=owner,
        deadline=deadline,
        kpi=kpi,
    )
    if not decision:
        await message.answer(f"Решение {decision_id} не найдено.")
        return

    await message.answer(
        f"Execution-план обновлен для {decision['id']}:\n"
        f"Owner: {decision.get('owner') or 'n/a'}\n"
        f"Deadline: {decision.get('deadline') or 'n/a'}\n"
        f"KPI: {decision.get('kpi') or 'n/a'}\n\n"
        "Команда: /decisions покажет обновленный decision log."
    )


@dp.message(Command("digestnow"))
async def cmd_digest_now(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только для админов.")
        return

    payload = load_product_insights(settings.product_insights_path)
    if not (payload.get("cases") or {}):
        await message.answer("Для дайджеста пока недостаточно накопленных данных.")
        return

    await message.answer(build_admin_digest_text(payload))


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


async def notify_admins_habits_log(user_id: int, full_name: str, text: str, photo_file_id: str | None = None) -> None:
    if not settings.admin_chat_ids:
        return

    caption = (
        f"🥗 <b>Новый отчет по тарифу «Привычки и тарелка»</b>\n\n"
        f"👤 Клиент: {full_name} (ID: {user_id})\n\n"
        f"📝 Сообщение: {text}"
    )

    for admin_chat_id in settings.admin_chat_ids:
        try:
            if photo_file_id:
                # Telegram captions are capped at 1024 characters
                await bot.send_photo(
                    admin_chat_id,
                    photo=photo_file_id,
                    caption=caption[:1020],
                    parse_mode="HTML"
                )
            else:
                await bot.send_message(
                    admin_chat_id,
                    caption[:4000],
                    parse_mode="HTML"
                )
        except Exception:
            logger.exception("Failed to notify admin of habits log for user %s", user_id)


# Handler to route admin replies back to clients in Habits or live support mode
@dp.message(lambda message: is_admin(message.from_user.id) and message.reply_to_message is not None)
async def handle_admin_reply_to_client(message: types.Message) -> None:
    replied = message.reply_to_message
    text_to_search = (replied.text or replied.caption or "")
    
    import re
    match = re.search(r"\(ID:\s*(\d+)\)", text_to_search)
    if not match:
        return

    try:
        client_user_id = int(match.group(1))
    except (ValueError, TypeError):
        return

    try:
        await bot.copy_message(
            chat_id=client_user_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.reply(f"✅ Ответ успешно отправлен клиенту (ID: {client_user_id}).")
    except Exception as exc:
        logger.exception("Failed to forward admin reply to client %s", client_user_id)
        await message.reply(f"❌ Не удалось отправить ответ клиенту: {exc}")


def build_habits_daily_report(text: str, *, has_photo: bool = False) -> str:
    lower = text.lower()
    positives = []
    improvements = []
    if has_photo or any(word in lower for word in ("завтрак", "обед", "ужин", "перекус")):
        positives.append("вы зафиксировали питание — уже есть материал для наблюдения")
    if any(word in lower for word in ("белок", "яй", "рыб", "творог", "мяс", "кур", "боб")):
        positives.append("в описании есть источник белка")
    else:
        improvements.append("проверить, был ли белок в каждом основном приёме пищи")
    if any(word in lower for word in ("овощ", "зелень", "ягод", "клетчат", "салат")):
        positives.append("есть опора на клетчатку/овощи")
    else:
        improvements.append("добавить овощи, зелень или другой источник клетчатки")
    if "коф" in lower:
        improvements.append("посмотреть время кофе: лучше не натощак и не поздно вечером")
    if any(word in lower for word in ("слад", "печен", "конфет", "булк")):
        improvements.append("отследить тягу к сладкому и связь с белком, сном и стрессом")
    if any(word in lower for word in ("сон", "стресс", "энерг", "отек", "отёк", "стул", "вздут")):
        positives.append("вы отметили самочувствие — это поможет увидеть связь привычек и состояния")

    positives_text = "; ".join(positives[:2]) if positives else "вы сделали первый шаг и прислали данные"
    improvements_text = "; ".join(improvements[:3]) if improvements else "сохранить регулярность и завтра снова прислать питание + самочувствие"
    return (
        "Короткий отчёт за сегодня:\n\n"
        f"1. Что получилось хорошо: {positives_text}.\n"
        f"2. Что можно улучшить: {improvements_text}.\n"
        "3. Главная точка внимания: белок в первой половине дня, клетчатка и время кофе.\n"
        "4. Связь питания и самочувствия: завтра отметьте энергию, тягу к сладкому, отёки, сон и ЖКТ.\n"
        "5. Фокус на завтра: прислать завтрак/обед/ужин, воду, кофе, сон и стресс по шкале 1-10.\n"
        "6. Поддержка: не ищем идеальную диету, ищем повторяющиеся закономерности и мягко их корректируем."
    )


def osipov_context_prompt() -> str:
    return (
        "🧬 Разбор ХМС/ГХ-МС по Осипову\n\n"
        "Напишите коротко контекст перед файлом:\n"
        "1. основные жалобы по ЖКТ;\n"
        "1. стул, вздутие, боли;\n"
        "1. питание, сладкое, молочные продукты, переносимость клетчатки;\n"
        "1. хронические заболевания ЖКТ, удалён ли желчный пузырь;\n"
        "1. лекарства, добавки, аллергии;\n"
        "1. беременность/ГВ, если актуально.\n\n"
        "После этого пришлите PDF или фото анализа."
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("tier_"))
async def process_tier_selection(callback_query: types.CallbackQuery) -> None:
    tier = callback_query.data.replace("tier_", "")
    if tier not in TIER_NAMES:
        tier = "standard"

    user_id = callback_query.from_user.id
    reset_chat_session(user_id)

    session = start_session(callback_query.from_user, tier=tier)
    if tier == "nutri_chat":
        session["product_mode"] = "nutri_chat"
    if tier == "habits":
        session["product_mode"] = "daily_habits"
    elif tier == "standard":
        session["product_mode"] = "standard_no_labs"
    elif tier == "premium":
        session["product_mode"] = "premium_labs"
    elif tier == "osipov":
        session["product_mode"] = "osipov"

    await bot.send_message(user_id, TIER_DESCRIPTIONS.get(tier, TIER_DESCRIPTIONS["standard"]), parse_mode="HTML")
    await bot.send_message(user_id, CONSENT_TEXT, reply_markup=consent_keyboard())
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(lambda c: c.data == "choose_product")
async def process_choose_product(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, PRODUCT_MENU_TEXT, reply_markup=product_keyboard(), parse_mode="HTML")
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "show_labs_link")
async def process_show_labs_link(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, LABS_GUIDANCE_TEXT)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(lambda c: c.data == "show_process")
async def process_show_process(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, ABOUT_TEXT)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "show_examples")
async def process_show_examples(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, PRODUCT_EXAMPLES_TEXT, reply_markup=product_keyboard())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "operator_help")
async def process_operator_help(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, OPERATOR_HELP_TEXT)
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
    session = get_session(callback_query.from_user.id) or start_session(callback_query.from_user, tier="standard")
    session["consent_given"] = True
    tier = str(session.get("tier") or session.get("offer") or "standard")

    await bot.send_message(callback_query.from_user.id, "Спасибо. Согласие зафиксировано.")

    if tier == "screening":
        session["step"] = "awaiting_screening_symptoms"
        touch_session()
        await bot.send_message(
            callback_query.from_user.id,
            "Пожалуйста, опишите своими словами 1-3 симптома или жалобы, которые вас беспокоят "
            "(например: <i>«постоянная усталость по утрам, выпадение волос, вздутие после еды»</i>).",
            parse_mode="HTML"
        )
    elif is_instant_paid_product(tier):
        session["step"] = "awaiting_product_payment"
        touch_session()
        await finalize_submission(callback_query.message, session)
    else:
        session["step"] = "full_name"
        touch_session()
        await send_step_prompt(callback_query.from_user.id, session["step"])

    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(lambda c: c.data == "consent_no")
async def process_consent_no(callback_query: types.CallbackQuery) -> None:
    clear_session(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, CONSENT_DECLINED_TEXT, reply_markup=main_menu_keyboard())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "manual_labs_help")
async def process_manual_labs_help(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id)
    if not session or session.get("step") != "lab_notes":
        await bot.answer_callback_query(callback_query.id, text="Сначала начните разбор заново через /start", show_alert=True)
        return

    await callback_query.message.answer(
        "Напишите текстом: какие анализы сдавали, дату, основные показатели и их значения. "
        "Можно также прикрепить фото/PDF бланка."
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(lambda c: c.data == "skip_labs")
async def process_skip_labs(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id)
    if not session or session.get("step") != "lab_notes":
        await bot.answer_callback_query(callback_query.id, text="Сначала начните intake заново через /start", show_alert=True)
        return

    session["lab_notes"] = session.get("lab_notes") or "Клиент пропустил ввод анализов."
    session["step"] = "red_flags"
    touch_session()
    await send_step_prompt(callback_query.message.chat.id, "red_flags")
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "labs_done")
async def process_labs_done(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id)
    if not session or session.get("step") != "lab_notes":
        await bot.answer_callback_query(callback_query.id, text="Сначала начните intake заново через /start", show_alert=True)
        return

    session["contact"] = "telegram_current_chat"
    session["step"] = "red_flags"
    touch_session()
    await send_step_prompt(callback_query.message.chat.id, "red_flags")
    await bot.answer_callback_query(callback_query.id)


@dp.message(lambda message: message.document is not None)
async def handle_document_upload(message: types.Message) -> None:
    if await check_and_prompt_pending_payment(message):
        return
    session = get_session(message.from_user.id)
    if session and session.get("step") == "osipov_upload":
        upload_dir = case_upload_dir(settings.uploads_dir, session["submission_id"]) / "osipov"
        upload_dir.mkdir(parents=True, exist_ok=True)
        original_name = message.document.file_name or "osipov_analysis.pdf"
        file_name = sanitize_filename(f"{utc_now_iso().replace(':', '').replace('-', '')}_{original_name}")
        destination = upload_dir / file_name
        await bot.download(message.document, destination=destination)
        session.setdefault("documents", []).append({"kind": "osipov_document", "file_name": file_name, "stored_path": str(destination)})
        session["step"] = "done"
        touch_session()
        await message.answer("Анализ Осипова принят. Я сохраню его как отдельный платный блок и подготовлю разбор: микробные маркеры, связь с жалобами, что требует врача и план нутрициологической поддержки.")
        return
    if not session or session.get("step") != "lab_notes":
        followup_case = find_active_followup_case(message.from_user.id)
        if followup_case:
            upload_dir = case_upload_dir(settings.uploads_dir, followup_case["submission_id"]) / "followup"
            upload_dir.mkdir(parents=True, exist_ok=True)
            original_name = message.document.file_name or "followup_document.pdf"
            file_name = sanitize_filename(f"{utc_now_iso().replace(':', '').replace('-', '')}_{original_name}")
            destination = upload_dir / file_name
            await bot.download(message.document, destination=destination)
            append_case_followup(
                followup_case,
                {
                    "kind": "document",
                    "file_name": original_name,
                    "stored_path": str(destination),
                    "mime_type": message.document.mime_type,
                    "note": "Uploaded during 30-day follow-up.",
                },
            )
            await message.answer(
                "Файл принят в сопровождение 30 дней. Я сохраню его к вашему кейсу.\n\n"
                "Если это анализы — я проверю читаемость и не буду делать выводы по сомнительным цифрам. "
                "Если это УЗИ, выписка из стационара, заключение специалиста или другой документ за последние 6 месяцев — "
                "напишите одним сообщением, какой вопрос по нему главный."
            )
            asyncio.create_task(process_ocr_background(build_session_from_submission(followup_case, message.from_user), destination, settings))
            return
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
    
    # [OCR TRIGGER] Background task for laboratory recognition
    asyncio.create_task(process_ocr_background(session, destination, settings))
    
    touch_session()
    await message.answer(
        "Файл сохранён. Если есть ещё документы или фото анализов — отправляйте. "
        "Когда закончите, напишите текстом: какие показатели/анализы сдавали и что показали, "
        "или просто напишите `готово` чтобы перейти дальше.",
    )


@dp.message(lambda message: bool(message.photo))
async def handle_photo_upload(message: types.Message) -> None:
    if await check_and_prompt_pending_payment(message):
        return
    session = get_session(message.from_user.id)
    if session and session.get("step") == "paid_nutri_chat":
        await message.answer("В Нутри-чате я работаю с текстовыми вопросами. Если хотите разбор фото тарелок, выберите тариф «Привычки и тарелка».")
        return
    if session and session.get("step") == "habits_daily_log":
        upload_dir = case_upload_dir(settings.uploads_dir, session["submission_id"]) / "plates"
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_name = sanitize_filename(f"{utc_now_iso().replace(':', '').replace('-', '')}_plate.jpg")
        destination = upload_dir / file_name
        await bot.download(message.photo[-1], destination=destination)
        caption = (message.caption or "Фото тарелки без подписи.").strip()
        session.setdefault("daily_logs", []).append({"created_at": utc_now_iso(), "kind": "plate_photo", "caption": caption, "stored_path": str(destination)})
        touch_session()
        await message.answer(build_habits_daily_report(caption, has_photo=True))
        
        # Forward the meal photo report to curators/admins
        full_name = session.get("full_name") or message.from_user.full_name or "Клиент"
        photo_file_id = message.photo[-1].file_id
        await notify_admins_habits_log(message.from_user.id, full_name, caption, photo_file_id)
        return
    if session and session.get("step") == "osipov_upload":
        upload_dir = case_upload_dir(settings.uploads_dir, session["submission_id"]) / "osipov"
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_name = sanitize_filename(f"{utc_now_iso().replace(':', '').replace('-', '')}_osipov_photo.jpg")
        destination = upload_dir / file_name
        await bot.download(message.photo[-1], destination=destination)
        session.setdefault("documents", []).append({"kind": "osipov_photo", "file_name": file_name, "stored_path": str(destination)})
        session["step"] = "done"
        touch_session()
        await message.answer("Фото анализа Осипова принято. Если цифры читаются плохо, я попрошу прислать PDF или более чёткое фото. Разбор будет оформлен как отдельный блок без диагнозов и без назначения лекарств.")
        return
    if not session or session.get("step") != "lab_notes":
        followup_case = find_active_followup_case(message.from_user.id)
        if followup_case:
            upload_dir = case_upload_dir(settings.uploads_dir, followup_case["submission_id"]) / "followup"
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_name = sanitize_filename(f"{utc_now_iso().replace(':', '').replace('-', '')}_followup_photo.jpg")
            destination = upload_dir / file_name
            await bot.download(message.photo[-1], destination=destination)
            caption = (message.caption or "").strip()
            append_case_followup(
                followup_case,
                {
                    "kind": "photo",
                    "caption": caption,
                    "stored_path": str(destination),
                    "note": "Uploaded during 30-day follow-up.",
                },
            )
            lower_caption = caption.lower()
            followup_session = build_session_from_submission(followup_case, message.from_user)
            if any(k in lower_caption for k in ["пятно", "кожа", "сып", "язык", "глаза", "лицо", "визуал", "родин"]):
                asyncio.create_task(process_vision_background(followup_session, destination, settings))
                await message.answer(
                    "Фото принято в сопровождение. Я могу помочь описать видимые признаки и срочность маршрута, "
                    "но не ставлю диагноз по фото.\n\n"
                    "Пожалуйста, допишите: где находится, как давно, меняется ли размер/цвет, есть ли боль, зуд, температура или кровоточивость."
                )
            else:
                asyncio.create_task(process_ocr_background(followup_session, destination, settings))
                await message.answer(
                    "Фото принято в сопровождение. Если это анализ — проверю читаемость. "
                    "Если это фото жалобы, подпишите: где находится, как давно и что беспокоит."
                )
            return
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
    
    # [VISION/OCR TRIGGER] Decide whether it's a lab result or physical photo
    # We can ask or try to detect. For simplicity, we run both or use caption detection.
    caption = (message.caption or "").lower()
    if any(k in caption for k in ["язык", "глаза", "лицо", "визуал"]):
        asyncio.create_task(process_vision_background(session, destination, settings))
        msg_text = "Фото принято. Запускаю анализ визуальных признаков. Это часть вашего премиального разбора."
    else:
        asyncio.create_task(process_ocr_background(session, destination, settings))
        msg_text = "Фото сохранено. Анализирую показатели... Можно отправить ещё фото/PDF или нажать кнопку."

    touch_session()
    await message.answer(msg_text)


@dp.message(F.voice)
async def handle_voice(message: types.Message) -> None:
    await message.answer(
        "❌ Голосовые сообщения отключены. Пожалуйста, напишите текстом."
    )





def get_user_approved_reports(user_id: int) -> list[dict[str, Any]]:
    reports = []
    submissions_dir = settings.submissions_dir
    if not submissions_dir.exists():
        return reports
    for path in submissions_dir.glob(f"*_{user_id}.json"):
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            pdf_path = data.get("pdf_path")
            if pdf_path and Path(pdf_path).exists():
                reports.append(data)
        except Exception:
            continue
    reports.sort(key=lambda r: r.get("status_updated_at") or r.get("created_at") or "", reverse=True)
    return reports


@dp.callback_query(lambda c: c.data and c.data.startswith("getpdf_"))
async def process_get_report_pdf(callback_query: types.CallbackQuery) -> None:
    submission_id = callback_query.data.replace("getpdf_", "")
    submission = load_submission(settings.submissions_dir, submission_id)
    if not submission:
        await bot.answer_callback_query(callback_query.id, "Отчет не найден.", show_alert=True)
        return
    pdf_path = submission.get("pdf_path")
    if not pdf_path or not Path(pdf_path).exists():
        await bot.answer_callback_query(callback_query.id, "Файл отчета не найден на сервере.", show_alert=True)
        return
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_chat_action(callback_query.from_user.id, "upload_document")
    from aiogram.types import FSInputFile
    pdf_doc = FSInputFile(pdf_path)
    offer_name = TIER_NAMES.get(submission.get("offer") or submission.get("tier"), "Wellness-Паспорт")
    await bot.send_document(
        callback_query.from_user.id,
        pdf_doc,
        caption=f"Ваш {offer_name} от нутрициолога Зинченко Ольги Викторовны."
    )


@dp.message()
async def handle_message(message: types.Message) -> None:
    if not message.text:
        await message.answer("Для этого шага отправьте текстовое сообщение.")
        return

    if message.text.startswith("/"):
        return

    session = get_session(message.from_user.id)
    text = message.text.strip()

    # --- Persistent Menu Handlers ---
    if text == "🔍 Диагностика симптомов (Бесплатно)":
        clear_session(message.from_user.id)
        reset_chat_session(message.from_user.id)
        session = start_session(message.from_user, tier="screening")
        await message.answer(
            "Рада приветствовать вас в блоке бесплатной экспресс-диагностики!\n\n"
            "Здесь вы можете описать свои симптомы, а я предложу возможные нутрициологические гипотезы и сориентирую по дальнейшим действиям.\n\n"
            f"{CONSENT_TEXT}",
            reply_markup=consent_keyboard(),
            parse_mode="HTML"
        )
        return

    if text == "🛍️ Выбрать программу":
        clear_session(message.from_user.id)
        reset_chat_session(message.from_user.id)
        await message.answer(PRODUCT_MENU_TEXT, reply_markup=product_keyboard(), parse_mode="HTML")
        return

    if text == "📊 Мои отчеты":
        reports = get_user_approved_reports(message.from_user.id)
        if not reports:
            await message.answer(
                "У вас пока нет готовых Wellness-Паспортов или отчетов.\n\n"
                "Чтобы получить персональный отчет, выберите подходящую программу в меню, пройдите анкету и пришлите анализы.",
                reply_markup=main_menu_keyboard()
            )
            return

        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
        inline_keyboard = []
        for r in reports:
            offer_name = TIER_NAMES.get(r.get("offer") or r.get("tier"), "Wellness-Паспорт")
            date_str = ""
            created_at = r.get("created_at")
            if created_at:
                try:
                    date_str = datetime.fromisoformat(created_at.replace("Z", "+00:00")).strftime("%d.%m.%Y")
                except Exception:
                    date_str = created_at[:10]
            btn_text = f"📄 {offer_name} ({date_str})"
            inline_keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=f"getpdf_{r['submission_id']}")])

        markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await message.answer(
            "📎 <b>Ваши готовые отчеты:</b>\n\n"
            "Нажмите на кнопку с датой, чтобы скачать нужный Wellness-Паспорт в формате PDF.",
            reply_markup=markup,
            parse_mode="HTML"
        )
        return

    if text == "📝 Заполнить анкету":
        if await check_and_prompt_pending_payment(message):
            return
        if not session:
            await message.answer(
                "У вас нет активной сессии для заполнения анкеты.\n\n"
                "Пожалуйста, выберите программу в меню, чтобы начать.",
                reply_markup=product_keyboard()
            )
            return

        step = session.get("step")
        if step == "consent":
            await message.answer(CONSENT_TEXT, reply_markup=consent_keyboard())
        elif step == "awaiting_product_payment":
            await message.answer("Ожидаем оплату выбранной программы. Если оплата проведена, ожидайте подтверждения от команды.")
        elif step in INTAKE_STEP_ORDER:
            await message.answer(f"Продолжаем заполнение анкеты.")
            await send_step_prompt(message.chat.id, step)
        else:
            await message.answer("Анкета заполнена или находится на проверке.")
        return

    if text == "🩸 Сдать анализы":
        await message.answer(
            "🩸 <b>Сдача анализов со скидкой</b>\n\n"
            "нутрициолог Зинченко Ольга Викторовна рекомендует не сдавать анализы наугад — это сэкономит ваш бюджет.\n\n"
            "Вы можете заказать анализы со скидкой в удобной лаборатории рядом с вашим домом через наш реферальный кабинет в <b>HelloDoc</b>. "
            "Результаты вы сможете прислать напрямую в этот бот.\n\n"
            "🔗 <a href='https://hellodoc.app/s/27u6a/'>Сдать анализы со скидкой через HelloDoc</a>\n"
            "Резервная ссылка: <a href='https://hellodoc.app/s/gdgjq/'>HelloDoc Резерв</a>",
            parse_mode="HTML"
        )
        return

    if text == "💬 Задать вопрос эксперту":
        await message.answer(OPERATOR_HELP_TEXT)
        return

    if text == "🚨 Красные флаги":
        await message.answer(RED_FLAGS_INFO_TEXT, parse_mode="HTML")
        return

    # Check pending payment before processing any standard messages/inputs
    if await check_and_prompt_pending_payment(message):
        return

    # SCREENING MODE: user sent symptoms after choosing 500 RUB tier
    if session and session.get("step") == "awaiting_screening_symptoms":
        session["screening_symptoms"] = text
        session["step"] = "screening_completed"
        touch_session()
        await bot.send_chat_action(message.chat.id, "typing")
        try:
            reply = await asyncio.to_thread(generate_screening_reply, settings, text)
        except Exception:
            logger.exception("Screening generation failed for user %s", message.from_user.id)
            await message.answer(
                "Не удалось подготовить ответ. Попробуйте ещё раз или напишите «нужен оператор»."
            )
            return

        if reply:
            await message.answer(reply[:TELEGRAM_MESSAGE_SAFE_LIMIT])
        else:
            await message.answer(
                "Не удалось обработать симптомы. Попробуйте описать их более конкретно "
                "или выберите другой формат разбора через /start"
            )
        return

    if session and session.get("step") == "paid_nutri_chat":
        expires_at = parse_utc_iso(session.get("nutri_chat_expires_at"))
        if expires_at and datetime.now(timezone.utc) > expires_at:
            clear_session(message.from_user.id)
            reset_chat_session(message.from_user.id)
            await message.answer(
                "Пробный Нутри-чат на 2 дня завершён. Если хотите продолжить, выберите подходящий тариф ниже.",
                reply_markup=product_keyboard(),
            )
            return
        if settings.llm_provider == "disabled" or not settings.llm_api_key or not settings.llm_model:
            await message.answer("Сейчас AI-ответы временно недоступны. Напишите вопрос позже или обратитесь к оператору.")
            return
        try:
            await bot.send_chat_action(message.chat.id, "typing")
            history = get_chat_history(message.from_user.id)
            nutri_prompt = (
                "Режим оплаченного тарифа Нутри-чат. Отвечай только на русском языке как нутрициологический помощник. "
                "Не ставь диагнозы, не обещай лечение, не отменяй лекарства. Используй формулировки: предварительная нутрициологическая гипотеза, возможная причина, что стоит проверить, что обсудить с врачом. "
                "Структура ответа: 1) кратко понять вопрос, 2) если данных мало - уточнить 1-2 важных детали, 3) объяснить возможную связь с питанием/режимом/ЖКТ/желчеоттоком/сном/стрессом, 4) дать 1-3 практических шага, 5) отметить красные флаги и врача, если актуально.\n\n"
                f"Вопрос клиента: {text}"
            )
            reply = await asyncio.to_thread(generate_live_reply, settings, history, nutri_prompt)
        except Exception:
            logger.exception("Paid nutri-chat response failed for user %s", message.from_user.id)
            await message.answer("Сейчас не удалось подготовить ответ. Попробуйте ещё раз через минуту или напишите оператору.")
            return
        if not reply:
            await message.answer("Не удалось сформировать ответ. Попробуйте переформулировать вопрос чуть конкретнее.")
            return
        append_chat_message(message.from_user.id, "user", text)
        append_chat_message(message.from_user.id, "assistant", reply)
        await message.answer(reply[:TELEGRAM_MESSAGE_SAFE_LIMIT])
        return
    if session and session.get("step") == "habits_daily_log":
        session.setdefault("daily_logs", []).append({"created_at": utc_now_iso(), "text": text})
        touch_session()
        await message.answer(build_habits_daily_report(text))
        
        # Forward the meal text report to curators/admins
        full_name = session.get("full_name") or message.from_user.full_name or "Клиент"
        await notify_admins_habits_log(message.from_user.id, full_name, text)
        return

    if session and session.get("step") == "osipov_context":
        session["osipov_context"] = text
        session["step"] = "osipov_upload"
        touch_session()
        await message.answer(
            "Контекст сохранён. Теперь пришлите PDF или фото анализа ХМС/ГХ-МС по Осипову.\n\n"
            "Я не буду ставить диагноз по анализу, а подготовлю нутрициологическую интерпретацию: микробные маркеры, связь с жалобами, что требует врача и что можно поддержать питанием/ЖКТ/микробиотой."
        )
        return

    if session and session.get("step") == "osipov_upload":
        session["osipov_extra_note"] = text
        touch_session()
        await message.answer(
            "Комментарий сохранён. Пришлите сам анализ PDF или фото. Если файла пока нет, можно вернуться позже в этот чат."
        )
        return
    if not session:
        followup_case = find_active_followup_case(message.from_user.id)
        if followup_case:
            if followup_case.get("lab_confirmation_status") == "pending_client_confirmation":
                if is_lab_confirmation_yes(text):
                    followup_case["lab_confirmation_status"] = "client_confirmed"
                    followup_case["lab_confirmation_needed"] = False
                    followup_case["pending_biomarker_confirmation"] = []
                    followup_case["requires_lab_resubmission"] = False
                    followup_case["enrichment_updated_at"] = utc_now_iso()
                    save_submission_state(settings.submissions_dir, followup_case)
                    await message.answer(
                        "Спасибо, зафиксировала: распознанные показатели подтверждены вами. "
                        "Теперь они будут использоваться в сопровождении как подтверждённые клиентом данные."
                    )
                    return

                medical_context = followup_case.setdefault("medical_context", {})
                current_notes = str(medical_context.get("lab_notes") or "").strip()
                correction_note = f"Клиент не подтвердил OCR и прислал уточнение: {text}"
                medical_context["lab_notes"] = f"{current_notes}\n{correction_note}".strip() if current_notes else correction_note
                followup_case["lab_confirmation_status"] = "client_correction_needed"
                followup_case["lab_confirmation_needed"] = False
                followup_case["requires_lab_resubmission"] = True
                followup_case["enrichment_updated_at"] = utc_now_iso()
                append_case_followup(
                    followup_case,
                    {
                        "kind": "lab_ocr_correction",
                        "text": text,
                        "note": "Client corrected OCR during 30-day follow-up.",
                    },
                )
                save_submission_state(settings.submissions_dir, followup_case)
                await message.answer(
                    "Принято. Я не буду использовать прежнее автоматическое распознавание как факт. "
                    "Ваше уточнение сохранено, показатели будут помечены как требующие ручной проверки."
                )
                return

            append_case_followup(
                followup_case,
                {
                    "kind": "text_question",
                    "text": text,
                    "note": "Question during active paid follow-up.",
                },
            )
            try:
                await bot.send_chat_action(message.chat.id, "typing")
                followup_prompt = build_followup_context(followup_case, text)
                reply = await asyncio.to_thread(generate_live_reply, settings, [], followup_prompt)
            except Exception:
                logger.exception("Follow-up response failed for user %s", message.from_user.id)
                await message.answer(
                    "Я сохранил вопрос к вашему сопровождению, но сейчас не смог подготовить ответ. "
                    "Команда увидит его и вернётся к вам здесь."
                )
                return

            await message.answer(
                (reply or "Я сохранил вопрос к вашему сопровождению. Команда вернётся к нему здесь, в Telegram.")[:3800]
            )
            return

        await message.answer(
            "Чтобы я корректно помогла, сначала выберите тариф. Ниже есть все варианты: от Нутри-чата до премиум-разбора с анализами.",
            reply_markup=product_keyboard(),
        )
        return

    step = session.get("step")

    if await handle_intake_navigation(message, session, text):
        return

    if step == "full_name":
        session["full_name"] = text
        session["step"] = "anthropometrics"
        touch_session()
        await send_step_prompt(message.chat.id, "anthropometrics")
        return

    if step == "anthropometrics":
        session["anthropometrics"] = text
        session["step"] = "symptoms"
        touch_session()
        await send_step_prompt(message.chat.id, "symptoms")
        return

    if step == "symptoms":
        session["symptoms"] = text
        session["step"] = "goals"
        touch_session()
        await send_step_prompt(message.chat.id, "goals")
        return

    if step == "goals":
        session["goals"] = text
        session["step"] = "nutrition_routine"
        touch_session()
        await send_step_prompt(message.chat.id, "nutrition_routine")
        return

    if step == "nutrition_routine":
        session["nutrition_routine"] = text
        session["step"] = "nutrition"
        touch_session()
        await send_step_prompt(message.chat.id, "nutrition")
        return

    if step == "nutrition":
        session["nutrition"] = text
        session["step"] = "food_behavior"
        touch_session()
        await send_step_prompt(message.chat.id, "food_behavior")
        return

    if step == "food_behavior":
        session["food_behavior"] = text
        session["step"] = "digestion"
        touch_session()
        await send_step_prompt(message.chat.id, "digestion")
        return

    if step == "digestion":
        session["digestion"] = text
        session["step"] = "water_alcohol"
        touch_session()
        await send_step_prompt(message.chat.id, "water_alcohol")
        return

    if step == "water_alcohol":
        session["water_alcohol"] = text
        session["step"] = "sleep_stress"
        touch_session()
        await send_step_prompt(message.chat.id, "sleep_stress")
        return

    if step == "sleep_stress":
        session["sleep_stress"] = text
        session["step"] = "work_lifestyle"
        touch_session()
        await send_step_prompt(message.chat.id, "work_lifestyle")
        return

    if step == "work_lifestyle":
        session["work_lifestyle"] = text
        session["step"] = "background"
        touch_session()
        await send_step_prompt(message.chat.id, "background")
        return

    if step == "background":
        session["background"] = text
        session["step"] = "female_hormones"
        touch_session()
        await send_step_prompt(message.chat.id, "female_hormones")
        return

    if step == "female_hormones":
        session["female_hormones"] = text
        if str(session.get("tier") or session.get("offer") or "") == "standard":
            session["lab_notes"] = "Стандартный тариф: лабораторные анализы не разбираются; бот формирует список анализов к сдаче."
            session["step"] = "red_flags"
            touch_session()
            await message.answer(
                "В стандартном тарифе я не разбираю лабораторные анализы. В итоговом разборе составлю список анализов, которые стоит сдать.\n\n"
                "Вы можете сдать их со скидкой в лаборатории рядом с вашим домом через наш реферальный кабинет в <b>HelloDoc</b>:\n"
                "🔗 <a href='https://hellodoc.app/s/27u6a/'>Сдать анализы со скидкой через HelloDoc</a>\n"
                "Резервная ссылка: <a href='https://hellodoc.app/s/gdgjq/'>HelloDoc Резерв</a>",
                parse_mode="HTML"
            )
            await send_step_prompt(message.chat.id, "red_flags")
            return
        session["step"] = "lab_notes"
        touch_session()
        await send_step_prompt(message.chat.id, "lab_notes")
        return

    if step == "lab_notes":
        if text == "Нет анализов (хочу сдать)":
            await message.answer(
                "🩸 <b>У вас нет готовых анализов на руках?</b>\n\n"
                "нутрициолог Зинченко Ольга Викторовна рекомендует не сдавать анализы наугад — это сэкономит ваш бюджет.\n\n"
                "Специально под вашу программу мы подготовили реферальное направление на анализы со скидкой в лаборатории-партнеры через сервис <b>HelloDoc</b>.\n\n"
                "<b>Как это работает:</b>\n"
                "1. Перейдите по ссылке ниже.\n"
                "2. Выберите удобный адрес лаборатории в вашем городе.\n"
                "3. Оплатите заказ со скидкой и сдайте кровь без очередей.\n"
                "4. Когда результаты будут готовы, пришлите их сюда в чат в формате PDF или фото бланков.\n\n"
                "🔗 <a href='https://hellodoc.app/s/27u6a/'>Сдать анализы со скидкой через HelloDoc</a>\n"
                "Резервная ссылка: <a href='https://hellodoc.app/s/gdgjq/'>HelloDoc Резерв</a>",
                parse_mode="HTML"
            )
            session["lab_notes"] = "Клиент выбрал сдачу анализов через HelloDoc."
        else:
            session["lab_notes"] = text
        
        touch_session()
        session["contact"] = "telegram_current_chat"
        session["step"] = "red_flags"
        await send_step_prompt(message.chat.id, "red_flags")
        return

    if step == "red_flags":
        session["red_flags"] = text
        touch_session()
        if text.lower().startswith("да"):
            await message.answer(
                "Спасибо. Такой ответ помечу как красный флаг. Это не экстренный чат, поэтому при ухудшении состояния "
                "нужна очная медицинская помощь. Анкету можно продолжить, чтобы команда увидела контекст."
            )
        session["step"] = "done"
        touch_session()
        await finalize_submission(message, session)
        return

    await message.answer(UNKNOWN_STATE_TEXT, reply_markup=start_keyboard())


async def process_ocr_background(session: dict, file_path: Path, settings: Any) -> None:
    """Helper to run OCR and append biomarkers to session."""
    raw_text = await recognize_text(file_path, settings)
    if not raw_text:
        quality_payload = {
            "status": "missing",
            "requires_resubmission": True,
            "issues": ["ocr_failed_or_empty"],
        }
        session["lab_quality_check"] = quality_payload
        session["requires_lab_resubmission"] = True
        touch_session()
        persist_submission_enrichment(
            settings.submissions_dir,
            session["submission_id"],
            now_iso=utc_now_iso(),
            lab_quality_check=quality_payload,
            requires_lab_resubmission=True,
        )
        await bot.send_message(session["telegram_user_id"], build_lab_resubmission_message())
        return

    structured = await parse_biomarkers(raw_text, settings)
    quality_payload = {
        "status": structured.get("quality_status", "unknown"),
        "requires_resubmission": structured.get("requires_resubmission", False),
        "issues": structured.get("issues", []),
    }
    session["lab_quality_check"] = quality_payload
    session["requires_lab_resubmission"] = quality_payload["requires_resubmission"]

    if quality_payload["requires_resubmission"]:
        touch_session()
        persist_submission_enrichment(
            settings.submissions_dir,
            session["submission_id"],
            now_iso=utc_now_iso(),
            lab_quality_check=quality_payload,
            requires_lab_resubmission=True,
        )
        await bot.send_message(session["telegram_user_id"], build_lab_resubmission_message())
        logger.warning(
            "OCR for session %s marked as unsafe. Issues: %s",
            session["submission_id"],
            quality_payload["issues"],
        )
        return

    biomarkers = structured.get("biomarkers") or []
    if biomarkers:
        if "parsed_biomarkers" not in session:
            session["parsed_biomarkers"] = []
        session["parsed_biomarkers"].extend(biomarkers)
        mark_lab_confirmation(
            session,
            status="pending_client_confirmation",
            note="OCR распознал показатели; ожидается подтверждение клиента перед использованием как подтверждённых данных.",
        )
        session["pending_biomarker_confirmation"] = biomarkers

    touch_session()
    persist_submission_enrichment(
        settings.submissions_dir,
        session["submission_id"],
        now_iso=utc_now_iso(),
        parsed_biomarkers=session.get("parsed_biomarkers", []),
        pending_biomarker_confirmation=session.get("pending_biomarker_confirmation", []),
        lab_confirmation_status=session.get("lab_confirmation_status"),
        lab_confirmation_needed=session.get("lab_confirmation_needed", False),
        lab_quality_check=quality_payload,
        requires_lab_resubmission=False,
    )
    if biomarkers:
        await bot.send_message(session["telegram_user_id"], build_biomarker_confirmation_message(biomarkers))
    logger.info(
        "OCR completed for session %s. Extracted %d biomarkers.",
        session["submission_id"],
        len(biomarkers),
    )

@dp.message(Command("tma"))
async def cmd_tma(message: types.Message) -> None:
    if not settings.tma_enabled:
        await message.answer(
            "Мини-приложение временно отключено до завершения security-hardening. "
            "Пока продолжаем безопасную работу только через основной Telegram-диалог."
        )
        return

    session = get_session(message.from_user.id)
    if not session:
        await message.answer(
            "Мини-приложение доступно только для активного кейса. Сначала начните или продолжите intake в этом чате."
        )
        return

    if not session.get("tma_access_token"):
        session["tma_access_token"] = secrets.token_urlsafe(24)
        touch_session()

    # Build URL - in production this would be a real domain
    # For Telegram Mini Apps, we can use the bot's domain or a tunnel
    web_url = (
        f"http://localhost:{ACTIVE_TMA_PORT}/static/tma.html"
        f"?user_id={message.from_user.id}&access_token={session['tma_access_token']}"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="💎 Открыть интерактивное досье",
        web_app=types.WebAppInfo(url=web_url)
    ))
    await message.answer(
        "Ваш личный кабинет Wellness-навигации готов. Здесь вы можете видеть динамику биомаркеров и ваш 8-недельный план.",
        reply_markup=builder.as_markup()
    )

# --- Web Server Handlers ---

async def handle_tma_api(request):
    """API called by the Mini App to fetch session data."""
    if not settings.tma_enabled:
        return web.json_response({"error": "TMA is disabled"}, status=403)

    user_id = request.query.get("user_id")
    access_token = request.query.get("access_token")
    if not user_id or not access_token:
        return web.json_response({"error": "Missing credentials"}, status=400)

    try:
        numeric_user_id = int(user_id)
    except ValueError:
        return web.json_response({"error": "Invalid user_id"}, status=400)

    session = get_session(numeric_user_id)
    if not session:
        return web.json_response({"error": "No active TMA session"}, status=404)

    expected_token = str(session.get("tma_access_token") or "")
    if not expected_token or not secrets.compare_digest(expected_token, access_token):
        return web.json_response({"error": "Forbidden"}, status=403)

    data = session

    # Load AI Draft if exists
    draft_content = {}
    if data.get("draft_path"):
        try:
            with open(data["draft_path"], "r", encoding="utf-8") as f:
                raw_draft = f.read()
                # Attempt to parse as JSON
                import json
                draft_content = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_draft.strip(), flags=re.IGNORECASE))
        except Exception:
            draft_content = {"hypotheses": ["Досье еще в процессе подготовки экспертом."]}

    return web.json_response({
        "profile": {
            "full_name": data.get("full_name") or data.get("user", {}).get("first_name"),
            "age": data.get("age"),
            "city": data.get("city")
        },
        "parsed_biomarkers": data.get("parsed_biomarkers", []),
        "vision_analysis": data.get("vision_analysis"),
        "hypotheses": draft_content.get("hypotheses", []),
        "strategy": draft_content.get("strategy", {}),
        "schemes": draft_content.get("schemes", []),
        "step": data.get("step")
    })

async def process_vision_background(session: dict, file_path: Path, settings: Any) -> None:
    """Helper to run Vision AI analysis for physical markers."""
    from lab_ocr import analyze_physical_markers
    analysis = await analyze_physical_markers(file_path, settings)
    session["vision_analysis"] = analysis
    touch_session()
    persist_submission_enrichment(
        settings.submissions_dir,
        session["submission_id"],
        now_iso=utc_now_iso(),
        vision_analysis=analysis,
    )
    logger.info("Vision AI completed for session %s", session["submission_id"])

def get_timezone_offset_for_city(city: str | None) -> int:
    # Default to Moscow Time (UTC+3)
    if not city:
        return 3
    city_lower = str(city).lower().strip()
    if any(x in city_lower for x in ("москв", "питер", "спб", "краснодар", "сочи", "ростов", "казан", "нижн", "ворон")):
        return 3
    if any(x in city_lower for x in ("калининград",)):
        return 2
    if any(x in city_lower for x in ("самар", "саратов", "ульян", "астрах", "ижевск")):
        return 4
    if any(x in city_lower for x in ("екатерин", "екат", "пермь", "уфа", "челябинск", "тюмень", "оренбург")):
        return 5
    if any(x in city_lower for x in ("омск",)):
        return 6
    if any(x in city_lower for x in ("новосибирск", "нск", "красноярск", "томск", "кемерово", "барнаул", "новокузнецк")):
        return 7
    if any(x in city_lower for x in ("иркутск", "улан-удэ")):
        return 8
    if any(x in city_lower for x in ("якутск", "чита")):
        return 9
    if any(x in city_lower for x in ("владивосток", "хабаровск")):
        return 10
    if any(x in city_lower for x in ("магадан", "сахалин")):
        return 11
    if any(x in city_lower for x in ("камчат", "петропавловск")):
        return 12
    return 3


async def nurture_engine_loop():
    """Background task to gently remind users to complete their intake or upload labs, and send daily habit reminders."""
    logger.info("Nurture engine started.")
    while True:
        try:
            # Get current UTC time
            now_utc = datetime.now(timezone.utc)
            current_hour_utc = now_utc.hour
            today_str = now_utc.date().isoformat()
            
            for user_id_str, session in list(user_sessions.items()):
                try:
                    user_id = int(user_id_str)
                except (ValueError, TypeError):
                    continue
                
                step = session.get("step")
                
                # 1. Check if the user is stuck on 'lab_notes'
                if step == "lab_notes" and not session.get("nurture_sent"):
                    try:
                        name = session.get("full_name", "Здравствуйте").split(" ")[0]
                        await bot.send_message(
                            user_id,
                            f"{name}, напишите, пожалуйста, какие анализы сдавали — или пришлите фото результатов. "
                            f"Это поможет мне собрать полную картину. Если анализов нет, просто напишите `пропустить`."
                        )
                        session["nurture_sent"] = True
                        touch_session()
                        logger.info("Nurture message sent to %s", user_id)
                    except Exception as e:
                        logger.error("Failed to send nurture to %s: %s", user_id, e)
                
                # 2. Habits daily log reminders (Water and sleep!)
                if step == "habits_daily_log":
                    # Get client's local hour
                    city_name = session.get("city") or session.get("profile", {}).get("city")
                    offset = get_timezone_offset_for_city(city_name)
                    local_hour = (current_hour_utc + offset) % 24
                    
                    reminders_sent = session.setdefault("last_habit_reminders", {})
                    
                    # A. Sleep reminder: at 22:00 local time (1 hour before 23:00)
                    if local_hour == 22:
                        key = f"sleep_22_{today_str}"
                        if not reminders_sent.get(key):
                            try:
                                name = (session.get("full_name") or session.get("profile", {}).get("full_name") or "Здравствуйте").split(" ")[0]
                                await bot.send_message(
                                    user_id,
                                    f"🌙 <b>{name}, пора готовиться ко сну!</b>\n\n"
                                    f"До 23:00 остался 1 час. Это лучшее время, чтобы отложить все гаджеты, "
                                    f"выпить немного теплой воды (если хочется) и настроить организм на восстановление, "
                                    f"чтобы уснуть до 23:00.\n\n"
                                    f"Спокойной ночи! 😴",
                                    parse_mode="HTML"
                                )
                                reminders_sent[key] = True
                                touch_session()
                                logger.info("Sent sleep reminder to %s", user_id)
                            except Exception as e:
                                logger.error("Failed to send sleep reminder to %s: %s", user_id, e)
                                
                    # B. Water reminders: e.g. at 11:00, 15:00, 19:00 local time
                    elif local_hour in {11, 15, 19}:
                        key = f"water_{local_hour}_{today_str}"
                        if not reminders_sent.get(key):
                            try:
                                name = (session.get("full_name") or session.get("profile", {}).get("full_name") or "Здравствуйте").split(" ")[0]
                                if local_hour == 11:
                                    msg = f"💧 <b>{name}, время чистой воды!</b>\n\nНе забывайте пить воду в первой половине дня для бодрости и хорошего желчеоттока."
                                elif local_hour == 15:
                                    msg = f"💧 <b>{name}, пора сделать пару глотков!</b>\n\nСтакан чистой теплой воды поможет избежать ложного чувства голода и поддержит энергию во второй половине дня."
                                else:
                                    msg = f"💧 <b>{name}, вечерний стакан воды!</b>\n\nВыпейте немного чистой теплой воды, чтобы поддержать гидратацию, но не слишком много перед сном."
                                
                                await bot.send_message(user_id, msg, parse_mode="HTML")
                                reminders_sent[key] = True
                                touch_session()
                                logger.info("Sent water reminder (%s) to %s", local_hour, user_id)
                            except Exception as e:
                                logger.error("Failed to send water reminder (%s) to %s: %s", local_hour, user_id, e)
                                
                # 3. Manual payment reminder
                submission_id = session.get("submission_id")
                if submission_id:
                    submission = load_submission(settings.submissions_dir, submission_id)
                    if submission and submission.get("intake_status") == "manual_payment_pending":
                        if not submission.get("client_reported_payment") and not submission.get("payment_reminder_sent"):
                            try:
                                pending_at_str = submission.get("manual_payment_pending_at") or submission.get("manual_handoff_started_at")
                                if pending_at_str:
                                    try:
                                        pending_at = datetime.strptime(pending_at_str, "%Y-%m-%dT%H:%M:%SZ")
                                    except ValueError:
                                        pending_at = datetime.utcnow()
                                    
                                    elapsed = (datetime.utcnow() - pending_at).total_seconds()
                                    if elapsed < 15 * 60:
                                        continue  # Skip sending the reminder if it has been less than 15 minutes
                                
                                name = (session.get("full_name") or session.get("profile", {}).get("full_name") or "Здравствуйте").split(" ")[0]
                                client_pay_markup = InlineKeyboardMarkup(
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="✅ Подтвердить оплату (я оплатил/а)",
                                                callback_data=f"clientconfirmpay_{submission_id}",
                                            )
                                        ]
                                    ]
                                )
                                await bot.send_message(
                                    user_id,
                                    f"🔔 <b>{name}, напоминание об оплате</b>\n\n"
                                    f"Вы начали оформление программы, но мы пока не получили вашу отметку об оплате.\n\n"
                                    f"Если вы уже провели платеж, пожалуйста, <b>нажмите на кнопку «Подтвердить оплату (я оплатил/а)» ниже</b>. "
                                    f"Это нужно, чтобы наша команда сразу увидела ваш платеж и открыла доступ к программе!\n\n"
                                    f"Если у вас возникли трудности с оплатой или вопросы, просто напишите здесь в чат.",
                                    reply_markup=client_pay_markup,
                                    parse_mode="HTML"
                                )
                                submission["payment_reminder_sent"] = True
                                save_submission_state(settings.submissions_dir, submission)
                                touch_session()
                                logger.info("Sent manual payment reminder with confirmation button to user %s", user_id)
                            except Exception as e:
                                logger.error("Failed to send manual payment reminder to %s: %s", user_id, e)
        except Exception as e:
            logger.exception("Nurture engine error: %s", e)
            
        await asyncio.sleep(60 * 30) # Run every 30 minutes


async def send_product_digest_to_admins(payload: dict[str, Any]) -> bool:
    if not settings.admin_chat_ids:
        return False

    if not (payload.get("cases") or {}):
        return False

    digest_chunks = split_telegram_text(build_admin_digest_text(payload))
    delivered = False
    for admin_chat_id in settings.admin_chat_ids:
        try:
            for chunk in digest_chunks:
                await bot.send_message(admin_chat_id, chunk)
            delivered = True
        except Exception:
            logger.exception("Failed to send product digest to admin chat %s", admin_chat_id)
    return delivered


async def maybe_send_weekly_product_digest() -> bool:
    payload = load_product_insights(settings.product_insights_path)
    if not is_weekly_digest_due(payload):
        return False

    delivered = await send_product_digest_to_admins(payload)
    if not delivered:
        return False

    updated_payload = mark_weekly_digest_sent(payload)
    save_product_insights(settings.product_insights_path, updated_payload)
    return True


async def weekly_digest_loop():
    """Background task to send a combined 7d/30d product digest every Monday after 10:00 MSK."""
    logger.info("Weekly digest loop started.")
    while True:
        try:
            await maybe_send_weekly_product_digest()
        except Exception:
            logger.exception("Weekly digest loop error")

        await asyncio.sleep(30 * 60)

async def init_web_app():
    app = web.Application()
    if settings.tma_enabled:
        app.router.add_get("/api/session", handle_tma_api)
        app.router.add_static("/static/", path="static", name="static")
    return app

def export_to_obsidian(session: dict, content: str) -> None:
    """Helper to save a case to the Obsidian Vault."""
    vault_path = Path("C:/Users/HP/Documents/Obsidian Vault/01_Clients")
    if not vault_path.exists():
        return
        
    client_name = session.get("full_name", "Anonymous").replace(" ", "_")
    case_id = session.get("submission_id")
    file_name = f"{client_name}_{case_id}.md"
    target = vault_path / file_name
    
    header = f"---\ntitle: Wellness Case: {client_name}\nid: {case_id}\ndate: {datetime.now().strftime('%Y-%m-%d')}\nstatus: Draft\n---\n\n"
    
    try:
        with open(target, "w", encoding="utf-8") as f:
            f.write(header + content)
        logger.info("Auto-exported case %s to Obsidian Vault", case_id)
    except Exception:
        logger.exception("Failed to export to Obsidian")

async def main() -> None:
    global ACTIVE_TMA_PORT

    # --- Single-instance lock ---
    lock_path = Path(__file__).parent / ".bot.lock"
    try:
        if lock_path.exists():
            old_pid = int(lock_path.read_text().strip())
            try:
                os.kill(old_pid, 0)  # check if alive
                logger.error("Another bot instance is running (PID %s). Exiting.", old_pid)
                return
            except (OSError, ValueError):
                pass  # stale lock
        lock_path.write_text(str(os.getpid()))
    except Exception as exc:
        logger.warning("PID lock file error: %s", exc)
    # --- end lock ---

    logger.info("Starting Wellness Bot")
    restore_runtime_state()
    asyncio.create_task(nurture_engine_loop())
    asyncio.create_task(weekly_digest_loop())
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())





























