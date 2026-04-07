use crate::types::{ToolRequest, ToolResponse, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::fs;
use std::time::Instant;

pub struct FileTool;

#[async_trait]
impl Tool for FileTool {
    async fn execute(&self, request: &ToolRequest) -> anyhow::Result<ToolResponse> {
        let start = Instant::now();
        
        let action = request.parameters.get("action")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("Missing 'action' parameter"))?;
            
        let path = request.parameters.get("path")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("Missing 'path' parameter"))?;
            
        let result = match action {
            "read" => {
                let content = fs::read_to_string(path)?;
                serde_json::json!({
                    "content": content,
                    "size": content.len()
                })
            },
            "write" => {
                let content = request.parameters.get("content")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'content' parameter for write"))?;
                fs::write(path, content)?;
                serde_json::json!({
                    "written": true,
                    "size": content.len()
                })
            },
            _ => return Err(anyhow::anyhow!("Unsupported file action: {}", action))
        };
        
        let execution_time = start.elapsed().as_millis() as u64;
        
        Ok(ToolResponse {
            id: request.id,
            result,
            execution_time_ms: execution_time,
            cached: false,
            timestamp: chrono::Utc::now(),
        })
    }
    
    fn tool_type(&self) -> ToolType {
        ToolType::File
    }
    
    fn name(&self) -> &'static str {
        "file"
    }
}
