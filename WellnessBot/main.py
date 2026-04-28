from __future__ import annotations

import asyncio
import logging
import json
import os
import re
import secrets
from pathlib import Path
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from typing import Any

from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    PreCheckoutQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

from ai_drafting import (
    generate_case_draft,
    generate_case_growth_report,
    generate_case_judge_report,
    generate_live_reply,
)
from case_service import (
    build_session_from_submission,
    build_submission_payload,
    persist_submission_enrichment,
    save_submission_state,
    update_submission_status,
)
from config import load_settings
from lab_ocr import (
    build_biomarker_confirmation_message,
    build_lab_resubmission_message,
    parse_biomarkers,
    parse_manual_biomarkers,
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
from voice_processor import (
    SYNC_STT_MAX_BYTES,
    SYNC_STT_MAX_DURATION_SECONDS,
    handle_audio_to_text,
    handle_voice_to_text,
)
from html_pdf_engine import create_premium_pdf
from texts import (
    ABOUT_TEXT,
    CONSENT_DECLINED_TEXT,
    CONSENT_TEXT,
    FINAL_MESSAGE,
    LABS_GUIDANCE_TEXT,
    MANUAL_HANDOFF_REVIEW_TEXT,
    MANUAL_HANDOFF_START_TEXT,
    OPERATOR_HELP_TEXT,
    PRODUCT_EXAMPLES_TEXT,
    PRODUCT_MENU_TEXT,
    RESET_TEXT,
    START_TEXT,
    TIER_DESCRIPTIONS,
    TIER_PREMIUM_DESC,
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
            [InlineKeyboardButton(text="Начать разбор", callback_data="choose_product")],
            [InlineKeyboardButton(text="Посмотреть пример результата", callback_data="show_examples")],
            [InlineKeyboardButton(text="ℹ️ Как это работает", callback_data="show_process")],
            [InlineKeyboardButton(text="Связь с Ольгой / оператором", callback_data="operator_help")],
            [InlineKeyboardButton(text="Живой диалог с нейросетью", callback_data="start_live_chat")],
        ]
    )


def product_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="7 дней — 3 900 ₽", callback_data="tier_week")],
            [InlineKeyboardButton(text="30 дней — 6 900 ₽", callback_data="tier_premium")],
            [InlineKeyboardButton(text="VIP 30 дней — 14 900 ₽", callback_data="tier_vip")],
            [InlineKeyboardButton(text="Посмотреть пример результата", callback_data="show_examples")],
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
    "week": "Разбор на 7 дней",
    "premium": "Персональный разбор на 30 дней",
    "vip": "VIP-сопровождение на 30 дней",
}

