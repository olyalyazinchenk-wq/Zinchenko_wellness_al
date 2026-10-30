from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from intake_schema import (
    GOAL_DEFAULT_METRICS,
    GOAL_FIRST_SAFE_STEPS,
    DiaryDay,
    NutriOKIntake,
)
from nutriok_product import (
    PRIMARY_GOALS,
    get_product_offer,
    normalize_product_code,
)
from nutriok_safety import (
    RED_FLAG_CLIENT_MESSAGE,
    find_red_flags,
    is_underage,
)
from nutriok_texts import CONSENT_TEXT, TIER_DESCRIPTIONS


nutriok_router = Router(name="nutriok_intake")

NUTRIOK_TIER_CODES = {"ok_start", "ok_express", "ok_review", "ok_result_8", "ok_rhythm"}
MAIN_MENU_TEXTS = {
    "🔍 Диагностика симптомов (Бесплатно)",
    "🛍️ Выбрать программу",
    "📊 Мои отчеты",
    "📝 Заполнить анкету",
    "Продолжить анкету",
    "🩸 Сдать анализы",
    "💬 Задать вопрос эксперту",
    "🚨 Красные флаги",
}
ACTIVE_NUTRIOK_STEPS = {
    "consent",
    "goal",
    "baseline",
    "metric",
    "metric_custom",
    "diary_day_1",
    "diary_day_2",
    "diary_day_3",
    "context",
    "labs",
    "confirm",
}


class NutriOKIntakeStates(StatesGroup):
    consent = State()
    goal = State()
    baseline = State()
    metric = State()
    metric_custom = State()
    diary_day_1 = State()
    diary_day_2 = State()
    diary_day_3 = State()
    context = State()
    labs = State()
    confirm = State()


class _RuntimeHooks:
    get_session: Callable[[int], dict[str, Any] | None] | None = None
    start_session: Callable[..., dict[str, Any]] | None = None
    clear_session: Callable[[int], None] | None = None
    touch_session: Callable[[], None] | None = None
    save_submission_from_session: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    finalize_submission: Callable[[types.Message, dict[str, Any]], Awaitable[None]] | None = None
    transcribe_voice: Callable[[str], Awaitable[str | None]] | None = None
    notify_red_flag: Callable[[dict[str, Any], list[str]], Awaitable[None]] | None = None


_hooks = _RuntimeHooks()


def configure_nutriok_intake(
    *,
    get_session: Callable[[int], dict[str, Any] | None],
    start_session: Callable[..., dict[str, Any]],
    clear_session: Callable[[int], None],
    touch_session: Callable[[], None],
    save_submission_from_session: Callable[[dict[str, Any]], dict[str, Any]],
    finalize_submission: Callable[[types.Message, dict[str, Any]], Awaitable[None]],
    transcribe_voice: Callable[[str], Awaitable[str | None]],
    notify_red_flag: Callable[[dict[str, Any], list[str]], Awaitable[None]] | None = None,
) -> None:
    _hooks.get_session = get_session
    _hooks.start_session = start_session
    _hooks.clear_session = clear_session
    _hooks.touch_session = touch_session
    _hooks.save_submission_from_session = save_submission_from_session
    _hooks.finalize_submission = finalize_submission
    _hooks.transcribe_voice = transcribe_voice
    _hooks.notify_red_flag = notify_red_flag


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_progress_header(step_index: int, total_steps: int) -> str:
    filled = max(1, min(step_index, total_steps))
    dots = ["●"] * filled + ["○"] * max(0, total_steps - filled)
    return f"{' '.join(dots)}  Шаг {filled} из {total_steps}"


def _step_progress(product_code: str, step: str) -> tuple[int, int]:
    code = "ok_start" if product_code == "ok_start" else normalize_product_code(product_code)
    if code == "ok_start":
        mapping = {"consent": 1, "goal": 2, "baseline": 3}
        return mapping.get(step, 1), 3

    has_labs = get_product_offer(code).labs_supported
    total = 8 if has_labs else 7
    mapping_paid = {
        "consent": 1,
        "goal": 2,
        "baseline": 3,
        "metric": 4,
        "metric_custom": 4,
        "diary_day_1": 5,
        "diary_day_2": 5,
        "diary_day_3": 5,
        "context": 6,
        "labs": 7,
        "confirm": total,
    }
    return mapping_paid.get(step, 1), total


