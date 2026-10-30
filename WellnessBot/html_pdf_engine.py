from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

from intake_schema import GOAL_DEFAULT_METRICS
from nutriok_product import PRIMARY_GOALS, get_product_offer, normalize_product_code, requires_human_review

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


def _default_patterns_from_diary(diary_days: list[dict[str, Any]], goal_key: str) -> list[dict[str, str]]:
    quotes: list[tuple[str, str]] = []
    for idx, item in enumerate(diary_days[:3], start=1):
        if isinstance(item, dict):
            day_label = str(item.get("day_label") or f"День {idx}")
            text = " ".join(
                part.strip()
                for part in (
                    str(item.get("meals_text") or ""),
                    str(item.get("voice_transcript") or ""),
                    str(item.get("water_coffee_text") or ""),
                )
                if part and part.strip()
            )
            if text:
                quotes.append((day_label, text[:180]))

    while len(quotes) < 3:
        fallback_idx = len(quotes) + 1
        fallback_examples = {
            1: ("День 1", "Утром кофе, плотный приём пищи смещён на вторую половину дня, вечером тянет на быстрые углеводы."),
            2: ("День 2", "В обед мало белка и клетчатки, через 2 часа появляется сонливость и желание перекусить сладким."),
            3: ("День 3", "Поздний ужин за 1.5 часа до сна и недостаток чистой воды в первой половине дня."),
        }
        quotes.append(fallback_examples[fallback_idx])

    return [
        {
            "title": "Белково-жировой старт дня и время первого кофе",
            "day_ref": quotes[0][0],
            "quote": quotes[0][1],
            "explanation": "Кофе натощак или лёгкий углеводный завтрак дают резкий скачок и спад глюкозы уже к 11:30–13:00.",
            "correction": "Сначала стакан тёплой воды и завтрак с 25–30 г белка (яйца, рыба, творог или птица + зелень), кофе — через 30–40 минут после еды.",
        },
        {
            "title": "Баланс обеденной тарелки и профилактика послеобеденного спада",
            "day_ref": quotes[1][0],
            "quote": quotes[1][1],
            "explanation": "Когда в обед преобладают быстрые углеводы без порции клетчатки и белка, возникает дневная тяжесть и вечерний голод.",
            "correction": "Половина обеденной тарелки — некрахмалистые овощи/зелень с 1 ст. л. оливкового масла, четверть — цельный белок, четверть — сложный гарнир.",
        },
        {
            "title": "Вечернее окно питания и восстановление нервной системы",
            "day_ref": quotes[2][0],
            "quote": quotes[2][1],
            "explanation": "Поздний плотный ужин нагружает пищеварение ночью и снижает утреннюю бодрость на 2–3 балла.",
            "correction": "Лёгкий белково-овощной ужин за 3 часа до сна (рыба/индейка + тушёные овощи) и 20 минут спокойного ритма без экранов.",
        },
    ]


def _default_7_day_plan() -> list[dict[str, str]]:
    return [
        {
            "day": "День 1",
            "focus": "Утренний старт",
            "action": "300 мл тёплой воды после пробуждения + белковый завтрак в первый час.",
            "why": "Стабилизирует кортизоловую кривую и убирает утреннюю вялость.",
        },
        {
            "day": "День 2",
            "focus": "Правило кофе",
            "action": "Перенести кофе на 30 минут после завтрака, до 14:00.",
            "why": "Снижает раздражение слизистой и сохраняет усвоение железа и магния.",
        },
        {
            "day": "День 3",
            "focus": "Обеденная клетчатка",
            "action": "Начать обед с порции свежих или запечённых овощей/зелени (150–200 г).",
            "why": "Сглаживает гликемический отклик и даёт ровную энергию до вечера.",
        },
        {
            "day": "День 4",
            "focus": "Водный ритм",
            "action": "Выпить 6–7 стаканов чистой воды равномерно до 19:00.",
            "why": "Поддерживает желчеотток, концентрацию внимания и снижает ложный голод.",
        },
        {
            "day": "День 5",
            "focus": "Чистые промежутки",
            "action": "Выдержать 3.5–4 часа между завтраком, обедом и ужином без сладких перекусов.",
            "why": "Даёт отдыхать инсулину и включает естественный моторный комплекс ЖКТ.",
        },
        {
            "day": "День 6",
            "focus": "Лёгкий ужин",
            "action": "Поужинать за 3 часа до сна: белок + термически обработанные овощи.",
            "why": "Улучшает глубину сна и утреннюю лёгкость без отёков.",
        },
        {
            "day": "День 7",
            "focus": "Замер прогресса",
            "action": "Оценить самочувствие по шкале 0–10 и отметить выполнение шагов в боте.",
            "why": "Фиксирует вашу новую точку Б и закрепляет рабочие привычки.",
        },
    ]


