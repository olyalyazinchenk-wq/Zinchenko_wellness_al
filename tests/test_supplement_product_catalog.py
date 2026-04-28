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
        self.assertTrue(context["supplement_context"]["recommendable_candidates"])


if __name__ == "__main__":
    unittest.main()
