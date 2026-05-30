@echo off
echo =================================================================
echo   Autonomous Multi-Agent Enterprise Intelligence Platform Launcher
echo =================================================================
echo.
echo [1/2] Launching browser to http://127.0.0.1:8000 ...
start "" "http://127.0.0.1:8000"
echo.
echo [2/2] Starting FastAPI backend server...
python backend/main.py
pause
