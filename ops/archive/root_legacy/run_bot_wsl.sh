#!/usr/bin/env bash
# Wellness Bot — WSL launcher
# После перезапуска WSL запускать эту команду:
# source run_bot_wsl.sh

set -e
cd "$(dirname "$0")/WellnessBot" || { echo "ERROR: WellnessBot dir not found"; exit 1; }
export PATH="$HOME/.local/bin:$PATH"

echo "=== Wellness Bot WSL Launcher ==="
echo "Workdir: $(pwd)"
echo "Python: $(python3 --version)"

# Проверка импортов
python3 -c "
import sys
sys.path.insert(0, '.')
for m in ['aiogram','aiohttp','aiohttp_socks','dotenv','config','texts','storage','lab_ocr']:
    __import__(m)
print('All imports OK')
" || { echo "ERROR: Missing dependencies"; exit 1; }

echo ""
echo "=== Starting bot ==="
python3 main.py
