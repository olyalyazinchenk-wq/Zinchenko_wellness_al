from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from case_service import (  # noqa: E402
    build_initial_submission_payload,
    build_session_from_submission,
    build_submission_payload,
    persist_submission_enrichment,
    save_submission_state,
    update_submission_status,
)
from payment_flow import (  # noqa: E402
    PAYMENT_STATUS_MANUAL_CONFIRMED,
    PAYMENT_STATUS_MANUAL_PENDING,
    PREMIUM_PRICE_KOPECKS,
    build_invoice_payload,
    build_payment_context,
    get_product_offer,
    is_payment_confirmed_for_dossier,
    mark_manual_payment_confirmed,
    mark_manual_payment_pending,
    parse_invoice_payload,
    validate_payment_event,
)
from storage import load_submission  # noqa: E402


def build_session_fixture() -> dict:
    return {
        "submission_id": "test_payment_case_001",
        "offer": "premium",
        "tier": "premium",
        "telegram_user_id": 1084557944,
        "telegram_username": "Olgazinchenko1186",
        "telegram_full_name": "Ольга",
        "full_name": "Ольга",
        "age": 40,
        "city": "Москва",
        "anthropometrics": "Рост 168, вес 72, желаемый вес 65",
        "contact": "telegram_current_chat",
        "work_lifestyle": "Сидячая работа, 8 часов за компьютером.",
        "symptoms": "Выпадение волос",
        "wellbeing_energy": "Энергия утром 4/10, днём 6/10, вечером 3/10.",
        "complaint_pattern": "Усилилось за последние 3 месяца, хуже на фоне стресса.",
        "goals": "Понять следующий шаг",
        "nutrition": "Нерегулярное питание, мало белка утром, кофе 2 раза в день.",
        "food_behavior": "Тяга к сладкому вечером, иногда заедание стресса.",
        "digestion": "Периодическое вздутие после сладкого.",
        "sleep_stress": "Сон 6 часов, высокий стресс.",
        "activity": "Сидячая работа, прогулки 2-3 раза в неделю.",
        "female_hormones": "Цикл регулярный, ПМС, обильность умеренная.",
        "emotional_stress": "Стресс 8/10, тревожность.",
        "background": "Без критичных диагнозов, принимает селен.",
        "risk_details": "Аллергий нет, давление иногда снижено.",
        "motivation": "Хочет больше энергии и устойчивый режим.",
        "red_flags": "Нет",
        "lab_notes": "Без приложений",
        "documents": [],
        "consent_given": True,
        "parsed_biomarkers": [],
        "vision_analysis": None,
    }


