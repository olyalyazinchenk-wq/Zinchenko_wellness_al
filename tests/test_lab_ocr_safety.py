from __future__ import annotations

import asyncio
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from lab_ocr import (  # noqa: E402
    assess_ocr_quality,
    build_biomarker_confirmation_message,
    build_lab_resubmission_message,
    extract_biomarkers_from_text,
    get_yandex_ocr_credentials,
    parse_manual_biomarkers,
    parse_biomarkers,
)


class LabOcrSafetyTests(unittest.TestCase):
    def test_assess_ocr_quality_flags_short_or_sparse_text(self) -> None:
        result = assess_ocr_quality("Ферритин 22")
        self.assertEqual(result["status"], "needs_resubmission")
        self.assertTrue(result["requires_resubmission"])

    def test_extract_biomarkers_from_clear_line_is_conservative(self) -> None:
        raw_text = (
            "Ферритин 22 нг/мл 15-150\n"
            "Витамин D 28 нг/мл 30-100\n"
            "Дата 12.04.2026\n"
        )
        biomarkers = extract_biomarkers_from_text(raw_text)
        self.assertEqual(len(biomarkers), 2)
        self.assertEqual(biomarkers[0]["name"], "Ферритин")
        self.assertEqual(biomarkers[0]["value"], "22")
        self.assertEqual(biomarkers[0]["reference_range"], "15-150")

    def test_extract_biomarkers_ignores_pdf_service_lines(self) -> None:
        raw_text = (
            "ЗИНЧЕНКО ОЛЬГА ВИКТОРОВНА (Жен., 09.04.1986, 38 лет)\n"
            "Заказ №: 74386-31515-00005202\n"
            "Зарегистрирован: 12.09.2024 08:36:02\n"
            "Метод и оборудование: Электрохемилюминесцентный иммуноанализ (Cobas 6000)\n"
            "Тироксин (Т4) свободный 11.20 пмоль/л 10.8-22.0\n"
            "Ферритин 31.60 нг/мл 15-150\n"
        )
        biomarkers = extract_biomarkers_from_text(raw_text)
        names = [item["name"] for item in biomarkers]
        self.assertEqual(len(biomarkers), 2)
        self.assertIn("Тироксин (Т4) свободный", names)
        self.assertIn("Ферритин", names)

    def test_parse_biomarkers_requests_resubmission_when_quality_is_low(self) -> None:
        settings = SimpleNamespace()
        result = asyncio.run(parse_biomarkers("ТТГ 2.1", settings))
        self.assertTrue(result["requires_resubmission"])
        self.assertEqual(result["biomarkers"], [])

    def test_parse_biomarkers_returns_structured_values_when_text_is_clear(self) -> None:
        settings = SimpleNamespace()
        raw_text = (
            "Ферритин 22 нг/мл 15-150\n"
            "ТТГ 1.8 мЕд/л 0.4-4.0\n"
            "Гемоглобин 126 г/л 120-150\n"
        )
        result = asyncio.run(parse_biomarkers(raw_text, settings))
        self.assertFalse(result["requires_resubmission"])
        self.assertEqual(result["quality_status"], "ok")
        self.assertEqual(len(result["biomarkers"]), 3)

    def test_parse_manual_biomarkers_accepts_short_client_typed_values(self) -> None:
        settings = SimpleNamespace()
        result = asyncio.run(parse_manual_biomarkers("Ферритин 18 нг/мл\nВитамин D 24 нг/мл", settings))
        self.assertFalse(result["requires_resubmission"])
        self.assertEqual(result["quality_status"], "manual_text_client_provided")
        self.assertEqual(len(result["biomarkers"]), 2)

    def test_resubmission_message_is_explicit(self) -> None:
        message = build_lab_resubmission_message()
        self.assertIn("не буду интерпретировать", message)
        self.assertIn("пришлите", message.lower())

    def test_confirmation_message_asks_client_to_verify_values(self) -> None:
        message = build_biomarker_confirmation_message(
            [
                {
                    "name": "Ферритин",
                    "value": "18",
                    "unit": "нг/мл",
                    "reference_range": "15-150",
                    "nutrition_optimal_range": "40-90 нг/мл",
                }
            ]
        )
        self.assertIn("проверьте", message.lower())
        self.assertIn("Ферритин 18 нг/мл", message)
        self.assertIn("да, верно", message.lower())
        self.assertIn("предварительно распознанными", message.lower())

    def test_yandex_ocr_uses_stt_credentials_when_llm_is_deepseek(self) -> None:
        settings = SimpleNamespace(
            llm_provider="openai_compatible",
            llm_api_key="deepseek-key",
            llm_project_id=None,
            llm_use_iam_token=False,
            stt_api_key="yandex-iam",
            stt_project_id="folder-id",
            stt_use_iam_token=True,
        )
        credentials = get_yandex_ocr_credentials(settings)
        self.assertEqual(credentials["api_key"], "yandex-iam")
        self.assertEqual(credentials["project_id"], "folder-id")
        self.assertTrue(credentials["use_iam_token"])

    def test_yandex_ocr_falls_back_to_yandex_llm_credentials(self) -> None:
        settings = SimpleNamespace(
            llm_provider="yandex_foundation",
            llm_api_key="yandex-llm-key",
            llm_project_id="folder-id",
            llm_use_iam_token=True,
            stt_api_key=None,
            stt_project_id=None,
            stt_use_iam_token=False,
        )
        credentials = get_yandex_ocr_credentials(settings)
        self.assertEqual(credentials["api_key"], "yandex-llm-key")
        self.assertEqual(credentials["project_id"], "folder-id")
        self.assertTrue(credentials["use_iam_token"])


if __name__ == "__main__":
    unittest.main()
