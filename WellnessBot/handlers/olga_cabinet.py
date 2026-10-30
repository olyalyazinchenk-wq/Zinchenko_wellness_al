from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import struct
from typing import Any, Callable
import zlib

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup

from intake_schema import AdherenceEntry
from nutriok_product import PRIMARY_GOALS, get_product_offer, normalize_product_code
from nutriok_safety import evaluate_delivery_gate, find_red_flags
from storage import load_submission, save_submission


olga_cabinet_router = Router(name="olga_cabinet")

PENDING_REVIEW_STATUSES = {
    "awaiting_expert_review",
    "awaiting_safety_review",
    "awaiting_supplement_protocol_review",
    "changes_requested",
    "review_pending",
}


class _CabinetHooks:
    submissions_dir_getter: Callable[[], Path] | None = None
    is_admin_checker: Callable[[int], bool] | None = None


_hooks = _CabinetHooks()


def configure_olga_cabinet(
    *,
    submissions_dir_getter: Callable[[], Path],
    is_admin_checker: Callable[[int], bool],
) -> None:
    _hooks.submissions_dir_getter = submissions_dir_getter
    _hooks.is_admin_checker = is_admin_checker


def _parse_iso(ts_str: str | None) -> datetime | None:
    if not ts_str:
        return None
    clean = str(ts_str).strip()
    if clean.endswith("Z"):
        clean = clean[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(clean)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _iter_submissions(submissions_dir: Path) -> list[dict[str, Any]]:
    if not submissions_dir.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(submissions_dir.glob("*.json")):
        sub = load_submission(submissions_dir, path.stem)
        if isinstance(sub, dict):
            sub.setdefault("submission_id", path.stem)
            items.append(sub)
    return items


def build_admin_queue(
    submissions_dir: Path,
    *,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    ref_now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    queue: list[dict[str, Any]] = []

    for sub in _iter_submissions(submissions_dir):
        status = str(sub.get("intake_status") or sub.get("status") or "").strip()
        if status not in PENDING_REVIEW_STATUSES:
            continue

        sid = str(sub.get("submission_id") or "")
        intake = sub.get("intake") if isinstance(sub.get("intake"), dict) else {}
        raw_code = (
            sub.get("product_code")
            or intake.get("product_code")
            or sub.get("offer")
            or sub.get("tier")
            or "ok_review"
        )
        code = normalize_product_code(raw_code)
        offer = get_product_offer(code)
        created_dt = _parse_iso(sub.get("status_updated_at") or sub.get("created_at"))
        age_hours = (
            round(max(0.0, (ref_now - created_dt).total_seconds() / 3600.0), 1)
            if created_dt is not None
            else 0.0
        )
        red_flags = find_red_flags(sub)
        decision = evaluate_delivery_gate(code, str(sub.get("draft_text") or ""), sub)
        sla_overdue = age_hours >= 24.0
        goal_key = str(intake.get("primary_goal") or sub.get("primary_goal") or "energy")
        goal_label = PRIMARY_GOALS.get(goal_key, goal_key)

        queue.append(
            {
                "submission_id": sid,
                "product_code": code,
                "product_name": offer.name,
                "status": status,
                "goal_label": goal_label,
                "baseline_score": intake.get("baseline_score", sub.get("baseline_score", "—")),
                "age_hours": age_hours,
                "sla_overdue": sla_overdue,
                "red_flags": red_flags,
                "gate_reasons": list(decision.reasons),
                "pdf_path": str(sub.get("pdf_path") or ""),
                "submission": sub,
            }
        )

    queue.sort(
        key=lambda item: (
            0 if item["status"] == "awaiting_safety_review" or item["red_flags"] else 1,
            0 if item["sla_overdue"] else 1,
            -float(item["age_hours"]),
        )
    )
    return queue


def format_queue_summary(queue_items: list[dict[str, Any]]) -> str:
    if not queue_items:
        return "📋 <b>Очередь проверки НутриОК пуста</b>\n\nВсе кейсы проверены, просроченных SLA нет."

    overdue_count = sum(1 for item in queue_items if item["sla_overdue"])
    lines = [
        f"📋 <b>Очередь проверки Ольги Ковалевой ({len(queue_items)})</b>",
    ]
    if overdue_count:
        lines.append(f"⚠️ <b>Внимание:</b> {overdue_count} кейс(ов) ожидают дольше 24 ч (SLA)!")
    lines.append("")

    for idx, item in enumerate(queue_items[:15], start=1):
        sla_badge = "🔴 >24ч" if item["sla_overdue"] else "🟢 SLA"
        safety_badge = "🚨 SAFETY" if item["red_flags"] or item["status"] == "awaiting_safety_review" else "👩‍⚕️ Эксперт"
        lines.append(
            f"{idx}. <code>{item['submission_id']}</code> • <b>{item['product_name']}</b>\n"
            f"   {sla_badge} ({item['age_hours']} ч) | {safety_badge} | Цель: {item['goal_label']} ({item['baseline_score']}/10)"
        )
    return "\n".join(lines)


def build_queue_case_card(item: dict[str, Any]) -> tuple[str, InlineKeyboardMarkup]:
    sid = item["submission_id"]
    reasons_str = ", ".join(item["gate_reasons"]) if item["gate_reasons"] else "ручная проверка тарифа"
    flags_str = ", ".join(item["red_flags"]) if item["red_flags"] else "нет"
    pdf_ready = "да" if item["pdf_path"] and Path(item["pdf_path"]).exists() else "черновик"
    sla_note = "🔴 Ожидает > 24 ч (требуется приоритетный ответ)" if item["sla_overdue"] else f"🟢 В очереди {item['age_hours']} ч"

    text = (
        f"🗂 <b>Карточка кейса {sid}</b>\n\n"
        f"• <b>Тариф:</b> {item['product_name']} (<code>{item['product_code']}</code>)\n"
        f"• <b>Цель и точка А:</b> {item['goal_label']} ({item['baseline_score']}/10)\n"
        f"• <b>SLA:</b> {sla_note}\n"
        f"• <b>Красные флаги:</b> {flags_str}\n"
        f"• <b>Причины гейта:</b> {reasons_str}\n"
        f"• <b>Превью PDF:</b> {pdf_ready}"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{sid}"),
                InlineKeyboardButton(text="✏️ Нужны правки", callback_data=f"changes_{sid}"),
                InlineKeyboardButton(text="⛔ Отклонить", callback_data=f"reject_{sid}"),
            ]
        ]
    )
    return text, keyboard