INTAKE_STEP_ORDER = [
    "full_name",
    "age",
    "city",
    "anthropometrics",
    "work_lifestyle",
    "symptoms",
    "wellbeing_energy",
    "complaint_pattern",
    "goals",
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
    "labs",
]
OPTIONAL_INTAKE_STEPS = {
    "anthropometrics",
    "female_hormones",
    "labs",
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
    if step == "labs":
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

    if normalized in SKIP_WORDS and step not in {"labs", "red_flags"}:
        session[step] = "Клиент пропустил шаг."
        next_step = intake_next_step(step)
        if not next_step:
            session["step"] = "labs"
            next_step = "labs"
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
                "wellbeing_energy": medical.get("wellbeing_energy"),
                "background": medical.get("background"),
                "risk_details": medical.get("risk_details"),
                "nutrition": medical.get("nutrition"),
                "food_behavior": medical.get("food_behavior"),
                "digestion": medical.get("digestion"),
                "sleep_stress": medical.get("sleep_stress"),
                "activity": medical.get("activity"),
                "female_hormones": medical.get("female_hormones"),
                "hormonal_reproductive_context": medical.get("hormonal_reproductive_context") or medical.get("female_hormones"),
                "emotional_stress": medical.get("emotional_stress"),
                "motivation": medical.get("motivation"),
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
        "full_name": "Шаг 1/21. Как к вам обращаться? Напишите имя и фамилию.",
        "age": "Шаг 2/21. Сколько вам полных лет?",
        "city": "Шаг 3/21. Из какого вы города и часового пояса?",
        "anthropometrics": (
            "Шаг 4/21. Укажите рост, текущий вес и желаемый вес, если это актуально. "
            "Можно одной строкой: `рост 168, вес 72, хочу 65`."
        ),
        "work_lifestyle": (
            "Шаг 5/21. Чем вы занимаетесь и какой характер работы: сидячая/активная, график, ночные смены, "
            "командировки, уровень нагрузки в обычный день?"
        ),
        "symptoms": (
            "Шаг 6/21. Какие 3-7 жалоб сейчас беспокоят сильнее всего? "
            "Например: усталость, сон, ЖКТ, желчный/желчеотток, кожа, волосы, отёки, тяга к сладкому, цикл, настроение."
        ),
        "wellbeing_energy": (
            "Шаг 7/21. Оцените самочувствие: энергия утром/днём/вечером по шкале 1-10, "
            "есть ли головные боли, сонливость, ПМС, отёки, тяжесть или утреннее разбитое состояние?"
        ),
        "complaint_pattern": (
            "Шаг 8/21. Опишите динамику жалоб: когда началось, что усиливает, что облегчает, "
            "есть ли повторяемость по времени суток, циклу, еде, стрессу или нагрузке?"
        ),
        "goals": (
            "Шаг 9/21. Какой результат вы хотите получить от разбора в ближайшие 4-8 недель "
            "и какой результат считаете реальным через 3 месяца?"
        ),
        "nutrition": (
            "Шаг 10/21. Опишите питание за обычный день: завтрак, обед, ужин, перекусы, вода, кофе/чай, "
            "сладкое, алкоголь, кто обычно готовит, есть ли ограничения или пищевые реакции."
        ),
        "food_behavior": (
            "Шаг 11/21. Опишите пищевое поведение: тяга к сладкому/солёному, переедание, заедание эмоций, "
            "голод физиологический или эмоциональный, что чувствуете после еды."
        ),
        "digestion": (
            "Шаг 12/21. Что сейчас с ЖКТ и желчеоттоком: аппетит, вздутие, изжога, отрыжка, тошнота, горечь во рту, "
            "тяжесть справа под рёбрами, стул, боли, реакция на жирное, молочные продукты, глютен или сладкое?"
        ),
        "sleep_stress": (
            "Шаг 13/21. Какой сон и восстановление: во сколько засыпаете/просыпаетесь, ночные пробуждения, "
            "утренние отёки/головная боль, уровень восстановления 1-10 и что чаще всего мешает сну?"
        ),
        "activity": (
            "Шаг 14/21. Какая активность сейчас: шаги, тренировки, сидячая работа, усталость после нагрузки, "
            "одышка, ограничения по здоровью или движения, которые вызывают дискомфорт?"
        ),
        "female_hormones": (
            "Шаг 15/21. Гормональный и репродуктивный фон, если актуально. "
            "Для женщин: цикл, регулярность, ПМС, болезненность, обильность, сгустки, роды/кесарево, "
            "гормональные препараты, приливы, потливость, либидо, изменения кожи/волос/веса за последний год. "
            "Для мужчин: либидо, восстановление, настроение, вес/талия, выпадение волос, мочеполовые жалобы, "
            "приём тестостерона/гормональных препаратов или наблюдение у уролога/эндокринолога. "
            "Если не актуально, напишите `не актуально`."
        ),
        "emotional_stress": (
            "Шаг 16/21. Эмоции и стресс: уровень стресса 1-10, главные источники, реакция на стресс "
            "(тревога, злость, апатия, переедание), что помогает расслабиться, есть ли выгорание?"
        ),
        "background": (
            "Шаг 17/21. Укажите важный медицинский фон: хронические заболевания, диагнозы, операции, травмы, роды, "
            "беременность/ГВ, детский или подростковый возраст, онкология в анамнезе."
        ),
        "risk_details": (
            "Шаг 18/21. Лекарства, витамины, БАДы и дозировки сейчас. Отдельно укажите аллергии, непереносимости, "
            "скачки давления, сердцебиение, головокружения, щитовидку, сахар/инсулин, когда сдавали анализы в последний раз "
            "и были ли УЗИ, консультации или выписки из стационара за последние 6 месяцев."
        ),
        "motivation": (
            "Шаг 19/21. Мотивация и тело: что хотите изменить в теле/самочувствии, почему занялись этим сейчас, "
            "что мешало удерживать результат раньше, есть ли поддержка семьи/окружения?"
        ),
        "red_flags": (
            "Шаг 20/21. Есть ли сейчас красные флаги: острая боль в груди, потеря сознания, кровь в стуле, "
            "температура несколько дней подряд, беременность с осложнениями или другое состояние, "
            "где нужна срочная очная помощь? Ответьте коротко: `да` или `нет`, и если нужно - уточните."
        ),
        "labs": "Шаг 21/21. " + LABS_GUIDANCE_TEXT,
        "contact": "Финальный шаг. Как лучше связаться с вами после разбора: Telegram, телефон или email?",
    }

    prompts["contact"] = (
        "Финальный шаг. По умолчанию продолжаем общение здесь, в Telegram. "
        "Если нужен другой Telegram-аккаунт, укажите его. "
        "Иначе просто ответьте: `этот чат`."
    )
    reply_markup = labs_keyboard() if step == "labs" else None
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


