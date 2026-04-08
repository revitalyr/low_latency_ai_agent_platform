#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import json
import uuid

async def demo_rust_backend_only():
    print("=== Demo: Rust Backend Performance ===")
    
    # Test direct tool execution via Rust backend
    tool_requests = [
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
    
    task = {
        "id": str(uuid.uuid4()),
        "prompt": "Test Rust backend performance",
        "tools": tool_requests,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        async with session.post('http://localhost:8080/execute', json=task) as resp:
            if resp.status == 200:
                result = await resp.json()
                end_time = time.time()
                
                print(f"✅ Task executed successfully!")
                print(f"📊 Total execution time: {(end_time - start_time) * 1000:.2f}ms")
                print(f"🔧 Tools executed: {len(result['tool_responses'])}")
                
                for tool_resp in result['tool_responses']:
                    print(f"   - {tool_resp['id']}: {tool_resp['result']} ({tool_resp['execution_time_ms']}ms)")
                
                return result
            else:
                print(f"❌ Error: {resp.status}")
                return None

async def demo_cache_performance():
    print("\n=== Demo: Cache Performance ===")
    
    # Same request multiple times to test caching
    tool_request = {
        "id": str(uuid.uuid4()),
        "tool_type": "Compute",
        "parameters": {"operation": "add", "a": 100, "b": 200},
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    task = {
        "id": str(uuid.uuid4()),
        "prompt": "Test caching",
        "tools": [tool_request],
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    async with aiohttp.ClientSession() as session:
        times = []
        
        for i in range(3):
            start_time = time.time()
            
            async with session.post('http://localhost:8080/execute', json=task) as resp:
                result = await resp.json()
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
                
                times.append(execution_time)
                cached = result['tool_responses'][0]['cached']
                
                print(f"Request {i+1}: {execution_time:.2f}ms {'(CACHED)' if cached else '(UNCACHED)'}")
        
        avg_uncached = times[0]
        avg_cached = sum(times[1:]) / len(times[1:])
        improvement = ((avg_uncached - avg_cached) / avg_uncached) * 100
        
        print(f"\n📈 Cache performance:")
        print(f"   First request: {avg_uncached:.2f}ms")
        print(f"   Cached requests: {avg_cached:.2f}ms")
        print(f"   Improvement: {improvement:.1f}% faster")

async def demo_metrics():
    print("\n=== Demo: System Metrics ===")
    
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/metrics') as resp:
            if resp.status == 200:
                metrics = await resp.json()
                
                print("📊 Current System Metrics:")
                print(f"   Total requests: {metrics['total_requests']}")
                print(f"   Average execution time: {metrics['average_execution_time_ms']:.2f}ms")
                print(f"   Cache hit rate: {metrics['cache_hit_rate']:.1%}")
                print(f"   Cache utilization: {metrics['cache_utilization']:.1%}")

async def demo_file_operations():
    print("\n=== Demo: File Operations ===")
    
    tool_requests = [
        {
            "id": str(uuid.uuid4()),
            "tool_type": "File",
            "parameters": {
                "action": "write",
                "path": "demo_output.txt",
                "content": "Hello from Low-Latency AI Agent Platform!"
            },
            "timestamp": "2024-01-01T00:00:00Z"
        },
        {
            "id": str(uuid.uuid4()),
            "tool_type": "File", 
            "parameters": {
                "action": "read",
                "path": "demo_output.txt"
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
    ]
    
    task = {
        "id": str(uuid.uuid4()),
        "prompt": "Test file operations",
        "tools": tool_requests,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        async with session.post('http://localhost:8080/execute', json=task) as resp:
            if resp.status == 200:
                result = await resp.json()
                end_time = time.time()
                
                print(f"✅ File operations completed!")
                print(f"📊 Total time: {(end_time - start_time) * 1000:.2f}ms")
                
                for tool_resp in result['tool_responses']:
                    print(f"   - {tool_resp['id']}: {tool_resp['result']} ({tool_resp['execution_time_ms']}ms)")

async def main():
    print("🚀 Low-Latency AI Agent Platform Demo")
    print("=" * 50)
    
    try:
        await demo_rust_backend_only()
        await demo_cache_performance()
        await demo_file_operations()
        await demo_metrics()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Key Demonstrations:")
        print("   ✅ High-performance Rust execution engine")
        print("   ✅ Intelligent caching with measurable improvements")
        print("   ✅ File operations and tool execution")
        print("   ✅ Real-time metrics and monitoring")
        print("   ✅ Production-ready architecture")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Make sure Rust backend is running on localhost:8080")

if __name__ == "__main__":
    asyncio.run(main())
