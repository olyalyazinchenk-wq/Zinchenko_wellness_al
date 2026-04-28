from __future__ import annotations

import json
import logging
import re
import httpx

from openai import OpenAI

from config import Settings
from medical_skill_database import build_medical_skill_context
from prompts import (
    DOSSIER_DRAFT_PROMPT,
    DOSSIER_GROWTH_ARCHITECT_PROMPT,
    DOSSIER_JUDGE_PROMPT,
    LIVE_CHAT_PROMPT,
    PREMIUM_PROMPT,
    REVIEW_REPLY_PROMPT,
    SOCIAL_PROMPT,
    SPORT_PROMPT,
)

TIER_PROMPTS = {
    "week": PREMIUM_PROMPT,
    "premium": PREMIUM_PROMPT,
    "vip": PREMIUM_PROMPT,
    "sport": SPORT_PROMPT,
    "social": SOCIAL_PROMPT,
}


def get_system_prompt_for_tier(tier: str | None) -> str:
    """Return the tier-specific system prompt, falling back to the generic dossier prompt."""
    if tier and tier in TIER_PROMPTS:
        return TIER_PROMPTS[tier] + "\n\n" + DOSSIER_DRAFT_PROMPT
    return DOSSIER_DRAFT_PROMPT

logger = logging.getLogger("wellness_bot.ai")
YANDEX_FOUNDATION_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
REFUSAL_MARKERS = (
    "я не могу обсуждать эту тему",
    "не могу обсуждать эту тему",
    "давайте поговорим о чём-нибудь ещё",
    "давайте поговорим о чем-нибудь еще",
    "я не могу помочь с этим",
    "не могу помочь с этим",
)
LATIN_LETTER_RE = re.compile(r"[A-Za-z]")
CYRILLIC_LETTER_RE = re.compile(r"[А-Яа-яЁё]")
EMERGENCY_MARKERS = (
    "боль в груди",
    "тяжело дышать",
    "кровь в мокроте",
    "не могу дышать",
    "теряю сознание",
    "потеря сознания",
    "сильное кровотечение",
)
CRISIS_MARKERS = (
    "не вижу смысла",
    "не справляюсь",
    "хочу умереть",
    "не хочу жить",
    "суиц",
)
LOGISTICS_MARKERS = (
    "продолжается здесь",
    "куда-то переходить",
    "куда то переходить",
    "останется здесь",
    "pdf",
    "фото результатов",
    "файл",
    "загруз",
    "прикреп",
    "отправить это в текущем чате",
)
HIGH_INTENT_MARKERS = (
    "хочу",
    "готов",
    "готова",
    "идти дальше",
    "хочу ясность",
    "наконец получить ясность",
)
INFORMATIVE_INTENT_MARKERS = (
    "как у вас устроен",
    "что я получу",
    "что получу",
    "на выходе",
    "premium wellness dossier",
    "в какой момент становится нужен",
    "зачем он мне",
)
POSITIVE_REVIEW_MARKERS = (
    "спасибо",
    "понят",
    "ясн",
    "полезн",
    "береж",
    "структур",
    "спокойн",
    "ценн",
    "понрав",
    "отклик",
)
NEGATIVE_REVIEW_MARKERS = (
    "не понрав",
    "разочар",
    "бесполез",
    "мало пользы",
    "слишком общ",
    "непонят",
    "хаос",
    "долго",
    "затянуто",
    "дорого",
    "ожидал",
    "ожидала",
    "грубо",
    "поверхност",
)
MIXED_REVIEW_MARKERS = (
    "но",
    "однако",
    "при этом",
    "местами",
    "место для доработки",
    "можно лучше",
)
MEDICAL_BOUNDARY_MARKERS = (
    "диагноз",
    "лечение",
    "назначили",
    "назначение",
    "терап",
    "вылеч",
)
CLARITY_MARKERS = ("ясн", "понят", "следующий шаг", "картина")
CARE_MARKERS = ("береж", "спокойн", "поддерж", "деликат")
STRUCTURE_MARKERS = ("структур", "собран", "по полочкам", "логик")
VALUE_MARKERS = ("полезн", "практич", "ценн", "ориентир")
CTA_HIGH_INTENT_TEXT = (
    "\n\nЕсли хотите запустить разбор прямо сейчас, напишите: «хочу разбор». "
    "Я сразу открою intake в этом чате."
)
CTA_INFORMATIVE_TEXT = (
    "\n\nЕсли хотите перейти от первой ясности к структурному Premium-разбору, "
    "напишите: «хочу разбор»."
)
CTA_DEFAULT_TEXT = (
    "\n\nЕсли решите идти глубже, напишите: «хочу разбор». "
    "Я запущу Premium Wellness Dossier в этом чате."
)


