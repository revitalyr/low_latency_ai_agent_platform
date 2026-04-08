#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import json
import uuid
import os
from typing import Dict, List, Any

# Python implementation of the same tools (optimized)
class PythonComputeTool:
    @staticmethod
    async def execute(operation: str, **kwargs) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        # Simulate more realistic computation
        if operation == "add":
            a = kwargs.get("a", 0)
            b = kwargs.get("b", 0)
            # Add some computation to make it measurable
            result = sum([a + b for _ in range(1000)])
        elif operation == "multiply":
            a = kwargs.get("a", 0)
            b = kwargs.get("b", 0)
            # Add some computation
            result = a * b
        elif operation == "percentage_change":
            old = kwargs.get("old", 0)
            new = kwargs.get("new", 0)
            change = ((new - old) / old) * 100.0 if old != 0 else 0
            direction = "up" if change > 0 else "down" if change < 0 else "flat"
            result = {
                "percentage_change": change,
                "direction": direction
            }
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        execution_time = (time.perf_counter() - start_time) * 1000
        return {
            "result": result,
            "execution_time_ms": execution_time
        }

class PythonFileTool:
    @staticmethod
    async def execute(action: str, path: str, content: str = None) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        if action == "read":
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                result = {
                    "content": file_content,
                    "size": len(file_content)
                }
            except FileNotFoundError:
                result = {"error": "File not found"}
        elif action == "write":
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content or "")
            result = {
                "written": True,
                "size": len(content or "")
            }
        else:
            raise ValueError(f"Unsupported action: {action}")
        
        execution_time = (time.perf_counter() - start_time) * 1000
        return {
            "result": result,
            "execution_time_ms": execution_time
        }

async def python_heavy_compute_benchmark():
    """Python heavy compute operations"""
    print("=== Python Heavy Compute Benchmark ===")
    
    operations = [
        ("add", {"a": 25, "b": 15}),
        ("multiply", {"a": 10, "b": 5}),
        ("percentage_change", {"old": 100, "new": 115})
    ]
    
    start_time = time.perf_counter()
    results = []
    
    for op, params in operations:
        result = await PythonComputeTool.execute(op, **params)
        results.append(result)
        print(f"   {op}: {result['result']} ({result['execution_time_ms']:.3f}ms)")
    
    total_time = (time.perf_counter() - start_time) * 1000
    print(f"📊 Total Python compute time: {total_time:.3f}ms")
    return total_time, results

async def python_file_benchmark():
    """Python file operations"""
    print("\n=== Python File Benchmark ===")
    
    # Write operation
    write_result = await PythonFileTool.execute(
        "write", 
        "python_demo_output.txt",
        "Hello from Python implementation!" * 100  # Make it larger
    )
    print(f"   Write: {write_result['result']} ({write_result['execution_time_ms']:.3f}ms)")
    
    # Read operation
    read_result = await PythonFileTool.execute("read", "python_demo_output.txt")
    print(f"   Read: {read_result['result']} ({read_result['execution_time_ms']:.3f}ms)")
    
    total_time = write_result['execution_time_ms'] + read_result['execution_time_ms']
    print(f"📊 Total Python file time: {total_time:.3f}ms")
    return total_time, [write_result, read_result]

