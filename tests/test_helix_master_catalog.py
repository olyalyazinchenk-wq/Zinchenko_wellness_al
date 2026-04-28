from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from helix_master_catalog import (  # noqa: E402
    HELIX_OFFICIAL_CATEGORIES,
    apply_nutrition_overlay_to_catalog_entries,
    build_helix_catalog_entry,
    helix_catalog_metadata,
)


class HelixMasterCatalogTests(unittest.TestCase):
    def test_metadata_contains_official_category_structure(self) -> None:
        metadata = helix_catalog_metadata()
        categories = metadata["source"]["official_categories"]

        self.assertGreaterEqual(len(categories), 20)
        self.assertIn("Все анализы", categories)
        self.assertIn("Превентивная медицина и нутрициология", categories)
        self.assertEqual(categories, list(HELIX_OFFICIAL_CATEGORIES))

    def test_build_entry_preserves_helix_identity_fields(self) -> None:
        entry = build_helix_catalog_entry(
            "06-012",
            "Витамин B12 (цианокобаламин)",
            "Анализы на витамины",
            sample_type="кровь",
            turnaround="До 2 суток",
        )
        self.assertEqual(entry["helix_code"], "06-012")
        self.assertEqual(entry["helix_name"], "Витамин B12 (цианокобаламин)")
        self.assertEqual(entry["category"], "Анализы на витамины")

    def test_overlay_can_attach_nutrition_ranges_to_catalog_entries(self) -> None:
        entries = [
            {
                "helix_code": "06-012",
                "helix_name": "Витамин B12 (цианокобаламин)",
                "category": "Анализы на витамины",
                "value": "320",
                "unit": "пг/мл",
                "reference_range": "191-663",
            }
        ]
        enriched = apply_nutrition_overlay_to_catalog_entries(entries)
        self.assertTrue(enriched[0]["nutrition_overlay_enabled"])
        self.assertEqual(enriched[0]["nutrition_marker_key"], "b12")
        self.assertEqual(enriched[0]["nutrition_status"], "below_nutrition_range")


if __name__ == "__main__":
    unittest.main()
