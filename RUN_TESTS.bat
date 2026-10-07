@echo off
echo ========================================
echo   GravityShift AI - Complete Test
echo ========================================
echo.

REM Test 1: Ollama
echo [TEST 1] Checking Ollama...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✅ Ollama is running
) else (
    echo     ❌ Ollama is NOT running
    echo     → Start with: ollama serve
    goto :end
)

REM Test 2: Backend
echo.
echo [TEST 2] Checking Backend...
curl -s http://127.0.0.1:5000/api >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✅ Backend is running
) else (
    echo     ❌ Backend is NOT running
    echo     → Start with: START_BACKEND.bat
    goto :end
)

REM Test 3: Python test
echo.
echo [TEST 3] Running Python tests...
cd /d "%~dp0backend"
python test_ollama.py

:end
echo.
echo ========================================
echo   Test Complete
echo ========================================
pause
