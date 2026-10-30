from __future__ import annotations

from dataclasses import dataclass
from typing import Any


BRAND_NAME = "НутриОК by Olga Kovaleva"
BOT_DISPLAY_NAME = "НутриОК | полный разбор"
CHANNEL_DISPLAY_NAME = "НутриОК | Ольга Ковалева"
BRAND_PROMISE = "Разбор, после которого понятно, что делать"

PARTNER_DISCLOSURE = (
    "Партнерские ссылки: Ольга может получить вознаграждение; "
    "выбор не меняет вашу схему или цену."
)
SUPPLEMENT_DISCLAIMER = "БАД не является лекарственным средством."


@dataclass(frozen=True)
class ProductOffer:
    code: str
    name: str
    pilot_price_rub: int
    regular_price_rub: int
    result: str
    human_review_required: bool
    labs_supported: bool


PRODUCT_OFFERS: dict[str, ProductOffer] = {
    "ok_start": ProductOffer(
        code="ok_start",
        name="ОК-Старт",
        pilot_price_rub=0,
        regular_price_rub=0,
        result="Главная цель, исходная оценка 0-10 и один безопасный первый шаг.",
        human_review_required=False,
        labs_supported=False,
    ),
    "ok_express": ProductOffer(
        code="ok_express",
        name="ОК-Экспресс",
        pilot_price_rub=990,
        regular_price_rub=1490,
        result="Три паттерна по дневнику питания за 3 дня и план на 7 дней.",
        human_review_required=False,
        labs_supported=False,
    ),
    "ok_review": ProductOffer(
        code="ok_review",
        name="ОК-Разбор",
        pilot_price_rub=5900,
        regular_price_rub=7900,
        result="Полный профиль, персональный минимум анализов и стратегия на 30 дней.",
        human_review_required=True,
        labs_supported=True,
    ),
    "ok_result_8": ProductOffer(
        code="ok_result_8",
        name="ОК-Результат 8",
        pilot_price_rub=14900,
        regular_price_rub=19900,
        result="Полный разбор и 8 недель сопровождения с еженедельной адаптацией.",
        human_review_required=True,
        labs_supported=True,
    ),
    "ok_rhythm": ProductOffer(
        code="ok_rhythm",
        name="ОК-Ритм",
        pilot_price_rub=1990,
        regular_price_rub=1990,
        result="Ежемесячное поддержание результата после основной программы.",
        human_review_required=True,
        labs_supported=True,
    ),
}

PRODUCT_ORDER = ("ok_start", "ok_express", "ok_review", "ok_result_8", "ok_rhythm")

# Old codes remain readable so existing cases and invoice payloads are not orphaned.
LEGACY_PRODUCT_ALIASES = {
    "screening": "ok_start",
    "nutri_chat": "ok_express",
    "week": "ok_express",
    "standard": "ok_review",
    "basic": "ok_review",
    "osipov": "ok_review",
    "gut_support_18": "ok_review",
    "premium": "ok_result_8",
    "full": "ok_result_8",
    "vip": "ok_result_8",
    "habits": "ok_result_8",
}

PRIMARY_GOALS = {
    "energy": "Энергия",
    "digestion": "Пищеварение",
    "weight_appetite": "Вес и аппетит",
    "skin_hair": "Кожа и волосы",
    "sleep_stress": "Сон и стресс",
}


def normalize_product_code(raw_code: str | None) -> str:
    code = str(raw_code or "ok_review").strip().lower()
    return LEGACY_PRODUCT_ALIASES.get(code, code if code in PRODUCT_OFFERS else "ok_review")


def get_product_offer(raw_code: str | None) -> ProductOffer:
    return PRODUCT_OFFERS[normalize_product_code(raw_code)]


def requires_human_review(raw_code: str | None) -> bool:
    return get_product_offer(raw_code).human_review_required


def upgrade_amount_due(
    from_code: str,
    to_code: str,
    *,
    pilot: bool = True,
    within_days: int = 30,
) -> int:
    if within_days < 0 or within_days > 30:
        return get_product_offer(to_code).pilot_price_rub if pilot else get_product_offer(to_code).regular_price_rub

    source = get_product_offer(from_code)
    target = get_product_offer(to_code)
    source_price = source.pilot_price_rub if pilot else source.regular_price_rub
    target_price = target.pilot_price_rub if pilot else target.regular_price_rub
    return max(0, target_price - source_price)


def validate_assessment_payload(payload: dict[str, Any], raw_code: str | None) -> list[str]:
    code = normalize_product_code(raw_code)
    errors: list[str] = []

    if str(payload.get("primary_goal") or "") not in PRIMARY_GOALS:
        errors.append("Выберите одну главную цель.")

    baseline = payload.get("baseline_score")
    if isinstance(baseline, bool) or not isinstance(baseline, (int, float)) or not 0 <= baseline <= 10:
        errors.append("Укажите исходную оценку цели от 0 до 10.")

    if code != "ok_start":
        diary = payload.get("nutrition_diary")
        if not isinstance(diary, list) or len([day for day in diary if str(day).strip()]) < 3:
            errors.append("Для платного разбора нужен дневник питания за 3 дня.")

    return errors
