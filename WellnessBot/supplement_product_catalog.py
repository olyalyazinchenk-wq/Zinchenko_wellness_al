from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


SUPPLEMENT_CATALOG_VERSION = "2026-04-25-v1"


@dataclass(frozen=True, slots=True)
class SupplementProduct:
    key: str
    brand: str
    name: str
    source_url: str
    availability_status: str
    category: str
    form: str
    active_components: tuple[str, ...]
    linked_markers: tuple[str, ...]
    linked_goals: tuple[str, ...]
    label_use: str | None
    safety_notes: tuple[str, ...]
    hard_exclusions: tuple[str, ...]
    recommendation_role: str


PRODUCTS: dict[str, SupplementProduct] = {
    "sw_vitamin_d3_500820": SupplementProduct(
        key="sw_vitamin_d3_500820",
        brand="Siberian Wellness",
        name="Витамин D3 - Essential Vitamins",
        source_url="https://ru.siberianhealth.com/ru/shop/catalog/product/500820/",
        availability_status="active_official_page",
        category="vitamin_d",
        form="drops",
        active_components=("витамин D3 (холекальциферол)", "МСТ-масло"),
        linked_markers=("vitamin_d",),
        linked_goals=("vitamin_d_support", "immune_support", "bone_support"),
        label_use="2 капли содержат 10 мкг (400 ME) витамина D3; способ применения смотреть по официальной этикетке.",
        safety_notes=(
            "Не использовать как лечебную дозировку при дефиците без врача.",
            "Учитывать беременность, ГВ, заболевания почек, кальций, камни, саркоидоз/гранулематозные состояния и другие препараты.",
        ),
        hard_exclusions=("hypercalcemia_or_unknown_calcium_status_with_risk", "pregnancy_or_breastfeeding_without_doctor"),
        recommendation_role="primary_siberian_wellness",
    ),
    "sw_vitamin_d3_max_501644": SupplementProduct(
        key="sw_vitamin_d3_max_501644",
        brand="Siberian Wellness",
        name="Витамин D3 MAX - Essential Vitamins",
        source_url="https://ru.siberianhealth.com/ru/shop/catalog/product/501644/",
        availability_status="active_official_page",
        category="vitamin_d",
        form="drops",
        active_components=("витамин D3 (холекальциферол)", "МСТ-масло"),
        linked_markers=("vitamin_d",),
        linked_goals=("vitamin_d_support", "immune_support", "bone_support"),
        label_use="1 капля содержит 12,5 мкг (500 ME) витамина D3; способ применения смотреть по официальной этикетке.",
        safety_notes=(
            "Не подбирать дозировку ботом при выраженном дефиците.",
            "Согласовать с врачом при беременности, ГВ, заболеваниях почек, нарушениях кальциевого обмена.",
        ),
        hard_exclusions=("hypercalcemia_or_unknown_calcium_status_with_risk", "pregnancy_or_breastfeeding_without_doctor"),
        recommendation_role="primary_siberian_wellness",
    ),
    "sw_organic_magnesium_500629": SupplementProduct(
        key="sw_organic_magnesium_500629",
        brand="Siberian Wellness",
        name="Органический магний - Essential Minerals",
        source_url="https://ru.siberianhealth.com/ru/shop/catalog/product/500629/",
        availability_status="active_official_page",
        category="magnesium_stress_sleep",
        form="capsules",
        active_components=("магния цитрат", "экстракт валерианы", "боярышник", "шлемник байкальский"),
        linked_markers=(),
        linked_goals=("stress_support", "sleep_support", "muscle_support"),
        label_use="Официальная страница указывает 3 капсулы в день во время еды; использовать только как этикеточную информацию.",
        safety_notes=(
            "Осторожность при низком давлении, седативных препаратах, беременности/ГВ, заболеваниях почек.",
            "Магний разносить с L-тироксином, железом, кальцием и некоторыми лекарствами по согласованию со специалистом.",
        ),
        hard_exclusions=("kidney_disease_without_doctor", "sedative_medication_without_review"),
        recommendation_role="primary_siberian_wellness",
    ),
    "sw_omega3_ultra_500484": SupplementProduct(
        key="sw_omega3_ultra_500484",
        brand="Siberian Wellness",
        name="Омега-3 Ультра - Fitness Catalyst",
        source_url="https://ru.siberianhealth.com/ru/shop/catalog/product/500484/",
        availability_status="active_official_page",
        category="omega_3",
        form="capsules",
        active_components=("концентрат омега-3 ПНЖК морских рыб", "витамин E"),
        linked_markers=("lipids",),
        linked_goals=("cardiometabolic_support", "inflammation_support", "skin_support"),
        label_use="Официальная страница указывает 4 капсулы содержат 1,8 г EPA/DHA; способ применения смотреть по этикетке.",
        safety_notes=(
            "Осторожность при антикоагулянтах/антиагрегантах, кровоточивости, операции, аллергии на рыбу/морепродукты.",
            "При обильных кровотечениях сначала оценить врачебный риск.",
        ),
        hard_exclusions=("fish_allergy", "anticoagulants_or_bleeding_without_doctor", "planned_surgery_without_doctor"),
        recommendation_role="primary_siberian_wellness",
    ),
    "sw_organic_iron_500627": SupplementProduct(
        key="sw_organic_iron_500627",
        brand="Siberian Wellness",
        name="Органическое железо - Essential Minerals",
        source_url="https://ru.siberianhealth.com/ru/shop/catalog/product/500627/",
        availability_status="discontinued_official_page",
        category="iron",
        form="capsules",
        active_components=("фумарат железа", "аскорбат железа", "витамины группы B", "витамин C"),
        linked_markers=("ferritin", "hemoglobin", "iron_profile"),
        linked_goals=("iron_support",),
        label_use="Официальная страница содержит этикеточную схему, но продукт отмечен как снятый с производства.",
        safety_notes=(
            "Железо не рекомендовать как самоназначение.",
            "Сначала уточнить ОАК, ферритин, железный профиль, источник потерь и врачебную тактику.",
        ),
        hard_exclusions=("not_available", "iron_without_doctor"),
        recommendation_role="reference_only_not_recommendable",
    ),
    "vitamax_d3_activator_7913": SupplementProduct(
        key="vitamax_d3_activator_7913",
        brand="Vitamax",
        name="D3 Активатор",
        source_url="https://store.vitamax.ru/catalog/immunitet/7913/",
        availability_status="active_official_page",
        category="vitamin_d_complex",
        form="capsules",
        active_components=("витамин D3", "витамин K2", "магний", "цинк", "селен", "витамины C/E/B2/B3"),
        linked_markers=("vitamin_d",),
        linked_goals=("vitamin_d_support", "immune_support"),
        label_use="Официальная страница указывает взрослым по 1 капсуле в день во время еды; использовать только как этикеточную информацию.",
        safety_notes=(
            "Комплекс содержит селен, цинк, K2 и магний; проверять совместимость с фоном и препаратами.",
            "Осторожность при антикоагулянтах, беременности/ГВ, заболеваниях щитовидной железы, почек и нарушениях кальциевого обмена.",
        ),
        hard_exclusions=("anticoagulants_without_doctor", "thyroid_disease_with_selenium_or_iodine_risk_without_doctor"),
        recommendation_role="alternative_vitamax",
    ),
    "vitamax_vita_d3": SupplementProduct(
        key="vitamax_vita_d3",
        brand="Vitamax",
        name="Вита D3",
        source_url="https://vitamax.shop/vita-d3",
        availability_status="active_store_page",
        category="vitamin_d",
        form="spray",
        active_components=("витамин D3", "витамин E"),
        linked_markers=("vitamin_d",),
        linked_goals=("vitamin_d_support",),
        label_use="Страница указывает 1 впрыск содержит 600 ME D3; способ применения смотреть по этикетке.",
        safety_notes=(
            "Проверять беременность/ГВ, кальций, почки, камни, сопутствующие препараты.",
            "Не использовать как лечебную дозировку без врача.",
        ),
        hard_exclusions=("hypercalcemia_or_unknown_calcium_status_with_risk", "pregnancy_or_breastfeeding_without_doctor"),
        recommendation_role="alternative_vitamax",
    ),
    "vitamax_vita_omega3_600": SupplementProduct(
        key="vitamax_vita_omega3_600",
        brand="Vitamax",
        name="Вита Омега-3 600",
        source_url="https://vitamax.shop/vita-omega-3-600",
        availability_status="active_store_page",
        category="omega_3",
        form="capsules",
        active_components=("рыбий жир", "омега-3 ПНЖК 600 мг", "смесь токоферолов"),
        linked_markers=("lipids",),
        linked_goals=("cardiometabolic_support", "inflammation_support"),
        label_use="Страница указывает 600 мг омега-3 на 1 капсулу; способ применения смотреть по этикетке.",
        safety_notes=(
            "Осторожность при антикоагулянтах/антиагрегантах, кровоточивости, операции, аллергии на рыбу/морепродукты.",
            "При обильных кровотечениях сначала оценить врачебный риск.",
        ),
        hard_exclusions=("fish_allergy", "anticoagulants_or_bleeding_without_doctor", "planned_surgery_without_doctor"),
        recommendation_role="alternative_vitamax",
    ),
}


