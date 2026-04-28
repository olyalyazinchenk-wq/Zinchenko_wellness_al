from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from ai_drafting import (  # noqa: E402
    build_review_reply_fallback,
    detect_review_focus,
    detect_review_mode,
    generate_review_reply,
)


class ReviewReplyLogicTests(unittest.TestCase):
    def test_detect_review_mode_uses_score_when_available(self) -> None:
        self.assertEqual(detect_review_mode("Текст", score=9), "positive")
        self.assertEqual(detect_review_mode("Текст", score=6), "mixed")
        self.assertEqual(detect_review_mode("Текст", score=3), "critical")

    def test_detect_review_focus_prefers_clarity_markers(self) -> None:
        self.assertEqual(
            detect_review_focus("После разбора стало намного понятнее, появилась ясность."),
            "ясность",
        )

    def test_positive_review_reply_stays_warm_and_positioned(self) -> None:
        reply = build_review_reply_fallback(
            "Спасибо, после разбора стало намного понятнее, что делать дальше.",
            score=10,
        )

        self.assertIn("Спасибо за такой содержательный отзыв.", reply)
        self.assertIn("следующий шаг", reply)
        self.assertNotIn("вы абсолютно правы", reply.lower())

    def test_mixed_review_reply_accepts_useful_critique_without_self_humiliation(self) -> None:
        reply = build_review_reply_fallback(
            "Было полезно, но местами текст показался слишком общим и длинным.",
            score=6,
        )

        self.assertIn("Спасибо за честный и внимательный отзыв.", reply)
        self.assertIn("недоработка", reply)
        self.assertNotIn("мы полностью провалились", reply.lower())

    def test_critical_review_reply_adds_medical_boundary_clarification(self) -> None:
        reply = build_review_reply_fallback(
            "Мне не понравилось, как будто мне поставили диагноз и назначили лечение.",
            score=3,
        )

        self.assertIn("Спасибо, что написали прямо.", reply)
        self.assertIn("мы не ставим диагнозы и не назначаем лечение", reply)

    def test_generate_review_reply_returns_fallback_when_provider_disabled(self) -> None:
        settings = SimpleNamespace(
            llm_provider="disabled",
            llm_api_key=None,
            llm_model=None,
            llm_api_mode="responses",
            llm_base_url=None,
            llm_project_id=None,
            llm_disable_server_logging=False,
            llm_use_iam_token=False,
        )

        reply = generate_review_reply(
            settings,
            "Спасибо, стало спокойнее и понятнее.",
            score=9,
        )
        self.assertIn("Спасибо за такой содержательный отзыв.", reply)


if __name__ == "__main__":
    unittest.main()
