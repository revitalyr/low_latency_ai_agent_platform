@echo off
REM Quick Start Script for Low-Latency AI Agent Platform
REM Simple script to start the system without rebuilding

echo ==========================================
echo Low-Latency AI Agent Platform
echo Quick Start Script
echo ==========================================

REM Check if Rust binary exists
if not exist "rust-core\target\release\rust-core.exe" (
    echo [ERROR] Rust binary not found. Please run: cargo build --release
    echo [INFO] Navigate to rust-core directory and run: cargo build --release
    pause
    exit /b 1
)

echo [SUCCESS] Rust binary found!

REM Start Rust backend
echo [INFO] Starting Rust backend...
cd rust-core
start /B "Rust Backend" target\release\rust-core.exe
cd ..

REM Wait for backend to start
echo [INFO] Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Test if backend is running
curl -s http://127.0.0.1:8080/health >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend failed to start or is not responding
    pause
    exit /b 1
)

echo [SUCCESS] Backend started successfully!
echo.
echo [INFO] System is running at: http://127.0.0.1:8080
echo [INFO] Health check: http://127.0.0.1:8080/health
echo [INFO] Metrics: http://127.0.0.1:8080/metrics
echo.
echo [WARNING] Press Ctrl+C to stop the backend
echo.

REM Run quick test
echo [INFO] Running quick test...
python quick_test.py

echo.
echo [INFO] Backend is still running. Press Ctrl+C to stop...
pause

REM Cleanup
echo [INFO] Stopping backend...
taskkill /F /IM rust-core.exe >nul 2>&1
echo [SUCCESS] Backend stopped!
