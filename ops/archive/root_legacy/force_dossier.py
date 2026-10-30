import sys
import os
import asyncio
import json
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add WellnessBot to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'WellnessBot')))

from config import load_settings
from main import normalize_dossier_pdf_data, apply_safe_action_floor, utc_now_iso
from html_pdf_engine import create_premium_pdf
from storage import load_submission, save_submission
from aiogram import Bot

async def main():
    settings = load_settings()
    submission_id = "20260531T183007Z_1084557944"
    client_id = 1084557944
    
    print(f"Loading submission: {submission_id}")
    submission = load_submission(settings.submissions_dir, submission_id)
    if not submission:
        print("Error: Submission not found!")
        return
        
    print("Preparing PDF data...")
    # Load JSON draft
    draft_path = Path(submission["draft_path"])
    draft_text = draft_path.read_text(encoding="utf-8")
    
    import re
    clean_json_str = draft_text.strip()
    clean_json_str = re.sub(r"^```(?:json)?\s*", "", clean_json_str, flags=re.IGNORECASE)
    clean_json_str = re.sub(r"\s*```$", "", clean_json_str)
    
    raw_data = json.loads(clean_json_str.strip())
    pdf_data = apply_safe_action_floor(
        normalize_dossier_pdf_data(raw_data),
        submission
    )
    
    pdf_filename = f"dossier_{submission_id}.pdf"
    pdf_path = settings.drafts_dir / pdf_filename
    
    print(f"Rendering premium PDF to {pdf_path}...")
    await asyncio.to_thread(create_premium_pdf, pdf_data, str(pdf_path))
    
    if pdf_path.exists():
        print("PDF generated successfully! Initializing bot to send...")
        bot = Bot(token=settings.bot_token, proxy=settings.bot_proxy_url)
        
        from aiogram.types import FSInputFile
        pdf_file = FSInputFile(str(pdf_path))
        
        print("Sending PDF to client Telegram...")
        await bot.send_document(
            chat_id=client_id,
            document=pdf_file,
            caption="✨ Ваше премиальное Wellness-досье готово! Извиняемся за небольшую техническую задержку."
        )
        
        # Update submission states
        submission["pdf_path"] = str(pdf_path)
        submission["intake_status"] = "delivered_to_client"
        submission["payment_status"] = "paid"
        submission["status_updated_at"] = utc_now_iso()
        save_submission(settings.submissions_dir, submission_id, submission)
        print("Database updated! Delivered to client.")
        await bot.session.close()
    else:
        print("Error: PDF file was not created!")

if __name__ == "__main__":
    asyncio.run(main())
