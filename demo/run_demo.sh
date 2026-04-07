#!/bin/bash

# Low-Latency AI Agent Platform - Quick Start Script

echo "Starting Low-Latency AI Agent Platform..."
echo "=========================================="

# Check if Rust backend is running
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "Starting Rust backend..."
    cd rust-core
    cargo run &
    RUST_PID=$!
    echo "Rust backend started with PID: $RUST_PID"
    
    # Wait for backend to be ready
    echo "Waiting for backend to be ready..."
    while ! curl -s http://localhost:8080/health > /dev/null; do
        sleep 1
    done
    echo "Backend is ready!"
    cd ..
else
    echo "Rust backend is already running"
fi

# Check Python environment
if [ ! -d "python-agent/venv" ]; then
    echo "Setting up Python environment..."
    cd python-agent
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo "Python environment setup complete"
fi

# Run demo
echo "Running demo..."
cd demo
python run_demo.py

echo "Demo completed!"

# Cleanup (optional)
read -p "Stop Rust backend? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -z "$RUST_PID" ]; then
        kill $RUST_PID
        echo "Rust backend stopped"
    fi
fi
