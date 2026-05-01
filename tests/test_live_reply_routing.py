from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from ai_drafting import route_live_reply  # noqa: E402


class LiveReplyRoutingTests(unittest.TestCase):
    def test_emergency_still_routes_to_safety_template(self) -> None:
        reply = route_live_reply("Сильная боль в груди и тяжело дышать уже 15 минут.")
        self.assertIsNotNone(reply)
        self.assertIn("103", reply or "")

    def test_upload_logistics_still_routes_to_instruction_template(self) -> None:
        reply = route_live_reply("У меня есть PDF с анализами. Как лучше отправить файл?")
        self.assertIsNotNone(reply)
        self.assertIn("текущий чат Telegram", reply or "")

    def test_symptom_and_lab_questions_reach_model_layer(self) -> None:
        symptom_prompts = [
            "Ферритин 14, выпадают волосы и тяжело вставать по утрам. Что проверить дальше?",
            "ТТГ 3.7, мёрзну, набираю вес и сонливость. Как на это смотреть?",
            "После антибиотиков нестабильный живот, вздутие и реакция на еду.",
            "Несколько месяцев слабость, тяга к сладкому и туман в голове.",
            "Цикл стал менее стабильным, кожа хуже, настроение скачет.",
        ]

        for prompt in symptom_prompts:
            with self.subTest(prompt=prompt):
                self.assertIsNone(route_live_reply(prompt))


if __name__ == "__main__":
    unittest.main()
