#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import json
import uuid
import os
from typing import Dict, List, Any

# Python implementation of the same tools
class PythonComputeTool:
    @staticmethod
    async def execute(operation: str, **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        
        if operation == "add":
            a = kwargs.get("a", 0)
            b = kwargs.get("b", 0)
            result = a + b
        elif operation == "multiply":
            a = kwargs.get("a", 0)
            b = kwargs.get("b", 0)
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
        
        execution_time = (time.time() - start_time) * 1000
        return {
            "result": result,
            "execution_time_ms": int(execution_time)
        }

class PythonFileTool:
    @staticmethod
    async def execute(action: str, path: str, content: str = None) -> Dict[str, Any]:
        start_time = time.time()
        
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
        
        execution_time = (time.time() - start_time) * 1000
        return {
            "result": result,
            "execution_time_ms": int(execution_time)
        }

class PythonHttpTool:
    @staticmethod
    async def execute(method: str, url: str, body: Dict = None) -> Dict[str, Any]:
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(url) as resp:
                    response_text = await resp.text()
                    status = resp.status
            elif method.upper() == "POST":
                async with session.post(url, json=body) as resp:
                    response_text = await resp.text()
                    status = resp.status
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        
        result = {
            "status": status,
            "response": response_text
        }
        
        execution_time = (time.time() - start_time) * 1000
        return {
            "result": result,
            "execution_time_ms": int(execution_time)
        }

async def python_compute_benchmark():
    """Python-only compute operations"""
    print("=== Python Compute Benchmark ===")
    
    operations = [
        ("add", {"a": 25, "b": 15}),
        ("multiply", {"a": 10, "b": 5}),
        ("percentage_change", {"old": 100, "new": 115})
    ]
    
    start_time = time.time()
    results = []
    
    for op, params in operations:
        result = await PythonComputeTool.execute(op, **params)
        results.append(result)
        print(f"   {op}: {result['result']} ({result['execution_time_ms']}ms)")
    
    total_time = (time.time() - start_time) * 1000
    print(f"📊 Total Python compute time: {total_time:.2f}ms")
    return total_time, results

async def python_file_benchmark():
    """Python-only file operations"""
    print("\n=== Python File Benchmark ===")
    
    # Write operation
    write_result = await PythonFileTool.execute(
        "write", 
        "python_demo_output.txt",
        "Hello from Python implementation!"
    )
    print(f"   Write: {write_result['result']} ({write_result['execution_time_ms']}ms)")
    
    # Read operation
    read_result = await PythonFileTool.execute("read", "python_demo_output.txt")
    print(f"   Read: {read_result['result']} ({read_result['execution_time_ms']}ms)")
    
    total_time = write_result['execution_time_ms'] + read_result['execution_time_ms']
    print(f"📊 Total Python file time: {total_time:.2f}ms")
    return total_time, [write_result, read_result]

async def rust_benchmark():
    """Rust backend benchmark"""
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
        start_time = time.time()
        
        async with session.post('http://localhost:8080/execute', json=compute_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_compute_time = (time.time() - start_time) * 1000
                
                print("   Rust compute results:")
                for tool_resp in result['tool_responses']:
                    print(f"   {tool_resp['result']} ({tool_resp['execution_time_ms']}ms)")
                
                print(f"📊 Total Rust compute time: {total_compute_time:.2f}ms")
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
                "content": "Hello from Rust backend!"
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
        start_time = time.time()
        
        async with session.post('http://localhost:8080/execute', json=file_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_file_time = (time.time() - start_time) * 1000
                
                print("   Rust file results:")
                for tool_resp in result['tool_responses']:
                    print(f"   {tool_resp['result']} ({tool_resp['execution_time_ms']}ms)")
                
                print(f"📊 Total Rust file time: {total_file_time:.2f}ms")
                file_time = total_file_time
                file_results = result['tool_responses']
            else:
                print(f"❌ Rust file error: {resp.status}")
                file_time = 0
                file_results = []
    
    return compute_time, compute_results, file_time, file_results

async def comprehensive_benchmark():
    """Run comprehensive benchmark comparing Python vs Rust"""
    print("🏁 Comprehensive Python vs Rust Benchmark")
    print("=" * 60)
    
    # Python benchmarks
    python_compute_time, python_compute_results = await python_compute_benchmark()
    python_file_time, python_file_results = await python_file_benchmark()
    
    # Rust benchmarks
    rust_compute_time, rust_compute_results, rust_file_time, rust_file_results = await rust_benchmark()
    
    # Analysis
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE COMPARISON")
    print("=" * 60)
    
    print("\n🧮 Compute Operations:")
    print(f"   Python: {python_compute_time:.2f}ms")
    print(f"   Rust:   {rust_compute_time:.2f}ms")
    
    if rust_compute_time > 0:
        compute_improvement = ((python_compute_time - rust_compute_time) / python_compute_time) * 100
        speedup = python_compute_time / rust_compute_time
        print(f"   Improvement: {compute_improvement:.1f}% faster ({speedup:.1f}x speedup)")
    
    print("\n📁 File Operations:")
    print(f"   Python: {python_file_time:.2f}ms")
    print(f"   Rust:   {rust_file_time:.2f}ms")
    
    if rust_file_time > 0:
        file_improvement = ((python_file_time - rust_file_time) / python_file_time) * 100
        speedup = python_file_time / rust_file_time
        print(f"   Improvement: {file_improvement:.1f}% faster ({speedup:.1f}x speedup)")
    
    # Overall comparison
    total_python = python_compute_time + python_file_time
    total_rust = rust_compute_time + rust_file_time
    
    print(f"\n🎯 Overall Performance:")
    print(f"   Python Total: {total_python:.2f}ms")
    print(f"   Rust Total:   {total_rust:.2f}ms")
    
    if total_rust > 0:
        overall_improvement = ((total_python - total_rust) / total_python) * 100
        overall_speedup = total_python / total_rust
        print(f"   Overall Improvement: {overall_improvement:.1f}% faster ({overall_speedup:.1f}x speedup)")
    
    # Detailed breakdown
    print(f"\n📈 Detailed Breakdown:")
    print("   Compute Operations:")
    print(f"     Python add: {python_compute_results[0]['execution_time_ms']}ms")
    print(f"     Python multiply: {python_compute_results[1]['execution_time_ms']}ms")
    print(f"     Python percentage: {python_compute_results[2]['execution_time_ms']}ms")
    
    if rust_compute_results:
        print(f"     Rust add: {rust_compute_results[0]['execution_time_ms']}ms")
        print(f"     Rust multiply: {rust_compute_results[1]['execution_time_ms']}ms")
        print(f"     Rust percentage: {rust_compute_results[2]['execution_time_ms']}ms")
    
    print("   File Operations:")
    print(f"     Python write: {python_file_results[0]['execution_time_ms']}ms")
    print(f"     Python read: {python_file_results[1]['execution_time_ms']}ms")
    
    if rust_file_results:
        print(f"     Rust write: {rust_file_results[0]['execution_time_ms']}ms")
        print(f"     Rust read: {rust_file_results[1]['execution_time_ms']}ms")
    
    # Cleanup
    for file in ["python_demo_output.txt", "rust_demo_output.txt"]:
        if os.path.exists(file):
            os.remove(file)
    
    print(f"\n🎉 Benchmark completed!")

async def main():
    try:
        await comprehensive_benchmark()
    except Exception as e:
        print(f"\n❌ Benchmark error: {e}")
        print("Make sure Rust backend is running on localhost:8080")

if __name__ == "__main__":
    asyncio.run(main())