def _load_intake_from_session(session: dict[str, Any]) -> NutriOKIntake:
    raw = session.get("nutriok_intake")
    raw_tier = str(session.get("tier") or session.get("offer") or "ok_start")
    code = "ok_start" if raw_tier in {"ok_start", "screening"} else normalize_product_code(raw_tier)
    if isinstance(raw, dict):
        intake = NutriOKIntake.from_dict(raw)
        intake.product_code = code
        return intake
    return NutriOKIntake(product_code=code)


def _sync_intake_to_session(session: dict[str, Any], intake: NutriOKIntake, *, step: str) -> None:
    intake_dict = intake.to_dict()
    session["flow"] = "nutriok"
    session["nutriok_step"] = step
    session["step"] = f"nutriok_{step}"
    session["nutriok_intake"] = intake_dict
    session["primary_goal"] = intake.primary_goal
    session["goals"] = PRIMARY_GOALS.get(str(intake.primary_goal or ""), intake.primary_goal or "")
    session["baseline_score"] = intake.baseline_score
    session["goal_metric"] = intake.goal_metric
    session["nutrition_diary"] = intake_dict["nutrition_diary"]
    session["nutrition"] = "\n".join(
        f"День {d.day_index}: {d.meals_text}" for d in intake.nutrition_diary if d.meals_text
    )
    session["symptoms"] = intake.symptoms
    session["medications"] = intake.medications
    session["allergies"] = intake.allergies
    session["lifestyle"] = intake.lifestyle
    session["work_lifestyle"] = intake.lifestyle
    session["background"] = (
        f"Лекарства/БАДы: {intake.medications or 'нет'}. "
        f"Аллергии: {intake.allergies or 'нет'}."
    )
    session["adult_confirmed"] = intake.adult_confirmed
    session["pd_consent_at"] = intake.pd_consent_at
    session["consent_given"] = bool(intake.pd_consent_at and intake.adult_confirmed)
    if _hooks.touch_session:
        _hooks.touch_session()
    if _hooks.save_submission_from_session:
        _hooks.save_submission_from_session(session)


def _consent_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Мне 18+, даю согласие (152-ФЗ)",
                    callback_data="ok_consent_accept",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отказаться",
                    callback_data="ok_consent_decline",
                )
            ],
        ]
    )


def _goal_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=f"ok_goal_{key}")]
        for key, label in PRIMARY_GOALS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _baseline_keyboard() -> InlineKeyboardMarkup:
    row1 = [InlineKeyboardButton(text=str(i), callback_data=f"ok_baseline_{i}") for i in range(0, 6)]
    row2 = [InlineKeyboardButton(text=str(i), callback_data=f"ok_baseline_{i}") for i in range(6, 11)]
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2])


def _metric_keyboard(goal_key: str | None) -> InlineKeyboardMarkup:
    default_metric = GOAL_DEFAULT_METRICS.get(str(goal_key or ""), "оценка цели 0–10")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"✅ Использовать: «{default_metric}»",
                    callback_data="ok_metric_default",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Свой вариант метрики",
                    callback_data="ok_metric_custom",
                )
            ],
        ]
    )


def _labs_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Готово, перейти к проверке", callback_data="ok_labs_done")],
            [InlineKeyboardButton(text="⏭ Пропустить анализы", callback_data="ok_labs_skip")],
        ]
    )


def _confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Отправить", callback_data="ok_confirm_submit")],
            [InlineKeyboardButton(text="✏️ Изменить", callback_data="ok_confirm_edit")],
        ]
    )


