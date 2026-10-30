from __future__ import annotations

from typing import Any


SUPPLEMENT_PROTOCOL_VERSION = "2026-07-16-v1"
PROTOCOL_ENABLED_PRODUCT_KEYS = {"vitamax_endoflora_8251"}

NEGATED_PHRASES = (
    "беременности нет",
    "беременности и гв нет",
    "не беременна",
    "гв нет",
    "не кормлю грудью",
    "аллергий нет",
    "аллергии отсутствуют",
    "лекарства не принимаю",
    "лекарств не принимаю",
    "препараты не принимаю",
    "бадов не принимаю",
    "лекарств и бадов нет",
    "лекарства и бады не принимаю",
    "хронических заболеваний нет",
    "диагнозов нет",
)

ACUTE_RED_FLAGS = (
    "кровь в стуле",
    "черный стул",
    "чёрный стул",
    "сильная боль",
    "острая боль",
    "высокая температура",
    "желтуха",
    "резкое похудение",
    "стойкая диарея",
    "обморок",
)

RISK_MARKERS: dict[str, tuple[str, ...]] = {
    "pregnancy": ("беременна", "беременность"),
    "breastfeeding": ("грудное вскармливание", "кормлю грудью", "лактация", "гв"),
    "oncology": ("онколог", "химиотерап", "лучевая терап"),
    "kidney_disease": ("почечная недостаточ", "болезнь почек", "нефрит", "диализ"),
    "liver_disease": ("печеночная недостаточ", "печёночная недостаточ", "цирроз", "гепатит"),
    "severe_immunocompromise": ("иммунодефиц", "нейтропен", "трансплантац"),
    "active_heartburn_or_reflux": ("изжог", "рефлюкс", "гэрб"),
    "gastritis_or_peptic_ulcer": ("гастрит", "язв"),
    "gallstones_or_biliary_obstruction": ("камни в желч", "желчнокамен", "билиарн", "желтуха"),
    "pancreatitis": ("панкреатит",),
    "anticoagulants_or_bleeding": ("антикоаг", "варфарин", "апиксабан", "ривароксабан", "кровоточ"),
}

GLOBAL_BLOCK_FLAGS = {
    "lab_data_requires_resubmission",
    "acute_gi_red_flags",
    "pregnancy",
    "breastfeeding",
    "oncology",
    "kidney_disease",
    "liver_disease",
    "severe_immunocompromise",
    "current_medications_or_supplements",
    "allergy_requires_component_review",
}


def _normalize(value: Any) -> str:
    return " ".join(str(value or "").lower().replace("ё", "е").split())


def _medical_text(submission: dict[str, Any]) -> str:
    medical = submission.get("medical_context")
    if not isinstance(medical, dict):
        medical = {}
    return _normalize(
        " ".join(
            str(medical.get(key) or "")
            for key in (
                "symptoms",
                "digestion",
                "background",
                "risk_details",
                "red_flags",
                "female_hormones",
                "osipov_context",
                "osipov_extra_note",
                "osipov_ocr_text",
            )
        )
    )


def _without_negations(text: str) -> str:
    cleaned = text
    for phrase in NEGATED_PHRASES:
        cleaned = cleaned.replace(_normalize(phrase), " ")
    return " ".join(cleaned.split())


def _adult_confirmed(submission: dict[str, Any]) -> bool:
    if submission.get("adult_confirmed"):
        return True
    profile = submission.get("profile")
    if not isinstance(profile, dict):
        return False
    raw_age = str(profile.get("age") or "")
    numbers = "".join(char if char.isdigit() else " " for char in raw_age).split()
    return bool(numbers and int(numbers[0]) >= 18)


def assess_supplement_safety(submission: dict[str, Any]) -> dict[str, Any]:
    medical = submission.get("medical_context")
    if not isinstance(medical, dict):
        medical = {}
    text = _medical_text(submission)
    risk_text = _without_negations(text)
    background = _normalize(medical.get("background"))
    osipov_context = _normalize(medical.get("osipov_context"))

    medication_status_known = any(
        marker in text
        for marker in ("лекар", "препарат", "бад", "принимаю", "не принимаю")
    )
    allergy_status_known = "аллерг" in text
    diagnosis_status_known = bool(background) or any(
        marker in osipov_context
        for marker in ("диагноз", "заболев", "хронич", "гастрит", "рефлюкс", "панкреат")
    )

    missing: list[str] = []
    if not _adult_confirmed(submission):
        missing.append("подтверждение возраста 18+")
    if not medication_status_known:
        missing.append("полный список лекарств и уже принимаемых БАДов")
    if not allergy_status_known:
        missing.append("аллергии и индивидуальная непереносимость")
    if not diagnosis_status_known:
        missing.append("диагнозы и хронические заболевания либо явное указание, что их нет")
    if not text:
        missing.append("анкета безопасности")

    risk_flags: list[str] = []
    if submission.get("requires_lab_resubmission"):
        risk_flags.append("lab_data_requires_resubmission")
    if any(marker in risk_text for marker in ACUTE_RED_FLAGS):
        risk_flags.append("acute_gi_red_flags")
    for flag, markers in RISK_MARKERS.items():
        if any(_normalize(marker) in risk_text for marker in markers):
            risk_flags.append(flag)

    if any(
        marker in risk_text
        for marker in (
            "принимаю",
            "принимает",
            "л-тирокс",
            "эутирокс",
            "метформин",
            "антибиот",
            "антидепресс",
            "контрацеп",
            "витамин d",
            "магний",
            "омега",
            "пробиот",
        )
    ):
        risk_flags.append("current_medications_or_supplements")
    if "аллерг" in risk_text:
        risk_flags.append("allergy_requires_component_review")

    risk_flags = list(dict.fromkeys(risk_flags))
    return {
        "status": "ready" if not missing and not (set(risk_flags) & GLOBAL_BLOCK_FLAGS) else "needs_clarification",
        "missing_safety_context": missing,
        "risk_flags": risk_flags,
        "medication_status_known": medication_status_known,
        "allergy_status_known": allergy_status_known,
        "diagnosis_status_known": diagnosis_status_known,
        "adult_confirmed": _adult_confirmed(submission),
    }