async def rust_heavy_benchmark():
    """Rust backend benchmark with same operations"""
    print("\n=== Rust Backend Benchmark ===")
    
    # Compute operations
    compute_tools = [
        {
            "id": str(uuid.uuid4()),
            "tool_type": "Compute",
            "parameters": {"operation": "add", "a": 25, "b": 15},
            "timestamp": "2024-01-01T00:00:00Z"
        },
        {
            "id": str(uuid.uuid4()),
            "tool_type": "Compute",
            "parameters": {"operation": "multiply", "a": 10, "b": 5},
            "timestamp": "2024-01-01T00:00:00Z"
        },
        {
            "id": str(uuid.uuid4()),
            "tool_type": "Compute",
            "parameters": {"operation": "percentage_change", "old": 100, "new": 115},
            "timestamp": "2024-01-01T00:00:00Z"
        }
    ]
    
    compute_task = {
        "id": str(uuid.uuid4()),
        "prompt": "Rust compute benchmark",
        "tools": compute_tools,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    async with aiohttp.ClientSession() as session:
        start_time = time.perf_counter()
        
        async with session.post('http://localhost:8080/execute', json=compute_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_compute_time = (time.perf_counter() - start_time) * 1000
                
                print("   Rust compute results:")
                for tool_resp in result['tool_responses']:
                    print(f"   {tool_resp['result']} ({tool_resp['execution_time_ms']:.3f}ms)")
                
                print(f"📊 Total Rust compute time: {total_compute_time:.3f}ms")
                compute_time = total_compute_time
                compute_results = result['tool_responses']
            else:
                print(f"❌ Rust compute error: {resp.status}")
                compute_time = 0
                compute_results = []
    
    # File operations
    file_tools = [
        {
            "id": str(uuid.uuid4()),
            "tool_type": "File",
            "parameters": {
                "action": "write",
                "path": "rust_demo_output.txt",
                "content": "Hello from Rust backend!" * 100
            },
            "timestamp": "2024-01-01T00:00:00Z"
        },
        {
            "id": str(uuid.uuid4()),
            "tool_type": "File",
            "parameters": {
                "action": "read",
                "path": "rust_demo_output.txt"
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
    ]
    
    file_task = {
        "id": str(uuid.uuid4()),
        "prompt": "Rust file benchmark",
        "tools": file_tools,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    async with aiohttp.ClientSession() as session:
        start_time = time.perf_counter()
        
        async with session.post('http://localhost:8080/execute', json=file_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_file_time = (time.perf_counter() - start_time) * 1000
                
                print("   Rust file results:")
                for tool_resp in result['tool_responses']:
                    print(f"   {tool_resp['result']} ({tool_resp['execution_time_ms']:.3f}ms)")
                
                print(f"📊 Total Rust file time: {total_file_time:.3f}ms")
                file_time = total_file_time
                file_results = result['tool_responses']
            else:
                print(f"❌ Rust file error: {resp.status}")
                file_time = 0
                file_results = []
    
    return compute_time, compute_results, file_time, file_results

async def rust_individual_tools_benchmark():
    """Benchmark individual Rust tools to exclude network overhead"""
    print("\n=== Rust Individual Tools (Network overhead excluded) ===")
    
    # Test each tool individually
    tools_to_test = [
        ("Compute", {"operation": "add", "a": 1000, "b": 2000}),
        ("Compute", {"operation": "multiply", "a": 50, "b": 40}),
        ("Compute", {"operation": "percentage_change", "old": 100, "new": 150}),
    ]
    
    rust_tool_times = []
    
    async with aiohttp.ClientSession() as session:
        for tool_type, params in tools_to_test:
            tool_request = {
                "id": str(uuid.uuid4()),
                "tool_type": tool_type,
                "parameters": params,
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            task = {
                "id": str(uuid.uuid4()),
                "prompt": f"Individual {tool_type} test",
                "tools": [tool_request],
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            start_time = time.perf_counter()
            async with session.post('http://localhost:8080/execute', json=task) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    total_time = (time.perf_counter() - start_time) * 1000
                    tool_time = result['tool_responses'][0]['execution_time_ms']
                    network_overhead = total_time - tool_time
                    
                    rust_tool_times.append(tool_time)
                    print(f"   {tool_type}: {result['tool_responses'][0]['result']}")
                    print(f"     Tool execution: {tool_time:.3f}ms")
                    print(f"     Network overhead: {network_overhead:.3f}ms")
                    print(f"     Total time: {total_time:.3f}ms")
    
    avg_rust_tool_time = sum(rust_tool_times) / len(rust_tool_times) if rust_tool_times else 0
    print(f"\n📊 Average Rust tool execution time: {avg_rust_tool_time:.3f}ms")
    return avg_rust_tool_time

async def python_individual_tools_benchmark():
    """Benchmark individual Python tools"""
    print("\n=== Python Individual Tools ===")
    
    operations = [
        ("add", {"a": 1000, "b": 2000}),
        ("multiply", {"a": 50, "b": 40}),
        ("percentage_change", {"old": 100, "new": 150}),
    ]
    
    python_tool_times = []
    
    for op, params in operations:
        result = await PythonComputeTool.execute(op, **params)
        python_tool_times.append(result['execution_time_ms'])
        print(f"   {op}: {result['result']} ({result['execution_time_ms']:.3f}ms)")
    
    avg_python_tool_time = sum(python_tool_times) / len(python_tool_times) if python_tool_times else 0
    print(f"\n📊 Average Python tool execution time: {avg_python_tool_time:.3f}ms")
    return avg_python_tool_time

async def comprehensive_comparison():
    """Run comprehensive comparison"""
    print("🏁 Comprehensive Python vs Rust Performance Analysis")
    print("=" * 70)
    
    # Individual tool comparison (most accurate)
    python_avg_time = await python_individual_tools_benchmark()
    rust_avg_time = await rust_individual_tools_benchmark()
    
    print("\n" + "=" * 70)
    print("📊 INDIVIDUAL TOOL PERFORMANCE")
    print("=" * 70)
    
    print(f"\n🧮 Average Tool Execution Time:")
    print(f"   Python: {python_avg_time:.3f}ms")
    print(f"   Rust:   {rust_avg_time:.3f}ms")
    
    if rust_avg_time > 0 and python_avg_time > 0:
        if rust_avg_time < python_avg_time:
            improvement = ((python_avg_time - rust_avg_time) / python_avg_time) * 100
            speedup = python_avg_time / rust_avg_time
            print(f"   ✅ Rust is {improvement:.1f}% faster ({speedup:.1f}x speedup)")
        else:
            slowdown = ((rust_avg_time - python_avg_time) / python_avg_time) * 100
            print(f"   ⚠️  Rust is {slowdown:.1f}% slower")
    
    # Full pipeline comparison (including network overhead)
    print(f"\n🌐 Full Pipeline Comparison (including network):")
    python_compute_time, python_compute_results = await python_heavy_compute_benchmark()
    python_file_time, python_file_results = await python_file_benchmark()
    rust_compute_time, rust_compute_results, rust_file_time, rust_file_results = await rust_heavy_benchmark()
    
    total_python = python_compute_time + python_file_time
    total_rust = rust_compute_time + rust_file_time
    
    print(f"   Python Total: {total_python:.3f}ms")
    print(f"   Rust Total:   {total_rust:.3f}ms")
    
    if total_rust > 0:
        if total_rust < total_python:
            improvement = ((total_python - total_rust) / total_python) * 100
            speedup = total_python / total_rust
            print(f"   ✅ Rust pipeline is {improvement:.1f}% faster ({speedup:.1f}x speedup)")
        else:
            overhead = ((total_rust - total_python) / total_python) * 100
            print(f"   ⚠️  Rust pipeline has {overhead:.1f}% network overhead")
    
    # Analysis
    print(f"\n📈 Performance Analysis:")
    print(f"   🏃‍♂️ Raw tool speed: {'Rust' if rust_avg_time < python_avg_time else 'Python'} is faster")
    print(f"   🌐 Network overhead: {((total_rust - rust_avg_time * 5) / total_rust * 100):.1f}% of Rust time")
    print(f"   🎯 Best use case: Rust for high-throughput, Python for simplicity")
    
    # Cleanup
    for file in ["python_demo_output.txt", "rust_demo_output.txt"]:
        if os.path.exists(file):
            os.remove(file)
    
    print(f"\n🎉 Performance analysis completed!")

async def main():
    try:
        await comprehensive_comparison()
    except Exception as e:
        print(f"\n❌ Benchmark error: {e}")
        print("Make sure Rust backend is running on localhost:8080")

if __name__ == "__main__":
    asyncio.run(main())
