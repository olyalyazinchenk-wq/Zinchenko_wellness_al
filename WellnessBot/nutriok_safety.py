from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from nutriok_product import normalize_product_code, requires_human_review


def _normalize_ru(text: str | None) -> str:
    return str(text or "").lower().replace("ё", "е")


def _within_words(group_a: str, group_b: str, max_words: int = 4) -> str:
    gap = rf"(?:\s+[^\s,.;!?\n]+){{0,{max_words}}}\s+"
    return rf"(?:(?:{group_a}){gap}(?:{group_b})|(?:{group_b}){gap}(?:{group_a}))"


BENIGN_LAB_OR_DIET_PHRASES_PATTERN = re.compile(
    r"\b(?:общ\w+\s+|клиническ\w+\s+|биохимическ\w+\s+)?анализ\w*\s+(?:кров\w*|кал\w*|моч\w*)"
    r"(?:\s+и\s+(?:кал\w*|кров\w*|моч\w*))?\b"
    r"|\bсда(?:ла?|ть|вала?|ю)\s+(?:кров\w*|кал\w*|анализ\w*)\b"
)

PAST_OR_NEGATED_PREGNANCY_PATTERN = re.compile(
    r"\bне\s+беременн\w*"
    r"|\bне\s+кормл\w+(?:\s+грудью)?"
    r"|\bбеременност\w*\s+(?:нет|не\s+планирую)"
    r"|\bпланиру\w+\s+беременност\w*(?:\s+через\s+[^\n,.;!?]+)?"
    r"|\bпосле\s+(?:завершен\w+|окончан\w+|прекращен\w+)\s+(?:грудн\w+\s+вскармливан\w*|\bгв\b|лактаци\w*)"
    r"|(?:грудн\w+\s+вскармливан\w*|\bгв\b|кормл\w+\s+грудью|лактаци\w*|беременност\w*)"
    r"\s+[^\n,.;!?]{0,35}?\b(?:закончил\w*|завершил\w*|прекратил\w*|была|год\w*\s+назад|месяц\w*\s+назад|в\s+прошлом)\b"
    r"|\b(?:закончил\w*|завершил\w*|прекратил\w*)\s+[^\n,.;!?]{0,30}?\b"
    r"(?:грудн\w+\s+вскармливан\w*|\bгв\b|кормит\w*\s+грудью|кормл\w+\s+грудью|лактаци\w*)"
)

