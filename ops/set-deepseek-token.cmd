@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0set-deepseek-token.ps1"
endlocal
pause
