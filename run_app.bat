@echo off
title ABES Student Support Help Desk Launcher
echo ========================================================
echo   ABES Engineering College - Student Support Help Desk
echo ========================================================
echo.
echo [1/3] Launching Backend on http://localhost:8000 ...
start "ABES Help Desk Backend" "%~dp0start_backend.bat"

ping -n 5 127.0.0.1 >nul

echo [2/3] Launching Frontend on http://localhost:5173 ...
start "ABES Help Desk Frontend" "%~dp0start_frontend.bat"

ping -n 4 127.0.0.1 >nul

echo [3/3] Opening ABES Help Desk in your browser ...
start http://localhost:5173

echo.
echo ========================================================
echo ABES Help Desk is Live!
echo - Web App: http://localhost:5173
echo - API Docs: http://localhost:8000/docs
echo ========================================================
echo (Keep the backend and frontend terminal windows open while using the app.)
echo.
pause
