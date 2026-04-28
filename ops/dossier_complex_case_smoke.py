from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from ai_drafting import generate_case_draft, generate_case_judge_report  # noqa: E402
from config import load_settings  # noqa: E402
from html_pdf_engine import create_premium_pdf  # noqa: E402
from main import apply_safe_action_floor, normalize_dossier_pdf_data, strip_json_code_fences  # noqa: E402


def build_complex_submission() -> dict:
    return {
        "submission_id": "smoke_complex_deepseek_001",
        "offer": "premium",
        "profile": {
            "full_name": "Тестовый сложный кейс",
            "age": "38",
            "city": "Москва",
            "telegram_user_id": 1084557944,
        },
        "medical_context": {
            "symptoms": (
                "усталость, выпадение волос, зябкость, вздутие, нестабильный стул, "
                "сердцебиение при нагрузке, болезненные обильные менструации"
            ),
            "complaint_pattern": "жалобы усиливаются последние 4 месяца, сон поверхностный, кофе натощак",
            "goal": "понять возможные дефицитные риски и безопасный следующий шаг",
            "background": "эндометриоз в анамнезе, узлы щитовидной железы под наблюдением, принимает L-тироксин",
            "red_flags": "нет острой боли и обмороков, но есть обильные кровотечения и сердцебиение",
            "nutrition": "завтрак часто кофе и сладкое, белка мало, ужин поздний",
            "digestion": "вздутие после молочных продуктов и выпечки, стул нерегулярный",
            "sleep_stress": "сон 5-6 часов, высокий стресс, поздний экран",
            "activity": "сидячая работа, тренировки нерегулярно, после интенсивной нагрузки сильная усталость",
            "medications": "L-тироксин, иногда обезболивающие в первые дни цикла",
            "supplements": "магний иногда, омега-3 нерегулярно",
            "lab_notes": "часть фото анализов была нечеткой; значения нужно подтверждать по PDF",
        },
        "parsed_biomarkers": [
            {
                "name": "Ферритин",
                "value": "18",
                "unit": "нг/мл",
                "reference_range": "15-150",
                "nutrition_marker_key": "ferritin",
                "nutrition_optimal_range": "40-90 нг/мл",
                "nutrition_status": "below_nutrition_range",
                "nutrition_range_basis": "нутрициологический ориентир",
                "source_line": "Ферритин 18 нг/мл 15-150",
            },
            {
                "name": "Витамин D",
                "value": "24",
                "unit": "нг/мл",
                "reference_range": "30-100",
                "nutrition_marker_key": "vitamin_d",
                "nutrition_optimal_range": "40-60 нг/мл",
                "nutrition_status": "below_nutrition_range",
                "nutrition_range_basis": "нутрициологический ориентир",
                "source_line": "Витамин D 24 нг/мл 30-100",
            },
            {
                "name": "ТТГ",
                "value": "3.8",
                "unit": "мЕд/л",
                "reference_range": "0.4-4.0",
                "source_line": "ТТГ 3.8 мЕд/л 0.4-4.0",
            },
        ],
        "lab_quality_check": {"status": "ok", "requires_resubmission": False, "issues": []},
        "requires_lab_resubmission": False,
        "consent_given": True,
    }


def main() -> None:
    settings = load_settings()
    reports_dir = PROJECT_ROOT / "ops" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    submission = build_complex_submission()
    draft_text = generate_case_draft(settings, submission, tier="premium")
    if not draft_text:
        raise RuntimeError("DeepSeek returned empty draft")

    raw_json = json.loads(strip_json_code_fences(draft_text))
    pdf_data = apply_safe_action_floor(normalize_dossier_pdf_data(raw_json), submission)
    final_json_path = reports_dir / "complex_case_dossier_payload.json"
    final_json_path.write_text(json.dumps(pdf_data, ensure_ascii=False, indent=2), encoding="utf-8")

    judge_text = generate_case_judge_report(settings, submission, json.dumps(pdf_data, ensure_ascii=False, indent=2))
    judge_path = reports_dir / "complex_case_judge_report.json"
    judge_path.write_text(judge_text or "{}", encoding="utf-8")

    pdf_path = reports_dir / "complex_case_dossier.pdf"
    create_premium_pdf(pdf_data, str(pdf_path))

    checks = {
        "provider": settings.llm_provider,
        "model": settings.llm_model,
        "json_path": str(final_json_path),
        "judge_path": str(judge_path),
        "pdf_path": str(pdf_path),
        "has_phased_plan": all(
            any(item.get("time") == phase for item in pdf_data.get("schemes", []))
            for phase in ["Сейчас / 24-72 часа", "7 дней", "2-4 недели"]
        ),
        "has_accuracy_protocol": any("Протокол точности" in item for item in pdf_data.get("additional_control", [])),
        "has_doctor_route": any(
            any(word in item for word in ["Эндокринолог", "Гинеколог", "Терапевт", "Гематолог"])
            for item in pdf_data.get("additional_control", [])
        ),
        "iron_not_recommended_as_supplement": not any(
            "желез" in str(item).lower() and "самостоятель" not in str(item).lower()
            for item in pdf_data.get("schemes", [])
        ),
    }
    print(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()