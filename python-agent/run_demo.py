#!/usr/bin/env python3
"""
Simplified Python Agent for Low-Latency AI Agent Platform
Principal-level optimization: Clean, minimal, focused
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class Agent:
    """Simplified AI Agent - Principal level design"""
    
    def __init__(self, client_url: str = "http://127.0.0.1:8080"):
        self.client_url = client_url
        self.session = None
    
    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def run(self, user_input: str) -> Dict[str, Any]:
        """Execute user request with minimal overhead"""
        await self._ensure_session()
        
        # Simple LLM simulation - in production, use real LLM
        if "http" in user_input.lower():
            plan = [
                {"tool": "http", "input": {"url": "https://httpbin.org/get", "method": "GET"}}
            ]
        elif "compute" in user_input.lower():
            plan = [
                {"tool": "compute", "input": {"operation": "add", "a": 10, "b": 20}}
            ]
        elif "file" in user_input.lower():
            plan = [
                {"tool": "file", "input": {"action": "read", "path": "demo.txt"}}
            ]
        else:
            plan = []
        
        print(f"🧠 Thought: {json.dumps(plan, indent=2)}")
        
        # Execute plan
        if plan:
            task = {
                "id": "demo-task",
                "prompt": user_input,
                "tools": plan
            }
            
            async with self.session.post(
                f"{self.client_url}/execute",
                json=task
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"🎯 Observation: {json.dumps(result, indent=2)}")
                    return result
                else:
                    print(f"❌ Error: {response.status}")
                    return {"error": f"HTTP {response.status}"}
        
        return {"result": "No tools executed"}
    
    async def close(self):
        if self.session:
            await self.session.close()

async def main():
    """Simple demo - Principal level clarity"""
    agent = Agent()
    
    try:
        # Demo requests
        requests = [
            "Make HTTP request to httpbin.org",
            "Compute 10 + 20", 
            "Read demo.txt file"
        ]
        
        for req in requests:
            print(f"\n🚀 Request: {req}")
            result = await agent.run(req)
            print(f"✅ Result: {result.get('result', 'No result')}")
        
        print("\n🎊 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
