from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from nutrition_reference_ranges import (
    NUTRITION_REFERENCE_CATALOG,
    match_nutrition_reference_entry,
    parse_numeric_value,
)
from supplement_product_catalog import build_supplement_context


MEDICAL_SKILL_DB_VERSION = "2026-04-25-v1"


@dataclass(frozen=True, slots=True)
class MarkerSkill:
    key: str
    display_name: str
    aliases: tuple[str, ...]
    system: str
    meaning: str
    low_signal: str | None
    high_signal: str | None
    clarify: tuple[str, ...]
    doctor_route: tuple[str, ...]
    self_action_boundary: str
    premium_action: str


MARKER_SKILLS: dict[str, MarkerSkill] = {
    "ferritin": MarkerSkill(
        key="ferritin",
        display_name="Ферритин",
        aliases=("ферритин",),
        system="железо / кровопотери / воспаление",
        meaning="Показывает запас железа; оценивается вместе с ОАК, железным профилем, симптомами и источником возможных потерь.",
        low_signal="Может поддерживать гипотезу железодефицитного риска, особенно при усталости, выпадении волос, зябкости, сердцебиении или обильном цикле.",
        high_signal="Может требовать исключения воспаления, перегрузки железом или других причин; не интерпретируется изолированно.",
        clarify=("ОАК с формулой", "сывороточное железо", "ОЖСС/трансферрин", "сатурация трансферрина", "СРБ", "характер менструальной кровопотери"),
        doctor_route=("терапевт", "гинеколог при обильном цикле", "гематолог по показаниям"),
        self_action_boundary="Не начинать железо самостоятельно без врача, причины потерь и оценки переносимости.",
        premium_action="Собрать дневник кровопотери 1-2 цикла и список симптомов, затем обсудить с врачом тактику коррекции.",
    ),
    "vitamin_d": MarkerSkill(
        key="vitamin_d",
        display_name="Витамин D",
        aliases=("витамин d", "25-oh", "25(oh)", "25-гидроксивитамин d"),
        system="витамин D / иммунная и костно-мышечная поддержка",
        meaning="Оценивается по 25(OH)D вместе с фоном, питанием, сезонностью, весом, ЖКТ и принимаемыми препаратами.",
        low_signal="Может быть одним из факторов усталости, мышечной слабости и снижения восстановления, но не объясняет картину целиком.",
        high_signal="Избыточные значения требуют осторожности и оценки кальция/почек; дозировки не подбираются ботом.",
        clarify=("25(OH)D в нг/мл", "кальций общий/ионизированный по показаниям", "креатинин", "лекарства и добавки"),
        doctor_route=("терапевт", "эндокринолог по показаниям"),
        self_action_boundary="Не давать лечебные дозировки без врача; учитывать кальций, почки, беременность/ГВ и лекарства.",
        premium_action="Обсудить с врачом безопасную коррекцию и контрольную точку, затем разнести приём добавок по совместимости.",
    ),
    "tsh": MarkerSkill(
        key="tsh",
        display_name="ТТГ",
        aliases=("ттг", "tsh", "тиреотроп"),
        system="щитовидная железа",
        meaning="Оценивается вместе со свободным Т4/Т3, антителами, УЗИ, симптомами и правилами приёма L-тироксина.",
        low_signal="Может требовать исключения избыточной тиреоидной стимуляции или влияния терапии; важен пульс и самочувствие.",
        high_signal="Может поддерживать гипотезу неполной компенсации щитовидного фона, особенно при зябкости, усталости, выпадении волос.",
        clarify=("свободный Т4", "свободный Т3 по показаниям", "АТ-ТПО/АТ-ТГ", "УЗИ щитовидной железы", "время приёма L-тироксина", "интервал с кофе/едой/железом/кальцием/магнием"),
        doctor_route=("эндокринолог",),
        self_action_boundary="Не менять дозу L-тироксина и не начинать йод/селен самостоятельно.",
        premium_action="Проверить правила приёма L-тироксина и подготовить эндокринологу вопрос по динамике ТТГ/св.Т4/симптомов.",
    ),
    "b12": MarkerSkill(
        key="b12",
        display_name="Витамин B12",
        aliases=("витамин b12", "b12", "кобаламин"),
        system="B12 / нервная система / кроветворение",
        meaning="Оценивается вместе с ОАК, фолатом, питанием, ЖКТ, метформином/ИПП и неврологическими симптомами.",
        low_signal="Может быть связан с усталостью, онемением, снижением концентрации или изменениями ОАК.",
        high_signal="Высокие значения без добавок требуют врачебной оценки контекста.",
        clarify=("ОАК", "фолат", "гомоцистеин по показаниям", "питание", "ЖКТ", "приём ИПП/метформина"),
        doctor_route=("терапевт", "гастроэнтеролог или невролог по симптомам"),
        self_action_boundary="Не объяснять неврологические симптомы только B12; при онемении/слабости нужна очная оценка.",
        premium_action="Собрать симптомы нервной системы и ЖКТ, затем уточнить связку B12-фолат-ОАК.",
    ),
    "fasting_glucose": MarkerSkill(
        key="fasting_glucose",
        display_name="Глюкоза натощак",
        aliases=("глюкоза", "glucose"),
        system="углеводный обмен",
        meaning="Оценивается вместе с HbA1c, инсулином, питанием, сном, стрессом и окружностью талии.",
        low_signal="Низкие значения требуют сопоставления с симптомами слабости, потливости, тремора и режимом питания.",
        high_signal="Может указывать на риск нарушения углеводного обмена; требует подтверждения и врачебной оценки.",
        clarify=("HbA1c", "инсулин натощак по показаниям", "питание за 3 дня", "сон", "стресс", "лекарства"),
        doctor_route=("терапевт", "эндокринолог по показаниям"),
        self_action_boundary="Не назначать сахароснижающие меры; питание корректировать мягко и безопасно.",
        premium_action="Сделать 3-дневный дневник еды/сна/тяги к сладкому и обсудить метаболический маршрут.",
    ),
    "hba1c": MarkerSkill(
        key="hba1c",
        display_name="Гликированный гемоглобин",
        aliases=("гликированный гемоглобин", "hba1c", "гликирован"),
        system="углеводный обмен за 2-3 месяца",
        meaning="Помогает оценивать средний гликемический фон; интерпретируется с глюкозой и ОАК.",
        low_signal="Низкие значения могут искажаться при особенностях крови; важно смотреть ОАК и контекст.",
        high_signal="Может требовать врачебной оценки риска нарушения углеводного обмена.",
        clarify=("глюкоза натощак", "ОАК", "инсулин по показаниям", "питание", "сон", "нагрузка"),
        doctor_route=("терапевт", "эндокринолог по показаниям"),
        self_action_boundary="Не ставить диагноз диабета по одному показателю в боте.",
        premium_action="Собрать питание/сон/нагрузку и подготовить врачу метаболические вопросы.",
    ),
}


