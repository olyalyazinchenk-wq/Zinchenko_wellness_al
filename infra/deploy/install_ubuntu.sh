#!/usr/bin/env bash
set -euo pipefail

# Production bootstrap for the Telegram-first Wellness bot on Ubuntu 22.04/24.04.
# Run from the project root after copying the repo to APP_DIR, or override APP_DIR.
#
# Example:
#   sudo APP_DIR=/opt/antigravity-wellness bash infra/deploy/install_ubuntu.sh

APP_DIR="${APP_DIR:-/opt/antigravity-wellness}"
APP_USER="${APP_USER:-wellnessbot}"
SERVICE_NAME="${SERVICE_NAME:-wellness-bot}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/wellness-bot}"

log() {
  printf '\n[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script as root."
  exit 1
fi

if [[ ! -d "${APP_DIR}" ]]; then
  echo "Application directory not found: ${APP_DIR}"
  echo "Copy the project to ${APP_DIR} first."
  exit 1
fi

if [[ ! -f "${APP_DIR}/WellnessBot/main.py" ]]; then
  echo "Missing bot entrypoint: ${APP_DIR}/WellnessBot/main.py"
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

log "Installing OS packages"
apt update
apt install -y python3 python3-venv python3-pip ca-certificates curl rsync ufw

if ! id -u "${APP_USER}" >/dev/null 2>&1; then
  log "Creating system user ${APP_USER}"
  useradd --system --home "${APP_DIR}" --shell /usr/sbin/nologin "${APP_USER}"
fi

log "Preparing app directories and permissions"
mkdir -p "${APP_DIR}/WellnessBot/data" "${BACKUP_DIR}"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}/WellnessBot/data"
chown -R root:root "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

cd "${APP_DIR}"

log "Creating Python virtual environment"
"${PYTHON_BIN}" -m venv .venv
.venv/bin/python -m pip install --upgrade pip wheel
.venv/bin/python -m pip install -r WellnessBot/requirements.txt

log "Installing systemd service"
install -m 0644 infra/deploy/wellness-bot.service "/etc/systemd/system/${SERVICE_NAME}.service"
install -m 0755 infra/deploy/backup_data.sh /usr/local/sbin/wellness-bot-backup

if [[ -f "${APP_DIR}/.env" ]]; then
  log "Locking down .env permissions"
  chown "${APP_USER}:${APP_USER}" "${APP_DIR}/.env"
  chmod 600 "${APP_DIR}/.env"
else
  log "No .env found yet. Copy infra/deploy/env.production.example to .env and fill secrets before start."
fi

log "Configuring firewall baseline"
ufw allow OpenSSH
ufw --force enable

log "Reloading systemd"
systemctl daemon-reload
systemctl enable "${SERVICE_NAME}.service"

if [[ -f "${APP_DIR}/.env" ]]; then
  log "Starting ${SERVICE_NAME}"
  systemctl restart "${SERVICE_NAME}.service"
  systemctl --no-pager --full status "${SERVICE_NAME}.service" || true
else
  log "Service enabled but not started because .env is missing."
fi

cat <<EOF

Install complete.

Useful commands:
  systemctl status ${SERVICE_NAME} --no-pager
  journalctl -u ${SERVICE_NAME} -f
  systemctl restart ${SERVICE_NAME}
  wellness-bot-backup

EOF
