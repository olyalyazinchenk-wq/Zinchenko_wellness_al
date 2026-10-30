from __future__ import annotations

import dataclasses
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


BOT_DIR = Path(__file__).resolve().parents[1] / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

import main as bot_main  # noqa: E402
from handlers.nutriok_intake import (  # noqa: E402
    configure_nutriok_intake,
    format_progress_header,
    handle_baseline_select,
    handle_confirm_edit,
    handle_confirm_submit,
    handle_consent_accept,
    handle_consent_decline,
    handle_context_entry,
    handle_continue_command,
    handle_diary_entry,
    handle_goal_select,
    handle_labs_complete,
    handle_labs_upload,
    handle_metric_custom_prompt,
    handle_metric_default,
    handle_metric_text,
    handle_nutriok_tier_start,
)
from storage import load_submission  # noqa: E402


def _make_user(user_id: int = 777001, full_name: str = "Анна Тест") -> SimpleNamespace:
    return SimpleNamespace(id=user_id, username="anna_test", full_name=full_name)


def _make_message(
    user: SimpleNamespace,
    *,
    text: str | None = None,
    voice_file_id: str | None = None,
    photo_file_id: str | None = None,
    caption: str | None = None,
    doc_file_id: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        from_user=user,
        chat=SimpleNamespace(id=user.id),
        text=text,
        caption=caption,
        voice=SimpleNamespace(file_id=voice_file_id) if voice_file_id else None,
        photo=[SimpleNamespace(file_id=photo_file_id)] if photo_file_id else None,
        document=SimpleNamespace(file_id=doc_file_id) if doc_file_id else None,
        answer=AsyncMock(),
    )


def _make_callback(user: SimpleNamespace, data: str) -> SimpleNamespace:
    msg = _make_message(user)
    return SimpleNamespace(
        id=f"cb_{data}",
        data=data,
        from_user=user,
        message=msg,
        answer=AsyncMock(),
    )


class NutriOKIntakeFlowTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.submissions_dir = base / "submissions"
        self.runtime_state_path = base / "runtime_state.json"
        self.submissions_dir.mkdir(parents=True, exist_ok=True)
        bot_main.user_sessions.clear()
        bot_main.chat_sessions.clear()
        self.patched_settings = dataclasses.replace(
            bot_main.settings,
            submissions_dir=self.submissions_dir,
            runtime_state_path=self.runtime_state_path,
            admin_chat_ids=(481955956,),
            payment_mode="manual",
            tma_enabled=False,
        )
        self.settings_patcher = patch.object(bot_main, "settings", self.patched_settings)
        self.settings_patcher.start()

        self.finalize_mock = AsyncMock()
        self.voice_mock = AsyncMock(return_value="Завтрак: творог и ягоды; обед: гречка с индейкой; ужин: салат.")
        self.red_flag_mock = AsyncMock()
        configure_nutriok_intake(
            get_session=bot_main.get_session,
            start_session=bot_main.start_session,
            clear_session=bot_main.clear_session,
            touch_session=bot_main.touch_session,
            save_submission_from_session=bot_main.save_submission_from_session,
            finalize_submission=self.finalize_mock,
            transcribe_voice=self.voice_mock,
            notify_red_flag=self.red_flag_mock,
        )

    def tearDown(self) -> None:
        self.settings_patcher.stop()
        self.temp_dir.cleanup()

    def test_progress_header_format(self) -> None:
        self.assertEqual(format_progress_header(3, 7), "● ● ● ○ ○ ○ ○  Шаг 3 из 7")
        self.assertEqual(format_progress_header(1, 3), "● ○ ○  Шаг 1 из 3")

    async def test_ok_start_flow_delivers_safe_step_and_express_offer(self) -> None:
        user = _make_user(777001)
        cb_tier = _make_callback(user, "tier_ok_start")
        await handle_nutriok_tier_start(cb_tier)
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "consent")

        cb_consent = _make_callback(user, "ok_consent_accept")
        await handle_consent_accept(cb_consent)
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "goal")

        cb_goal = _make_callback(user, "ok_goal_energy")
        await handle_goal_select(cb_goal)
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "baseline")

        cb_base = _make_callback(user, "ok_baseline_4")
        await handle_baseline_select(cb_base)
        session = bot_main.get_session(user.id)
        self.assertEqual(session["nutriok_step"], "done")
        sent_text = cb_base.message.answer.call_args.args[0]
        self.assertIn("ОК-Старт завершён", sent_text)
        self.assertIn("ОК-Экспресс", sent_text)
        self.finalize_mock.assert_not_awaited()

    async def test_ok_express_e2e_with_text_voice_and_photo_diary_and_restart_persistence(self) -> None:
        user = _make_user(777002)
        await handle_nutriok_tier_start(_make_callback(user, "tier_ok_express"))
        await handle_consent_accept(_make_callback(user, "ok_consent_accept"))
        await handle_goal_select(_make_callback(user, "ok_goal_digestion"))
        await handle_baseline_select(_make_callback(user, "ok_baseline_3"))
        await handle_metric_default(_make_callback(user, "ok_metric_default"))

        # Day 1: text
        await handle_diary_entry(
            _make_message(user, text="Завтрак: омлет и кофе; обед: борщ; ужин: рыба с овощами.")
        )
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "diary_day_2")

        # Simulate bot restart (in-memory clear + restore_runtime_state)
        bot_main.user_sessions.clear()
        bot_main.restore_runtime_state()
        restored = bot_main.get_session(user.id)
        self.assertIsNotNone(restored)
        self.assertEqual(restored["nutriok_step"], "diary_day_2")

        # /continue resumes right at diary_day_2
        cont_msg = _make_message(user, text="/continue")
        await handle_continue_command(cont_msg)
        self.assertIn("День 2 из 3", cont_msg.answer.call_args.args[0])

        # Day 2: voice message -> transcribed via STT hook
        await handle_diary_entry(_make_message(user, voice_file_id="voice_file_123"))
        self.voice_mock.assert_awaited_once_with("voice_file_123")
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "diary_day_3")

        # Day 3: photo with caption
        await handle_diary_entry(
            _make_message(user, photo_file_id="photo_day_3", caption="Завтрак, обед и ужин на фото")
        )
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "context")

        # Health context
        await handle_context_entry(
            _make_message(
                user,
                text="Вздутие вечером\nвитамин D 1000 МЕ\nаллергий нет\nсон 7 часов, сидячая работа",
            )
        )
        # ok_express does not support labs -> jumps directly to confirm
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "confirm")

        cb_submit = _make_callback(user, "ok_confirm_submit")
        await handle_confirm_submit(cb_submit)
        self.finalize_mock.assert_awaited_once()

        session = bot_main.get_session(user.id)
        saved = load_submission(self.submissions_dir, session["submission_id"])
        self.assertIsNotNone(saved)
        self.assertEqual(saved["primary_goal"], "digestion")
        self.assertEqual(saved["baseline_score"], 3)
        self.assertEqual(saved["goal_metric"], "вздутие после еды, 0–10")
        self.assertEqual(len(saved["nutrition_diary"]), 3)
        self.assertEqual(saved["nutrition_diary"][1]["meals_text"], self.voice_mock.return_value)

    async def test_ok_review_includes_labs_step_and_custom_metric(self) -> None:
        user = _make_user(777003)
        await handle_nutriok_tier_start(_make_callback(user, "tier_ok_review"))
        await handle_consent_accept(_make_callback(user, "ok_consent_accept"))
        await handle_goal_select(_make_callback(user, "ok_goal_sleep_stress"))
        await handle_baseline_select(_make_callback(user, "ok_baseline_2"))
        await handle_metric_custom_prompt(_make_callback(user, "ok_metric_custom"))
        await handle_metric_text(_make_message(user, text="Пробуждения за ночь, кол-во"))

        for idx in range(1, 4):
            await handle_diary_entry(_make_message(user, text=f"Рацион за день {idx}"))

        await handle_context_entry(_make_message(user, text="нет"))
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "labs")

        await handle_labs_upload(_make_message(user, doc_file_id="lab_doc_01"))
        self.assertIn("lab_doc_01", bot_main.get_session(user.id)["nutriok_intake"]["labs_upload_ids"])

        await handle_labs_complete(_make_callback(user, "ok_labs_done"))
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "confirm")

        await handle_confirm_edit(_make_callback(user, "ok_confirm_edit"))
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "goal")

    async def test_confirm_validation_errors_redirect_to_missing_step(self) -> None:
        user = _make_user(777004)
        await handle_nutriok_tier_start(_make_callback(user, "tier_ok_express"))
        await handle_consent_accept(_make_callback(user, "ok_consent_accept"))
        await handle_goal_select(_make_callback(user, "ok_goal_energy"))
        await handle_baseline_select(_make_callback(user, "ok_baseline_5"))

        # Force jump to confirm with only 1 diary day
        session = bot_main.get_session(user.id)
        session["nutriok_intake"]["goal_metric"] = "энергия в 15:00, 0–10"
        session["nutriok_intake"]["nutrition_diary"] = [
            {"day_index": 1, "meals_text": "День 1", "photo_file_ids": []}
        ]
        session["nutriok_step"] = "confirm"

        cb_submit = _make_callback(user, "ok_confirm_submit")
        await handle_confirm_submit(cb_submit)
        self.finalize_mock.assert_not_awaited()
        self.assertEqual(bot_main.get_session(user.id)["nutriok_step"], "diary_day_2")

    async def test_red_flag_and_underage_handling_in_context(self) -> None:
        user_rf = _make_user(777005)
        await handle_nutriok_tier_start(_make_callback(user_rf, "tier_ok_express"))
        await handle_consent_accept(_make_callback(user_rf, "ok_consent_accept"))
        await handle_goal_select(_make_callback(user_rf, "ok_goal_digestion"))
        await handle_baseline_select(_make_callback(user_rf, "ok_baseline_2"))
        await handle_metric_default(_make_callback(user_rf, "ok_metric_default"))
        for idx in range(1, 4):
            await handle_diary_entry(_make_message(user_rf, text=f"День {idx}"))

        rf_msg = _make_message(user_rf, text="Вчера была кровь в стуле и резкое похудение")
        await handle_context_entry(rf_msg)
        self.red_flag_mock.assert_awaited_once()
        self.assertIn("врачу", rf_msg.answer.call_args_list[0].args[0])

        # Underage stop
        user_kid = _make_user(777006)
        await handle_nutriok_tier_start(_make_callback(user_kid, "tier_ok_express"))
        await handle_consent_accept(_make_callback(user_kid, "ok_consent_accept"))
        await handle_goal_select(_make_callback(user_kid, "ok_goal_energy"))
        await handle_baseline_select(_make_callback(user_kid, "ok_baseline_5"))
        await handle_metric_default(_make_callback(user_kid, "ok_metric_default"))
        for idx in range(1, 4):
            await handle_diary_entry(_make_message(user_kid, text=f"День {idx}"))

        kid_msg = _make_message(user_kid, text="Мне 15 лет, усталость после школы")
        await handle_context_entry(kid_msg)
        self.assertEqual(bot_main.get_session(user_kid.id)["nutriok_step"], "stopped_underage")
        self.assertIn("18+", kid_msg.answer.call_args.args[0])

    async def test_consent_decline_clears_session(self) -> None:
        user = _make_user(777007)
        await handle_nutriok_tier_start(_make_callback(user, "tier_ok_start"))
        await handle_consent_decline(_make_callback(user, "ok_consent_decline"))
        self.assertIsNone(bot_main.get_session(user.id))


if __name__ == "__main__":
    unittest.main()