def normalize_text(value: str) -> str:
    return " ".join(value.lower().replace("ё", "е").split())


def contains_any(value: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in value for keyword in keywords)


def detect_review_mode(review_text: str, score: int | None = None) -> str:
    normalized = normalize_text(review_text)

    if score is not None:
        if score <= 4:
            return "critical"
        if score <= 7:
            return "mixed"
        return "positive"

    has_negative = contains_any(normalized, NEGATIVE_REVIEW_MARKERS)
    has_positive = contains_any(normalized, POSITIVE_REVIEW_MARKERS)
    has_mixed = contains_any(normalized, MIXED_REVIEW_MARKERS)

    if has_negative and (has_positive or has_mixed):
        return "mixed"
    if has_negative:
        return "critical"
    return "positive"


def detect_review_focus(review_text: str) -> str:
    normalized = normalize_text(review_text)

    if contains_any(normalized, CLARITY_MARKERS):
        return "ясность"
    if contains_any(normalized, CARE_MARKERS):
        return "бережность"
    if contains_any(normalized, STRUCTURE_MARKERS):
        return "структура"
    if contains_any(normalized, VALUE_MARKERS):
        return "практическая польза"
    return "суть разбора"


def build_review_boundary_clarification(review_text: str) -> str:
    normalized = normalize_text(review_text)
    if not contains_any(normalized, MEDICAL_BOUNDARY_MARKERS):
        return ""
    return (
        "\n\nИ отдельно аккуратно уточню: в этом формате мы не ставим диагнозы и не назначаем лечение. "
        "Задача разбора — помочь увидеть возможные риски и следующий шаг, а медицинские решения обсуждаются с врачом."
    )


def build_review_reply_fallback(review_text: str, score: int | None = None) -> str:
    mode = detect_review_mode(review_text, score=score)
    focus = detect_review_focus(review_text)
    clarification = build_review_boundary_clarification(review_text)

    if mode == "positive":
        return (
            "Спасибо за такой содержательный отзыв.\n\n"
            f"Для нас особенно ценно, что в разборе сработали {focus}, а не просто общий поток советов. "
            "Именно на это и опирается сервис: спокойно собрать картину, убрать хаос и помочь увидеть следующий шаг."
            f"{clarification}"
        )

    if mode == "mixed":
        return (
            "Спасибо за честный и внимательный отзыв.\n\n"
            f"Я забрала из него и то, что было полезно, и то, где по {focus} ощущалась недоработка. "
            "Для нас это важнее формальной похвалы, потому что продукт должен давать не красивое впечатление, а реальную ясность и пользу."
            f"{clarification}"
        )

    return (
        "Спасибо, что написали прямо.\n\n"
        "Такой отзыв не хочется отмахивать или сглаживать. Для нас он полезен именно потому, что показывает, "
        "где результат не совпал с ожиданием и где сервису нужно быть точнее, яснее и сильнее."
        f"{clarification}\n\n"
        "Если захотите, можно одним сообщением написать, что именно ощущалось слабее всего: анкета, логика разбора, "
        "рекомендации или формат выдачи. Это поможет доработать продукт по сути, а не по формальности."
    )


def looks_like_refusal(reply: str | None) -> bool:
    if not reply:
        return True
    normalized = normalize_text(reply)
    return contains_any(normalized, REFUSAL_MARKERS)


def select_premium_cta(user_text: str) -> str | None:
    normalized = normalize_text(user_text)
    if contains_any(normalized, EMERGENCY_MARKERS):
        return None
    if contains_any(normalized, CRISIS_MARKERS):
        return None
    if contains_any(normalized, LOGISTICS_MARKERS):
        return None
    if contains_any(normalized, HIGH_INTENT_MARKERS):
        return CTA_HIGH_INTENT_TEXT
    if contains_any(normalized, INFORMATIVE_INTENT_MARKERS):
        return CTA_INFORMATIVE_TEXT
    return CTA_DEFAULT_TEXT