def normalize_dossier_pdf_data(raw_data: dict[str, Any]) -> dict[str, Any]:
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

    return {
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
    }


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
    if client_id:
        try:
            await bot.send_message(
                client_id,
                "Оплата подтверждена. Мы начинаем сборку премиального досье, а перед отправкой результат пройдёт экспертную проверку.",
            )
        except Exception:
            logger.exception("Failed to notify client about manual payment confirmation for %s", submission_id)

    admin_chat_id = callback_query.message.chat.id if callback_query.message else callback_query.from_user.id
    await bot.send_message(
        admin_chat_id,
        f"✅ Ручная оплата подтверждена для {submission_id}. Запускаю сборку досье.",
    )
    await bot.answer_callback_query(callback_query.id, "Ручная оплата подтверждена.")

    session = build_session_from_submission(
        submission,
        SimpleNamespace(
            id=client_id,
            username=submission.get("profile", {}).get("telegram_username"),
            full_name=submission.get("profile", {}).get("telegram_full_name"),
        ),
    )
    await build_dossier_after_payment(
        callback_query.message,
        session,
        progress_chat_id=admin_chat_id,
        client_chat_id=client_id,
    )

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

    from aiogram.types import FSInputFile
    pdf_doc = FSInputFile(pdf_path)
    
    await bot.send_document(
        client_id,
        document=pdf_doc,
        caption=(
            "Ваше досье готово. Начните с первой страницы: там карта ближайших 14 дней, "
            "план на 3 дня и стоп-сигналы.\n\n"
            "В течение 30 дней можно присылать сюда анализы, УЗИ, выписки за последние 6 месяцев, фото жалоб и вопросы по плану. "
            "Я помогу аккуратно скорректировать маршрут без диагнозов и самоназначений."
        )
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
            normalize_dossier_pdf_data(json.loads(clean_json_str.strip())),
            submission,
        )
        pdf_filename = f"dossier_{submission_id}.pdf"
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