SYMPTOM_ROUTES: tuple[dict[str, Any], ...] = (
    {
        "key": "heavy_bleeding",
        "markers": ("обильн", "кровотеч", "сгуст", "протек", "эндометри", "болезненные менструации"),
        "signal": "Возможный маршрут кровопотерь/гинекологического фона.",
        "questions": (
            "Сколько прокладок/тампонов уходит в самые обильные дни?",
            "Есть ли ночные протекания, сгустки, слабость, головокружение?",
            "Есть ли УЗИ, диагноз эндометриоза, миомы, полипы или сильная боль?",
        ),
        "doctor_route": ("гинеколог", "терапевт/гематолог при низком ферритине или анемическом паттерне"),
    },
    {
        "key": "tachycardia",
        "markers": ("сердц", "тахик", "пульс", "одыш", "боль в груди"),
        "signal": "Сердцебиение нельзя списывать только на дефициты или стресс.",
        "questions": (
            "Какой пульс в покое и при нагрузке?",
            "Есть ли боль в груди, одышка, предобморок, скачки давления?",
            "Есть ли ЭКГ/Холтер/контроль давления?",
        ),
        "doctor_route": ("терапевт", "кардиолог"),
    },
    {
        "key": "gi_complaints",
        "markers": ("вздут", "стул", "диар", "запор", "изжог", "тошнот", "живот"),
        "signal": "ЖКТ-жалобы важны для переносимости питания и добавок.",
        "questions": (
            "После каких продуктов усиливается симптом?",
            "Есть ли боль, кровь, снижение веса, температура?",
            "Какой стул по частоте и консистенции?",
        ),
        "doctor_route": ("гастроэнтеролог", "терапевт при красных флагах"),
    },
    {
        "key": "skin_photo",
        "markers": ("пятно", "сып", "кожа", "родин", "зуд", "кровоточ", "растет", "меняется"),
        "signal": "Фото помогает описать видимые признаки, но не заменяет очный осмотр.",
        "questions": (
            "Где находится, как давно, меняется ли размер/цвет/форма?",
            "Есть ли боль, зуд, кровоточивость, температура?",
            "Есть ли травма, новый препарат, косметика или контакт с аллергеном?",
        ),
        "doctor_route": ("дерматолог", "терапевт/неотложная помощь при быстром ухудшении"),
    },
)

