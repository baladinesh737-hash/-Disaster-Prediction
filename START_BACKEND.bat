@echo off
echo ========================================
echo   GravityShift AI - Startup Script
echo ========================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✅ Ollama is running
) else (
    echo     ❌ Ollama is NOT running
    echo     → Please start Ollama first: ollama serve
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Flask Backend...
cd /d "%~dp0backend"
echo     → Backend starting on http://127.0.0.1:5000
echo     → Press Ctrl+C to stop
echo.

REM Start Flask
python app.py

pause
