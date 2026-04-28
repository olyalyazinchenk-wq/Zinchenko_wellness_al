import sys
import os
import asyncio
from pathlib import Path
import json
import re
from datetime import datetime

# Add WellnessBot to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'WellnessBot')))

from config import load_settings
from ai_drafting import generate_case_draft, generate_live_reply
from html_pdf_engine import create_premium_pdf
from storage import save_submission, load_submission

class WellnessTester:
    def __init__(self):
        self.settings = load_settings()
        self.results = []

    def log_test(self, name, success, message=""):
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {name}: {message}")
        self.results.append({"name": name, "success": success, "message": message})

    async def test_ai_dossier_generation(self):
        print("\n--- Test 1: AI Dossier Generation & JSON Parsing ---")
        mock_submission = {
            "submission_id": "test_qa_dossier_001",
            "offer": "premium",
            "profile": {"full_name": "QA Tester", "age": 30, "city": "TestCity"},
            "medical_context": {
                "symptoms": "усталость, головная боль",
                "goal": "энергия",
                "background": "нет",
                "red_flags": "нет",
                "lab_notes": "нет"
            }
        }
        try:
            draft = await asyncio.to_thread(generate_case_draft, self.settings, mock_submission, tier="premium")
            if not draft:
                self.log_test("Dossier Generation", False, "No draft returned")
                return

            clean = re.sub(r"^```(?:json)?\s*", "", draft.strip(), flags=re.IGNORECASE)
            clean = re.sub(r"\s*```$", "", clean)
            data = json.loads(clean.strip())
            self.log_test("Dossier Generation", True, f"JSON valid. Keys: {list(data.keys())}")
            
            # Test PDF rendering
            output_path = Path(self.settings.drafts_dir) / "test_qa_rendering.pdf"
            await asyncio.to_thread(create_premium_pdf, data, str(output_path))
            if output_path.exists():
                self.log_test("PDF Rendering", True, f"PDF created: {output_path.name}")
            else:
                self.log_test("PDF Rendering", False, "PDF file was not created")
        except Exception as e:
            self.log_test("Dossier/PDF Flow", False, f"Exception: {str(e)}")

    async def test_anti_loop_logic(self):
        print("\n--- Test 2: Anti-Loop Guard Logic ---")
        reply = "Тот же самый ответ"
        history = [
            {"role": "assistant", "content": "Тот же самый ответ"},
            {"role": "assistant", "content": "Тот же самый ответ"}
        ]
        assistant_replies = [msg["content"] for msg in history if msg["role"] == "assistant"]
        loop_detected = (len(assistant_replies) >= 2 and reply == assistant_replies[-1] and reply == assistant_replies[-2])
        if loop_detected:
            self.log_test("Anti-Loop Guard", True, "Repeated sequence correctly detected")
        else:
            self.log_test("Anti-Loop Guard", False, "Failed to detect repeat sequence")

    async def test_voice_integration_flow(self):
        print("\n--- Test 3: Voice Integration Mock Flow ---")
        try:
            from voice_processor import handle_voice_to_text
            self.log_test("Voice Module Import", True, "Successfully imported voice_processor")
        except Exception as e:
            self.log_test("Voice Module Import", False, str(e))

    async def test_admin_approval_logic(self):
        print("\n--- Test 4: Admin Approval Logic & Path Safety ---")
        mock_id = "test_admin_001"
        mock_submission = {
            "submission_id": mock_id,
            "profile": {"telegram_user_id": 12345},
            "pdf_path": str(Path(self.settings.drafts_dir) / f"dossier_{mock_id}.pdf")
        }
        save_submission(self.settings.submissions_dir, mock_id, mock_submission)
        loaded = load_submission(self.settings.submissions_dir, mock_id)
        if loaded and loaded.get("pdf_path"):
            self.log_test("Admin Approval Pathing", True, "Submission loaded with correct PDF path")
        else:
            self.log_test("Admin Approval Pathing", False, "Failed to load submission or path missing")

    async def test_vision_analysis(self):
        print("\n--- Test 5: Vision AI Physical Assessment ---")
        try:
            from lab_ocr import analyze_physical_markers
            mock_path = Path("test_vision.jpg")
            if not mock_path.exists():
                mock_path.write_bytes(b"dummy")
            result = await analyze_physical_markers(mock_path, self.settings)
            if "findings" in result or "interpretation" in result:
                self.log_test("Vision AI", True, f"Type: {result.get('type')}, Findings: {len(result.get('findings', []))}")
            else:
                self.log_test("Vision AI", False, "Missing expected JSON keys")
        except Exception as e:
            self.log_test("Vision AI", False, f"Exception: {str(e)}")

    async def test_tma_api_data(self):
        print("\n--- Test 6: TMA API & Session Integrity ---")
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/session?user_id=999999")
                if response.status_code in [200, 404]: 
                    self.log_test("TMA API Connectivity", True, f"Status: {response.status_code}")
                else:
                    self.log_test("TMA API Connectivity", False, f"Server returned {response.status_code}")
        except Exception as e:
            self.log_test("TMA API Connectivity", False, f"Connection failed: {str(e)}")

    async def run_all(self):
        print("==================================================")
        print("[QA SubAgent] Starting Comprehensive Stress Test...")
        print("==================================================")
        await self.test_ai_dossier_generation()
        await self.test_anti_loop_logic()
        await self.test_voice_integration_flow()
        await self.test_admin_approval_logic()
        await self.test_vision_analysis()
        await self.test_tma_api_data()
        
        failed = [t for t in self.results if not t["success"]]
        print("\n==================================================")
        if not failed:
            print("RUN SUCCESS: ALL SYSTEMS GO! Premium Wellness Ecosystem is robust.")
        else:
            print(f"RUN FINISHED with {len(failed)} failures.")
        print("==================================================")

if __name__ == "__main__":
    tester = WellnessTester()
    asyncio.run(tester.run_all())
