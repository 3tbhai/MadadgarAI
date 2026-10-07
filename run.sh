#!/usr/bin/env bash
# Launcher for MadadgaarAI Platform

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "======================================================="
echo "   🚀 Starting MadadgaarAI Platform (Vidyarthi Hub)    "
echo "======================================================="

if [ -f "./venv/bin/python" ]; then
    echo "[OK] Using virtual environment Python (venv)..."
    exec ./venv/bin/python run.py
else
    echo "[INFO] Virtual environment not found, using system python..."
    exec python3 run.py
fi