def _candidate_block_reasons(candidate: dict[str, Any], safety: dict[str, Any]) -> list[str]:
    reasons = list(safety.get("missing_safety_context") or [])
    flags = set(safety.get("risk_flags") or [])
    reasons.extend(sorted(flags & GLOBAL_BLOCK_FLAGS))
    if candidate.get("key") == "vitamax_ksf_pro_8253":
        reasons.extend(
            sorted(
                flags
                & {
                    "active_heartburn_or_reflux",
                    "gastritis_or_peptic_ulcer",
                    "gallstones_or_biliary_obstruction",
                    "pancreatitis",
                }
            )
        )
    if candidate.get("key") not in PROTOCOL_ENABLED_PRODUCT_KEYS:
        reasons.append("нет утвержденного автоматического протокола для этого продукта")
    return list(dict.fromkeys(reasons))


def _build_protocol_recommendations(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for product in products:
        if product.get("key") != "vitamax_endoflora_8251":
            continue
        result.append(
            {
                "protocol_id": "gut_microbiome_endoflora_v1",
                "protocol_version": SUPPLEMENT_PROTOCOL_VERSION,
                "product_key": product["key"],
                "brand": product["brand"],
                "name": product["name"],
                "source_url": product["source_url"],
                "rationale": "Мягкая нутрицевтическая поддержка микробиоты при жалобах ЖКТ и отсутствии стоп-факторов.",
                "label_use": product["label_use"],
                "monitoring": (
                    "Начинать с нижней границы инструкции производителя; 7 дней отслеживать вздутие, боль, стул и переносимость."
                ),
                "stop_signals": (
                    "Прекратить приём и обратиться за очной оценкой при нарастающей боли, крови в стуле, температуре, "
                    "стойкой диарее, аллергической реакции или резком ухудшении."
                ),
                "safety_notes": product.get("safety_notes") or (),
                "commercial_disclosure": (
                    "Для сайта SPZ-03 можно использовать промокод 844131; он может дать скидку клиенту и выгоду владельцу кода."
                ),
                "delivery_status": "draft_requires_human_review",
            }
        )
    return result


def apply_supplement_protocol_guard(
    supplement_context: dict[str, Any],
    submission: dict[str, Any],
) -> dict[str, Any]:
    guarded = dict(supplement_context)
    safety = assess_supplement_safety(submission)
    candidates = [
        item
        for item in supplement_context.get("recommendable_candidates", [])
        if isinstance(item, dict)
    ]
    allowed: list[dict[str, Any]] = []
    blocked = [
        item
        for item in supplement_context.get("blocked_candidates", [])
        if isinstance(item, dict)
    ]

    for candidate in candidates:
        reasons = _candidate_block_reasons(candidate, safety)
        if reasons:
            blocked.append({**candidate, "block_reasons": reasons})
        else:
            allowed.append(candidate)

    recommendations = _build_protocol_recommendations(allowed)
    status = (
        "eligible_for_human_review"
        if recommendations
        else "blocked_safety_context"
        if safety["missing_safety_context"] or (set(safety["risk_flags"]) & GLOBAL_BLOCK_FLAGS)
        else "no_approved_protocol"
    )
    guarded.update(
        {
            "protocol_version": SUPPLEMENT_PROTOCOL_VERSION,
            "safety_assessment": safety,
            "recommendation_status": status,
            "client_delivery_allowed": False,
            "recommendable_candidates": allowed,
            "blocked_candidates": blocked,
            "protocol_recommendations": recommendations,
        }
    )
    return guarded


def build_supplement_scheme_entries(supplement_context: dict[str, Any]) -> list[dict[str, str]]:
    if supplement_context.get("recommendation_status") != "eligible_for_human_review":
        return []
    entries: list[dict[str, str]] = []
    for item in supplement_context.get("protocol_recommendations", []):
        safety = " ".join(str(value) for value in item.get("safety_notes", ()))
        entries.append(
            {
                "time": "После проверки специалистом / этап 1",
                "name": f"{item['name']} ({item['brand']})",
                "comment": (
                    f"Цель: {item['rationale']} Приём: {item['label_use']} Контроль: {item['monitoring']} "
                    f"Стоп-сигналы: {item['stop_signals']} Безопасность: {safety} "
                    f"Официальная страница: {item['source_url']}. {item['commercial_disclosure']}"
                ),
            }
        )
    return entries
