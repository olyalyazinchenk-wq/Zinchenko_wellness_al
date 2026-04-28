#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/antigravity-wellness}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/wellness-bot}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"

timestamp="$(date -u '+%Y%m%dT%H%M%SZ')"
archive="${BACKUP_DIR}/wellness-bot-data-${timestamp}.tar.gz"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script as root."
  exit 1
fi

if [[ ! -d "${APP_DIR}/WellnessBot/data" ]]; then
  echo "Data directory not found: ${APP_DIR}/WellnessBot/data"
  exit 1
fi

mkdir -p "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

tar -czf "${archive}" -C "${APP_DIR}" WellnessBot/data
chmod 600 "${archive}"

find "${BACKUP_DIR}" -type f -name 'wellness-bot-data-*.tar.gz' -mtime +"${RETENTION_DAYS}" -delete

echo "Backup created: ${archive}"
