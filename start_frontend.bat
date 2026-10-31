@echo off
title ABES Student Support Help Desk - Frontend
echo ========================================================
echo   Starting ABES Help Desk Frontend (React + Vite)...
echo ========================================================
set "PATH=C:\Program Files\nodejs;%PATH%"
cd /d "%~dp0frontend"
cmd.exe /c npm run dev
pause
