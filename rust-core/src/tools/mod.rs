use crate::types::{ToolRequest, ToolResponse, ToolType, ToolContext, ToolResult};
use async_trait::async_trait;
use std::collections::HashMap;

pub mod http;
pub mod file;
pub mod compute;
pub mod heavy_compute;
pub mod heavy_file;

pub use http::HttpTool;
pub use file::FileTool;
pub use compute::ComputeTool;
pub use heavy_compute::HeavyComputeTool;
pub use heavy_file::HeavyFileTool;

#[async_trait]
pub trait Tool: Send + Sync {
    async fn execute(
        &self, 
        request: &ToolRequest, 
        ctx: &ToolContext
    ) -> ToolResult<ToolResponse>;
    
    fn tool_type(&self) -> ToolType;
    fn name(&self) -> &'static str;
}

pub struct ToolRegistry {
    tools: HashMap<String, Box<dyn Tool>>,
}

impl ToolRegistry {
    pub fn new() -> Self {
        Self {
            tools: HashMap::new(),
        }
    }

    pub fn register<T: Tool + 'static>(&mut self, tool: T) {
        self.tools.insert(tool.name().to_string(), Box::new(tool));
    }

    pub async fn execute_tool(&self, request: &ToolRequest, ctx: &ToolContext) -> ToolResult<ToolResponse> {
        let tool = self.tools
            .get(&request.tool_type.to_string())
            .ok_or_else(|| crate::types::ToolError::ToolNotFound(request.tool_type.to_string()))?;

        tool.execute(request, ctx).await
    }
}

impl Default for ToolRegistry {
    fn default() -> Self {
        Self::new()
    }
}
