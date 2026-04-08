#!/bin/bash
# Simple Start Script for Low-Latency AI Agent Platform
# Works around file lock issues

set -e

echo "=========================================="
echo "Low-Latency AI Agent Platform"
echo "Simple Start Script"
echo "=========================================="

# Check if Rust binary exists
if [ ! -f "rust-core/target/release/rust-core" ]; then
    echo "[ERROR] Rust binary not found. Building first..."
    cd rust-core
    
    # Kill any existing Rust processes
    echo "[INFO] Killing existing Rust processes..."
    pkill -f rustc || true
    pkill -f cargo || true
    sleep 2
    
    # Clean and build
    echo "[INFO] Building Rust backend..."
    cargo clean
    cargo build --release
    
    cd ..
fi

echo "[SUCCESS] Rust binary found!"

# Start Rust backend
echo "[INFO] Starting Rust backend..."
cd rust-core
./target/release/rust-core &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "[INFO] Waiting for backend to start..."
sleep 5

# Test if backend is running
if curl -s http://127.0.0.1:8080/health > /dev/null; then
    echo "[SUCCESS] Backend started successfully! (PID: $BACKEND_PID)"
else
    echo "[ERROR] Backend failed to start or is not responding"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "[INFO] System is running at: http://127.0.0.1:8080"
echo "[INFO] Health check: http://127.0.0.1:8080/health"
echo "[INFO] Metrics: http://127.0.0.1:8080/metrics"
echo ""

# Run quick test
echo "[INFO] Running quick test..."
python3 quick_test.py || python quick_test.py

echo ""
echo "[INFO] Backend is still running. Press Ctrl+C to stop..."
echo ""

# Wait for user interrupt
trap 'echo "[INFO] Stopping backend..."; kill $BACKEND_PID 2>/dev/null || true; echo "[SUCCESS] Backend stopped!"; exit 0' INT

# Keep script running
wait $BACKEND_PID