async def finalize_submission(message: types.Message, session: dict[str, Any]) -> None:
    submission = build_submission_payload(session)
    submission["payment_context"] = build_payment_context(session, now_iso=utc_now_iso())
    use_telegram_invoice = settings.payment_mode == "telegram" and bool(settings.tg_payment_token)

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
            await message.answer(
                "Анкета сохранена, но сейчас не удалось открыть оплату автоматически. "
                "Команда получила ваш кейс и свяжется с вами здесь, в Telegram."
            )
            return
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
    await message.answer(MANUAL_HANDOFF_START_TEXT)


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

    await message.answer("✅ Оплата успешно получена. Запускаю сборку премиального досье.")
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
                draft_payload = normalize_dossier_pdf_data(json.loads(strip_json_code_fences(draft_text)))
                draft_payload = apply_safe_action_floor(draft_payload, submission)
                draft_text = json.dumps(draft_payload, ensure_ascii=False, indent=2)
            except Exception:
                logger.exception("Failed to apply safe action floor before review for %s", session["submission_id"])

            draft_path = save_draft(settings.drafts_dir, session["submission_id"], draft_text)
            submission["draft_path"] = str(draft_path)

            try:
                judge_report_text = await asyncio.wait_for(
                    asyncio.to_thread(generate_case_judge_report, settings, submission, draft_text),
                    timeout=90,
                )
            except Exception:
                logger.exception("Judge review failed for %s", session["submission_id"])
                judge_report_text = None

            if judge_report_text:
                review_path = save_review_report(settings.drafts_dir, session["submission_id"], judge_report_text)
                submission["judge_report_path"] = str(review_path)

            try:
                growth_governance = load_product_governance(settings.product_governance_path)
                growth_governance_context = build_growth_governance_context(growth_governance)
                growth_report_text = await asyncio.wait_for(
                    asyncio.to_thread(
                        generate_case_growth_report,
                        settings,
                        submission,
                        draft_text,
                        judge_report_text,
                        growth_governance_context,
                    ),
                    timeout=90,
                )
            except Exception:
                logger.exception("Growth architect review failed for %s", session["submission_id"])
                growth_report_text = None

            if growth_report_text:
                growth_path = save_growth_report(settings.drafts_dir, session["submission_id"], growth_report_text)
                submission["growth_report_path"] = str(growth_path)

            review_signals = apply_internal_review_signals(
                submission,
                judge_report_text,
                growth_report_text,
            )
            product_insights_payload = update_product_insights_memory(
                submission,
                judge_report_text,
                growth_report_text,
            )
            governance_payload = sync_governance_experiments_from_insights(product_insights_payload)
            submission["product_insights_updated_at"] = product_insights_payload.get("updated_at")
            submission["product_governance_updated_at"] = governance_payload.get("updated_at")

            # [OBSIDIAN SYNC] Automatically export the draft to the expert's Second Brain
            await asyncio.to_thread(export_to_obsidian, session, draft_text)
            
            # Generation of Premium PDF from strictly structured JSON
            try:
                import re
                clean_json_str = strip_json_code_fences(draft_text)
                
                pdf_data = apply_safe_action_floor(
                    normalize_dossier_pdf_data(json.loads(clean_json_str)),
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
                
                pdf_filename = f"dossier_{session['submission_id']}.pdf"
                pdf_path = settings.drafts_dir / pdf_filename
                
                # Run playwright pdf generation in thread pool
                await asyncio.to_thread(create_premium_pdf, pdf_data, str(pdf_path))
                submission["pdf_path"] = str(pdf_path)
            except Exception as e:
                logger.exception("Failed to render Premium PDF. Check JSON formatting.")
            
        if review_signals.get("needs_quality_rework") and review_signals.get("needs_market_rework"):
            update_submission_status(submission, intake_status="review_priority_quality_and_market", now_iso=utc_now_iso())
        elif review_signals.get("needs_quality_rework"):
            update_submission_status(submission, intake_status="review_priority_quality_rework", now_iso=utc_now_iso())
        elif review_signals.get("needs_market_rework"):
            update_submission_status(submission, intake_status="review_priority_market_rework", now_iso=utc_now_iso())
        elif submission.get("pdf_path"):
            update_submission_status(submission, intake_status="awaiting_human_review", now_iso=utc_now_iso())
        elif submission.get("draft_path"):
            update_submission_status(submission, intake_status="draft_ready_human_review", now_iso=utc_now_iso())
        else:
            update_submission_status(submission, intake_status="awaiting_manual_review_no_draft", now_iso=utc_now_iso())
        submission["generation_finished_at"] = utc_now_iso()
        save_submission_state(settings.submissions_dir, submission)
    finally:
        loading_task.cancel()
        try:
            await bot.delete_message(chat_id=progress_chat_id, message_id=start_msg.message_id)
        except:
            pass

    logger.info("Saved submission %s to %s", session["submission_id"], submission_path)
    await notify_admins(submission, draft_text, judge_report_text, growth_report_text)
    clear_session(int(session["telegram_user_id"]))
    if settings.tg_payment_token:
        await bot.send_message(
            client_chat_id,
            "Анкета отправлена на проверку.\n\n"
            "Главный эксперт изучит материалы, и мы вышлем ваше Премиальное Wellness-досье прямо в этот чат.\n\n"
            "Если нужно начать заново, используйте /reset."
        )
        return

    await bot.send_message(client_chat_id, MANUAL_HANDOFF_REVIEW_TEXT)


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
        "Режим живого диалога включён. Пишите вопрос обычным сообщением, я отвечу как нейросетевой ассистент."
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
            f"вЂў <code>{case.get('submission_id')}</code>\n"
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
        f"- Proxy: {settings.bot_proxy_url or 'disabled'}",
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


@dp.callback_query(lambda c: c.data and c.data.startswith("tier_"))
async def process_tier_selection(callback_query: types.CallbackQuery) -> None:
    tier = callback_query.data.replace("tier_", "")
    if tier not in TIER_NAMES:
        tier = "premium"

    reset_chat_session(callback_query.from_user.id)
    start_session(callback_query.from_user, tier=tier)

    await bot.send_message(callback_query.from_user.id, TIER_DESCRIPTIONS.get(tier, TIER_PREMIUM_DESC))
    await bot.send_message(callback_query.from_user.id, CONSENT_TEXT, reply_markup=consent_keyboard())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "choose_product")