def _build_summary_text(intake: NutriOKIntake) -> str:
    step_idx, total = _step_progress(intake.product_code, "confirm")
    header = format_progress_header(step_idx, total)
    offer = get_product_offer(intake.product_code)
    goal_label = PRIMARY_GOALS.get(str(intake.primary_goal or ""), str(intake.primary_goal or "—"))
    diary_lines = []
    for day in intake.nutrition_diary:
        photos_note = f" (фото: {len(day.photo_file_ids)})" if day.photo_file_ids else ""
        diary_lines.append(f"• День {day.day_index}: {day.meals_text or 'фото'}{photos_note}")
    diary_block = "\n".join(diary_lines) if diary_lines else "—"

    return (
        f"<b>{header}</b>\n\n"
        f"📋 <b>Проверьте анкету перед отправкой ({offer.name}):</b>\n\n"
        f"🎯 <b>Главная цель:</b> {goal_label}\n"
        f"📊 <b>Точка А (0–10):</b> {intake.baseline_score}\n"
        f"📏 <b>Метрика прогресса:</b> {intake.goal_metric or '—'}\n\n"
        f"🍽 <b>Дневник питания за 3 дня:</b>\n{diary_block}\n\n"
        f"🩺 <b>Симптомы:</b> {intake.symptoms or 'нет'}\n"
        f"💊 <b>Лекарства и БАДы:</b> {intake.medications or 'нет'}\n"
        f"🌿 <b>Аллергии и непереносимости:</b> {intake.allergies or 'нет'}\n"
        f"🏃‍♀️ <b>Образ жизни:</b> {intake.lifestyle or 'нет'}\n"
        f"🧪 <b>Файлов анализов:</b> {len(intake.labs_upload_ids)}"
    )


async def send_current_nutriok_step_prompt(
    target: types.Message | types.CallbackQuery,
    session: dict[str, Any],
) -> None:
    intake = _load_intake_from_session(session)
    step = str(session.get("nutriok_step") or "consent")
    step_idx, total = _step_progress(intake.product_code, step)
    header = format_progress_header(step_idx, total)

    send_fn = (
        target.message.answer
        if hasattr(target, "message") and getattr(target, "message") is not None
        else target.answer
    )

    if step == "consent":
        await send_fn(
            f"<b>{header}</b>\n\n{CONSENT_TEXT}\n\n"
            "Для продолжения подтвердите, что вам исполнилось 18 лет и вы даёте согласие на обработку персональных данных (152-ФЗ).",
            reply_markup=_consent_keyboard(),
            parse_mode="HTML",
        )
    elif step == "goal":
        await send_fn(
            f"<b>{header}</b>\n\n"
            "Выберите <b>одну главную цель</b>, на которой сфокусируемся в первую очередь:",
            reply_markup=_goal_keyboard(),
            parse_mode="HTML",
        )
    elif step == "baseline":
        goal_label = PRIMARY_GOALS.get(str(intake.primary_goal or ""), "выбранной цели")
        await send_fn(
            f"<b>{header}</b>\n\n"
            f"Оцените вашу текущую точку А по цели «<b>{goal_label}</b>» от 0 до 10\n"
            "<i>(0 — совсем плохо / выраженный дискомфорт, 10 — отличное состояние)</i>:",
            reply_markup=_baseline_keyboard(),
            parse_mode="HTML",
        )
    elif step == "metric":
        default_metric = GOAL_DEFAULT_METRICS.get(str(intake.primary_goal or ""), "оценка цели 0–10")
        await send_fn(
            f"<b>{header}</b>\n\n"
            "Выберите <b>метрику</b>, по которой мы будем отслеживать реальные изменения каждую неделю.\n"
            f"Рекомендуемая метрика: <b>{default_metric}</b>",
            reply_markup=_metric_keyboard(intake.primary_goal),
            parse_mode="HTML",
        )
    elif step == "metric_custom":
        await send_fn(
            f"<b>{header}</b>\n\n"
            "Напишите одним сообщением вашу метрику для отслеживания прогресса "
            "(например: <i>«уровень бодрости после обеда 0–10»</i>):",
            parse_mode="HTML",
        )
    elif step in {"diary_day_1", "diary_day_2", "diary_day_3"}:
        day_num = int(step.rsplit("_", 1)[-1])
        await send_fn(
            f"<b>{header}</b>\n\n"
            f"🍽 <b>Дневник питания — День {day_num} из 3</b>\n\n"
            "Опишите всё, что вы ели и пили за этот день (завтрак, обед, ужин, перекусы, кофе/вода и время приёмов).\n"
            "Можно отправить <b>текстом</b>, <b>голосовым сообщением</b> или <b>фотографией с подписью</b>.",
            parse_mode="HTML",
        )
    elif step == "context":
        await send_fn(
            f"<b>{header}</b>\n\n"
            "🩺 <b>Контекст здоровья и образа жизни</b>\n\n"
            "Напишите одним сообщением (можно коротко, «нет» допустимо):\n"
            "1. Симптомы и жалобы\n"
            "2. Принимаемые лекарства и БАДы\n"
            "3. Аллергии и непереносимости\n"
            "4. Режим сна, работа и уровень стресса",
            parse_mode="HTML",
        )
    elif step == "labs":
        await send_fn(
            f"<b>{header}</b>\n\n"
            "🧪 <b>Анализы и исследования (по желанию)</b>\n\n"
            "Пришлите PDF или фото имеющихся анализов (включая ХМС по Осипову, если есть), "
            "затем нажмите «Готово», либо нажмите «Пропустить анализы».",
            reply_markup=_labs_keyboard(),
            parse_mode="HTML",
        )
    elif step == "confirm":
        await send_fn(
            _build_summary_text(intake),
            reply_markup=_confirm_keyboard(),
            parse_mode="HTML",
        )


