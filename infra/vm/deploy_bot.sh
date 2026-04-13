#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/antigravity-wellness"
SERVICE_NAME="wellness-bot"

if [[ ! -d "$APP_DIR" ]]; then
  echo "Application directory $APP_DIR not found"
  exit 1
fi

cd "$APP_DIR"

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r WellnessBot/requirements.txt

sudo cp infra/vm/wellness-bot.service /etc/systemd/system/${SERVICE_NAME}.service
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}
sudo systemctl status ${SERVICE_NAME} --no-pager
