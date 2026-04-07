use crate::types::{ToolRequest, ToolResponse, ToolType};
use crate::tools::Tool;
use async_trait::async_trait;
use reqwest;
use std::time::Instant;

pub struct HttpTool;

#[async_trait]
impl Tool for HttpTool {
    async fn execute(&self, request: &ToolRequest) -> anyhow::Result<ToolResponse> {
        let start = Instant::now();
        
        let url = request.parameters.get("url")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("Missing 'url' parameter"))?;
            
        let method = request.parameters.get("method")
            .and_then(|v| v.as_str())
            .unwrap_or("GET");
            
        let client = reqwest::Client::new();
        let req_builder = match method {
            "GET" => client.get(url),
            "POST" => {
                if let Some(body) = request.parameters.get("body") {
                    client.post(url).json(body)
                } else {
                    client.post(url)
                }
            },
            _ => return Err(anyhow::anyhow!("Unsupported HTTP method: {}", method))
        };
        
        let response = req_builder.send().await?;
        let status = response.status();
        let response_text = response.text().await?;
        
        let result = serde_json::json!({
            "status": status.as_u16(),
            "response": response_text
        });
        
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
        ToolType::Http
    }
    
    fn name(&self) -> &'static str {
        "http"
    }
}