GOAL_TO_PRODUCT_KEYS: dict[str, tuple[str, ...]] = {
    "vitamin_d_support": (
        "sw_vitamin_d3_500820",
        "sw_vitamin_d3_max_501644",
        "vitamax_d3_activator_7913",
        "vitamax_vita_d3",
    ),
    "stress_support": (
        "sw_organic_magnesium_500629",
    ),
    "sleep_support": (
        "sw_organic_magnesium_500629",
    ),
    "omega_3_support": (
        "sw_omega3_ultra_500484",
        "vitamax_vita_omega3_600",
    ),
    "iron_support": (
        "sw_organic_iron_500627",
    ),
}


MARKER_TO_GOALS: dict[str, tuple[str, ...]] = {
    "vitamin_d": ("vitamin_d_support",),
    "ferritin": ("iron_support",),
    "hba1c": (),
    "fasting_glucose": (),
    "tsh": (),
    "b12": (),
}


def product_to_dict(product: SupplementProduct) -> dict[str, Any]:
    return asdict(product)


def export_supplement_catalog() -> dict[str, Any]:
    return {
        "version": SUPPLEMENT_CATALOG_VERSION,
        "policy": {
            "primary_brand": "Siberian Wellness",
            "alternative_brand": "Vitamax",
            "medical_boundary": "Продукты являются нутрицевтическими ориентирами, не лекарственным назначением.",
            "recommendation_rule": "Рекомендовать только active_* продукты; discontinued/reference_only продукты показывать только как недоступные или требующие замены.",
        },
        "products": {key: product_to_dict(value) for key, value in PRODUCTS.items()},
        "goal_to_product_keys": GOAL_TO_PRODUCT_KEYS,
        "marker_to_goals": MARKER_TO_GOALS,
    }