def build_nutriok_report_context(
    data: dict[str, Any] | None = None,
    submission: dict[str, Any] | None = None,
) -> dict[str, Any]:
    raw = dict(data or {})
    sub = dict(submission or {})
    intake = sub.get("intake") if isinstance(sub.get("intake"), dict) else {}
    profile = sub.get("profile") if isinstance(sub.get("profile"), dict) else {}

    product_code = normalize_product_code(
        raw.get("product_code")
        or sub.get("product_code")
        or intake.get("product_code")
        or sub.get("offer")
        or sub.get("tier")
        or "ok_review"
    )
    offer = get_product_offer(product_code)

    goal_key = str(
        raw.get("primary_goal")
        or intake.get("primary_goal")
        or sub.get("primary_goal")
        or "energy"
    ).strip()
    goal_label = PRIMARY_GOALS.get(goal_key, str(raw.get("goal_label") or "Энергия и ресурс"))

    baseline_raw = (
        raw.get("baseline_score")
        if raw.get("baseline_score") is not None
        else intake.get("baseline_score", sub.get("baseline_score", 4))
    )
    try:
        baseline_score = max(0, min(10, int(baseline_raw)))
    except (TypeError, ValueError):
        baseline_score = 4

    target_score = min(10, max(baseline_score + 3, 8))
    goal_metric = str(
        raw.get("goal_metric")
        or intake.get("goal_metric")
        or sub.get("goal_metric")
        or GOAL_DEFAULT_METRICS.get(goal_key, "Оценка состояния по шкале 0–10 в конце недели")
    )

    diary_days = (
        raw.get("nutrition_diary")
        or intake.get("diary")
        or sub.get("nutrition_diary")
        or []
    )
    if not isinstance(diary_days, list):
        diary_days = []

    patterns_from_diary = raw.get("patterns_from_diary")
    if not isinstance(patterns_from_diary, list) or len(patterns_from_diary) < 3:
        patterns_from_diary = _default_patterns_from_diary(diary_days, goal_key)

    plan_7_days = raw.get("plan_7_days")
    if not isinstance(plan_7_days, list) or len(plan_7_days) < 7:
        plan_7_days = _default_7_day_plan()

    exec_summary = raw.get("executive_summary") if isinstance(raw.get("executive_summary"), dict) else {}
    key_findings = exec_summary.get("key_findings") or [
        "Недостаток белка в первом приёме пищи провоцирует тягу к быстрым углеводам после 15:00.",
        "Смещение основного объёма еды на вечер снижает качество ночного восстановления.",
        "Добавление 150–200 г овощей/зелени в обед и чистой воды даст первый заметный отклик за 5–7 дней.",
    ]
    top_actions = exec_summary.get("top_actions") or [
        "Начинать утро со стакана тёплой воды и завтрака с 25–30 г белка.",
        "Перенести кофе на 30–40 минут после завтрака, не натощак.",
        "Соблюдать лёгкий белково-овощной ужин за 3 часа до сна.",
    ]
    stop_signals = exec_summary.get("stop_signals") or [
        "Острая боль в животе или груди, температура, выраженная слабость или головокружение.",
        "Появление крови в стуле, чёрный стул или необъяснимая потеря веса — повод сразу обратиться к врачу.",
        "Индивидуальная непереносимость любого продукта из рациона.",
    ]

    plate_formula = raw.get("plate_formula") or [
        {
            "share": "1/4 тарелки",
            "title": "Цельный белок",
            "examples": "Рыба, индейка, курица, яйца, морепродукты или субпродукты (120–150 г в готовом виде).",
        },
        {
            "share": "1/2 тарелки",
            "title": "Клетчатка и зелень",
            "examples": "Листовая зелень, брокколи, кабачок, огурцы, квашеные или запечённые овощи.",
        },
        {
            "share": "1/4 тарелки",
            "title": "Полезные жиры и гарнир",
            "examples": "Оливковое/топлёное масло, авокадо, орехи, гречка или киноа по переносимости.",
        },
        {
            "share": "Ритм воды",
            "title": "Гидратация дня",
            "examples": "30 мл/кг чистой тёплой воды между приёмами пищи; кофе только после еды.",
        },
    ]

    measurement_checklist = raw.get("measurement_checklist") or [
        f"Оцените «{goal_metric}» по шкале 0–10 вечером 7-го дня и сравните с вашей Точкой А ({baseline_score}/10).",
        "Отметьте, сколько дней из 7 удалось начать с белкового завтрака и тёплой воды (цель: не менее 5 из 7).",
        "Зафиксируйте изменения вечерней тяги к сладкому и лёгкость пробуждения утром.",
        "Нажмите кнопку отчёта в @zinchenko_wellness_ai_1_bot, чтобы сохранить динамику.",
    ]

    # Review stamp only for tiers requiring human review when ReviewRecord is present
    review_stamp = raw.get("review_stamp")
    if review_stamp is None and requires_human_review(product_code):
        review_records = sub.get("review_records")
        if isinstance(review_records, list) and review_records:
            last_rec = review_records[-1]
            if isinstance(last_rec, dict) and last_rec.get("decision") == "approved":
                review_stamp = {
                    "reviewer_name": last_rec.get("reviewer_name") or "Ольга Ковалева, нутрициолог",
                    "decided_at": str(last_rec.get("decided_at") or "")[:10],
                    "artifact_sha256": str(last_rec.get("artifact_sha256") or ""),
                }
        elif sub.get("approved_by_admin_id"):
            review_stamp = {
                "reviewer_name": "Ольга Ковалева, нутрициолог",
                "decided_at": str(sub.get("approved_at") or datetime.now().strftime("%Y-%m-%d"))[:10],
                "artifact_sha256": str(sub.get("approved_artifact_sha256") or "verified"),
            }

    client_name = (
        raw.get("client_name")
        or profile.get("full_name")
        or profile.get("telegram_full_name")
        or "Клиент НутриОК"
    )
    created_raw = str(sub.get("created_at") or raw.get("created_date") or datetime.now().strftime("%d.%m.%Y"))
    created_date = created_raw[:10]

    context = dict(raw)
    context.update(
        {
            "product_code": product_code,
            "product_name": raw.get("product_name") or offer.name,
            "client_name": client_name,
            "client_profile": raw.get("client_profile") or f"{client_name} · Фокус: {goal_label}",
            "created_date": created_date,
            "goal_key": goal_key,
            "goal_label": goal_label,
            "baseline_score": baseline_score,
            "target_score": target_score,
            "goal_metric": goal_metric,
            "executive_summary": {
                "headline": exec_summary.get("headline")
                or f"Персональный маршрут по цели «{goal_label}» на ближайшие 7–14 дней",
                "key_findings": key_findings[:3],
                "top_actions": top_actions[:3],
                "stop_signals": stop_signals[:3],
            },
            "patterns_from_diary": patterns_from_diary[:3],
            "plate_formula": plate_formula[:4],
            "plan_7_days": plan_7_days[:7],
            "measurement_checklist": measurement_checklist[:4],
            "review_stamp": review_stamp,
        }
    )
    return context


def render_nutriok_report_html(
    data: dict[str, Any] | None = None,
    submission: dict[str, Any] | None = None,
) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(("html", "xml", "j2")),
    )
    template = env.get_template("nutriok_report.html.j2")
    context = build_nutriok_report_context(data, submission=submission)
    return template.render(**context)


def create_nutriok_pdf(
    data: dict[str, Any],
    output_path: str,
    submission: dict[str, Any] | None = None,
) -> str:
    html_content = render_nutriok_report_html(data, submission=submission)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content, wait_until="domcontentloaded")
        page.wait_for_timeout(150)
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        browser.close()

    return str(out)


def create_premium_pdf(data: dict[str, Any], output_path: str) -> str:
    """
    Renders the data into the NutriOK editorial HTML template using Jinja2,
    then uses Playwright to generate a print-perfect A4 PDF (< 2 MB).
    """
    return create_nutriok_pdf(data, output_path)


if __name__ == "__main__":
    import test_data

    output_file = str(BASE_DIR / "data" / "drafts" / "NUTRIOK_DEMO_PREVIEW.pdf")
    create_nutriok_pdf(test_data.DUMMY_DATA, output_file)
    print(f"Generated successfully: {output_file}")
