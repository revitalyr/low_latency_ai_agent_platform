use crate::types::{ToolRequest, ToolResponse, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::time::Instant;

pub struct ExecutionEngine {
    start_time: Instant,
}

impl ExecutionEngine {
    pub fn new() -> Self {
        Self {
            start_time: Instant::now(),
        }
    }

    pub async fn execute_task(
        &self,
        tool_requests: Vec<ToolRequest>,
        tool_registry: &crate::tools::ToolRegistry,
    ) -> anyhow::Result<Vec<ToolResponse>> {
        let mut responses = Vec::new();
        
        for request in tool_requests {
            let start = Instant::now();
            let response = tool_registry.execute_tool(&request).await?;
            let execution_time = start.elapsed().as_millis() as u64;
            
            tracing::info!(
                tool_type = ?request.tool_type,
                execution_time_ms = execution_time,
                cached = response.cached,
                "Tool executed"
            );
            
            responses.push(response);
        }
        
        Ok(responses)
    }
}

impl Default for ExecutionEngine {
    fn default() -> Self {
        Self::new()
    }
}
