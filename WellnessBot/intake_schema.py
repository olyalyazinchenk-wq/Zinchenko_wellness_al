from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from nutriok_product import (
    PRIMARY_GOALS,
    normalize_product_code,
    validate_assessment_payload,
)


GOAL_DEFAULT_METRICS: dict[str, str] = {
    "energy": "энергия в 15:00, 0–10",
    "digestion": "вздутие после еды, 0–10",
    "weight_appetite": "тяга к сладкому, 0–10",
    "skin_hair": "состояние кожи, 0–10 / фото раз в неделю",
    "sleep_stress": "качество сна, 0–10",
}

GOAL_FIRST_SAFE_STEPS: dict[str, str] = {
    "energy": (
        "Завтра добавьте источник белка в первый приём пищи в течение 90 минут после подъёма "
        "и перенесите первую чашку кофе на время после еды. Отметьте уровень энергии в 15:00 по шкале 0–10."
    ),
    "digestion": (
        "В ближайшие 24 часа сделайте 3 спокойных приёма пищи без перекусов на бегу и добавьте стакан тёплой воды "
        "за 20 минут до еды. Отметьте комфорт после ужина по шкале 0–10."
    ),
    "weight_appetite": (
        "Начните обед и ужин с порции некрахмалистых овощей и белка, прежде чем переходить к гарниру. "
        "Вечером оцените тягу к сладкому по шкале 0–10."
    ),
    "skin_hair": (
        "Включите в каждый основной приём пищи источник белка и полезные жиры (рыба, яйца, оливковое масло, орехи) "
        "и уберите сладкие напитки на 3 дня. Зафиксируйте исходное состояние кожи 0–10."
    ),
    "sleep_stress": (
        "Завершите последний плотный приём пищи за 3 часа до сна и уберите кофеин после 14:00. "
        "Утром оцените качество сна и бодрость по шкале 0–10."
    ),
}


@dataclass
class DiaryDay:
    day_index: int                    # 1..3
    meals_text: str                   # свободный текст / транскрипт голоса
    photo_file_ids: list[str] = field(default_factory=list)
    water_ml: int | None = None
    wellbeing_0_10: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any] | str, default_index: int = 1) -> "DiaryDay":
        if isinstance(d, str):
            return cls(day_index=default_index, meals_text=d.strip())
        if not isinstance(d, dict):
            return cls(day_index=default_index, meals_text="")
        water_raw = d.get("water_ml")
        wellbeing_raw = d.get("wellbeing_0_10")
        return cls(
            day_index=int(d.get("day_index") or default_index),
            meals_text=str(d.get("meals_text") or "").strip(),
            photo_file_ids=[str(x) for x in (d.get("photo_file_ids") or []) if str(x).strip()],
            water_ml=int(water_raw) if water_raw is not None and not isinstance(water_raw, bool) else None,
            wellbeing_0_10=(
                int(wellbeing_raw)
                if wellbeing_raw is not None and not isinstance(wellbeing_raw, bool)
                else None
            ),
        )


@dataclass
class AdherenceEntry:
    week: int
    adherence_pct: int
    metric_value: float
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "AdherenceEntry":
        return cls(
            week=int(d.get("week") or 1),
            adherence_pct=int(d.get("adherence_pct") or 0),
            metric_value=float(d.get("metric_value") or 0.0),
            note=str(d.get("note") or "").strip(),
        )