NUTRITION_PROTOCOL_ROUTES: tuple[dict[str, Any], ...] = (
    {
        "key": "bile_flow_support",
        "name": "Желчеотток и переваривание жиров",
        "markers": (
            "горечь",
            "желч",
            "правом подреберье",
            "справа под реб",
            "после жир",
            "жирный стул",
            "светлый стул",
            "запор",
            "тошнот",
            "вздут",
            "отрыж",
        ),
        "hypothesis": "Возможна нутрициологическая гипотеза нарушения желчеоттока/переваривания жиров, особенно если симптомы усиливаются после жирной пищи.",
        "clarify": (
            "Есть ли УЗИ брюшной полости/желчного пузыря и были ли камни/сладж/перегиб?",
            "Есть ли боль справа, температура, желтушность кожи/склер, потемнение мочи или светлый стул?",
            "Как переносится жирная пища, яйца, молочные продукты, кофе?",
            "Какие АЛТ, АСТ, ГГТ, ЩФ, билирубин, амилаза/липаза, если анализы есть?",
        ),
        "safe_support": (
            "Дробность и регулярность питания без жёсткого голодания, если это подходит клиенту.",
            "Мягко оценить переносимость жиров, не уходить в обезжиренное питание без причины.",
            "Наладить стул: вода, клетчатка из еды, режим, движение.",
            "Уточнить УЗИ/биохимию до любых желчегонных средств.",
        ),
        "stop_rules": (
            "Не рекомендовать желчегонные средства при камнях, острой боли, температуре, желтушности, беременности/ГВ или неизвестном УЗИ.",
            "Не обещать лечение желчного пузыря и не назначать урсодезоксихолевую кислоту.",
        ),
        "doctor_route": ("гастроэнтеролог", "терапевт при боли/температуре/желтушности"),
    },
    {
        "key": "parasite_hypothesis_route",
        "name": "Паразитарная гипотеза и подготовка к проверке",
        "markers": (
            "паразит",
            "глист",
            "эозиноф",
            "зуд",
            "скрежет",
            "аллерг",
            "сып",
            "нестабильный стул",
            "поездк",
            "животн",
            "тяга к слад",
        ),
        "hypothesis": "Можно рассмотреть паразитарную гипотезу только как одну из версий, если есть симптомы, эозинофилия, контакты/поездки или ЖКТ-картина.",
        "clarify": (
            "Есть ли эозинофилы в ОАК, общий IgE, кожный зуд/сыпь, боли в животе, нестабильный стул?",
            "Были ли поездки, контакт с животными, сырая рыба/мясо, вода из сомнительных источников?",
            "Есть ли температура, похудение, кровь в стуле или выраженная боль?",
            "Какие анализы уже сдавались и каким методом?",
        ),
        "safe_support": (
            "Не начинать антипаразитарные препараты или интенсивные травяные схемы без подтверждения.",
            "Сначала собрать симптомы, ОАК с эозинофилами и обсудить с врачом релевантные исследования.",
            "Поддерживать регулярный стул, питание и восстановление слизистых без агрессивных чисток.",
        ),
        "stop_rules": (
            "Не назначать полынь, пижму, гвоздику, чёрный орех, медикаменты или сорбенты как антипаразитарный курс.",
            "Беременность/ГВ, дети/подростки, онкология, болезни печени/почек, лекарства и выраженные симптомы требуют врача.",
        ),
        "doctor_route": ("терапевт", "гастроэнтеролог", "инфекционист по показаниям"),
    },
    {
        "key": "detox_support_route",
        "name": "Детокс-поддержка без агрессивных чисток",
        "markers": (
            "детокс",
            "токс",
            "головные боли",
            "запах",
            "хими",
            "кожа",
            "сып",
            "запор",
            "отек",
            "усталость",
            "потлив",
        ),
        "hypothesis": "Детокс-поддержка в нутрициологии означает поддержку естественных путей выведения, а не обещание очищения организма.",
        "clarify": (
            "Есть ли запоры, мало воды/клетчатки, плохой сон, низкий белок в питании?",
            "Есть ли контакт с химией, растворителями, пластиком, дымом, вредными условиями?",
            "Какие лекарства/БАДы уже принимаются, есть ли болезни печени/почек/желчного?",
            "Есть ли анализы печени: АЛТ, АСТ, ГГТ, ЩФ, билирубин?",
        ),
        "safe_support": (
            "Регулярный стул, вода, клетчатка из еды, достаточный белок, сон и мягкое движение.",
            "Снижение бытовой токсической нагрузки: запахи, пластик, алкоголь, перегрев, бессистемные добавки.",
            "Антиоксидантную поддержку рассматривать только после оценки фона и совместимости.",
        ),
        "stop_rules": (
            "Не рекомендовать голодание, жёсткие чистки, бесконтрольные сорбенты, интенсивные сауны и высокие дозы антиоксидантов.",
            "При болезнях печени/почек/желчного, беременности/ГВ, онкологии и лекарствах требуется врачебная осторожность.",
        ),
        "doctor_route": ("терапевт", "гастроэнтеролог при печёночных/желчных маркерах"),
    },
    {
        "key": "deficiency_restoration_route",
        "name": "Восстановление дефицитных рисков",
        "markers": (
            "дефицит",
            "ферритин",
            "витамин d",
            "b12",
            "фолат",
            "магний",
            "цинк",
            "желез",
            "устал",
            "волос",
            "ногт",
            "сонлив",
        ),
        "hypothesis": "Восстановление дефицитов строится по подтверждённым данным: симптомы + анализы + причины потерь/усвоения + безопасность.",
        "clarify": (
            "Какие показатели подтверждены: ОАК, ферритин, B12, фолат, витамин D, железный профиль, ТТГ/св.Т4, глюкоза/HbA1c?",
            "Есть ли кровопотери, ЖКТ-жалобы, ограничения питания, лекарства, беременность/ГВ?",
            "Что уже принимается, в какой форме, как переносится и есть ли динамика?",
        ),
        "safe_support": (
            "Сначала подтвердить дефицитный риск и причину, затем выбирать форму и совместимость.",
            "Разносить несовместимые нутрицевтики по времени и отслеживать переносимость.",
            "Планировать контрольную точку: самочувствие, симптомы и повторные анализы по показаниям.",
        ),
        "stop_rules": (
            "Не начинать железо, йод, селен, гормонально-активные комплексы и высокие дозы витамина D без подтверждённых данных и оценки риска.",
            "Не объяснять все жалобы одним дефицитом.",
        ),
        "doctor_route": ("терапевт", "эндокринолог", "гематолог/гастроэнтеролог по показаниям"),
    },
)


