@echo off
setlocal

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found at venv\Scripts\python.exe
    echo Create it first, then install dependencies with:
    echo python -m venv venv
    echo venv\Scripts\python.exe -m pip install -r backend\requirements.txt
    exit /b 1
)

venv\Scripts\python.exe backend\app.py