def _is_active_nutriok_session(user_id: int, expected_steps: set[str] | None = None) -> bool:
    if not _hooks.get_session:
        return False
    session = _hooks.get_session(user_id)
    if not session or session.get("flow") != "nutriok":
        return False
    step = str(session.get("nutriok_step") or "")
    if expected_steps is not None:
        return step in expected_steps
    return step in ACTIVE_NUTRIOK_STEPS


def _extract_tier_code(data: str) -> str | None:
    if data.startswith("tier_"):
        raw = data[len("tier_"):]
    elif data.startswith("ok_select_"):
        raw = data[len("ok_select_"):]
    else:
        raw = data
    if raw in NUTRIOK_TIER_CODES:
        return raw
    return None


@nutriok_router.callback_query(
    lambda c: c.data is not None and _extract_tier_code(c.data) is not None
)
async def handle_nutriok_tier_start(callback_query: types.CallbackQuery) -> None:
    tier = _extract_tier_code(callback_query.data or "") or "ok_start"
    if not _hooks.start_session:
        return

    session = _hooks.start_session(callback_query.from_user, tier=tier)
    intake = NutriOKIntake(product_code=tier)
    _sync_intake_to_session(session, intake, step="consent")

    desc = TIER_DESCRIPTIONS.get(tier, TIER_DESCRIPTIONS["ok_review"])
    await callback_query.message.answer(desc, parse_mode="HTML")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