def normalize_text(value: str | None) -> str:
    return " ".join((value or "").lower().replace("ё", "е").split())


def match_marker_skill(name: str, unit: str | None = None) -> tuple[str | None, MarkerSkill | None]:
    marker_key, _entry = match_nutrition_reference_entry(name, unit)
    if marker_key and marker_key in MARKER_SKILLS:
        return marker_key, MARKER_SKILLS[marker_key]

    normalized = normalize_text(name)
    for key, skill in MARKER_SKILLS.items():
        if any(alias in normalized for alias in skill.aliases):
            return key, skill
    return None, None


def analyze_biomarker_with_skill(biomarker: dict[str, Any]) -> dict[str, Any]:
    name = str(biomarker.get("name") or "")
    unit = biomarker.get("unit")
    marker_key, skill = match_marker_skill(name, unit)
    if not skill:
        return {
            "name": name,
            "value": biomarker.get("value"),
            "unit": unit,
            "matched": False,
            "note": "Показатель сохранён, но для него пока нет отдельной экспертной карточки в базе навыков.",
        }

    value = parse_numeric_value(biomarker.get("value"))
    nutrition_entry = NUTRITION_REFERENCE_CATALOG.get(marker_key)
    status = biomarker.get("nutrition_status")
    if not status and value is not None and nutrition_entry:
        if value < nutrition_entry["optimal_min"]:
            status = "below_nutrition_range"
        elif value > nutrition_entry["optimal_max"]:
            status = "above_nutrition_range"
        else:
            status = "within_nutrition_range"

    signal = None
    if status == "below_nutrition_range":
        signal = skill.low_signal
    elif status == "above_nutrition_range":
        signal = skill.high_signal
    elif status == "within_nutrition_range":
        signal = "По нутрициологическому ориентиру показатель выглядит в целевом диапазоне; всё равно оценивается вместе с симптомами."

    return {
        "name": name,
        "value": biomarker.get("value"),
        "unit": unit,
        "matched": True,
        "marker_key": marker_key,
        "display_name": skill.display_name,
        "system": skill.system,
        "nutrition_status": status,
        "nutrition_optimal_range": biomarker.get("nutrition_optimal_range") or (nutrition_entry or {}).get("display_range"),
        "meaning": skill.meaning,
        "signal": signal,
        "clarify": list(skill.clarify),
        "doctor_route": list(skill.doctor_route),
        "self_action_boundary": skill.self_action_boundary,
        "premium_action": skill.premium_action,
    }