async def process_choose_product(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.from_user.id, PRODUCT_MENU_TEXT, reply_markup=product_keyboard())
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
    session = get_session(callback_query.from_user.id) or start_session(callback_query.from_user)
    session["consent_given"] = True
    session["step"] = "full_name"
    touch_session()
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
    touch_session()
    await finalize_submission(callback_query.message, session)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(lambda c: c.data == "labs_done")
async def process_labs_done(callback_query: types.CallbackQuery) -> None:
    session = get_session(callback_query.from_user.id)
    if not session or session.get("step") != "labs":
        await bot.answer_callback_query(callback_query.id, text="Сначала начните intake заново через /start", show_alert=True)
        return

    if session.get("lab_confirmation_status") == "pending_client_confirmation":
        await callback_query.message.answer(
            "Я уже распознал(а) показатели из файла, но мне нужно ваше подтверждение, чтобы не ошибиться.\n\n"
            "Ответьте, пожалуйста: «да, верно» — если всё совпадает, или напишите исправления по цифрам/единицам."
        )
        await bot.answer_callback_query(callback_query.id)
        return

    session["contact"] = "telegram_current_chat"
    session["step"] = "done"
    touch_session()
    await finalize_submission(callback_query.message, session)
    await bot.answer_callback_query(callback_query.id)


@dp.message(lambda message: message.document is not None)
async def handle_document_upload(message: types.Message) -> None:
    session = get_session(message.from_user.id)
    if not session or session.get("step") != "labs":
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
        "Файл сохранён. Я начал автоматическое распознавание данных из него. Если есть ещё документы, отправляйте. Когда закончите, нажмите кнопку.",
        reply_markup=labs_keyboard(),
    )


@dp.message(lambda message: bool(message.photo))
async def handle_photo_upload(message: types.Message) -> None:
    session = get_session(message.from_user.id)
    if not session or session.get("step") != "labs":
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
    await message.answer(msg_text, reply_markup=labs_keyboard())


@dp.message(F.voice)
async def handle_voice(message: types.Message) -> None:
    session = get_session(message.from_user.id)
    if not session and (settings.llm_provider == "disabled" or not settings.llm_api_key):
        await message.answer(UNKNOWN_STATE_TEXT, reply_markup=start_keyboard())
        return
        
    await bot.send_chat_action(message.chat.id, "typing")
    text = await handle_voice_to_text(bot, message.voice.file_id, settings)
    
    if not text:
        await message.answer(
            "Извините, я не смог расшифровать голосовое сообщение. "
            "Пожалуйста, повторите текстом."
        )
        return
        
    # Simulate a text message with the decoded voice
    message.text = f"🎤 Распознано: {text}"
    _text_backup = message.text 
    message.text = text # provide clean text to the handler
    await message.answer(f"<i>{_text_backup}</i>", parse_mode="HTML")
    await handle_message(message)


