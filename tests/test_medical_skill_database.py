from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from medical_skill_database import (  # noqa: E402
    analyze_biomarker_with_skill,
    build_medical_skill_context,
    export_medical_skill_database,
)


class MedicalSkillDatabaseTests(unittest.TestCase):
    def test_ferritin_analysis_has_route_and_boundary(self) -> None:
        result = analyze_biomarker_with_skill(
            {
                "name": "Ферритин",
                "value": "18",
                "unit": "нг/мл",
                "nutrition_status": "below_nutrition_range",
                "nutrition_optimal_range": "40-90 нг/мл",
            }
        )
        self.assertTrue(result["matched"])
        self.assertEqual(result["marker_key"], "ferritin")
        self.assertIn("гинеколог при обильном цикле", result["doctor_route"])
        self.assertIn("Не начинать железо", result["self_action_boundary"])

    def test_context_detects_symptom_routes_and_confirmation_status(self) -> None:
        submission = {
            "medical_context": {
                "symptoms": "усталость, сердцебиение",
                "red_flags": "обильные менструации",
                "background": "эндометриоз",
            },
            "parsed_biomarkers": [
                {
                    "name": "ТТГ",
                    "value": "3.8",
                    "unit": "мЕд/л",
                    "nutrition_status": "above_nutrition_range",
                }
            ],
            "lab_confirmation_status": "client_confirmed",
        }
        context = build_medical_skill_context(submission)
        self.assertTrue(context["lab_values_confirmed"])
        route_keys = {item["key"] for item in context["symptom_routes"]}
        self.assertIn("heavy_bleeding", route_keys)
        self.assertIn("tachycardia", route_keys)
        self.assertTrue(context["priority_actions"])

    def test_export_database_has_core_sections(self) -> None:
        payload = export_medical_skill_database()
        self.assertIn("markers", payload)
        self.assertIn("ferritin", payload["markers"])
        self.assertIn("symptom_routes", payload)
        self.assertGreaterEqual(len(payload["symptom_routes"]), 3)


if __name__ == "__main__":
    unittest.main()