def analyze_symptom_routes(medical_context: dict[str, Any]) -> list[dict[str, Any]]:
    haystack = normalize_text(
        " ".join(str(medical_context.get(key) or "") for key in medical_context)
    )
    routes: list[dict[str, Any]] = []
    for route in SYMPTOM_ROUTES:
        if any(marker in haystack for marker in route["markers"]):
            routes.append(
                {
                    "key": route["key"],
                    "signal": route["signal"],
                    "questions": list(route["questions"]),
                    "doctor_route": list(route["doctor_route"]),
                }
            )
    return routes


def analyze_nutrition_protocol_routes(medical_context: dict[str, Any]) -> list[dict[str, Any]]:
    haystack = normalize_text(
        " ".join(str(medical_context.get(key) or "") for key in medical_context)
    )
    routes: list[dict[str, Any]] = []
    for route in NUTRITION_PROTOCOL_ROUTES:
        if any(marker in haystack for marker in route["markers"]):
            routes.append(
                {
                    "key": route["key"],
                    "name": route["name"],
                    "hypothesis": route["hypothesis"],
                    "clarify": list(route["clarify"]),
                    "safe_support": list(route["safe_support"]),
                    "stop_rules": list(route["stop_rules"]),
                    "doctor_route": list(route["doctor_route"]),
                }
            )
    return routes


def build_medical_skill_context(submission: dict[str, Any]) -> dict[str, Any]:
    biomarkers = submission.get("parsed_biomarkers") if isinstance(submission.get("parsed_biomarkers"), list) else []
    medical_context = submission.get("medical_context") if isinstance(submission.get("medical_context"), dict) else {}
    confirmation_status = submission.get("lab_confirmation_status")
    values_are_confirmed = confirmation_status in {None, "", "client_confirmed", "client_provided_text"}

    biomarker_analysis = [analyze_biomarker_with_skill(item) for item in biomarkers]
    matched = [item for item in biomarker_analysis if item.get("matched")]

    priority_actions: list[str] = []
    for item in matched[:6]:
        action = item.get("premium_action")
        if action and action not in priority_actions:
            priority_actions.append(action)

    boundaries = []
    for item in matched:
        boundary = item.get("self_action_boundary")
        if boundary and boundary not in boundaries:
            boundaries.append(boundary)

    context = {
        "version": MEDICAL_SKILL_DB_VERSION,
        "purpose": "Справочник для нутрициологической навигации: факты, гипотезы, уточняющие вопросы, врачебный маршрут. Не диагноз и не назначение лечения.",
        "lab_values_confirmed": values_are_confirmed,
        "lab_confirmation_status": confirmation_status,
        "biomarker_analysis": biomarker_analysis,
        "symptom_routes": analyze_symptom_routes(medical_context),
        "nutrition_protocol_routes": analyze_nutrition_protocol_routes(medical_context),
        "priority_actions": priority_actions[:6],
        "safety_boundaries": boundaries[:8],
        "global_rules": [
            "Не ставить диагноз по одному показателю.",
            "Не назначать лекарства, гормоны, железо, йод, селен и лечебные дозировки добавок.",
            "Если показатель неясен, единицы странные или данные противоречат жалобам, запросить уточнение.",
            "Использовать нутрициологические ориентиры как навигацию, а не как медицинское заключение.",
        ],
    }
    context["supplement_context"] = build_supplement_context(context, medical_context)
    return context


def export_medical_skill_database() -> dict[str, Any]:
    return {
        "version": MEDICAL_SKILL_DB_VERSION,
        "markers": {key: asdict(value) for key, value in MARKER_SKILLS.items()},
        "symptom_routes": list(SYMPTOM_ROUTES),
        "nutrition_protocol_routes": list(NUTRITION_PROTOCOL_ROUTES),
        "rules": [
            "Факты отделять от гипотез.",
            "Любое сомнение по анализу уточнять у клиента или выводить в ручную проверку.",
            "Врачебные диагнозы и лечение не формулировать.",
            "Давать практический маршрут: что проверить, к кому идти, что наблюдать дома, чего не делать самостоятельно.",
        ],
    }
