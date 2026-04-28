import os
import json
from pathlib import Path
from datetime import datetime

SUBMISSIONS_DIR = Path("C:/Users/HP/Desktop/Новая папка/WellnessBot/data/submissions")
OBSIDIAN_DIR = Path("C:/Users/HP/Documents/Obsidian Vault/01_Clients")

def generate_crm_dashboard():
    print("🔄 Запуск синхронизации Obsidian CRM...")
    
    if not SUBMISSIONS_DIR.exists():
        print(f"❌ Папка с данными не найдена: {SUBMISSIONS_DIR}")
        return
        
    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    
    clients = []
    
    for file_path in SUBMISSIONS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            profile = data.get("profile", {})
            name = profile.get("full_name") or profile.get("telegram_full_name") or "Неизвестно"
            case_id = data.get("submission_id", "N/A")
            status = data.get("intake_status", "В процессе (Intake)")
            offer = data.get("offer", "premium")
            date_str = case_id.split("_")[0] if "_" in case_id else "Недавние"
            
            # Format Date nicely if possible
            if len(date_str) > 8 and "T" in date_str:
                try:
                    dt = datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
                    date_str = dt.strftime("%d.%m.%Y")
                except ValueError:
                    pass

            clients.append({
                "name": name,
                "id": case_id,
                "date": date_str,
                "status": status,
                "offer": offer
            })
        except Exception as e:
            print(f"⚠️ Ошибка при чтении {file_path.name}: {e}")
            
    # Sort by ID descending (newest first)
    clients.sort(key=lambda x: x["id"], reverse=True)
    
    # ---------------------------------------------------------
    # Формирование Markdown Документа
    # ---------------------------------------------------------
    
    md_content = f"""---
title: "Мастер-Дашборд Клиентов"
date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
tags:
  - #crm
  - #dashboard
---

# 📊 WellnessAI: Клиентский Дашборд

Это автоматически генерируемая таблица всех ваших клиентов. Обновляется скриптом-синхронизатором.

**Всего клиентов в базе:** {len(clients)}

## 🗂 Активные Кейсы

| Дата | Клиент | Статус | Услуга | ID Кейса (Файл) |
| :--- | :--- | :--- | :--- | :--- |
"""

    for c in clients:
        # Prettify Status
        status = c["status"]
        if status == "payment_received": status = "🟢 Оплачено"
        elif status == "awaiting_payment": status = "💳 Ждет оплату"
        elif status == "dossier_generation_in_progress": status = "⚙️ AI работает"
        elif status == "delivered_to_client": status = "💎 Доставлено"
        else: status = f"⏳ {status}"
        
        # Cross-link to individual case file if it exists
        case_link = f"[[{c['name'].replace(' ', '_')}_{c['id']}]]"
        
        row = f"| {c['date']} | **{c['name']}** | {status} | {c['offer'].title()} | {case_link} |\n"
        md_content += row
        
    md_content += """
---
> [!info] Подсказка
> Чтобы открыть досье клиента, просто кликните по ID в последней колонке.
"""

    target_file = OBSIDIAN_DIR / "Master_Dashboard.md"
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ Успех! Создан/обновлен сводный дашборд: {target_file}")
    except Exception as e:
        print(f"❌ Ошибка записи {target_file}: {e}")

if __name__ == "__main__":
    generate_crm_dashboard()
