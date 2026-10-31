@echo off
title ABES Student Support Help Desk - Backend
echo ========================================================
echo   Starting ABES Help Desk Backend (FastAPI)...
echo ========================================================
cd /d "%~dp0backend"
".\venv\Scripts\uvicorn.exe" app.main:app --reload --host 0.0.0.0 --port 8000
pause
