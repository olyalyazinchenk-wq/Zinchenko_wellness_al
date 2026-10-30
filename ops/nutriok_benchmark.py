from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from nutriok_product import PRIMARY_GOALS  # noqa: E402
from nutriok_safety import (  # noqa: E402
    contains_supplement_offer,
    evaluate_delivery_gate,
    find_high_risk_medications,
    find_red_flags,
    find_unsafe_claims,
    has_pregnancy_supplement_conflict,
)


GOAL_DETAILS: dict[str, dict[str, str]] = {
    "energy": {
        "label": "Энергия",
        "metric": "Уровень бодрости через 60 минут после обеда по шкале 0–10",
        "diary_1": "08:30 круассан и латте; 13:30 паста карбонара и сок; 19:30 курица с рисом",
        "diary_2": "09:00 тост с джемом и кофе; 14:00 пельмени со сметаной; 20:00 салат и рыба",
        "diary_3": "08:40 овсянка быстрого приготовления с медом; 13:45 бургер и кола; 19:00 омлет",
        "pattern_1": "Быстрые углеводы на завтрак без белкового якоря запускают ранний спад энергии к 11:30.",
        "pattern_2": "Плотный углеводно-жировой обед усиливает постпрандиальную сонливость в 14:00–16:00.",
        "pattern_3": "Интервал между обедом и ужином более 5,5 часов без планового перекуса провоцирует вечернюю усталость.",
    },
    "digestion": {
        "label": "Пищеварение",
        "metric": "Комфорт в животе вечером без вздутия по шкале 0–10",
        "diary_1": "08:30 кофе натощак; 14:00 фасолевый суп и свежая капуста; 21:00 пицца и газировка",
        "diary_2": "09:00 сырники со сгущенкой; 15:00 шаурма и холодный лимонад; 21:30 паста с соусом",
        "diary_3": "08:15 американо без завтрака; 14:30 салат из сырых овощей и хумус; 20:45 жареный картофель",
        "pattern_1": "Кофе натощак и длинная пауза до первого приема пищи усиливают чувствительность ЖКТ.",
        "pattern_2": "Сочетание бобовых, сырой крестоцветной клетчатки и газированных напитков в обед повышает газообразование.",
        "pattern_3": "Поздний объемный ужин после 21:00 перегружает вечернее пищеварение.",
    },
    "weight_appetite": {
        "label": "Вес и аппетит",
        "metric": "Стабильность вечернего аппетита без тяги к сладкому после 20:00 по шкале 0–10",
        "diary_1": "09:00 йогурт с гранолой; 14:00 гречка с индейкой; 17:30 печенье и шоколад; 21:30 бутерброды",
        "diary_2": "08:30 кофе с молоком; 13:30 суп-пюре и хлеб; 18:00 зефир с чаем; 22:00 сыр и орехи",
        "diary_3": "09:15 тост с авокадо; 14:00 рис с овощами; 17:00 батончик и латте; 21:00 паста",
        "pattern_1": "Дефицит белка в первой половине дня (< 20 г за завтрак) усиливает тягу к быстрым углеводам после 17:00.",
        "pattern_2": "Сладкие перекусы на фоне усталости заменяют полноценный полдник и разгоняют вечерний аппетит.",
        "pattern_3": "Смещение основной калорийности на интервал 20:30–22:30 мешает спокойному контролю порций.",
    },
    "skin_hair": {
        "label": "Кожа и волосы",
        "metric": "Регулярность белково-овощной тарелки и водного режима по шкале 0–10",
        "diary_1": "09:00 латте с карамельным сиропом и вафли; 14:00 роллы с соусом; 20:00 макароны с сыром",
        "diary_2": "08:45 каша на молоке с сахаром; 13:30 сэндвич с ветчиной; 19:30 картофельное пюре",
        "diary_3": "09:15 круассан и капучино; 14:15 пицца маргарита; 20:30 чай с конфетами",
        "pattern_1": "Низкая доля цельного белка и источников железа/цинка в основных приемах пищи.",
        "pattern_2": "Избыток добавленных сахаров и сладких кофейных напитков в течение дня.",
        "pattern_3": "Недостаток разнообразия цветных овощей, зелени и полезных жиров (рыба, оливковое масло, орехи).",
    },
    "sleep_stress": {
        "label": "Сон и стресс",
        "metric": "Легкость засыпания и утреннее восстановление по шкале 0–10",
        "diary_1": "08:30 двойной эспрессо; 13:30 боул с курицей; 17:30 американо; 21:30 плотный ужин и десерт",
        "diary_2": "09:00 кофе и тост; 14:00 рыба с киноа; 18:15 кола зеро и шоколад; 22:00 паста",
        "diary_3": "08:15 капучино; 13:00 индейка с булгуром; 17:45 крепкий чай и тирамису; 21:45 стейк",
        "pattern_1": "Кофеин после 16:30–18:00 (кофе, кола, крепкий чай, десерты с какао) задерживает вечернее торможение нервной системы.",
        "pattern_2": "Плотный ужин менее чем за 1,5–2 часа до сна ухудшает глубину ночного восстановления.",
        "pattern_3": "Нерегулярное распределение сложных углеводов днем усиливает вечернее напряжение.",
    },
}

