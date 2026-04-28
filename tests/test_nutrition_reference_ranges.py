from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from nutrition_reference_ranges import (  # noqa: E402
    enrich_biomarkers_with_nutrition_ranges,
    match_nutrition_reference_entry,
)


class NutritionReferenceRangeTests(unittest.TestCase):
    def test_match_ferritin_range(self) -> None:
        marker_key, entry = match_nutrition_reference_entry("Ферритин", "нг/мл")
        self.assertEqual(marker_key, "ferritin")
        self.assertIsNotNone(entry)

    def test_enrich_biomarker_with_nutrition_range_status(self) -> None:
        biomarkers = enrich_biomarkers_with_nutrition_ranges(
            [
                {
                    "name": "Ферритин",
                    "value": "22",
                    "unit": "нг/мл",
                    "reference_range": "15-150",
                }
            ]
        )
        self.assertEqual(biomarkers[0]["nutrition_marker_key"], "ferritin")
        self.assertEqual(biomarkers[0]["nutrition_optimal_range"], "40-90 нг/мл")
        self.assertEqual(biomarkers[0]["nutrition_status"], "below_nutrition_range")

    def test_glucose_without_unit_is_not_force_matched(self) -> None:
        biomarkers = enrich_biomarkers_with_nutrition_ranges(
            [
                {
                    "name": "Глюкоза",
                    "value": "4.9",
                    "unit": None,
                }
            ]
        )
        self.assertNotIn("nutrition_marker_key", biomarkers[0])


if __name__ == "__main__":
    unittest.main()
