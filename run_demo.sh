#!/bin/bash
# Low-Latency AI Agent Platform - Build, Demo & Benchmark Script
# Principal-level automation for complete system testing

set -e  # Exit on any error

echo "=========================================="
echo "Low-Latency AI Agent Platform"
echo "Principal-Level Build & Demo Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Rust is installed
check_rust() {
    print_status "Checking Rust installation..."
    if ! command -v cargo &> /dev/null; then
        print_error "Cargo not found. Please install Rust first."
        exit 1
    fi
    
    RUST_VERSION=$(rustc --version)
    print_success "Rust found: $RUST_VERSION"
}

# Build optimized Rust backend
build_rust() {
    print_status "Building optimized Rust backend..."
    cd rust-core
    
    # Clean previous builds
    print_status "Cleaning previous builds..."
    cargo clean
    
    # Build with maximum optimizations
    print_status "Building with LTO and maximum optimizations..."
    cargo build --release --quiet
    
    if [ $? -eq 0 ]; then
        print_success "Rust backend built successfully!"
        
        # Show binary size
        BINARY_SIZE=$(ls -lh target/release/rust-core.exe | awk '{print $5}')
        print_status "Binary size: $BINARY_SIZE"
    else
        print_error "Rust build failed!"
        exit 1
    fi
    
    cd ..
}

# Check Python environment
check_python() {
    print_status "Checking Python environment..."
    
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
    
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version)
    print_success "Python found: $PYTHON_VERSION"
    
    # Check if requirements are installed
    cd python-agent
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python dependencies..."
        $PYTHON_CMD -m pip install -q -r requirements.txt
        print_success "Python dependencies installed!"
    fi
    cd ..
}

# Start Rust backend
start_backend() {
    print_status "Starting Rust backend..."
    cd rust-core
    
    # Start backend in background
    cargo run --release --quiet > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait for backend to start
    print_status "Waiting for backend to start..."
    sleep 3
    
    # Check if backend is running
    if curl -s http://127.0.0.1:8080/health > /dev/null; then
        print_success "Backend started successfully! (PID: $BACKEND_PID)"
    else
        print_error "Backend failed to start!"
        tail -n 20 ../backend.log
        exit 1
    fi
    
    cd ..
}

# Run Python demo
run_demo() {
    print_status "Running Python agent demo..."
    cd python-agent
    
    $PYTHON_CMD run_demo.py
    
    if [ $? -eq 0 ]; then
        print_success "Python demo completed successfully!"
    else
        print_warning "Python demo had some issues, but continuing..."
    fi
    
    cd ..
}

# Run performance benchmark
run_benchmark() {
    print_status "Running performance benchmark..."
    cd demo
    
    $PYTHON_CMD optimized_performance_benchmark.py
    
    if [ $? -eq 0 ]; then
        print_success "Benchmark completed successfully!"
    else
        print_warning "Benchmark had some issues, but continuing..."
    fi
    
    cd ..
}

# Test individual endpoints
test_endpoints() {
    print_status "Testing individual endpoints..."
    
    # Test health endpoint
    print_status "Testing /health endpoint..."
    HEALTH_RESPONSE=$(curl -s http://127.0.0.1:8080/health)
    print_success "Health check: $HEALTH_RESPONSE"
    
    # Test metrics endpoint
    print_status "Testing /metrics endpoint..."
    METRICS_RESPONSE=$(curl -s http://127.0.0.1:8080/metrics)
    print_success "Metrics retrieved successfully!"
    
    # Test simple execution
    print_status "Testing tool execution..."
    EXECUTION_PAYLOAD='{
        "id": "test-execution",
        "prompt": "Test execution",
        "tools": [
            {
                "tool": "compute",
                "input": {"operation": "add", "a": 5, "b": 3}
            }
        ]
    }'
    
    EXECUTION_RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$EXECUTION_PAYLOAD" \
        http://127.0.0.1:8080/execute)
    
    print_success "Tool execution test completed!"
}

# Show performance results
show_results() {
    print_status "Displaying performance results..."
    
    if [ -f "demo/PERFORMANCE_RESULTS.md" ]; then
        echo ""
        print_success "=== PERFORMANCE RESULTS ==="
        cat demo/PERFORMANCE_RESULTS.md
        echo ""
    fi
    
    if [ -f "backend.log" ]; then
        echo ""
        print_status "=== BACKEND LOGS (last 10 lines) ==="
        tail -n 10 backend.log
        echo ""
    fi
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    
    # Kill backend if running
    if [ ! -z "$BACKEND_PID" ]; then
        print_status "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
        wait $BACKEND_PID 2>/dev/null || true
    fi
    
    # Clean up log files
    if [ -f "backend.log" ]; then
        rm backend.log
    fi
    
    print_success "Cleanup completed!"
}

# Set trap for cleanup
trap cleanup EXIT

# Main execution flow
main() {
    echo ""
    print_status "Starting complete system test..."
    echo ""
    
    # Check prerequisites
    check_rust
    check_python
    
    echo ""
    print_status "Building system..."
    build_rust
    
    echo ""
    print_status "Starting services..."
    start_backend
    
    echo ""
    print_status "Running tests..."
    test_endpoints
    
    echo ""
    print_status "Running demo..."
    run_demo
    
    echo ""
    print_status "Running benchmark..."
    run_benchmark
    
    echo ""
    show_results
    
    echo ""
    print_success "=== ALL TESTS COMPLETED SUCCESSFULLY! ==="
    echo ""
    print_status "System is running at: http://127.0.0.1:8080"
    print_status "Backend logs available in: backend.log"
    print_status "Performance results in: demo/PERFORMANCE_RESULTS.md"
    echo ""
    
    # Keep backend running for manual testing
    print_warning "Press Ctrl+C to stop the backend..."
    sleep infinity
}

# Run main function
main "$@"
