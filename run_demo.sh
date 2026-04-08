#!/bin/bash

echo "========================================"
echo "Low-Latency AI Agent Platform Demo"
echo "========================================"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# [1/5] Check dependencies
echo "[1/5] Checking dependencies..."
if ! command_exists cargo; then
    echo "❌ Rust not found. Please install Rust first."
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

# [2/5] Build Rust backend
echo "[2/5] Building Rust backend..."
cd "$(dirname "$0")/rust-core"
if [ ! -f "target/release/rust-core" ]; then
    cargo build --release
    if [ $? -ne 0 ]; then
        echo "❌ Build failed!"
        exit 1
    fi
fi

# [3/5] Start Rust backend in background
echo "[3/5] Starting Rust backend..."
cargo run --release &
RUST_PID=$!

# Wait for server to start
echo "[4/5] Waiting for server to start..."
sleep 3

# Check if server is responding
for i in {1..10}; do
    if curl -s http://127.0.0.1:8080/health >/dev/null 2>&1; then
        echo "✅ Server is running!"
        break
    fi
    sleep 1
done

if ! curl -s http://127.0.0.1:8080/health >/dev/null 2>&1; then
    echo "❌ Server failed to start!"
    kill $RUST_PID 2>/dev/null
    exit 1
fi

# [5/5] Run demo and benchmark
echo "[5/5] Running demo and benchmark..."
cd "$(dirname "$0")"

# Run demo
echo "🚀 Running interactive demo..."
python3 demo/run_demo.py

echo ""
echo "📊 Running performance benchmark..."
python3 demo/performance_benchmark.py

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $RUST_PID 2>/dev/null

echo ""
echo "========================================"
echo "🎉 Demo completed successfully!"
echo "========================================"
