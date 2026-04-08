@echo off
echo ========================================
echo Low-Latency AI Agent Platform Demo
echo ========================================
echo.

echo [1/5] Checking Rust backend...
cd /d "%~dp0"rust-core
if not exist "target\release\rust-core.exe" (
    echo Building Rust backend...
    cargo build --release
    if errorlevel 1 (
        echo ❌ Build failed!
        pause
        exit /b 1
    )
)

echo [2/5] Starting Rust backend...
echo Starting server on http://127.0.0.1:8080
start /B cargo run --release
timeout /t 3 >nul

echo [3/5] Waiting for server to start...
timeout /t 5 >nul

echo [4/5] Running demo...
cd /d "%~dp0"
python demo\run_demo.py

echo [5/5] Running performance benchmark...
python demo\performance_benchmark.py

echo.
echo ========================================
echo 🎉 Demo completed successfully!
echo ========================================
pause