RED_FLAG_PATTERNS: dict[str, re.Pattern[str]] = {
    "blood_in_stool_or_vomit": re.compile(
        "|".join(
            [
                _within_words(
                    r"\b(?:кров\w*|кровав\w*)\b",
                    r"(?:\b(?:стул\w*|кал\w*|дефекац\w*|туалет\w*|унитаз\w*|анус\w*)\b|прям\w+\s+кишк\w*)",
                    4,
                ),
                _within_words(
                    r"\b(?:кров\w*|кровав\w*)\b",
                    r"\b(?:рвот\w*|рвал\w*|вырвал\w*|стошнил\w*)\b",
                    4,
                ),
                r"\bкофейн\w+\s+гущ\w*",
            ]
        )
    ),
    "black_tarry_stool": re.compile(
        "|".join(
            [
                _within_words(
                    r"\b(?:стул\w*|кал\w*|испражнени\w*)\b",
                    r"\b(?:черн\w*|дегт\w*|деготь)\b",
                    4,
                ),
                r"\bмелен[аыеу]\b",
            ]
        )
    ),
    "rapid_weight_loss": re.compile(
        "|".join(
            [
                _within_words(
                    r"\b(?:резк\w+|стремительн\w+)\b",
                    r"(?:\b(?:похуден\w*|похудел\w*)\b|(?:снижен\w+|потер\w+|сброс\w+|уход\w*)\s+вес\w*|\bвес\s+(?:упал\w*|ушел|снизил\w*))",
                    4,
                ),
                r"\b(?:похудел\w*|потерял\w*|сбросил\w*|ушло)\s+[^\n.;!?]{0,30}?\b\d+\s*(?:кг|килограмм\w*)\b"
                r"[^\n.;!?]{0,45}?\b(?:без\s+(?:\w+\s+)?причин\w*|сам[аио]?\s+по\s+себе|не\s+стараясь|не\s+худея|за\s+(?:месяц|\d+\s*недел\w*))\b",
                r"\b(?:без\s+(?:\w+\s+)?причин\w*|сам[аио]?\s+по\s+себе|не\s+стараясь|не\s+худея|за\s+(?:месяц|\d+\s*недел\w*))\s+"
                r"[^\n.;!?]{0,30}?\b(?:похудел\w*|потерял\w*|сбросил\w*|ушло)\s+[^\n.;!?]{0,25}?\b\d+\s*(?:кг|килограмм\w*)\b",
                r"\b(?:похудел\w*|потерял\w*|сбросил\w*|ушло)\s+[^\n.;!?]{0,30}?\b"
                r"(?:без\s+(?:\w+\s+)?причин\w*|сам[аио]?\s+по\s+себе|не\s+стараясь|не\s+худея|за\s+(?:месяц|\d+\s*недел\w*))\s+"
                r"[^\n.;!?]{0,25}?\b\d+\s*(?:кг|килограмм\w*)\b",
            ]
        )
    ),
    "jaundice": re.compile(
        "|".join(
            [
                r"\bжелтух\w*",
                _within_words(
                    r"\b(?:пожелтел\w*|желт\w+)\b",
                    r"\b(?:кож\w*|глаз\w*|белк\w*|склер\w*)\b",
                    4,
                ),
            ]
        )
    ),
    "prolonged_fever": re.compile(
        r"\bтемператур\w*[^\n.;!?]{0,45}?\b(?:недел\w*|\d+\s*дн(?:ей|я)|несколько\s+дней|много\s+дней|вторую\s+неделю)\b"
    ),
    "angioedema": re.compile(
        "|".join(
            [
                _within_words(
                    r"\b(?:отек\w*|опух\w*)\b",
                    r"\b(?:лиц\w*|губ\w*|горл\w*|гортан\w*|язык\w*|ше[ияю])\b",
                    4,
                ),
                r"\bотек\w*\s+квинке\b",
            ]
        )
    ),
    "syncope": re.compile(
        "|".join(
            [
                r"\b(?:обморок\w*|предобморочн\w*)",
                _within_words(r"\b(?:теря\w+|потер\w+|лишил\w*)\b", r"\bсознани\w*\b", 4),
            ]
        )
    ),
    "chest_pain": re.compile(
        _within_words(
            r"\b(?:бол\w*|давит|сжима\w*|жжет|жжени\w*|печет)\b",
            r"(?:в\s+груд\w*|за\s+грудин\w*|грудн\w+\s+клетк\w*|област\w*\s+сердц\w*)",
            4,
        )
    ),
    "dyspnea_at_rest": re.compile(
        "|".join(
            [
                _within_words(
                    r"\b(?:одышк\w*|задыха\w*|удушь\w*)\b",
                    r"\b(?:поко\w*|лежа|сидя|без\s+нагрузк\w*)\b",
                    4,
                ),
                r"(?:не\s+могу|тяжело|трудно|нечем)\s+дышат\w*",
            ]
        )
    ),
    "severe_bleeding": re.compile(
        _within_words(r"\b(?:сильн\w+|обильн\w+|неукротим\w+)\b", r"\bкровотечени\w*\b", 4)
    ),
    "suicidal_ideation": re.compile(
        r"не\s+хочу\s+жит\w*|хочу\s+умерет\w*|покончит\w*(?:\s+с\s+собой|\s+с\s+жизн\w*)?|\bсуицид\w*|мысл\w+\s+о\s+смерт\w*"
    ),
    "eating_disorder": re.compile(
        "|".join(
            [
                _within_words(r"\b(?:вызыва\w+|провоциру\w+)\b", r"\bрвот\w*\b", 4),
                r"\bне\s+ем\s+(?:по\s+|уже\s+)?(?:\d+|несколько|много|нескольку)\s*(?:дн\w*|сут\w*)\b",
                _within_words(
                    r"\b(?:слабительн\w*|мочегонн\w*|диуретик\w*)\b",
                    r"\b(?:похуден\w*|снижен\w+\s+вес\w*|сброс\w+\s+вес\w*)\b",
                    4,
                ),
            ]
        )
    ),
}

HIGH_RISK_MEDICATION_PATTERN = re.compile(
    r"\b(?:антикоагулянт\w*|варфарин\w*|эликвис\w*|апиксабан\w*|ксарелто|ривароксабан\w*|"
    r"прадакса|дабигатран\w*|гепарин\w*|клексан\w*|инсулин\w*|химиотерапи\w*|цитостатик\w*|"
    r"антидепрессант\w*|сиозс|флуоксетин\w*|сертралин\w*|эсциталопрам\w*|пароксетин\w*|"
    r"венлафаксин\w*|дулоксетин\w*|амитриптилин\w*)\b"
)

PREGNANCY_LACTATION_PATTERN = re.compile(
    r"\b(?:беременн\w*|кормл\w+\s+грудью|грудн\w+\s+вскармливан\w*|лактаци\w*|на\s+гв)\b"
)

SUPPLEMENT_REQUEST_PATTERN = re.compile(
    r"\b(?:бад\w*|витамин\w*|добавк\w*|нутрицевтик\w*|омега|магний|железо)\b"
)

