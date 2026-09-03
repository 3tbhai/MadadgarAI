# 1-Click PowerShell Launcher for MadadgaarAI Platform
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "   🚀 Starting MadadgaarAI Platform (Vidyarthi Hub)    " -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path ".\venv\Scripts\python.exe") {
    Write-Host "[OK] Using virtual environment Python (venv)..." -ForegroundColor Yellow
    & ".\venv\Scripts\python.exe" run.py
} else {
    Write-Host "[INFO] Virtual environment not found, using system python..." -ForegroundColor Yellow
    python run.py
}
