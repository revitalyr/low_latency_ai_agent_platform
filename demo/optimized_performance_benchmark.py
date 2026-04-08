#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import json
import uuid
import os
from typing import Dict, List, Any

# Optimized Python implementations for fair comparison
class OptimizedPythonTools:
    @staticmethod
    async def optimized_heavy_computation(iterations: int = 100000) -> Dict[str, Any]:
        """Optimized heavy computation matching Rust optimizations"""
        start = time.perf_counter()
        
        # Optimized computation using chunks
        CHUNK_SIZE = 1024
        chunks = (iterations + CHUNK_SIZE - 1) // CHUNK_SIZE
        
        result = 0
        for chunk in range(chunks):
            start_idx = chunk * CHUNK_SIZE
            end_idx = min(start_idx + CHUNK_SIZE, iterations)
            
            chunk_result = 0
            for i in range(start_idx, end_idx):
                # Optimized arithmetic without float conversions
                chunk_result = (chunk_result + (i * i) % 1000) % 1000000
                # Fixed-point arithmetic
                chunk_result = (chunk_result * 11 // 10) % 1000000
            
            result = (result + chunk_result) % 1000000
        
        # Optimized string processing
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        char_count = sum(1 for c in text if 'a' <= c <= 'z') * 20
        
        exec_time = (time.perf_counter() - start) * 1000
        return {
            "result": {
                "computation_result": result,
                "char_count": char_count,
                "iterations": iterations,
                "optimized": True
            },
            "execution_time_ms": exec_time
        }
    
    @staticmethod
    async def optimized_heavy_file_processing(size_mb: int = 5) -> Dict[str, Any]:
        """Optimized file processing matching Rust optimizations"""
        start = time.perf_counter()
        
        target_size = size_mb * 1024 * 1024
        chunk = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        
        # Pre-allocate list for better performance
        chunks = []
        total_len = 0
        
        while total_len + len(chunk) + 1 <= target_size:
            chunks.append(chunk + '\n')
            total_len += len(chunk) + 1
        
        # Final chunk
        remaining = target_size - total_len
        if remaining > 0:
            chunks.append(chunk[:remaining])
            total_len += remaining
        
        content = ''.join(chunks)
        
        # Optimized file I/O
        filename = f"optimized_heavy_test_{size_mb}mb.txt"
        
        # Buffered write
        with open(filename, 'w', buffering=8192) as f:
            f.write(content)
        
        # Optimized reading
        with open(filename, 'r', buffering=8192) as f:
            file_content = f.read()
        
        # Optimized content processing using bytes
        byte_content = file_content.encode()
        word_count = 0
        char_count = len(byte_content)
        line_count = 0
        in_word = False
        
        for byte in byte_content:
            if byte in b' \t\r\n':
                if in_word:
                    word_count += 1
                    in_word = False
                if byte == ord('\n'):
                    line_count += 1
            else:
                in_word = True
        
        if in_word:
            word_count += 1
        
        # Cleanup
        os.remove(filename)
        
        exec_time = (time.perf_counter() - start) * 1000
        return {
            "result": {
                "size_mb": size_mb,
                "word_count": word_count,
                "char_count": char_count,
                "line_count": line_count,
                "optimized": True
            },
            "execution_time_ms": exec_time
        }
    
    @staticmethod
    async def optimized_concurrent_operations(count: int = 20) -> Dict[str, Any]:
        """Optimized concurrent operations"""
        start = time.perf_counter()
        
        tasks = []
        for i in range(count):
            task = OptimizedPythonTools.optimized_heavy_computation(10000)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        total_result = sum(r["result"]["computation_result"] for r in results)
        
        exec_time = (time.perf_counter() - start) * 1000
        return {
            "result": {
                "concurrent_operations": count,
                "total_result": total_result,
                "average_result": total_result / count,
                "optimized": True
            },
            "execution_time_ms": exec_time
        }

async def test_optimized_rust_tools():
    """Test optimized Rust tools"""
    print("=== Optimized Rust Tools Test ===")
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        # Test optimized heavy computation
        print("Testing optimized heavy computation...")
        tool_request = {
            "id": str(uuid.uuid4()),
            "tool_type": "Compute",
            "parameters": {
                "operation": "heavy_computation",
                "iterations": 100000
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        task = {
            "id": str(uuid.uuid4()),
            "prompt": "Optimized heavy computation test",
            "tools": [tool_request],
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        start = time.perf_counter()
        async with session.post('http://localhost:8080/execute', json=task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_time = (time.perf_counter() - start) * 1000
                
                print(f"   Result: {result['tool_responses'][0]['result']['computation_result']}")
                print(f"   Tool time: {result['tool_responses'][0]['execution_time_ms']:.2f}ms")
                print(f"   Total time: {total_time:.2f}ms")
                
                results.append(("optimized_heavy_computation", {
                    "tool_time": result['tool_responses'][0]['execution_time_ms'],
                    "total_time": total_time,
                    "result": result['tool_responses'][0]['result']
                }))
            else:
                print(f"   Error: {resp.status}")
        
        # Test optimized heavy file processing
        print("\nTesting optimized heavy file processing...")
        file_tool = {
            "id": str(uuid.uuid4()),
            "tool_type": "File",
            "parameters": {
                "action": "heavy_processing",
                "size_mb": 5
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        file_task = {
            "id": str(uuid.uuid4()),
            "prompt": "Optimized heavy file processing test",
            "tools": [file_tool],
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        start = time.perf_counter()
        async with session.post('http://localhost:8080/execute', json=file_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_time = (time.perf_counter() - start) * 1000
                
                print(f"   Result: {result['tool_responses'][0]['result']['size_mb']}MB processed")
                print(f"   Tool time: {result['tool_responses'][0]['execution_time_ms']:.2f}ms")
                print(f"   Total time: {total_time:.2f}ms")
                
                results.append(("optimized_heavy_file", {
                    "tool_time": result['tool_responses'][0]['execution_time_ms'],
                    "total_time": total_time,
                    "result": result['tool_responses'][0]['result']
                }))
            else:
                print(f"   Error: {resp.status}")
        
        # Test optimized concurrent operations
        print("\nTesting optimized concurrent operations...")
        concurrent_tools = []
        for i in range(10):
            tool = {
                "id": str(uuid.uuid4()),
                "tool_type": "Compute",
                "parameters": {
                    "operation": "concurrent_computation",
                    "task_id": i
                },
                "timestamp": "2024-01-01T00:00:00Z"
            }
            concurrent_tools.append(tool)
        
        concurrent_task = {
            "id": str(uuid.uuid4()),
            "prompt": "Optimized concurrent operations test",
            "tools": concurrent_tools,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        start = time.perf_counter()
        async with session.post('http://localhost:8080/execute', json=concurrent_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                total_time = (time.perf_counter() - start) * 1000
                
                print(f"   Result: {len(result['tool_responses'])} concurrent operations")
                print(f"   Total time: {total_time:.2f}ms")
                
                results.append(("optimized_concurrent", {
                    "tool_time": sum(r['execution_time_ms'] for r in result['tool_responses']),
                    "total_time": total_time,
                    "result": {"operations": len(result['tool_responses'])}
                }))
            else:
                print(f"   Error: {resp.status}")
    
    return results

async def benchmark_optimized_python():
    """Benchmark optimized Python implementations"""
    print("\n=== Optimized Python Benchmark ===")
    
    results = []
    
    # Optimized heavy computation
    print("Running optimized heavy computation...")
    comp_result = await OptimizedPythonTools.optimized_heavy_computation(100000)
    results.append(("optimized_heavy_computation", comp_result))
    print(f"   Time: {comp_result['execution_time_ms']:.2f}ms")
    
    # Optimized file processing
    print("Running optimized file processing...")
    file_result = await OptimizedPythonTools.optimized_heavy_file_processing(5)
    results.append(("optimized_heavy_file", file_result))
    print(f"   Time: {file_result['execution_time_ms']:.2f}ms")
    
    # Optimized concurrent operations
    print("Running optimized concurrent operations...")
    concurrent_result = await OptimizedPythonTools.optimized_concurrent_operations(20)
    results.append(("optimized_concurrent", concurrent_result))
    print(f"   Time: {concurrent_result['execution_time_ms']:.2f}ms")
    
    total_python_time = sum(r[1]['execution_time_ms'] for r in results)
    print(f"\nTotal Python time: {total_python_time:.2f}ms")
    
    return results, total_python_time

async def comprehensive_optimized_benchmark():
    """Comprehensive benchmark of optimized implementations"""
    print("=== Comprehensive Optimized Benchmark ===")
    print("Testing optimized Rust vs optimized Python implementations")
    
    # Test optimized Python
    python_results, python_time = await benchmark_optimized_python()
    
    # Test optimized Rust
    rust_results = await test_optimized_rust_tools()
    
    # Analysis
    print("\n" + "=" * 60)
    print("OPTIMIZED PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    print(f"\nOptimized Python Results:")
    for op, result in python_results:
        print(f"   {op}: {result['execution_time_ms']:.2f}ms")
    
    print(f"\nOptimized Rust Results:")
    for op, result in rust_results:
        print(f"   {op}: {result['tool_time']:.2f}ms (tool), {result['total_time']:.2f}ms (total)")
    
    # Performance comparison
    print(f"\nPerformance Comparison:")
    
    rust_tool_time = sum(r[1]['tool_time'] for r in rust_results)
    rust_total_time = sum(r[1]['total_time'] for r in rust_results)
    
    print(f"   Python total: {python_time:.2f}ms")
    print(f"   Rust tool time: {rust_tool_time:.2f}ms")
    print(f"   Rust total time: {rust_total_time:.2f}ms")
    
    if rust_tool_time > 0:
        tool_speedup = python_time / rust_tool_time
        print(f"   Rust tool speedup: {tool_speedup:.1f}x faster")
    
    if rust_total_time > 0:
        total_speedup = python_time / rust_total_time
        print(f"   Rust total speedup: {total_speedup:.1f}x faster")
    
    # Detailed comparison
    print(f"\nDetailed Comparison:")
    for i, (op, py_result) in enumerate(python_results):
        if i < len(rust_results):
            rust_op, rust_result = rust_results[i]
            py_time = py_result['execution_time_ms']
            rust_time = rust_result['tool_time']
            
            if rust_time > 0:
                speedup = py_time / rust_time
                print(f"   {op}: {speedup:.1f}x faster")
    
    print(f"\nOptimization Impact:")
    print(f"   Both implementations now use:")
    print(f"   - Chunked processing for better cache performance")
    print(f"   - Buffered I/O operations")
    print(f"   - Optimized string processing")
    print(f"   - Memory-efficient algorithms")
    
    print(f"\nRecommendations:")
    if rust_tool_time < python_time:
        print(f"   Rust still superior for production workloads")
        print(f"   Use Rust for high-throughput systems")
    else:
        print(f"   Python optimization closed the gap")
        print(f"   Consider network overhead in distributed systems")

async def main():
    """Run optimized benchmark"""
    print("=== Optimized Performance Benchmark ===")
    print("Testing optimized Rust vs optimized Python implementations")
    
    try:
        await comprehensive_optimized_benchmark()
        print(f"\nOptimized benchmark completed!")
    except Exception as e:
        print(f"\nBenchmark error: {e}")
        print("Make sure Rust backend is running on localhost:8080")

if __name__ == "__main__":
    asyncio.run(main())
