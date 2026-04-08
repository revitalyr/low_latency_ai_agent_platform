use crate::types::{ToolRequest, ToolResponse, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::time::Instant;

/// High-performance execution engine for AI agent tools
/// 
/// This component handles the orchestration and execution of tool requests,
/// providing async execution capabilities and performance tracking.
pub struct ExecutionEngine {
    /// Start time of the execution engine
    start_time: Instant,
}

impl ExecutionEngine {
    /// Creates a new execution engine instance
    /// 
    /// # Returns
    /// 
    /// A new ExecutionEngine with initialized start time
    pub fn new() -> Self {
        Self {
            start_time: Instant::now(),
        }
    }

    /// Executes a batch of tool requests using the provided tool registry
    /// 
    /// # Arguments
    /// 
    /// * `tool_requests` - Vector of tool requests to execute
    /// * `tool_registry` - Registry containing available tools
    /// 
    /// # Returns
    /// 
    /// Result containing vector of tool responses or error
    /// 
    /// # Performance Notes
    /// 
    /// This method executes tools sequentially but could be enhanced
    /// for parallel execution in future versions.
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
