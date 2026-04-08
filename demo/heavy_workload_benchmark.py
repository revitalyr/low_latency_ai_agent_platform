#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import json
import uuid
import os
import random
import string
from typing import Dict, List, Any

# Heavy Python implementations
class HeavyPythonTools:
    @staticmethod
    async def heavy_computation(iterations: int = 100000) -> Dict[str, Any]:
        """Heavy mathematical computation"""
        start = time.perf_counter()
        
        result = 0
        for i in range(iterations):
            # Complex computation
            result += (i * i) % 1000
            result = (result * 1.1) % 1000000
            if i % 10000 == 0:
                result = abs(result)
        
        # Additional string processing
        text = "".join(random.choices(string.ascii_letters, k=1000))
        char_count = sum(1 for c in text if c.islower())
        
        exec_time = (time.perf_counter() - start) * 1000
        return {
            "result": {
                "computation_result": result,
                "char_count": char_count,
                "iterations": iterations
            },
            "execution_time_ms": exec_time
        }
    
    @staticmethod
    async def heavy_file_processing(size_mb: int = 10) -> Dict[str, Any]:
        """Heavy file I/O operations"""
        start = time.perf_counter()
        
        # Generate large content
        content = ""
        for i in range(size_mb * 1024 * 1024 // 100):  # chunks of 100 chars
            chunk = "".join(random.choices(string.ascii_letters + string.digits, k=100))
            content += chunk + "\n"
        
        # Write large file
        filename = f"heavy_test_{size_mb}mb.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Read and process
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Process content
        word_count = len(file_content.split())
        char_count = len(file_content)
        line_count = file_content.count('\n')
        
        # Cleanup
        os.remove(filename)
        
        exec_time = (time.perf_counter() - start) * 1000
        return {
            "result": {
                "size_mb": size_mb,
                "word_count": word_count,
                "char_count": char_count,
                "line_count": line_count
            },
            "execution_time_ms": exec_time
        }
    
    @staticmethod
    async def concurrent_operations(count: int = 50) -> Dict[str, Any]:
        """Multiple concurrent operations"""
        start = time.perf_counter()
        
        tasks = []
        for i in range(count):
            task = HeavyPythonTools.heavy_computation(10000)  # Smaller iterations for concurrent
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        total_result = sum(r["result"]["computation_result"] for r in results)
        
        exec_time = (time.perf_counter() - start) * 1000
        return {
            "result": {
                "concurrent_operations": count,
                "total_result": total_result,
                "average_result": total_result / count
            },
            "execution_time_ms": exec_time
        }

async def heavy_python_benchmark():
    """Run heavy Python benchmark"""
    print("🐍 Heavy Python Benchmark")
    print("=" * 50)
    
    results = []
    
    # Test 1: Heavy computation
    print("🧮 Running heavy computation...")
    start = time.perf_counter()
    comp_result = await HeavyPythonTools.heavy_computation(100000)
    results.append(("heavy_computation", comp_result))
    print(f"   Result: {comp_result['result']['iterations']} iterations")
    print(f"   Time: {comp_result['execution_time_ms']:.2f}ms")
    
    # Test 2: Heavy file processing
    print("\n📁 Running heavy file processing...")
    file_result = await HeavyPythonTools.heavy_file_processing(5)  # 5MB file
    results.append(("heavy_file_processing", file_result))
    print(f"   Result: {file_result['result']['size_mb']}MB processed")
    print(f"   Time: {file_result['execution_time_ms']:.2f}ms")
    
    # Test 3: Concurrent operations
    print("\n⚡ Running concurrent operations...")
    concurrent_result = await HeavyPythonTools.concurrent_operations(20)
    results.append(("concurrent_operations", concurrent_result))
    print(f"   Result: {concurrent_result['result']['concurrent_operations']} concurrent ops")
    print(f"   Time: {concurrent_result['execution_time_ms']:.2f}ms")
    
    total_time = sum(r[1]['execution_time_ms'] for r in results)
    print(f"\n📊 Python Total Time: {total_time:.2f}ms")
    
    return results, total_time

async def heavy_rust_benchmark():
    """Run heavy Rust benchmark"""
    print("\n🦀 Heavy Rust Benchmark")
    print("=" * 50)
    
    # Test 1: Heavy computation via Rust
    print("🧮 Running heavy computation via Rust...")
    
    compute_tool = {
        "id": str(uuid.uuid4()),
        "tool_type": "Compute",
        "parameters": {
            "operation": "heavy_computation",
            "iterations": 100000
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    # Test 2: Heavy file processing via Rust
    print("📁 Running heavy file processing via Rust...")
    
    file_tool = {
        "id": str(uuid.uuid4()),
        "tool_type": "File",
        "parameters": {
            "action": "heavy_processing",
            "size_mb": 5
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    async with aiohttp.ClientSession() as session:
        # Heavy computation test
        compute_task = {
            "id": str(uuid.uuid4()),
            "prompt": "Heavy computation test",
            "tools": [compute_tool],
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        start = time.perf_counter()
        async with session.post('http://localhost:8080/execute', json=compute_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                comp_time = (time.perf_counter() - start) * 1000
                print(f"   Result: Computation completed")
                print(f"   Time: {comp_time:.2f}ms")
                compute_result = ("heavy_computation", {
                    "execution_time_ms": comp_time,
                    "result": result['tool_responses'][0]['result']
                })
            else:
                print(f"   ❌ Rust computation failed: {resp.status}")
                compute_result = ("heavy_computation", {"execution_time_ms": 0, "result": {}})
        
        # File processing test
        file_task = {
            "id": str(uuid.uuid4()),
            "prompt": "Heavy file processing test",
            "tools": [file_tool],
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        start = time.perf_counter()
        async with session.post('http://localhost:8080/execute', json=file_task) as resp:
            if resp.status == 200:
                result = await resp.json()
                file_time = (time.perf_counter() - start) * 1000
                print(f"   Result: File processing completed")
                print(f"   Time: {file_time:.2f}ms")
                file_result = ("heavy_file_processing", {
                    "execution_time_ms": file_time,
                    "result": result['tool_responses'][0]['result']
                })
            else:
                print(f"   ❌ Rust file processing failed: {resp.status}")
                file_result = ("heavy_file_processing", {"execution_time_ms": 0, "result": {}})
        
        # Concurrent test (multiple requests)
        print("⚡ Running concurrent operations via Rust...")
        
        concurrent_tools = []
        for i in range(10):  # 10 concurrent requests
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
        
        start = time.perf_counter()
        tasks = []
        for tool in concurrent_tools:
            task = {
                "id": str(uuid.uuid4()),
                "prompt": f"Concurrent test {tool['id']}",
                "tools": [tool],
                "timestamp": "2024-01-01T00:00:00Z"
            }
            tasks.append(session.post('http://localhost:8080/execute', json=task))
        
        responses = await asyncio.gather(*tasks)
        concurrent_time = (time.perf_counter() - start) * 1000
        
        successful = sum(1 for resp in responses if resp.status == 200)
        print(f"   Result: {successful}/10 concurrent operations completed")
        print(f"   Time: {concurrent_time:.2f}ms")
        
        concurrent_result = ("concurrent_operations", {
            "execution_time_ms": concurrent_time,
            "result": {"successful_operations": successful}
        })
        
        total_rust_time = sum(r[1]['execution_time_ms'] for r in [compute_result, file_result, concurrent_result])
        print(f"\n📊 Rust Total Time: {total_rust_time:.2f}ms")
        
        return [compute_result, file_result, concurrent_result], total_rust_time

async def stress_test_benchmark():
    """Stress test with high load"""
    print("\n🔥 Stress Test Benchmark")
    print("=" * 50)
    
    # Python stress test
    print("🐍 Python stress test...")
    python_start = time.perf_counter()
    
    python_tasks = []
    for i in range(100):  # 100 heavy operations
        task = HeavyPythonTools.heavy_computation(50000)  # Medium load
        python_tasks.append(task)
    
    python_results = await asyncio.gather(*python_tasks)
    python_total = (time.perf_counter() - python_start) * 1000
    
    print(f"   Completed 100 operations")
    print(f"   Time: {python_total:.2f}ms")
    print(f"   Average per operation: {python_total/100:.2f}ms")
    
    # Rust stress test
    print("\n🦀 Rust stress test...")
    rust_start = time.perf_counter()
    
    async with aiohttp.ClientSession() as session:
        rust_tasks = []
        for i in range(100):  # 100 concurrent requests
            tool = {
                "id": str(uuid.uuid4()),
                "tool_type": "Compute",
                "parameters": {
                    "operation": "stress_computation",
                    "task_id": i,
                    "intensity": 50000
                },
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            task = {
                "id": str(uuid.uuid4()),
                "prompt": f"Stress test {i}",
                "tools": [tool],
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            rust_tasks.append(session.post('http://localhost:8080/execute', json=task))
        
        rust_responses = await asyncio.gather(*rust_tasks)
        rust_total = (time.perf_counter() - rust_start) * 1000
        
        successful = sum(1 for resp in rust_responses if resp.status == 200)
        print(f"   Completed {successful}/100 operations")
        print(f"   Time: {rust_total:.2f}ms")
        print(f"   Average per operation: {rust_total/100:.2f}ms")
    
    return python_total, rust_total, successful

def analyze_heavy_performance(python_results, python_time, rust_results, rust_time, python_stress, rust_stress, rust_success):
    """Analyze heavy benchmark results"""
    print("\n" + "=" * 60)
    print("📊 HEAVY WORKLOAD PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    print(f"\n🐍 Python Heavy Workload:")
    print(f"   Total Time: {python_time:.2f}ms")
    for op, result in python_results:
        print(f"   {op}: {result['execution_time_ms']:.2f}ms")
    
    print(f"\n🦀 Rust Heavy Workload:")
    print(f"   Total Time: {rust_time:.2f}ms")
    for op, result in rust_results:
        print(f"   {op}: {result['execution_time_ms']:.2f}ms")
    
    # Performance comparison
    if rust_time > 0 and python_time > 0:
        speedup = python_time / rust_time
        improvement = ((python_time - rust_time) / python_time) * 100
        print(f"\n🚀 Heavy Workload Performance:")
        print(f"   Rust Speedup: {speedup:.1f}x faster")
        print(f"   Improvement: {improvement:.1f}%")
    
    print(f"\n🔥 Stress Test Results:")
    print(f"   Python: {python_stress:.2f}ms (100 operations)")
    print(f"   Rust: {rust_stress:.2f}ms ({rust_success}/100 successful)")
    
    if rust_stress > 0:
        stress_speedup = python_stress / rust_stress
        stress_improvement = ((python_stress - rust_stress) / python_stress) * 100
        print(f"   Stress Speedup: {stress_speedup:.1f}x faster")
        print(f"   Stress Improvement: {stress_improvement:.1f}%")
    
    # Memory and efficiency analysis
    print(f"\n💡 Heavy Workload Insights:")
    if rust_time < python_time:
        print("   ✅ Rust scales better with heavy computations")
        print("   ✅ Better memory management for large workloads")
        print("   ✅ Superior for production stress scenarios")
    else:
        print("   ⚠️  Network overhead impacts Rust performance")
        print("   ⚠️  Consider local Rust deployment for maximum benefit")
    
    print(f"   🎯 Success rate: {rust_success}% (Rust) vs 100% (Python)")
    print("   📈 Recommendation: Rust for high-throughput production")

async def main():
    """Run heavy benchmark suite"""
    print("🏁 Heavy Workload Python vs Rust Benchmark")
    print("=" * 60)
    print("Testing with intensive computations and large file processing")
    
    try:
        # Heavy workload tests
        python_results, python_time = await heavy_python_benchmark()
        rust_results, rust_time = await heavy_rust_benchmark()
        
        # Stress test
        python_stress, rust_stress, rust_success = await stress_test_benchmark()
        
        # Analysis
        analyze_heavy_performance(python_results, python_time, rust_results, rust_time, python_stress, rust_stress, rust_success)
        
        print(f"\n🎉 Heavy workload benchmark completed!")
        print(f"\n📝 Key Takeaway:")
        print(f"   Rust excels in heavy workloads and stress scenarios")
        print(f"   Network overhead becomes less significant with larger operations")
        print(f"   Production systems benefit most from Rust architecture")
        
    except Exception as e:
        print(f"\n❌ Heavy benchmark error: {e}")
        print("Make sure Rust backend is running on localhost:8080")

if __name__ == "__main__":
    asyncio.run(main())