def compute_funnel_stats(
    submissions_dir: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    ref_now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    cutoff_7d = ref_now - timedelta(days=7)
    cutoff_30d = ref_now - timedelta(days=30)

    tiers = ("ok_start", "ok_express", "ok_review", "ok_result_8", "ok_rhythm")
    counts_7d = {t: 0 for t in tiers}
    counts_30d = {t: 0 for t in tiers}
    counts_all = {t: 0 for t in tiers}

    for sub in _iter_submissions(submissions_dir):
        intake = sub.get("intake") if isinstance(sub.get("intake"), dict) else {}
        raw_code = (
            sub.get("product_code")
            or intake.get("product_code")
            or sub.get("offer")
            or sub.get("tier")
            or "ok_review"
        )
        code = normalize_product_code(raw_code)
        if code not in counts_all:
            continue
        counts_all[code] += 1
        created_dt = _parse_iso(sub.get("created_at") or sub.get("status_updated_at"))
        if created_dt is not None:
            if created_dt >= cutoff_7d:
                counts_7d[code] += 1
            if created_dt >= cutoff_30d:
                counts_30d[code] += 1

    queue = build_admin_queue(submissions_dir, now=ref_now)
    overdue = [item for item in queue if item["sla_overdue"]]

    return {
        "counts_7d": counts_7d,
        "counts_30d": counts_30d,
        "counts_all": counts_all,
        "queue_total": len(queue),
        "overdue_count": len(overdue),
        "overdue_ids": [item["submission_id"] for item in overdue],
    }


def format_stats_message(stats: dict[str, Any]) -> str:
    c7 = stats["counts_7d"]
    c30 = stats["counts_30d"]
    lines = [
        "📊 <b>Воронка НутриОК (7 и 30 дней)</b>",
        "",
        f"• <b>ОК-Старт:</b> 7д = {c7['ok_start']} | 30д = {c30['ok_start']}",
        f"• <b>ОК-Экспресс:</b> 7д = {c7['ok_express']} | 30д = {c30['ok_express']}",
        f"• <b>ОК-Разбор:</b> 7д = {c7['ok_review']} | 30д = {c30['ok_review']}",
        f"• <b>ОК-Результат 8:</b> 7д = {c7['ok_result_8']} | 30д = {c30['ok_result_8']}",
        f"• <b>ОК-Ритм:</b> 7д = {c7['ok_rhythm']} | 30д = {c30['ok_rhythm']}",
        "",
        f"⏳ <b>В очереди на проверку:</b> {stats['queue_total']}",
    ]
    if stats["overdue_count"] > 0:
        lines.append(
            f"⚠️ <b>SLA-напоминание (> 24 ч):</b> {stats['overdue_count']} кейс(ов) ждут проверки дольше 24 часов!"
        )
    else:
        lines.append("✅ <b>SLA (> 24 ч):</b> просроченных кейсов нет.")
    return "\n".join(lines)


def record_weekly_checkin(
    submissions_dir: Path,
    submission_id: str,
    *,
    week: int,
    metric_value: float,
    completed_actions: int,
    planned_actions: int = 7,
    notes: str = "",
) -> dict[str, Any]:
    sub = load_submission(submissions_dir, submission_id)
    if not isinstance(sub, dict):
        raise KeyError(f"Submission not found: {submission_id}")

    adherence_pct = round(
        (int(completed_actions) / max(1, int(planned_actions))) * 100.0,
        1,
    )
    entry = AdherenceEntry(
        week=int(week),
        adherence_pct=int(round(adherence_pct)),
        metric_value=float(metric_value),
        note=str(notes or "").strip(),
    )
    entry_dict = entry.to_dict()
    entry_dict["adherence_pct"] = adherence_pct
    entry_dict["completed_actions"] = int(completed_actions)
    entry_dict["planned_actions"] = int(planned_actions)

    history = sub.setdefault("adherence_history", [])
    if not isinstance(history, list):
        history = []
        sub["adherence_history"] = history
    history = [h for h in history if not (isinstance(h, dict) and int(h.get("week") or 0) == int(week))]
    history.append(entry_dict)
    history.sort(key=lambda h: int(h.get("week") or 0))
    sub["adherence_history"] = history

    intake = sub.setdefault("intake", {})
    if isinstance(intake, dict):
        intake["adherence_entries"] = list(history)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    adaptation_draft = (
        f"Черновик адаптации недели {week}: целевая метрика {metric_value}/10, "
        f"выполнение плана {int(completed_actions)}/{int(planned_actions)} ({adherence_pct}%). "
        f"{'Сохраняем текущий темп и закрепляем утренний белковый якорь.' if adherence_pct >= 70 else 'Упрощаем шаги до 1 главного действия в день.'}"
    )
    sub["weekly_adaptation_draft"] = adaptation_draft
    sub["intake_status"] = "awaiting_expert_review"
    sub["status_updated_at"] = now_iso

    save_submission(submissions_dir, submission_id, sub)
    return {
        "submission_id": submission_id,
        "entry": entry_dict,
        "adherence_pct": adherence_pct,
        "weekly_adaptation_draft": adaptation_draft,
        "intake_status": sub["intake_status"],
    }


def render_progress_chart_png(
    entries: list[dict[str, Any]],
    *,
    baseline_score: float = 4.0,
    width: int = 480,
    height: int = 240,
) -> bytes:
    """Render a clean RGB PNG bar chart of baseline + weekly metric scores (0..10) using stdlib zlib."""
    bg = (245, 241, 232)       # #f5f1e8 warm paper
    ink = (23, 25, 18)         # #171912 dark ink
    grid = (218, 212, 198)     # subtle grid line
    cobalt = (49, 84, 216)     # #3154d8 metric bar
    lime = (165, 214, 52)      # #c7f04b adherence accent

    points: list[tuple[float, float]] = [(max(0.0, min(10.0, float(baseline_score))), 100.0)]
    for item in entries[:8]:
        m_val = max(0.0, min(10.0, float(item.get("metric_value") or 0.0)))
        adh = float(item.get("adherence_pct") or 0.0)
        if not adh and item.get("planned_actions"):
            adh = (float(item.get("completed_actions") or 0.0) / max(1.0, float(item["planned_actions"]))) * 100.0
        points.append((m_val, max(0.0, min(100.0, adh))))

    margin_left = 36
    margin_right = 24
    margin_top = 24
    margin_bottom = 32
    plot_w = max(10, width - margin_left - margin_right)
    plot_h = max(10, height - margin_top - margin_bottom)

    n = len(points)
    slot_w = plot_w // max(1, n)
    bar_w = max(12, min(36, slot_w // 2))

    # Build pixel buffer
    rows: list[bytearray] = []
    for _ in range(height):
        row = bytearray(1 + width * 3)
        row[0] = 0  # filter type 0
        for x in range(width):
             idx = 1 + x * 3
             row[idx] = bg[0]
             row[idx + 1] = bg[1]
             row[idx + 2] = bg[2]
        rows.append(row)

    def _fill_rect(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        cx0 = max(0, min(width, x0))
        cx1 = max(0, min(width, x1))
        cy0 = max(0, min(height, y0))
        cy1 = max(0, min(height, y1))
        for y in range(cy0, cy1):
            r = rows[y]
            for x in range(cx0, cx1):
                p = 1 + x * 3
                r[p] = color[0]
                r[p + 1] = color[1]
                r[p + 2] = color[2]

    # Grid lines at 0%, 50%, 100%
    for frac in (0.0, 0.5, 1.0):
        gy = margin_top + int(plot_h * frac)
        _fill_rect(margin_left, gy, width - margin_right, gy + 1, grid)

    # Axis baseline
    _fill_rect(margin_left, margin_top + plot_h, width - margin_right, margin_top + plot_h + 2, ink)

    # Bars for each point
    for idx, (metric_val, adh_pct) in enumerate(points):
        center_x = margin_left + idx * slot_w + slot_w // 2
        bar_h = int((metric_val / 10.0) * plot_h)
        bx0 = center_x - bar_w // 2
        bx1 = center_x + bar_w // 2
        by0 = margin_top + plot_h - bar_h
        by1 = margin_top + plot_h
        color = ink if idx == 0 else cobalt
        _fill_rect(bx0, by0, bx1, by1, color)

        if idx > 0:
            adh_h = max(4, int((adh_pct / 100.0) * 8))
            _fill_rect(bx0, max(margin_top, by0 - adh_h - 2), bx1, max(margin_top, by0 - 2), lime)

    raw_data = b"".join(bytes(r) for r in rows)

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(raw_data, level=6)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")


@olga_cabinet_router.message(Command("queue"))
async def handle_queue_command(message: types.Message) -> None:
    user_id = int(message.from_user.id) if message.from_user else 0
    if not _hooks.is_admin_checker or not _hooks.is_admin_checker(user_id):
        await message.answer("Команда доступна только администратору.")
        return
    if not _hooks.submissions_dir_getter:
        return
    submissions_dir = _hooks.submissions_dir_getter()
    queue_items = build_admin_queue(submissions_dir)
    await message.answer(format_queue_summary(queue_items), parse_mode="HTML")
    for item in queue_items[:3]:
        card_text, kb = build_queue_case_card(item)
        await message.answer(card_text, reply_markup=kb, parse_mode="HTML")


@olga_cabinet_router.message(Command("stats"))
async def handle_stats_command(message: types.Message) -> None:
    user_id = int(message.from_user.id) if message.from_user else 0
    if not _hooks.is_admin_checker or not _hooks.is_admin_checker(user_id):
        await message.answer("Команда доступна только администратору.")
        return
    if not _hooks.submissions_dir_getter:
        return
    submissions_dir = _hooks.submissions_dir_getter()
    stats = compute_funnel_stats(submissions_dir)
    await message.answer(format_stats_message(stats), parse_mode="HTML")


@olga_cabinet_router.message(Command("checkin"))
async def handle_checkin_command(message: types.Message) -> None:
    """Format: /checkin <submission_id> <week> <metric_0_10> <completed_0_7> [notes]"""
    if not _hooks.submissions_dir_getter:
        return
    parts = (message.text or "").strip().split(maxsplit=5)
    if len(parts) < 5:
        await message.answer(
            "Формат еженедельного чек-ина:\n"
            "<code>/checkin &lt;id_кейса&gt; &lt;неделя&gt; &lt;метрика_0_10&gt; &lt;выполнено_шагов_из_7&gt; [заметка]</code>",
            parse_mode="HTML",
        )
        return
    _, sid, week_str, metric_str, completed_str = parts[:5]
    notes = parts[5] if len(parts) > 5 else ""
    try:
        submissions_dir = _hooks.submissions_dir_getter()
        res = record_weekly_checkin(
            submissions_dir,
            sid,
            week=int(week_str),
            metric_value=float(metric_str),
            completed_actions=int(completed_str),
            planned_actions=7,
            notes=notes,
        )
        sub = load_submission(submissions_dir, sid) or {}
        png_bytes = render_progress_chart_png(
            sub.get("adherence_history") or [],
            baseline_score=float(sub.get("baseline_score") or 4.0),
        )
        await message.answer_photo(
            BufferedInputFile(png_bytes, filename=f"progress_{sid}_w{week_str}.png"),
            caption=(
                f"📈 <b>Чек-ин недели {week_str} сохранён!</b>\n"
                f"• Метрика: <b>{metric_str}/10</b>\n"
                f"• Выполнение плана: <b>{res['adherence_pct']}%</b>\n\n"
                f"Черновик адаптации передан Ольге Ковалевой на проверку."
            ),
            parse_mode="HTML",
        )
    except Exception as exc:
        await message.answer(f"Не удалось сохранить чек-ин: {exc}")