def get_candidate_products_for_goals(goals: list[str]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    products: list[dict[str, Any]] = []
    for goal in goals:
        for key in GOAL_TO_PRODUCT_KEYS.get(goal, ()):
            if key in seen:
                continue
            seen.add(key)
            product = PRODUCTS.get(key)
            if product:
                products.append(product_to_dict(product))
    return products


def build_supplement_context(medical_skill_context: dict[str, Any], medical_context: dict[str, Any]) -> dict[str, Any]:
    del medical_context
    goals: list[str] = []
    for item in medical_skill_context.get("biomarker_analysis", []):
        marker_key = item.get("marker_key")
        status = item.get("nutrition_status")
        if marker_key and status in {"below_nutrition_range", "above_nutrition_range"}:
            for goal in MARKER_TO_GOALS.get(marker_key, ()):
                if goal not in goals:
                    goals.append(goal)

    candidates = get_candidate_products_for_goals(goals)
    recommendable = [
        item for item in candidates
        if str(item.get("availability_status", "")).startswith("active")
        and item.get("recommendation_role") != "reference_only_not_recommendable"
    ]
    unavailable = [
        item for item in candidates
        if not str(item.get("availability_status", "")).startswith("active")
        or item.get("recommendation_role") == "reference_only_not_recommendable"
    ]

    return {
        "catalog_version": SUPPLEMENT_CATALOG_VERSION,
        "goals": goals,
        "recommendable_candidates": recommendable,
        "unavailable_or_reference_only": unavailable,
        "rules": [
            "Сначала предлагать Siberian Wellness, затем Vitamax как альтернативу.",
            "Не рекомендовать снятые с производства продукты как доступный вариант.",
            "Железо, йод, селен, гормонально-активные комплексы и лечебные дозировки не назначать ботом.",
            "При беременности, ГВ, детях, онкологии, антикоагулянтах, щитовидной железе, почках или кровоточивости выводить врачебную осторожность.",
            "Если врач уже назначил схему, бот может помочь разложить время приема, совместимость и наблюдение реакции, не меняя назначение.",
        ],
    }