@nutriok_router.message(Command("continue"))
async def handle_continue_command(message: types.Message) -> None:
    session = _hooks.get_session(message.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok" or session.get("nutriok_step") not in ACTIVE_NUTRIOK_STEPS:
        await message.answer(
            "У вас нет незавершённой анкеты НутриОК. Выберите формат через /start.",
        )
        return
    await send_current_nutriok_step_prompt(message, session)


@nutriok_router.callback_query(F.data == "ok_continue")
async def handle_continue_callback(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok" or session.get("nutriok_step") not in ACTIVE_NUTRIOK_STEPS:
        await callback_query.answer("Незавершённая анкета не найдена.", show_alert=True)
        return
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


@nutriok_router.message(
    lambda m: bool(
        m.text
        and m.text.strip() in {"Продолжить анкету", "📝 Заполнить анкету"}
        and _is_active_nutriok_session(m.from_user.id)
    )
)
async def handle_continue_button_text(message: types.Message) -> None:
    session = _hooks.get_session(message.from_user.id)
    if session:
        await send_current_nutriok_step_prompt(message, session)


@nutriok_router.callback_query(F.data == "ok_consent_accept")
async def handle_consent_accept(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена. Начните с /start.", show_alert=True)
        return

    intake = _load_intake_from_session(session)
    intake.adult_confirmed = True
    intake.pd_consent_at = utc_now_iso()
    _sync_intake_to_session(session, intake, step="goal")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer("Согласие принято")


@nutriok_router.callback_query(F.data == "ok_consent_decline")
async def handle_consent_decline(callback_query: types.CallbackQuery) -> None:
    if _hooks.clear_session:
        _hooks.clear_session(callback_query.from_user.id)
    await callback_query.message.answer(
        "Вы отказались от обработки данных. Без согласия и подтверждения 18+ мы не можем собирать анкету. "
        "Если передумаете — нажмите /start."
    )
    await callback_query.answer()


@nutriok_router.callback_query(lambda c: bool(c.data and c.data.startswith("ok_goal_")))
async def handle_goal_select(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена. Начните с /start.", show_alert=True)
        return

    goal_key = (callback_query.data or "").replace("ok_goal_", "", 1)
    if goal_key not in PRIMARY_GOALS:
        await callback_query.answer("Неизвестная цель.", show_alert=True)
        return

    intake = _load_intake_from_session(session)
    intake.primary_goal = goal_key
    intake.goal_metric = GOAL_DEFAULT_METRICS.get(goal_key, intake.goal_metric)
    _sync_intake_to_session(session, intake, step="baseline")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


@nutriok_router.callback_query(lambda c: bool(c.data and c.data.startswith("ok_baseline_")))
async def handle_baseline_select(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена. Начните с /start.", show_alert=True)
        return

    raw_score = (callback_query.data or "").replace("ok_baseline_", "", 1)
    try:
        score = int(raw_score)
    except ValueError:
        await callback_query.answer("Укажите число от 0 до 10.", show_alert=True)
        return
    if not 0 <= score <= 10:
        await callback_query.answer("Оценка должна быть от 0 до 10.", show_alert=True)
        return

    intake = _load_intake_from_session(session)
    intake.baseline_score = score

    # ok_start finishes right after baseline with one safe step + Express offer
    if intake.product_code == "ok_start":
        errors = intake.validation_errors()
        if errors:
            await callback_query.message.answer("\n".join(errors))
            await callback_query.answer()
            return
        _sync_intake_to_session(session, intake, step="done")
        goal_label = PRIMARY_GOALS.get(str(intake.primary_goal or ""), "выбранная цель")
        first_step = GOAL_FIRST_SAFE_STEPS.get(
            str(intake.primary_goal or "energy"),
            GOAL_FIRST_SAFE_STEPS["energy"],
        )
        offer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Перейти к ОК-Экспресс — 990 ₽",
                        callback_data="tier_ok_express",
                    )
                ]
            ]
        )
        await callback_query.message.answer(
            f"✅ <b>ОК-Старт завершён!</b>\n\n"
            f"🎯 <b>Ваша цель:</b> {goal_label}\n"
            f"📊 <b>Исходная точка:</b> {score}/10\n\n"
            f"🌿 <b>Ваш безопасный первый шаг на сегодня:</b>\n{first_step}\n\n"
            "Чтобы увидеть 3 ключевых паттерна по вашему реальному питанию за 3 дня и получить "
            "пошаговый план на 7 дней, переходите к формату <b>ОК-Экспресс (990 ₽)</b>:",
            reply_markup=offer_kb,
            parse_mode="HTML",
        )
        await callback_query.answer()
        return

    _sync_intake_to_session(session, intake, step="metric")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


@nutriok_router.callback_query(F.data == "ok_metric_default")
async def handle_metric_default(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена.", show_alert=True)
        return

    intake = _load_intake_from_session(session)
    intake.goal_metric = GOAL_DEFAULT_METRICS.get(str(intake.primary_goal or ""), "оценка цели 0–10")
    _sync_intake_to_session(session, intake, step="diary_day_1")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


@nutriok_router.callback_query(F.data == "ok_metric_custom")
async def handle_metric_custom_prompt(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена.", show_alert=True)
        return

    intake = _load_intake_from_session(session)
    _sync_intake_to_session(session, intake, step="metric_custom")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


@nutriok_router.message(
    lambda m: bool(
        m.from_user
        and m.text
        and not m.text.startswith("/")
        and m.text.strip() not in MAIN_MENU_TEXTS
        and _is_active_nutriok_session(m.from_user.id, {"metric", "metric_custom"})
    )
)
async def handle_metric_text(message: types.Message) -> None:
    session = _hooks.get_session(message.from_user.id)
    if not session:
        return
    metric_text = (message.text or "").strip()
    if not metric_text:
        await message.answer("Пожалуйста, укажите метрику текстом.")
        return

    intake = _load_intake_from_session(session)
    intake.goal_metric = metric_text
    _sync_intake_to_session(session, intake, step="diary_day_1")
    await send_current_nutriok_step_prompt(message, session)


def _upsert_diary_day(
    intake: NutriOKIntake,
    day_index: int,
    *,
    meals_text: str = "",
    photo_file_id: str | None = None,
) -> None:
    existing_map = {d.day_index: d for d in intake.nutrition_diary}
    current = existing_map.get(day_index) or DiaryDay(day_index=day_index, meals_text="")
    if meals_text:
        current.meals_text = (
            f"{current.meals_text}\n{meals_text}".strip() if current.meals_text else meals_text.strip()
        )
    if photo_file_id and photo_file_id not in current.photo_file_ids:
        current.photo_file_ids.append(photo_file_id)
    if not current.meals_text and current.photo_file_ids:
        current.meals_text = "[Фото дневника питания]"
    existing_map[day_index] = current
    intake.nutrition_diary = [existing_map[k] for k in sorted(existing_map)]


def _next_step_after_diary(day_index: int) -> str:
    if day_index == 1:
        return "diary_day_2"
    if day_index == 2:
        return "diary_day_3"
    return "context"


@nutriok_router.message(
    lambda m: bool(
        m.from_user
        and (m.text or m.voice or m.photo)
        and not (m.text and (m.text.startswith("/") or m.text.strip() in MAIN_MENU_TEXTS))
        and _is_active_nutriok_session(
            m.from_user.id,
            {"diary_day_1", "diary_day_2", "diary_day_3"},
        )
    )
)
async def handle_diary_entry(message: types.Message) -> None:
    session = _hooks.get_session(message.from_user.id)
    if not session:
        return
    step = str(session.get("nutriok_step") or "diary_day_1")
    day_index = int(step.rsplit("_", 1)[-1])
    intake = _load_intake_from_session(session)

    meals_text = ""
    photo_id: str | None = None

    if message.voice:
        if _hooks.transcribe_voice:
            transcript = await _hooks.transcribe_voice(message.voice.file_id)
            if transcript and transcript.strip():
                meals_text = transcript.strip()
        if not meals_text:
            await message.answer(
                "Не удалось распознать голосовое сообщение. Пожалуйста, напишите рацион за этот день текстом."
            )
            return
    elif message.photo:
        photo_id = message.photo[-1].file_id
        meals_text = (message.caption or "").strip()
    elif message.text:
        meals_text = message.text.strip()

    if not meals_text and not photo_id:
        await message.answer("Пожалуйста, отправьте описание питания текстом, голосом или фото.")
        return

    _upsert_diary_day(intake, day_index, meals_text=meals_text, photo_file_id=photo_id)
    next_step = _next_step_after_diary(day_index)
    _sync_intake_to_session(session, intake, step=next_step)
    await send_current_nutriok_step_prompt(message, session)


def _parse_context_message(raw_text: str) -> tuple[str, str, str, str]:
    text = raw_text.strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) >= 4:
        return lines[0], lines[1], lines[2], " ".join(lines[3:])
    return text, text, "нет", text


@nutriok_router.message(
    lambda m: bool(
        m.from_user
        and m.text
        and not m.text.startswith("/")
        and m.text.strip() not in MAIN_MENU_TEXTS
        and _is_active_nutriok_session(m.from_user.id, {"context"})
    )
)
async def handle_context_entry(message: types.Message) -> None:
    session = _hooks.get_session(message.from_user.id)
    if not session:
        return
    raw_text = (message.text or "").strip()
    if not raw_text:
        await message.answer("Напишите контекст здоровья или «нет».")
        return

    intake = _load_intake_from_session(session)
    symptoms, medications, allergies, lifestyle = _parse_context_message(raw_text)
    intake.symptoms = symptoms
    intake.medications = medications
    intake.allergies = allergies
    intake.lifestyle = lifestyle

    probe_submission = {"intake": intake.to_dict(), "symptoms": symptoms, "medications": medications}
    if is_underage(probe_submission):
        intake.adult_confirmed = False
        _sync_intake_to_session(session, intake, step="stopped_underage")
        await message.answer(
            "Сервис НутриОК предназначен только для совершеннолетних (18+). "
            "Для подбора питания ребёнку или подростку, пожалуйста, обратитесь к врачу-педиатру."
        )
        if _hooks.notify_red_flag:
            await _hooks.notify_red_flag(session, ["underage_lt_18"])
        return

    red_flags = find_red_flags(probe_submission)
    if red_flags:
        session["red_flags"] = ", ".join(red_flags)
        await message.answer(RED_FLAG_CLIENT_MESSAGE)
        if _hooks.notify_red_flag:
            await _hooks.notify_red_flag(session, red_flags)

    offer = get_product_offer(intake.product_code)
    next_step = "labs" if offer.labs_supported else "confirm"
    _sync_intake_to_session(session, intake, step=next_step)
    await send_current_nutriok_step_prompt(message, session)


@nutriok_router.message(
    lambda m: bool(
        m.from_user
        and (m.document or m.photo)
        and _is_active_nutriok_session(m.from_user.id, {"labs"})
    )
)
async def handle_labs_upload(message: types.Message) -> None:
    session = _hooks.get_session(message.from_user.id)
    if not session:
        return
    intake = _load_intake_from_session(session)
    file_id = message.document.file_id if message.document else message.photo[-1].file_id
    if file_id not in intake.labs_upload_ids:
        intake.labs_upload_ids.append(file_id)
    session.setdefault("documents", []).append(
        {"kind": "nutriok_lab", "telegram_file_id": file_id}
    )
    _sync_intake_to_session(session, intake, step="labs")
    await message.answer(
        f"📎 Файл принят (всего загружено: {len(intake.labs_upload_ids)}). "
        "Можете отправить ещё файлы или нажать «Готово, перейти к проверке».",
        reply_markup=_labs_keyboard(),
    )


@nutriok_router.callback_query(F.data.in_({"ok_labs_done", "ok_labs_skip"}))
async def handle_labs_complete(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена.", show_alert=True)
        return
    intake = _load_intake_from_session(session)
    _sync_intake_to_session(session, intake, step="confirm")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer()


def _first_invalid_step(intake: NutriOKIntake) -> str:
    if not intake.adult_confirmed or not intake.pd_consent_at:
        return "consent"
    if intake.primary_goal not in PRIMARY_GOALS:
        return "goal"
    if intake.baseline_score is None or not (0 <= intake.baseline_score <= 10):
        return "baseline"
    if intake.product_code != "ok_start":
        if not str(intake.goal_metric or "").strip():
            return "metric"
        valid_days = [
            d for d in intake.nutrition_diary if d.meals_text.strip() or d.photo_file_ids
        ]
        if len(valid_days) < 3:
            return f"diary_day_{min(3, len(valid_days) + 1)}"
    return "goal"


@nutriok_router.callback_query(F.data == "ok_confirm_edit")
async def handle_confirm_edit(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена.", show_alert=True)
        return
    intake = _load_intake_from_session(session)
    _sync_intake_to_session(session, intake, step="goal")
    await send_current_nutriok_step_prompt(callback_query, session)
    await callback_query.answer("Возвращаемся к редактированию")


@nutriok_router.callback_query(F.data == "ok_confirm_submit")
async def handle_confirm_submit(callback_query: types.CallbackQuery) -> None:
    session = _hooks.get_session(callback_query.from_user.id) if _hooks.get_session else None
    if not session or session.get("flow") != "nutriok":
        await callback_query.answer("Сессия не найдена.", show_alert=True)
        return

    intake = _load_intake_from_session(session)
    errors = intake.validation_errors()
    if errors:
        return_step = _first_invalid_step(intake)
        _sync_intake_to_session(session, intake, step=return_step)
        await callback_query.message.answer(
            "⚠️ Не все обязательные поля заполнены:\n• " + "\n• ".join(errors)
        )
        await send_current_nutriok_step_prompt(callback_query, session)
        await callback_query.answer("Нужно дополнить анкету", show_alert=True)
        return

    _sync_intake_to_session(session, intake, step="awaiting_product_payment")
    session["step"] = "awaiting_product_payment"
    if _hooks.touch_session:
        _hooks.touch_session()
    if _hooks.save_submission_from_session:
        _hooks.save_submission_from_session(session)

    await callback_query.answer("Анкета отправлена!")
    if _hooks.finalize_submission:
        await _hooks.finalize_submission(callback_query.message, session)