@dp.message(F.audio)
async def handle_audio(message: types.Message) -> None:
    session = get_session(message.from_user.id)
    if not session and (settings.llm_provider == "disabled" or not settings.llm_api_key):
        await message.answer(UNKNOWN_STATE_TEXT, reply_markup=start_keyboard())
        return

    audio = message.audio
    if not audio:
        await message.answer(
            "Я не увидел аудиофайл. Попробуйте отправить его ещё раз или используйте голосовое сообщение."
        )
        return

    await bot.send_chat_action(message.chat.id, "typing")
    text = await handle_audio_to_text(
        bot,
        audio.file_id,
        settings,
        file_name=audio.file_name,
        mime_type=audio.mime_type,
        duration_seconds=audio.duration,
        file_size=audio.file_size,
    )

    if not text:
        if settings.llm_provider == "yandex_foundation":
            duration_note = ""
            if audio.duration and audio.duration > SYNC_STT_MAX_DURATION_SECONDS:
                duration_note = f"Длительность аудио сейчас {audio.duration} сек., а безопасный предел для этого режима — до {SYNC_STT_MAX_DURATION_SECONDS} сек. "
            size_note = ""
            if audio.file_size and audio.file_size > SYNC_STT_MAX_BYTES:
                size_note = "Файл получился слишком тяжёлым для текущего режима распознавания. "
            await message.answer(
                "Я пока не смог распознать этот аудиофайл. "
                f"{duration_note}{size_note}"
                "Надёжнее всего отправить речь как обычное голосовое сообщение в Telegram. "
                "Если хотите именно аудиофайлом, лучше использовать короткий `.ogg/.opus` файл."
            )
            return

        await message.answer(
            "Я не смог распознать этот аудиофайл. Попробуйте отправить его ещё раз или используйте голосовое сообщение."
        )
        return

    message.text = f"🎧 Распознано из аудио: {text}"
    _text_backup = message.text
    message.text = text
    await message.answer(f"<i>{_text_backup}</i>", parse_mode="HTML")
    await handle_message(message)