def append_premium_cta(reply: str, user_text: str) -> str:
    cta_text = select_premium_cta(user_text)
    if not cta_text:
        return reply
    if "хочу разбор" in normalize_text(reply):
        return reply
    return f"{reply}{cta_text}"


def route_live_reply(user_text: str) -> str | None:
    normalized = normalize_text(user_text)

    if contains_any(
        normalized,
        EMERGENCY_MARKERS,
    ):
        return (
            "По описанию это похоже на ситуацию, где нужна срочная офлайн-помощь. "
            "Лучше прямо сейчас вызвать 103 или 112, а не продолжать разбор в чате.\n\n"
            "Если сможете, коротко напишите, вызвали ли помощь. Дальше я помогу структурировать всё остальное уже после стабилизации."
        )

    if contains_any(
        normalized,
        CRISIS_MARKERS,
    ):
        return (
            "Сейчас важнее не разбор, а живая поддержка рядом. Пожалуйста, сразу напишите близкому человеку или позвоните в 112, "
            "если есть риск причинить себе вред.\n\n"
            "Если можете, не оставайтесь одной и напишите мне одним сообщением: «я сейчас не одна» или «я позвонила»."
        )

    if contains_any(normalized, ("продолжается здесь", "куда-то переходить", "куда то переходить", "останется здесь")):
        return "Общение продолжается здесь, в этом Telegram-чате. Никуда переходить не нужно."

    if contains_any(normalized, ("можно начать без", "без анализ", "потом дослать", "дослать позже")):
        return (
            "Да, начать можно и без анализов. Сначала разберём симптомы, контекст и главные вопросы, а результаты можно дослать позже прямо сюда, в этот чат.\n\n"
            "Так мы не тормозим старт, но всё равно сохраняем возможность уточнить картину, когда появятся данные."
        )

    if contains_any(normalized, ("5 базовых анализ", "какие 5 базовых анализ", "анализов пока нет")):
        return (
            "Если анализов пока нет, я бы начала с пяти базовых точек, которые чаще всего быстро убирают хаос:\n\n"
            "1. ОАК.\n"
            "2. Ферритин.\n"
            "3. ТТГ.\n"
            "4. Витамин D.\n"
            "5. Глюкоза натощак или гликированный гемоглобин.\n\n"
            "Этого уже достаточно, чтобы понять, куда смотреть дальше без лишних трат и без длинного списка «на всё сразу»."
        )

    if contains_any(normalized, ("pdf", "фото результатов", "файл", "загруз", "прикреп", "отправить это в текущем чате")):
        return (
            "Да, можно отправлять всё прямо сюда, в текущий чат Telegram. Лучше всего так:\n\n"
            "1. Одним сообщением коротко написать, что вас беспокоит сильнее всего.\n"
            "2. Затем приложить PDF или фото анализов.\n"
            "3. Если анализов пока не хватает, можно начать без них и дослать позже.\n\n"
            "После этого я соберу первичную картину и покажу, где уже есть ясность, а что стоит уточнить."
        )

    if contains_any(normalized, ("где срочность", "как вы обычно это разделяете", "это экстренно")):
        return (
            "Мы делим это на две группы. Если есть признаки риска прямо сейчас, например сильная боль в груди, нарастающая одышка, кровь, потеря сознания, "
            "очень высокая температура несколько дней подряд, здесь нужен не чат, а срочная офлайн-помощь.\n\n"
            "Если угрозы прямо сейчас нет, тогда идём спокойно: собираем симптомы, понимаем, что здесь главное, и определяем следующий разумный шаг без паники."
        )

    if contains_any(normalized, ("как у вас устроен", "разбор у вас", "что я получу", "что получу", "на выходе", "список добавок", "именно так и работаете")):
        return (
            "Мы работаем не как поток общих советов, а как разбор кейса в одном Telegram-диалоге.\n\n"
            "Сначала собираем симптомы, цели и, если есть, анализы. Затем формируем понятную картину: что здесь похоже на главное, "
            "что вторично, какие вопросы реально важны и какой следующий шаг разумный.\n\n"
            "Когда нужен более глубокий и собранный результат, подключается Premium Wellness Dossier: это уже структурированный документ "
            "с логикой кейса, маркерами внимания и приоритетным планом следующего шага."
        )

    if contains_any(normalized, ("premium wellness dossier", "premium", "досье", "в какой момент становится нужен")):
        return (
            "Premium Wellness Dossier нужен в момент, когда после первой ясности уже хочется не просто поговорить, а собрать кейс в цельную рабочую картину.\n\n"
            "Он полезен, когда симптомов и данных уже достаточно, чтобы структурировать гипотезы, маркеры внимания, последовательность следующих шагов "
            "и материал для обсуждения с врачом или специалистом.\n\n"
            "То есть сначала Telegram помогает убрать хаос, а Dossier нужен там, где требуется уже собранный премиальный результат."
        )

    if contains_any(normalized, ("ферритин", "желез", "выпадают волосы", "волосы", "тяжело вставать")):
        return (
            "Ферритин на нижней границе или ниже неё действительно может складываться в одну картину с усталостью, выпадением волос "
            "и слабым восстановлением. Это ещё не диагноз, но такая связка уже заслуживает спокойного уточнения.\n\n"
            "Разумный следующий шаг: посмотреть ОАК, гемоглобин, ферритин в динамике и базово понять, нет ли параллельно факторов вроде ТТГ или B12.\n\n"
            "Если хотите, я могу сразу помочь собрать минимальный список анализов без лишнего."
        )

    if contains_any(normalized, ("ттг", "щитовид", "мерзну", "мёрзну", "сонлив", "набираю вес")):
        return (
            "Если на фоне ТТГ около верхней части референса есть зябкость, сонливость и набор веса, это не повод паниковать, "
            "но и не то, что стоит отмахнуть фразой «всё в норме».\n\n"
            "Спокойный следующий шаг: смотреть не один ТТГ в отрыве, а картину целиком — симптомы, свободные Т4/Т3, ферритин, витамин D и общую клинику.\n\n"
            "Можем разобрать это именно в таком формате: что уже похоже на рабочую гипотезу, а что ещё нужно уточнить."
        )

    if contains_any(normalized, ("витамин d", "витамин д", "разбит", "сплю по 9", "сплю 9")):
        return (
            "Витамин D на таком уровне может быть частью картины разбитости, но обычно не единственным объяснением. "
            "Поэтому лучше смотреть не только на один показатель, а на сочетание сна, энергии, ферритина, ТТГ и общего фона.\n\n"
            "Практичный ход: не метаться между добавками и жёсткими схемами, а сначала собрать короткую базу маркеров и понять, "
            "что здесь выглядит главным драйвером состояния."
        )

    if contains_any(normalized, ("вздут", "тяжесть", "живот", "запор", "антибиотик", "реакция на еду", "жкт")):
        return (
            "Такая история действительно может складываться в понятную функциональную картину: чувствительное ЖКТ, сбой после антибиотиков, "
            "перегрузка по рациону или сочетание нескольких факторов сразу.\n\n"
            "Первый аккуратный шаг обычно не в радикальной диете, а в том, чтобы на 7-10 дней спокойно убрать хаос: "
            "не экспериментировать со всем сразу, отметить ключевые триггеры и понять, что ухудшает состояние сильнее всего.\n\n"
            "Если хотите, я помогу разложить это в короткий первичный план без крайностей."
        )

    if contains_any(normalized, ("цикл", "кожа", "настроение", "горм", "пмс")):
        return (
            "Да, это вполне может складываться в одну картину, а не быть набором случайных жалоб. "
            "Цикл, энергия, кожа и настроение часто связаны между собой через общий гормональный и стрессовый контур.\n\n"
            "Здесь полезно не искать диагноз в одно сообщение, а сначала собрать паттерн: как давно это началось, "
            "что изменилось по циклу, есть ли усталость, выпадение волос, проблемы со сном или ЖКТ.\n\n"
            "Если хотите, начнём именно с такой структуры и быстро поймём, что проверять первым."
        )

    if contains_any(normalized, ("устал", "слабость", "туман", "тяга к сладкому", "нет сил")):
        return (
            "Когда несколько месяцев держатся усталость, туман в голове и нестабильная энергия, обычно полезнее не искать одну магическую причину, "
            "а быстро собрать базовую карту состояния.\n\n"
            "Обычно я бы начала с 5 опорных точек: ОАК, ферритин, ТТГ, витамин D и базовая глюкоза или гликированный гемоглобин. "
            "Этого уже достаточно, чтобы убрать большую часть хаоса и понять следующий шаг.\n\n"
            "Если анализов пока нет, можно начать и без них — сначала соберём паттерн симптомов."
        )

    return None


