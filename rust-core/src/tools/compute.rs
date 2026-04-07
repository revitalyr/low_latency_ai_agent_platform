use crate::types::{ToolRequest, ToolResponse, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use std::time::Instant;

pub struct ComputeTool;

#[async_trait]
impl Tool for ComputeTool {
    async fn execute(&self, request: &ToolRequest) -> anyhow::Result<ToolResponse> {
        let start = Instant::now();
        
        let operation = request.parameters.get("operation")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("Missing 'operation' parameter"))?;
            
        let result = match operation {
            "add" => {
                let a = request.parameters.get("a")
                    .and_then(|v| v.as_f64())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'a' parameter"))?;
                let b = request.parameters.get("b")
                    .and_then(|v| v.as_f64())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'b' parameter"))?;
                serde_json::json!(a + b)
            },
            "multiply" => {
                let a = request.parameters.get("a")
                    .and_then(|v| v.as_f64())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'a' parameter"))?;
                let b = request.parameters.get("b")
                    .and_then(|v| v.as_f64())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'b' parameter"))?;
                serde_json::json!(a * b)
            },
            "percentage_change" => {
                let old = request.parameters.get("old")
                    .and_then(|v| v.as_f64())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'old' parameter"))?;
                let new = request.parameters.get("new")
                    .and_then(|v| v.as_f64())
                    .ok_or_else(|| anyhow::anyhow!("Missing 'new' parameter"))?;
                let change = ((new - old) / old) * 100.0;
                serde_json::json!({
                    "percentage_change": change,
                    "direction": if change > 0.0 { "up" } else if change < 0.0 { "down" } else { "flat" }
                })
            },
            _ => return Err(anyhow::anyhow!("Unsupported compute operation: {}", operation))
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
        ToolType::Compute
    }
    
    fn name(&self) -> &'static str {
        "compute"
    }
}
