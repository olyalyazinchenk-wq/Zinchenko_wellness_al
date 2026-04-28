from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from voice_processor import is_sync_audio_compatible  # noqa: E402


class VoiceProcessorTests(unittest.TestCase):
    def test_sync_audio_compatibility_detection(self) -> None:
        self.assertTrue(is_sync_audio_compatible(file_name="note.ogg"))
        self.assertTrue(is_sync_audio_compatible(file_name="note.OPUS"))
        self.assertTrue(is_sync_audio_compatible(mime_type="audio/ogg"))
        self.assertFalse(is_sync_audio_compatible(file_name="recording.mp3"))
        self.assertFalse(is_sync_audio_compatible(file_name="memo.m4a"))
        self.assertFalse(is_sync_audio_compatible(mime_type="audio/mpeg"))


if __name__ == "__main__":
    unittest.main()
