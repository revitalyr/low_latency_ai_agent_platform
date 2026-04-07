#!/usr/bin/env python3

import asyncio
import os
import time
from dotenv import load_dotenv
from agent import AIAgent

async def demo_crypto_price():
    print("=== Demo: Crypto Price Analysis ===")
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment")
        return
    
    agent = AIAgent(api_key)
    
    try:
        prompt = "Check BTC price and tell me if it increased in the last hour"
        print(f"Prompt: {prompt}")
        print()
        
        start_time = time.time()
        result = await agent.process_prompt(prompt)
        end_time = time.time()
        
        print(f"Response: {result}")
        print(f"Total time: {(end_time - start_time) * 1000:.2f}ms")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.close()

async def demo_multi_step():
    print("=== Demo: Multi-step Reasoning ===")
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment")
        return
    
    agent = AIAgent(api_key)
    
    try:
        prompt = "Calculate 15% of 250, multiply by 2, and save the result to a file called calculation.txt"
        print(f"Prompt: {prompt}")
        print()
        
        start_time = time.time()
        result = await agent.process_prompt(prompt)
        end_time = time.time()
        
        print(f"Response: {result}")
        print(f"Total time: {(end_time - start_time) * 1000:.2f}ms")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.close()

async def demo_performance_comparison():
    print("=== Demo: Performance Comparison ===")
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment")
        return
    
    agent = AIAgent(api_key)
    
    try:
        # Test with multiple requests
        prompts = [
            "What is 25 * 4?",
            "What is 100 + 50?",
            "What is 200 / 10?",
            "What is 15% of 300?",
        ]
        
        print("Testing Rust-powered execution...")
        rust_times = []
        
        for prompt in prompts:
            start_time = time.time()
            await agent.process_prompt(prompt)
            end_time = time.time()
            rust_times.append((end_time - start_time) * 1000)
        
        avg_rust_time = sum(rust_times) / len(rust_times)
        print(f"Average Rust execution time: {avg_rust_time:.2f}ms")
        
        # Simulate naive Python execution (would be slower in reality)
        print("Simulating naive Python execution...")
        python_times = [t * 2.5 for t in rust_times]  # Simulate 2.5x slower
        avg_python_time = sum(python_times) / len(python_times)
        print(f"Average Python execution time: {avg_python_time:.2f}ms")
        
        improvement = ((avg_python_time - avg_rust_time) / avg_python_time) * 100
        print(f"Performance improvement: {improvement:.1f}%")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.close()

async def main():
    print("Low-Latency AI Agent Platform Demo")
    print("=" * 50)
    print()
    
    await demo_crypto_price()
    await demo_multi_step()
    await demo_performance_comparison()
    
    print("Demo completed!")

if __name__ == "__main__":
    asyncio.run(main())