def build_live_fallback(user_text: str) -> str:
    routed_reply = route_live_reply(user_text)
    if routed_reply:
        return append_premium_cta(routed_reply, user_text)

    fallback = (
        "Здесь лучше идти не от случайных советов, а от короткого структурного разбора: что именно беспокоит, как давно это длится, "
        "что уже проверяли и где сейчас больше всего неопределённости.\n\n"
        "Опишите в 3-5 строках главные симптомы и, если есть, приложите анализы. После этого я помогу собрать первую ясную картину и следующий разумный шаг."
    )
    return append_premium_cta(fallback, user_text)


def looks_english_heavy(reply: str | None) -> bool:
    if not reply:
        return False
    latin_count = len(LATIN_LETTER_RE.findall(reply))
    cyrillic_count = len(CYRILLIC_LETTER_RE.findall(reply))
    return latin_count >= 40 and latin_count > cyrillic_count * 1.5


def finalize_live_reply(reply: str | None, user_text: str) -> str:
    if looks_like_refusal(reply):
        logger.warning("Model returned empty or refusal-style reply. Using local fallback.")
        return build_live_fallback(user_text)
    final_reply = reply or build_live_fallback(user_text)
    if looks_english_heavy(final_reply):
        logger.warning("Model returned English-heavy live reply. Using Russian fallback.")
        return build_live_fallback(user_text)
    return append_premium_cta(final_reply, user_text)


