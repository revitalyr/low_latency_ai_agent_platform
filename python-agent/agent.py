import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pydantic import BaseModel
import structlog
from openai import AsyncOpenAI

logger = structlog.get_logger()

@dataclass
class ToolRequest:
    id: str
    tool_type: str
    parameters: Dict[str, Any]
    timestamp: str

@dataclass  
class ToolResponse:
    id: str
    result: Dict[str, Any]
    execution_time_ms: int
    cached: bool
    timestamp: str

@dataclass
class AgentTask:
    id: str
    prompt: str
    tools: List[ToolRequest]
    timestamp: str

@dataclass
class AgentResponse:
    id: str
    result: str
    tool_responses: List[ToolResponse]
    total_execution_time_ms: int
    timestamp: str

class RustCoreClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = None

    async def _get_session(self):
        if self.session is None:
            import aiohttp
            self.session = aiohttp.ClientSession()
        return self.session

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        session = await self._get_session()
        
        payload = {
            "id": task.id,
            "prompt": task.prompt,
            "tools": [
                {
                    "id": t.id,
                    "tool_type": t.tool_type,
                    "parameters": t.parameters,
                    "timestamp": t.timestamp
                } for t in task.tools
            ],
            "timestamp": task.timestamp
        }
        
        start_time = time.time()
        async with session.post(f"{self.base_url}/execute", json=payload) as resp:
            response_data = await resp.json()
        
        tool_responses = [
            ToolResponse(
                id=t["id"],
                result=t["result"],
                execution_time_ms=t["execution_time_ms"],
                cached=t["cached"],
                timestamp=t["timestamp"]
            ) for t in response_data["tool_responses"]
        ]
        
        return AgentResponse(
            id=response_data["id"],
            result=response_data["result"],
            tool_responses=tool_responses,
            total_execution_time_ms=response_data["total_execution_time_ms"],
            timestamp=response_data["timestamp"]
        )

    async def close(self):
        if self.session:
            await self.session.close()

class AIAgent:
    def __init__(self, openai_api_key: str, rust_core_url: str = "http://localhost:8080"):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.rust_client = RustCoreClient(rust_core_url)
        
    async def process_prompt(self, prompt: str) -> str:
        logger.info("Processing prompt", prompt=prompt)
        
        tool_requests = await self._plan_tools(prompt)
        
        task = AgentTask(
            id=f"task_{int(time.time())}",
            prompt=prompt,
            tools=tool_requests,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
        
        response = await self.rust_client.execute_task(task)
        
        final_result = await self._synthesize_result(prompt, response)
        
        logger.info(
            "Task completed",
            total_time_ms=response.total_execution_time_ms,
            tools_executed=len(response.tool_responses)
        )
        
        return final_result
    
    async def _plan_tools(self, prompt: str) -> List[ToolRequest]:
        system_prompt = """
        You are an AI agent that can use tools to complete tasks. Available tools:
        1. HTTP tool - make HTTP requests (url, method, body)
        2. File tool - read/write files (action: read/write, path, content)
        3. Compute tool - perform calculations (operation: add/multiply/percentage_change, a, b, old, new)
        
        Analyze the prompt and determine which tools are needed. Return as JSON list.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Plan tools for: {prompt}"}
            ],
            response_format={"type": "json_object"}
        )
        
        tools_plan = json.loads(response.choices[0].message.content)
        tool_requests = []
        
        for i, tool in enumerate(tools_plan.get("tools", [])):
            tool_requests.append(ToolRequest(
                id=f"tool_{int(time.time())}_{i}",
                tool_type=tool["type"],
                parameters=tool["parameters"],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            ))
        
        return tool_requests
    
    async def _synthesize_result(self, prompt: str, response: AgentResponse) -> str:
        tool_results = []
        for tool_resp in response.tool_responses:
            tool_results.append(f"Tool {tool_resp.id}: {tool_resp.result}")
        
        system_prompt = """
        You are an AI assistant that received results from tool executions.
        Synthesize these results into a coherent answer to the user's original prompt.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original prompt: {prompt}\n\nTool results:\n" + "\n".join(tool_results)}
            ]
        )
        
        return response.choices[0].message.content

    async def close(self):
        await self.rust_client.close()