UNDERAGE_TEXT_PATTERN = re.compile(
    r"\b(?:мне|возраст|ребенку|подростку)\s*:?\s*(?:1[0-7]|[1-9])\s*(?:лет|год\w*)\b"
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

RED_FLAG_CLIENT_MESSAGE = (
    "Пожалуйста, обратитесь к врачу: в анкете отмечены симптомы или состояния, которые требуют "
    "очной медицинской оценки. Я передала вашу анкету Ольге Ковалевой — автоматические нутрициологические "
    "рекомендации в такой ситуации не выдаются."
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


def _submission_corpus(submission: dict[str, Any]) -> str:
    intake = submission.get("intake") if isinstance(submission.get("intake"), dict) else {}
    return _normalize_ru(
        _flatten_text(
            {
                "symptoms": submission.get("symptoms") or intake.get("symptoms"),
                "red_flags": submission.get("red_flags"),
                "background": submission.get("background"),
                "risk_details": submission.get("risk_details"),
                "medications": submission.get("medications") or intake.get("medications"),
                "allergies": submission.get("allergies") or intake.get("allergies"),
                "lifestyle": submission.get("lifestyle") or intake.get("lifestyle"),
                "nutrition_diary": submission.get("nutrition_diary") or intake.get("nutrition_diary"),
                "goal_notes": submission.get("goal") or intake.get("primary_goal"),
            }
        )
    )


def is_underage(submission: dict[str, Any]) -> bool:
    for container in (
        submission,
        submission.get("profile") if isinstance(submission.get("profile"), dict) else {},
        submission.get("intake") if isinstance(submission.get("intake"), dict) else {},
    ):
        age_raw = container.get("age")
        if age_raw is not None and not isinstance(age_raw, bool):
            try:
                if int(str(age_raw).strip()) < 18:
                    return True
            except ValueError:
                pass
    corpus = _submission_corpus(submission)
    return bool(UNDERAGE_TEXT_PATTERN.search(corpus))


def find_red_flags(submission: dict[str, Any]) -> list[str]:
    raw_corpus = _submission_corpus(submission)
    corpus = BENIGN_LAB_OR_DIET_PHRASES_PATTERN.sub(" ", raw_corpus)
    matched: list[str] = []
    for name, pattern in RED_FLAG_PATTERNS.items():
        if pattern.search(corpus):
            matched.append(name)
    if is_underage(submission):
        matched.append("underage_lt_18")
    return matched


def find_high_risk_medications(submission: dict[str, Any]) -> list[str]:
    intake = submission.get("intake") if isinstance(submission.get("intake"), dict) else {}
    med_corpus = _normalize_ru(
        _flatten_text(
            {
                "medications": submission.get("medications") or intake.get("medications"),
                "background": submission.get("background"),
                "symptoms": submission.get("symptoms") or intake.get("symptoms"),
            }
        )
    )
    matches = HIGH_RISK_MEDICATION_PATTERN.findall(med_corpus)
    return list(dict.fromkeys(matches))


def has_pregnancy_supplement_conflict(
    submission: dict[str, Any],
    draft_text: str | None = None,
) -> bool:
    raw_corpus = _submission_corpus(submission)
    cleaned_corpus = PAST_OR_NEGATED_PREGNANCY_PATTERN.sub(" ", raw_corpus)
    if not PREGNANCY_LACTATION_PATTERN.search(cleaned_corpus):
        return False
    if SUPPLEMENT_REQUEST_PATTERN.search(raw_corpus):
        return True
    if contains_supplement_offer(draft_text) or SUPPLEMENT_REQUEST_PATTERN.search(_normalize_ru(draft_text)):
        return True
    return False


def find_unsafe_claims(draft_text: str | None) -> list[str]:
    text = _normalize_ru(draft_text)
    return [name for name, pattern in UNSAFE_CLAIM_PATTERNS.items() if pattern.search(text)]


def contains_supplement_offer(draft_text: str | None) -> bool:
    normalized = _normalize_ru(draft_text)
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

    high_risk_meds = find_high_risk_medications(submission)
    if high_risk_meds:
        reasons.append("high_risk_medications:" + ",".join(high_risk_meds))

    if has_pregnancy_supplement_conflict(submission, draft_text):
        reasons.append("pregnancy_or_lactation_supplement_review")

    unsafe_claims = find_unsafe_claims(draft_text)
    if unsafe_claims:
        reasons.append("unsafe_claims:" + ",".join(unsafe_claims))

    if contains_supplement_offer(draft_text):
        reasons.append("supplement_offer_requires_olga_approval")

    if requires_human_review(code):
        reasons.append("tier_requires_olga_approval")

    if reasons:
        safety_triggered = bool(red_flags or high_risk_meds or unsafe_claims)
        status = "awaiting_safety_review" if safety_triggered else "awaiting_expert_review"
        return DeliveryDecision(False, status, tuple(reasons))

    return DeliveryDecision(True, "approved_for_automatic_delivery", ())