def build_review_reply_payload(review_text: str, score: int | None = None) -> str:
    return json.dumps(
        {
            "review_text": review_text,
            "score": score,
        },
        ensure_ascii=False,
        indent=2,
    )


def finalize_review_reply(reply: str | None, review_text: str, score: int | None = None) -> str:
    if looks_like_refusal(reply):
        logger.warning("Model returned empty or refusal-style review reply. Using local fallback.")
        return build_review_reply_fallback(review_text, score=score)
    if looks_english_heavy(reply):
        logger.warning("Model returned English-heavy review reply. Using Russian fallback.")
        return build_review_reply_fallback(review_text, score=score)
    return reply or build_review_reply_fallback(review_text, score=score)


def build_client(settings: Settings) -> OpenAI:
    client_kwargs: dict = {"api_key": settings.llm_api_key}

    if settings.llm_base_url:
        client_kwargs["base_url"] = settings.llm_base_url

    if settings.llm_project_id:
        client_kwargs["project"] = settings.llm_project_id

    if settings.llm_disable_server_logging:
        client_kwargs["default_headers"] = {"x-data-logging-enabled": "false"}

    return OpenAI(**client_kwargs)


def generate_case_draft_yandex_foundation(settings: Settings, submission: dict, tier: str | None = None) -> str | None:
    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    enriched_submission = dict(submission)
    enriched_submission["medical_skill_context"] = build_medical_skill_context(submission)

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": "2000",
        },
        "messages": [
            {"role": "system", "text": get_system_prompt_for_tier(tier).strip()},
            {"role": "user", "text": json.dumps(enriched_submission, ensure_ascii=False, indent=2)},
        ],
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None


def generate_live_reply_yandex_foundation(
    settings: Settings,
    history: list[dict[str, str]],
    user_text: str,
) -> str | None:
    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    messages: list[dict[str, str]] = [{"role": "system", "text": LIVE_CHAT_PROMPT.strip()}]
    for item in history[-10:]:
        role = item.get("role")
        text = (item.get("content") or "").strip()
        if role in {"user", "assistant"} and text:
            messages.append({"role": role, "text": text})
    messages.append({"role": "user", "text": user_text.strip()})

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": "1200",
        },
        "messages": messages,
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None


