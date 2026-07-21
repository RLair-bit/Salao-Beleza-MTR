@echo off
title Salao de Beleza
cd /d "%~dp0"

echo.
echo   A iniciar o Salao de Beleza...
echo.

call venv\Scripts\activate.bat

start "Salao de Beleza - servidor" cmd /k "python manage.py runserver"

timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:8000

exit