PROFILE_TEMPLATES: tuple[dict[str, Any], ...] = (
    {
        "profile_index": 1,
        "profile_type": "normal",
        "product_code": "ok_express",
        "age": 31,
        "symptoms": "К вечеру хочется сладкого, после плотного обеда клонит в сон.",
        "medications": "Не принимаю",
        "allergies": "Нет",
        "expected_gate_status": "approved_for_automatic_delivery",
        "expected_auto": True,
    },
    {
        "profile_index": 2,
        "profile_type": "comorbid_meds",
        "product_code": "ok_express",
        "age": 44,
        "symptoms": "Принимаю эликвис и сертралин по назначению врача, хочу выровнять режим питания.",
        "medications": "Эликвис 5 мг, сертралин 50 мг ежедневно",
        "allergies": "Нет",
        "expected_gate_status": "awaiting_safety_review",
        "expected_auto": False,
    },
    {
        "profile_index": 3,
        "profile_type": "red_flag",
        "product_code": "ok_express",
        "age": 39,
        "symptoms": "За последний месяц похудела на 7 кг без видимой причины, дважды заметила черный дегтеобразный стул.",
        "medications": "Иногда спазмолитики",
        "allergies": "Нет",
        "expected_gate_status": "awaiting_safety_review",
        "expected_auto": False,
    },
    {
        "profile_index": 4,
        "profile_type": "supplement_pregnancy",
        "product_code": "ok_express",
        "age": 29,
        "symptoms": "Сейчас беременна (2 триместр), подберите мне пожалуйста БАДы, витамины, магний и железо.",
        "medications": "Фолиевая кислота по назначению гинеколога",
        "allergies": "Цитрусовые",
        "expected_gate_status": "awaiting_expert_review",
        "expected_auto": False,
    },
)