@dp.message()
async def handle_message(message: types.Message) -> None:
    if not message.text:
        await message.answer("Для этого шага лучше отправить текстовый ответ или голосовое сообщение.")
        return

    if message.text.startswith("/"):
        return

    session = get_session(message.from_user.id)
    text = message.text.strip()

    if not session:
        if wants_premium_intake(text):
            reset_chat_session(message.from_user.id)
            start_session(message.from_user, tier="premium")
            await message.answer(TIER_PREMIUM_DESC)
            await message.answer(CONSENT_TEXT, reply_markup=consent_keyboard())
            return

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
                    "note": "Question during 30-day follow-up.",
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

        # [ANTI-LOOP VALIDATOR]
        history = get_chat_history(message.from_user.id)
        assistant_replies = [msg["content"] for msg in history if msg["role"] == "assistant"]
        if len(assistant_replies) >= 2 and reply == assistant_replies[-1] and reply == assistant_replies[-2]:
            logger.warning("[ANTI-LOOP] Detected repetitive AI loop for user %s", message.from_user.id)
            await message.answer("⚠️ Защита от зацикливания: Я заметил, что повторяюсь. Давайте обнулим контекст живого диалога, чтобы вернуть ясность.")
            reset_chat_session(message.from_user.id)
            return

        append_chat_message(message.from_user.id, "user", text)
        append_chat_message(message.from_user.id, "assistant", reply)
        await message.answer(reply[:3800])
        return

    step = session.get("step")

    if await handle_intake_navigation(message, session, text):
        return

    if step == "full_name":
        session["full_name"] = text
        session["step"] = "age"
        touch_session()
        await send_step_prompt(message.chat.id, "age")
        return

    if step == "age":
        if not text.isdigit():
            await message.answer("Возраст лучше указать числом, например: 34")
            return
        session["age"] = int(text)
        session["step"] = "city"
        touch_session()
        await send_step_prompt(message.chat.id, "city")
        return

    if step == "city":
        session["city"] = text
        session["step"] = "anthropometrics"
        touch_session()
        await send_step_prompt(message.chat.id, "anthropometrics")
        return

    if step == "anthropometrics":
        session["anthropometrics"] = text
        session["step"] = "work_lifestyle"
        touch_session()
        await send_step_prompt(message.chat.id, "work_lifestyle")
        return

    if step == "work_lifestyle":
        session["work_lifestyle"] = text
        session["step"] = "symptoms"
        touch_session()
        await send_step_prompt(message.chat.id, "symptoms")
        return

    if step == "symptoms":
        session["symptoms"] = text
        session["step"] = "wellbeing_energy"
        touch_session()
        await send_step_prompt(message.chat.id, "wellbeing_energy")
        return

    if step == "wellbeing_energy":
        session["wellbeing_energy"] = text
        session["step"] = "complaint_pattern"
        touch_session()
        await send_step_prompt(message.chat.id, "complaint_pattern")
        return

    if step == "complaint_pattern":
        session["complaint_pattern"] = text
        session["step"] = "goals"
        touch_session()
        await send_step_prompt(message.chat.id, "goals")
        return

    if step == "goals":
        session["goals"] = text
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
        session["step"] = "sleep_stress"
        touch_session()
        await send_step_prompt(message.chat.id, "sleep_stress")
        return

    if step == "sleep_stress":
        session["sleep_stress"] = text
        session["step"] = "activity"
        touch_session()
        await send_step_prompt(message.chat.id, "activity")
        return

    if step == "activity":
        session["activity"] = text
        session["step"] = "female_hormones"
        touch_session()
        await send_step_prompt(message.chat.id, "female_hormones")
        return

    if step == "female_hormones":
        session["female_hormones"] = text
        session["step"] = "emotional_stress"
        touch_session()
        await send_step_prompt(message.chat.id, "emotional_stress")
        return

    if step == "emotional_stress":
        session["emotional_stress"] = text
        session["step"] = "background"
        touch_session()
        await send_step_prompt(message.chat.id, "background")
        return

    if step == "background":
        session["background"] = text
        session["step"] = "risk_details"
        touch_session()
        await send_step_prompt(message.chat.id, "risk_details")
        return

    if step == "risk_details":
        session["risk_details"] = text
        session["step"] = "motivation"
        touch_session()
        await send_step_prompt(message.chat.id, "motivation")
        return

    if step == "motivation":
        session["motivation"] = text
        session["step"] = "red_flags"
        touch_session()
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
        session["step"] = "labs"
        touch_session()
        await send_step_prompt(message.chat.id, "labs")
        return

    if step == "labs":
        if session.get("lab_confirmation_status") == "pending_client_confirmation":
            if is_lab_confirmation_yes(text):
                mark_lab_confirmation(
                    session,
                    status="client_confirmed",
                    note="Клиент подтвердил, что OCR-распознавание анализов верно.",
                )
                session["requires_lab_resubmission"] = False
                session.pop("pending_biomarker_confirmation", None)
                session["contact"] = "telegram_current_chat"
                session["step"] = "done"
                touch_session()
                await message.answer(
                    "Спасибо, зафиксировала: распознанные показатели подтверждены вами. "
                    "Теперь я могу использовать их в разборе как подтверждённые клиентом данные."
                )
                await finalize_submission(message, session)
                return

            mark_lab_confirmation(
                session,
                status="client_correction_needed",
                note=f"Клиент не подтвердил OCR и прислал уточнение: {text}",
            )
            session["requires_lab_resubmission"] = True
            session["contact"] = "telegram_current_chat"
            session["step"] = "done"
            touch_session()
            await message.answer(
                "Принято. Я не буду использовать прежнее автоматическое распознавание как факт. "
                "Ваше уточнение сохранено, а показатели будут помечены как требующие ручной проверки."
            )
            await finalize_submission(message, session)
            return

        if text.lower() in SKIP_WORDS:
            session["lab_notes"] = "Клиент пропустил загрузку анализов на этом этапе."
            session["contact"] = "telegram_current_chat"
            session["step"] = "done"
            touch_session()
            await finalize_submission(message, session)
            return

        manual_structured = await parse_manual_biomarkers(text, settings)
        manual_biomarkers = manual_structured.get("biomarkers") or []
        session["lab_notes"] = text
        if manual_biomarkers:
            session.setdefault("parsed_biomarkers", []).extend(manual_biomarkers)
            mark_lab_confirmation(
                session,
                status="client_provided_text",
                note="Клиент вручную указал показатели анализов текстом; значения считаются клиентским вводом.",
            )
            session["lab_quality_check"] = {
                "status": manual_structured.get("quality_status", "manual_text_client_provided"),
                "requires_resubmission": False,
                "issues": [],
            }
            session["requires_lab_resubmission"] = False
        session["contact"] = "telegram_current_chat"
        session["step"] = "done"
        touch_session()
        if manual_biomarkers:
            await message.answer(
                "Принято. Я сохранил(а) показатели, которые вы написали текстом, как клиентский ввод. "
                "Если в какой-то цифре или единице измерения есть сомнение — лучше дослать PDF или уточнить отдельным сообщением."
            )
        else:
            await message.answer(
                "Принято. Я сохранил(а) текстовое описание анализов. Если захотите, позже можно дослать PDF или фото прямо в диалог."
            )
        await finalize_submission(message, session)
        return

    if step == "contact":
        session["contact"] = "telegram_current_chat" if text.strip() else "telegram_current_chat"
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