def extract_chat_completion_text(response) -> str | None:
    if not response.choices:
        return None

    message = response.choices[0].message
    content = getattr(message, "content", None)

    if isinstance(content, str):
        return content.strip() or None

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text_value = getattr(item, "text", None)
            if text_value:
                parts.append(text_value)
        merged = "\n".join(parts).strip()
        return merged or None

    return None


def generate_case_draft(settings: Settings, submission: dict, tier: str | None = None) -> str | None:
    if settings.llm_provider == "disabled":
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return None

    if settings.llm_provider == "yandex_foundation":
        return generate_case_draft_yandex_foundation(settings, submission, tier=tier)

    client = build_client(settings)
    enriched_submission = dict(submission)
    enriched_submission["medical_skill_context"] = build_medical_skill_context(submission)
    submission_payload = json.dumps(enriched_submission, ensure_ascii=False, indent=2)

    if settings.llm_api_mode == "chat_completions":
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": get_system_prompt_for_tier(tier)},
                {"role": "user", "content": submission_payload},
            ],
            temperature=0.2,
        )
        return extract_chat_completion_text(response)

    response = client.responses.create(
        model=settings.llm_model,
        instructions=get_system_prompt_for_tier(tier),
        input=submission_payload,
    )
    return (response.output_text or "").strip() or None



def build_judge_payload(submission: dict, draft_text: str) -> str:
    return json.dumps(
        {
            "submission": submission,
            "draft": draft_text,
        },
        ensure_ascii=False,
        indent=2,
    )



def generate_case_judge_report_yandex_foundation(
    settings: Settings,
    submission: dict,
    draft_text: str,
) -> str | None:
    if not draft_text:
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": "1500",
        },
        "messages": [
            {"role": "system", "text": DOSSIER_JUDGE_PROMPT.strip()},
            {"role": "user", "text": build_judge_payload(submission, draft_text)},
        ],
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None



def generate_case_judge_report(
    settings: Settings,
    submission: dict,
    draft_text: str,
) -> str | None:
    if not draft_text:
        return None

    if settings.llm_provider == "disabled":
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return None

    if settings.llm_provider == "yandex_foundation":
        return generate_case_judge_report_yandex_foundation(settings, submission, draft_text)

    client = build_client(settings)
    judge_input = build_judge_payload(submission, draft_text)

    if settings.llm_api_mode == "chat_completions":
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": DOSSIER_JUDGE_PROMPT},
                {"role": "user", "content": judge_input},
            ],
            temperature=0.1,
        )
        return extract_chat_completion_text(response)

    response = client.responses.create(
        model=settings.llm_model,
        instructions=DOSSIER_JUDGE_PROMPT,
        input=judge_input,
    )
    return (response.output_text or "").strip() or None


def build_growth_architect_payload(
    submission: dict,
    draft_text: str,
    judge_report_text: str | None,
    governance_context: dict | None = None,
) -> str:
    return json.dumps(
        {
            "submission": submission,
            "draft": draft_text,
            "judge_report": judge_report_text,
            "governance_context": governance_context or {},
        },
        ensure_ascii=False,
        indent=2,
    )


def generate_case_growth_report_yandex_foundation(
    settings: Settings,
    submission: dict,
    draft_text: str,
    judge_report_text: str | None = None,
    governance_context: dict | None = None,
) -> str | None:
    if not draft_text:
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": "1500",
        },
        "messages": [
            {"role": "system", "text": DOSSIER_GROWTH_ARCHITECT_PROMPT.strip()},
            {
                "role": "user",
                "text": build_growth_architect_payload(
                    submission,
                    draft_text,
                    judge_report_text,
                    governance_context=governance_context,
                ),
            },
        ],
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None


