@echo off
setlocal
title Set PAYMENT_TOKEN
echo Запуск настройки PAYMENT_TOKEN...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0set-payment-token.ps1"
echo.
if errorlevel 1 (
  echo Скрипт завершился с ошибкой. Сообщение выше.
) else (
  echo Скрипт завершился успешно.
)
echo Нажмите любую клавишу, чтобы закрыть окно.
pause >nul
endlocal