@dataclass
class NutriOKIntake:
    schema_version: int = 1
    product_code: str = "ok_start"
    primary_goal: str | None = None            # ключ из PRIMARY_GOALS
    baseline_score: int | None = None          # 0..10
    goal_metric: str | None = None
    nutrition_diary: list[DiaryDay] = field(default_factory=list)
    symptoms: str = ""
    medications: str = ""
    allergies: str = ""
    lifestyle: str = ""
    labs_upload_ids: list[str] = field(default_factory=list)
    adherence: list[AdherenceEntry] = field(default_factory=list)
    adult_confirmed: bool = False
    pd_consent_at: str | None = None           # ISO, обязателен до сбора данных

    def __post_init__(self) -> None:
        self.product_code = normalize_product_code(self.product_code)
        if self.primary_goal in GOAL_DEFAULT_METRICS and self.goal_metric is None:
            self.goal_metric = GOAL_DEFAULT_METRICS[self.primary_goal]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": int(self.schema_version),
            "product_code": normalize_product_code(self.product_code),
            "primary_goal": self.primary_goal,
            "baseline_score": self.baseline_score,
            "goal_metric": self.goal_metric,
            "nutrition_diary": [day.to_dict() for day in self.nutrition_diary],
            "symptoms": str(self.symptoms or ""),
            "medications": str(self.medications or ""),
            "allergies": str(self.allergies or ""),
            "lifestyle": str(self.lifestyle or ""),
            "labs_upload_ids": list(self.labs_upload_ids),
            "adherence": [entry.to_dict() for entry in self.adherence],
            "adult_confirmed": bool(self.adult_confirmed),
            "pd_consent_at": self.pd_consent_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> "NutriOKIntake":
        if not isinstance(d, dict):
            return cls()
        raw_diary = d.get("nutrition_diary") or []
        diary_days: list[DiaryDay] = []
        if isinstance(raw_diary, list):
            for idx, item in enumerate(raw_diary, start=1):
                if isinstance(item, DiaryDay):
                    diary_days.append(item)
                else:
                    diary_days.append(DiaryDay.from_dict(item, default_index=idx))

        raw_adherence = d.get("adherence") or []
        adherence_entries: list[AdherenceEntry] = []
        if isinstance(raw_adherence, list):
            for item in raw_adherence:
                if isinstance(item, AdherenceEntry):
                    adherence_entries.append(item)
                elif isinstance(item, dict):
                    adherence_entries.append(AdherenceEntry.from_dict(item))

        baseline_raw = d.get("baseline_score")
        baseline_score: int | None = None
        if baseline_raw is not None and not isinstance(baseline_raw, bool):
            try:
                baseline_score = int(baseline_raw)
            except (TypeError, ValueError):
                baseline_score = None

        raw_code = str(d.get("product_code") or "ok_start").strip().lower()
        product_code = "ok_start" if raw_code in {"ok_start", "screening"} else normalize_product_code(raw_code)

        return cls(
            schema_version=int(d.get("schema_version") or 1),
            product_code=product_code,
            primary_goal=str(d["primary_goal"]) if d.get("primary_goal") else None,
            baseline_score=baseline_score,
            goal_metric=str(d["goal_metric"]).strip() if d.get("goal_metric") else None,
            nutrition_diary=diary_days,
            symptoms=str(d.get("symptoms") or "").strip(),
            medications=str(d.get("medications") or "").strip(),
            allergies=str(d.get("allergies") or "").strip(),
            lifestyle=str(d.get("lifestyle") or "").strip(),
            labs_upload_ids=[str(x) for x in (d.get("labs_upload_ids") or []) if str(x).strip()],
            adherence=adherence_entries,
            adult_confirmed=bool(d.get("adult_confirmed")),
            pd_consent_at=str(d["pd_consent_at"]).strip() if d.get("pd_consent_at") else None,
        )

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        if not self.adult_confirmed:
            errors.append("Подтвердите, что вам исполнилось 18 лет (18+).")
        if not str(self.pd_consent_at or "").strip():
            errors.append("Необходимо согласие на обработку персональных данных (152-ФЗ).")

        payload = self.to_dict()
        errors.extend(validate_assessment_payload(payload, self.product_code))

        if normalize_product_code(self.product_code) != "ok_start":
            if not str(self.goal_metric or "").strip():
                errors.append("Выберите или укажите метрику отслеживания цели.")

        return errors