class PaymentCaseServiceTests(unittest.TestCase):
    def test_initial_submission_payload_marks_consent_pending(self) -> None:
        session = build_session_fixture()
        session["consent_given"] = False

        submission = build_initial_submission_payload(session, now_iso="2026-05-01T07:20:00Z")

        self.assertEqual(submission["submission_id"], session["submission_id"])
        self.assertEqual(submission["offer"], "premium")
        self.assertEqual(submission["intake_status"], "consent_pending")
        self.assertEqual(submission["status_updated_at"], "2026-05-01T07:20:00Z")
        self.assertEqual(submission["created_at"], "2026-05-01T07:20:00Z")
        self.assertFalse(submission["consent_given"])

    def test_invoice_payload_roundtrip_and_invalid_cases(self) -> None:
        payload = build_invoice_payload("case_001", 12345)
        self.assertEqual(parse_invoice_payload(payload), ("case_001", 12345))
        self.assertEqual(parse_invoice_payload("broken"), (None, None))
        self.assertEqual(parse_invoice_payload(None), (None, None))
        self.assertEqual(parse_invoice_payload("premium:case_001:not_an_int"), ("case_001", None))

    def test_validate_payment_event_accepts_match_and_rejects_mismatch(self) -> None:
        session = build_session_fixture()
        submission = build_submission_payload(session)
        submission["payment_context"] = build_payment_context(session, now_iso="2026-04-21T00:30:00Z")

        self.assertIsNone(
            validate_payment_event(
                submission,
                telegram_user_id=session["telegram_user_id"],
                invoice_payload=submission["payment_context"]["invoice_payload"],
                currency="RUB",
                total_amount=PREMIUM_PRICE_KOPECKS,
            )
        )
        self.assertIn(
            "Сумма оплаты не совпадает",
            validate_payment_event(
                submission,
                telegram_user_id=session["telegram_user_id"],
                invoice_payload=submission["payment_context"]["invoice_payload"],
                currency="RUB",
                total_amount=1,
            )
            or "",
        )
        self.assertIn(
            "Пользователь оплаты не совпадает",
            validate_payment_event(
                submission,
                telegram_user_id=999,
                invoice_payload=submission["payment_context"]["invoice_payload"],
                currency="RUB",
                total_amount=PREMIUM_PRICE_KOPECKS,
            )
            or "",
        )

    def test_payment_context_uses_selected_product_price(self) -> None:
        session = build_session_fixture()
        session["offer"] = "vip"
        context = build_payment_context(session, now_iso="2026-04-21T00:30:00Z")

        self.assertEqual(context["offer_code"], "vip")
        self.assertEqual(context["amount_rub"], get_product_offer("vip")["price_rub"])
        self.assertEqual(context["amount_kop"], get_product_offer("vip")["amount_kop"])

    def test_manual_payment_state_transitions(self) -> None:
        session = build_session_fixture()
        submission = build_submission_payload(session)

        self.assertFalse(is_payment_confirmed_for_dossier(submission))

        mark_manual_payment_pending(
            submission,
            now_iso="2026-04-22T00:12:00Z",
            reason="payment_provider_not_configured",
        )
        self.assertEqual(submission["intake_status"], PAYMENT_STATUS_MANUAL_PENDING)
        self.assertEqual(submission["payment_status"], PAYMENT_STATUS_MANUAL_PENDING)
        self.assertFalse(is_payment_confirmed_for_dossier(submission))

        mark_manual_payment_confirmed(
            submission,
            now_iso="2026-04-22T00:13:00Z",
            admin_user_id=1084557944,
            note="Unit test confirmation",
        )
        self.assertEqual(submission["intake_status"], PAYMENT_STATUS_MANUAL_CONFIRMED)
        self.assertEqual(submission["payment_status"], PAYMENT_STATUS_MANUAL_CONFIRMED)
        self.assertEqual(submission["manual_payment_confirmed_by"], 1084557944)
        self.assertTrue(is_payment_confirmed_for_dossier(submission))

    def test_case_service_roundtrip_and_enrichment(self) -> None:
        session = build_session_fixture()
        submission = build_submission_payload(session)
        update_submission_status(
            submission,
            intake_status="awaiting_payment",
            now_iso="2026-04-21T00:31:00Z",
            payment_status="awaiting_payment",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            submissions_dir = Path(tmp_dir)
            save_submission_state(submissions_dir, submission)

            persist_submission_enrichment(
                submissions_dir,
                submission["submission_id"],
                now_iso="2026-04-21T00:32:00Z",
                parsed_biomarkers=[{"marker": "Ferritin", "value": "22"}],
                vision_analysis="Нужен follow-up по фото анализов.",
            )
            loaded = load_submission(submissions_dir, submission["submission_id"])
            assert loaded is not None

            self.assertEqual(loaded["parsed_biomarkers"][0]["marker"], "Ferritin")
            self.assertEqual(loaded["vision_analysis"], "Нужен follow-up по фото анализов.")
            self.assertEqual(loaded["enrichment_updated_at"], "2026-04-21T00:32:00Z")

            restored = build_session_from_submission(
                loaded,
                SimpleNamespace(
                    id=session["telegram_user_id"],
                    username=session["telegram_username"],
                    full_name=session["telegram_full_name"],
                ),
            )
            self.assertEqual(restored["submission_id"], submission["submission_id"])
            self.assertEqual(restored["step"], "done")
            self.assertEqual(restored["full_name"], "Ольга")
            self.assertEqual(restored["anthropometrics"], session["anthropometrics"])
            self.assertEqual(restored["work_lifestyle"], session["work_lifestyle"])
            self.assertEqual(restored["nutrition"], session["nutrition"])
            self.assertEqual(restored["food_behavior"], session["food_behavior"])
            self.assertEqual(restored["digestion"], session["digestion"])
            self.assertEqual(restored["sleep_stress"], session["sleep_stress"])
            self.assertEqual(restored["female_hormones"], session["female_hormones"])
            self.assertEqual(restored["risk_details"], session["risk_details"])
            self.assertTrue(restored["consent_given"])


if __name__ == "__main__":
    unittest.main()
