@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0set-aitunnel-deepseek-token.ps1"
endlocal
pause
