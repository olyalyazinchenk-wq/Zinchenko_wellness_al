import asyncio
import base64
import json
import logging
import re
from pathlib import Path
from typing import Any, Optional

import httpx
from pypdf import PdfReader
from nutrition_reference_ranges import enrich_biomarkers_with_nutrition_ranges

logger = logging.getLogger("wellness_bot.ocr")

MIN_OCR_TEXT_LENGTH = 80
MIN_NUMERIC_LINES = 2
LAB_HEADER_STOPWORDS = (
    "дата",
    "лаборат",
    "пациент",
    "исследован",
    "бланк",
    "номер",
    "пол",
    "возраст",
    "фамил",
    "имя",
    "отчество",
    "заказ",
    "зарегистрирован",
    "регистрация",
    "валидация",
    "образец",
    "место взятия",
    "взятие биоматериала",
    "отчет создан",
    "отчёт создан",
    "метод",
    "оборудование",
    "gmt",
    "страница",
)
KNOWN_MARKER_ALIASES = (
    # General blood count and iron metabolism.
    "ферритин",
    "железо",
    "сывороточное железо",
    "трансферрин",
    "нтж",
    "насыщение трансферрина",
    "ожсс",
    "общая железосвязывающая способность",
    "лжсс",
    "латентная железосвязывающая способность",
    "ретикулоцит",
    "гемоглобин",
    "hgb",
    "эритроцит",
    "rbc",
    "лейкоцит",
    "wbc",
    "тромбоцит",
    "plt",
    "гематокрит",
    "hct",
    "mcv",
    "mch",
    "mchc",
    "rdw",
    "соэ",
    "esr",
    "нейтрофил",
    "лимфоцит",
    "моноцит",
    "эозинофил",
    "базофил",
    # Vitamins and methylation-related markers.
    "витамин d",
    "25-oh",
    "25(oh)",
    "25 oh",
    "25-гидроксивитамин d",
    "кальциферол",
    "b12",
    "витамин b12",
    "цианокобаламин",
    "кобаламин",
    "фолат",
    "фолиевая",
    "витамин в9",
    "гомоцистеин",
    "hcy",
    "витамин а",
    "ретинол",
    "витамин е",
    "токоферол",
    "витамин к",
    "витамин с",
    "аскорбиновая кислота",
    "витамин в1",
    "тиамин",
    "витамин в2",
    "рибофлавин",
    "витамин в3",
    "ниацин",
    "витамин в5",
    "пантотеновая кислота",
    "витамин в6",
    "пиридоксин",
    "витамин в7",
    "биотин",
    # Thyroid panel.
    "ттг",
    "tsh",
    "тиреотроп",
    "тиреотропный гормон",
    "т4 свобод",
    "свободный тироксин",
    "тироксин",
    "т4",
    "т3 свобод",
    "свободный трийодтиронин",
    "трийодтиронин",
    "т3",
    "ат-тпо",
    "ат тпо",
    "антитела к тпо",
    "ат-тг",
    "ат тг",
    "антитела к тг",
    "тиреоглобулин",
    "реверсивный т3",
    "rt3",
    # Glucose and lipid metabolism.
    "глюкоза",
    "сахар",
    "инсулин",
    "hba1c",
    "гликирован",
    "гликированный гемоглобин",
    "с-пептид",
    "c-peptide",
    "фруктозамин",
    "homa-ir",
    "homa ir",
    "лептин",
    "адипонектин",
    "холестерин",
    "холестерол",
    "общий холестерин",
    "лпнп",
    "ldl",
    "лпвп",
    "hdl",
    "лпонп",
    "vldl",
    "триглицер",
    "триглицериды",
    "коэффициент атерогенности",
    "аполипопротеин а",
    "апоа",
    "аполипопротеин в",
    "апоб",
    "липопротеин а",
    # Liver, pancreas, kidney, electrolytes.
    "алт",
    "алат",
    "аланинаминотрансфераза",
    "аст",
    "асат",
    "аспартатаминотрансфераза",
    "билирубин",
    "билирубин общий",
    "билирубин прямой",
    "билирубин непрямой",
    "ггт",
    "гамма-глутамилтрансфераза",
    "щелочная фосфатаза",
    "щф",
    "лдг",
    "лактатдегидрогеназа",
    "общий белок",
    "альбумин",
    "глобулин",
    "амилаза",
    "липаза",
    "креатинин",
    "мочевина",
    "мочевая кислота",
    "скф",
    "скорость клубочковой фильтрации",
    "egfr",
    "цистатин",
    "калий",
    "натрий",
    "хлор",
    "кальций",
    "кальций общий",
    "кальций ионизированный",
    "магний",
    "фосфор",
    "неорганический фосфор",
    # Inflammation and selected hormones relevant for navigation.
    "срб",
    "c-реактив",
    "c-реактивный белок",
    "crp",
    "фибриноген",
    "кортизол",
    "актг",
    "дгэа",
    "дгэа-с",
    "dhea",
    "dhea-s",
    "эстрадиол",
    "пролактин",
    "прогестерон",
    "лг",
    "фсг",
    "тестостерон",
    "амг",
    "антимюллеров гормон",
    "сшг",
    "shbg",
    # Minerals commonly used in nutrition navigation.
    "цинк",
    "селен",
    "медь",
    "хром",
    "марганец",
    "йод",
)
REFERENCE_PATTERN = re.compile(
    r"([<>]?\s*\d+(?:[.,]\d+)?\s*[-–]\s*[<>]?\s*\d+(?:[.,]\d+)?|[<>]\s*\d+(?:[.,]\d+)?)"
)
VALUE_PATTERN = re.compile(r"(?<![A-Za-zА-Яа-яЁё\d])([<>]?\d+(?:[.,]\d+)?)(?![A-Za-zА-Яа-яЁё\d.,])")