async def nurture_engine_loop():
    """Background task to gently remind users to complete their intake or upload labs."""
    import time
    logger.info("Nurture engine started.")
    while True:
        try:
            for user_id_str, session in list(user_sessions.items()):
                user_id = int(user_id_str)
                step = session.get("step")
                
                # Check if the user is stuck on 'labs'
                if step == "labs" and not session.get("nurture_sent"):
                    try:
                        name = session.get("full_name", "Здравствуйте").split(" ")[0]
                        await bot.send_message(
                            user_id,
                            f"{name}, я жду ваши результаты анализов, чтобы начать собирать стратегию. Если у вас возникли трудности с PDF-форматом — просто сфотографируйте бланки, и мой Vision AI всё распознает."
                        )
                        session["nurture_sent"] = True
                        touch_session()
                        logger.info("Nurture message sent to %s", user_id)
                    except Exception as e:
                        logger.error("Failed to send nurture to %s: %s", user_id, e)
        except Exception as e:
            logger.exception("Nurture engine error: %s", e)
            
        await asyncio.sleep(60 * 60) # Run every hour


async def send_product_digest_to_admins(payload: dict[str, Any]) -> bool:
    if not settings.admin_chat_ids:
        return False

    if not (payload.get("cases") or {}):
        return False

    digest_text = build_admin_digest_text(payload)
    delivered = False
    for admin_chat_id in settings.admin_chat_ids:
        try:
            await bot.send_message(admin_chat_id, digest_text)
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
        app.router.add_static("/static/", path="WellnessBot/static", name="static")
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
    logger.info("Starting Wellness Ecosystem (Bot + TMA Server)")
    restore_runtime_state()
    
    # Start Web Server
    app = await init_web_app()
    asyncio.create_task(nurture_engine_loop())
    asyncio.create_task(weekly_digest_loop())
    runner = web.AppRunner(app)
    await runner.setup()
    base_port = int(os.getenv("TMA_PORT", "8000"))
    last_error: OSError | None = None
    started_port: int | None = None
    for candidate_port in (base_port, base_port + 1, base_port + 2):
        try:
            site = web.TCPSite(runner, "localhost", candidate_port)
            await site.start()
            started_port = candidate_port
            break
        except OSError as exc:
            last_error = exc
            logger.warning("TMA bind failed on localhost:%s (%s). Trying next port.", candidate_port, exc)

    if started_port is None:
        raise last_error or RuntimeError("Failed to start TMA server")

    ACTIVE_TMA_PORT = started_port
    logger.info("TMA Server started at http://localhost:%s", started_port)
    
    # Start Bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