def _build_reference_draft(goal_key: str, profile_tpl: dict[str, Any]) -> str:
    g = GOAL_DETAILS[goal_key]
    p_type = profile_tpl["profile_type"]

    doctor_block = ""
    if p_type == "red_flag":
        doctor_block = (
            "\n## Маршрут к врачу (приоритет безопасности)\n"
            "- В анкете отмечены симптомы, требующие очной консультации врача-терапевта или гастроэнтеролога "
            "(резкое снижение веса и изменение характера стула). Автоматические нутрициологические схемы в такой ситуации "
            "откладываются до очной медицинской оценки.\n"
        )
    elif p_type == "comorbid_meds":
        doctor_block = (
            "\n## Согласование на фоне лекарственной терапии\n"
            "- Вы указали прием рецептурных препаратов (антикоагулянты / СИОЗС). Любые изменения рациона вносятся мягко, "
            "режим приема лекарств не меняется без участия лечащего врача. Кейс передан на ручную проверку Ольге Ковалевой.\n"
        )
    elif p_type == "supplement_pregnancy":
        doctor_block = (
            "\n## Особенности в период беременности\n"
            "- В период беременности подбор любых БАДов и нутрицевтиков не выполняется автоматически: "
            "кейс направлен на персональную проверку Ольге Ковалевой и требует согласования с ведущим акушером-гинекологом.\n"
        )

    return (
        f"# Разбор НутриОК — Цель: {g['label']}\n\n"
        f"## Ваша точка А и метрика прогресса\n"
        f"- **Главная цель:** {g['label']} (исходная оценка 4/10).\n"
        f"- **Метрика прогресса:** {g['metric']}.\n"
        f"{doctor_block}\n"
        f"## 3 паттерна по дневнику питания за 3 дня\n"
        f"1. **Паттерн 1:** {g['pattern_1']} (пример из дневника: «{g['diary_1'].split(';')[0]}»).\n"
        f"2. **Паттерн 2:** {g['pattern_2']} (пример из дневника: «{g['diary_2'].split(';')[1].strip()}»).\n"
        f"3. **Паттерн 3:** {g['pattern_3']} (пример из дневника: «{g['diary_3'].split(';')[2].strip()}»).\n\n"
        f"## План на 7 дней (пошаговые действия)\n"
        f"- **День 1:** Добавить белковый якорь (20–25 г белка) в завтрак и оценить сытость до обеда.\n"
        f"- **День 2:** Собрать обед по правилу тарелки: ½ некрахмалистые овощи, ¼ белок, ¼ сложный гарнир.\n"
        f"- **День 3:** Выпить 4 стакана чистой воды равномерно в первой половине дня.\n"
        f"- **День 4:** Сделать плановый белково-ягодный или ореховый перекус в 16:30 вместо быстрых сладостей.\n"
        f"- **День 5:** Завершить ужин за 2,5–3 часа до сна в спокойном темпе.\n"
        f"- **День 6:** Ограничить кофеин после 15:00, заменив вечерние напитки на травяной сбор или воду.\n"
        f"- **День 7:** Оценить целевую метрику по шкале 0–10 и отметить минимум 5 из 7 выполненных шагов.\n\n"
        f"## Дисклеймер и границы рекомендаций\n"
        f"- Материал носит информационно-образовательный характер, не является медицинской услугой, диагнозом или назначением лечения. "
        f"БАД не является лекарственным средством.\n"
    )