def get_yandex_ocr_credentials(settings: Any) -> dict[str, Any]:
    """Return Yandex credentials for OCR without depending on the active LLM provider."""
    api_key = getattr(settings, "stt_api_key", None)
    project_id = getattr(settings, "stt_project_id", None)
    use_iam_token = bool(getattr(settings, "stt_use_iam_token", False))

    if not api_key and getattr(settings, "llm_provider", None) == "yandex_foundation":
        api_key = getattr(settings, "llm_api_key", None)
        project_id = project_id or getattr(settings, "llm_project_id", None)
        use_iam_token = bool(getattr(settings, "llm_use_iam_token", False))

    return {
        "api_key": api_key,
        "project_id": project_id,
        "use_iam_token": use_iam_token,
    }


def normalize_ocr_line(value: str) -> str:
    return " ".join(value.replace("\t", " ").split())


def assess_ocr_quality(raw_text: str) -> dict[str, Any]:
    lines = [normalize_ocr_line(line) for line in raw_text.splitlines() if normalize_ocr_line(line)]
    numeric_lines = [line for line in lines if re.search(r"\d", line)]
    strange_char_count = raw_text.count("�")

    issues: list[str] = []
    if len(raw_text.strip()) < MIN_OCR_TEXT_LENGTH and len(numeric_lines) < 3:
        issues.append("too_short")
    if len(numeric_lines) < MIN_NUMERIC_LINES:
        issues.append("too_few_numeric_lines")
    if strange_char_count:
        issues.append("replacement_chars_detected")

    status = "ok" if not issues else "needs_resubmission"
    return {
        "status": status,
        "requires_resubmission": status != "ok",
        "issues": issues,
        "line_count": len(lines),
        "numeric_line_count": len(numeric_lines),
    }


def build_lab_resubmission_message() -> str:
    return (
        "Я не буду интерпретировать этот файл автоматически, потому что часть показателей читается неуверенно.\n\n"
        "Пришлите данные любым удобным вариантом:\n"
        "1. отправить PDF из лаборатории,\n"
        "2. прислать фото лучше качества: без бликов, весь бланк в кадре, текст и цифры чёткие,\n"
        "3. написать показатели вручную прямо здесь.\n\n"
        "Если пишете вручную, лучше по одному показателю на строку:\n"
        "Ферритин 18 нг/мл\n"
        "Витамин D 24 нг/мл\n"
        "ТТГ 3,8 мЕд/л\n"
        "Глюкоза 5.1 ммоль/л\n\n"
        "Если единицы измерения есть в бланке, укажите их тоже — так разбор будет точнее."
    )


def build_manual_biomarker_rewrite_message() -> str:
    return (
        "Я вижу, что вы написали цифры, но не смог(ла) надежно разобрать, где название показателя, "
        "значение и единицы измерения. Чтобы не ошибиться, пришлите, пожалуйста, показатели в таком формате:\n\n"
        "Ферритин 18 нг/мл\n"
        "Витамин D 24 нг/мл\n"
        "ТТГ 3,8 мЕд/л\n"
        "Глюкоза 5.1 ммоль/л\n\n"
        "Можно без референсов лаборатории, но название + значение + единицы измерения очень желательны. "
        "Если удобнее, можно вместо этого отправить PDF из лаборатории."
    )


def build_manual_biomarker_input_message() -> str:
    return (
        "Можно ввести показатели вручную прямо здесь, без файла. Лучше писать по одному показателю на строку:\n\n"
        "Ферритин 18 нг/мл\n"
        "Витамин D 24 нг/мл\n"
        "ТТГ 3,8 мЕд/л\n"
        "Глюкоза 5.1 ммоль/л\n\n"
        "Если знаете дату анализа и единицы измерения — укажите их. Если единицы не уверены, лучше отправьте PDF из лаборатории."
    )


