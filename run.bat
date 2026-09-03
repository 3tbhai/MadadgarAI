@echo off
title MadadgaarAI - Indian Scholarships and Research Funding System
echo =======================================================
echo    🚀 Starting MadadgaarAI Platform (Vidyarthi Hub)
echo =======================================================
echo.

if exist venv\Scripts\python.exe (
    echo [OK] Using virtual environment Python...
    venv\Scripts\python.exe run.py
) else (
    echo [INFO] Virtual environment not found, using system python...
    python run.py
)

pause
