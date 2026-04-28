from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from nutrition_reference_ranges import (
    NUTRITION_REFERENCE_CATALOG,
    enrich_biomarkers_with_nutrition_ranges,
)


HELIX_SOURCE_CAPTURED_AT = "2026-04-21"
HELIX_SOURCE_URL = "https://helix.ru/"
HELIX_ESTIMATED_TOTAL_TESTS = 3600

# Top-level catalog categories mirrored from the official Helix navigation as captured on 2026-04-21.
HELIX_OFFICIAL_CATEGORIES = (
    "Популярные анализы",
    "Все анализы",
    "Комплексы анализов",
    "Анализы на аллергию",
    "Анализы на витамины",
    "Анализы на гормоны",
    "Анализы на ЗППП (заболевания, передающиеся половым путем)",
    "Анализы на инфекции",
    "Анализы на аутоиммунные заболевания",
    "Анализы для беременных",
    "Иммунограммы, анализы на маркеры иммунитета",
    "ЭКГ (электрокардиограмма)",
    "Анализы на генетику",
    "Анализы для онкодиагностики",
    "Анализы на цитологию и гистологию",
    "Бактериологические исследования и посевы",
    "Лекарственный мониторинг",
    "Общий анализ крови",
    "Биохимические анализы",
    "Анализы кала",
    "Анализы мочи",
    "Анализы спермы",
    "Анализы на свертываемость крови",
    "Анализы на группу крови и резус-фактор",
    "Анализы на тяжелые металлы и микроэлементы",
    "Анализы на COVID-19",
    "Превентивная медицина и нутрициология",
)


@dataclass(slots=True)
class HelixCatalogEntry:
    helix_code: str
    helix_name: str
    category: str
    sample_type: str | None = None
    turnaround: str | None = None
    nutrition_marker_key: str | None = None
    nutrition_optimal_range: str | None = None
    nutrition_status: str | None = None
    nutrition_range_basis: str | None = None
    nutrition_overlay_enabled: bool = False


def helix_catalog_metadata() -> dict[str, Any]:
    return {
        "source": {
            "provider": "Helix",
            "captured_at": HELIX_SOURCE_CAPTURED_AT,
            "source_url": HELIX_SOURCE_URL,
            "estimated_total_tests": HELIX_ESTIMATED_TOTAL_TESTS,
            "official_categories": list(HELIX_OFFICIAL_CATEGORIES),
        },
        "nutrition_overlay": {
            "catalog_version": "v1",
            "covered_marker_keys": sorted(NUTRITION_REFERENCE_CATALOG.keys()),
        },
    }


def build_helix_catalog_entry(
    helix_code: str,
    helix_name: str,
    category: str,
    *,
    sample_type: str | None = None,
    turnaround: str | None = None,
) -> dict[str, Any]:
    entry = HelixCatalogEntry(
        helix_code=helix_code,
        helix_name=helix_name,
        category=category,
        sample_type=sample_type,
        turnaround=turnaround,
    )
    return asdict(entry)


def apply_nutrition_overlay_to_catalog_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    biomarker_like_entries = [
        {
            "name": item.get("helix_name"),
            "value": item.get("value"),
            "unit": item.get("unit"),
            "reference_range": item.get("reference_range"),
        }
        for item in entries
    ]
    enriched_biomarkers = enrich_biomarkers_with_nutrition_ranges(biomarker_like_entries)

    merged: list[dict[str, Any]] = []
    for original, enriched in zip(entries, enriched_biomarkers):
        merged_entry = dict(original)
        if enriched.get("nutrition_marker_key"):
            merged_entry["nutrition_marker_key"] = enriched.get("nutrition_marker_key")
            merged_entry["nutrition_optimal_range"] = enriched.get("nutrition_optimal_range")
            merged_entry["nutrition_status"] = enriched.get("nutrition_status")
            merged_entry["nutrition_range_basis"] = enriched.get("nutrition_range_basis")
            merged_entry["nutrition_overlay_enabled"] = True
        else:
            merged_entry["nutrition_overlay_enabled"] = False
        merged.append(merged_entry)
    return merged