def format_biomarker_for_confirmation(item: dict[str, Any]) -> str:
    name = str(item.get("name") or "").strip()
    value = str(item.get("value") or "").strip()
    unit = str(item.get("unit") or "").strip()
    reference = str(item.get("reference_range") or "").strip()
    optimal = str(item.get("nutrition_optimal_range") or "").strip()
    parts = [name, value, unit]
    line = " ".join(part for part in parts if part)
    if reference:
        line += f" | референс бланка: {reference}"
    if optimal:
        line += f" | нутрициологический ориентир: {optimal}"
    return line


def build_biomarker_confirmation_message(biomarkers: list[dict[str, Any]]) -> str:
    preview = "\n".join(
        f"{idx}. {format_biomarker_for_confirmation(item)}"
        for idx, item in enumerate(biomarkers[:12], start=1)
    )
    hidden_count = max(0, len(biomarkers) - 12)
    hidden_note = f"\n\nЕщё {hidden_count} показателей я сохраню в кейсе, но не показываю здесь, чтобы сообщение не было слишком длинным." if hidden_count else ""
    return (
        "Я распознал(а) показатели из файла. Пожалуйста, проверьте, всё ли верно:\n\n"
        f"{preview}"
        f"{hidden_note}\n\n"
        "Ответьте одним сообщением:\n"
        "• «да, верно» — если цифры, единицы и названия совпадают;\n"
        "• или напишите исправления, например: «Ферритин не 18, а 48 нг/мл».\n\n"
        "До вашего подтверждения я буду считать эти значения предварительно распознанными, а не окончательными."
    )


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract embedded text from lab PDFs before falling back to OCR."""
    try:
        reader = PdfReader(str(file_path))
        pages: list[str] = []
        for page in reader.pages[:12]:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text)
        return "\n".join(pages).strip()
    except Exception:
        logger.exception("PDF text extraction failed for %s", file_path.name)
        return ""


def should_skip_ocr_line(name_part: str) -> bool:
    normalized = normalize_ocr_line(name_part).lower().replace("ё", "е")
    if len(normalized) < 2:
        return True
    if not re.search(r"[A-Za-zА-Яа-яЁё]", normalized):
        return True
    if any(stopword in normalized for stopword in LAB_HEADER_STOPWORDS):
        return True
    if len(normalized) > 80:
        return True
    if not any(alias in normalized for alias in KNOWN_MARKER_ALIASES):
        return True
    return False


def extract_biomarkers_from_text(raw_text: str) -> list[dict[str, Any]]:
    biomarkers: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for raw_line in raw_text.splitlines():
        line = normalize_ocr_line(raw_line)
        if not line or not re.search(r"\d", line):
            continue

        value_matches = list(VALUE_PATTERN.finditer(line))
        if not value_matches:
            continue

        value_match = value_matches[0]
        candidate_name = line[:value_match.start()].strip(" :-")
        if should_skip_ocr_line(candidate_name) and len(value_matches) > 1:
            for candidate_match in value_matches[1:]:
                candidate_name = line[:candidate_match.start()].strip(" :-")
                if not should_skip_ocr_line(candidate_name):
                    value_match = candidate_match
                    break

        name_part = line[:value_match.start()].strip(" :-")
        if should_skip_ocr_line(name_part):
            continue

        value = value_match.group(1).replace(",", ".")
        tail = line[value_match.end():].strip()

        reference_match = REFERENCE_PATTERN.search(tail)
        if reference_match:
            reference_range = re.sub(r"\s+", "", reference_match.group(1))
            unit = tail[:reference_match.start()].strip(" ;,()")
        else:
            reference_range = None
            unit = tail.strip(" ;,()")

        if unit and not re.search(r"[A-Za-zА-Яа-яЁё%/µμ]", unit):
            unit = ""

        key = (name_part.lower(), value)
        if key in seen:
            continue
        seen.add(key)

        biomarker = {
            "name": name_part,
            "value": value,
            "unit": unit or None,
            "reference_range": reference_range,
            "source_line": line,
        }
        biomarkers.append(biomarker)

    return biomarkers


async def recognize_text(file_path: Path, settings: Any) -> Optional[str]:
    """Recognizes text using Yandex Vision OCR (Table Model)."""
    if file_path.suffix.lower() == ".pdf":
        embedded_text = extract_text_from_pdf(file_path)
        if embedded_text:
            return embedded_text

    credentials = get_yandex_ocr_credentials(settings)
    if not credentials["api_key"] or not credentials["project_id"]:
        logger.warning("Yandex OCR credentials are missing. OCR is skipped for %s.", file_path.name)
        return None

    try:
        with open(file_path, "rb") as f:
            file_content = base64.b64encode(f.read()).decode("utf-8")

        mime_type = "application/pdf" if file_path.suffix.lower() == ".pdf" else "image/jpeg"
        if file_path.suffix.lower() == ".png":
            mime_type = "image/png"

        url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
        auth_scheme = "Bearer" if credentials["use_iam_token"] else "Api-Key"
        headers = {
            "Authorization": f"{auth_scheme} {credentials['api_key']}",
            "x-folder-id": credentials["project_id"],
            "Content-Type": "application/json",
        }

        body = {
            "mimeType": mime_type,
            "languageCodes": ["ru", "en"],
            "model": "table",
            "content": file_content,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body, timeout=60.0)
            response.raise_for_status()
            data = response.json()

            text_result = ""
            for result in data.get("results", []):
                for text_annotation in result.get("textAnnotation", {}).get("blocks", []):
                    for line in text_annotation.get("lines", []):
                        text_result += line.get("text", "") + "\n"

            return text_result.strip()

    except Exception:
        logger.exception("Yandex OCR failed for %s", file_path.name)
        return None


async def parse_biomarkers(raw_text: str, settings: Any) -> dict[str, Any]:
    """Conservatively parse only clearly readable biomarker lines from OCR text."""
    del settings  # Reserved for future provider-aware parsing.

    if not raw_text:
        return {
            "biomarkers": [],
            "quality_status": "missing",
            "requires_resubmission": True,
            "issues": ["empty_ocr_text"],
        }

    quality = assess_ocr_quality(raw_text)
    if quality["requires_resubmission"]:
        return {
            "biomarkers": [],
            "quality_status": quality["status"],
            "requires_resubmission": True,
            "issues": quality["issues"],
        }

    biomarkers = enrich_biomarkers_with_nutrition_ranges(extract_biomarkers_from_text(raw_text))
    if not biomarkers:
        return {
            "biomarkers": [],
            "quality_status": "needs_resubmission",
            "requires_resubmission": True,
            "issues": ["no_clear_biomarker_lines"],
        }

    return {
        "biomarkers": biomarkers,
        "quality_status": "ok",
        "requires_resubmission": False,
        "issues": [],
    }


async def parse_manual_biomarkers(raw_text: str, settings: Any) -> dict[str, Any]:
    """Parse client-typed lab values without requiring a full lab-form OCR structure."""
    del settings
    biomarkers = enrich_biomarkers_with_nutrition_ranges(extract_biomarkers_from_text(raw_text or ""))
    if not biomarkers:
        return {
            "biomarkers": [],
            "quality_status": "manual_text_no_clear_biomarkers",
            "requires_resubmission": False,
            "issues": ["no_clear_biomarker_lines_in_manual_text"],
        }
    return {
        "biomarkers": biomarkers,
        "quality_status": "manual_text_client_provided",
        "requires_resubmission": False,
        "issues": [],
    }


async def analyze_physical_markers(file_path: Path, settings: Any) -> dict[str, Any]:
    """Uses Vision AI to analyze photos of tongue/eyes for clinical signs."""
    if not settings.llm_api_key:
        return {"analysis": "Vision AI disabled"}

    try:
        with open(file_path, "rb") as f:
            file_content = base64.b64encode(f.read()).decode("utf-8")

        prompt = """
        Ты — AI-ассистент нутрициологической навигации. Твоя задача — аккуратно описать фото
        языка или конъюнктивы глаза как предварительные визуальные маркеры без постановки диагноза.
        Найди визуальные признаки (налет, трещины, цвет, отечность), если они заметны.
        Верни СТРОГО JSON.

        Формат:
        {
          "type": "tongue/eye",
          "findings": ["Признак 1", "Признак 2"],
          "interpretation": "Что это может значить как осторожная гипотеза на языке нутрициолога (кратко)",
          "status": "vulnerable/normal"
        }
        """

        from ai_drafting import generate_live_reply

        response = await asyncio.to_thread(
            generate_live_reply,
            settings,
            [],
            prompt + f"\n[IMAGE_DATA_ATTACHED: {file_path.name}]",
        )

        clean_json = re.sub(r"^```(?:json)?\s*", "", response.strip(), flags=re.IGNORECASE)
        clean_json = re.sub(r"\s*```$", "", clean_json)
        return json.loads(clean_json)
    except Exception:
        logger.exception("Vision AI physical analysis failed")
        return {"findings": [], "interpretation": "Не удалось проанализировать автоматически"}
