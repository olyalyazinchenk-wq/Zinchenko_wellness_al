# DeepSeek VM in Yandex Cloud

This directory contains the minimum deployment assets for a Russian-contour DeepSeek runtime:

- `cloud-init/deepseek-bootstrap.yaml` installs Ollama and pulls `deepseek-r1:8b`
- `vm/wellness-bot.service` runs the Telegram bot as a systemd service
- `vm/deploy_bot.sh` installs Python dependencies and enables the service

Recommended contour for the current cloud limits:

- Ubuntu 24.04 VM
- CPU-only
- no public Ollama port
- Telegram bot and Ollama on the same VM

Reason:

- current cloud has zero GPU quota
- this keeps client payloads inside Yandex Cloud once Telegram delivers the message to the bot