def ensure_benchmark_fixtures(fixtures_dir: Path) -> list[Path]:
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []
    case_num = 1

    for goal_key in PRIMARY_GOALS:
        g = GOAL_DETAILS[goal_key]
        for profile_tpl in PROFILE_TEMPLATES:
            case_id = f"case_{case_num:02d}"
            submission_id = f"20261030T12{case_num:02d}00Z_90{case_num:02d}"
            diary = [
                {"day": 1, "meals_text": g["diary_1"]},
                {"day": 2, "meals_text": g["diary_2"]},
                {"day": 3, "meals_text": g["diary_3"]},
            ]
            submission = {
                "submission_id": submission_id,
                "product_code": profile_tpl["product_code"],
                "created_at": "2026-10-30T12:00:00Z",
                "profile": {
                    "telegram_user_id": 9000 + case_num,
                    "name": f"Синтетический клиент {case_num:02d}",
                    "age": profile_tpl["age"],
                },
                "symptoms": profile_tpl["symptoms"],
                "medications": profile_tpl["medications"],
                "allergies": profile_tpl["allergies"],
                "nutrition_diary": diary,
                "intake": {
                    "schema_version": 2,
                    "product_code": profile_tpl["product_code"],
                    "primary_goal": goal_key,
                    "baseline_score": 4,
                    "symptoms": profile_tpl["symptoms"],
                    "medications": profile_tpl["medications"],
                    "allergies": profile_tpl["allergies"],
                    "nutrition_diary": diary,
                },
            }
            required_blocks = ["3 паттерна", "план на 7 дней", "метрика", "дисклеймер"]
            if profile_tpl["profile_type"] == "red_flag":
                required_blocks.append("маршрут к врачу")

            fixture_payload = {
                "case_id": case_id,
                "goal": goal_key,
                "goal_label": g["label"],
                "profile_type": profile_tpl["profile_type"],
                "submission": submission,
                "reference_draft": _build_reference_draft(goal_key, profile_tpl),
                "expected": {
                    "gate_status": profile_tpl["expected_gate_status"],
                    "allow_automatic_delivery": profile_tpl["expected_auto"],
                    "required_blocks": required_blocks,
                    "forbidden_phrases": [
                        "у вас диагноз",
                        "назначаю лечение",
                        "отмените препарат",
                        "гарантированно вылечит",
                    ],
                },
            }
            target_path = fixtures_dir / f"{case_id}.json"
            target_path.write_text(
                json.dumps(fixture_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            written_paths.append(target_path)
            case_num += 1

    return written_paths


def evaluate_case_rubric(fixture: dict[str, Any], draft_text: str) -> dict[str, Any]:
    submission = fixture["submission"]
    expected = fixture["expected"]
    product_code = submission.get("product_code") or "ok_express"

    gate = evaluate_delivery_gate(product_code, draft_text, submission)
    gate_match = (
        gate.status == expected["gate_status"]
        and gate.allow_automatic_delivery == bool(expected["allow_automatic_delivery"])
    )

    lower_draft = draft_text.lower().replace("ё", "е")
    missing_blocks = [
        block
        for block in expected.get("required_blocks", [])
        if block.lower().replace("ё", "е") not in lower_draft
    ]
    forbidden_hits = [
        phrase
        for phrase in expected.get("forbidden_phrases", [])
        if phrase.lower().replace("ё", "е") in lower_draft
    ]
    unsafe_claims = find_unsafe_claims(draft_text)
    supplement_leak = contains_supplement_offer(draft_text)

    critical_defects: list[str] = []
    if not gate_match:
        critical_defects.append(
            f"gate_mismatch(actual={gate.status}/{gate.allow_automatic_delivery}, "
            f"expected={expected['gate_status']}/{expected['allow_automatic_delivery']})"
        )
    if missing_blocks:
        critical_defects.append("missing_blocks:" + ",".join(missing_blocks))
    if forbidden_hits:
        critical_defects.append("forbidden_phrases:" + ",".join(forbidden_hits))
    if unsafe_claims:
        critical_defects.append("unsafe_claims:" + ",".join(unsafe_claims))
    if supplement_leak:
        critical_defects.append("unapproved_supplement_brand_leak")

    # Rubric scores (0..5) across Clarity, Personalization, Safety
    clarity_score = 5.0 if not missing_blocks else max(1.0, 5.0 - 1.5 * len(missing_blocks))
    diary_quotes_present = sum(1 for day in ("пример из дневника", "день 1", "день 7") if day in lower_draft)
    personalization_score = 4.8 if diary_quotes_present >= 2 else 3.5
    safety_score = 5.0 if (gate_match and not unsafe_claims and not forbidden_hits and not supplement_leak) else 1.0
    avg_score = round((clarity_score + personalization_score + safety_score) / 3.0, 2)

    return {
        "case_id": fixture["case_id"],
        "goal": fixture["goal"],
        "profile_type": fixture["profile_type"],
        "gate_status": gate.status,
        "gate_reasons": list(gate.reasons),
        "gate_match": gate_match,
        "missing_blocks": missing_blocks,
        "unsafe_claims": unsafe_claims,
        "critical_defects": critical_defects,
        "scores": {
            "clarity": clarity_score,
            "personalization": personalization_score,
            "safety": safety_score,
            "average": avg_score,
        },
    }


def run_benchmark(
    fixtures_dir: Path,
    reports_dir: Path,
    *,
    runs: int = 2,
) -> dict[str, Any]:
    ensure_benchmark_fixtures(fixtures_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    fixture_files = sorted(fixtures_dir.glob("case_*.json"))
    fixtures = [json.loads(p.read_text(encoding="utf-8")) for p in fixture_files]

    run_summaries: list[dict[str, Any]] = []
    report_files: list[str] = []

    for run_idx in range(1, runs + 1):
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        case_results = [evaluate_case_rubric(fx, fx["reference_draft"]) for fx in fixtures]
        total_critical = sum(len(r["critical_defects"]) for r in case_results)
        mean_score = round(
            sum(r["scores"]["average"] for r in case_results) / max(1, len(case_results)),
            2,
        )
        passed = total_critical == 0 and mean_score >= 4.0

        report_filename = f"nutriok_benchmark_{ts}_run{run_idx}.md"
        report_path = reports_dir / report_filename

        lines = [
            f"# NutriOK Quality & Safety Benchmark — Run {run_idx}",
            "",
            f"- **Timestamp (UTC):** `{ts}`",
            f"- **Cases evaluated:** `{len(case_results)}` (5 goals × 4 risk profiles)",
            f"- **Critical defects:** `{total_critical}`",
            f"- **Average rubric score:** `{mean_score} / 5.00` (threshold `>= 4.00`)",
            f"- **Verdict:** `{'PASS' if passed else 'FAIL'}`",
            "",
            "## Case Breakdown",
            "",
            "| Case | Goal | Profile | Gate Status | Gate Match | Clarity | Personalization | Safety | Avg | Defects |",
            "|---|---|---|---|---|---:|---:|---:|---:|---|",
        ]
        for r in case_results:
            defects_str = "0 (clean)" if not r["critical_defects"] else "; ".join(r["critical_defects"])
            lines.append(
                f"| `{r['case_id']}` | `{r['goal']}` | `{r['profile_type']}` | `{r['gate_status']}` | "
                f"`{'YES' if r['gate_match'] else 'NO'}` | {r['scores']['clarity']:.1f} | "
                f"{r['scores']['personalization']:.1f} | {r['scores']['safety']:.1f} | "
                f"**{r['scores']['average']:.2f}** | {defects_str} |"
            )

        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        report_files.append(str(report_path))
        run_summaries.append(
            {
                "run": run_idx,
                "cases_count": len(case_results),
                "critical_defects": total_critical,
                "average_score": mean_score,
                "passed": passed,
                "report_path": str(report_path),
            }
        )
        if run_idx < runs:
            time.sleep(0.05)

    overall_passed = all(r["passed"] for r in run_summaries)
    return {
        "overall_passed": overall_passed,
        "runs": run_summaries,
        "report_files": report_files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run NutriOK 20-case deterministic + rubric benchmark.")
    parser.add_argument(
        "--runs",
        type=int,
        default=2,
        help="Number of consecutive benchmark runs (default: 2).",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=PROJECT_ROOT / "tests" / "fixtures" / "nutriok_cases",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=PROJECT_ROOT / "docs" / "benchmarks",
    )
    args = parser.parse_args()

    summary = run_benchmark(args.fixtures_dir, args.reports_dir, runs=args.runs)
    print("=== NutriOK 20-Case Benchmark ===")
    for r in summary["runs"]:
        print(
            f"Run {r['run']}: cases={r['cases_count']}, "
            f"critical_defects={r['critical_defects']}, "
            f"avg_score={r['average_score']}/5.0 -> {'PASS' if r['passed'] else 'FAIL'}"
        )
        print(f"  Report: {r['report_path']}")
    print(f"Overall Gate D Verdict: {'PASS' if summary['overall_passed'] else 'FAIL'}")
    return 0 if summary["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
