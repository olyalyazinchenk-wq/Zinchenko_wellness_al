from __future__ import annotations

from typing import Any


def normalize_marker_text(value: str | None) -> str:
    return " ".join((value or "").lower().replace("ё", "е").split())


def normalize_unit_text(value: str | None) -> str:
    return normalize_marker_text(value).replace(" ", "")


NUTRITION_REFERENCE_CATALOG: dict[str, dict[str, Any]] = {
    "ferritin": {
        "aliases": ("ферритин",),
        "acceptable_units": {"нг/мл", "мкг/л", "ng/ml", "ug/l"},
        "allow_missing_unit": True,
        "optimal_min": 40.0,
        "optimal_max": 90.0,
        "display_range": "40-90 нг/мл",
        "basis": "нутрициологический ориентир v1",
    },
    "vitamin_d": {
        "aliases": ("витамин d", "витаминд", "25-oh", "25(oh)", "25 oh", "25-гидроксивитамин d"),
        "acceptable_units": {"нг/мл", "ng/ml"},
        "allow_missing_unit": True,
        "optimal_min": 50.0,
        "optimal_max": 80.0,
        "display_range": "50-80 нг/мл",
        "basis": "нутрициологический ориентир v1",
    },
    "tsh": {
        "aliases": ("ттг", "tsh", "тиреотроп"),
        "acceptable_units": {"мме/л", "мед/л", "мкме/мл", "miu/l", "uiu/ml", "mu/l"},
        "allow_missing_unit": True,
        "optimal_min": 1.0,
        "optimal_max": 2.5,
        "display_range": "1.0-2.5 мМЕ/л",
        "basis": "нутрициологический ориентир v1",
    },
    "b12": {
        "aliases": ("витамин b12", "b12", "цианокобаламин", "кобаламин"),
        "acceptable_units": {"пг/мл", "pg/ml"},
        "allow_missing_unit": True,
        "optimal_min": 500.0,
        "optimal_max": 900.0,
        "display_range": "500-900 пг/мл",
        "basis": "нутрициологический ориентир v1",
    },
    "fasting_glucose": {
        "aliases": ("глюкоза", "glucose"),
        "acceptable_units": {"ммоль/л", "mmol/l"},
        "allow_missing_unit": False,
        "optimal_min": 4.6,
        "optimal_max": 5.2,
        "display_range": "4.6-5.2 ммоль/л",
        "basis": "нутрициологический ориентир v1",
    },
    "hba1c": {
        "aliases": ("гликированный гемоглобин", "hba1c", "гликирован"),
        "acceptable_units": {"%"},
        "allow_missing_unit": False,
        "optimal_min": 4.8,
        "optimal_max": 5.4,
        "display_range": "4.8-5.4 %",
        "basis": "нутрициологический ориентир v1",
    },
}


def match_nutrition_reference_entry(marker_name: str, unit: str | None = None) -> tuple[str | None, dict[str, Any] | None]:
    normalized_name = normalize_marker_text(marker_name)
    normalized_unit = normalize_unit_text(unit)

    for key, entry in NUTRITION_REFERENCE_CATALOG.items():
        if any(alias in normalized_name for alias in entry["aliases"]):
            acceptable_units = {normalize_unit_text(item) for item in entry["acceptable_units"]}
            if normalized_unit:
                if normalized_unit not in acceptable_units:
                    return None, None
            elif not entry.get("allow_missing_unit"):
                return None, None
            return key, entry
    return None, None


def parse_numeric_value(value: Any) -> float | None:
    try:
        return float(str(value).replace(",", ".").strip())
    except (TypeError, ValueError):
        return None


def compute_nutrition_status(value: float, optimal_min: float, optimal_max: float) -> str:
    if value < optimal_min:
        return "below_nutrition_range"
    if value > optimal_max:
        return "above_nutrition_range"
    return "within_nutrition_range"


def enrich_biomarkers_with_nutrition_ranges(biomarkers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []

    for biomarker in biomarkers:
        annotated = dict(biomarker)
        marker_key, entry = match_nutrition_reference_entry(
            str(biomarker.get("name") or ""),
            biomarker.get("unit"),
        )
        if not entry:
            enriched.append(annotated)
            continue

        value = parse_numeric_value(biomarker.get("value"))
        if value is None:
            enriched.append(annotated)
            continue

        annotated["nutrition_marker_key"] = marker_key
        annotated["nutrition_optimal_range"] = entry["display_range"]
        annotated["nutrition_range_basis"] = entry["basis"]
        annotated["nutrition_status"] = compute_nutrition_status(
            value,
            entry["optimal_min"],
            entry["optimal_max"],
        )
        enriched.append(annotated)

    return enriched