def generate_review_reply_yandex_foundation(
    settings: Settings,
    review_text: str,
    score: int | None = None,
) -> str | None:
    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("Yandex foundation provider is enabled but API key or model URI is missing.")
        return None

    auth_scheme = "Bearer" if settings.llm_use_iam_token else "Api-Key"
    headers = {
        "Authorization": f"{auth_scheme} {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    if settings.llm_project_id:
        headers["x-folder-id"] = settings.llm_project_id

    payload = {
        "modelUri": settings.llm_model,
        "completionOptions": {
            "stream": False,
            "temperature": 0.25,
            "maxTokens": "700",
        },
        "messages": [
            {"role": "system", "text": REVIEW_REPLY_PROMPT.strip()},
            {"role": "user", "text": build_review_reply_payload(review_text, score=score)},
        ],
    }

    response = httpx.post(
        settings.llm_base_url or YANDEX_FOUNDATION_URL,
        headers=headers,
        json=payload,
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    data = response.json()
    alternatives = data.get("result", {}).get("alternatives", [])
    if not alternatives:
        return None
    message = alternatives[0].get("message", {})
    text = message.get("text", "").strip()
    return text or None


def generate_case_growth_report(
    settings: Settings,
    submission: dict,
    draft_text: str,
    judge_report_text: str | None = None,
    governance_context: dict | None = None,
) -> str | None:
    if not draft_text:
        return None

    if settings.llm_provider == "disabled":
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return None

    if settings.llm_provider == "yandex_foundation":
        return generate_case_growth_report_yandex_foundation(
            settings,
            submission,
            draft_text,
            judge_report_text=judge_report_text,
            governance_context=governance_context,
        )

    client = build_client(settings)
    growth_input = build_growth_architect_payload(
        submission,
        draft_text,
        judge_report_text,
        governance_context=governance_context,
    )

    if settings.llm_api_mode == "chat_completions":
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": DOSSIER_GROWTH_ARCHITECT_PROMPT},
                {"role": "user", "content": growth_input},
            ],
            temperature=0.2,
        )
        return extract_chat_completion_text(response)

    response = client.responses.create(
        model=settings.llm_model,
        instructions=DOSSIER_GROWTH_ARCHITECT_PROMPT,
        input=growth_input,
    )
    return (response.output_text or "").strip() or None


def generate_live_reply(
    settings: Settings,
    history: list[dict[str, str]],
    user_text: str,
) -> str | None:
    if settings.llm_provider == "disabled":
        return None

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return None

    routed_reply = route_live_reply(user_text)
    if routed_reply:
        return append_premium_cta(routed_reply, user_text)

    if settings.llm_provider == "yandex_foundation":
        return generate_live_reply_yandex_foundation(settings, history, user_text)

    client = build_client(settings)
    if settings.llm_api_mode == "chat_completions":
        messages: list[dict[str, str]] = [{"role": "system", "content": LIVE_CHAT_PROMPT}]
        for item in history[-10:]:
            role = item.get("role")
            text = (item.get("content") or "").strip()
            if role in {"user", "assistant"} and text:
                messages.append({"role": role, "content": text})
        messages.append({"role": "user", "content": user_text.strip()})

        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            temperature=0.4,
        )
        return finalize_live_reply(extract_chat_completion_text(response), user_text)

    transcript = []
    for item in history[-10:]:
        role = item.get("role")
        text = (item.get("content") or "").strip()
        if role in {"user", "assistant"} and text:
            transcript.append(f"{role}: {text}")
    transcript.append(f"user: {user_text.strip()}")
    response = client.responses.create(
        model=settings.llm_model,
        instructions=LIVE_CHAT_PROMPT,
        input="\n".join(transcript),
    )
    return finalize_live_reply((response.output_text or "").strip() or None, user_text)


def generate_review_reply(
    settings: Settings,
    review_text: str,
    score: int | None = None,
) -> str:
    if settings.llm_provider == "disabled":
        return build_review_reply_fallback(review_text, score=score)

    if not settings.llm_api_key or not settings.llm_model:
        logger.warning("LLM provider is enabled but API key or model is missing.")
        return build_review_reply_fallback(review_text, score=score)

    if settings.llm_provider == "yandex_foundation":
        reply = generate_review_reply_yandex_foundation(settings, review_text, score=score)
        return finalize_review_reply(reply, review_text, score=score)

    client = build_client(settings)
    review_input = build_review_reply_payload(review_text, score=score)

    if settings.llm_api_mode == "chat_completions":
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": REVIEW_REPLY_PROMPT},
                {"role": "user", "content": review_input},
            ],
            temperature=0.25,
        )
        return finalize_review_reply(
            extract_chat_completion_text(response),
            review_text,
            score=score,
        )

    response = client.responses.create(
        model=settings.llm_model,
        instructions=REVIEW_REPLY_PROMPT,
        input=review_input,
    )
    return finalize_review_reply((response.output_text or "").strip() or None, review_text, score=score)
