@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0payment-token-to-clipboard.ps1"
endlocal
