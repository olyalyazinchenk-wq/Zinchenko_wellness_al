from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from nutriok_product import normalize_product_code, requires_human_review


RED_FLAG_MARKERS = (
    "боль в груди",
    "не могу дышать",
    "тяжело дышать",
    "кровь в стуле",
    "кровь в рвоте",
    "потеря сознания",
    "сильное кровотечение",
    "хочу умереть",
    "не хочу жить",
)

UNSAFE_CLAIM_PATTERNS = {
    "diagnosis": re.compile(r"\b(?:у вас|это)\s+(?:диагноз|анемия|гипотиреоз|сибр)\b", re.IGNORECASE),
    "treatment": re.compile(r"\b(?:назначаю|лечение состоит|лечить будем|вылечит)\b", re.IGNORECASE),
    "medication_change": re.compile(
        r"\b(?:отмените|прекратите принимать|замените)\s+(?:лекарство|препарат|таблетк)",
        re.IGNORECASE,
    ),
    "guarantee": re.compile(r"\b(?:гарантированно|точно)\s+(?:вылечит|устранит|нормализует)\b", re.IGNORECASE),
}

SUPPLEMENT_MARKERS = (
    "vitamax",
    "витамакс",
    "siberian wellness",
    "сибирское здоровье",
    "промокод",
    "партнерская ссылка",
    "партнёрская ссылка",
)


@dataclass(frozen=True)
class DeliveryDecision:
    allow_automatic_delivery: bool
    status: str
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_flatten_text(item) for item in value.values())
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten_text(item) for item in value)
    return str(value or "")


def find_red_flags(submission: dict[str, Any]) -> list[str]:
    corpus = _flatten_text(
        {
            "symptoms": submission.get("symptoms"),
            "red_flags": submission.get("red_flags"),
            "background": submission.get("background"),
            "risk_details": submission.get("risk_details"),
        }
    ).lower().replace("ё", "е")
    return [marker for marker in RED_FLAG_MARKERS if marker.replace("ё", "е") in corpus]


def find_unsafe_claims(draft_text: str | None) -> list[str]:
    text = str(draft_text or "")
    return [name for name, pattern in UNSAFE_CLAIM_PATTERNS.items() if pattern.search(text)]


def contains_supplement_offer(draft_text: str | None) -> bool:
    normalized = str(draft_text or "").lower().replace("ё", "е")
    return any(marker.replace("ё", "е") in normalized for marker in SUPPLEMENT_MARKERS)


def evaluate_delivery_gate(
    raw_code: str | None,
    draft_text: str | None,
    submission: dict[str, Any],
) -> DeliveryDecision:
    code = normalize_product_code(raw_code)
    reasons: list[str] = []

    red_flags = find_red_flags(submission)
    if red_flags:
        reasons.append("red_flags:" + ",".join(red_flags))

    unsafe_claims = find_unsafe_claims(draft_text)
    if unsafe_claims:
        reasons.append("unsafe_claims:" + ",".join(unsafe_claims))

    if contains_supplement_offer(draft_text):
        reasons.append("supplement_offer_requires_olga_approval")

    if requires_human_review(code):
        reasons.append("tier_requires_olga_approval")

    if reasons:
        status = "awaiting_safety_review" if red_flags or unsafe_claims else "awaiting_expert_review"
        return DeliveryDecision(False, status, tuple(reasons))

    return DeliveryDecision(True, "approved_for_automatic_delivery", ())
