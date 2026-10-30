from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from medical_skill_database import build_medical_skill_context  # noqa: E402
from supplement_product_catalog import (  # noqa: E402
    build_supplement_context,
    export_supplement_catalog,
    get_candidate_products_for_goals,
)
from supplement_protocols import (  # noqa: E402
    assess_supplement_safety,
    build_supplement_scheme_entries,
)


class SupplementProductCatalogTests(unittest.TestCase):
    def test_export_contains_primary_and_alternative_brands(self) -> None:
        payload = export_supplement_catalog()
        products = payload["products"].values()
        brands = {item["brand"] for item in products}
        self.assertIn("Siberian Wellness", brands)
        self.assertIn("Vitamax", brands)

    def test_vitamin_d_candidates_prioritize_siberian_wellness(self) -> None:
        candidates = get_candidate_products_for_goals(["vitamin_d_support"])
        self.assertGreaterEqual(len(candidates), 2)
        self.assertEqual(candidates[0]["brand"], "Siberian Wellness")
        self.assertEqual(candidates[0]["recommendation_role"], "primary_siberian_wellness")

    def test_discontinued_iron_is_not_recommendable(self) -> None:
        candidates = get_candidate_products_for_goals(["iron_support"])
        self.assertEqual(candidates[0]["availability_status"], "discontinued_official_page")
        context = build_supplement_context(
            {
                "biomarker_analysis": [
                    {
                        "marker_key": "ferritin",
                        "nutrition_status": "below_nutrition_range",
                    }
                ]
            },
            {},
        )
        self.assertEqual(context["recommendable_candidates"], [])
        self.assertTrue(context["unavailable_or_reference_only"])

    def test_medical_skill_context_includes_supplement_context(self) -> None:
        context = build_medical_skill_context(
            {
                "medical_context": {"symptoms": "усталость"},
                "parsed_biomarkers": [
                    {
                        "name": "Витамин D",
                        "value": "24",
                        "unit": "нг/мл",
                        "nutrition_status": "below_nutrition_range",
                    }
                ],
                "lab_confirmation_status": "client_confirmed",
            }
        )
        self.assertIn("supplement_context", context)
        self.assertEqual(
            context["supplement_context"]["recommendation_status"],
            "blocked_safety_context",
        )

    def test_gut_support_uses_verified_spz03_products_and_excludes_enzymes_for_heartburn(self) -> None:
        context = build_medical_skill_context(
            {
                "offer": "gut_support_18",
                "profile": {"age": 40},
                "adult_confirmed": True,
                "medical_context": {
                    "symptoms": "изжога и нестабильный стул",
                    "background": "Хронических заболеваний нет. Лекарства и БАДы не принимаю.",
                    "risk_details": "Аллергий нет, беременности и ГВ нет.",
                },
            }
        )
        products = context["supplement_context"]["recommendable_candidates"]
        names = {item["name"] for item in products}
        self.assertIn("ЭндоФлора, 60 капсул", names)
        self.assertNotIn("Комплекс сильных ферментов Про, 60 таблеток", names)
        endoflora = next(item for item in products if item["name"] == "ЭндоФлора, 60 капсул")
        self.assertEqual(
            endoflora["source_url"],
            "https://spz03.ru/catalog/detail/endoflora-banka-60-kaps-8251/",
        )

    def test_safe_adult_osipov_context_builds_deterministic_protocol(self) -> None:
        context = build_medical_skill_context(
            {
                "offer": "osipov",
                "profile": {"age": 40},
                "adult_confirmed": True,
                "medical_context": {
                    "symptoms": "вздутие и нестабильный стул",
                    "background": "Хронических заболеваний нет. Лекарства и БАДы не принимаю.",
                    "risk_details": "Аллергий нет, беременности и ГВ нет.",
                    "osipov_context": "Жалобы ЖКТ, хронических заболеваний нет.",
                    "osipov_ocr_text": "Bifidobacterium spp. ниже референса",
                },
            }
        )["supplement_context"]

        self.assertEqual(context["recommendation_status"], "eligible_for_human_review")
        self.assertFalse(context["client_delivery_allowed"])
        self.assertEqual(len(context["protocol_recommendations"]), 1)
        self.assertEqual(
            context["protocol_recommendations"][0]["product_key"],
            "vitamax_endoflora_8251",
        )
        schemes = build_supplement_scheme_entries(context)
        self.assertIn("1-2 капсулы", schemes[0]["comment"])
        self.assertIn("844131", schemes[0]["comment"])

    def test_missing_medications_or_allergies_blocks_protocol(self) -> None:
        context = build_medical_skill_context(
            {
                "offer": "osipov",
                "profile": {"age": 40},
                "adult_confirmed": True,
                "medical_context": {
                    "symptoms": "вздутие",
                    "background": "Диагнозов нет",
                },
            }
        )["supplement_context"]

        self.assertEqual(context["recommendation_status"], "blocked_safety_context")
        self.assertFalse(context["protocol_recommendations"])
        self.assertIn(
            "полный список лекарств и уже принимаемых БАДов",
            context["safety_assessment"]["missing_safety_context"],
        )

    def test_current_medication_blocks_automatic_protocol(self) -> None:
        context = build_medical_skill_context(
            {
                "offer": "osipov",
                "profile": {"age": 40},
                "adult_confirmed": True,
                "medical_context": {
                    "symptoms": "вздутие и нестабильный стул",
                    "background": "Гипотиреоз, принимаю L-тироксин 50 мкг.",
                    "risk_details": "Аллергий нет.",
                },
            }
        )["supplement_context"]

        self.assertEqual(context["recommendation_status"], "blocked_safety_context")
        self.assertIn(
            "current_medications_or_supplements",
            context["safety_assessment"]["risk_flags"],
        )
        self.assertFalse(context["recommendable_candidates"])

    def test_pregnancy_blocks_automatic_protocol(self) -> None:
        safety = assess_supplement_safety(
            {
                "profile": {"age": 30},
                "adult_confirmed": True,
                "medical_context": {
                    "background": "Хронических заболеваний нет, лекарства и БАДы не принимаю.",
                    "risk_details": "Аллергий нет, беременность 12 недель.",
                },
            }
        )
        self.assertIn("pregnancy", safety["risk_flags"])


if __name__ == "__main__":
    unittest.main()
